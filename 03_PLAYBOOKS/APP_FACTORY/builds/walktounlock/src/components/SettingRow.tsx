import React from 'react';
import { View, StyleSheet, Text, Switch, Pressable } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';

interface SettingRowProps {
  title: string;
  subtitle?: string;
  value?: string | number | boolean;
  type?: 'toggle' | 'value' | 'action';
  onPress?: () => void;
  onToggle?: (value: boolean) => void;
  disabled?: boolean;
  showArrow?: boolean;
}

export const SettingRow: React.FC<SettingRowProps> = ({
  title,
  subtitle,
  value,
  type = 'action',
  onPress,
  onToggle,
  disabled = false,
  showArrow = true,
}) => {
  const renderRight = () => {
    if (type === 'toggle' && typeof value === 'boolean') {
      return (
        <Switch
          value={value}
          onValueChange={onToggle}
          trackColor={{ false: COLORS.backgroundLighter, true: COLORS.primaryDark }}
          thumbColor={value ? COLORS.primary : COLORS.textMuted}
          disabled={disabled}
        />
      );
    }

    if (type === 'value') {
      return (
        <View style={styles.valueContainer}>
          <Text style={styles.valueText}>{String(value)}</Text>
          {showArrow && <Text style={styles.arrow}>{'\u203A'}</Text>}
        </View>
      );
    }

    if (showArrow) {
      return <Text style={styles.arrow}>{'\u203A'}</Text>;
    }

    return null;
  };

  const content = (
    <>
      <View style={styles.leftContent}>
        <Text style={[styles.title, disabled && styles.disabledText]}>{title}</Text>
        {subtitle && (
          <Text style={[styles.subtitle, disabled && styles.disabledText]}>
            {subtitle}
          </Text>
        )}
      </View>
      {renderRight()}
    </>
  );

  if (type === 'toggle') {
    return (
      <View style={[styles.container, disabled && styles.disabled]}>
        {content}
      </View>
    );
  }

  return (
    <Pressable
      style={({ pressed }) => [
        styles.container,
        pressed && styles.pressed,
        disabled && styles.disabled,
      ]}
      onPress={onPress}
      disabled={disabled}
    >
      {content}
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.surface,
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.sm,
  },
  pressed: {
    opacity: 0.7,
  },
  disabled: {
    opacity: 0.5,
  },
  leftContent: {
    flex: 1,
    marginRight: SPACING.md,
  },
  title: {
    fontSize: 16,
    fontWeight: '500',
    color: COLORS.text,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  disabledText: {
    color: COLORS.textMuted,
  },
  valueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  valueText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginRight: SPACING.xs,
  },
  arrow: {
    fontSize: 20,
    color: COLORS.textMuted,
    fontWeight: '300',
  },
});
