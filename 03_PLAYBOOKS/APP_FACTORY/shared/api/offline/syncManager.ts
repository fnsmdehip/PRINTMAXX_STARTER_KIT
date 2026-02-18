/**
 * syncManager.ts - Sync data when back online
 *
 * Manages bidirectional sync between local and remote data.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';
import { offlineQueue } from './offlineQueue';
import { resolveConflict, ConflictResolutionStrategy } from './conflictResolution';

// ============================================================================
// Types
// ============================================================================

export interface SyncableEntity {
  id: string;
  updatedAt: string;
  version?: number;
  _localChanges?: LocalChange[];
  _syncStatus?: SyncStatus;
}

export interface LocalChange {
  field: string;
  oldValue: unknown;
  newValue: unknown;
  timestamp: number;
}

export type SyncStatus = 'synced' | 'pending' | 'conflict' | 'error';

export interface SyncResult<T> {
  success: boolean;
  synced: T[];
  conflicts: SyncConflict<T>[];
  errors: SyncError[];
}

export interface SyncConflict<T> {
  localEntity: T;
  remoteEntity: T;
  resolved?: T;
  resolution?: 'local' | 'remote' | 'merged';
}

export interface SyncError {
  entityId: string;
  error: string;
  timestamp: number;
}

export interface SyncConfig<T extends SyncableEntity> {
  entityName: string;
  storageKey: string;
  fetchRemote: () => Promise<T[]>;
  pushLocal: (entity: T) => Promise<T>;
  conflictStrategy?: ConflictResolutionStrategy;
  onSyncStart?: () => void;
  onSyncComplete?: (result: SyncResult<T>) => void;
  onConflict?: (conflict: SyncConflict<T>) => Promise<T>;
}

export interface SyncState {
  lastSyncAt: number | null;
  isSyncing: boolean;
  pendingCount: number;
  errorCount: number;
}

// ============================================================================
// SyncManager Class
// ============================================================================

class SyncManager<T extends SyncableEntity> {
  private config: SyncConfig<T>;
  private localEntities: Map<string, T> = new Map();
  private syncState: SyncState = {
    lastSyncAt: null,
    isSyncing: false,
    pendingCount: 0,
    errorCount: 0,
  };
  private listeners: Set<(state: SyncState) => void> = new Set();

  constructor(config: SyncConfig<T>) {
    this.config = {
      conflictStrategy: 'server-wins',
      ...config,
    };
  }

  // --------------------------------------------------------------------------
  // Initialization
  // --------------------------------------------------------------------------

  /**
   * Initialize sync manager
   */
  async initialize(): Promise<void> {
    await this.loadLocalEntities();
    this.updatePendingCount();

    // Setup network listener for auto-sync
    NetInfo.addEventListener((state) => {
      if (state.isConnected && this.syncState.pendingCount > 0) {
        this.sync();
      }
    });
  }

  // --------------------------------------------------------------------------
  // Local Operations
  // --------------------------------------------------------------------------

  /**
   * Get all local entities
   */
  getAll(): T[] {
    return Array.from(this.localEntities.values());
  }

  /**
   * Get entity by ID
   */
  getById(id: string): T | undefined {
    return this.localEntities.get(id);
  }

  /**
   * Save entity locally (and queue for sync)
   */
  async save(entity: T): Promise<T> {
    const existingEntity = this.localEntities.get(entity.id);

    // Track changes for conflict resolution
    const changes: LocalChange[] = [];
    if (existingEntity) {
      for (const key of Object.keys(entity)) {
        const oldValue = (existingEntity as Record<string, unknown>)[key];
        const newValue = (entity as Record<string, unknown>)[key];
        if (oldValue !== newValue && key !== '_localChanges' && key !== '_syncStatus') {
          changes.push({
            field: key,
            oldValue,
            newValue,
            timestamp: Date.now(),
          });
        }
      }
    }

    const updatedEntity: T = {
      ...entity,
      updatedAt: new Date().toISOString(),
      _localChanges: changes,
      _syncStatus: 'pending' as SyncStatus,
    };

    this.localEntities.set(entity.id, updatedEntity);
    await this.persistLocalEntities();
    this.updatePendingCount();
    this.notifyListeners();

    // Queue for sync
    await this.queueForSync(updatedEntity);

    return updatedEntity;
  }

  /**
   * Delete entity locally (and queue deletion for sync)
   */
  async delete(id: string): Promise<void> {
    const entity = this.localEntities.get(id);
    if (!entity) return;

    // Mark as deleted (soft delete for sync)
    const deletedEntity: T = {
      ...entity,
      _syncStatus: 'pending' as SyncStatus,
    };

    this.localEntities.delete(id);
    await this.persistLocalEntities();
    this.updatePendingCount();
    this.notifyListeners();

    // Queue deletion for sync
    await offlineQueue.enqueue(
      `/api/${this.config.entityName}/${id}`,
      {
        method: 'DELETE',
        priority: 'normal',
        metadata: { entityId: id, type: 'delete' },
      }
    );
  }

  // --------------------------------------------------------------------------
  // Sync Operations
  // --------------------------------------------------------------------------

  /**
   * Perform full sync
   */
  async sync(): Promise<SyncResult<T>> {
    if (this.syncState.isSyncing) {
      return {
        success: false,
        synced: [],
        conflicts: [],
        errors: [{ entityId: '', error: 'Sync already in progress', timestamp: Date.now() }],
      };
    }

    const netState = await NetInfo.fetch();
    if (!netState.isConnected) {
      return {
        success: false,
        synced: [],
        conflicts: [],
        errors: [{ entityId: '', error: 'No network connection', timestamp: Date.now() }],
      };
    }

    this.syncState.isSyncing = true;
    this.notifyListeners();
    this.config.onSyncStart?.();

    const result: SyncResult<T> = {
      success: true,
      synced: [],
      conflicts: [],
      errors: [],
    };

    try {
      // 1. Fetch remote entities
      const remoteEntities = await this.config.fetchRemote();
      const remoteMap = new Map(remoteEntities.map((e) => [e.id, e]));

      // 2. Find and resolve conflicts
      for (const [id, localEntity] of this.localEntities) {
        if (localEntity._syncStatus !== 'pending') continue;

        const remoteEntity = remoteMap.get(id);

        if (remoteEntity) {
          // Check for conflict
          const localUpdated = new Date(localEntity.updatedAt).getTime();
          const remoteUpdated = new Date(remoteEntity.updatedAt).getTime();

          if (remoteUpdated > localUpdated - 1000) { // 1 second tolerance
            // Potential conflict
            const conflict: SyncConflict<T> = {
              localEntity,
              remoteEntity,
            };

            // Try to resolve
            let resolved: T;
            if (this.config.onConflict) {
              resolved = await this.config.onConflict(conflict);
            } else {
              resolved = resolveConflict(localEntity, remoteEntity, {
                strategy: this.config.conflictStrategy!,
              });
            }

            conflict.resolved = resolved;
            result.conflicts.push(conflict);

            // Push resolved entity
            try {
              const synced = await this.config.pushLocal(resolved);
              this.localEntities.set(id, { ...synced, _syncStatus: 'synced' as SyncStatus });
              result.synced.push(synced);
            } catch (error) {
              result.errors.push({
                entityId: id,
                error: (error as Error).message,
                timestamp: Date.now(),
              });
            }
          } else {
            // No conflict, push local changes
            try {
              const synced = await this.config.pushLocal(localEntity);
              this.localEntities.set(id, { ...synced, _syncStatus: 'synced' as SyncStatus });
              result.synced.push(synced);
            } catch (error) {
              result.errors.push({
                entityId: id,
                error: (error as Error).message,
                timestamp: Date.now(),
              });
            }
          }
        } else {
          // New local entity, push to remote
          try {
            const synced = await this.config.pushLocal(localEntity);
            this.localEntities.set(id, { ...synced, _syncStatus: 'synced' as SyncStatus });
            result.synced.push(synced);
          } catch (error) {
            result.errors.push({
              entityId: id,
              error: (error as Error).message,
              timestamp: Date.now(),
            });
          }
        }
      }

      // 3. Pull new remote entities
      for (const [id, remoteEntity] of remoteMap) {
        if (!this.localEntities.has(id)) {
          this.localEntities.set(id, { ...remoteEntity, _syncStatus: 'synced' as SyncStatus });
          result.synced.push(remoteEntity);
        }
      }

      // 4. Persist and update state
      await this.persistLocalEntities();
      this.syncState.lastSyncAt = Date.now();
      this.syncState.errorCount = result.errors.length;

      result.success = result.errors.length === 0;
    } catch (error) {
      result.success = false;
      result.errors.push({
        entityId: '',
        error: (error as Error).message,
        timestamp: Date.now(),
      });
    } finally {
      this.syncState.isSyncing = false;
      this.updatePendingCount();
      this.notifyListeners();
      this.config.onSyncComplete?.(result);
    }

    return result;
  }

  /**
   * Force push all local changes
   */
  async forcePush(): Promise<SyncResult<T>> {
    const originalStrategy = this.config.conflictStrategy;
    this.config.conflictStrategy = 'client-wins';
    const result = await this.sync();
    this.config.conflictStrategy = originalStrategy;
    return result;
  }

  /**
   * Force pull all remote data
   */
  async forcePull(): Promise<SyncResult<T>> {
    const originalStrategy = this.config.conflictStrategy;
    this.config.conflictStrategy = 'server-wins';
    const result = await this.sync();
    this.config.conflictStrategy = originalStrategy;
    return result;
  }

  // --------------------------------------------------------------------------
  // State Management
  // --------------------------------------------------------------------------

  /**
   * Get current sync state
   */
  getState(): SyncState {
    return { ...this.syncState };
  }

  /**
   * Subscribe to state changes
   */
  subscribe(listener: (state: SyncState) => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(): void {
    const state = this.getState();
    this.listeners.forEach((listener) => listener(state));
  }

  private updatePendingCount(): void {
    this.syncState.pendingCount = Array.from(this.localEntities.values())
      .filter((e) => e._syncStatus === 'pending').length;
  }

  // --------------------------------------------------------------------------
  // Persistence
  // --------------------------------------------------------------------------

  private async persistLocalEntities(): Promise<void> {
    try {
      const data = Array.from(this.localEntities.entries());
      await AsyncStorage.setItem(this.config.storageKey, JSON.stringify(data));
    } catch (error) {
      console.error('Failed to persist local entities:', error);
    }
  }

  private async loadLocalEntities(): Promise<void> {
    try {
      const data = await AsyncStorage.getItem(this.config.storageKey);
      if (data) {
        const entries: [string, T][] = JSON.parse(data);
        this.localEntities = new Map(entries);
      }
    } catch (error) {
      console.error('Failed to load local entities:', error);
    }
  }

  // --------------------------------------------------------------------------
  // Queue Integration
  // --------------------------------------------------------------------------

  private async queueForSync(entity: T): Promise<void> {
    await offlineQueue.enqueue(
      `/api/${this.config.entityName}/${entity.id}`,
      {
        method: 'PUT',
        body: entity,
        priority: 'normal',
        metadata: { entityId: entity.id, type: 'update' },
      }
    );
  }
}

// ============================================================================
// Factory Function
// ============================================================================

export function createSyncManager<T extends SyncableEntity>(
  config: SyncConfig<T>
): SyncManager<T> {
  return new SyncManager(config);
}

export default SyncManager;
