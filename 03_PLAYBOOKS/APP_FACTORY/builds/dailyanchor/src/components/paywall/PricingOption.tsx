import React from 'react';
import { TouchableOpacity, View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../../utils/constants';

interface PricingOptionProps {
  title: string;
  price: string;
  period: string;
  savings?: string;
  isPopular?: boolean;
  isSelected: boolean;
  onSelect: () => void;
}

export function PricingOption({
  title,
  price,
  period,
  savings,
  isPopular = false,
  isSelected,
  onSelect,
}: PricingOptionProps) {
  return (
    <TouchableOpacity
      style={[
        styles.container,
        isSelected && styles.selected,
        isPopular && styles.popular,
      ]}
      onPress={onSelect}
      activeOpacity={0.7}>
      {isPopular && (
        <View style={styles.popularBadge}>
          <Text style={styles.popularText}>Best value</Text>
        </View>
      )}

      <View style={styles.radioOuter}>
        {isSelected && <View style={styles.radioInner} />}
      </View>

      <View style={styles.content}>
        <Text style={styles.title}>{title}</Text>
        <View style={styles.priceRow}>
          <Text style={styles.price}>{price}</Text>
          <Text style={styles.period}>/{period}</Text>
        </View>
        {savings && <Text style={styles.savings}>{savings}</Text>}
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: COLORS.card,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.border,
    marginBottom: 12,
    position: 'relative',
  },
  selected: {
    borderColor: COLORS.primary,
    backgroundColor: '#EEF2FF',
  },
  popular: {
    borderColor: COLORS.primary,
  },
  popularBadge: {
    position: 'absolute',
    top: -10,
    right: 12,
    backgroundColor: COLORS.primary,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
  },
  popularText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#FFFFFF',
    textTransform: 'uppercase',
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.primary,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  price: {
    fontSize: 24,
    fontWeight: '800',
    color: COLORS.text,
  },
  period: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginLeft: 2,
  },
  savings: {
    fontSize: 12,
    color: COLORS.completed,
    fontWeight: '600',
    marginTop: 4,
  },
});
