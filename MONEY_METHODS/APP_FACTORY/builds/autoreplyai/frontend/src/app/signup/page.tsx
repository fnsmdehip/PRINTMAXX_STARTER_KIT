'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api, { bindToast } from '@/lib/api';
import { useToast } from '@/components/Toast';

export default function SignupPage() {
  const router = useRouter();
  const toast = useToast();
  const [step, setStep] = useState<'form' | 'success'>('form');
  const [form, setForm] = useState({ name: '', url: '', email: '' });
  const [generatedKey, setGeneratedKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    bindToast(toast.error, toast.success);
  }, [toast]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!form.name.trim() || !form.url.trim() || !form.email.trim()) {
      setError('All fields are required.');
      return;
    }

    setLoading(true);
    try {
      const data = await api.register(form.name.trim(), form.url.trim(), form.email.trim());
      api.setApiKey(data.apiKey);
      setGeneratedKey(data.apiKey);
      setStep('success');
    } catch (err: any) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  const copyKey = useCallback(() => {
    navigator.clipboard.writeText(generatedKey);
    setCopied(true);
    toast.success('Copied', 'API key copied to clipboard.');
    setTimeout(() => setCopied(false), 2000);
  }, [generatedKey, toast]);

  if (step === 'success') {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 bg-surface">
        <div className="w-full max-w-lg animate-scale-in">
          <div className="card p-8 lg:p-10 text-center">
            <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-success-500/15 border border-success-500/25 flex items-center justify-center">
              <svg className="w-8 h-8 text-success-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <h2 className="text-2xl font-bold text-white mb-2">You are all set!</h2>
            <p className="text-gray-400 text-sm mb-8">
              Save this API key securely. You will need it to sign in.
            </p>

            <div className="relative group">
              <div className="bg-surface-300 rounded-lg p-4 font-mono text-sm text-success-400 break-all text-left border border-white/[0.06] select-all">
                {generatedKey}
              </div>
              <button
                onClick={copyKey}
                className="absolute top-2 right-2 p-2 rounded-md bg-surface-100 text-gray-400 hover:text-white border border-white/[0.08] transition-all hover:border-white/[0.15] opacity-0 group-hover:opacity-100"
                aria-label="Copy API key"
              >
                {copied ? (
                  <svg className="w-4 h-4 text-success-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                  </svg>
                )}
              </button>
            </div>

            <div className="flex items-center gap-2 mt-4 p-3 rounded-lg bg-warning-500/10 border border-warning-500/20">
              <svg className="w-4 h-4 text-warning-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              <p className="text-xs text-warning-400">
                This key is shown only once. Copy and store it securely.
              </p>
            </div>

            <button
              onClick={() => router.push('/dashboard')}
              className="btn-primary w-full py-3 mt-8"
            >
              Go to Dashboard
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-surface-300 relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-30" />
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[400px] h-[400px] bg-brand-500/10 rounded-full blur-[100px]" />
        <div className="relative flex flex-col justify-center px-16">
          <Link href="/" className="flex items-center gap-2.5 mb-12">
            <div className="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-xl font-bold text-white">
              AutoReply<span className="text-brand-400">AI</span>
            </span>
          </Link>
          <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
            Get started in minutes
          </h1>
          <p className="text-gray-400 text-lg leading-relaxed max-w-md">
            Register your website, set up your knowledge base, and deploy your AI support agent with a single line of code.
          </p>
          <div className="mt-12 space-y-4">
            {[
              { step: '1', text: 'Register your website' },
              { step: '2', text: 'Add knowledge base content' },
              { step: '3', text: 'Embed widget on your site' },
            ].map((item) => (
              <div key={item.step} className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-full bg-brand-500/15 border border-brand-500/25 flex items-center justify-center text-sm font-semibold text-brand-400">
                  {item.step}
                </div>
                <span className="text-sm text-gray-400">{item.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-8 bg-surface">
        <div className="w-full max-w-md">
          <div className="lg:hidden mb-8">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span className="text-lg font-bold text-white">
                AutoReply<span className="text-brand-400">AI</span>
              </span>
            </Link>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-1">Create your account</h2>
            <p className="text-gray-500 text-sm">Free plan includes 100 messages per month</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="flex items-start gap-3 bg-danger-500/10 border border-danger-500/20 rounded-lg px-4 py-3">
                <svg className="w-5 h-5 text-danger-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
                <p className="text-sm text-danger-400">{error}</p>
              </div>
            )}

            <div>
              <label className="label">Website Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="input"
                autoComplete="organization"
              />
            </div>

            <div>
              <label className="label">Website URL</label>
              <input
                type="url"
                value={form.url}
                onChange={(e) => setForm({ ...form, url: e.target.value })}
                placeholder="https://"
                className="input"
                autoComplete="url"
              />
            </div>

            <div>
              <label className="label">Email Address</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="input"
                autoComplete="email"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Creating account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            Already have an account?{' '}
            <Link href="/login" className="text-brand-400 hover:text-brand-300 font-medium transition-colors">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
