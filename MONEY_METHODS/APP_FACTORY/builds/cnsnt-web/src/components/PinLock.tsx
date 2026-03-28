import { useState, useEffect, useCallback } from 'react';
import { hashPin, verifyPin } from '../crypto/vault';
import { addAuditEntry, getLastAuditHash } from '../db/store';
import { computeChainHash } from '../crypto/hmac';

const PIN_HASH_KEY = 'cnsnt_pin_hash';
const LOCKOUT_KEY = 'cnsnt_lockout';
const FAIL_COUNT_KEY = 'cnsnt_fail_count';
const MAX_FAILURES = 5;
const LOCKOUT_DURATION = 15 * 60 * 1000; // 15 minutes

interface PinLockProps {
  onUnlock: (pin: string) => void;
  isSetup: boolean;
}

export default function PinLock({ onUnlock, isSetup }: PinLockProps) {
  const [pin, setPin] = useState('');
  const [confirmPin, setConfirmPin] = useState('');
  const [step, setStep] = useState<'enter' | 'confirm'>('enter');
  const [error, setError] = useState('');
  const [isLocked, setIsLocked] = useState(false);
  const [lockoutRemaining, setLockoutRemaining] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const lockout = localStorage.getItem(LOCKOUT_KEY);
    if (lockout) {
      const until = parseInt(lockout);
      if (Date.now() < until) {
        setIsLocked(true);
        setLockoutRemaining(Math.ceil((until - Date.now()) / 1000));
      } else {
        localStorage.removeItem(LOCKOUT_KEY);
        localStorage.removeItem(FAIL_COUNT_KEY);
      }
    }
  }, []);

  useEffect(() => {
    if (!isLocked) return;
    const interval = setInterval(() => {
      const lockout = localStorage.getItem(LOCKOUT_KEY);
      if (!lockout) {
        setIsLocked(false);
        setLockoutRemaining(0);
        return;
      }
      const until = parseInt(lockout);
      const remaining = Math.ceil((until - Date.now()) / 1000);
      if (remaining <= 0) {
        setIsLocked(false);
        setLockoutRemaining(0);
        localStorage.removeItem(LOCKOUT_KEY);
        localStorage.removeItem(FAIL_COUNT_KEY);
      } else {
        setLockoutRemaining(remaining);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [isLocked]);

  const logAudit = useCallback(async (action: 'login' | 'login_failed' | 'lockout', details: string) => {
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
  }, []);

  const handleDigit = (digit: string) => {
    if (isLocked || loading) return;
    setError('');
    if (step === 'confirm') {
      if (confirmPin.length < 6) setConfirmPin((prev) => prev + digit);
    } else {
      if (pin.length < 6) setPin((prev) => prev + digit);
    }
  };

  const handleDelete = () => {
    if (isLocked || loading) return;
    if (step === 'confirm') {
      setConfirmPin((prev) => prev.slice(0, -1));
    } else {
      setPin((prev) => prev.slice(0, -1));
    }
  };

  useEffect(() => {
    if (isSetup && step === 'enter' && pin.length === 6) {
      setStep('confirm');
    }
  }, [pin, isSetup, step]);

  useEffect(() => {
    if (isSetup && step === 'confirm' && confirmPin.length === 6) {
      handleSetup();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [confirmPin]);

  useEffect(() => {
    if (!isSetup && pin.length === 6) {
      handleVerify();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pin, isSetup]);

  const handleSetup = async () => {
    if (pin !== confirmPin) {
      setError('PINs do not match. Try again.');
      setPin('');
      setConfirmPin('');
      setStep('enter');
      return;
    }
    setLoading(true);
    const hashed = await hashPin(pin);
    localStorage.setItem(PIN_HASH_KEY, hashed);
    await logAudit('login', 'PIN created successfully');
    setLoading(false);
    onUnlock(pin);
  };

  const handleVerify = async () => {
    setLoading(true);
    const stored = localStorage.getItem(PIN_HASH_KEY);
    if (!stored) {
      setLoading(false);
      return;
    }

    const valid = await verifyPin(pin, stored);
    if (valid) {
      localStorage.removeItem(FAIL_COUNT_KEY);
      await logAudit('login', 'PIN verified successfully');
      setLoading(false);
      onUnlock(pin);
    } else {
      const fails = parseInt(localStorage.getItem(FAIL_COUNT_KEY) || '0') + 1;
      localStorage.setItem(FAIL_COUNT_KEY, String(fails));

      if (fails >= MAX_FAILURES) {
        const until = Date.now() + LOCKOUT_DURATION;
        localStorage.setItem(LOCKOUT_KEY, String(until));
        setIsLocked(true);
        setLockoutRemaining(Math.ceil(LOCKOUT_DURATION / 1000));
        await logAudit('lockout', `${MAX_FAILURES} failed attempts - locked for 15 minutes`);
      } else {
        await logAudit('login_failed', `Failed attempt ${fails}/${MAX_FAILURES}`);
        setError(`Wrong PIN. ${MAX_FAILURES - fails} attempts remaining.`);
      }
      setPin('');
      setLoading(false);
    }
  };

  const renderDots = (value: string) => (
    <div className="flex gap-3 justify-center my-6">
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className={`w-4 h-4 rounded-full border-2 transition-all duration-200 ${
            i < value.length
              ? 'bg-coral border-coral scale-110'
              : 'border-gray-500 bg-transparent'
          }`}
        />
      ))}
    </div>
  );

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-navy flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 rounded-2xl bg-navy-light border border-gray-700 flex items-center justify-center mx-auto mb-4">
            <svg viewBox="0 0 40 40" className="w-10 h-10" fill="none">
              <path d="M20 4L8 10v10c0 8.4 5.12 16.24 12 18 6.88-1.76 12-9.6 12-18V10L20 4z" stroke="#e94560" strokeWidth="2.5" fill="none" />
              <path d="M15 20l3 3 7-7" stroke="#e94560" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">cnsnt</h1>
          <p className="text-gray-400 text-sm mt-1">Encrypted Consent Vault</p>
        </div>

        {isLocked ? (
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-red-900/30 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <p className="text-red-400 font-medium mb-2">Account Locked</p>
            <p className="text-gray-400 text-sm">Too many failed attempts.</p>
            <p className="text-white text-2xl font-mono mt-4">{formatTime(lockoutRemaining)}</p>
          </div>
        ) : (
          <>
            <p className="text-center text-gray-300 mb-2">
              {isSetup
                ? step === 'enter'
                  ? 'Create a 6-digit PIN'
                  : 'Confirm your PIN'
                : 'Enter your PIN'}
            </p>

            {renderDots(step === 'confirm' ? confirmPin : pin)}

            {error && (
              <p className="text-red-400 text-center text-sm mb-4">{error}</p>
            )}

            {loading && (
              <p className="text-gray-400 text-center text-sm mb-4">Verifying...</p>
            )}

            {/* Keypad */}
            <div className="grid grid-cols-3 gap-3 max-w-xs mx-auto">
              {['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'del'].map(
                (key) => {
                  if (key === '') return <div key="empty" />;
                  if (key === 'del') {
                    return (
                      <button
                        key="del"
                        onClick={handleDelete}
                        className="h-16 rounded-xl bg-navy-light text-gray-400 text-lg font-medium active:bg-gray-700 transition-colors flex items-center justify-center"
                      >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2M3 12l6.414-6.414A2 2 0 0110.828 5H21a2 2 0 012 2v10a2 2 0 01-2 2H10.828a2 2 0 01-1.414-.586L3 12z" />
                        </svg>
                      </button>
                    );
                  }
                  return (
                    <button
                      key={key}
                      onClick={() => handleDigit(key)}
                      className="h-16 rounded-xl bg-navy-light text-white text-2xl font-medium active:bg-coral/20 active:scale-95 transition-all"
                    >
                      {key}
                    </button>
                  );
                }
              )}
            </div>
          </>
        )}

        <p className="text-gray-600 text-xs text-center mt-8">
          Your data is encrypted and stored locally on this device only.
        </p>
      </div>
    </div>
  );
}
