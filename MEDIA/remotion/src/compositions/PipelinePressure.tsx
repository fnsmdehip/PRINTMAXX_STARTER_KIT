import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from 'remotion';

type PressureStat = {
  value: string;
  label: string;
  color?: string;
};

export type PipelinePressureProps = {
  headline: string;
  stats: PressureStat[];
  punchline: string;
  brand?: string;
};

const AnimatedCounter: React.FC<{
  value: string;
  label: string;
  index: number;
  color?: string;
}> = ({value, label, index, color = '#667eea'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const delay = index * 12;
  const scale = spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: {damping: 60, mass: 0.8, stiffness: 200},
  });
  const opacity = interpolate(frame, [delay, delay + 10], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  const glowIntensity = interpolate(
    frame,
    [delay + 10, delay + 20, delay + 30],
    [0, 0.4, 0.15],
    {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'}
  );

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
        transform: `scale(${scale})`,
        padding: '24px 32px',
        background: `rgba(255,255,255,0.03)`,
        border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: 16,
        boxShadow: `0 0 ${glowIntensity * 60}px ${glowIntensity * 20}px ${color}33`,
        minWidth: 200,
      }}
    >
      <div
        style={{
          fontSize: 56,
          fontWeight: 900,
          letterSpacing: -2,
          lineHeight: 1,
          marginBottom: 8,
          background: `linear-gradient(135deg, ${color}, ${color}cc)`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontSize: 13,
          fontWeight: 500,
          color: 'rgba(255,255,255,0.45)',
          textTransform: 'uppercase' as const,
          letterSpacing: 2,
        }}
      >
        {label}
      </div>
    </div>
  );
};

const PressureBar: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const barWidth = spring({
    frame: Math.max(0, frame - 50),
    fps,
    config: {damping: 40, mass: 1.2, stiffness: 80},
  });

  const pulseOpacity = interpolate(
    frame,
    [70, 80, 90, 100, 110, 120],
    [0.6, 1, 0.6, 1, 0.6, 1],
    {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'}
  );

  return (
    <div
      style={{
        width: '100%',
        height: 6,
        background: 'rgba(255,255,255,0.05)',
        borderRadius: 3,
        overflow: 'hidden',
        marginTop: 32,
        marginBottom: 32,
      }}
    >
      <div
        style={{
          width: `${barWidth * 100}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #667eea, #f093fb, #f5576c)',
          borderRadius: 3,
          opacity: pulseOpacity,
          boxShadow: '0 0 20px #667eea66',
        }}
      />
    </div>
  );
};

export const PipelinePressure: React.FC<PipelinePressureProps> = ({
  headline,
  stats,
  punchline,
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const headlineOpacity = interpolate(frame, [5, 18], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const headlineY = interpolate(frame, [5, 18], [15, 0], {
    extrapolateRight: 'clamp',
  });

  const punchDelay = 55 + stats.length * 12;
  const punchOpacity = interpolate(
    frame,
    [punchDelay, punchDelay + 15],
    [0, 1],
    {extrapolateRight: 'clamp'}
  );
  const punchY = interpolate(frame, [punchDelay, punchDelay + 15], [10, 0], {
    extrapolateRight: 'clamp',
  });

  const brandOpacity = interpolate(
    frame,
    [punchDelay + 20, punchDelay + 35],
    [0, 0.25],
    {extrapolateRight: 'clamp'}
  );

  const scanlineY = interpolate(frame, [0, 180], [-10, 110], {
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
        justifyContent: 'center',
        padding: '60px 80px',
        overflow: 'hidden',
      }}
    >
      {/* Subtle grid overlay */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />

      {/* Animated scanline */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: `${scanlineY}%`,
          height: 1,
          background:
            'linear-gradient(90deg, transparent 0%, rgba(102,126,234,0.15) 30%, rgba(102,126,234,0.15) 70%, transparent 100%)',
        }}
      />

      {/* Headline */}
      <div
        style={{
          fontSize: 32,
          fontWeight: 700,
          letterSpacing: -0.5,
          marginBottom: 40,
          opacity: headlineOpacity,
          transform: `translateY(${headlineY}px)`,
          color: 'rgba(255,255,255,0.85)',
        }}
      >
        {headline}
      </div>

      {/* Stats grid */}
      <div
        style={{
          display: 'flex',
          gap: 20,
          flexWrap: 'wrap',
          justifyContent: 'center',
        }}
      >
        {stats.map((stat, i) => (
          <AnimatedCounter
            key={i}
            value={stat.value}
            label={stat.label}
            index={i}
            color={stat.color}
          />
        ))}
      </div>

      {/* Pressure bar */}
      <Sequence from={50}>
        <PressureBar />
      </Sequence>

      {/* Punchline */}
      <div
        style={{
          fontSize: 22,
          fontWeight: 500,
          color: 'rgba(255,255,255,0.55)',
          textAlign: 'center' as const,
          maxWidth: 700,
          alignSelf: 'center',
          lineHeight: 1.5,
          opacity: punchOpacity,
          transform: `translateY(${punchY}px)`,
          fontStyle: 'italic',
        }}
      >
        {punchline}
      </div>

      {/* Brand */}
      <div
        style={{
          position: 'absolute',
          bottom: 30,
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
