'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface UsageData {
  plan: string;
  actionsUsed: number;
  actionsLimit: number;
  actionsRemaining: number;
}

export default function DashboardPage() {
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const router = useRouter();

  // We store the token from localStorage
  const [token, setToken] = useState('');

  useEffect(() => {
    const t = localStorage.getItem('rmx_token');
    if (!t) {
      router.push('/login');
      return;
    }
    setToken(t);

    fetch('/api/usage', {
      headers: { Authorization: `Bearer ${t}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Unauthorized');
        return res.json();
      })
      .then((data) => {
        setUsage(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Session expired. Please log in again.');
        setLoading(false);
        localStorage.removeItem('rmx_token');
      });
  }, [router]);

  function handleCopy() {
    navigator.clipboard.writeText(token);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function handleLogout() {
    localStorage.removeItem('rmx_token');
    router.push('/');
  }

  if (loading) {
    return (
      <main className="dashboard-page">
        <div className="dashboard-container">
          <p style={{ color: 'var(--text-muted)' }}>Loading...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="dashboard-page">
        <div className="dashboard-container">
          <div className="auth-error">{error}</div>
          <Link href="/login" className="cta-btn" style={{ display: 'inline-block', marginTop: 16 }}>
            Log in
          </Link>
        </div>
      </main>
    );
  }

  const usagePercent = usage
    ? Math.round((usage.actionsUsed / usage.actionsLimit) * 100)
    : 0;

  return (
    <main className="dashboard-page">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <button className="btn-secondary" onClick={handleLogout}>
            Log out
          </button>
        </div>

        {/* Usage stats */}
        <div className="dashboard-grid">
          <div className="dash-card">
            <h3>Plan</h3>
            <div className="dash-stat">{usage?.plan || 'free'}</div>
            <Link href="/#pricing" className="dash-upgrade-link">
              Upgrade
            </Link>
          </div>

          <div className="dash-card">
            <h3>Actions used</h3>
            <div className="dash-stat">
              {usage?.actionsUsed ?? 0}
              <span className="dash-stat-sub"> / {usage?.actionsLimit ?? 250}</span>
            </div>
            <div className="usage-bar">
              <div
                className="usage-bar-fill"
                style={{ width: `${Math.min(usagePercent, 100)}%` }}
              />
            </div>
          </div>

          <div className="dash-card">
            <h3>Remaining</h3>
            <div className="dash-stat">{usage?.actionsRemaining ?? 0}</div>
          </div>
        </div>

        {/* API Key */}
        <div className="dash-section">
          <h2>Your API token</h2>
          <p className="dash-description">
            Paste this into the RobloxMaxx plugin in Roblox Studio.
          </p>
          <div className="api-key-box">
            <code>{token.slice(0, 20)}...{token.slice(-8)}</code>
            <button className="copy-btn" onClick={handleCopy}>
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
        </div>

        {/* Quick start */}
        <div className="dash-section">
          <h2>Quick start</h2>
          <div className="quick-start-steps">
            <div className="qs-step">
              <div className="qs-number">1</div>
              <div>
                <h4>Install the plugin</h4>
                <p>
                  Download <code>RobloxMaxxPlugin.lua</code> and place it in your
                  Roblox Studio plugins folder. Or install from the Creator Store.
                </p>
                <a href="/api/download" className="btn-secondary" style={{ marginTop: 8, display: 'inline-block' }}>
                  Download plugin
                </a>
              </div>
            </div>

            <div className="qs-step">
              <div className="qs-number">2</div>
              <div>
                <h4>Paste your token</h4>
                <p>
                  Open the plugin panel in Roblox Studio. Paste your API token in
                  the auth field. Select &quot;RobloxMaxx&quot; as the provider.
                </p>
              </div>
            </div>

            <div className="qs-step">
              <div className="qs-number">3</div>
              <div>
                <h4>Generate code</h4>
                <p>
                  Pick a genre, describe what you want, and hit Generate. The AI
                  creates scripts directly in your game. Tycoons, obbys, simulators,
                  RPGs, horror. Anything.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="dash-section">
          <h2>Resources</h2>
          <div className="dash-links">
            <Link href="/docs" className="dash-link-card">
              <h4>Documentation</h4>
              <p>API reference, genre guide, tutorials</p>
            </Link>
            <Link href="/#pricing" className="dash-link-card">
              <h4>Upgrade plan</h4>
              <p>More actions, faster models, team seats</p>
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
