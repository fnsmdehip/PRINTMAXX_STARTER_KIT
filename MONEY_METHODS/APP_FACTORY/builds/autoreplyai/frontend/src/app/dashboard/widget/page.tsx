'use client';

import { useEffect, useState, useCallback } from 'react';
import api from '@/lib/api';
import { useToast } from '@/components/Toast';
import { Skeleton } from '@/components/Skeleton';

interface WidgetSettings {
  primaryColor: string;
  position: string;
  greeting: string;
}

const PRESET_COLORS = [
  '#3B82F6', '#2563EB', '#6366F1', '#8B5CF6',
  '#EC4899', '#EF4444', '#F59E0B', '#10B981',
  '#06B6D4', '#0EA5E9', '#F97316', '#84CC16',
];

export default function WidgetSettingsPage() {
  const toast = useToast();
  const [settings, setSettings] = useState<WidgetSettings>({
    primaryColor: '#3B82F6',
    position: 'bottom-right',
    greeting: 'Hi! How can I help you today?',
  });
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [previewOpen, setPreviewOpen] = useState(true);

  useEffect(() => {
    api
      .getMe()
      .then((data) => {
        if (data.settings) setSettings(data.settings);
        setApiKey(api.getApiKey() || '');
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.updateSettings(settings);
    } catch {
      // Toast handled by API client
    } finally {
      setSaving(false);
    }
  };

  const embedCode = `<script src="${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/widget/widget.js" data-key="${apiKey}"></script>`;

  const copyEmbed = useCallback(() => {
    navigator.clipboard.writeText(embedCode);
    setCopied(true);
    toast.success('Copied', 'Embed code copied to clipboard.');
    setTimeout(() => setCopied(false), 2000);
  }, [embedCode, toast]);

  if (loading) {
    return (
      <div className="max-w-5xl grid lg:grid-cols-5 gap-6">
        <div className="lg:col-span-3 space-y-6">
          <div className="card p-6 space-y-4">
            <Skeleton className="h-5 w-40" />
            <div className="flex gap-2">
              {Array.from({ length: 8 }).map((_, i) => (
                <Skeleton key={i} className="w-10 h-10 rounded-full" />
              ))}
            </div>
            <Skeleton className="h-10 w-full rounded-lg" />
            <Skeleton className="h-10 w-full rounded-lg" />
          </div>
        </div>
        <div className="lg:col-span-2">
          <div className="card p-6">
            <Skeleton className="h-5 w-24 mb-4" />
            <Skeleton className="h-72 w-full rounded-lg" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl grid lg:grid-cols-5 gap-6">
      {/* Settings panel */}
      <div className="lg:col-span-3 space-y-6">
        {/* Appearance */}
        <div className="card p-6 space-y-6">
          <h2 className="section-heading text-sm">Widget Appearance</h2>

          {/* Color */}
          <div>
            <label className="label">Primary Color</label>
            <div className="flex items-center gap-2 flex-wrap">
              {PRESET_COLORS.map((color) => (
                <button
                  key={color}
                  onClick={() => setSettings({ ...settings, primaryColor: color })}
                  className={`w-9 h-9 rounded-full border-2 transition-all duration-150 hover:scale-110 ${
                    settings.primaryColor === color
                      ? 'border-white scale-110 shadow-lg'
                      : 'border-transparent'
                  }`}
                  style={{ backgroundColor: color }}
                  aria-label={`Color ${color}`}
                />
              ))}
              <div className="relative">
                <input
                  type="color"
                  value={settings.primaryColor}
                  onChange={(e) => setSettings({ ...settings, primaryColor: e.target.value })}
                  className="w-9 h-9 rounded-full cursor-pointer border-0 bg-transparent"
                  title="Custom color"
                />
              </div>
              <span className="text-xs font-mono text-gray-600 ml-1">{settings.primaryColor}</span>
            </div>
          </div>

          {/* Position */}
          <div>
            <label className="label">Widget Position</label>
            <div className="flex gap-2">
              {[
                { value: 'bottom-right', label: 'Bottom Right' },
                { value: 'bottom-left', label: 'Bottom Left' },
              ].map((pos) => (
                <button
                  key={pos.value}
                  onClick={() => setSettings({ ...settings, position: pos.value })}
                  className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-medium transition-all border ${
                    settings.position === pos.value
                      ? 'bg-brand-500/15 text-brand-400 border-brand-500/30'
                      : 'bg-surface-300 text-gray-400 border-white/[0.06] hover:border-white/[0.1] hover:text-gray-300'
                  }`}
                >
                  <div className={`w-4 h-4 border border-current rounded-sm relative ${
                    settings.position === pos.value ? 'border-brand-400' : 'border-gray-600'
                  }`}>
                    <div
                      className={`absolute w-1.5 h-1.5 rounded-full ${
                        settings.position === pos.value ? 'bg-brand-400' : 'bg-gray-600'
                      }`}
                      style={{
                        bottom: '1px',
                        [pos.value === 'bottom-right' ? 'right' : 'left']: '1px',
                      }}
                    />
                  </div>
                  {pos.label}
                </button>
              ))}
            </div>
          </div>

          {/* Greeting */}
          <div>
            <label className="label">Greeting Message</label>
            <input
              type="text"
              value={settings.greeting}
              onChange={(e) => setSettings({ ...settings, greeting: e.target.value })}
              className="input"
              maxLength={200}
            />
            <p className="text-[11px] text-gray-600 mt-1">
              {settings.greeting.length}/200 characters
            </p>
          </div>

          <button
            onClick={handleSave}
            disabled={saving}
            className="btn-primary text-xs py-2.5"
          >
            {saving ? (
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Saving...
              </div>
            ) : (
              'Save Settings'
            )}
          </button>
        </div>

        {/* Embed Code */}
        <div className="card p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="section-heading text-sm">Embed Code</h2>
            <button
              onClick={copyEmbed}
              className={`btn-secondary text-xs py-1.5 ${copied ? 'text-success-400 border-success-500/20' : ''}`}
            >
              {copied ? (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  Copied
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                  </svg>
                  Copy
                </>
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500">
            Add this before the closing <code className="font-mono text-brand-400">&lt;/body&gt;</code> tag on your website.
          </p>
          <div className="bg-surface-300 rounded-lg p-4 font-mono text-xs text-success-400 break-all border border-white/[0.04] select-all leading-relaxed">
            {embedCode}
          </div>
        </div>
      </div>

      {/* Live Preview */}
      <div className="lg:col-span-2">
        <div className="card p-5 lg:sticky lg:top-20">
          <h2 className="section-heading text-sm mb-4">Live Preview</h2>
          <div className="relative bg-surface-300 rounded-lg overflow-hidden border border-white/[0.04]" style={{ height: '440px' }}>
            {/* Fake website content */}
            <div className="p-4 space-y-3">
              <div className="h-3 bg-white/[0.03] rounded w-3/4" />
              <div className="h-3 bg-white/[0.03] rounded w-1/2" />
              <div className="h-20 bg-white/[0.02] rounded-lg mt-4" />
              <div className="h-3 bg-white/[0.03] rounded w-2/3" />
              <div className="h-3 bg-white/[0.03] rounded w-1/3" />
            </div>

            {/* Widget preview */}
            <div
              className="absolute"
              style={{
                bottom: '16px',
                [settings.position === 'bottom-right' ? 'right' : 'left']: '16px',
              }}
            >
              {/* Chat window */}
              {previewOpen && (
                <div
                  className="mb-3 w-[260px] bg-white rounded-2xl shadow-2xl shadow-black/40 overflow-hidden animate-scale-in"
                  style={{
                    [settings.position === 'bottom-right' ? 'right' : 'left']: '0',
                    position: 'absolute',
                    bottom: '56px',
                  }}
                >
                  {/* Header */}
                  <div
                    className="px-4 py-3 flex items-center justify-between"
                    style={{ backgroundColor: settings.primaryColor }}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </div>
                      <span className="text-white text-xs font-semibold">Support</span>
                    </div>
                    <button
                      onClick={() => setPreviewOpen(false)}
                      className="text-white/70 hover:text-white text-sm"
                    >
                      x
                    </button>
                  </div>

                  {/* Messages */}
                  <div className="p-3 bg-gray-50 space-y-2" style={{ minHeight: '140px' }}>
                    <div className="flex gap-2">
                      <div className="bg-gray-200 text-gray-700 px-3 py-2 rounded-xl rounded-bl-md text-[11px] max-w-[80%] leading-relaxed">
                        {settings.greeting}
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <div
                        className="text-white px-3 py-2 rounded-xl rounded-br-md text-[11px] max-w-[80%]"
                        style={{ backgroundColor: settings.primaryColor }}
                      >
                        How do I track my order?
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <div className="bg-gray-200 text-gray-700 px-3 py-2 rounded-xl rounded-bl-md text-[11px] max-w-[80%] leading-relaxed">
                        You can track your order by visiting our tracking page with your order number.
                      </div>
                    </div>
                  </div>

                  {/* Input */}
                  <div className="p-2 bg-white border-t border-gray-100 flex gap-2">
                    <div className="flex-1 bg-gray-100 rounded-full px-3 py-1.5 text-[10px] text-gray-400">
                      Type a message...
                    </div>
                    <div
                      className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: settings.primaryColor }}
                    >
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                      </svg>
                    </div>
                  </div>
                </div>
              )}

              {/* Toggle button */}
              <button
                onClick={() => setPreviewOpen(!previewOpen)}
                className="w-12 h-12 rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-110"
                style={{ backgroundColor: settings.primaryColor }}
              >
                {previewOpen ? (
                  <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
