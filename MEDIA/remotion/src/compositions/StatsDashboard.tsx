import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

type StatItem = {
  value: string;
  label: string;
  delta: string;
};

export type StatsDashboardProps = {
  title: string;
  subtitle: string;
  stats: StatItem[];
  brand?: string;
};

const StatCard: React.FC<{stat: StatItem; index: number}> = ({stat, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const delay = index * 8;
  const scale = spring({frame: frame - delay, fps, config: {damping: 80}});
  const opacity = interpolate(frame, [delay, delay + 15], [0, 1], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'});

  return (
    <div style={{
      background: 'rgba(255,255,255,0.04)',
      border: '1px solid rgba(255,255,255,0.08)',
      borderRadius: 12,
      padding: 28,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      opacity,
      transform: `scale(${scale})`,
    }}>
      <div style={{
        fontSize: 48,
        fontWeight: 800,
        background: 'linear-gradient(135deg, #667eea, #764ba2)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        marginBottom: 8,
      }}>
        {stat.value}
      </div>
      <div style={{
        fontSize: 14,
        color: 'rgba(255,255,255,0.5)',
        textTransform: 'uppercase' as const,
        letterSpacing: 1,
      }}>
        {stat.label}
      </div>
      <div style={{
        fontSize: 14,
        color: '#4ade80',
        marginTop: 4,
      }}>
        {stat.delta}
      </div>
    </div>
  );
};

export const StatsDashboard: React.FC<StatsDashboardProps> = ({
  title,
  subtitle,
  stats,
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 15], [0, 1], {extrapolateRight: 'clamp'});
  const brandOpacity = interpolate(frame, [60, 75], [0, 0.2], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{
      background: '#0a0a0a',
      fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
      color: '#ffffff',
      display: 'flex',
      flexDirection: 'column',
      padding: 60,
    }}>
      <div style={{opacity: titleOpacity}}>
        <div style={{fontSize: 28, fontWeight: 700, marginBottom: 8, letterSpacing: -0.5}}>
          {title}
        </div>
        <div style={{fontSize: 16, color: 'rgba(255,255,255,0.4)', marginBottom: 40}}>
          {subtitle}
        </div>
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${Math.min(stats.length, 4)}, 1fr)`,
        gap: 24,
        flex: 1,
      }}>
        {stats.map((stat, i) => (
          <StatCard key={i} stat={stat} index={i} />
        ))}
      </div>
      <div style={{
        position: 'absolute',
        bottom: 30,
        right: 40,
        fontSize: 14,
        fontWeight: 700,
        color: `rgba(255,255,255,${brandOpacity})`,
        letterSpacing: 3,
        textTransform: 'uppercase' as const,
      }}>
        {brand}
      </div>
    </AbsoluteFill>
  );
};
