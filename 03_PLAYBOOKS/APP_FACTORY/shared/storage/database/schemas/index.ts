/**
 * Database Schemas - Table definitions for app data
 *
 * All table schemas are defined here for centralized management.
 * Use these schemas with DatabaseService.createTable()
 */

import { TableSchema } from '../DatabaseService';

/**
 * User preferences and settings
 */
export const UserPreferencesSchema: TableSchema = {
  name: 'user_preferences',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'key', type: 'TEXT', notNull: true, unique: true },
    { name: 'value', type: 'TEXT', notNull: true },
    { name: 'updated_at', type: 'TEXT', notNull: true },
  ],
  indexes: [{ name: 'idx_preferences_key', columns: ['key'], unique: true }],
};

/**
 * Streak tracking for gamification
 */
export const StreakDataSchema: TableSchema = {
  name: 'streak_data',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'user_id', type: 'TEXT', notNull: true },
    { name: 'streak_type', type: 'TEXT', notNull: true },
    { name: 'current_count', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'longest_count', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'last_activity_date', type: 'TEXT' },
    { name: 'started_at', type: 'TEXT', notNull: true },
    { name: 'updated_at', type: 'TEXT', notNull: true },
  ],
  indexes: [
    { name: 'idx_streak_user', columns: ['user_id'] },
    { name: 'idx_streak_type', columns: ['streak_type'] },
    { name: 'idx_streak_user_type', columns: ['user_id', 'streak_type'], unique: true },
  ],
};

/**
 * Content cache for offline access
 */
export const CachedContentSchema: TableSchema = {
  name: 'cached_content',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'content_id', type: 'TEXT', notNull: true, unique: true },
    { name: 'content_type', type: 'TEXT', notNull: true },
    { name: 'data', type: 'TEXT', notNull: true },
    { name: 'etag', type: 'TEXT' },
    { name: 'expires_at', type: 'TEXT' },
    { name: 'created_at', type: 'TEXT', notNull: true },
    { name: 'accessed_at', type: 'TEXT', notNull: true },
  ],
  indexes: [
    { name: 'idx_content_id', columns: ['content_id'], unique: true },
    { name: 'idx_content_type', columns: ['content_type'] },
    { name: 'idx_content_expires', columns: ['expires_at'] },
  ],
};

/**
 * User activity log for analytics
 */
export const ActivityLogSchema: TableSchema = {
  name: 'activity_log',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'event_type', type: 'TEXT', notNull: true },
    { name: 'event_data', type: 'TEXT' },
    { name: 'screen', type: 'TEXT' },
    { name: 'session_id', type: 'TEXT' },
    { name: 'timestamp', type: 'TEXT', notNull: true },
    { name: 'synced', type: 'INTEGER', notNull: true, default: 0 },
  ],
  indexes: [
    { name: 'idx_activity_type', columns: ['event_type'] },
    { name: 'idx_activity_timestamp', columns: ['timestamp'] },
    { name: 'idx_activity_synced', columns: ['synced'] },
  ],
};

/**
 * Sync queue for offline changes
 */
export const SyncQueueSchema: TableSchema = {
  name: 'sync_queue',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'operation', type: 'TEXT', notNull: true }, // CREATE, UPDATE, DELETE
    { name: 'entity_type', type: 'TEXT', notNull: true },
    { name: 'entity_id', type: 'TEXT', notNull: true },
    { name: 'payload', type: 'TEXT', notNull: true },
    { name: 'priority', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'attempts', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'last_error', type: 'TEXT' },
    { name: 'created_at', type: 'TEXT', notNull: true },
    { name: 'updated_at', type: 'TEXT', notNull: true },
  ],
  indexes: [
    { name: 'idx_sync_entity', columns: ['entity_type', 'entity_id'] },
    { name: 'idx_sync_priority', columns: ['priority'] },
    { name: 'idx_sync_created', columns: ['created_at'] },
  ],
};

/**
 * Achievements and badges
 */
export const AchievementsSchema: TableSchema = {
  name: 'achievements',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'achievement_id', type: 'TEXT', notNull: true, unique: true },
    { name: 'title', type: 'TEXT', notNull: true },
    { name: 'description', type: 'TEXT' },
    { name: 'icon', type: 'TEXT' },
    { name: 'unlocked', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'unlocked_at', type: 'TEXT' },
    { name: 'progress', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'target', type: 'INTEGER', notNull: true, default: 100 },
  ],
  indexes: [
    { name: 'idx_achievement_id', columns: ['achievement_id'], unique: true },
    { name: 'idx_achievement_unlocked', columns: ['unlocked'] },
  ],
};

/**
 * Favorites/bookmarks
 */
export const FavoritesSchema: TableSchema = {
  name: 'favorites',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'item_id', type: 'TEXT', notNull: true },
    { name: 'item_type', type: 'TEXT', notNull: true },
    { name: 'title', type: 'TEXT' },
    { name: 'thumbnail', type: 'TEXT' },
    { name: 'metadata', type: 'TEXT' },
    { name: 'created_at', type: 'TEXT', notNull: true },
  ],
  indexes: [
    { name: 'idx_favorite_item', columns: ['item_id', 'item_type'], unique: true },
    { name: 'idx_favorite_type', columns: ['item_type'] },
    { name: 'idx_favorite_created', columns: ['created_at'] },
  ],
};

/**
 * Download progress for offline content
 */
export const DownloadsSchema: TableSchema = {
  name: 'downloads',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'content_id', type: 'TEXT', notNull: true, unique: true },
    { name: 'content_type', type: 'TEXT', notNull: true },
    { name: 'url', type: 'TEXT', notNull: true },
    { name: 'local_path', type: 'TEXT' },
    { name: 'file_size', type: 'INTEGER' },
    { name: 'downloaded_size', type: 'INTEGER', notNull: true, default: 0 },
    { name: 'status', type: 'TEXT', notNull: true, default: "'pending'" }, // pending, downloading, completed, failed
    { name: 'error', type: 'TEXT' },
    { name: 'started_at', type: 'TEXT' },
    { name: 'completed_at', type: 'TEXT' },
  ],
  indexes: [
    { name: 'idx_download_content', columns: ['content_id'], unique: true },
    { name: 'idx_download_status', columns: ['status'] },
  ],
};

/**
 * Search history
 */
export const SearchHistorySchema: TableSchema = {
  name: 'search_history',
  columns: [
    { name: 'id', type: 'INTEGER', primaryKey: true, autoIncrement: true },
    { name: 'query', type: 'TEXT', notNull: true },
    { name: 'result_count', type: 'INTEGER' },
    { name: 'timestamp', type: 'TEXT', notNull: true },
  ],
  indexes: [
    { name: 'idx_search_query', columns: ['query'] },
    { name: 'idx_search_timestamp', columns: ['timestamp'] },
  ],
};

/**
 * All schemas for easy iteration
 */
export const AllSchemas: TableSchema[] = [
  UserPreferencesSchema,
  StreakDataSchema,
  CachedContentSchema,
  ActivityLogSchema,
  SyncQueueSchema,
  AchievementsSchema,
  FavoritesSchema,
  DownloadsSchema,
  SearchHistorySchema,
];

/**
 * Initialize all tables
 */
export async function initializeAllTables(
  createTable: (schema: TableSchema) => Promise<{ success: boolean }>
): Promise<{ success: boolean; errors: string[] }> {
  const errors: string[] = [];

  for (const schema of AllSchemas) {
    const result = await createTable(schema);
    if (!result.success) {
      errors.push(`Failed to create table: ${schema.name}`);
    }
  }

  return {
    success: errors.length === 0,
    errors,
  };
}
