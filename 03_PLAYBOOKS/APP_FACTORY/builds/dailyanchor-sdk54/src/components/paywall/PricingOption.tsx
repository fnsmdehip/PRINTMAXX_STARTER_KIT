import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { COLORS } from '../../utils/constants';

interface PricingOptionProps {
  title: string;
  price: string;
  period: string;
  onSelect: () => void;
  selected?: boolean;
}

export function PricingOption({
  title,
  price,
  period,
  onSelect,
  selected,
}: PricingOptionProps) {
  return (
    <TouchableOpacity
      style={[styles.container, selected && styles.selected]}
      onPress={onSelect}
    >
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.price}>{price}</Text>
      <Text style={styles.period}>per {period}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'center',
  },
  selected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '10',
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  price: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  period: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
});
