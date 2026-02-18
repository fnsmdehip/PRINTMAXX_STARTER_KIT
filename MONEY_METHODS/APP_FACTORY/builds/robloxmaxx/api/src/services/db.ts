import Database from 'better-sqlite3';
import path from 'path';

const DB_PATH = path.join(process.cwd(), 'data', 'robloxmaxx.db');

let db: Database.Database;

export function getDb(): Database.Database {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
    initSchema();
  }
  return db;
}

function initSchema() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      plan TEXT DEFAULT 'free',
      stripe_customer_id TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS api_keys (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      key TEXT UNIQUE NOT NULL,
      name TEXT DEFAULT 'Default',
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS usage_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      action_type TEXT NOT NULL,
      genre TEXT,
      mode TEXT,
      tokens_used INTEGER DEFAULT 0,
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS projects (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      name TEXT NOT NULL,
      genre TEXT DEFAULT 'general',
      game_context TEXT DEFAULT '',
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS project_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id INTEGER NOT NULL,
      prompt TEXT NOT NULL,
      response TEXT NOT NULL,
      actions_json TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (project_id) REFERENCES projects(id)
    );
  `);
}

export function createUser(email: string, passwordHash: string) {
  const stmt = getDb().prepare(
    'INSERT INTO users (email, password_hash) VALUES (?, ?)'
  );
  return stmt.run(email, passwordHash);
}

export function getUserByEmail(email: string) {
  return getDb()
    .prepare('SELECT * FROM users WHERE email = ?')
    .get(email) as Record<string, unknown> | undefined;
}

export function getUserById(id: number) {
  return getDb()
    .prepare('SELECT * FROM users WHERE id = ?')
    .get(id) as Record<string, unknown> | undefined;
}

export function getUserByApiKey(key: string) {
  const row = getDb()
    .prepare(
      `SELECT u.* FROM users u
       JOIN api_keys ak ON u.id = ak.user_id
       WHERE ak.key = ?`
    )
    .get(key) as Record<string, unknown> | undefined;
  return row;
}

export function incrementUsage(userId: number, actionType: string, genre: string, mode: string, tokensUsed: number) {
  const db = getDb();
  // Analytics only - no limits enforced. User pays their own API costs (BYOK).
  db.prepare(
    'INSERT INTO usage_log (user_id, action_type, genre, mode, tokens_used) VALUES (?, ?, ?, ?, ?)'
  ).run(userId, actionType, genre, mode, tokensUsed);
}

export function createApiKey(userId: number, key: string, name: string) {
  return getDb()
    .prepare('INSERT INTO api_keys (user_id, key, name) VALUES (?, ?, ?)')
    .run(userId, key, name);
}
