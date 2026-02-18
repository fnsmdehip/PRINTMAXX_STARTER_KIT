import { View, Text, StyleSheet, ScrollView, Dimensions } from 'react-native';
import { useDevotionStore } from '../../src/stores/devotionStore';

const { width } = Dimensions.get('window');
const DAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

function CalendarGrid() {
  const completedDates = useDevotionStore((state) => state.completedDates);

  // Generate last 35 days (5 weeks)
  const today = new Date();
  const days: { date: Date; completed: boolean; isToday: boolean }[] = [];

  for (let i = 34; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    days.push({
      date,
      completed: completedDates.includes(dateStr),
      isToday: i === 0,
    });
  }

  return (
    <View style={styles.calendarContainer}>
      <View style={styles.dayLabels}>
        {DAYS.map((day, i) => (
          <Text key={i} style={styles.dayLabel}>{day}</Text>
        ))}
      </View>
      <View style={styles.calendarGrid}>
        {days.map((day, i) => (
          <View
            key={i}
            style={[
              styles.calendarDay,
              day.completed && styles.calendarDayCompleted,
              day.isToday && styles.calendarDayToday,
            ]}
          >
            <Text style={[
              styles.calendarDayText,
              day.completed && styles.calendarDayTextCompleted,
            ]}>
              {day.date.getDate()}
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
}

export default function Stats() {
  const currentStreak = useDevotionStore((state) => state.currentStreak);
  const longestStreak = useDevotionStore((state) => state.longestStreak);
  const totalDaysCompleted = useDevotionStore((state) => state.totalDaysCompleted);
  const sessions = useDevotionStore((state) => state.sessions);

  // Calculate total prayer time
  const totalMinutes = sessions.reduce((acc, session) => {
    if (session.completedAt) {
      return acc + Math.floor(session.timerDuration / 60);
    }
    return acc;
  }, 0);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.sectionTitle}>Your Progress</Text>

      <View style={styles.statsGrid}>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>🔥</Text>
          <Text style={styles.statNumber}>{currentStreak}</Text>
          <Text style={styles.statLabel}>Current Streak</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>🏆</Text>
          <Text style={styles.statNumber}>{longestStreak}</Text>
          <Text style={styles.statLabel}>Longest Streak</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>📅</Text>
          <Text style={styles.statNumber}>{totalDaysCompleted}</Text>
          <Text style={styles.statLabel}>Total Days</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>⏱️</Text>
          <Text style={styles.statNumber}>{totalMinutes}</Text>
          <Text style={styles.statLabel}>Minutes Prayed</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Last 5 Weeks</Text>
      <CalendarGrid />

      {currentStreak > 0 && (
        <View style={styles.motivationCard}>
          <Text style={styles.motivationEmoji}>💪</Text>
          <Text style={styles.motivationText}>
            {currentStreak >= 7
              ? "Amazing! You're building a powerful habit!"
              : currentStreak >= 3
              ? "Great progress! Keep it going!"
              : "You're on your way. Stay consistent!"}
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 32,
  },
  statCard: {
    backgroundColor: '#2a2a4e',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    width: (width - 56) / 2,
    marginBottom: 8,
  },
  statIcon: {
    fontSize: 24,
    marginBottom: 8,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  statLabel: {
    fontSize: 12,
    color: '#8b8b9e',
    marginTop: 4,
  },
  calendarContainer: {
    backgroundColor: '#2a2a4e',
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
  },
  dayLabels: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 12,
  },
  dayLabel: {
    color: '#8b8b9e',
    fontSize: 12,
    width: 36,
    textAlign: 'center',
  },
  calendarGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'flex-start',
  },
  calendarDay: {
    width: 36,
    height: 36,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 2,
    marginVertical: 2,
    backgroundColor: '#3a3a5e',
  },
  calendarDayCompleted: {
    backgroundColor: '#6c63ff',
  },
  calendarDayToday: {
    borderWidth: 2,
    borderColor: '#fff',
  },
  calendarDayText: {
    color: '#8b8b9e',
    fontSize: 12,
  },
  calendarDayTextCompleted: {
    color: '#fff',
    fontWeight: '600',
  },
  motivationCard: {
    backgroundColor: '#2a2a4e',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 32,
  },
  motivationEmoji: {
    fontSize: 32,
    marginBottom: 12,
  },
  motivationText: {
    fontSize: 16,
    color: '#fff',
    textAlign: 'center',
    lineHeight: 24,
  },
});
