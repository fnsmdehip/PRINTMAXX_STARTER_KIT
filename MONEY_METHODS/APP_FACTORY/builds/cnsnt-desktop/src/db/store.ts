import { openDB, type IDBPDatabase } from 'idb';
import type { EncryptedRecord, AuditEntry, VideoConsentRecord } from '../types';

const DB_NAME = 'cnsnt-vault';
const DB_VERSION = 2;

export const FREE_RECORD_LIMIT = 3;

let dbInstance: IDBPDatabase | null = null;

async function getDb(): Promise<IDBPDatabase> {
  if (dbInstance) return dbInstance;

  dbInstance = await openDB(DB_NAME, DB_VERSION, {
    upgrade(db, oldVersion) {
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
      if (oldVersion < 2) {
        if (!db.objectStoreNames.contains('videos')) {
          const videoStore = db.createObjectStore('videos', { keyPath: 'id' });
          videoStore.createIndex('consentRecordId', 'consentRecordId');
          videoStore.createIndex('timestamp', 'timestamp');
        }
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
  const videos = await getAllVideos();
  return JSON.stringify({ version: 2, records, audit, videos, exportedAt: new Date().toISOString() });
}

export async function importAllData(jsonStr: string): Promise<{ records: number; audit: number; videos: number }> {
  const data = JSON.parse(jsonStr);
  if (!data.version || !data.records || !data.audit) {
    throw new Error('Invalid backup file format');
  }

  const db = await getDb();
  let recordCount = 0;
  let auditCount = 0;
  let videoCount = 0;

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

  // Import videos if present (v2 format)
  if (data.videos && Array.isArray(data.videos) && db.objectStoreNames.contains('videos')) {
    const tx3 = db.transaction('videos', 'readwrite');
    for (const video of data.videos) {
      await tx3.store.put(video);
      videoCount++;
    }
    await tx3.done;
  }

  return { records: recordCount, audit: auditCount, videos: videoCount };
}

export async function clearAllData(): Promise<void> {
  const db = await getDb();
  const tx1 = db.transaction('records', 'readwrite');
  await tx1.store.clear();
  await tx1.done;
  const tx2 = db.transaction('audit', 'readwrite');
  await tx2.store.clear();
  await tx2.done;
  if (db.objectStoreNames.contains('videos')) {
    const tx3 = db.transaction('videos', 'readwrite');
    await tx3.store.clear();
    await tx3.done;
  }
}

// --- Video Consent ---

export interface StoredVideo {
  id: string;
  consentRecordId?: string;
  encryptedBlob: string; // base64 of encrypted blob
  encryptedMeta: string; // base64 of encrypted metadata JSON
  iv: string;
  salt: string;
  metaIv: string;
  metaSalt: string;
  hmac: string;
  timestamp: string;
  title: string;
}

export async function saveVideo(video: StoredVideo): Promise<void> {
  const db = await getDb();
  await db.put('videos', video);
}

export async function getVideo(id: string): Promise<StoredVideo | undefined> {
  const db = await getDb();
  return db.get('videos', id);
}

export async function getAllVideos(): Promise<StoredVideo[]> {
  const db = await getDb();
  const videos = await db.getAll('videos');
  return videos.sort(
    (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );
}

export async function deleteVideo(id: string): Promise<void> {
  const db = await getDb();
  await db.delete('videos', id);
}

export async function getVideosByRecord(consentRecordId: string): Promise<StoredVideo[]> {
  const db = await getDb();
  const index = db.transaction('videos').store.index('consentRecordId');
  return index.getAll(consentRecordId);
}

export async function getVideoCount(): Promise<number> {
  const db = await getDb();
  return db.count('videos');
}

// --- Free tier check ---

export async function canCreateRecord(isPremium: boolean): Promise<boolean> {
  if (isPremium) return true;
  const count = await getRecordCount();
  return count < FREE_RECORD_LIMIT;
}
