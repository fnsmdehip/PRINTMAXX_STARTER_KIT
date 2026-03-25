'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import api, { bindToast } from '@/lib/api';
import { useToast } from '@/components/Toast';
import { Skeleton } from '@/components/Skeleton';

const NAV_ITEMS = [
  {
    href: '/dashboard',
    label: 'Overview',
    icon: 'M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25',
  },
  {
    href: '/dashboard/knowledge',
    label: 'Knowledge Base',
    icon: 'M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25',
  },
  {
    href: '/dashboard/conversations',
    label: 'Conversations',
    icon: 'M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155',
  },
  {
    href: '/dashboard/widget',
    label: 'Widget',
    icon: 'M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42',
  },
  {
    href: '/dashboard/billing',
    label: 'Billing',
    icon: 'M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z',
  },
];

function SidebarSkeleton() {
  return (
    <div className="w-64 bg-surface-200 border-r border-white/[0.04] flex flex-col">
      <div className="h-16 px-5 flex items-center border-b border-white/[0.04]">
        <Skeleton className="h-6 w-32" />
      </div>
      <div className="flex-1 p-3 space-y-1">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full rounded-lg" />
        ))}
      </div>
    </div>
  );
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const toast = useToast();
  const [website, setWebsite] = useState<any>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    bindToast(toast.error, toast.success);
  }, [toast]);

  useEffect(() => {
    const key = api.getApiKey();
    if (!key) {
      router.push('/login');
      return;
    }
    api.getMe().then(setWebsite).catch(() => {
      api.clearApiKey();
      router.push('/login');
    });
  }, [router]);

  const handleLogout = () => {
    api.clearApiKey();
    router.push('/login');
  };

  if (!website) {
    return (
      <div className="min-h-screen bg-surface flex">
        <SidebarSkeleton />
        <div className="flex-1 p-8">
          <Skeleton className="h-8 w-48 mb-8" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="card p-6 space-y-3">
                <Skeleton className="h-3 w-24" />
                <Skeleton className="h-8 w-16" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const currentTitle = NAV_ITEMS.find((i) => i.href === pathname)?.label || 'Dashboard';

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-30 w-64 bg-surface-200 border-r border-white/[0.04] flex flex-col transform transition-transform duration-200 lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between h-16 px-5 border-b border-white/[0.04] flex-shrink-0">
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-sm font-bold text-white">
              AutoReply<span className="text-brand-400">AI</span>
            </span>
          </Link>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-1 text-gray-500 hover:text-white rounded transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-brand-500/15 text-brand-400 border border-brand-500/20'
                    : 'text-gray-400 hover:bg-white/[0.04] hover:text-gray-200 border border-transparent'
                }`}
              >
                <svg
                  className={`w-[18px] h-[18px] flex-shrink-0 ${isActive ? 'text-brand-400' : 'text-gray-500'}`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={1.5}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
                </svg>
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/[0.04] flex-shrink-0">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-8 h-8 rounded-full bg-brand-500/15 border border-brand-500/25 flex items-center justify-center text-xs font-semibold text-brand-400">
              {website.name?.charAt(0)?.toUpperCase() || 'A'}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm text-gray-300 truncate font-medium">{website.name}</div>
              <div className="text-xs text-gray-600 uppercase tracking-wider">{website.plan} plan</div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full text-left flex items-center gap-2 px-3 py-2 text-xs text-gray-500 hover:text-gray-300 rounded-lg hover:bg-white/[0.04] transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
            </svg>
            Sign Out
          </button>
        </div>
      </aside>

      {/* Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen min-w-0">
        <header className="h-14 bg-surface-200/80 backdrop-blur-lg border-b border-white/[0.04] flex items-center px-4 lg:px-8 flex-shrink-0 sticky top-0 z-10">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden mr-3 p-1.5 text-gray-400 hover:text-white rounded-lg hover:bg-white/[0.05] transition-colors"
            aria-label="Open sidebar"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          </button>
          <h1 className="text-sm font-semibold text-white">{currentTitle}</h1>
        </header>

        <main className="flex-1 p-4 lg:p-8 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
