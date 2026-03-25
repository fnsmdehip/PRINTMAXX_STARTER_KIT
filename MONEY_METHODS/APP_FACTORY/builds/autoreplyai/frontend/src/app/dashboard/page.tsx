'use client';

import { useEffect, useState, useMemo } from 'react';
import api from '@/lib/api';
import { SkeletonStatCards, SkeletonChart } from '@/components/Skeleton';

interface OverviewData {
  totalConversations: number;
  totalMessages: number;
  messagesToday: number;
  activeConversations: number;
  avgResponseTime: number;
  satisfactionRate: number;
  plan: string;
  messageCount: number;
  messageLimits: Record<string, number>;
}

interface DayData {
  date: string;
  count: number;
}

/* ──────────────────── Stat Card ──────────────────── */
function StatCard({
  label,
  value,
  sub,
  icon,
  trend,
}: {
  label: string;
  value: string | number;
  sub?: string;
  icon: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
}) {
  return (
    <div className="card p-5 animate-fade-in">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-lg bg-brand-500/10 border border-brand-500/20 flex items-center justify-center">
          {icon}
        </div>
        {trend && trend !== 'neutral' && (
          <span
            className={`badge text-[10px] ${
              trend === 'up' ? 'badge-green' : 'badge-red'
            }`}
          >
            {trend === 'up' ? '+12%' : '-3%'}
          </span>
        )}
      </div>
      <div className="text-2xl font-bold text-white mb-0.5">{value}</div>
      <div className="text-xs text-gray-500">{label}</div>
      {sub && <div className="text-[10px] text-gray-600 mt-1">{sub}</div>}
    </div>
  );
}

/* ──────────────────── Area Chart ──────────────────── */
function AreaChart({ data }: { data: DayData[] }) {
  const { pathD, areaD, max, points } = useMemo(() => {
    if (!data.length) return { pathD: '', areaD: '', max: 0, points: [] };

    const maxVal = Math.max(...data.map((d) => d.count), 1);
    const w = 100;
    const h = 100;
    const padding = 2;

    const pts = data.map((d, i) => ({
      x: padding + (i / (data.length - 1)) * (w - padding * 2),
      y: h - padding - (d.count / maxVal) * (h - padding * 2),
      ...d,
    }));

    const line = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
    const area = `${line} L ${pts[pts.length - 1].x} ${h} L ${pts[0].x} ${h} Z`;

    return { pathD: line, areaD: area, max: maxVal, points: pts };
  }, [data]);

  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-52 text-gray-600 text-sm">
        No message data yet
      </div>
    );
  }

  return (
    <div className="relative h-52">
      {/* Y-axis labels */}
      <div className="absolute left-0 top-0 bottom-6 w-10 flex flex-col justify-between text-[10px] text-gray-600 font-mono">
        <span>{max}</span>
        <span>{Math.round(max / 2)}</span>
        <span>0</span>
      </div>

      {/* Chart area */}
      <div
        className="ml-12 h-full relative"
        onMouseLeave={() => setHoveredIdx(null)}
      >
        <svg
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          className="w-full h-[calc(100%-24px)]"
        >
          {/* Grid lines */}
          {[0.25, 0.5, 0.75].map((pct) => (
            <line
              key={pct}
              x1="0"
              y1={pct * 100}
              x2="100"
              y2={pct * 100}
              stroke="rgba(255,255,255,0.03)"
              strokeWidth="0.3"
            />
          ))}

          {/* Area fill */}
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#3B82F6" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d={areaD} fill="url(#areaGrad)" />

          {/* Line */}
          <path
            d={pathD}
            fill="none"
            stroke="#3B82F6"
            strokeWidth="0.6"
            strokeLinecap="round"
            strokeLinejoin="round"
            vectorEffect="non-scaling-stroke"
          />
        </svg>

        {/* Hover targets */}
        <div className="absolute inset-0 flex" style={{ bottom: '24px' }}>
          {data.map((d, i) => (
            <div
              key={d.date}
              className="flex-1 relative"
              onMouseEnter={() => setHoveredIdx(i)}
            >
              {hoveredIdx === i && (
                <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                  <div className="bg-surface-100 border border-white/[0.1] rounded-lg px-3 py-2 text-center shadow-xl shadow-black/40 whitespace-nowrap">
                    <div className="text-xs text-gray-400">{d.date}</div>
                    <div className="text-sm font-semibold text-white">{d.count} messages</div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* X-axis labels */}
        <div className="flex justify-between h-6 items-center text-[10px] text-gray-600 font-mono">
          <span>{data[0]?.date.slice(5)}</span>
          <span>{data[Math.floor(data.length / 2)]?.date.slice(5)}</span>
          <span>{data[data.length - 1]?.date.slice(5)}</span>
        </div>
      </div>
    </div>
  );
}

/* ──────────────────── Usage Bar ──────────────────── */
function UsageBar({
  used,
  limit,
  plan,
}: {
  used: number;
  limit: number;
  plan: string;
}) {
  const pct = limit > 0 ? Math.min((used / limit) * 100, 100) : 0;
  const color =
    pct > 90 ? 'bg-danger-500' : pct > 70 ? 'bg-warning-500' : 'bg-brand-500';

  return (
    <div className="card p-5 animate-fade-in">
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-sm text-gray-300 font-medium">Message Usage</span>
          <span className="badge-gray ml-2 text-[10px] uppercase">{plan}</span>
        </div>
        <span className="text-sm text-gray-400 font-mono">
          {used.toLocaleString()}{' '}
          <span className="text-gray-600">/ {limit === -1 ? 'Unlimited' : limit.toLocaleString()}</span>
        </span>
      </div>
      {limit > 0 && (
        <div className="w-full bg-surface-300 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-500 ${color}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      )}
    </div>
  );
}

/* ══════════════════ DASHBOARD OVERVIEW ══════════════════ */
export default function DashboardOverview() {
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [chartData, setChartData] = useState<DayData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getAnalyticsOverview(), api.getMessagesPerDay(30)])
      .then(([ov, chart]) => {
        setOverview(ov);
        setChartData(chart.data || []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <SkeletonStatCards count={4} />
        <SkeletonChart />
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="card p-12 text-center">
        <p className="text-gray-400">Unable to load analytics. Please try again.</p>
      </div>
    );
  }

  const msgLimit = overview.messageLimits[overview.plan] || 100;

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total Conversations"
          value={overview.totalConversations.toLocaleString()}
          icon={
            <svg className="w-5 h-5 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
            </svg>
          }
        />
        <StatCard
          label="Messages Today"
          value={overview.messagesToday.toLocaleString()}
          icon={
            <svg className="w-5 h-5 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
            </svg>
          }
        />
        <StatCard
          label="Avg Response Time"
          value={
            overview.avgResponseTime > 0
              ? `${(overview.avgResponseTime / 1000).toFixed(1)}s`
              : 'N/A'
          }
          icon={
            <svg className="w-5 h-5 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
        <StatCard
          label="Satisfaction"
          value={
            overview.satisfactionRate > 0
              ? `${overview.satisfactionRate.toFixed(1)}/5`
              : 'N/A'
          }
          icon={
            <svg className="w-5 h-5 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
            </svg>
          }
        />
      </div>

      {/* Usage */}
      <UsageBar used={overview.messageCount} limit={msgLimit} plan={overview.plan} />

      {/* Chart */}
      <div className="card p-5 animate-fade-in">
        <div className="flex items-center justify-between mb-4">
          <h2 className="section-heading text-sm">Messages (Last 30 Days)</h2>
          <span className="text-xs text-gray-600 font-mono">
            {overview.totalMessages.toLocaleString()} total
          </span>
        </div>
        <AreaChart data={chartData} />
      </div>
    </div>
  );
}
