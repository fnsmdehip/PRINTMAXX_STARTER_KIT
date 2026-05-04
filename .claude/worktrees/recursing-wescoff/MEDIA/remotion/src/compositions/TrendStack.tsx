import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

type TrendItem = {
  title: string;
  confidence: number;
  tag?: string;
};

export type TrendStackProps = {
  headline: string;
  subtitle?: string;
  trends: TrendItem[];
  brand?: string;
};

const TrendRow: React.FC<{
  trend: TrendItem;
  index: number;
  total: number;
}> = ({trend, index, total}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const delay = 20 + index * 10;
  const slideX = interpolate(frame, [delay, delay + 8], [-40, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  const opacity = interpolate(frame, [delay, delay + 8], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  // Confidence bar animates
  const barDelay = delay + 5;
  const barWidth = spring({
    frame: Math.max(0, frame - barDelay),
    fps,
    config: {damping: 60, mass: 0.8},
  });

  const confColor =
    trend.confidence >= 90
      ? '#4ade80'
      : trend.confidence >= 80
      ? '#667eea'
      : '#f59e0b';

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        padding: '10px 0',
        opacity,
        transform: `translateX(${slideX}px)`,
        borderBottom:
          index < total - 1
            ? '1px solid rgba(255,255,255,0.04)'
            : 'none',
      }}
    >
      {/* Number */}
      <div
        style={{
          fontSize: 16,
          fontWeight: 800,
          color: 'rgba(255,255,255,0.2)',
          width: 28,
          textAlign: 'right' as const,
          flexShrink: 0,
        }}
      >
        {String(index + 1).padStart(2, '0')}
      </div>

      {/* Content */}
      <div style={{flex: 1, minWidth: 0}}>
        <div
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: 'rgba(255,255,255,0.85)',
            marginBottom: 6,
            whiteSpace: 'nowrap' as const,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}
        >
          {trend.title}
        </div>
        {/* Confidence bar */}
        <div
          style={{
            width: '100%',
            height: 3,
            background: 'rgba(255,255,255,0.05)',
            borderRadius: 2,
          }}
        >
          <div
            style={{
              width: `${barWidth * trend.confidence}%`,
              height: '100%',
              background: confColor,
              borderRadius: 2,
              boxShadow: `0 0 8px ${confColor}44`,
            }}
          />
        </div>
      </div>

      {/* Confidence label */}
      <div
        style={{
          fontSize: 14,
          fontWeight: 700,
          color: confColor,
          width: 48,
          textAlign: 'right' as const,
          flexShrink: 0,
        }}
      >
        {trend.confidence}%
      </div>

      {/* Tag */}
      {trend.tag && (
        <div
          style={{
            fontSize: 11,
            fontWeight: 600,
            color: confColor,
            background: `${confColor}15`,
            border: `1px solid ${confColor}30`,
            borderRadius: 4,
            padding: '3px 8px',
            textTransform: 'uppercase' as const,
            letterSpacing: 1,
            flexShrink: 0,
          }}
        >
          {trend.tag}
        </div>
      )}
    </div>
  );
};

export const TrendStack: React.FC<TrendStackProps> = ({
  headline,
  subtitle,
  trends,
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();

  const headlineOpacity = interpolate(frame, [3, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const headlineY = interpolate(frame, [3, 15], [12, 0], {
    extrapolateRight: 'clamp',
  });

  const subtitleOpacity = interpolate(frame, [10, 20], [0, 0.5], {
    extrapolateRight: 'clamp',
  });

  const endDelay = 20 + trends.length * 10 + 20;
  const brandOpacity = interpolate(
    frame,
    [endDelay, endDelay + 15],
    [0, 0.25],
    {extrapolateRight: 'clamp'}
  );

  // Scanline
  const scanY = interpolate(frame, [0, 240], [-5, 105], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: '#08080a',
        fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        padding: '50px 70px',
        overflow: 'hidden',
      }}
    >
      {/* Grid bg */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />

      {/* Scanline */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: `${scanY}%`,
          height: 1,
          background:
            'linear-gradient(90deg, transparent 0%, rgba(102,126,234,0.12) 30%, rgba(102,126,234,0.12) 70%, transparent 100%)',
        }}
      />

      {/* Headline */}
      <div
        style={{
          fontSize: 32,
          fontWeight: 800,
          letterSpacing: -0.5,
          marginBottom: 6,
          opacity: headlineOpacity,
          transform: `translateY(${headlineY}px)`,
        }}
      >
        {headline}
      </div>

      {subtitle && (
        <div
          style={{
            fontSize: 16,
            color: `rgba(255,255,255,${subtitleOpacity})`,
            marginBottom: 28,
          }}
        >
          {subtitle}
        </div>
      )}

      {/* Trend list */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        {trends.map((trend, i) => (
          <TrendRow key={i} trend={trend} index={i} total={trends.length} />
        ))}
      </div>

      {/* Brand */}
      <div
        style={{
          position: 'absolute',
          bottom: 28,
          right: 50,
          fontSize: 14,
          fontWeight: 700,
          color: `rgba(255,255,255,${brandOpacity})`,
          letterSpacing: 4,
          textTransform: 'uppercase' as const,
        }}
      >
        {brand}
      </div>
    </AbsoluteFill>
  );
};
