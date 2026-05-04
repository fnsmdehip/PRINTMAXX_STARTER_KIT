import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

export type QuoteCardProps = {
  quote: string;
  attribution?: string;
};

export const QuoteCard: React.FC<QuoteCardProps> = ({
  quote,
  attribution = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const borderOpacity = interpolate(frame, [0, 20], [0, 0.2], {extrapolateRight: 'clamp'});
  const quoteMarkScale = spring({frame, fps, config: {damping: 60, mass: 0.5}});
  const textOpacity = interpolate(frame, [15, 35], [0, 1], {extrapolateRight: 'clamp'});
  const textY = interpolate(frame, [15, 35], [20, 0], {extrapolateRight: 'clamp'});
  const attrOpacity = interpolate(frame, [40, 55], [0, 0.4], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{
      background: '#0a0a0a',
      fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
      color: '#ffffff',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 100,
    }}>
      <div style={{
        position: 'absolute',
        top: 30, left: 30, right: 30, bottom: 30,
        border: `1px solid rgba(102, 126, 234, ${borderOpacity})`,
        borderRadius: 8,
      }} />
      <div style={{
        fontSize: 120,
        fontWeight: 900,
        background: 'linear-gradient(135deg, #667eea, #764ba2)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        lineHeight: 0.6,
        marginBottom: 40,
        transform: `scale(${quoteMarkScale})`,
      }}>
        "
      </div>
      <div style={{
        fontSize: 36,
        fontWeight: 600,
        lineHeight: 1.4,
        textAlign: 'center' as const,
        maxWidth: 800,
        marginBottom: 48,
        opacity: textOpacity,
        transform: `translateY(${textY}px)`,
      }}>
        {quote}
      </div>
      <div style={{
        fontSize: 20,
        fontWeight: 400,
        color: `rgba(255,255,255,${attrOpacity})`,
        letterSpacing: 2,
        textTransform: 'uppercase' as const,
      }}>
        {attribution}
      </div>
    </AbsoluteFill>
  );
};
