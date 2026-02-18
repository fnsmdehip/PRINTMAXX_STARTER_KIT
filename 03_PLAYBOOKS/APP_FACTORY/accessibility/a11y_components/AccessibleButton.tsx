import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
  AccessibilityRole,
  AccessibilityState,
} from 'react-native';

interface AccessibleButtonProps {
  // Required
  label: string;
  onPress: () => void;

  // Display
  title?: string;
  icon?: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'small' | 'medium' | 'large';

  // State
  disabled?: boolean;
  loading?: boolean;
  selected?: boolean;

  // Accessibility
  hint?: string;
  role?: AccessibilityRole;

  // Styling
  style?: ViewStyle;
  textStyle?: TextStyle;
  testID?: string;
}

export function AccessibleButton({
  label,
  onPress,
  title,
  icon,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  selected = false,
  hint,
  role = 'button',
  style,
  textStyle,
  testID,
}: AccessibleButtonProps) {
  const isDisabled = disabled || loading;

  // Build accessibility state
  const accessibilityState: AccessibilityState = {
    disabled: isDisabled,
    selected,
    busy: loading,
  };

  // Build accessibility label
  // Include state info for screen readers
  let accessibilityLabel = label;
  if (loading) {
    accessibilityLabel = `${label}, loading`;
  }

  return (
    <TouchableOpacity
      accessible={true}
      accessibilityLabel={accessibilityLabel}
      accessibilityHint={hint}
      accessibilityRole={role}
      accessibilityState={accessibilityState}
      onPress={onPress}
      disabled={isDisabled}
      style={[
        styles.base,
        styles[variant],
        styles[size],
        isDisabled && styles.disabled,
        style,
      ]}
      activeOpacity={0.7}
      testID={testID}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'primary' ? '#FFFFFF' : '#000000'}
          size="small"
        />
      ) : (
        <>
          {icon}
          {title && (
            <Text
              style={[
                styles.text,
                styles[`${variant}Text`],
                styles[`${size}Text`],
                textStyle,
              ]}
            >
              {title}
            </Text>
          )}
        </>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 8,
    gap: 8,
  },

  // Variants
  primary: {
    backgroundColor: '#007AFF',
  },
  secondary: {
    backgroundColor: '#E5E5EA',
  },
  ghost: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#007AFF',
  },
  danger: {
    backgroundColor: '#FF3B30',
  },

  // Sizes - meet minimum touch target (44x44)
  small: {
    minHeight: 44,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  medium: {
    minHeight: 48,
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  large: {
    minHeight: 56,
    paddingHorizontal: 32,
    paddingVertical: 16,
  },

  // Disabled state
  disabled: {
    opacity: 0.5,
  },

  // Text base
  text: {
    fontWeight: '600',
    textAlign: 'center',
  },

  // Text variants
  primaryText: {
    color: '#FFFFFF',
  },
  secondaryText: {
    color: '#000000',
  },
  ghostText: {
    color: '#007AFF',
  },
  dangerText: {
    color: '#FFFFFF',
  },

  // Text sizes
  smallText: {
    fontSize: 14,
  },
  mediumText: {
    fontSize: 16,
  },
  largeText: {
    fontSize: 18,
  },
});

// Usage examples:
/*
// Basic button
<AccessibleButton
  label="Submit form"
  title="Submit"
  onPress={handleSubmit}
/>

// Icon-only button (label is required for screen readers)
<AccessibleButton
  label="Add item to cart"
  hint="Adds one unit of this product to your shopping cart"
  icon={<PlusIcon />}
  onPress={handleAddToCart}
/>

// Loading state
<AccessibleButton
  label="Submitting order"
  title="Submit"
  loading={isSubmitting}
  onPress={handleSubmit}
/>

// Toggle button
<AccessibleButton
  label="Favorite"
  icon={isFavorite ? <HeartFilledIcon /> : <HeartOutlineIcon />}
  selected={isFavorite}
  onPress={toggleFavorite}
/>
*/
