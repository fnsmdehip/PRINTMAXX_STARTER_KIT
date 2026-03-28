import { useState, useEffect } from 'react';
import { getAllRecords, getRecordCount, searchRecords } from '../db/store';
import type { EncryptedRecord, ViewName } from '../types';

interface DashboardProps {
  navigate: (view: ViewName, recordId?: string) => void;
  isPremium: boolean;
}

const FREE_RECORD_LIMIT = 3;

export default function Dashboard({ navigate, isPremium }: DashboardProps) {
  const [records, setRecords] = useState<EncryptedRecord[]>([]);
  const [recordCount, setRecordCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    const all = await getAllRecords();
    const count = await getRecordCount();
    setRecords(all);
    setRecordCount(count);
    setLoading(false);
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      const all = await getAllRecords();
      setRecords(all);
    } else {
      const results = await searchRecords(query);
      setRecords(results);
    }
  };

  const canCreateMore = isPremium || recordCount < FREE_RECORD_LIMIT;

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  return (
    <div className="p-4 md:p-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Your Vault</h1>
          <p className="text-gray-400 text-sm mt-1">
            {recordCount} record{recordCount !== 1 ? 's' : ''} stored
            {!isPremium && (
              <span className="text-coral"> ({FREE_RECORD_LIMIT - recordCount} free remaining)</span>
            )}
          </p>
        </div>
        {isPremium && (
          <span className="px-3 py-1 bg-coral/20 text-coral text-xs font-semibold rounded-full">PRO</span>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <button
          onClick={() => {
            if (canCreateMore) {
              navigate('create');
            } else {
              navigate('paywall');
            }
          }}
          className="bg-coral text-white rounded-xl p-4 text-left active:scale-[0.98] transition-transform"
        >
          <svg className="w-6 h-6 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-sm font-medium">New Record</span>
        </button>

        <button
          onClick={() => navigate('templates')}
          className="bg-navy-light border border-gray-700 text-white rounded-xl p-4 text-left active:scale-[0.98] transition-transform"
        >
          <svg className="w-6 h-6 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="text-sm font-medium">Templates</span>
        </button>

        <button
          onClick={() => navigate('backup')}
          className="bg-navy-light border border-gray-700 text-white rounded-xl p-4 text-left active:scale-[0.98] transition-transform"
        >
          <svg className="w-6 h-6 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <span className="text-sm font-medium">Backup</span>
        </button>

        <button
          onClick={() => navigate('audit')}
          className="bg-navy-light border border-gray-700 text-white rounded-xl p-4 text-left active:scale-[0.98] transition-transform"
        >
          <svg className="w-6 h-6 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <span className="text-sm font-medium">Audit Log</span>
        </button>
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search records..."
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          className="w-full bg-navy-light border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none transition-colors"
        />
      </div>

      {/* Records List */}
      {loading ? (
        <div className="text-center py-12">
          <div className="w-8 h-8 border-2 border-coral border-t-transparent rounded-full animate-spin mx-auto" />
        </div>
      ) : records.length === 0 ? (
        <div className="text-center py-16">
          <div className="w-20 h-20 rounded-full bg-navy-light flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <p className="text-gray-400 text-lg font-medium">
            {searchQuery ? 'No records found' : 'Your vault is empty'}
          </p>
          <p className="text-gray-500 text-sm mt-2">
            {searchQuery ? 'Try a different search' : 'Create your first consent record'}
          </p>
          {!searchQuery && (
            <button
              onClick={() => navigate('create')}
              className="mt-6 px-6 py-3 bg-coral text-white rounded-xl font-medium active:scale-[0.98] transition-transform"
            >
              Create Record
            </button>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {records.map((record) => (
            <button
              key={record.id}
              onClick={() => navigate('viewer', record.id)}
              className="w-full bg-navy-light border border-gray-700 rounded-xl p-4 text-left hover:border-gray-600 active:scale-[0.99] transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="min-w-0 flex-1">
                  <h3 className="text-white font-medium truncate">{record.title}</h3>
                  <p className="text-gray-400 text-sm mt-1">
                    {formatDate(record.createdAt)}
                  </p>
                </div>
                <svg className="w-5 h-5 text-gray-500 flex-shrink-0 ml-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Upgrade Banner (free users) */}
      {!isPremium && recordCount > 0 && (
        <div className="mt-8 bg-gradient-to-r from-coral/20 to-ocean/20 border border-coral/30 rounded-xl p-4">
          <p className="text-white font-medium">Unlock Unlimited Records</p>
          <p className="text-gray-300 text-sm mt-1">
            Upgrade to Pro for unlimited records, all templates, and PDF export.
          </p>
          <button
            onClick={() => navigate('paywall')}
            className="mt-3 px-5 py-2 bg-coral text-white rounded-lg text-sm font-medium"
          >
            Upgrade to Pro
          </button>
        </div>
      )}
    </div>
  );
}
