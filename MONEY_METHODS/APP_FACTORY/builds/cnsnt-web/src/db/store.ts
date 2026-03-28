import { openDB, type IDBPDatabase } from 'idb';
import type { EncryptedRecord, AuditEntry } from '../types';

const DB_NAME = 'cnsnt-vault';
const DB_VERSION = 1;

let dbInstance: IDBPDatabase | null = null;

async function getDb(): Promise<IDBPDatabase> {
  if (dbInstance) return dbInstance;

  dbInstance = await openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains('records')) {
        const recordStore = db.createObjectStore('records', { keyPath: 'id' });
        recordStore.createIndex('createdAt', 'createdAt');
        recordStore.createIndex('title', 'title');
      }
      if (!db.objectStoreNames.contains('audit')) {
        const auditStore = db.createObjectStore('audit', { keyPath: 'id' });
        auditStore.createIndex('timestamp', 'timestamp');
        auditStore.createIndex('action', 'action');
      }
    },
  });

  return dbInstance;
}

// --- Records ---

export async function saveRecord(record: EncryptedRecord): Promise<void> {
  const db = await getDb();
  await db.put('records', record);
}

export async function getRecord(id: string): Promise<EncryptedRecord | undefined> {
  const db = await getDb();
  return db.get('records', id);
}

export async function getAllRecords(): Promise<EncryptedRecord[]> {
  const db = await getDb();
  const records = await db.getAll('records');
  return records.sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
}

export async function deleteRecord(id: string): Promise<void> {
  const db = await getDb();
  await db.delete('records', id);
}

export async function getRecordCount(): Promise<number> {
  const db = await getDb();
  return db.count('records');
}

export async function searchRecords(query: string): Promise<EncryptedRecord[]> {
  const all = await getAllRecords();
  const lower = query.toLowerCase();
  return all.filter((r) => r.title.toLowerCase().includes(lower));
}

// --- Audit Log ---

export async function addAuditEntry(entry: AuditEntry): Promise<void> {
  const db = await getDb();
  await db.put('audit', entry);
}

export async function getAllAuditEntries(): Promise<AuditEntry[]> {
  const db = await getDb();
  const entries = await db.getAll('audit');
  return entries.sort(
    (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );
}

export async function getLastAuditHash(): Promise<string> {
  const entries = await getAllAuditEntries();
  if (entries.length === 0) return 'GENESIS';
  return entries[0].hash;
}

// --- Backup ---

export async function exportAllData(): Promise<string> {
  const records = await getAllRecords();
  const audit = await getAllAuditEntries();
  return JSON.stringify({ version: 1, records, audit, exportedAt: new Date().toISOString() });
}

export async function importAllData(jsonStr: string): Promise<{ records: number; audit: number }> {
  const data = JSON.parse(jsonStr);
  if (!data.version || !data.records || !data.audit) {
    throw new Error('Invalid backup file format');
  }

  const db = await getDb();
  let recordCount = 0;
  let auditCount = 0;

  const tx1 = db.transaction('records', 'readwrite');
  for (const record of data.records) {
    await tx1.store.put(record);
    recordCount++;
  }
  await tx1.done;

  const tx2 = db.transaction('audit', 'readwrite');
  for (const entry of data.audit) {
    await tx2.store.put(entry);
    auditCount++;
  }
  await tx2.done;

  return { records: recordCount, audit: auditCount };
}

export async function clearAllData(): Promise<void> {
  const db = await getDb();
  const tx1 = db.transaction('records', 'readwrite');
  await tx1.store.clear();
  await tx1.done;
  const tx2 = db.transaction('audit', 'readwrite');
  await tx2.store.clear();
  await tx2.done;
}
