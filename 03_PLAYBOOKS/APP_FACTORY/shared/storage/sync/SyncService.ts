/**
 * SyncService - Cloud synchronization with offline support
 *
 * Features:
 * - Offline-first architecture
 * - Background sync
 * - Conflict detection and resolution
 * - Retry with exponential backoff
 * - Network state awareness
 */

import NetInfo, { NetInfoState } from '@react-native-community/netinfo';
import { SyncQueueQueries, ActivityQueries } from '../database/queries';
import { ConflictResolution, ConflictResolver, ConflictType } from './conflictResolution';

// Types
export interface SyncConfig {
  baseUrl: string;
  authToken?: string;
  maxRetries?: number;
  batchSize?: number;
  syncIntervalMs?: number;
}

export interface SyncResult {
  success: boolean;
  synced: number;
  failed: number;
  conflicts: number;
  errors: SyncError[];
}

export interface SyncError {
  entityType: string;
  entityId: string;
  operation: string;
  error: string;
}

export interface SyncPayload {
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  entityType: string;
  entityId: string;
  data: Record<string, unknown>;
  clientTimestamp: string;
}

export interface ServerResponse {
  success: boolean;
  data?: Record<string, unknown>;
  serverTimestamp?: string;
  conflict?: {
    type: ConflictType;
    serverData: Record<string, unknown>;
  };
  error?: string;
}

export type SyncStatus = 'idle' | 'syncing' | 'offline' | 'error';

export interface SyncState {
  status: SyncStatus;
  lastSyncAt: string | null;
  pendingCount: number;
  failedCount: number;
  isOnline: boolean;
}

type SyncEventCallback = (state: SyncState) => void;

class SyncServiceClass {
  private config: SyncConfig | null = null;
  private isOnline = true;
  private isSyncing = false;
  private syncInterval: NodeJS.Timeout | null = null;
  private listeners: Set<SyncEventCallback> = new Set();
  private conflictResolver: ConflictResolver | null = null;
  private lastSyncAt: string | null = null;
  private unsubscribeNetInfo: (() => void) | null = null;

  /**
   * Initialize sync service
   */
  async init(config: SyncConfig): Promise<void> {
    this.config = {
      maxRetries: 3,
      batchSize: 10,
      syncIntervalMs: 30000, // 30 seconds
      ...config,
    };

    this.conflictResolver = new ConflictResolver();

    // Set up network monitoring
    this.unsubscribeNetInfo = NetInfo.addEventListener((state: NetInfoState) => {
      const wasOnline = this.isOnline;
      this.isOnline = state.isConnected ?? false;

      // If we just came online, trigger sync
      if (!wasOnline && this.isOnline) {
        this.sync();
      }

      this.notifyListeners();
    });

    // Get initial network state
    const netState = await NetInfo.fetch();
    this.isOnline = netState.isConnected ?? false;

    // Start periodic sync
    this.startPeriodicSync();
  }

  /**
   * Clean up resources
   */
  destroy(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }

    if (this.unsubscribeNetInfo) {
      this.unsubscribeNetInfo();
      this.unsubscribeNetInfo = null;
    }

    this.listeners.clear();
  }

  /**
   * Update auth token
   */
  setAuthToken(token: string): void {
    if (this.config) {
      this.config.authToken = token;
    }
  }

  /**
   * Queue a change for sync
   */
  async queueChange(
    operation: 'CREATE' | 'UPDATE' | 'DELETE',
    entityType: string,
    entityId: string,
    data: Record<string, unknown>,
    priority = 0
  ): Promise<boolean> {
    const payload: SyncPayload = {
      operation,
      entityType,
      entityId,
      data,
      clientTimestamp: new Date().toISOString(),
    };

    const result = await SyncQueueQueries.add(operation, entityType, entityId, payload, priority);

    this.notifyListeners();

    // Trigger immediate sync if online
    if (this.isOnline && !this.isSyncing) {
      this.sync();
    }

    return result;
  }

  /**
   * Main sync function
   */
  async sync(): Promise<SyncResult> {
    if (!this.config) {
      return { success: false, synced: 0, failed: 0, conflicts: 0, errors: [{ entityType: '', entityId: '', operation: '', error: 'Sync not initialized' }] };
    }

    if (!this.isOnline) {
      return { success: false, synced: 0, failed: 0, conflicts: 0, errors: [{ entityType: '', entityId: '', operation: '', error: 'Device is offline' }] };
    }

    if (this.isSyncing) {
      return { success: false, synced: 0, failed: 0, conflicts: 0, errors: [{ entityType: '', entityId: '', operation: '', error: 'Sync already in progress' }] };
    }

    this.isSyncing = true;
    this.notifyListeners();

    const result: SyncResult = {
      success: true,
      synced: 0,
      failed: 0,
      conflicts: 0,
      errors: [],
    };

    try {
      // Process sync queue
      const queueItems = await SyncQueueQueries.getNext(this.config.batchSize);

      for (const item of queueItems) {
        const payload: SyncPayload = JSON.parse(item.payload);

        try {
          const response = await this.sendToServer(payload);

          if (response.success) {
            await SyncQueueQueries.remove(item.id);
            result.synced++;
          } else if (response.conflict) {
            // Handle conflict
            const resolved = await this.handleConflict(
              payload,
              response.conflict.serverData,
              response.conflict.type
            );

            if (resolved) {
              await SyncQueueQueries.remove(item.id);
              result.conflicts++;
              result.synced++;
            } else {
              result.failed++;
              result.errors.push({
                entityType: item.entity_type,
                entityId: item.entity_id,
                operation: item.operation,
                error: 'Conflict could not be resolved',
              });
            }
          } else {
            await SyncQueueQueries.markAttempted(item.id, response.error);
            result.failed++;
            result.errors.push({
              entityType: item.entity_type,
              entityId: item.entity_id,
              operation: item.operation,
              error: response.error ?? 'Unknown error',
            });
          }
        } catch (error) {
          await SyncQueueQueries.markAttempted(
            item.id,
            error instanceof Error ? error.message : 'Unknown error'
          );
          result.failed++;
          result.errors.push({
            entityType: item.entity_type,
            entityId: item.entity_id,
            operation: item.operation,
            error: error instanceof Error ? error.message : 'Unknown error',
          });
        }
      }

      // Sync activity logs
      const activities = await ActivityQueries.getUnsynced(50);
      if (activities.length > 0) {
        try {
          const activityResponse = await this.syncActivities(activities);
          if (activityResponse.success) {
            await ActivityQueries.markSynced(activities.map((a) => a.id));
          }
        } catch {
          // Activity sync failure is non-critical
        }
      }

      this.lastSyncAt = new Date().toISOString();
      result.success = result.failed === 0;
    } catch (error) {
      result.success = false;
      result.errors.push({
        entityType: '',
        entityId: '',
        operation: '',
        error: error instanceof Error ? error.message : 'Sync failed',
      });
    } finally {
      this.isSyncing = false;
      this.notifyListeners();
    }

    return result;
  }

  /**
   * Force sync now
   */
  async forcSync(): Promise<SyncResult> {
    return this.sync();
  }

  /**
   * Get current sync state
   */
  async getState(): Promise<SyncState> {
    const pendingCount = await SyncQueueQueries.getCount();
    const failedCount = await SyncQueueQueries.getFailedCount();

    return {
      status: this.isSyncing ? 'syncing' : this.isOnline ? 'idle' : 'offline',
      lastSyncAt: this.lastSyncAt,
      pendingCount,
      failedCount,
      isOnline: this.isOnline,
    };
  }

  /**
   * Subscribe to sync state changes
   */
  subscribe(callback: SyncEventCallback): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  /**
   * Clear all pending sync items
   */
  async clearQueue(): Promise<void> {
    const items = await SyncQueueQueries.getNext(1000);
    for (const item of items) {
      await SyncQueueQueries.remove(item.id);
    }
    this.notifyListeners();
  }

  // Private methods

  private startPeriodicSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    this.syncInterval = setInterval(() => {
      if (this.isOnline && !this.isSyncing) {
        this.sync();
      }
    }, this.config?.syncIntervalMs ?? 30000);
  }

  private async notifyListeners(): Promise<void> {
    const state = await this.getState();
    this.listeners.forEach((callback) => callback(state));
  }

  private async sendToServer(payload: SyncPayload): Promise<ServerResponse> {
    if (!this.config?.baseUrl) {
      throw new Error('Sync not configured');
    }

    const endpoint = `${this.config.baseUrl}/sync/${payload.entityType}`;

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.authToken && { Authorization: `Bearer ${this.config.authToken}` }),
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.text();
      return {
        success: false,
        error: `HTTP ${response.status}: ${error}`,
      };
    }

    return response.json();
  }

  private async syncActivities(activities: Array<{ id: number; event_type: string; event_data: string | null; timestamp: string }>): Promise<{ success: boolean }> {
    if (!this.config?.baseUrl) {
      throw new Error('Sync not configured');
    }

    const response = await fetch(`${this.config.baseUrl}/analytics/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.authToken && { Authorization: `Bearer ${this.config.authToken}` }),
      },
      body: JSON.stringify({ events: activities }),
    });

    return { success: response.ok };
  }

  private async handleConflict(
    clientPayload: SyncPayload,
    serverData: Record<string, unknown>,
    conflictType: ConflictType
  ): Promise<boolean> {
    if (!this.conflictResolver) {
      return false;
    }

    const resolved = this.conflictResolver.resolve(
      clientPayload.data,
      serverData,
      conflictType,
      ConflictResolution.SERVER_WINS // Default strategy
    );

    if (resolved) {
      // Re-sync with resolved data
      const retryPayload: SyncPayload = {
        ...clientPayload,
        data: resolved,
        clientTimestamp: new Date().toISOString(),
      };

      const response = await this.sendToServer(retryPayload);
      return response.success;
    }

    return false;
  }
}

// Export singleton
export const SyncService = new SyncServiceClass();

// Export class for testing
export { SyncServiceClass };
