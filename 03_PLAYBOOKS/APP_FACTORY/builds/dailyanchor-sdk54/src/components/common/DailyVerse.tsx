import { useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { COLORS } from '../../utils/constants';
import { useVerseStore } from '../../store';

export function DailyVerse() {
  const { verse, isLoading, fetchVerse } = useVerseStore();

  useEffect(() => {
    fetchVerse();
  }, [fetchVerse]);

  return (
    <View style={styles.container}>
      {isLoading ? (
        <ActivityIndicator color={COLORS.primary} />
      ) : verse ? (
        <>
          <Text style={styles.reference}>{verse.reference}</Text>
          <Text style={styles.text}>{verse.text}</Text>
        </>
      ) : (
        <Text style={styles.placeholder}>Failed to load verse</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    minHeight: 120,
    justifyContent: 'center',
  },
  reference: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
    marginBottom: 8,
  },
  text: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 24,
  },
  placeholder: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
