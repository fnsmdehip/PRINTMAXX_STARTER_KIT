import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { COLORS } from '../utils/constants';

interface Props {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

const buttonSizeStyles = {
  small: {
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  medium: {
    paddingVertical: 14,
    paddingHorizontal: 24,
  },
  large: {
    paddingVertical: 18,
    paddingHorizontal: 32,
  },
};

const textSizeStyles = {
  small: {
    fontSize: 14,
  },
  medium: {
    fontSize: 16,
  },
  large: {
    fontSize: 18,
  },
};

export function Button({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  style,
  textStyle,
}: Props) {
  const getButtonStyle = (): ViewStyle[] => {
    const base: ViewStyle[] = [styles.button, buttonSizeStyles[size]];

    switch (variant) {
      case 'secondary':
        base.push(styles.buttonSecondary);
        break;
      case 'outline':
        base.push(styles.buttonOutline);
        break;
      case 'text':
        base.push(styles.buttonText);
        break;
      default:
        base.push(styles.buttonPrimary);
    }

    if (disabled || loading) {
      base.push(styles.buttonDisabled);
    }

    return base;
  };

  const getTextStyle = (): TextStyle[] => {
    const base: TextStyle[] = [styles.text, textSizeStyles[size]];

    switch (variant) {
      case 'secondary':
        base.push(styles.textSecondary);
        break;
      case 'outline':
        base.push(styles.textOutline);
        break;
      case 'text':
        base.push(styles.textText);
        break;
      default:
        base.push(styles.textPrimary);
    }

    if (disabled || loading) {
      base.push(styles.textDisabled);
    }

    return base;
  };

  return (
    <TouchableOpacity
      style={[...getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'primary' ? COLORS.surface : COLORS.primary}
          size="small"
        />
      ) : (
        <Text style={[...getTextStyle(), textStyle]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonPrimary: {
    backgroundColor: COLORS.primary,
  },
  buttonSecondary: {
    backgroundColor: COLORS.secondary,
  },
  buttonOutline: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  buttonText: {
    backgroundColor: 'transparent',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  text: {
    fontWeight: '600',
  },
  textPrimary: {
    color: COLORS.surface,
  },
  textSecondary: {
    color: COLORS.surface,
  },
  textOutline: {
    color: COLORS.primary,
  },
  textText: {
    color: COLORS.primary,
  },
  textDisabled: {
    color: COLORS.disabled,
  },
});
