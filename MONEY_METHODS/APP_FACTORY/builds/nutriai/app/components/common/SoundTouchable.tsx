/**
 * Drop-in replacement for TouchableOpacity with sound + haptic feedback.
 * Usage: import { SoundTouchable as TouchableOpacity } from '../components/common/SoundTouchable'
 */

import React, { useCallback } from 'react';
import { TouchableOpacity, TouchableOpacityProps } from 'react-native';
import { haptics } from '../../utils/haptics';
import { playSound, SoundName } from '../../sounds/SoundEngine';

interface SoundTouchableProps extends TouchableOpacityProps {
  sound?: SoundName | 'none';
  haptic?: 'light' | 'medium' | 'heavy' | 'success' | 'error' | 'none';
}

export function SoundTouchable({
  sound = 'tap',
  haptic = 'light',
  onPress,
  ...props
}: SoundTouchableProps) {
  const handlePress = useCallback(
    (event: any) => {
      if (sound !== 'none') playSound(sound as SoundName);
      if (haptic !== 'none') {
        switch (haptic) {
          case 'light': haptics.light(); break;
          case 'medium': haptics.medium(); break;
          case 'heavy': haptics.heavy(); break;
          case 'success': haptics.success(); break;
          case 'error': haptics.error(); break;
        }
      }
      onPress?.(event);
    },
    [sound, haptic, onPress]
  );

  return <TouchableOpacity {...props} onPress={handlePress} />;
}

export default SoundTouchable;
