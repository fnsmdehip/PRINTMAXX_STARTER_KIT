import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { TimerDisplay } from '../../src/components/timer/TimerDisplay';
import { TimerControls } from '../../src/components/timer/TimerControls';
import { StreakBadge } from '../../src/components/common/StreakBadge';
import { useTimer } from '../../src/hooks/useTimer';
import { useStreakStore } from '../../src/stores/streakStore';
import { COLORS, TYPOGRAPHY, SPACING, STUDY_QUOTES } from '../../src/utils/constants';
import { formatDuration } from '../../src/utils/dateUtils';

export default function HomeScreen() {
  const {
    timerState,
    remainingSeconds,
    totalSeconds,
    currentSessionType,
    todayStudyTime,
    isStudying,
    isOnBreak,
    sessionsCompletedToday,
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    startBreak,
    skipBreak,
  } = useTimer();

  const { currentStreak } = useStreakStore();

  // Get random quote for motivation
  const [quote] = React.useState(() =>
    STUDY_QUOTES[Math.floor(Math.random() * STUDY_QUOTES.length)]
  );

  const handleEndSession = () => {
    endSession(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header with streak */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              {getGreeting()}, Student
            </Text>
            <Text style={styles.todayStats}>
              {formatDuration(todayStudyTime)} studied today
            </Text>
          </View>
          <StreakBadge streak={currentStreak} size="medium" />
        </View>

        {/* Timer */}
        <View style={styles.timerContainer}>
          <TimerDisplay
            remainingSeconds={remainingSeconds}
            totalSeconds={totalSeconds}
            isStudying={isStudying || timerState === 'paused'}
            isBreak={isOnBreak}
          />
        </View>

        {/* Motivational quote during session */}
        {(isStudying || timerState === 'paused') && (
          <View style={styles.quoteContainer}>
            <Text style={styles.quote}>"{quote}"</Text>
          </View>
        )}

        {/* Session info */}
        {timerState === 'idle' && (
          <View style={styles.sessionInfo}>
            <View style={styles.sessionStat}>
              <Text style={styles.sessionStatValue}>{sessionsCompletedToday}</Text>
              <Text style={styles.sessionStatLabel}>
                session{sessionsCompletedToday !== 1 ? 's' : ''} today
              </Text>
            </View>
          </View>
        )}

        {/* Controls */}
        <View style={styles.controlsContainer}>
          <TimerControls
            timerState={timerState}
            currentSessionType={currentSessionType}
            onStart={startSession}
            onPause={pauseSession}
            onResume={resumeSession}
            onEnd={handleEndSession}
            onStartBreak={startBreak}
            onSkipBreak={skipBreak}
          />
        </View>

        {/* Blocking notice */}
        {isStudying && (
          <View style={styles.blockingNotice}>
            <Text style={styles.blockingIcon}>🔒</Text>
            <Text style={styles.blockingText}>
              Distracting apps are blocked until your session ends
            </Text>
          </View>
        )}

        {/* Break notice */}
        {isOnBreak && (
          <View style={styles.breakNotice}>
            <Text style={styles.breakIcon}>☕</Text>
            <Text style={styles.breakText}>
              Take a break! Stretch, hydrate, rest your eyes.
            </Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  greeting: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
  },
  todayStats: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  quoteContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.xl,
  },
  quote: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    fontStyle: 'italic',
    textAlign: 'center',
  },
  sessionInfo: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  sessionStat: {
    alignItems: 'center',
  },
  sessionStatValue: {
    ...TYPOGRAPHY.h1,
    color: COLORS.primary,
  },
  sessionStatLabel: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
  },
  controlsContainer: {
    marginBottom: SPACING.xl,
  },
  blockingNotice: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary + '10',
    borderRadius: 12,
    padding: SPACING.md,
  },
  blockingIcon: {
    fontSize: 20,
    marginRight: SPACING.sm,
  },
  blockingText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.primary,
    flex: 1,
  },
  breakNotice: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.secondary + '10',
    borderRadius: 12,
    padding: SPACING.md,
  },
  breakIcon: {
    fontSize: 20,
    marginRight: SPACING.sm,
  },
  breakText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.secondary,
    flex: 1,
  },
});
