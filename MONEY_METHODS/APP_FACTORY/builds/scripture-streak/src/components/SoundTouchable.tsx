/**
 * Drop-in replacement for TouchableOpacity with sound + haptic feedback.
 * Usage: import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable'
 */

import React, { useCallback } from 'react';
import { TouchableOpacity, TouchableOpacityProps } from 'react-native';
import * as Haptics from 'expo-haptics';
import { playSound, SoundName } from '../sounds/SoundEngine';

interface SoundTouchableProps extends TouchableOpacityProps {
  sound?: SoundName | 'none';
  haptic?: 'light' | 'medium' | 'heavy' | 'success' | 'error' | 'none';
}

const HAPTIC_MAP: Record<string, (() => void) | null> = {
  light: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light),
  medium: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium),
  heavy: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy),
  success: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success),
  error: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error),
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
      if (sound !== 'none') playSound(sound as SoundName);
      const fn = HAPTIC_MAP[haptic];
      if (fn) fn();
      onPress?.(event);
    },
    [sound, haptic, onPress]
  );

  return <TouchableOpacity {...props} onPress={handlePress} />;
}

export default SoundTouchable;
