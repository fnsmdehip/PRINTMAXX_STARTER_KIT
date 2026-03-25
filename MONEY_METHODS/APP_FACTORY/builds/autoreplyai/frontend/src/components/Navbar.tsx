'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

const NAV_LINKS = [
  { href: '#features', label: 'Features' },
  { href: '#pricing', label: 'Pricing' },
  { href: '#testimonials', label: 'Testimonials' },
  { href: '#faq', label: 'FAQ' },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsLoggedIn(!!localStorage.getItem('arai_api_key'));
    }

    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-surface/90 backdrop-blur-xl border-b border-white/[0.06] shadow-lg shadow-black/20'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center transition-transform group-hover:scale-105">
              <svg className="w-4.5 h-4.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-lg font-bold text-white tracking-tight">
              AutoReply<span className="text-brand-400">AI</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="px-3.5 py-2 text-sm text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/[0.04]"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-3">
            {isLoggedIn ? (
              <Link href="/dashboard" className="btn-primary text-sm">
                Dashboard
              </Link>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors"
                >
                  Sign In
                </Link>
                <Link href="/signup" className="btn-primary text-sm">
                  Get Started Free
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/[0.05] transition-colors"
            aria-label="Toggle navigation"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden bg-surface-200/95 backdrop-blur-xl border-t border-white/[0.06] animate-fade-in-down">
          <div className="px-4 py-4 space-y-1">
            {NAV_LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="block px-4 py-2.5 text-sm text-gray-300 hover:text-white rounded-lg hover:bg-white/[0.05] transition-colors"
              >
                {link.label}
              </a>
            ))}
            <div className="pt-3 mt-3 border-t border-white/[0.06] space-y-2">
              {isLoggedIn ? (
                <Link
                  href="/dashboard"
                  className="block text-center btn-primary w-full"
                  onClick={() => setMobileOpen(false)}
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="block text-center px-4 py-2.5 text-sm text-gray-300 hover:text-white rounded-lg hover:bg-white/[0.05]"
                    onClick={() => setMobileOpen(false)}
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="block text-center btn-primary w-full"
                    onClick={() => setMobileOpen(false)}
                  >
                    Get Started Free
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
