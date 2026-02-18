import React from 'react';
import {
  ScrollView,
  TouchableOpacity,
  Text,
  StyleSheet,
  View,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Category, CATEGORIES } from '../types';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';

interface CategoryChipsProps {
  selectedCategory: Category | null;
  onSelectCategory: (category: Category | null) => void;
}

const getCategoryIcon = (key: Category): string => {
  const icons: Record<Category, string> = {
    writing: 'pencil',
    coding: 'code-tags',
    marketing: 'bullhorn',
    analysis: 'chart-bar',
    creative: 'lightbulb',
    business: 'briefcase',
    productivity: 'clock-outline',
    learning: 'school',
    career: 'account-tie',
  };
  return icons[key] || 'tag';
};

export default function CategoryChips({
  selectedCategory,
  onSelectCategory,
}: CategoryChipsProps) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.container}
    >
      <TouchableOpacity
        style={[
          styles.chip,
          !selectedCategory && styles.chipSelected,
        ]}
        onPress={() => onSelectCategory(null)}
      >
        <MaterialCommunityIcons
          name="view-grid"
          size={16}
          color={!selectedCategory ? colors.background : colors.textSecondary}
        />
        <Text
          style={[
            styles.chipText,
            !selectedCategory && styles.chipTextSelected,
          ]}
        >
          All
        </Text>
      </TouchableOpacity>

      {CATEGORIES.map((cat) => {
        const isSelected = selectedCategory === cat.key;
        const categoryColor = colors.categoryColors[cat.key];

        return (
          <TouchableOpacity
            key={cat.key}
            style={[
              styles.chip,
              isSelected && { backgroundColor: categoryColor },
            ]}
            onPress={() => onSelectCategory(cat.key)}
          >
            <MaterialCommunityIcons
              name={getCategoryIcon(cat.key) as any}
              size={16}
              color={isSelected ? colors.background : categoryColor}
            />
            <Text
              style={[
                styles.chipText,
                isSelected
                  ? styles.chipTextSelected
                  : { color: colors.textSecondary },
              ]}
            >
              {cat.label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    gap: spacing.sm,
  },
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    marginRight: spacing.sm,
    gap: spacing.xs,
  },
  chipSelected: {
    backgroundColor: colors.primary,
  },
  chipText: {
    fontSize: fontSize.sm,
    fontWeight: '500',
    color: colors.textSecondary,
  },
  chipTextSelected: {
    color: colors.background,
    fontWeight: '600',
  },
});
