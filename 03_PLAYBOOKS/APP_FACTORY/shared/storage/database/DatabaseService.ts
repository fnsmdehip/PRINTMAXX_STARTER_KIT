/**
 * DatabaseService - SQLite/WatermelonDB setup for structured data
 *
 * Features:
 * - SQLite for complex queries and relationships
 * - Type-safe schema definitions
 * - Migration support
 * - Transaction support
 * - Query builders
 */

import * as SQLite from 'expo-sqlite';

// Types
export interface DatabaseConfig {
  name: string;
  version: number;
}

export interface QueryResult<T> {
  rows: T[];
  insertId?: number;
  rowsAffected: number;
}

export interface DatabaseError {
  code: 'CONNECTION_ERROR' | 'QUERY_ERROR' | 'MIGRATION_ERROR' | 'TRANSACTION_ERROR';
  message: string;
  query?: string;
  originalError?: Error;
}

export type DatabaseResult<T> = { success: true; data: T } | { success: false; error: DatabaseError };

export interface Migration {
  version: number;
  up: string[];
  down: string[];
}

export interface TableSchema {
  name: string;
  columns: ColumnDefinition[];
  indexes?: IndexDefinition[];
}

export interface ColumnDefinition {
  name: string;
  type: 'TEXT' | 'INTEGER' | 'REAL' | 'BLOB' | 'BOOLEAN';
  primaryKey?: boolean;
  autoIncrement?: boolean;
  notNull?: boolean;
  unique?: boolean;
  default?: string | number | boolean | null;
  references?: {
    table: string;
    column: string;
    onDelete?: 'CASCADE' | 'SET NULL' | 'RESTRICT';
  };
}

export interface IndexDefinition {
  name: string;
  columns: string[];
  unique?: boolean;
}

class DatabaseServiceClass {
  private db: SQLite.SQLiteDatabase | null = null;
  private config: DatabaseConfig | null = null;
  private migrations: Migration[] = [];
  private isInitialized = false;

  /**
   * Initialize the database connection
   */
  async init(config: DatabaseConfig): Promise<DatabaseResult<void>> {
    try {
      this.config = config;
      this.db = await SQLite.openDatabaseAsync(config.name);

      // Enable foreign keys
      await this.db.execAsync('PRAGMA foreign_keys = ON;');

      // Create migrations table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS _migrations (
          version INTEGER PRIMARY KEY,
          applied_at TEXT NOT NULL
        );
      `);

      this.isInitialized = true;
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'CONNECTION_ERROR',
          message: `Failed to initialize database: ${config.name}`,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Register migrations
   */
  registerMigrations(migrations: Migration[]): void {
    this.migrations = migrations.sort((a, b) => a.version - b.version);
  }

  /**
   * Run pending migrations
   */
  async runMigrations(): Promise<DatabaseResult<number>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      // Get current version
      const result = await this.db.getFirstAsync<{ version: number }>(
        'SELECT MAX(version) as version FROM _migrations'
      );
      const currentVersion = result?.version ?? 0;

      let migrationsRun = 0;

      for (const migration of this.migrations) {
        if (migration.version > currentVersion) {
          await this.db.withTransactionAsync(async () => {
            for (const sql of migration.up) {
              await this.db!.execAsync(sql);
            }

            await this.db!.runAsync(
              'INSERT INTO _migrations (version, applied_at) VALUES (?, ?)',
              [migration.version, new Date().toISOString()]
            );
          });

          migrationsRun++;
        }
      }

      return { success: true, data: migrationsRun };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'MIGRATION_ERROR',
          message: 'Failed to run migrations',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Create a table from schema
   */
  async createTable(schema: TableSchema): Promise<DatabaseResult<void>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const columns = schema.columns.map((col) => {
        let def = `${col.name} ${col.type}`;
        if (col.primaryKey) def += ' PRIMARY KEY';
        if (col.autoIncrement) def += ' AUTOINCREMENT';
        if (col.notNull) def += ' NOT NULL';
        if (col.unique) def += ' UNIQUE';
        if (col.default !== undefined) {
          const defaultValue = typeof col.default === 'string' ? `'${col.default}'` : col.default;
          def += ` DEFAULT ${defaultValue}`;
        }
        if (col.references) {
          def += ` REFERENCES ${col.references.table}(${col.references.column})`;
          if (col.references.onDelete) def += ` ON DELETE ${col.references.onDelete}`;
        }
        return def;
      });

      const sql = `CREATE TABLE IF NOT EXISTS ${schema.name} (${columns.join(', ')});`;
      await this.db.execAsync(sql);

      // Create indexes
      if (schema.indexes) {
        for (const index of schema.indexes) {
          const indexSql = `CREATE ${index.unique ? 'UNIQUE ' : ''}INDEX IF NOT EXISTS ${index.name} ON ${schema.name} (${index.columns.join(', ')});`;
          await this.db.execAsync(indexSql);
        }
      }

      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: `Failed to create table: ${schema.name}`,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Execute a raw SQL query
   */
  async execute<T = unknown>(sql: string, params: unknown[] = []): Promise<DatabaseResult<QueryResult<T>>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const result = await this.db.runAsync(sql, params);
      return {
        success: true,
        data: {
          rows: [],
          insertId: result.lastInsertRowId,
          rowsAffected: result.changes,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: 'Query execution failed',
          query: sql,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Query multiple rows
   */
  async query<T>(sql: string, params: unknown[] = []): Promise<DatabaseResult<T[]>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const rows = await this.db.getAllAsync<T>(sql, params);
      return { success: true, data: rows };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: 'Query failed',
          query: sql,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Query a single row
   */
  async queryOne<T>(sql: string, params: unknown[] = []): Promise<DatabaseResult<T | null>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const row = await this.db.getFirstAsync<T>(sql, params);
      return { success: true, data: row };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: 'Query failed',
          query: sql,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Insert a record
   */
  async insert<T extends Record<string, unknown>>(
    table: string,
    data: T
  ): Promise<DatabaseResult<number>> {
    const columns = Object.keys(data);
    const values = Object.values(data);
    const placeholders = columns.map(() => '?').join(', ');

    const sql = `INSERT INTO ${table} (${columns.join(', ')}) VALUES (${placeholders})`;
    const result = await this.execute(sql, values);

    if (result.success) {
      return { success: true, data: result.data.insertId ?? 0 };
    }

    return result;
  }

  /**
   * Update records
   */
  async update<T extends Record<string, unknown>>(
    table: string,
    data: T,
    where: string,
    whereParams: unknown[] = []
  ): Promise<DatabaseResult<number>> {
    const sets = Object.keys(data)
      .map((col) => `${col} = ?`)
      .join(', ');
    const values = [...Object.values(data), ...whereParams];

    const sql = `UPDATE ${table} SET ${sets} WHERE ${where}`;
    const result = await this.execute(sql, values);

    if (result.success) {
      return { success: true, data: result.data.rowsAffected };
    }

    return result;
  }

  /**
   * Delete records
   */
  async delete(table: string, where: string, whereParams: unknown[] = []): Promise<DatabaseResult<number>> {
    const sql = `DELETE FROM ${table} WHERE ${where}`;
    const result = await this.execute(sql, whereParams);

    if (result.success) {
      return { success: true, data: result.data.rowsAffected };
    }

    return result;
  }

  /**
   * Upsert (insert or update)
   */
  async upsert<T extends Record<string, unknown>>(
    table: string,
    data: T,
    conflictColumns: string[]
  ): Promise<DatabaseResult<number>> {
    const columns = Object.keys(data);
    const values = Object.values(data);
    const placeholders = columns.map(() => '?').join(', ');

    const updateSets = columns
      .filter((col) => !conflictColumns.includes(col))
      .map((col) => `${col} = excluded.${col}`)
      .join(', ');

    const sql = `
      INSERT INTO ${table} (${columns.join(', ')})
      VALUES (${placeholders})
      ON CONFLICT(${conflictColumns.join(', ')})
      DO UPDATE SET ${updateSets}
    `;

    const result = await this.execute(sql, values);

    if (result.success) {
      return { success: true, data: result.data.insertId ?? result.data.rowsAffected };
    }

    return result;
  }

  /**
   * Run operations in a transaction
   */
  async transaction<T>(callback: () => Promise<T>): Promise<DatabaseResult<T>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      let result: T;
      await this.db.withTransactionAsync(async () => {
        result = await callback();
      });
      return { success: true, data: result! };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'TRANSACTION_ERROR',
          message: 'Transaction failed',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Check if database is initialized
   */
  isReady(): boolean {
    return this.isInitialized && this.db !== null;
  }

  /**
   * Get database version
   */
  async getVersion(): Promise<DatabaseResult<number>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const result = await this.db.getFirstAsync<{ version: number }>(
        'SELECT MAX(version) as version FROM _migrations'
      );
      return { success: true, data: result?.version ?? 0 };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: 'Failed to get version',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Close database connection
   */
  async close(): Promise<DatabaseResult<void>> {
    if (!this.db) {
      return { success: true, data: undefined };
    }

    try {
      await this.db.closeAsync();
      this.db = null;
      this.isInitialized = false;
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'CONNECTION_ERROR',
          message: 'Failed to close database',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Drop all tables (use with caution!)
   */
  async dropAllTables(): Promise<DatabaseResult<void>> {
    if (!this.db) {
      return {
        success: false,
        error: { code: 'CONNECTION_ERROR', message: 'Database not initialized' },
      };
    }

    try {
      const tables = await this.db.getAllAsync<{ name: string }>(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != '_migrations'"
      );

      for (const table of tables) {
        await this.db.execAsync(`DROP TABLE IF EXISTS ${table.name}`);
      }

      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'QUERY_ERROR',
          message: 'Failed to drop tables',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }
}

// Export singleton
export const DatabaseService = new DatabaseServiceClass();

// Export class for testing
export { DatabaseServiceClass };
