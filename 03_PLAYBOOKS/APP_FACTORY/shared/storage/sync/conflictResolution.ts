/**
 * Conflict Resolution - Strategies for handling sync conflicts
 *
 * When local and server data diverge, these strategies determine
 * how to merge or choose between them.
 */

// Types
export enum ConflictType {
  /** Both client and server modified the same field */
  FIELD_COLLISION = 'FIELD_COLLISION',
  /** Client tried to update deleted server record */
  UPDATE_DELETED = 'UPDATE_DELETED',
  /** Client tried to delete modified server record */
  DELETE_MODIFIED = 'DELETE_MODIFIED',
  /** Client created record with same ID as server */
  DUPLICATE_CREATE = 'DUPLICATE_CREATE',
  /** Server version is newer than client version */
  VERSION_MISMATCH = 'VERSION_MISMATCH',
}

export enum ConflictResolution {
  /** Server data wins, discard client changes */
  SERVER_WINS = 'SERVER_WINS',
  /** Client data wins, overwrite server */
  CLIENT_WINS = 'CLIENT_WINS',
  /** Merge both, client fields take precedence on collision */
  MERGE_CLIENT_PRIORITY = 'MERGE_CLIENT_PRIORITY',
  /** Merge both, server fields take precedence on collision */
  MERGE_SERVER_PRIORITY = 'MERGE_SERVER_PRIORITY',
  /** Use most recent timestamp */
  LATEST_WINS = 'LATEST_WINS',
  /** Keep both versions (create duplicate) */
  KEEP_BOTH = 'KEEP_BOTH',
  /** Manual resolution required */
  MANUAL = 'MANUAL',
}

export interface ConflictContext {
  entityType: string;
  entityId: string;
  conflictType: ConflictType;
  clientData: Record<string, unknown>;
  serverData: Record<string, unknown>;
  clientTimestamp: string;
  serverTimestamp?: string;
}

export interface ResolvedConflict {
  resolved: boolean;
  data?: Record<string, unknown>;
  action: 'apply' | 'discard' | 'duplicate' | 'manual';
  message?: string;
}

export type ConflictHandler = (context: ConflictContext) => Promise<ResolvedConflict>;

/**
 * Conflict Resolver class
 */
export class ConflictResolver {
  private defaultStrategy: ConflictResolution = ConflictResolution.SERVER_WINS;
  private entityStrategies: Map<string, ConflictResolution> = new Map();
  private customHandlers: Map<string, ConflictHandler> = new Map();

  /**
   * Set default resolution strategy
   */
  setDefaultStrategy(strategy: ConflictResolution): void {
    this.defaultStrategy = strategy;
  }

  /**
   * Set strategy for specific entity type
   */
  setEntityStrategy(entityType: string, strategy: ConflictResolution): void {
    this.entityStrategies.set(entityType, strategy);
  }

  /**
   * Register custom handler for specific entity type
   */
  registerHandler(entityType: string, handler: ConflictHandler): void {
    this.customHandlers.set(entityType, handler);
  }

  /**
   * Resolve a conflict
   */
  resolve(
    clientData: Record<string, unknown>,
    serverData: Record<string, unknown>,
    conflictType: ConflictType,
    strategy?: ConflictResolution,
    entityType?: string
  ): Record<string, unknown> | null {
    const effectiveStrategy = strategy ?? this.entityStrategies.get(entityType ?? '') ?? this.defaultStrategy;

    switch (effectiveStrategy) {
      case ConflictResolution.SERVER_WINS:
        return serverData;

      case ConflictResolution.CLIENT_WINS:
        return clientData;

      case ConflictResolution.MERGE_CLIENT_PRIORITY:
        return this.mergeData(serverData, clientData);

      case ConflictResolution.MERGE_SERVER_PRIORITY:
        return this.mergeData(clientData, serverData);

      case ConflictResolution.LATEST_WINS:
        return this.resolveByTimestamp(clientData, serverData);

      case ConflictResolution.KEEP_BOTH:
        // Return client data with modified ID
        return {
          ...clientData,
          _id: `${clientData._id ?? clientData.id}_conflict_${Date.now()}`,
          _conflictOf: clientData._id ?? clientData.id,
        };

      case ConflictResolution.MANUAL:
        // Return null to indicate manual resolution needed
        return null;

      default:
        return serverData;
    }
  }

  /**
   * Resolve conflict asynchronously (for custom handlers)
   */
  async resolveAsync(context: ConflictContext): Promise<ResolvedConflict> {
    // Check for custom handler
    const handler = this.customHandlers.get(context.entityType);
    if (handler) {
      return handler(context);
    }

    // Use standard resolution
    const strategy = this.entityStrategies.get(context.entityType) ?? this.defaultStrategy;
    const data = this.resolve(
      context.clientData,
      context.serverData,
      context.conflictType,
      strategy,
      context.entityType
    );

    if (data === null) {
      return {
        resolved: false,
        action: 'manual',
        message: 'Manual resolution required',
      };
    }

    return {
      resolved: true,
      data,
      action: 'apply',
    };
  }

  /**
   * Detect conflict type between client and server data
   */
  detectConflictType(
    clientData: Record<string, unknown>,
    serverData: Record<string, unknown> | null,
    operation: 'CREATE' | 'UPDATE' | 'DELETE'
  ): ConflictType | null {
    // No server data means no conflict for CREATE
    if (!serverData && operation === 'CREATE') {
      return null;
    }

    // Server deleted the record we're trying to update
    if (!serverData && operation === 'UPDATE') {
      return ConflictType.UPDATE_DELETED;
    }

    // Trying to delete but server has modified
    if (serverData && operation === 'DELETE') {
      const clientVersion = clientData._version as number | undefined;
      const serverVersion = serverData._version as number | undefined;
      if (clientVersion && serverVersion && serverVersion > clientVersion) {
        return ConflictType.DELETE_MODIFIED;
      }
    }

    // Check version mismatch
    if (serverData) {
      const clientVersion = clientData._version as number | undefined;
      const serverVersion = serverData._version as number | undefined;
      if (clientVersion && serverVersion && serverVersion > clientVersion) {
        return ConflictType.VERSION_MISMATCH;
      }
    }

    // Check for duplicate create
    if (serverData && operation === 'CREATE') {
      return ConflictType.DUPLICATE_CREATE;
    }

    // Check for field collision
    if (serverData && operation === 'UPDATE') {
      const collisions = this.findFieldCollisions(clientData, serverData);
      if (collisions.length > 0) {
        return ConflictType.FIELD_COLLISION;
      }
    }

    return null;
  }

  /**
   * Find fields that both client and server modified
   */
  findFieldCollisions(
    clientData: Record<string, unknown>,
    serverData: Record<string, unknown>
  ): string[] {
    const collisions: string[] = [];
    const ignoredFields = ['_version', '_timestamp', '_syncedAt', 'updatedAt', 'updated_at'];

    for (const key of Object.keys(clientData)) {
      if (ignoredFields.includes(key)) continue;
      if (key in serverData && clientData[key] !== serverData[key]) {
        collisions.push(key);
      }
    }

    return collisions;
  }

  // Private methods

  private mergeData(
    base: Record<string, unknown>,
    override: Record<string, unknown>
  ): Record<string, unknown> {
    const merged: Record<string, unknown> = { ...base };

    for (const [key, value] of Object.entries(override)) {
      if (value !== undefined && value !== null) {
        if (typeof value === 'object' && !Array.isArray(value) && typeof merged[key] === 'object' && !Array.isArray(merged[key])) {
          // Deep merge objects
          merged[key] = this.mergeData(
            merged[key] as Record<string, unknown>,
            value as Record<string, unknown>
          );
        } else {
          merged[key] = value;
        }
      }
    }

    return merged;
  }

  private resolveByTimestamp(
    clientData: Record<string, unknown>,
    serverData: Record<string, unknown>
  ): Record<string, unknown> {
    const clientTime = this.extractTimestamp(clientData);
    const serverTime = this.extractTimestamp(serverData);

    if (!clientTime || !serverTime) {
      // Default to server if no timestamps
      return serverData;
    }

    return clientTime > serverTime ? clientData : serverData;
  }

  private extractTimestamp(data: Record<string, unknown>): Date | null {
    const timestampFields = ['_timestamp', 'updatedAt', 'updated_at', 'modifiedAt', 'modified_at'];

    for (const field of timestampFields) {
      if (data[field]) {
        const date = new Date(data[field] as string);
        if (!isNaN(date.getTime())) {
          return date;
        }
      }
    }

    return null;
  }
}

/**
 * Default conflict resolution strategies by entity type
 */
export const DefaultEntityStrategies: Record<string, ConflictResolution> = {
  user_preferences: ConflictResolution.CLIENT_WINS,
  streak_data: ConflictResolution.LATEST_WINS,
  favorites: ConflictResolution.MERGE_CLIENT_PRIORITY,
  achievements: ConflictResolution.MERGE_SERVER_PRIORITY,
  activity_log: ConflictResolution.CLIENT_WINS,
  cached_content: ConflictResolution.SERVER_WINS,
};

/**
 * Create a pre-configured conflict resolver
 */
export function createDefaultResolver(): ConflictResolver {
  const resolver = new ConflictResolver();
  resolver.setDefaultStrategy(ConflictResolution.SERVER_WINS);

  for (const [entityType, strategy] of Object.entries(DefaultEntityStrategies)) {
    resolver.setEntityStrategy(entityType, strategy);
  }

  return resolver;
}
