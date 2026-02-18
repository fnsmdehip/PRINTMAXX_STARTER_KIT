import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../../utils/constants';
import { Card } from '../common';

interface StreakCounterProps {
  currentStreak: number;
  longestStreak: number;
}

export function StreakCounter({ currentStreak, longestStreak }: StreakCounterProps) {
  return (
    <Card>
      <View style={styles.container}>
        <View style={styles.streakBox}>
          <Text style={styles.emoji}>🔥</Text>
          <Text style={styles.label}>Current Streak</Text>
          <Text style={styles.value}>{currentStreak}</Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.streakBox}>
          <Text style={styles.emoji}>🏆</Text>
          <Text style={styles.label}>Best Streak</Text>
          <Text style={styles.value}>{longestStreak}</Text>
        </View>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  streakBox: {
    flex: 1,
    alignItems: 'center',
  },
  emoji: {
    fontSize: 28,
    marginBottom: 8,
  },
  label: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  value: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  divider: {
    width: 1,
    height: 60,
    backgroundColor: COLORS.border,
  },
});
