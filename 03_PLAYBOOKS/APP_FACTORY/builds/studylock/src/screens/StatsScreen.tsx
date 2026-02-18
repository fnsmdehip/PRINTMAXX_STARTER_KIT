import React, { useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useUserStore } from '../stores/userStore';
import { COLORS, SUBJECTS } from '../utils/constants';
import { formatMinutes, formatHoursDecimal, getLast7Days } from '../utils/timer';
import Card from '../components/Card';
import StatsCard from '../components/StatsCard';
import StreakBadge from '../components/StreakBadge';
import WeeklyChart from '../components/WeeklyChart';

export default function StatsScreen() {
  const router = useRouter();
  const { progress, dailyStats } = useUserStore();

  // Calculate weekly stats
  const weeklyStats = useMemo(() => {
    const last7Days = getLast7Days();
    const weekData = dailyStats.filter((s) => last7Days.includes(s.date));

    return {
      totalMinutes: weekData.reduce((sum, d) => sum + d.totalMinutes, 0),
      totalSessions: weekData.reduce((sum, d) => sum + d.sessions, 0),
      questionsAnswered: weekData.reduce((sum, d) => sum + d.questionsAnswered, 0),
      correctAnswers: weekData.reduce((sum, d) => sum + d.correctAnswers, 0),
    };
  }, [dailyStats]);

  // Calculate subject breakdown
  const subjectBreakdown = useMemo(() => {
    const totals: Record<string, number> = {};

    dailyStats.forEach((day) => {
      Object.entries(day.subjectBreakdown).forEach(([subject, minutes]) => {
        totals[subject] = (totals[subject] || 0) + minutes;
      });
    });

    return Object.entries(totals)
      .filter(([_, minutes]) => minutes > 0)
      .sort(([, a], [, b]) => b - a)
      .map(([subject, minutes]) => ({
        subject,
        minutes,
        percentage: Math.round((minutes / progress.totalStudyMinutes) * 100) || 0,
      }));
  }, [dailyStats, progress.totalStudyMinutes]);

  const quizAccuracy =
    progress.questionsAnswered > 0
      ? Math.round((progress.correctAnswers / progress.questionsAnswered) * 100)
      : 0;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color={COLORS.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Statistics</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Streak */}
        <View style={styles.streakSection}>
          <StreakBadge streak={progress.currentStreak} size="large" />
        </View>

        {/* Overview Stats */}
        <View style={styles.statsGrid}>
          <StatsCard
            title="Total Hours"
            value={formatHoursDecimal(progress.totalStudyMinutes)}
            subtitle={`${progress.totalSessions} sessions`}
            icon="time-outline"
            iconColor={COLORS.primary}
          />
          <StatsCard
            title="Best Streak"
            value={progress.longestStreak}
            subtitle="days"
            icon="flame-outline"
            iconColor={COLORS.accent}
          />
          <StatsCard
            title="This Week"
            value={formatMinutes(weeklyStats.totalMinutes)}
            subtitle={`${weeklyStats.totalSessions} sessions`}
            icon="calendar-outline"
            iconColor={COLORS.secondary}
          />
          <StatsCard
            title="Quiz Accuracy"
            value={`${quizAccuracy}%`}
            subtitle={`${progress.questionsAnswered} questions`}
            icon="school-outline"
            iconColor="#9333EA"
          />
        </View>

        {/* Weekly Chart */}
        <Card variant="outlined" padding="none" style={styles.chartCard}>
          <WeeklyChart dailyStats={dailyStats} height={140} />
        </Card>

        {/* Subject Breakdown */}
        <Text style={styles.sectionTitle}>Subject Breakdown</Text>
        <Card variant="outlined" padding="medium" style={styles.subjectCard}>
          {subjectBreakdown.length > 0 ? (
            subjectBreakdown.map(({ subject, minutes, percentage }) => {
              const subjectInfo = SUBJECTS.find((s) => s.id === subject);

              return (
                <View key={subject} style={styles.subjectRow}>
                  <View style={styles.subjectInfo}>
                    <Text style={styles.subjectEmoji}>{subjectInfo?.emoji || '📚'}</Text>
                    <Text style={styles.subjectName}>
                      {subjectInfo?.label || subject}
                    </Text>
                  </View>
                  <View style={styles.subjectStats}>
                    <View style={styles.progressBarContainer}>
                      <View
                        style={[
                          styles.progressBarFill,
                          { width: `${percentage}%` },
                        ]}
                      />
                    </View>
                    <Text style={styles.subjectMinutes}>
                      {formatMinutes(minutes)}
                    </Text>
                  </View>
                </View>
              );
            })
          ) : (
            <View style={styles.emptySubjects}>
              <Ionicons name="analytics-outline" size={40} color={COLORS.textMuted} />
              <Text style={styles.emptyText}>No study data yet</Text>
              <Text style={styles.emptySubtext}>
                Complete study sessions to see your subject breakdown
              </Text>
            </View>
          )}
        </Card>

        {/* Quiz Stats */}
        <Text style={styles.sectionTitle}>Quiz Performance</Text>
        <Card variant="outlined" padding="medium" style={styles.quizCard}>
          <View style={styles.quizStatRow}>
            <View style={styles.quizStat}>
              <Text style={styles.quizStatValue}>{progress.questionsAnswered}</Text>
              <Text style={styles.quizStatLabel}>Questions Answered</Text>
            </View>
            <View style={styles.quizStatDivider} />
            <View style={styles.quizStat}>
              <Text style={styles.quizStatValue}>{progress.correctAnswers}</Text>
              <Text style={styles.quizStatLabel}>Correct Answers</Text>
            </View>
            <View style={styles.quizStatDivider} />
            <View style={styles.quizStat}>
              <Text style={[styles.quizStatValue, { color: COLORS.success }]}>
                {quizAccuracy}%
              </Text>
              <Text style={styles.quizStatLabel}>Accuracy</Text>
            </View>
          </View>

          <TouchableOpacity
            style={styles.practiceButton}
            onPress={() => router.push('/quiz')}
          >
            <Ionicons name="school" size={20} color={COLORS.primary} />
            <Text style={styles.practiceButtonText}>Practice Quiz</Text>
            <Ionicons name="chevron-forward" size={20} color={COLORS.primary} />
          </TouchableOpacity>
        </Card>

        {/* Milestones */}
        <Text style={styles.sectionTitle}>Milestones</Text>
        <Card variant="outlined" padding="medium">
          <View style={styles.milestonesGrid}>
            {[
              { hours: 1, icon: 'star', unlocked: progress.totalStudyMinutes >= 60 },
              { hours: 10, icon: 'medal', unlocked: progress.totalStudyMinutes >= 600 },
              { hours: 50, icon: 'trophy', unlocked: progress.totalStudyMinutes >= 3000 },
              { hours: 100, icon: 'ribbon', unlocked: progress.totalStudyMinutes >= 6000 },
            ].map((milestone) => (
              <View
                key={milestone.hours}
                style={[
                  styles.milestone,
                  !milestone.unlocked && styles.milestoneLocked,
                ]}
              >
                <Ionicons
                  name={milestone.icon as keyof typeof Ionicons.glyphMap}
                  size={24}
                  color={milestone.unlocked ? COLORS.accent : COLORS.textMuted}
                />
                <Text
                  style={[
                    styles.milestoneText,
                    !milestone.unlocked && styles.milestoneTextLocked,
                  ]}
                >
                  {milestone.hours}h
                </Text>
              </View>
            ))}
          </View>
        </Card>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  headerSpacer: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 40,
  },
  streakSection: {
    alignItems: 'center',
    marginVertical: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 16,
  },
  chartCard: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 12,
    marginLeft: 4,
  },
  subjectCard: {
    gap: 16,
    marginBottom: 24,
  },
  subjectRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  subjectInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  subjectEmoji: {
    fontSize: 20,
  },
  subjectName: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.text,
    textTransform: 'capitalize',
  },
  subjectStats: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
    marginLeft: 16,
  },
  progressBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: COLORS.surfaceAlt,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  subjectMinutes: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    width: 50,
    textAlign: 'right',
  },
  emptySubjects: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  emptyText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 12,
  },
  emptySubtext: {
    fontSize: 13,
    color: COLORS.textMuted,
    textAlign: 'center',
    marginTop: 4,
  },
  quizCard: {
    marginBottom: 24,
  },
  quizStatRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  quizStat: {
    flex: 1,
    alignItems: 'center',
  },
  quizStatValue: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  quizStatLabel: {
    fontSize: 11,
    color: COLORS.textSecondary,
    marginTop: 4,
    textAlign: 'center',
  },
  quizStatDivider: {
    width: 1,
    backgroundColor: COLORS.border,
    marginVertical: 4,
  },
  practiceButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary + '10',
    paddingVertical: 12,
    borderRadius: 12,
    gap: 8,
  },
  practiceButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  milestonesGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  milestone: {
    alignItems: 'center',
    padding: 12,
  },
  milestoneLocked: {
    opacity: 0.4,
  },
  milestoneText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 4,
  },
  milestoneTextLocked: {
    color: COLORS.textMuted,
  },
});
