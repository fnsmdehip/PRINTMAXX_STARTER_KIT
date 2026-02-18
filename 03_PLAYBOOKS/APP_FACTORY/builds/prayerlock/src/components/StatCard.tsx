import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../constants';

interface StatCardProps {
  value: string | number;
  label: string;
  icon?: string;
  highlight?: boolean;
}

export function StatCard({ value, label, icon, highlight = false }: StatCardProps) {
  return (
    <View style={[styles.container, highlight && styles.highlightContainer]}>
      {icon && <Text style={styles.icon}>{icon}</Text>}
      <Text style={[styles.value, highlight && styles.highlightValue]}>
        {value}
      </Text>
      <Text style={[styles.label, highlight && styles.highlightLabel]}>
        {label}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    minWidth: 100,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  highlightContainer: {
    backgroundColor: Colors.primary,
  },
  icon: {
    fontSize: 24,
    marginBottom: 8,
  },
  value: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.text,
  },
  highlightValue: {
    color: Colors.white,
  },
  label: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 4,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  highlightLabel: {
    color: 'rgba(255, 255, 255, 0.9)',
  },
});
