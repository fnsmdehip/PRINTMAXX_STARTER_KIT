import React, { useEffect, useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  RefreshControl,
} from 'react-native';
import { COLORS } from '../utils/constants';
import { ProgressRing } from '../components/ProgressRing';
import { StreakBadge } from '../components/StreakBadge';
import { Button } from '../components/Button';
import { useStepStore } from '../stores/stepStore';
import { useUserStore } from '../stores/userStore';
import { getTodaySteps } from '../services/stepService';
import { updateBlockingState } from '../services/blockerService';
import { estimateWalkingTime, formatTimeRemaining } from '../utils/dateUtils';

interface Props {
  navigation: any;
}

export function HomeScreen({ navigation }: Props) {
  const [refreshing, setRefreshing] = useState(false);

  const {
    currentSteps,
    stepGoal,
    isUnlocked,
    todayCompleted,
    setCurrentSteps,
    markTodayCompleted,
    setLoading,
    setError,
  } = useStepStore();

  const { settings, streak, updateStreak } = useUserStore();

  const progress = stepGoal > 0 ? currentSteps / stepGoal : 0;
  const stepsRemaining = Math.max(0, stepGoal - currentSteps);
  const timeRemaining = estimateWalkingTime(stepsRemaining);

  const fetchSteps = useCallback(async () => {
    setLoading(true);
    setError(null);

    const result = await getTodaySteps();

    if (result.error) {
      setError(result.error);
    } else {
      setCurrentSteps(result.steps);

      // Check if goal was just met
      if (result.steps >= stepGoal && !todayCompleted) {
        markTodayCompleted();
        updateStreak(true);
        await updateBlockingState(true, settings.blockedApps);
      }
    }

    setLoading(false);
  }, [
    stepGoal,
    todayCompleted,
    settings.blockedApps,
    setCurrentSteps,
    markTodayCompleted,
    updateStreak,
    setLoading,
    setError,
  ]);

  useEffect(() => {
    fetchSteps();

    // Set up interval for background refresh
    const interval = setInterval(fetchSteps, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, [fetchSteps]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchSteps();
    setRefreshing(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={COLORS.primary}
          />
        }
      >
        {/* Status Badge */}
        <View style={styles.statusContainer}>
          <View
            style={[
              styles.statusBadge,
              isUnlocked ? styles.statusUnlocked : styles.statusLocked,
            ]}
          >
            <Text style={styles.statusText}>
              {isUnlocked ? '🔓 Apps Unlocked' : '🔒 Apps Locked'}
            </Text>
          </View>
          <StreakBadge streak={streak} compact />
        </View>

        {/* Progress Ring */}
        <View style={styles.progressContainer}>
          <ProgressRing
            progress={progress}
            steps={currentSteps}
            goal={stepGoal}
          />
        </View>

        {/* Remaining Info */}
        {!isUnlocked && (
          <View style={styles.remainingContainer}>
            <Text style={styles.remainingSteps}>
              {stepsRemaining.toLocaleString()} steps to go
            </Text>
            <Text style={styles.remainingTime}>
              About {formatTimeRemaining(timeRemaining)} of walking
            </Text>
          </View>
        )}

        {/* Success Message */}
        {isUnlocked && (
          <View style={styles.successContainer}>
            <Text style={styles.successTitle}>Great job!</Text>
            <Text style={styles.successMessage}>
              You've hit your {stepGoal.toLocaleString()} step goal.
              All your apps are unlocked for the rest of the day.
            </Text>
          </View>
        )}

        {/* Quick Actions */}
        <View style={styles.actionsContainer}>
          {settings.blockedApps.length === 0 && (
            <View style={styles.warningCard}>
              <Text style={styles.warningText}>
                No apps blocked. Add apps in Settings to start.
              </Text>
              <Button
                title="Add apps to block"
                onPress={() => navigation.navigate('Settings')}
                variant="outline"
                size="small"
              />
            </View>
          )}

          {settings.blockedApps.length > 0 && !isUnlocked && (
            <View style={styles.blockedCard}>
              <Text style={styles.blockedTitle}>
                {settings.blockedApps.length} app{settings.blockedApps.length !== 1 ? 's' : ''} blocked
              </Text>
              <Text style={styles.blockedList}>
                {settings.blockedApps
                  .slice(0, 3)
                  .map((app) => app.name)
                  .join(', ')}
                {settings.blockedApps.length > 3 && ` +${settings.blockedApps.length - 3} more`}
              </Text>
            </View>
          )}
        </View>

        {/* Motivation Quote */}
        <View style={styles.quoteContainer}>
          <Text style={styles.quote}>
            "{getMotivationalQuote(progress, isUnlocked)}"
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function getMotivationalQuote(progress: number, isUnlocked: boolean): string {
  if (isUnlocked) {
    return "You earned it. Enjoy your apps.";
  }
  if (progress === 0) {
    return "Every step counts. Start walking.";
  }
  if (progress < 0.25) {
    return "You're getting started. Keep moving.";
  }
  if (progress < 0.5) {
    return "Solid progress. You're warming up.";
  }
  if (progress < 0.75) {
    return "More than halfway there. Push through.";
  }
  return "Almost there. Finish strong.";
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: 20,
  },
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  statusBadge: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  statusLocked: {
    backgroundColor: '#FFEBEE',
  },
  statusUnlocked: {
    backgroundColor: '#E8F5E9',
  },
  statusText: {
    fontSize: 14,
    fontWeight: '600',
  },
  progressContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  remainingContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  remainingSteps: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  remainingTime: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  successContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 24,
  },
  successTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.success,
    marginBottom: 8,
  },
  successMessage: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  actionsContainer: {
    marginBottom: 24,
  },
  warningCard: {
    backgroundColor: '#FFF3E0',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
  },
  warningText: {
    fontSize: 14,
    color: '#E65100',
    marginBottom: 12,
    textAlign: 'center',
  },
  blockedCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
  },
  blockedTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  blockedList: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  quoteContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
  },
  quote: {
    fontSize: 16,
    fontStyle: 'italic',
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
