import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

export type SocialHookProps = {
  hookText: string;
  highlightWord: string;
  subtitle: string;
  brand?: string;
};

export const SocialHook: React.FC<SocialHookProps> = ({
  hookText,
  highlightWord,
  subtitle,
  brand = 'PRINTMAXX',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const accentBarWidth = spring({frame, fps, config: {damping: 80}}) * 60;
  const hookOpacity = interpolate(frame, [10, 25], [0, 1], {extrapolateRight: 'clamp'});
  const hookY = interpolate(frame, [10, 25], [30, 0], {extrapolateRight: 'clamp'});
  const subtitleOpacity = interpolate(frame, [35, 50], [0, 1], {extrapolateRight: 'clamp'});
  const brandOpacity = interpolate(frame, [50, 65], [0, 0.3], {extrapolateRight: 'clamp'});

  const parts = hookText.split(highlightWord);
  const hookContent = parts.length > 1
    ? <>{parts[0]}<span style={{
        background: 'linear-gradient(90deg, #667eea, #764ba2)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
      }}>{highlightWord}</span>{parts[1]}</>
    : hookText;

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, Inter, sans-serif',
      color: '#ffffff',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      padding: 80,
    }}>
      <div style={{
        width: accentBarWidth,
        height: 4,
        background: 'linear-gradient(90deg, #667eea, #764ba2)',
        borderRadius: 2,
        marginBottom: 32,
      }} />
      <div style={{
        fontSize: 52,
        fontWeight: 800,
        lineHeight: 1.15,
        letterSpacing: -1,
        marginBottom: 24,
        maxWidth: 900,
        opacity: hookOpacity,
        transform: `translateY(${hookY}px)`,
      }}>
        {hookContent}
      </div>
      <div style={{
        fontSize: 24,
        fontWeight: 400,
        color: 'rgba(255,255,255,0.6)',
        maxWidth: 700,
        lineHeight: 1.5,
        opacity: subtitleOpacity,
      }}>
        {subtitle}
      </div>
      <div style={{
        position: 'absolute',
        bottom: 40,
        right: 60,
        fontSize: 18,
        fontWeight: 700,
        color: `rgba(255,255,255,${brandOpacity})`,
        letterSpacing: 4,
        textTransform: 'uppercase' as const,
      }}>
        {brand}
      </div>
    </AbsoluteFill>
  );
};
