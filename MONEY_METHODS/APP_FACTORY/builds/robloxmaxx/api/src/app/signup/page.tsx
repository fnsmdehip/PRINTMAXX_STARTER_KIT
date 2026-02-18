'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Registration failed');
        return;
      }

      localStorage.setItem('rmx_token', data.token);
      setApiKey(data.apiKey);
      setSuccess(true);
    } catch {
      setError('Network error. Try again.');
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <main className="auth-page">
        <div className="auth-card">
          <h1>You&apos;re in</h1>
          <p className="auth-subtitle">
            250 free actions. Here&apos;s your API key for the Roblox Studio plugin.
          </p>

          <div className="api-key-display">
            <label>Your API key</label>
            <div className="api-key-box">
              <code>{apiKey}</code>
              <button
                className="copy-btn"
                onClick={() => {
                  navigator.clipboard.writeText(apiKey);
                }}
              >
                Copy
              </button>
            </div>
          </div>

          <div className="next-steps">
            <h3>Next steps</h3>
            <ol>
              <li>Install the RobloxMaxx plugin in Roblox Studio</li>
              <li>Paste your API key in the plugin settings</li>
              <li>Select a genre and describe your game</li>
            </ol>
          </div>

          <div className="auth-actions">
            <Link href="/dashboard" className="cta-btn" style={{ display: 'block', textAlign: 'center' }}>
              Go to dashboard
            </Link>
            <Link href="/docs" className="auth-link" style={{ display: 'block', textAlign: 'center', marginTop: 16 }}>
              Read the docs
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="auth-page">
      <div className="auth-card">
        <h1>Create your account</h1>
        <p className="auth-subtitle">
          250 free actions per month. No credit card required.
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="auth-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@email.com"
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="8+ characters"
              required
              minLength={8}
              autoComplete="new-password"
            />
          </div>

          <button type="submit" className="cta-btn auth-submit" disabled={loading}>
            {loading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account? <Link href="/login">Log in</Link>
        </p>
      </div>
    </main>
  );
}
