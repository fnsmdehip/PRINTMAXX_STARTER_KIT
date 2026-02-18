import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from 'react-native';
import { router } from 'expo-router';
import { useDevotionStore } from '../../src/stores/devotionStore';
import { useUserStore } from '../../src/stores/userStore';

const { width } = Dimensions.get('window');

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
}

export default function Home() {
  const currentStreak = useDevotionStore((state) => state.currentStreak);
  const todayCompleted = useDevotionStore((state) => state.isTodayCompleted());
  const settings = useUserStore((state) => state.settings);
  const greeting = getGreeting();

  const handleStartDevotion = () => {
    if (settings.requireTimer) {
      router.push('/timer');
    } else if (settings.requireScripture) {
      router.push('/scripture');
    } else {
      router.push('/timer');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>{greeting}</Text>
        <Text style={styles.subtitle}>
          {todayCompleted
            ? "You've completed today's devotional"
            : "Start your devotional to unlock your apps"}
        </Text>
      </View>

      <View style={styles.streakCard}>
        <Text style={styles.streakEmoji}>🔥</Text>
        <Text style={styles.streakNumber}>{currentStreak}</Text>
        <Text style={styles.streakLabel}>Day Streak</Text>
      </View>

      {!todayCompleted ? (
        <TouchableOpacity style={styles.startButton} onPress={handleStartDevotion}>
          <Text style={styles.startButtonText}>Begin Devotional</Text>
          <Text style={styles.startButtonSubtext}>
            {settings.devotionDurationMinutes} min prayer
            {settings.requireScripture && ' + scripture'}
          </Text>
        </TouchableOpacity>
      ) : (
        <View style={styles.completedCard}>
          <Text style={styles.completedEmoji}>✓</Text>
          <Text style={styles.completedText}>Today Complete</Text>
          <Text style={styles.completedSubtext}>
            Apps unlocked until {settings.dailyResetTime}
          </Text>
        </View>
      )}

      <View style={styles.quickActions}>
        <TouchableOpacity
          style={styles.quickAction}
          onPress={() => router.push('/scripture')}
        >
          <Text style={styles.quickActionIcon}>📖</Text>
          <Text style={styles.quickActionText}>Read Scripture</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.quickAction}
          onPress={() => router.push('/timer')}
        >
          <Text style={styles.quickActionIcon}>⏱️</Text>
          <Text style={styles.quickActionText}>Prayer Timer</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 20,
  },
  header: {
    marginBottom: 32,
  },
  greeting: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#8b8b9e',
  },
  streakCard: {
    backgroundColor: '#2a2a4e',
    borderRadius: 20,
    padding: 32,
    alignItems: 'center',
    marginBottom: 24,
  },
  streakEmoji: {
    fontSize: 48,
    marginBottom: 8,
  },
  streakNumber: {
    fontSize: 64,
    fontWeight: 'bold',
    color: '#fff',
  },
  streakLabel: {
    fontSize: 18,
    color: '#8b8b9e',
    marginTop: 4,
  },
  startButton: {
    backgroundColor: '#6c63ff',
    borderRadius: 16,
    paddingVertical: 20,
    paddingHorizontal: 24,
    alignItems: 'center',
    marginBottom: 24,
  },
  startButtonText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  startButtonSubtext: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
  },
  completedCard: {
    backgroundColor: '#1e3a2f',
    borderRadius: 16,
    paddingVertical: 24,
    paddingHorizontal: 24,
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#2d5a47',
  },
  completedEmoji: {
    fontSize: 32,
    color: '#4caf50',
    marginBottom: 8,
  },
  completedText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#4caf50',
    marginBottom: 4,
  },
  completedSubtext: {
    fontSize: 14,
    color: '#7fc494',
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  quickAction: {
    backgroundColor: '#2a2a4e',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    width: (width - 56) / 2,
  },
  quickActionIcon: {
    fontSize: 28,
    marginBottom: 8,
  },
  quickActionText: {
    fontSize: 14,
    color: '#fff',
    fontWeight: '500',
  },
});
