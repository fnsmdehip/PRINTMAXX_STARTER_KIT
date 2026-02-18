import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../../utils/constants';

interface PremiumFeatureCardProps {
  title: string;
  description: string;
}

export function PremiumFeatureCard({ title, description }: PremiumFeatureCardProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.icon}>✨</Text>
      <View>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.description}>{description}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'flex-start',
  },
  icon: {
    fontSize: 20,
    marginRight: 12,
  },
  title: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  description: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
