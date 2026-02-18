/**
 * conflictResolution.ts - Resolve sync conflicts between local and remote data
 */

// ============================================================================
// Types
// ============================================================================

export type ConflictResolutionStrategy =
  | 'client-wins'
  | 'server-wins'
  | 'latest-wins'
  | 'merge'
  | 'manual';

export interface ConflictResolutionConfig {
  strategy: ConflictResolutionStrategy;
  mergeFields?: string[];
  excludeFields?: string[];
  customMerge?: <T>(local: T, remote: T) => T;
}

export interface ConflictInfo<T> {
  field: string;
  localValue: unknown;
  remoteValue: unknown;
  localTimestamp?: number;
  remoteTimestamp?: number;
  resolved?: boolean;
  resolvedValue?: unknown;
}

export interface ConflictReport<T> {
  entity: {
    localId: string;
    remoteId: string;
  };
  conflicts: ConflictInfo<T>[];
  resolution: ConflictResolutionStrategy;
  result: T;
}

// ============================================================================
// Core Resolution Function
// ============================================================================

/**
 * Resolve conflict between local and remote entities
 */
export function resolveConflict<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  config: ConflictResolutionConfig
): T {
  const { strategy, mergeFields, excludeFields, customMerge } = config;

  switch (strategy) {
    case 'client-wins':
      return resolveClientWins(local, remote, excludeFields);

    case 'server-wins':
      return resolveServerWins(local, remote, excludeFields);

    case 'latest-wins':
      return resolveLatestWins(local, remote, excludeFields);

    case 'merge':
      return resolveMerge(local, remote, mergeFields, excludeFields);

    case 'manual':
      // Return remote by default for manual resolution
      // Caller should handle this case
      return remote;

    default:
      return customMerge ? customMerge(local, remote) : remote;
  }
}

// ============================================================================
// Resolution Strategies
// ============================================================================

/**
 * Client/local data wins
 */
function resolveClientWins<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  excludeFields?: string[]
): T {
  const result = { ...remote };

  for (const key of Object.keys(local)) {
    if (excludeFields?.includes(key)) continue;
    if (key.startsWith('_')) continue; // Skip internal fields
    result[key] = local[key];
  }

  return result as T;
}

/**
 * Server/remote data wins
 */
function resolveServerWins<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  excludeFields?: string[]
): T {
  const result = { ...local };

  for (const key of Object.keys(remote)) {
    if (excludeFields?.includes(key)) continue;
    if (key.startsWith('_')) continue;
    result[key] = remote[key];
  }

  return result as T;
}

/**
 * Most recently updated data wins
 */
function resolveLatestWins<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  excludeFields?: string[]
): T {
  const localUpdated = getTimestamp(local);
  const remoteUpdated = getTimestamp(remote);

  if (localUpdated >= remoteUpdated) {
    return resolveClientWins(local, remote, excludeFields);
  }

  return resolveServerWins(local, remote, excludeFields);
}

/**
 * Merge fields from both entities
 */
function resolveMerge<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  mergeFields?: string[],
  excludeFields?: string[]
): T {
  const result = { ...remote };

  // Use local values for specified merge fields
  if (mergeFields) {
    for (const field of mergeFields) {
      if (excludeFields?.includes(field)) continue;
      if (local[field] !== undefined) {
        result[field] = local[field];
      }
    }
  } else {
    // Default merge: use latest value for each field
    for (const key of Object.keys(local)) {
      if (excludeFields?.includes(key)) continue;
      if (key.startsWith('_')) continue;

      const localVal = local[key];
      const remoteVal = remote[key];

      // Prefer non-null/undefined values
      if (localVal !== null && localVal !== undefined) {
        if (remoteVal === null || remoteVal === undefined) {
          result[key] = localVal;
        }
      }

      // For arrays, merge unique items
      if (Array.isArray(localVal) && Array.isArray(remoteVal)) {
        result[key] = mergeArrays(localVal, remoteVal);
      }

      // For objects, deep merge
      if (isPlainObject(localVal) && isPlainObject(remoteVal)) {
        result[key] = deepMerge(localVal, remoteVal);
      }
    }
  }

  return result as T;
}

// ============================================================================
// Field-Level Resolution
// ============================================================================

/**
 * Detect conflicts between two entities
 */
export function detectConflicts<T extends Record<string, unknown>>(
  local: T,
  remote: T,
  excludeFields?: string[]
): ConflictInfo<T>[] {
  const conflicts: ConflictInfo<T>[] = [];
  const allKeys = new Set([...Object.keys(local), ...Object.keys(remote)]);

  for (const key of allKeys) {
    if (excludeFields?.includes(key)) continue;
    if (key.startsWith('_')) continue;

    const localValue = local[key];
    const remoteValue = remote[key];

    if (!isEqual(localValue, remoteValue)) {
      conflicts.push({
        field: key,
        localValue,
        remoteValue,
      });
    }
  }

  return conflicts;
}

/**
 * Resolve specific field conflict
 */
export function resolveFieldConflict<T>(
  field: string,
  localValue: T,
  remoteValue: T,
  strategy: ConflictResolutionStrategy
): T {
  switch (strategy) {
    case 'client-wins':
      return localValue;
    case 'server-wins':
      return remoteValue;
    case 'latest-wins':
      // Without timestamps, default to remote
      return remoteValue;
    default:
      return remoteValue;
  }
}

// ============================================================================
// Batch Resolution
// ============================================================================

/**
 * Resolve conflicts for multiple entities
 */
export function resolveConflictsBatch<T extends Record<string, unknown>>(
  pairs: { local: T; remote: T }[],
  config: ConflictResolutionConfig
): ConflictReport<T>[] {
  return pairs.map(({ local, remote }) => {
    const conflicts = detectConflicts(local, remote, config.excludeFields);
    const result = resolveConflict(local, remote, config);

    return {
      entity: {
        localId: String(local.id ?? 'unknown'),
        remoteId: String(remote.id ?? 'unknown'),
      },
      conflicts,
      resolution: config.strategy,
      result,
    };
  });
}

// ============================================================================
// Three-Way Merge
// ============================================================================

/**
 * Three-way merge using a common ancestor
 */
export function threeWayMerge<T extends Record<string, unknown>>(
  ancestor: T,
  local: T,
  remote: T,
  excludeFields?: string[]
): T {
  const result = { ...ancestor };

  const allKeys = new Set([
    ...Object.keys(ancestor),
    ...Object.keys(local),
    ...Object.keys(remote),
  ]);

  for (const key of allKeys) {
    if (excludeFields?.includes(key)) continue;
    if (key.startsWith('_')) continue;

    const ancestorVal = ancestor[key];
    const localVal = local[key];
    const remoteVal = remote[key];

    // Neither changed
    if (isEqual(localVal, ancestorVal) && isEqual(remoteVal, ancestorVal)) {
      result[key] = ancestorVal;
    }
    // Only local changed
    else if (!isEqual(localVal, ancestorVal) && isEqual(remoteVal, ancestorVal)) {
      result[key] = localVal;
    }
    // Only remote changed
    else if (isEqual(localVal, ancestorVal) && !isEqual(remoteVal, ancestorVal)) {
      result[key] = remoteVal;
    }
    // Both changed to same value
    else if (isEqual(localVal, remoteVal)) {
      result[key] = localVal;
    }
    // Both changed to different values - conflict
    else {
      // Default to remote, but this should be handled by caller
      result[key] = remoteVal;
    }
  }

  return result as T;
}

// ============================================================================
// Helpers
// ============================================================================

function getTimestamp(entity: Record<string, unknown>): number {
  const updatedAt = entity.updatedAt || entity.updated_at || entity.modifiedAt;
  if (typeof updatedAt === 'string') {
    return new Date(updatedAt).getTime();
  }
  if (typeof updatedAt === 'number') {
    return updatedAt;
  }
  return 0;
}

function isEqual(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (a === null || b === null) return false;
  if (typeof a !== typeof b) return false;

  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    return a.every((val, idx) => isEqual(val, b[idx]));
  }

  if (typeof a === 'object' && typeof b === 'object') {
    const aKeys = Object.keys(a as object);
    const bKeys = Object.keys(b as object);
    if (aKeys.length !== bKeys.length) return false;
    return aKeys.every((key) =>
      isEqual((a as Record<string, unknown>)[key], (b as Record<string, unknown>)[key])
    );
  }

  return false;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value) &&
    Object.getPrototypeOf(value) === Object.prototype
  );
}

function mergeArrays<T>(arr1: T[], arr2: T[]): T[] {
  const seen = new Set<string>();
  const result: T[] = [];

  for (const item of [...arr1, ...arr2]) {
    const key = JSON.stringify(item);
    if (!seen.has(key)) {
      seen.add(key);
      result.push(item);
    }
  }

  return result;
}

function deepMerge(
  target: Record<string, unknown>,
  source: Record<string, unknown>
): Record<string, unknown> {
  const result = { ...target };

  for (const key of Object.keys(source)) {
    const targetVal = target[key];
    const sourceVal = source[key];

    if (isPlainObject(targetVal) && isPlainObject(sourceVal)) {
      result[key] = deepMerge(targetVal, sourceVal);
    } else if (Array.isArray(targetVal) && Array.isArray(sourceVal)) {
      result[key] = mergeArrays(targetVal, sourceVal);
    } else {
      result[key] = sourceVal;
    }
  }

  return result;
}

export default resolveConflict;
