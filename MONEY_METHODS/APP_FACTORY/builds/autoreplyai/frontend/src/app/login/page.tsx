'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api, { bindToast } from '@/lib/api';
import { useToast } from '@/components/Toast';

export default function LoginPage() {
  const router = useRouter();
  const toast = useToast();
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    bindToast(toast.error, toast.success);
  }, [toast]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!apiKey.trim()) {
      setError('Please enter your API key.');
      return;
    }

    setLoading(true);
    try {
      await api.login(apiKey.trim());
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid API key. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left panel - branding */}
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
            Welcome back
          </h1>
          <p className="text-gray-400 text-lg leading-relaxed max-w-md">
            Sign in to manage your AI support agent, view analytics, and customize your widget.
          </p>
          <div className="mt-12 flex items-center gap-6">
            <div className="flex -space-x-2">
              {['SC', 'MR', 'EP', 'JK'].map((initials) => (
                <div
                  key={initials}
                  className="w-9 h-9 rounded-full bg-surface-100 border-2 border-surface-300 flex items-center justify-center text-xs font-medium text-gray-400"
                >
                  {initials}
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500">
              Trusted by <span className="text-gray-300 font-medium">2,000+</span> businesses
            </p>
          </div>
        </div>
      </div>

      {/* Right panel - form */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-8 bg-surface">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
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
            <h2 className="text-2xl font-bold text-white mb-1">Sign in</h2>
            <p className="text-gray-500 text-sm">Enter your API key to access the dashboard</p>
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
              <label htmlFor="apiKey" className="label">
                API Key
              </label>
              <div className="relative">
                <input
                  id="apiKey"
                  type="text"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="arai_..."
                  className="input font-mono text-sm pr-10"
                  autoComplete="off"
                  spellCheck="false"
                />
                <div className="absolute right-3 top-1/2 -translate-y-1/2">
                  <svg className="w-4.5 h-4.5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
                  </svg>
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-600">
                This is the key you received when you registered.
              </p>
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
                  Signing in...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            {"Don't have an account? "}
            <Link href="/signup" className="text-brand-400 hover:text-brand-300 font-medium transition-colors">
              Register your website
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
