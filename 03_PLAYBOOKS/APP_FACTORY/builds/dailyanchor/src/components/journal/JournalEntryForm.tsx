import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { JournalEntry } from '../../types';
import { GratitudeInput } from './GratitudeInput';
import { Button, Card } from '../common';
import { COLORS } from '../../utils/constants';
import { useJournalStore } from '../../store';
import { getToday, formatDisplayDate } from '../../utils/dateUtils';

interface JournalEntryFormProps {
  date?: string;
  onSave?: () => void;
}

export function JournalEntryForm({
  date = getToday(),
  onSave,
}: JournalEntryFormProps) {
  const { getEntryForDate, addEntry } = useJournalStore();

  const [gratitude, setGratitude] = useState<string[]>([]);
  const [prayerRequest, setPrayerRequest] = useState('');
  const [reflection, setReflection] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  // Load existing entry
  useEffect(() => {
    const existing = getEntryForDate(date);
    if (existing) {
      setGratitude(existing.gratitude);
      setPrayerRequest(existing.prayerRequest);
      setReflection(existing.reflection);
    } else {
      setGratitude([]);
      setPrayerRequest('');
      setReflection('');
    }
  }, [date, getEntryForDate]);

  const handleSave = async () => {
    setIsSaving(true);

    addEntry({
      date,
      gratitude,
      prayerRequest,
      reflection,
    });

    setIsSaving(false);
    onSave?.();
  };

  const hasContent =
    gratitude.length > 0 || prayerRequest.trim() || reflection.trim();

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled">
        <Text style={styles.dateLabel}>{formatDisplayDate(date)}</Text>

        <Card style={styles.section}>
          <GratitudeInput items={gratitude} onChange={setGratitude} />
        </Card>

        <Card style={styles.section}>
          <Text style={styles.label}>Prayer request</Text>
          <Text style={styles.hint}>
            What do you want to bring before God today?
          </Text>
          <TextInput
            style={styles.textArea}
            placeholder="Write your prayer..."
            placeholderTextColor={COLORS.textSecondary}
            value={prayerRequest}
            onChangeText={setPrayerRequest}
            multiline
            numberOfLines={4}
            textAlignVertical="top"
          />
        </Card>

        <Card style={styles.section}>
          <Text style={styles.label}>Reflection</Text>
          <Text style={styles.hint}>
            What stood out from today's reading or prayer?
          </Text>
          <TextInput
            style={styles.textArea}
            placeholder="Write your thoughts..."
            placeholderTextColor={COLORS.textSecondary}
            value={reflection}
            onChangeText={setReflection}
            multiline
            numberOfLines={6}
            textAlignVertical="top"
          />
        </Card>

        <View style={styles.footer}>
          <Button
            title={isSaving ? 'Saving...' : 'Save entry'}
            onPress={handleSave}
            disabled={!hasContent}
            loading={isSaving}
            size="large"
          />
          <Text style={styles.privacyNote}>
            {'\u{1F512}'} Your journal is private and stored locally
          </Text>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  dateLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 16,
  },
  section: {
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  hint: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  textArea: {
    backgroundColor: '#F8FAFC',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    color: COLORS.text,
    minHeight: 100,
  },
  footer: {
    marginTop: 8,
    alignItems: 'center',
  },
  privacyNote: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 12,
    textAlign: 'center',
  },
});
