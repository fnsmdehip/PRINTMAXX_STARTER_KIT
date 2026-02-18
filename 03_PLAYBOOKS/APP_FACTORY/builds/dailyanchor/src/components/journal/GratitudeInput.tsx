import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { COLORS } from '../../utils/constants';

interface GratitudeInputProps {
  items: string[];
  onChange: (items: string[]) => void;
  maxItems?: number;
}

export function GratitudeInput({
  items,
  onChange,
  maxItems = 3,
}: GratitudeInputProps) {
  const [newItem, setNewItem] = useState('');

  const addItem = () => {
    const trimmed = newItem.trim();
    if (trimmed && items.length < maxItems) {
      onChange([...items, trimmed]);
      setNewItem('');
    }
  };

  const removeItem = (index: number) => {
    const updated = items.filter((_, i) => i !== index);
    onChange(updated);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>What are you grateful for?</Text>

      <View style={styles.items}>
        {items.map((item, index) => (
          <View key={index} style={styles.item}>
            <Text style={styles.itemNumber}>{index + 1}.</Text>
            <Text style={styles.itemText}>{item}</Text>
            <TouchableOpacity
              onPress={() => removeItem(index)}
              style={styles.removeButton}>
              <Text style={styles.removeText}>{'\u00D7'}</Text>
            </TouchableOpacity>
          </View>
        ))}
      </View>

      {items.length < maxItems && (
        <View style={styles.inputRow}>
          <TextInput
            style={styles.input}
            placeholder={`Gratitude ${items.length + 1}...`}
            placeholderTextColor={COLORS.textSecondary}
            value={newItem}
            onChangeText={setNewItem}
            onSubmitEditing={addItem}
            returnKeyType="done"
          />
          <TouchableOpacity
            style={[
              styles.addButton,
              !newItem.trim() && styles.addButtonDisabled,
            ]}
            onPress={addItem}
            disabled={!newItem.trim()}>
            <Text style={styles.addText}>+</Text>
          </TouchableOpacity>
        </View>
      )}

      <Text style={styles.hint}>
        {items.length}/{maxItems} gratitudes
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {},
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  items: {
    marginBottom: 12,
  },
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0FDF4',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
  },
  itemNumber: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.completed,
    marginRight: 8,
  },
  itemText: {
    flex: 1,
    fontSize: 14,
    color: COLORS.text,
  },
  removeButton: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: COLORS.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  removeText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    fontWeight: 'bold',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    backgroundColor: '#F8FAFC',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    color: COLORS.text,
    marginRight: 8,
  },
  addButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addButtonDisabled: {
    backgroundColor: COLORS.border,
  },
  addText: {
    fontSize: 24,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  hint: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 8,
    textAlign: 'right',
  },
});
