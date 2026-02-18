import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../constants';

interface VerseCardProps {
  text: string;
  reference: string;
  variant?: 'light' | 'dark';
}

export function VerseCard({ text, reference, variant = 'light' }: VerseCardProps) {
  const isDark = variant === 'dark';

  return (
    <View style={[styles.container, isDark && styles.containerDark]}>
      <Text style={[styles.quoteIcon, isDark && styles.textDark]}>"</Text>
      <Text style={[styles.verseText, isDark && styles.textDark]}>{text}</Text>
      <Text style={[styles.reference, isDark && styles.referenceDark]}>
        — {reference}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 24,
    marginHorizontal: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  containerDark: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  quoteIcon: {
    fontSize: 48,
    color: Colors.primary,
    fontFamily: 'Georgia',
    lineHeight: 48,
    marginBottom: -10,
  },
  verseText: {
    fontSize: 20,
    lineHeight: 30,
    color: Colors.text,
    fontFamily: 'Georgia',
    fontStyle: 'italic',
  },
  textDark: {
    color: Colors.white,
  },
  reference: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 16,
    fontWeight: '600',
  },
  referenceDark: {
    color: 'rgba(255, 255, 255, 0.7)',
  },
});
