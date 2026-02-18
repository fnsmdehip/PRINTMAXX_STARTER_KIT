/**
 * Database Migrations - Schema version management
 *
 * Each migration has:
 * - version: Incrementing version number
 * - up: SQL statements to apply the migration
 * - down: SQL statements to revert the migration (for rollback)
 *
 * Migrations are applied in order and tracked in _migrations table.
 */

import { Migration } from '../DatabaseService';

/**
 * Migration 1: Initial schema
 * Creates core tables for app functionality
 */
export const migration_001_initial: Migration = {
  version: 1,
  up: [
    // User preferences
    `CREATE TABLE IF NOT EXISTS user_preferences (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      key TEXT NOT NULL UNIQUE,
      value TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_preferences_key ON user_preferences(key)`,

    // Streak data
    `CREATE TABLE IF NOT EXISTS streak_data (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT NOT NULL,
      streak_type TEXT NOT NULL,
      current_count INTEGER NOT NULL DEFAULT 0,
      longest_count INTEGER NOT NULL DEFAULT 0,
      last_activity_date TEXT,
      started_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )`,
    `CREATE INDEX IF NOT EXISTS idx_streak_user ON streak_data(user_id)`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_streak_user_type ON streak_data(user_id, streak_type)`,

    // Cached content
    `CREATE TABLE IF NOT EXISTS cached_content (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      content_id TEXT NOT NULL UNIQUE,
      content_type TEXT NOT NULL,
      data TEXT NOT NULL,
      etag TEXT,
      expires_at TEXT,
      created_at TEXT NOT NULL,
      accessed_at TEXT NOT NULL
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_content_id ON cached_content(content_id)`,
    `CREATE INDEX IF NOT EXISTS idx_content_expires ON cached_content(expires_at)`,
  ],
  down: [
    'DROP TABLE IF EXISTS cached_content',
    'DROP TABLE IF EXISTS streak_data',
    'DROP TABLE IF EXISTS user_preferences',
  ],
};

/**
 * Migration 2: Activity tracking
 * Adds activity log and sync queue for offline support
 */
export const migration_002_activity: Migration = {
  version: 2,
  up: [
    // Activity log
    `CREATE TABLE IF NOT EXISTS activity_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      event_data TEXT,
      screen TEXT,
      session_id TEXT,
      timestamp TEXT NOT NULL,
      synced INTEGER NOT NULL DEFAULT 0
    )`,
    `CREATE INDEX IF NOT EXISTS idx_activity_type ON activity_log(event_type)`,
    `CREATE INDEX IF NOT EXISTS idx_activity_synced ON activity_log(synced)`,

    // Sync queue
    `CREATE TABLE IF NOT EXISTS sync_queue (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      operation TEXT NOT NULL,
      entity_type TEXT NOT NULL,
      entity_id TEXT NOT NULL,
      payload TEXT NOT NULL,
      priority INTEGER NOT NULL DEFAULT 0,
      attempts INTEGER NOT NULL DEFAULT 0,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )`,
    `CREATE INDEX IF NOT EXISTS idx_sync_priority ON sync_queue(priority)`,
  ],
  down: ['DROP TABLE IF EXISTS sync_queue', 'DROP TABLE IF EXISTS activity_log'],
};

/**
 * Migration 3: Gamification
 * Adds achievements and favorites
 */
export const migration_003_gamification: Migration = {
  version: 3,
  up: [
    // Achievements
    `CREATE TABLE IF NOT EXISTS achievements (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      achievement_id TEXT NOT NULL UNIQUE,
      title TEXT NOT NULL,
      description TEXT,
      icon TEXT,
      unlocked INTEGER NOT NULL DEFAULT 0,
      unlocked_at TEXT,
      progress INTEGER NOT NULL DEFAULT 0,
      target INTEGER NOT NULL DEFAULT 100
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_achievement_id ON achievements(achievement_id)`,

    // Favorites
    `CREATE TABLE IF NOT EXISTS favorites (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id TEXT NOT NULL,
      item_type TEXT NOT NULL,
      title TEXT,
      thumbnail TEXT,
      metadata TEXT,
      created_at TEXT NOT NULL
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_favorite_item ON favorites(item_id, item_type)`,
    `CREATE INDEX IF NOT EXISTS idx_favorite_type ON favorites(item_type)`,
  ],
  down: ['DROP TABLE IF EXISTS favorites', 'DROP TABLE IF EXISTS achievements'],
};

/**
 * Migration 4: Downloads and search
 * Adds download tracking and search history
 */
export const migration_004_downloads: Migration = {
  version: 4,
  up: [
    // Downloads
    `CREATE TABLE IF NOT EXISTS downloads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      content_id TEXT NOT NULL UNIQUE,
      content_type TEXT NOT NULL,
      url TEXT NOT NULL,
      local_path TEXT,
      file_size INTEGER,
      downloaded_size INTEGER NOT NULL DEFAULT 0,
      status TEXT NOT NULL DEFAULT 'pending',
      error TEXT,
      started_at TEXT,
      completed_at TEXT
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_download_content ON downloads(content_id)`,
    `CREATE INDEX IF NOT EXISTS idx_download_status ON downloads(status)`,

    // Search history
    `CREATE TABLE IF NOT EXISTS search_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      query TEXT NOT NULL,
      result_count INTEGER,
      timestamp TEXT NOT NULL
    )`,
    `CREATE INDEX IF NOT EXISTS idx_search_timestamp ON search_history(timestamp)`,
  ],
  down: ['DROP TABLE IF EXISTS search_history', 'DROP TABLE IF EXISTS downloads'],
};

/**
 * Migration 5: Add notification preferences
 */
export const migration_005_notifications: Migration = {
  version: 5,
  up: [
    `CREATE TABLE IF NOT EXISTS notification_settings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      notification_type TEXT NOT NULL UNIQUE,
      enabled INTEGER NOT NULL DEFAULT 1,
      frequency TEXT,
      quiet_start TEXT,
      quiet_end TEXT,
      updated_at TEXT NOT NULL
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_notification_type ON notification_settings(notification_type)`,
  ],
  down: ['DROP TABLE IF EXISTS notification_settings'],
};

/**
 * Migration 6: Add purchase history for RevenueCat
 */
export const migration_006_purchases: Migration = {
  version: 6,
  up: [
    `CREATE TABLE IF NOT EXISTS purchase_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      transaction_id TEXT NOT NULL UNIQUE,
      product_id TEXT NOT NULL,
      purchase_date TEXT NOT NULL,
      expires_date TEXT,
      is_active INTEGER NOT NULL DEFAULT 0,
      store TEXT NOT NULL,
      raw_data TEXT,
      synced INTEGER NOT NULL DEFAULT 0
    )`,
    `CREATE UNIQUE INDEX IF NOT EXISTS idx_purchase_transaction ON purchase_history(transaction_id)`,
    `CREATE INDEX IF NOT EXISTS idx_purchase_product ON purchase_history(product_id)`,
    `CREATE INDEX IF NOT EXISTS idx_purchase_active ON purchase_history(is_active)`,
  ],
  down: ['DROP TABLE IF EXISTS purchase_history'],
};

/**
 * All migrations in order
 */
export const AllMigrations: Migration[] = [
  migration_001_initial,
  migration_002_activity,
  migration_003_gamification,
  migration_004_downloads,
  migration_005_notifications,
  migration_006_purchases,
];

/**
 * Current schema version (latest migration version)
 */
export const CURRENT_SCHEMA_VERSION = AllMigrations[AllMigrations.length - 1].version;

/**
 * Get migrations to run from a given version
 */
export function getMigrationsFrom(fromVersion: number): Migration[] {
  return AllMigrations.filter((m) => m.version > fromVersion);
}

/**
 * Validate migration sequence
 * Ensures versions are sequential and unique
 */
export function validateMigrations(): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  const versions = new Set<number>();

  for (let i = 0; i < AllMigrations.length; i++) {
    const migration = AllMigrations[i];

    // Check for duplicate versions
    if (versions.has(migration.version)) {
      errors.push(`Duplicate migration version: ${migration.version}`);
    }
    versions.add(migration.version);

    // Check for sequential ordering
    if (i > 0 && AllMigrations[i - 1].version >= migration.version) {
      errors.push(`Migration version ${migration.version} is not greater than previous`);
    }

    // Check for empty up statements
    if (migration.up.length === 0) {
      errors.push(`Migration ${migration.version} has no up statements`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
