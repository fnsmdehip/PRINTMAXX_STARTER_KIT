import { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
} from 'react-native';
import { JournalEntryForm } from '../../src/components/journal';
import { COLORS } from '../../src/utils/constants';
import { useJournalStore } from '../../src/store';
import { getToday } from '../../src/utils/dateUtils';

export default function JournalScreen() {
  const { loadFromStorage } = useJournalStore();
  const [savedMessage, setSavedMessage] = useState(false);

  useEffect(() => {
    loadFromStorage();
  }, [loadFromStorage]);

  const handleSave = () => {
    setSavedMessage(true);
    setTimeout(() => setSavedMessage(false), 2000);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Journal</Text>
        {savedMessage && (
          <View style={styles.savedBadge}>
            <Text style={styles.savedText}>{'\u2713'} Saved</Text>
          </View>
        )}
      </View>

      <JournalEntryForm date={getToday()} onSave={handleSave} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
  },
  savedBadge: {
    backgroundColor: '#F0FDF4',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  savedText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.completed,
  },
});
