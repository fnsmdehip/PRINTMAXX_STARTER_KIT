import { useState, useRef } from 'react';
import { exportAllData, importAllData, addAuditEntry, getLastAuditHash } from '../db/store';
import { computeChainHash } from '../crypto/hmac';
import type { ViewName } from '../types';

interface BackupManagerProps {
  navigate: (view: ViewName) => void;
}

export default function BackupManager({ navigate }: BackupManagerProps) {
  const [status, setStatus] = useState('');
  const [statusType, setStatusType] = useState<'success' | 'error' | ''>('');
  const [exporting, setExporting] = useState(false);
  const [importing, setImporting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const logAudit = async (action: 'backup_export' | 'backup_import', details: string) => {
    const prevHash = await getLastAuditHash();
    const timestamp = new Date().toISOString();
    const content = `${action}|${timestamp}|${details}`;
    const hash = await computeChainHash(content, prevHash);
    await addAuditEntry({
      id: crypto.randomUUID(),
      action,
      timestamp,
      details,
      prevHash,
      hash,
    });
  };

  const handleExport = async () => {
    setExporting(true);
    setStatus('');
    try {
      const data = await exportAllData();
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cnsnt-backup-${new Date().toISOString().split('T')[0]}.cnsnt`;
      a.click();
      URL.revokeObjectURL(url);
      await logAudit('backup_export', 'Full backup exported');
      setStatus('Backup exported successfully.');
      setStatusType('success');
    } catch (err) {
      setStatus('Export failed. Please try again.');
      setStatusType('error');
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImporting(true);
    setStatus('');

    try {
      const text = await file.text();
      const result = await importAllData(text);
      const videoMsg = result.videos ? `, ${result.videos} videos` : '';
      await logAudit('backup_import', `Imported ${result.records} records, ${result.audit} audit entries${videoMsg}`);
      setStatus(`Imported ${result.records} records, ${result.audit} audit entries${videoMsg}.`);
      setStatusType('success');
    } catch (err) {
      setStatus('Import failed. File may be corrupted or in wrong format.');
      setStatusType('error');
      console.error(err);
    } finally {
      setImporting(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-2">Backup & Restore</h1>
      <p className="text-gray-400 text-sm mb-8">
        Your data is encrypted and stored only on this device. Back up regularly to avoid data loss.
      </p>

      {status && (
        <div className={`mb-6 p-4 rounded-xl ${
          statusType === 'success'
            ? 'bg-green-900/20 border border-green-800/30 text-green-400'
            : 'bg-red-900/20 border border-red-800/30 text-red-400'
        }`}>
          <p className="text-sm font-medium">{status}</p>
        </div>
      )}

      <div className="space-y-4">
        {/* Export */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-ocean/20 flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-white font-semibold">Export Backup</h3>
              <p className="text-gray-400 text-sm mt-1">
                Download an encrypted .cnsnt backup file containing all your records and audit log.
              </p>
              <button
                onClick={handleExport}
                disabled={exporting}
                className="mt-3 px-5 py-2 bg-coral text-white rounded-lg text-sm font-medium disabled:opacity-50"
              >
                {exporting ? 'Exporting...' : 'Export Backup File'}
              </button>
            </div>
          </div>
        </div>

        {/* Import */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-green-900/20 flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-white font-semibold">Import Backup</h3>
              <p className="text-gray-400 text-sm mt-1">
                Restore from a .cnsnt backup file. Existing records with the same ID will be updated.
              </p>
              <label className="mt-3 inline-block px-5 py-2 bg-ocean text-white rounded-lg text-sm font-medium cursor-pointer">
                {importing ? 'Importing...' : 'Choose .cnsnt File'}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".cnsnt,.json"
                  onChange={handleImport}
                  disabled={importing}
                  className="hidden"
                />
              </label>
            </div>
          </div>
        </div>

        {/* Info */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h3 className="text-white font-semibold mb-3">About Backups</h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <div>
                <p className="text-gray-300 text-sm font-medium">Records stay encrypted</p>
                <p className="text-gray-500 text-xs">Backup files contain your data in its encrypted form. Your PIN is required to decrypt.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <div>
                <p className="text-gray-300 text-sm font-medium">Local file storage</p>
                <p className="text-gray-500 text-xs">Backups are saved directly to your device. No data is sent to any server.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.834-1.964-.834-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <div>
                <p className="text-gray-300 text-sm font-medium">Keep your PIN</p>
                <p className="text-gray-500 text-xs">If you forget your PIN, you cannot decrypt your records. Store your PIN securely.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
