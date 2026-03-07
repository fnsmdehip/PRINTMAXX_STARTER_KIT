import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

type CompareRow = {
  before: string;
  after: string;
};

export type BeforeAfterProps = {
  title: string;
  beforeLabel?: string;
  afterLabel?: string;
  rows: CompareRow[];
  footnote?: string;
  brand?: string;
};

const RowItem: React.FC<{
  row: CompareRow;
  index: number;
}> = ({row, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const delay = 25 + index * 10;
  const opacity = interpolate(frame, [delay, delay + 8], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  const slideX = interpolate(frame, [delay, delay + 8], [20, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  const strikeDelay = delay + 5;
  const strikeWidth = spring({
    frame: Math.max(0, frame - strikeDelay),
    fps,
    config: {damping: 80, mass: 0.6},
  });

  const afterDelay = delay + 8;
  const afterOpacity = interpolate(frame, [afterDelay, afterDelay + 6], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 24,
        opacity,
        transform: `translateX(${slideX}px)`,
        padding: '12px 0',
        borderBottom: '1px solid rgba(255,255,255,0.04)',
      }}
    >
      <div style={{position: 'relative'}}>
        <div
          style={{
            fontSize: 20,
            fontWeight: 500,
            color: 'rgba(255,255,255,0.45)',
          }}
        >
          {row.before}
        </div>
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: 0,
            width: `${strikeWidth * 100}%`,
            height: 2,
            background: '#f5576c',
            opacity: 0.6,
          }}
        />
      </div>
      <div
        style={{
          fontSize: 20,
          fontWeight: 600,
          color: '#4ade80',
          opacity: afterOpacity,
        }}
      >
        {row.after}
      </div>
    </div>
  );
};

export const BeforeAfter: React.FC<BeforeAfterProps> = ({
  title,
  beforeLabel = '2025',
  afterLabel = '2026',
  rows,
  footnote,
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const titleOpacity = interpolate(frame, [3, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [3, 15], [12, 0], {
    extrapolateRight: 'clamp',
  });

  const headerOpacity = interpolate(frame, [12, 22], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const footnoteDelay = 25 + rows.length * 10 + 15;
  const footnoteOpacity = interpolate(
    frame,
    [footnoteDelay, footnoteDelay + 12],
    [0, 1],
    {extrapolateRight: 'clamp'}
  );

  const brandOpacity = interpolate(
    frame,
    [footnoteDelay + 5, footnoteDelay + 20],
    [0, 0.25],
    {extrapolateRight: 'clamp'}
  );

  const dividerHeight = spring({
    frame: Math.max(0, frame - 15),
    fps,
    config: {damping: 60, mass: 1},
  });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(180deg, #08080a 0%, #0d0d12 100%)',
        fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        padding: '50px 70px',
        overflow: 'hidden',
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: 34,
          fontWeight: 800,
          letterSpacing: -0.5,
          marginBottom: 32,
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
        }}
      >
        {title}
      </div>

      {/* Column headers */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 24,
          marginBottom: 16,
          opacity: headerOpacity,
          position: 'relative',
        }}
      >
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: 'rgba(255,255,255,0.3)',
            textTransform: 'uppercase' as const,
            letterSpacing: 3,
          }}
        >
          {beforeLabel}
        </div>
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: '#4ade80',
            textTransform: 'uppercase' as const,
            letterSpacing: 3,
            opacity: 0.6,
          }}
        >
          {afterLabel}
        </div>
      </div>

      {/* Center divider */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: 100,
          bottom: 60,
          width: 1,
          background: 'rgba(255,255,255,0.06)',
          transform: `scaleY(${dividerHeight})`,
          transformOrigin: 'top',
        }}
      />

      {/* Rows */}
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 2}}>
        {rows.map((row, i) => (
          <RowItem key={i} row={row} index={i} />
        ))}
      </div>

      {/* Footnote */}
      {footnote && (
        <div
          style={{
            fontSize: 18,
            fontWeight: 500,
            color: 'rgba(255,255,255,0.5)',
            marginTop: 24,
            opacity: footnoteOpacity,
            fontStyle: 'italic',
          }}
        >
          {footnote}
        </div>
      )}

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
