import { useState, useEffect, useRef } from 'react';
import { decrypt } from '../crypto/vault';
import { verifyHmac, computeChainHash } from '../crypto/hmac';
import { getRecord, deleteRecord, addAuditEntry, getLastAuditHash } from '../db/store';
import type { ConsentRecord, EncryptedRecord, ViewName } from '../types';

interface RecordViewerProps {
  recordId: string;
  pin: string;
  navigate: (view: ViewName) => void;
  isPremium: boolean;
}

export default function RecordViewer({ recordId, pin, navigate, isPremium }: RecordViewerProps) {
  const [encrypted, setEncrypted] = useState<EncryptedRecord | null>(null);
  const [record, setRecord] = useState<ConsentRecord | null>(null);
  const [integrityOk, setIntegrityOk] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showDelete, setShowDelete] = useState(false);
  const [exporting, setExporting] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadRecord();
  }, [recordId]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadRecord = async () => {
    setLoading(true);
    try {
      const enc = await getRecord(recordId);
      if (!enc) {
        setError('Record not found.');
        setLoading(false);
        return;
      }
      setEncrypted(enc);

      // Verify HMAC integrity
      const valid = await verifyHmac(enc.ciphertext, enc.hmac);
      setIntegrityOk(valid);

      // Decrypt
      const plaintext = await decrypt(enc.ciphertext, enc.iv, enc.salt, pin);
      const parsed = JSON.parse(plaintext) as ConsentRecord;
      setRecord(parsed);

      // Audit: view
      const prevHash = await getLastAuditHash();
      const content = `view|${recordId}|${new Date().toISOString()}`;
      const hash = await computeChainHash(content, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'view',
        recordId,
        timestamp: new Date().toISOString(),
        details: `Viewed record: ${enc.title}`,
        prevHash,
        hash,
      });
    } catch (err) {
      setError('Failed to decrypt record. PIN may have changed.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    const prevHash = await getLastAuditHash();
    const content = `delete|${recordId}|${new Date().toISOString()}`;
    const hash = await computeChainHash(content, prevHash);
    await addAuditEntry({
      id: crypto.randomUUID(),
      action: 'delete',
      recordId,
      timestamp: new Date().toISOString(),
      details: `Deleted record: ${encrypted?.title}`,
      prevHash,
      hash,
    });
    await deleteRecord(recordId);
    navigate('dashboard');
  };

  const handleExportPdf = async () => {
    if (!isPremium) {
      navigate('paywall');
      return;
    }
    if (!record || !printRef.current) return;
    setExporting(true);

    try {
      const { default: jsPDF } = await import('jspdf');
      const { default: html2canvas } = await import('html2canvas');

      const canvas = await html2canvas(printRef.current, {
        backgroundColor: '#1a1a2e',
        scale: 2,
        useCORS: true,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
      });

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`cnsnt-${record.title.replace(/\s+/g, '-').toLowerCase()}.pdf`);

      // Audit: export
      const prevHash = await getLastAuditHash();
      const content = `export|${recordId}|${new Date().toISOString()}`;
      const hash = await computeChainHash(content, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'export',
        recordId,
        timestamp: new Date().toISOString(),
        details: `Exported PDF: ${record.title}`,
        prevHash,
        hash,
      });
    } catch (err) {
      setError('PDF export failed.');
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-8 h-8 border-2 border-coral border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 max-w-2xl mx-auto text-center py-16">
        <p className="text-red-400 text-lg">{error}</p>
        <button
          onClick={() => navigate('dashboard')}
          className="mt-4 px-6 py-3 bg-navy-light border border-gray-700 rounded-xl text-white"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  if (!record) return null;

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => navigate('dashboard')}
          className="text-gray-400 flex items-center gap-1"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <div className="flex items-center gap-2">
          <button
            onClick={handleExportPdf}
            disabled={exporting}
            className="px-3 py-2 bg-ocean text-white rounded-lg text-sm font-medium disabled:opacity-50"
          >
            {exporting ? 'Exporting...' : 'PDF'}
          </button>
          <button
            onClick={() => setShowDelete(true)}
            className="px-3 py-2 bg-red-900/30 text-red-400 rounded-lg text-sm font-medium"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Integrity badge */}
      <div className={`mb-4 p-3 rounded-xl flex items-center gap-2 ${
        integrityOk
          ? 'bg-green-900/20 border border-green-800/30'
          : 'bg-red-900/20 border border-red-800/30'
      }`}>
        <svg className={`w-5 h-5 ${integrityOk ? 'text-green-400' : 'text-red-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          {integrityOk ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.834-1.964-.834-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          )}
        </svg>
        <span className={`text-sm font-medium ${integrityOk ? 'text-green-400' : 'text-red-400'}`}>
          {integrityOk ? 'Integrity verified (HMAC-SHA-256)' : 'Integrity check FAILED - record may be tampered'}
        </span>
      </div>

      {/* Printable content */}
      <div ref={printRef} className="space-y-4">
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h1 className="text-2xl font-bold text-white mb-1">{record.title}</h1>
          <p className="text-gray-400 text-sm">
            Created: {new Date(record.timestamp).toLocaleString()}
          </p>
          {record.geolocation && (
            <p className="text-gray-500 text-xs mt-1">
              Location: {record.geolocation.latitude.toFixed(4)}, {record.geolocation.longitude.toFixed(4)}
            </p>
          )}
        </div>

        {/* Parties */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-coral text-xs font-semibold uppercase tracking-wide mb-3">Parties</h2>
          {record.parties.map((party, i) => (
            <div key={i} className="mb-2 last:mb-0">
              <span className="text-gray-400 text-sm">{party.role}:</span>{' '}
              <span className="text-white font-medium">{party.name}</span>
              {party.email && <span className="text-gray-500 text-sm ml-2">{party.email}</span>}
            </div>
          ))}
        </div>

        {/* Terms */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-coral text-xs font-semibold uppercase tracking-wide mb-3">Terms & Conditions</h2>
          <div className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
            {record.terms}
          </div>
        </div>

        {/* Details */}
        {record.details && (
          <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
            <h2 className="text-coral text-xs font-semibold uppercase tracking-wide mb-3">Details</h2>
            <div className="text-gray-300 text-sm whitespace-pre-wrap">{record.details}</div>
          </div>
        )}

        {/* Signatures */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-coral text-xs font-semibold uppercase tracking-wide mb-3">Signatures</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {record.signatures.map((sig, i) => (
              <div key={i} className="bg-navy rounded-lg p-3 text-center">
                <img src={sig.dataUrl} alt={`${sig.partyName} signature`} className="h-20 mx-auto mb-2" />
                <p className="text-white text-sm font-medium">{sig.partyName}</p>
                <p className="text-gray-500 text-xs">
                  {new Date(sig.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Crypto footer */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-4 text-center">
          <p className="text-gray-500 text-xs">
            Encrypted with AES-256-GCM | Integrity: HMAC-SHA-256 | Record ID: {record.id.slice(0, 8)}...
          </p>
          <p className="text-gray-600 text-xs mt-1">
            Created with cnsnt - encrypted consent documentation
          </p>
        </div>
      </div>

      {/* Delete confirmation */}
      {showDelete && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <div className="bg-navy-light rounded-2xl p-6 max-w-sm w-full">
            <h3 className="text-white text-lg font-bold mb-2">Delete Record?</h3>
            <p className="text-gray-400 text-sm mb-6">
              This action cannot be undone. The encrypted record will be permanently deleted from your device.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDelete(false)}
                className="flex-1 py-3 rounded-xl border border-gray-600 text-gray-300 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 py-3 rounded-xl bg-red-600 text-white font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
