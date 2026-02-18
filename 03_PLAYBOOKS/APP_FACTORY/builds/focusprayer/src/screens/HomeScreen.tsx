/**
 * Home Screen
 * Main dashboard showing devotion status, streak, and actions
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useUserStore } from '../stores/userStore';
import { useDevotionStore } from '../stores/devotionStore';
import { fetchDailyPassage } from '../services/bibleService';
import { getStreakMessage, getEncouragement, isStreakAtRisk } from '../services/streakService';
import { COLORS } from '../utils/constants';
import { formatDuration } from '../utils/dateUtils';
import { RootStackParamList, DevotionStatus } from '../types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [loading, setLoading] = useState(true);

  const { settings, checkAccess, getTrialDaysRemaining } = useUserStore();
  const {
    todayStatus,
    streak,
    loadTodayStatus,
    loadStreak,
    setTodaysPassage,
    startSession,
  } = useDevotionStore();

  useEffect(() => {
    initializeHome();
  }, []);

  async function initializeHome() {
    setLoading(true);
    try {
      await Promise.all([loadTodayStatus(), loadStreak()]);

      // Pre-fetch today's passage
      const passage = await fetchDailyPassage();
      setTodaysPassage(passage);
    } catch (error) {
      console.error('Failed to initialize home:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleStartDevotion() {
    // Check subscription access
    if (!checkAccess()) {
      navigation.navigate('Paywall');
      return;
    }

    startSession(settings.devotionDurationMinutes);

    if (settings.requireTimer && settings.requireScripture) {
      // Both required, start with timer
      navigation.navigate('Timer');
    } else if (settings.requireTimer) {
      navigation.navigate('Timer');
    } else if (settings.requireScripture) {
      navigation.navigate('Scripture');
    }
  }

  function getStatusDisplay(): { title: string; subtitle: string; color: string } {
    switch (todayStatus) {
      case 'completed':
        return {
          title: 'Devotion Complete',
          subtitle: 'Your apps are unlocked for the day',
          color: COLORS.success,
        };
      case 'bypassed':
        return {
          title: 'Emergency Unlock Used',
          subtitle: 'Your streak has been reset',
          color: COLORS.warning,
        };
      case 'in_progress':
        return {
          title: 'In Progress',
          subtitle: 'Continue your devotion',
          color: COLORS.primary,
        };
      default:
        return {
          title: 'Apps Locked',
          subtitle: 'Complete your devotion to unlock',
          color: COLORS.error,
        };
    }
  }

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  const hasAccess = checkAccess();
  const trialDays = getTrialDaysRemaining();
  const status = getStatusDisplay();
  const streakAtRisk = isStreakAtRisk(streak);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Trial Banner */}
      {hasAccess && trialDays > 0 && (
        <View style={styles.trialBanner}>
          <Text style={styles.trialText}>
            {trialDays} day{trialDays !== 1 ? 's' : ''} left in trial
          </Text>
        </View>
      )}

      {/* Status Card */}
      <View style={[styles.statusCard, { borderLeftColor: status.color }]}>
        <Text style={styles.statusTitle}>{status.title}</Text>
        <Text style={styles.statusSubtitle}>{status.subtitle}</Text>
      </View>

      {/* Streak Display */}
      <View style={styles.streakCard}>
        <View style={styles.streakMain}>
          <Text style={styles.streakNumber}>{streak.currentStreak}</Text>
          <Text style={styles.streakLabel}>day streak</Text>
        </View>

        {streakAtRisk && todayStatus === 'not_started' && (
          <View style={styles.streakWarning}>
            <Text style={styles.streakWarningText}>
              Complete today to keep your streak alive
            </Text>
          </View>
        )}

        <Text style={styles.streakMessage}>{getStreakMessage(streak)}</Text>

        <View style={styles.streakStats}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{streak.longestStreak}</Text>
            <Text style={styles.statLabel}>Best</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{streak.totalDaysCompleted}</Text>
            <Text style={styles.statLabel}>Total</Text>
          </View>
        </View>
      </View>

      {/* Today's Devotion Info */}
      {todayStatus === 'not_started' && (
        <View style={styles.devotionInfo}>
          <Text style={styles.devotionInfoTitle}>Today's devotion</Text>
          <View style={styles.devotionRequirements}>
            {settings.requireTimer && (
              <View style={styles.requirement}>
                <Text style={styles.requirementIcon}>&#128336;</Text>
                <Text style={styles.requirementText}>
                  {formatDuration(settings.devotionDurationMinutes * 60)} prayer
                </Text>
              </View>
            )}
            {settings.requireScripture && (
              <View style={styles.requirement}>
                <Text style={styles.requirementIcon}>&#128214;</Text>
                <Text style={styles.requirementText}>Scripture reading</Text>
              </View>
            )}
          </View>
        </View>
      )}

      {/* Action Button */}
      {todayStatus !== 'completed' && (
        <TouchableOpacity
          style={styles.actionButton}
          onPress={handleStartDevotion}
          activeOpacity={0.8}
        >
          <Text style={styles.actionButtonText}>
            {todayStatus === 'in_progress' ? 'Continue Devotion' : 'Start Devotion'}
          </Text>
        </TouchableOpacity>
      )}

      {/* Encouragement */}
      <Text style={styles.encouragement}>
        {getEncouragement(streak.currentStreak)}
      </Text>

      {/* Blocked Apps Info */}
      {settings.blockedApps.length > 0 && todayStatus !== 'completed' && (
        <View style={styles.blockedInfo}>
          <Text style={styles.blockedInfoText}>
            {settings.blockedApps.length} app
            {settings.blockedApps.length !== 1 ? 's' : ''} blocked until complete
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  loadingText: {
    marginTop: 12,
    color: COLORS.textSecondary,
    fontSize: 16,
  },
  trialBanner: {
    backgroundColor: COLORS.secondary,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  trialText: {
    color: COLORS.surface,
    fontWeight: '600',
    textAlign: 'center',
  },
  statusCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statusTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  statusSubtitle: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  streakCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 24,
    marginBottom: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  streakMain: {
    alignItems: 'center',
    marginBottom: 12,
  },
  streakNumber: {
    fontSize: 64,
    fontWeight: '800',
    color: COLORS.streak,
  },
  streakLabel: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginTop: -8,
  },
  streakWarning: {
    backgroundColor: COLORS.warning + '20',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    marginBottom: 12,
  },
  streakWarningText: {
    color: COLORS.warning,
    fontWeight: '600',
    fontSize: 14,
  },
  streakMessage: {
    fontSize: 16,
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 20,
  },
  streakStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statItem: {
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  statDivider: {
    width: 1,
    height: 40,
    backgroundColor: COLORS.disabled,
  },
  devotionInfo: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
  },
  devotionInfoTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  devotionRequirements: {
    gap: 12,
  },
  requirement: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  requirementIcon: {
    fontSize: 20,
  },
  requirementText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 18,
    alignItems: 'center',
    marginBottom: 20,
  },
  actionButtonText: {
    color: COLORS.surface,
    fontSize: 18,
    fontWeight: '700',
  },
  encouragement: {
    textAlign: 'center',
    color: COLORS.textSecondary,
    fontSize: 15,
    fontStyle: 'italic',
    marginBottom: 20,
  },
  blockedInfo: {
    alignItems: 'center',
  },
  blockedInfoText: {
    color: COLORS.error,
    fontSize: 14,
  },
});
