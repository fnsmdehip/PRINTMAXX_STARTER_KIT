import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from 'remotion';

type SupportingStat = {
  value: string;
  label: string;
};

export type BigNumberProps = {
  number: string;
  label: string;
  source?: string;
  supportingStats?: SupportingStat[];
  accentColor?: string;
  brand?: string;
};

export const BigNumber: React.FC<BigNumberProps> = ({
  number,
  label,
  source,
  supportingStats = [],
  accentColor = '#667eea',
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Accent line draws in
  const lineWidth = spring({frame, fps, config: {damping: 80}}) * 120;

  // Big number scales in with bounce
  const numScale = spring({
    frame: Math.max(0, frame - 8),
    fps,
    config: {damping: 40, mass: 0.8, stiffness: 180},
  });
  const numOpacity = interpolate(frame, [8, 18], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  // Label fades in
  const labelOpacity = interpolate(frame, [22, 35], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const labelY = interpolate(frame, [22, 35], [15, 0], {
    extrapolateRight: 'clamp',
  });

  // Source fades in
  const sourceOpacity = interpolate(frame, [38, 48], [0, 0.35], {
    extrapolateRight: 'clamp',
  });

  // Supporting stats
  const brandOpacity = interpolate(frame, [70, 85], [0, 0.2], {
    extrapolateRight: 'clamp',
  });

  // Glow pulse on number
  const glowIntensity = interpolate(
    frame,
    [20, 35, 50],
    [0, 0.5, 0.2],
    {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'}
  );

  return (
    <AbsoluteFill
      style={{
        background: '#08080a',
        fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '80px 60px',
        overflow: 'hidden',
      }}
    >
      {/* Subtle radial glow behind number */}
      <div
        style={{
          position: 'absolute',
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accentColor}${Math.round(glowIntensity * 25).toString(16).padStart(2, '0')} 0%, transparent 70%)`,
          top: '30%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      />

      {/* Accent line */}
      <div
        style={{
          width: lineWidth,
          height: 3,
          background: `linear-gradient(90deg, ${accentColor}, ${accentColor}88)`,
          borderRadius: 2,
          marginBottom: 48,
        }}
      />

      {/* Big number */}
      <div
        style={{
          fontSize: 120,
          fontWeight: 900,
          letterSpacing: -4,
          lineHeight: 1,
          marginBottom: 20,
          opacity: numOpacity,
          transform: `scale(${numScale})`,
          background: `linear-gradient(135deg, ${accentColor}, #f093fb)`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          textAlign: 'center' as const,
        }}
      >
        {number}
      </div>

      {/* Label */}
      <div
        style={{
          fontSize: 28,
          fontWeight: 600,
          color: 'rgba(255,255,255,0.75)',
          textAlign: 'center' as const,
          maxWidth: 500,
          lineHeight: 1.3,
          opacity: labelOpacity,
          transform: `translateY(${labelY}px)`,
          marginBottom: 16,
        }}
      >
        {label}
      </div>

      {/* Source */}
      {source && (
        <div
          style={{
            fontSize: 16,
            fontWeight: 400,
            color: `rgba(255,255,255,${sourceOpacity})`,
            marginBottom: 48,
          }}
        >
          {source}
        </div>
      )}

      {/* Supporting stats row */}
      {supportingStats.length > 0 && (
        <Sequence from={50}>
          <div
            style={{
              display: 'flex',
              gap: 40,
              justifyContent: 'center',
              position: 'absolute',
              bottom: 160,
              left: 0,
              right: 0,
            }}
          >
            {supportingStats.map((stat, i) => {
              const sFrame = useCurrentFrame();
              const sDelay = i * 8;
              const sOpacity = interpolate(
                sFrame,
                [sDelay, sDelay + 10],
                [0, 1],
                {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'}
              );
              return (
                <div
                  key={i}
                  style={{
                    textAlign: 'center' as const,
                    opacity: sOpacity,
                  }}
                >
                  <div
                    style={{
                      fontSize: 32,
                      fontWeight: 800,
                      color: accentColor,
                    }}
                  >
                    {stat.value}
                  </div>
                  <div
                    style={{
                      fontSize: 13,
                      color: 'rgba(255,255,255,0.4)',
                      textTransform: 'uppercase' as const,
                      letterSpacing: 1,
                    }}
                  >
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </Sequence>
      )}

      {/* Brand */}
      <div
        style={{
          position: 'absolute',
          bottom: 50,
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
