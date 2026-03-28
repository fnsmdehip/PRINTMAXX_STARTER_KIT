import { useState } from 'react';
import { clearAllData } from '../db/store';
import type { ViewName } from '../types';

interface SettingsProps {
  navigate: (view: ViewName) => void;
  isPremium: boolean;
  onLock: () => void;
}

export default function Settings({ navigate, isPremium, onLock }: SettingsProps) {
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [clearing, setClearing] = useState(false);

  const handleClearData = async () => {
    setClearing(true);
    await clearAllData();
    setClearing(false);
    setShowClearConfirm(false);
    navigate('dashboard');
  };

  const handleResetPin = () => {
    localStorage.removeItem('cnsnt_pin_hash');
    localStorage.removeItem('cnsnt_lockout');
    localStorage.removeItem('cnsnt_fail_count');
    onLock();
  };

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6">Settings</h1>

      <div className="space-y-4">
        {/* Account */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-white font-semibold mb-4">Account</h2>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Subscription</p>
                <p className={`text-sm font-medium ${isPremium ? 'text-green-400' : 'text-gray-500'}`}>
                  {isPremium ? 'Pro' : 'Free'}
                </p>
              </div>
              {!isPremium && (
                <button
                  onClick={() => navigate('paywall')}
                  className="px-4 py-2 bg-coral text-white rounded-lg text-sm font-medium"
                >
                  Upgrade
                </button>
              )}
            </div>

            {isPremium && (
              <div className="pt-3 border-t border-gray-700">
                <p className="text-gray-400 text-xs">
                  Manage your subscription through the{' '}
                  <a
                    href="https://billing.stripe.com/p/login/8wMcPU1FqaH60RG144"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-coral underline"
                  >
                    Stripe customer portal
                  </a>
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Security */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-white font-semibold mb-4">Security</h2>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Encryption</p>
                <p className="text-gray-500 text-xs">AES-256-GCM + PBKDF2</p>
              </div>
              <span className="text-green-400 text-sm">Active</span>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Integrity Verification</p>
                <p className="text-gray-500 text-xs">HMAC-SHA-256</p>
              </div>
              <span className="text-green-400 text-sm">Active</span>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Auto-lock timeout</p>
                <p className="text-gray-500 text-xs">2 minutes of inactivity</p>
              </div>
              <span className="text-gray-400 text-sm">On</span>
            </div>

            <div className="pt-3 border-t border-gray-700">
              <button
                onClick={handleResetPin}
                className="text-coral text-sm font-medium"
              >
                Reset PIN
              </button>
              <p className="text-gray-500 text-xs mt-1">
                Warning: You will need to set a new PIN. Existing records encrypted with the old PIN will still require the old PIN to decrypt.
              </p>
            </div>
          </div>
        </div>

        {/* Data */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-white font-semibold mb-4">Data</h2>

          <div className="space-y-3">
            <button
              onClick={() => navigate('backup')}
              className="w-full text-left flex items-center justify-between py-2"
            >
              <span className="text-gray-300 text-sm">Backup & Restore</span>
              <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button
              onClick={() => navigate('audit')}
              className="w-full text-left flex items-center justify-between py-2"
            >
              <span className="text-gray-300 text-sm">Audit Log</span>
              <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <div className="pt-3 border-t border-gray-700">
              <button
                onClick={() => setShowClearConfirm(true)}
                className="text-red-400 text-sm font-medium"
              >
                Clear All Data
              </button>
              <p className="text-gray-500 text-xs mt-1">
                Permanently delete all records and audit log. This cannot be undone.
              </p>
            </div>
          </div>
        </div>

        {/* About */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5">
          <h2 className="text-white font-semibold mb-4">About</h2>
          <div className="space-y-2">
            <p className="text-gray-400 text-sm">cnsnt v1.0.0</p>
            <p className="text-gray-400 text-sm">Encrypted consent documentation</p>
            <div className="pt-3 flex gap-4">
              <a
                href="https://printmaxx-privacy.surge.sh"
                target="_blank"
                rel="noopener noreferrer"
                className="text-coral text-sm"
              >
                Privacy Policy
              </a>
              <a
                href="https://printmaxx-tos.surge.sh"
                target="_blank"
                rel="noopener noreferrer"
                className="text-coral text-sm"
              >
                Terms of Service
              </a>
            </div>
          </div>
        </div>

        {/* Lock button */}
        <button
          onClick={onLock}
          className="w-full py-4 bg-navy-light border border-gray-700 rounded-xl text-gray-300 font-medium flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Lock Vault
        </button>
      </div>

      {/* Clear data confirmation */}
      {showClearConfirm && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <div className="bg-navy-light rounded-2xl p-6 max-w-sm w-full">
            <h3 className="text-white text-lg font-bold mb-2">Clear All Data?</h3>
            <p className="text-gray-400 text-sm mb-6">
              This will permanently delete all records, audit entries, and settings. This action cannot be undone. Consider exporting a backup first.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowClearConfirm(false)}
                className="flex-1 py-3 rounded-xl border border-gray-600 text-gray-300 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleClearData}
                disabled={clearing}
                className="flex-1 py-3 rounded-xl bg-red-600 text-white font-medium disabled:opacity-50"
              >
                {clearing ? 'Clearing...' : 'Clear Everything'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
