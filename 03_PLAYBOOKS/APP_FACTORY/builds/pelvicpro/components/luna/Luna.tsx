import React from 'react';
import { View, StyleSheet, Animated, Easing } from 'react-native';
import { Svg, Circle, Ellipse, Path, G } from 'react-native-svg';
import { colors } from '@/constants/theme';
import type { LunaState } from '@/constants/luna';

interface LunaProps {
  state: LunaState;
  size?: number;
}

// Luna the Cat - SVG mascot component
// Orange tabby cat with cute expressions
export default function Luna({ state = 'idle', size = 80 }: LunaProps) {
  const scale = size / 80;

  // Get expression based on state
  const getEyeExpression = () => {
    switch (state) {
      case 'sleeping':
        return { closed: true };
      case 'happy':
      case 'celebrating':
        return { happy: true };
      case 'excited':
        return { sparkle: true };
      default:
        return { normal: true };
    }
  };

  const getMouthExpression = () => {
    switch (state) {
      case 'sleeping':
        return 'sleeping';
      case 'happy':
      case 'celebrating':
      case 'excited':
        return 'smile';
      case 'cheering':
        return 'open';
      default:
        return 'neutral';
    }
  };

  const eyes = getEyeExpression();
  const mouth = getMouthExpression();

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size} viewBox="0 0 80 80">
        <G transform={`scale(${scale > 1 ? 1 : scale})`}>
          {/* Body (hidden, just head for this icon) */}

          {/* Head - Orange circle */}
          <Circle cx="40" cy="42" r="28" fill={colors.lunaPrimary} />

          {/* Inner face - lighter orange */}
          <Circle cx="40" cy="44" r="22" fill={colors.lunaSecondary} />

          {/* Left Ear */}
          <Path
            d="M18 28 L12 8 L30 22 Z"
            fill={colors.lunaPrimary}
          />
          <Path
            d="M20 26 L16 12 L28 22 Z"
            fill="#FFB8A0"
          />

          {/* Right Ear */}
          <Path
            d="M62 28 L68 8 L50 22 Z"
            fill={colors.lunaPrimary}
          />
          <Path
            d="M60 26 L64 12 L52 22 Z"
            fill="#FFB8A0"
          />

          {/* Eyes */}
          {eyes.closed ? (
            // Sleeping eyes - curved lines
            <>
              <Path
                d="M28 42 Q32 38 36 42"
                stroke={colors.text}
                strokeWidth="2"
                fill="none"
                strokeLinecap="round"
              />
              <Path
                d="M44 42 Q48 38 52 42"
                stroke={colors.text}
                strokeWidth="2"
                fill="none"
                strokeLinecap="round"
              />
            </>
          ) : eyes.happy ? (
            // Happy eyes - upward curves
            <>
              <Path
                d="M28 44 Q32 40 36 44"
                stroke={colors.text}
                strokeWidth="2.5"
                fill="none"
                strokeLinecap="round"
              />
              <Path
                d="M44 44 Q48 40 52 44"
                stroke={colors.text}
                strokeWidth="2.5"
                fill="none"
                strokeLinecap="round"
              />
            </>
          ) : eyes.sparkle ? (
            // Excited eyes - stars/sparkles
            <>
              <Circle cx="32" cy="42" r="5" fill={colors.text} />
              <Circle cx="32" cy="40" r="2" fill={colors.surface} />
              <Circle cx="48" cy="42" r="5" fill={colors.text} />
              <Circle cx="48" cy="40" r="2" fill={colors.surface} />
              {/* Star sparkles */}
              <Path
                d="M26 36 L27 34 L28 36 L30 35 L28 36 L27 38 L26 36 L24 35 Z"
                fill={colors.warning}
              />
              <Path
                d="M52 36 L53 34 L54 36 L56 35 L54 36 L53 38 L52 36 L50 35 Z"
                fill={colors.warning}
              />
            </>
          ) : (
            // Normal eyes
            <>
              <Ellipse cx="32" cy="42" rx="4" ry="5" fill={colors.text} />
              <Circle cx="33" cy="41" r="1.5" fill={colors.surface} />
              <Ellipse cx="48" cy="42" rx="4" ry="5" fill={colors.text} />
              <Circle cx="49" cy="41" r="1.5" fill={colors.surface} />
            </>
          )}

          {/* Blush marks */}
          <Ellipse cx="24" cy="50" rx="5" ry="3" fill="#FFAAAA" opacity={0.5} />
          <Ellipse cx="56" cy="50" rx="5" ry="3" fill="#FFAAAA" opacity={0.5} />

          {/* Nose */}
          <Ellipse cx="40" cy="50" rx="3" ry="2" fill="#FF9999" />

          {/* Mouth */}
          {mouth === 'sleeping' ? (
            // ZZZ for sleeping
            <>
              <Path
                d="M38 56 Q40 54 42 56"
                stroke={colors.text}
                strokeWidth="1.5"
                fill="none"
              />
              <Path
                d="M60 30 L64 30 L60 34 L64 34"
                stroke={colors.text}
                strokeWidth="1.5"
                fill="none"
              />
              <Path
                d="M66 24 L69 24 L66 27 L69 27"
                stroke={colors.text}
                strokeWidth="1"
                fill="none"
              />
            </>
          ) : mouth === 'smile' ? (
            // Happy smile
            <Path
              d="M34 54 Q40 62 46 54"
              stroke={colors.text}
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
            />
          ) : mouth === 'open' ? (
            // Open mouth (cheering)
            <>
              <Ellipse cx="40" cy="56" rx="6" ry="5" fill={colors.text} />
              <Ellipse cx="40" cy="54" rx="4" ry="3" fill="#FF8888" />
            </>
          ) : (
            // Neutral - small W shape
            <Path
              d="M36 55 L38 57 L40 55 L42 57 L44 55"
              stroke={colors.text}
              strokeWidth="1.5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {/* Whiskers */}
          <G stroke={colors.text} strokeWidth="1" opacity={0.4}>
            <Path d="M20 48 L10 46" />
            <Path d="M20 52 L10 52" />
            <Path d="M20 56 L10 58" />
            <Path d="M60 48 L70 46" />
            <Path d="M60 52 L70 52" />
            <Path d="M60 56 L70 58" />
          </G>

          {/* Celebrating state extras */}
          {state === 'celebrating' && (
            <>
              {/* Confetti dots */}
              <Circle cx="15" cy="20" r="2" fill={colors.primary} />
              <Circle cx="65" cy="15" r="2" fill={colors.accent} />
              <Circle cx="10" cy="35" r="1.5" fill={colors.secondary} />
              <Circle cx="70" cy="30" r="1.5" fill={colors.warning} />
              <Circle cx="25" cy="10" r="1.5" fill={colors.success} />
              <Circle cx="55" cy="8" r="2" fill={colors.primary} />
              {/* Hearts */}
              <Path
                d="M8 50 C8 46 14 46 14 50 C14 54 8 58 8 58 C8 58 2 54 2 50 C2 46 8 46 8 50"
                fill={colors.primary}
                transform="scale(0.5) translate(135, 5)"
              />
            </>
          )}

          {/* Waving paw for waving state */}
          {state === 'waving' && (
            <G transform="translate(58, 55)">
              <Ellipse cx="0" cy="0" rx="8" ry="6" fill={colors.lunaPrimary} />
              <Circle cx="-4" cy="2" r="2" fill={colors.lunaSecondary} />
              <Circle cx="0" cy="4" r="2" fill={colors.lunaSecondary} />
              <Circle cx="4" cy="2" r="2" fill={colors.lunaSecondary} />
            </G>
          )}
        </G>
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
});
