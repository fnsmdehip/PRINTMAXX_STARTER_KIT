import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { COLORS } from '../../utils/constants';

interface JournalEntryFormProps {
  onSubmit: (data: any) => void;
}

export function JournalEntryForm({ onSubmit }: JournalEntryFormProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Journal Entry</Text>
      <TextInput
        style={styles.input}
        placeholder="Write your thoughts here..."
        multiline
        numberOfLines={6}
        placeholderTextColor={COLORS.textSecondary}
      />
      <TouchableOpacity style={styles.button} onPress={() => onSubmit({})}>
        <Text style={styles.buttonText}>Save Entry</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    padding: 12,
    color: COLORS.text,
    fontSize: 14,
    minHeight: 120,
    textAlignVertical: 'top',
    marginBottom: 12,
  },
  button: {
    backgroundColor: COLORS.primary,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
