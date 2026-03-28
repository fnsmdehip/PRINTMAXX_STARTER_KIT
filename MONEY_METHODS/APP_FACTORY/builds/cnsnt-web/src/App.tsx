import { useState, useEffect, useCallback, useRef } from 'react';
import PinLock from './components/PinLock';
import Dashboard from './components/Dashboard';
import RecordCreator from './components/RecordCreator';
import RecordViewer from './components/RecordViewer';
import TemplateLibrary from './components/TemplateLibrary';
import AuditLog from './components/AuditLog';
import BackupManager from './components/BackupManager';
import Settings from './components/Settings';
import Paywall from './components/Paywall';
import VideoConsent from './components/VideoConsent';
import VideoPlayer from './components/VideoPlayer';
import type { ViewName } from './types';

const AUTO_LOCK_MS = 2 * 60 * 1000; // 2 minutes
const PREMIUM_KEY = 'cnsnt_premium';
const PIN_HASH_KEY = 'cnsnt_pin_hash';

export default function App() {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [isPinSet, setIsPinSet] = useState(false);
  const [isPremium, setIsPremium] = useState(false);
  const [currentView, setCurrentView] = useState<ViewName>('dashboard');
  const [selectedRecord, setSelectedRecord] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [pin, setPin] = useState('');
  const lockTimerRef = useRef<number | null>(null);

  // Check if PIN is set on mount
  useEffect(() => {
    const pinHash = localStorage.getItem(PIN_HASH_KEY);
    setIsPinSet(!!pinHash);
    setIsPremium(localStorage.getItem(PREMIUM_KEY) === 'true');
  }, []);

  // Auto-lock on inactivity
  const resetLockTimer = useCallback(() => {
    if (lockTimerRef.current) {
      clearTimeout(lockTimerRef.current);
    }
    if (isUnlocked) {
      lockTimerRef.current = window.setTimeout(() => {
        setIsUnlocked(false);
        setPin('');
        setCurrentView('dashboard');
      }, AUTO_LOCK_MS);
    }
  }, [isUnlocked]);

  useEffect(() => {
    const events = ['mousedown', 'mousemove', 'keypress', 'touchstart', 'scroll'];
    const handler = () => resetLockTimer();
    events.forEach((e) => document.addEventListener(e, handler, { passive: true }));
    resetLockTimer();
    return () => {
      events.forEach((e) => document.removeEventListener(e, handler));
      if (lockTimerRef.current) clearTimeout(lockTimerRef.current);
    };
  }, [resetLockTimer]);

  const handleUnlock = (userPin: string) => {
    setPin(userPin);
    setIsUnlocked(true);
    setIsPinSet(true);
    setCurrentView('dashboard');
    resetLockTimer();
  };

  const handleLock = () => {
    setIsUnlocked(false);
    setPin('');
    setCurrentView('dashboard');
  };

  const navigate = (view: ViewName, extra?: string) => {
    if (view === 'viewer' && extra) {
      setSelectedRecord(extra);
    }
    if (view === 'video-player' && extra) {
      setSelectedVideo(extra);
    }
    if (view === 'create' && extra) {
      setSelectedTemplate(extra);
    } else if (view === 'create') {
      setSelectedTemplate(null);
    }
    setCurrentView(view);
    resetLockTimer();
  };

  const activatePremium = () => {
    localStorage.setItem(PREMIUM_KEY, 'true');
    setIsPremium(true);
    setCurrentView('dashboard');
  };

  // PIN screen
  if (!isUnlocked) {
    return <PinLock onUnlock={handleUnlock} isSetup={!isPinSet} />;
  }

  // Paywall
  if (currentView === 'paywall') {
    return <Paywall navigate={navigate} onActivate={activatePremium} />;
  }

  return (
    <div className="min-h-screen bg-navy">
      {/* Navigation bar - desktop sidebar / mobile bottom */}
      <div className="lg:flex">
        {/* Desktop sidebar */}
        <nav className="hidden lg:flex lg:flex-col lg:w-64 lg:min-h-screen bg-navy-dark border-r border-gray-800 p-4">
          <div className="flex items-center gap-3 mb-8 px-2">
            <div className="w-10 h-10 rounded-xl bg-navy-light border border-gray-700 flex items-center justify-center">
              <svg viewBox="0 0 40 40" className="w-6 h-6" fill="none">
                <path d="M20 4L8 10v10c0 8.4 5.12 16.24 12 18 6.88-1.76 12-9.6 12-18V10L20 4z" stroke="#e94560" strokeWidth="2.5" fill="none" />
                <path d="M15 20l3 3 7-7" stroke="#e94560" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div>
              <h1 className="text-white font-bold text-lg">cnsnt</h1>
              {isPremium && <span className="text-coral text-xs font-semibold">PRO</span>}
            </div>
          </div>

          <div className="space-y-1 flex-1">
            {[
              { view: 'dashboard' as ViewName, label: 'Vault', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
              { view: 'templates' as ViewName, label: 'Templates', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
              { view: 'audit' as ViewName, label: 'Audit Log', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
              { view: 'backup' as ViewName, label: 'Backup', icon: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12' },
              { view: 'settings' as ViewName, label: 'Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
            ].map(({ view, label, icon }) => (
              <button
                key={view}
                onClick={() => navigate(view)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors ${
                  currentView === view
                    ? 'bg-coral/10 text-coral'
                    : 'text-gray-400 hover:text-white hover:bg-navy-light'
                }`}
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} />
                </svg>
                <span className="text-sm font-medium">{label}</span>
              </button>
            ))}
          </div>

          <button
            onClick={handleLock}
            className="mt-auto flex items-center gap-3 px-3 py-2.5 text-gray-500 hover:text-white transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span className="text-sm">Lock</span>
          </button>
        </nav>

        {/* Main content */}
        <main className="flex-1 pb-20 lg:pb-0">
          {currentView === 'dashboard' && (
            <Dashboard navigate={navigate} isPremium={isPremium} />
          )}
          {currentView === 'create' && (
            <RecordCreator
              pin={pin}
              templateId={selectedTemplate}
              navigate={navigate}
              isPremium={isPremium}
            />
          )}
          {currentView === 'viewer' && selectedRecord && (
            <RecordViewer
              recordId={selectedRecord}
              pin={pin}
              navigate={navigate}
              isPremium={isPremium}
            />
          )}
          {currentView === 'templates' && (
            <TemplateLibrary navigate={navigate} isPremium={isPremium} />
          )}
          {currentView === 'audit' && <AuditLog navigate={navigate} />}
          {currentView === 'backup' && <BackupManager navigate={navigate} />}
          {currentView === 'video-consent' && (
            <VideoConsent pin={pin} navigate={navigate} isPremium={isPremium} />
          )}
          {currentView === 'video-player' && selectedVideo && (
            <VideoPlayer videoId={selectedVideo} pin={pin} navigate={navigate} />
          )}
          {currentView === 'settings' && (
            <Settings navigate={navigate} isPremium={isPremium} onLock={handleLock} />
          )}
        </main>
      </div>

      {/* Mobile bottom nav */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-navy-dark border-t border-gray-800 px-2 py-2 z-40">
        <div className="flex items-center justify-around max-w-lg mx-auto">
          {[
            { view: 'dashboard' as ViewName, label: 'Vault', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
            { view: 'templates' as ViewName, label: 'Templates', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
            { view: 'create' as ViewName, label: 'New', icon: 'M12 4v16m8-8H4' },
            { view: 'audit' as ViewName, label: 'Audit', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
            { view: 'settings' as ViewName, label: 'Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
          ].map(({ view, label, icon }) => (
            <button
              key={view}
              onClick={() => navigate(view)}
              className={`flex flex-col items-center gap-1 px-3 py-1 rounded-lg transition-colors ${
                currentView === view ? 'text-coral' : 'text-gray-500'
              }`}
            >
              {view === 'create' ? (
                <div className="w-10 h-10 -mt-4 bg-coral rounded-full flex items-center justify-center shadow-lg shadow-coral/30">
                  <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d={icon} />
                  </svg>
                </div>
              ) : (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} />
                </svg>
              )}
              <span className="text-xs">{label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Legal footer - visible on desktop */}
      <footer className="hidden lg:block fixed bottom-0 right-0 p-3 text-gray-600 text-xs">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Data never leaves your device
          </span>
          <a href="https://printmaxx-privacy.surge.sh" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">Privacy</a>
          <a href="https://printmaxx-tos.surge.sh" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">Terms</a>
        </div>
      </footer>
    </div>
  );
}
