import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../../utils/constants';

interface StreakCalendarProps {
  completionDates: string[];
}

export function StreakCalendar({ completionDates }: StreakCalendarProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Completion History</Text>
      <Text style={styles.placeholder}>Completed on {completionDates.length} days</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 12,
  },
  placeholder: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
});
