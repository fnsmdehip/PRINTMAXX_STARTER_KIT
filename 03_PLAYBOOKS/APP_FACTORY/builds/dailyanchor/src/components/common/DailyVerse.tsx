import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { Card } from './Card';
import { COLORS } from '../../utils/constants';
import { useVerseStore } from '../../store';

interface DailyVerseProps {
  compact?: boolean;
}

export function DailyVerse({ compact = false }: DailyVerseProps) {
  const { verse, isLoading, fetchVerse } = useVerseStore();

  useEffect(() => {
    fetchVerse();
  }, [fetchVerse]);

  if (isLoading) {
    return (
      <Card style={styles.container}>
        <ActivityIndicator color={COLORS.primary} />
      </Card>
    );
  }

  if (!verse) {
    return null;
  }

  return (
    <Card style={[styles.container, compact && styles.compact]}>
      <View style={styles.header}>
        <Text style={styles.icon}>{'\u{1F4D6}'}</Text>
        <Text style={styles.label}>Today's verse</Text>
      </View>

      <Text style={[styles.text, compact && styles.compactText]}>
        "{verse.text}"
      </Text>

      <View style={styles.footer}>
        <Text style={styles.reference}>{verse.reference}</Text>
        <Text style={styles.translation}>{verse.translation}</Text>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#EEF2FF',
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary,
  },
  compact: {
    padding: 12,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  icon: {
    fontSize: 20,
    marginRight: 8,
  },
  label: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.primary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  text: {
    fontSize: 16,
    lineHeight: 24,
    color: COLORS.text,
    fontStyle: 'italic',
    marginBottom: 12,
  },
  compactText: {
    fontSize: 14,
    lineHeight: 20,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  reference: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  translation: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
