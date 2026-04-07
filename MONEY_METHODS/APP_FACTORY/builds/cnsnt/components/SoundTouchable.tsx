/**
 * Drop-in replacement for Pressable/TouchableOpacity with automatic sound + haptic feedback.
 *
 * Usage: import { SoundTouchable as Pressable } from '../components/SoundTouchable'
 *
 * Props:
 *   sound  -- which sound to play (default: 'tap')
 *   haptic -- haptic feedback type (default: 'light')
 *   sound='none' -- disable sound for this element
 */

import React, { useCallback } from 'react';
import { Pressable, PressableProps } from 'react-native';
import * as Haptics from 'expo-haptics';
import { playSound, SoundName } from '../sounds/SoundEngine';

type HapticType =
  | 'light'
  | 'medium'
  | 'heavy'
  | 'success'
  | 'warning'
  | 'error'
  | 'none';

interface SoundTouchableProps extends PressableProps {
  sound?: SoundName | 'none';
  haptic?: HapticType;
}

const HAPTIC_MAP: Record<HapticType, (() => void) | null> = {
  light: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light),
  medium: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium),
  heavy: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy),
  success: () =>
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success),
  warning: () =>
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning),
  error: () =>
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error),
  none: null,
};

export function SoundTouchable({
  sound = 'tap',
  haptic = 'light',
  onPress,
  ...props
}: SoundTouchableProps) {
  const handlePress = useCallback(
    (event: any) => {
      if (sound !== 'none') {
        playSound(sound as SoundName);
      }
      const hapticFn = HAPTIC_MAP[haptic];
      if (hapticFn) hapticFn();
      onPress?.(event);
    },
    [sound, haptic, onPress],
  );

  return <Pressable {...props} onPress={handlePress} />;
}

export default SoundTouchable;
