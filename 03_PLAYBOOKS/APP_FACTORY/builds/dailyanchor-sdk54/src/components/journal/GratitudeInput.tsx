import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { COLORS } from '../../utils/constants';

interface GratitudeInputProps {
  onAdd: (text: string) => void;
}

export function GratitudeInput({ onAdd }: GratitudeInputProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>What are you grateful for?</Text>
      <TextInput
        style={styles.input}
        placeholder="Add a gratitude..."
        placeholderTextColor={COLORS.textSecondary}
        onSubmitEditing={(e) => {
          if (e.nativeEvent.text) {
            onAdd(e.nativeEvent.text);
          }
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    padding: 12,
    color: COLORS.text,
    fontSize: 14,
  },
});
