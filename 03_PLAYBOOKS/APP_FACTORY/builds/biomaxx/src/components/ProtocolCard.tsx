import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Pressable,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { COLORS } from '../utils/constants';
import { Protocol } from '../types';
import { StreakBadge } from './StreakBadge';

interface ProtocolCardProps {
  protocol: Protocol;
  streak: number;
  todayValue: number;
  isPremiumUser: boolean;
  onPress: () => void;
  onStartSession?: () => void;
  onLog?: () => void;
}

export function ProtocolCard({
  protocol,
  streak,
  todayValue,
  isPremiumUser,
  onPress,
  onStartSession,
  onLog,
}: ProtocolCardProps) {
  const isLocked = protocol.isPremium && !isPremiumUser;
  const progress = Math.min((todayValue / protocol.dailyGoal) * 100, 100);
  const isComplete = progress >= 100;

  const handlePress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    onPress();
  };

  const handleAction = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    if (protocol.unit === 'minutes' || protocol.unit === 'hours') {
      onStartSession?.();
    } else {
      onLog?.();
    }
  };

  const getProgressColor = () => {
    if (isComplete) return COLORS.accent;
    if (progress > 50) return COLORS.primary;
    return COLORS.primaryLight;
  };

  const formatValue = () => {
    if (protocol.unit === 'hours') {
      return `${todayValue.toFixed(1)}h / ${protocol.dailyGoal}h`;
    }
    if (protocol.unit === 'minutes') {
      return `${Math.round(todayValue)}m / ${protocol.dailyGoal}m`;
    }
    return `${todayValue} / ${protocol.dailyGoal}`;
  };

  const getActionLabel = () => {
    if (protocol.unit === 'minutes' || protocol.unit === 'hours') {
      return 'Start Session';
    }
    return 'Log';
  };

  return (
    <Pressable
      style={({ pressed }) => [
        styles.container,
        pressed && styles.pressed,
        isLocked && styles.locked,
      ]}
      onPress={handlePress}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.iconContainer}>
          <Ionicons
            name={protocol.icon as any}
            size={24}
            color={isLocked ? COLORS.textMuted : COLORS.primary}
          />
        </View>
        <View style={styles.titleContainer}>
          <View style={styles.titleRow}>
            <Text style={[styles.name, isLocked && styles.lockedText]}>
              {protocol.name}
            </Text>
            {isLocked && (
              <Ionicons
                name="lock-closed"
                size={14}
                color={COLORS.textMuted}
                style={styles.lockIcon}
              />
            )}
          </View>
          <Text style={styles.description} numberOfLines={1}>
            {protocol.description}
          </Text>
        </View>
        {streak > 0 && !isLocked && <StreakBadge streak={streak} size="small" />}
      </View>

      {/* Progress */}
      {!isLocked && (
        <View style={styles.progressSection}>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressFill,
                {
                  width: `${progress}%`,
                  backgroundColor: getProgressColor(),
                },
              ]}
            />
          </View>
          <Text style={styles.progressText}>{formatValue()}</Text>
        </View>
      )}

      {/* Action Button */}
      <TouchableOpacity
        style={[styles.actionButton, isLocked && styles.actionButtonLocked]}
        onPress={isLocked ? handlePress : handleAction}
        activeOpacity={0.7}
      >
        <Text style={[styles.actionText, isLocked && styles.actionTextLocked]}>
          {isLocked ? 'Unlock Premium' : getActionLabel()}
        </Text>
        <Ionicons
          name={isLocked ? 'arrow-forward' : 'play'}
          size={16}
          color={isLocked ? COLORS.textMuted : COLORS.background}
        />
      </TouchableOpacity>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  pressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
  locked: {
    opacity: 0.7,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  iconContainer: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  titleContainer: {
    flex: 1,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  lockedText: {
    color: COLORS.textMuted,
  },
  lockIcon: {
    marginLeft: 6,
  },
  description: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  progressSection: {
    marginBottom: 12,
  },
  progressBar: {
    height: 6,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: 3,
    overflow: 'hidden',
    marginBottom: 6,
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  progressText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textAlign: 'right',
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
  },
  actionButtonLocked: {
    backgroundColor: COLORS.surfaceLight,
  },
  actionText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.background,
  },
  actionTextLocked: {
    color: COLORS.textMuted,
  },
});
