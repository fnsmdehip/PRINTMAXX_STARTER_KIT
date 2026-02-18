/**
 * offlineQueue.ts - Queue requests when offline
 *
 * Stores failed requests for retry when connectivity is restored.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo, { NetInfoState } from '@react-native-community/netinfo';

// ============================================================================
// Types
// ============================================================================

export interface QueuedRequest {
  id: string;
  timestamp: number;
  url: string;
  method: string;
  headers: Record<string, string>;
  body?: string;
  retryCount: number;
  maxRetries: number;
  priority: RequestPriority;
  metadata?: Record<string, unknown>;
}

export type RequestPriority = 'high' | 'normal' | 'low';

export interface OfflineQueueConfig {
  maxQueueSize?: number;
  maxRetries?: number;
  storageKey?: string;
  retryDelay?: number;
  onRequestQueued?: (request: QueuedRequest) => void;
  onRequestCompleted?: (request: QueuedRequest) => void;
  onRequestFailed?: (request: QueuedRequest, error: Error) => void;
  onQueueProcessed?: (successful: number, failed: number) => void;
}

export interface QueueStats {
  totalQueued: number;
  pendingCount: number;
  processingCount: number;
  completedCount: number;
  failedCount: number;
}

// ============================================================================
// Constants
// ============================================================================

const DEFAULT_CONFIG: Required<Omit<OfflineQueueConfig, 'onRequestQueued' | 'onRequestCompleted' | 'onRequestFailed' | 'onQueueProcessed'>> = {
  maxQueueSize: 100,
  maxRetries: 3,
  storageKey: '@offline_queue',
  retryDelay: 1000,
};

// ============================================================================
// OfflineQueue Class
// ============================================================================

class OfflineQueue {
  private config: Required<Omit<OfflineQueueConfig, 'onRequestQueued' | 'onRequestCompleted' | 'onRequestFailed' | 'onQueueProcessed'>> & Partial<Pick<OfflineQueueConfig, 'onRequestQueued' | 'onRequestCompleted' | 'onRequestFailed' | 'onQueueProcessed'>>;
  private queue: QueuedRequest[] = [];
  private isProcessing: boolean = false;
  private isOnline: boolean = true;
  private unsubscribeNetInfo: (() => void) | null = null;
  private listeners: Set<(queue: QueuedRequest[]) => void> = new Set();
  private completedCount: number = 0;
  private failedCount: number = 0;

  constructor(config: OfflineQueueConfig = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  // --------------------------------------------------------------------------
  // Initialization
  // --------------------------------------------------------------------------

  /**
   * Initialize the queue and start monitoring connectivity
   */
  async initialize(): Promise<void> {
    // Load persisted queue
    await this.loadQueue();

    // Start monitoring network state
    this.unsubscribeNetInfo = NetInfo.addEventListener(this.handleConnectivityChange);

    // Check initial state
    const state = await NetInfo.fetch();
    this.isOnline = state.isConnected ?? false;

    // Process queue if online
    if (this.isOnline && this.queue.length > 0) {
      this.processQueue();
    }
  }

  /**
   * Cleanup and stop monitoring
   */
  destroy(): void {
    if (this.unsubscribeNetInfo) {
      this.unsubscribeNetInfo();
      this.unsubscribeNetInfo = null;
    }
  }

  // --------------------------------------------------------------------------
  // Queue Management
  // --------------------------------------------------------------------------

  /**
   * Add a request to the queue
   */
  async enqueue(
    url: string,
    options: {
      method: string;
      headers?: Record<string, string>;
      body?: unknown;
      priority?: RequestPriority;
      maxRetries?: number;
      metadata?: Record<string, unknown>;
    }
  ): Promise<string> {
    const request: QueuedRequest = {
      id: this.generateId(),
      timestamp: Date.now(),
      url,
      method: options.method,
      headers: options.headers ?? {},
      body: options.body ? JSON.stringify(options.body) : undefined,
      retryCount: 0,
      maxRetries: options.maxRetries ?? this.config.maxRetries,
      priority: options.priority ?? 'normal',
      metadata: options.metadata,
    };

    // Enforce queue size limit
    if (this.queue.length >= this.config.maxQueueSize) {
      // Remove oldest low-priority request
      const lowPriorityIndex = this.queue.findIndex((r) => r.priority === 'low');
      if (lowPriorityIndex >= 0) {
        this.queue.splice(lowPriorityIndex, 1);
      } else {
        throw new Error('Queue is full');
      }
    }

    // Add to queue based on priority
    this.insertByPriority(request);
    await this.persistQueue();

    this.config.onRequestQueued?.(request);
    this.notifyListeners();

    // Try to process immediately if online
    if (this.isOnline && !this.isProcessing) {
      this.processQueue();
    }

    return request.id;
  }

  /**
   * Remove a request from the queue
   */
  async remove(requestId: string): Promise<boolean> {
    const index = this.queue.findIndex((r) => r.id === requestId);
    if (index >= 0) {
      this.queue.splice(index, 1);
      await this.persistQueue();
      this.notifyListeners();
      return true;
    }
    return false;
  }

  /**
   * Clear the entire queue
   */
  async clear(): Promise<void> {
    this.queue = [];
    await this.persistQueue();
    this.notifyListeners();
  }

  /**
   * Get all queued requests
   */
  getQueue(): QueuedRequest[] {
    return [...this.queue];
  }

  /**
   * Get queue statistics
   */
  getStats(): QueueStats {
    return {
      totalQueued: this.queue.length,
      pendingCount: this.queue.filter((r) => r.retryCount === 0).length,
      processingCount: this.isProcessing ? 1 : 0,
      completedCount: this.completedCount,
      failedCount: this.failedCount,
    };
  }

  /**
   * Check if queue has pending requests
   */
  hasPending(): boolean {
    return this.queue.length > 0;
  }

  // --------------------------------------------------------------------------
  // Queue Processing
  // --------------------------------------------------------------------------

  /**
   * Process the queue
   */
  async processQueue(): Promise<void> {
    if (this.isProcessing || !this.isOnline || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;
    let successCount = 0;
    let failCount = 0;

    while (this.queue.length > 0 && this.isOnline) {
      const request = this.queue[0];

      try {
        await this.executeRequest(request);

        // Remove from queue on success
        this.queue.shift();
        await this.persistQueue();

        successCount++;
        this.completedCount++;
        this.config.onRequestCompleted?.(request);
      } catch (error) {
        request.retryCount++;

        if (request.retryCount >= request.maxRetries) {
          // Max retries reached, remove and report failure
          this.queue.shift();
          await this.persistQueue();

          failCount++;
          this.failedCount++;
          this.config.onRequestFailed?.(request, error as Error);
        } else {
          // Move to back of queue for retry
          this.queue.shift();
          this.queue.push(request);
          await this.persistQueue();

          // Wait before next retry
          await this.delay(this.config.retryDelay * request.retryCount);
        }
      }

      this.notifyListeners();
    }

    this.isProcessing = false;
    this.config.onQueueProcessed?.(successCount, failCount);
  }

  /**
   * Force process the queue (ignore online state)
   */
  async forceProcess(): Promise<void> {
    const wasOnline = this.isOnline;
    this.isOnline = true;
    await this.processQueue();
    this.isOnline = wasOnline;
  }

  // --------------------------------------------------------------------------
  // Request Execution
  // --------------------------------------------------------------------------

  private async executeRequest(request: QueuedRequest): Promise<Response> {
    const response = await fetch(request.url, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    return response;
  }

  // --------------------------------------------------------------------------
  // Connectivity Handling
  // --------------------------------------------------------------------------

  private handleConnectivityChange = (state: NetInfoState): void => {
    const wasOnline = this.isOnline;
    this.isOnline = state.isConnected ?? false;

    // Process queue when coming back online
    if (!wasOnline && this.isOnline && this.queue.length > 0) {
      this.processQueue();
    }
  };

  /**
   * Check current online status
   */
  isConnected(): boolean {
    return this.isOnline;
  }

  // --------------------------------------------------------------------------
  // Persistence
  // --------------------------------------------------------------------------

  private async persistQueue(): Promise<void> {
    try {
      await AsyncStorage.setItem(
        this.config.storageKey,
        JSON.stringify(this.queue)
      );
    } catch (error) {
      console.error('Failed to persist offline queue:', error);
    }
  }

  private async loadQueue(): Promise<void> {
    try {
      const data = await AsyncStorage.getItem(this.config.storageKey);
      if (data) {
        this.queue = JSON.parse(data);
      }
    } catch (error) {
      console.error('Failed to load offline queue:', error);
      this.queue = [];
    }
  }

  // --------------------------------------------------------------------------
  // Listeners
  // --------------------------------------------------------------------------

  /**
   * Subscribe to queue changes
   */
  subscribe(listener: (queue: QueuedRequest[]) => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(): void {
    const queueCopy = this.getQueue();
    this.listeners.forEach((listener) => listener(queueCopy));
  }

  // --------------------------------------------------------------------------
  // Helpers
  // --------------------------------------------------------------------------

  private insertByPriority(request: QueuedRequest): void {
    if (request.priority === 'high') {
      // Insert at the beginning
      this.queue.unshift(request);
    } else if (request.priority === 'low') {
      // Insert at the end
      this.queue.push(request);
    } else {
      // Insert after high priority items
      const insertIndex = this.queue.findIndex((r) => r.priority !== 'high');
      if (insertIndex >= 0) {
        this.queue.splice(insertIndex, 0, request);
      } else {
        this.queue.push(request);
      }
    }
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const offlineQueue = new OfflineQueue();

export default offlineQueue;
