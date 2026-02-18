/**
 * Common Database Queries - Reusable query functions
 *
 * Provides type-safe query functions for common database operations.
 * Use these instead of writing raw SQL in components.
 */

import { DatabaseService } from '../DatabaseService';

// Types
export interface UserPreference {
  id: number;
  key: string;
  value: string;
  updated_at: string;
}

export interface StreakData {
  id: number;
  user_id: string;
  streak_type: string;
  current_count: number;
  longest_count: number;
  last_activity_date: string | null;
  started_at: string;
  updated_at: string;
}

export interface CachedContent {
  id: number;
  content_id: string;
  content_type: string;
  data: string;
  etag: string | null;
  expires_at: string | null;
  created_at: string;
  accessed_at: string;
}

export interface ActivityLog {
  id: number;
  event_type: string;
  event_data: string | null;
  screen: string | null;
  session_id: string | null;
  timestamp: string;
  synced: number;
}

export interface SyncQueueItem {
  id: number;
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  entity_type: string;
  entity_id: string;
  payload: string;
  priority: number;
  attempts: number;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export interface Achievement {
  id: number;
  achievement_id: string;
  title: string;
  description: string | null;
  icon: string | null;
  unlocked: number;
  unlocked_at: string | null;
  progress: number;
  target: number;
}

export interface Favorite {
  id: number;
  item_id: string;
  item_type: string;
  title: string | null;
  thumbnail: string | null;
  metadata: string | null;
  created_at: string;
}

export interface Download {
  id: number;
  content_id: string;
  content_type: string;
  url: string;
  local_path: string | null;
  file_size: number | null;
  downloaded_size: number;
  status: 'pending' | 'downloading' | 'completed' | 'failed';
  error: string | null;
  started_at: string | null;
  completed_at: string | null;
}

// User Preferences Queries

export const PreferencesQueries = {
  async get(key: string): Promise<string | null> {
    const result = await DatabaseService.queryOne<UserPreference>(
      'SELECT * FROM user_preferences WHERE key = ?',
      [key]
    );
    return result.success ? result.data?.value ?? null : null;
  },

  async set(key: string, value: string): Promise<boolean> {
    const now = new Date().toISOString();
    const result = await DatabaseService.upsert(
      'user_preferences',
      { key, value, updated_at: now },
      ['key']
    );
    return result.success;
  },

  async getAll(): Promise<Record<string, string>> {
    const result = await DatabaseService.query<UserPreference>('SELECT * FROM user_preferences');
    if (!result.success) return {};

    return result.data.reduce(
      (acc, pref) => {
        acc[pref.key] = pref.value;
        return acc;
      },
      {} as Record<string, string>
    );
  },

  async delete(key: string): Promise<boolean> {
    const result = await DatabaseService.delete('user_preferences', 'key = ?', [key]);
    return result.success;
  },
};

// Streak Queries

export const StreakQueries = {
  async get(userId: string, streakType: string): Promise<StreakData | null> {
    const result = await DatabaseService.queryOne<StreakData>(
      'SELECT * FROM streak_data WHERE user_id = ? AND streak_type = ?',
      [userId, streakType]
    );
    return result.success ? result.data : null;
  },

  async getAll(userId: string): Promise<StreakData[]> {
    const result = await DatabaseService.query<StreakData>(
      'SELECT * FROM streak_data WHERE user_id = ?',
      [userId]
    );
    return result.success ? result.data : [];
  },

  async update(
    userId: string,
    streakType: string,
    data: Partial<Pick<StreakData, 'current_count' | 'longest_count' | 'last_activity_date'>>
  ): Promise<boolean> {
    const now = new Date().toISOString();
    const result = await DatabaseService.upsert(
      'streak_data',
      {
        user_id: userId,
        streak_type: streakType,
        ...data,
        started_at: now,
        updated_at: now,
      },
      ['user_id', 'streak_type']
    );
    return result.success;
  },

  async increment(userId: string, streakType: string): Promise<StreakData | null> {
    const existing = await this.get(userId, streakType);
    const now = new Date().toISOString();
    const today = now.split('T')[0];

    if (!existing) {
      await this.update(userId, streakType, {
        current_count: 1,
        longest_count: 1,
        last_activity_date: today,
      });
      return this.get(userId, streakType);
    }

    const lastDate = existing.last_activity_date?.split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    let newCount = existing.current_count;

    if (lastDate === today) {
      // Already logged today, no change
      return existing;
    } else if (lastDate === yesterday) {
      // Consecutive day
      newCount = existing.current_count + 1;
    } else {
      // Streak broken
      newCount = 1;
    }

    const newLongest = Math.max(existing.longest_count, newCount);

    await this.update(userId, streakType, {
      current_count: newCount,
      longest_count: newLongest,
      last_activity_date: today,
    });

    return this.get(userId, streakType);
  },

  async reset(userId: string, streakType: string): Promise<boolean> {
    return this.update(userId, streakType, {
      current_count: 0,
      last_activity_date: null,
    });
  },
};

// Cache Queries

export const CacheQueries = {
  async get<T>(contentId: string): Promise<T | null> {
    const result = await DatabaseService.queryOne<CachedContent>(
      'SELECT * FROM cached_content WHERE content_id = ?',
      [contentId]
    );

    if (!result.success || !result.data) return null;

    // Check expiration
    if (result.data.expires_at && new Date(result.data.expires_at) < new Date()) {
      await this.delete(contentId);
      return null;
    }

    // Update accessed_at
    await DatabaseService.update(
      'cached_content',
      { accessed_at: new Date().toISOString() },
      'content_id = ?',
      [contentId]
    );

    try {
      return JSON.parse(result.data.data) as T;
    } catch {
      return null;
    }
  },

  async set<T>(contentId: string, contentType: string, data: T, ttlMs?: number): Promise<boolean> {
    const now = new Date().toISOString();
    const expiresAt = ttlMs ? new Date(Date.now() + ttlMs).toISOString() : null;

    const result = await DatabaseService.upsert(
      'cached_content',
      {
        content_id: contentId,
        content_type: contentType,
        data: JSON.stringify(data),
        expires_at: expiresAt,
        created_at: now,
        accessed_at: now,
      },
      ['content_id']
    );

    return result.success;
  },

  async delete(contentId: string): Promise<boolean> {
    const result = await DatabaseService.delete('cached_content', 'content_id = ?', [contentId]);
    return result.success;
  },

  async deleteByType(contentType: string): Promise<boolean> {
    const result = await DatabaseService.delete('cached_content', 'content_type = ?', [contentType]);
    return result.success;
  },

  async cleanExpired(): Promise<number> {
    const now = new Date().toISOString();
    const result = await DatabaseService.delete('cached_content', 'expires_at IS NOT NULL AND expires_at < ?', [
      now,
    ]);
    return result.success ? result.data : 0;
  },

  async getSize(): Promise<number> {
    const result = await DatabaseService.queryOne<{ total: number }>(
      'SELECT SUM(LENGTH(data)) as total FROM cached_content'
    );
    return result.success ? result.data?.total ?? 0 : 0;
  },
};

// Activity Queries

export const ActivityQueries = {
  async log(
    eventType: string,
    eventData?: Record<string, unknown>,
    screen?: string,
    sessionId?: string
  ): Promise<boolean> {
    const result = await DatabaseService.insert('activity_log', {
      event_type: eventType,
      event_data: eventData ? JSON.stringify(eventData) : null,
      screen: screen ?? null,
      session_id: sessionId ?? null,
      timestamp: new Date().toISOString(),
      synced: 0,
    });
    return result.success;
  },

  async getUnsynced(limit = 100): Promise<ActivityLog[]> {
    const result = await DatabaseService.query<ActivityLog>(
      'SELECT * FROM activity_log WHERE synced = 0 ORDER BY timestamp ASC LIMIT ?',
      [limit]
    );
    return result.success ? result.data : [];
  },

  async markSynced(ids: number[]): Promise<boolean> {
    if (ids.length === 0) return true;
    const placeholders = ids.map(() => '?').join(',');
    const result = await DatabaseService.execute(
      `UPDATE activity_log SET synced = 1 WHERE id IN (${placeholders})`,
      ids
    );
    return result.success;
  },

  async getByType(eventType: string, limit = 50): Promise<ActivityLog[]> {
    const result = await DatabaseService.query<ActivityLog>(
      'SELECT * FROM activity_log WHERE event_type = ? ORDER BY timestamp DESC LIMIT ?',
      [eventType, limit]
    );
    return result.success ? result.data : [];
  },

  async getRecent(limit = 50): Promise<ActivityLog[]> {
    const result = await DatabaseService.query<ActivityLog>(
      'SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT ?',
      [limit]
    );
    return result.success ? result.data : [];
  },

  async cleanup(olderThanDays = 30): Promise<number> {
    const cutoff = new Date(Date.now() - olderThanDays * 86400000).toISOString();
    const result = await DatabaseService.delete('activity_log', 'timestamp < ? AND synced = 1', [cutoff]);
    return result.success ? result.data : 0;
  },
};

// Sync Queue Queries

export const SyncQueueQueries = {
  async add(
    operation: 'CREATE' | 'UPDATE' | 'DELETE',
    entityType: string,
    entityId: string,
    payload: Record<string, unknown>,
    priority = 0
  ): Promise<boolean> {
    const now = new Date().toISOString();
    const result = await DatabaseService.insert('sync_queue', {
      operation,
      entity_type: entityType,
      entity_id: entityId,
      payload: JSON.stringify(payload),
      priority,
      attempts: 0,
      last_error: null,
      created_at: now,
      updated_at: now,
    });
    return result.success;
  },

  async getNext(limit = 10): Promise<SyncQueueItem[]> {
    const result = await DatabaseService.query<SyncQueueItem>(
      'SELECT * FROM sync_queue WHERE attempts < 5 ORDER BY priority DESC, created_at ASC LIMIT ?',
      [limit]
    );
    return result.success ? result.data : [];
  },

  async markAttempted(id: number, error?: string): Promise<boolean> {
    const result = await DatabaseService.update(
      'sync_queue',
      {
        attempts: DatabaseService.isReady() ? 'attempts + 1' : 1,
        last_error: error ?? null,
        updated_at: new Date().toISOString(),
      },
      'id = ?',
      [id]
    );
    return result.success;
  },

  async remove(id: number): Promise<boolean> {
    const result = await DatabaseService.delete('sync_queue', 'id = ?', [id]);
    return result.success;
  },

  async removeByEntity(entityType: string, entityId: string): Promise<boolean> {
    const result = await DatabaseService.delete('sync_queue', 'entity_type = ? AND entity_id = ?', [
      entityType,
      entityId,
    ]);
    return result.success;
  },

  async getCount(): Promise<number> {
    const result = await DatabaseService.queryOne<{ count: number }>(
      'SELECT COUNT(*) as count FROM sync_queue'
    );
    return result.success ? result.data?.count ?? 0 : 0;
  },

  async getFailedCount(): Promise<number> {
    const result = await DatabaseService.queryOne<{ count: number }>(
      'SELECT COUNT(*) as count FROM sync_queue WHERE attempts >= 5'
    );
    return result.success ? result.data?.count ?? 0 : 0;
  },
};

// Favorites Queries

export const FavoritesQueries = {
  async add(itemId: string, itemType: string, title?: string, thumbnail?: string, metadata?: Record<string, unknown>): Promise<boolean> {
    const result = await DatabaseService.upsert(
      'favorites',
      {
        item_id: itemId,
        item_type: itemType,
        title: title ?? null,
        thumbnail: thumbnail ?? null,
        metadata: metadata ? JSON.stringify(metadata) : null,
        created_at: new Date().toISOString(),
      },
      ['item_id', 'item_type']
    );
    return result.success;
  },

  async remove(itemId: string, itemType: string): Promise<boolean> {
    const result = await DatabaseService.delete('favorites', 'item_id = ? AND item_type = ?', [
      itemId,
      itemType,
    ]);
    return result.success;
  },

  async isFavorite(itemId: string, itemType: string): Promise<boolean> {
    const result = await DatabaseService.queryOne<Favorite>(
      'SELECT * FROM favorites WHERE item_id = ? AND item_type = ?',
      [itemId, itemType]
    );
    return result.success && result.data !== null;
  },

  async getByType(itemType: string, limit = 50): Promise<Favorite[]> {
    const result = await DatabaseService.query<Favorite>(
      'SELECT * FROM favorites WHERE item_type = ? ORDER BY created_at DESC LIMIT ?',
      [itemType, limit]
    );
    return result.success ? result.data : [];
  },

  async getAll(limit = 100): Promise<Favorite[]> {
    const result = await DatabaseService.query<Favorite>(
      'SELECT * FROM favorites ORDER BY created_at DESC LIMIT ?',
      [limit]
    );
    return result.success ? result.data : [];
  },

  async getCount(): Promise<number> {
    const result = await DatabaseService.queryOne<{ count: number }>('SELECT COUNT(*) as count FROM favorites');
    return result.success ? result.data?.count ?? 0 : 0;
  },
};

// Achievements Queries

export const AchievementsQueries = {
  async unlock(achievementId: string, title: string, description?: string, icon?: string): Promise<boolean> {
    const result = await DatabaseService.upsert(
      'achievements',
      {
        achievement_id: achievementId,
        title,
        description: description ?? null,
        icon: icon ?? null,
        unlocked: 1,
        unlocked_at: new Date().toISOString(),
        progress: 100,
        target: 100,
      },
      ['achievement_id']
    );
    return result.success;
  },

  async updateProgress(achievementId: string, progress: number, target: number): Promise<boolean> {
    const unlocked = progress >= target ? 1 : 0;
    const unlockedAt = progress >= target ? new Date().toISOString() : null;

    const result = await DatabaseService.upsert(
      'achievements',
      {
        achievement_id: achievementId,
        title: achievementId, // Placeholder, should be updated with actual title
        progress,
        target,
        unlocked,
        unlocked_at: unlockedAt,
      },
      ['achievement_id']
    );
    return result.success;
  },

  async get(achievementId: string): Promise<Achievement | null> {
    const result = await DatabaseService.queryOne<Achievement>(
      'SELECT * FROM achievements WHERE achievement_id = ?',
      [achievementId]
    );
    return result.success ? result.data : null;
  },

  async getUnlocked(): Promise<Achievement[]> {
    const result = await DatabaseService.query<Achievement>(
      'SELECT * FROM achievements WHERE unlocked = 1 ORDER BY unlocked_at DESC'
    );
    return result.success ? result.data : [];
  },

  async getAll(): Promise<Achievement[]> {
    const result = await DatabaseService.query<Achievement>('SELECT * FROM achievements ORDER BY unlocked DESC, progress DESC');
    return result.success ? result.data : [];
  },

  async getUnlockedCount(): Promise<number> {
    const result = await DatabaseService.queryOne<{ count: number }>(
      'SELECT COUNT(*) as count FROM achievements WHERE unlocked = 1'
    );
    return result.success ? result.data?.count ?? 0 : 0;
  },
};
