import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useUserStore } from '../stores/userStore';
import { useStudyStore } from '../stores/studyStore';
import { COLORS, FOCUS_MODES } from '../utils/constants';
import { formatMinutes } from '../utils/timer';
import Card from '../components/Card';
import Button from '../components/Button';
import StreakBadge from '../components/StreakBadge';
import StatsCard from '../components/StatsCard';
import WeeklyChart from '../components/WeeklyChart';
import SubjectPicker from '../components/SubjectPicker';
import DurationSelector from '../components/DurationSelector';
import FocusModeSelector from '../components/FocusModeSelector';

export default function HomeScreen() {
  const router = useRouter();
  const { progress, dailyStats, loadUserData, isLoading } = useUserStore();
  const {
    selectedSubject,
    setSelectedSubject,
    timer,
    customDuration,
    setCustomDuration,
  } = useStudyStore();

  const [selectedMode, setSelectedMode] = React.useState<'pomodoro' | 'deepWork' | 'examPrep' | 'custom'>('pomodoro');
  const [selectedDuration, setSelectedDuration] = React.useState(25);

  useEffect(() => {
    loadUserData();
  }, []);

  const handleStartSession = () => {
    router.push({
      pathname: '/timer',
      params: {
        mode: selectedMode,
        duration: selectedDuration,
        subject: selectedSubject,
      },
    });
  };

  const todayStats = dailyStats.find(
    (s) => s.date === new Date().toISOString().split('T')[0]
  );

  const todayMinutes = todayStats?.totalMinutes || 0;
  const todaySessions = todayStats?.sessions || 0;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Ready to study?</Text>
            <Text style={styles.tagline}>Study First, Scroll Later</Text>
          </View>
          <TouchableOpacity
            style={styles.settingsButton}
            onPress={() => router.push('/settings')}
          >
            <Ionicons name="settings-outline" size={24} color={COLORS.text} />
          </TouchableOpacity>
        </View>

        {/* Streak Badge */}
        <View style={styles.streakContainer}>
          <StreakBadge streak={progress.currentStreak} size="large" />
        </View>

        {/* Today's Summary */}
        <View style={styles.statsRow}>
          <StatsCard
            title="Today"
            value={formatMinutes(todayMinutes)}
            subtitle={`${todaySessions} session${todaySessions !== 1 ? 's' : ''}`}
            icon="today-outline"
            iconColor={COLORS.primary}
          />
          <StatsCard
            title="Total Hours"
            value={Math.floor(progress.totalStudyMinutes / 60)}
            subtitle={`${progress.totalSessions} sessions`}
            icon="time-outline"
            iconColor={COLORS.secondary}
          />
        </View>

        {/* Focus Mode Selection */}
        <FocusModeSelector
          selectedMode={selectedMode}
          onSelectMode={setSelectedMode}
        />

        {/* Duration Selection */}
        <DurationSelector
          selectedDuration={selectedDuration}
          onSelectDuration={setSelectedDuration}
          isPremium={progress.isPremium}
          maxFreeDuration={25}
        />

        {/* Subject Selection */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionLabel}>Study Subject</Text>
        </View>
        <SubjectPicker
          selectedSubject={selectedSubject}
          onSelectSubject={setSelectedSubject}
        />

        {/* Weekly Progress */}
        <Card variant="outlined" padding="none" style={styles.chartCard}>
          <WeeklyChart dailyStats={dailyStats} />
        </Card>

        {/* Quick Stats */}
        <View style={styles.quickStats}>
          <View style={styles.quickStatItem}>
            <Text style={styles.quickStatValue}>
              {Math.round(
                (progress.correctAnswers / Math.max(progress.questionsAnswered, 1)) * 100
              )}%
            </Text>
            <Text style={styles.quickStatLabel}>Quiz Accuracy</Text>
          </View>
          <View style={styles.quickStatDivider} />
          <View style={styles.quickStatItem}>
            <Text style={styles.quickStatValue}>{progress.longestStreak}</Text>
            <Text style={styles.quickStatLabel}>Best Streak</Text>
          </View>
          <View style={styles.quickStatDivider} />
          <View style={styles.quickStatItem}>
            <Text style={styles.quickStatValue}>{progress.questionsAnswered}</Text>
            <Text style={styles.quickStatLabel}>Questions</Text>
          </View>
        </View>

        {/* Start Button */}
        <View style={styles.startButtonContainer}>
          <Button
            title="Start Focus Session"
            onPress={handleStartSession}
            size="large"
            fullWidth
          />
        </View>

        {/* Pro Upgrade Banner (if not premium) */}
        {!progress.isPremium && (
          <TouchableOpacity
            style={styles.proBanner}
            onPress={() => router.push('/paywall')}
          >
            <View style={styles.proBannerContent}>
              <Ionicons name="star" size={20} color={COLORS.accent} />
              <View style={styles.proBannerText}>
                <Text style={styles.proBannerTitle}>Unlock StudyLock Pro</Text>
                <Text style={styles.proBannerSubtitle}>
                  Unlimited sessions, all subjects, and more
                </Text>
              </View>
            </View>
            <Ionicons name="chevron-forward" size={20} color={COLORS.textSecondary} />
          </TouchableOpacity>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 100,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 16,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
  },
  tagline: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  settingsButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
  },
  streakContainer: {
    alignItems: 'center',
    marginVertical: 24,
  },
  statsRow: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    gap: 12,
  },
  sectionHeader: {
    paddingHorizontal: 16,
    marginTop: 8,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  chartCard: {
    marginHorizontal: 16,
    marginTop: 24,
  },
  quickStats: {
    flexDirection: 'row',
    marginHorizontal: 16,
    marginTop: 16,
    padding: 16,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
  },
  quickStatItem: {
    flex: 1,
    alignItems: 'center',
  },
  quickStatValue: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
  },
  quickStatLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  quickStatDivider: {
    width: 1,
    backgroundColor: COLORS.border,
    marginVertical: 4,
  },
  startButtonContainer: {
    paddingHorizontal: 16,
    marginTop: 24,
  },
  proBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginHorizontal: 16,
    marginTop: 16,
    padding: 16,
    backgroundColor: COLORS.accent + '10',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.accent + '30',
  },
  proBannerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  proBannerText: {
    gap: 2,
  },
  proBannerTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
  },
  proBannerSubtitle: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
