import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { useDevotionStore } from '../src/stores/devotionStore';

const UNLOCK_PHRASE = 'I am breaking my commitment';

export default function EmergencyUnlock() {
  const [inputText, setInputText] = useState('');
  const emergencyUnlock = useDevotionStore((state) => state.emergencyUnlock);

  const isMatch = inputText.toLowerCase().trim() === UNLOCK_PHRASE.toLowerCase();

  const handleUnlock = () => {
    if (!isMatch) return;

    Alert.alert(
      'Confirm Emergency Unlock',
      'This will reset your streak and log the bypass. Are you sure?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Yes, Unlock',
          style: 'destructive',
          onPress: async () => {
            await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
            emergencyUnlock();
            router.replace('/(tabs)');
          },
        },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.warningIcon}>⚠️</Text>
        <Text style={styles.title}>Emergency Unlock</Text>
        <Text style={styles.subtitle}>
          This should only be used in genuine emergencies.
        </Text>
      </View>

      <View style={styles.consequences}>
        <Text style={styles.consequencesTitle}>Consequences:</Text>
        <Text style={styles.consequenceItem}>
          • Your current streak will be reset to 0
        </Text>
        <Text style={styles.consequenceItem}>
          • This bypass will be logged in your history
        </Text>
        <Text style={styles.consequenceItem}>
          • You'll need to start building your habit again
        </Text>
      </View>

      <View style={styles.inputSection}>
        <Text style={styles.inputLabel}>
          To unlock, type the following:
        </Text>
        <View style={styles.phraseContainer}>
          <Text style={styles.phrase}>{UNLOCK_PHRASE}</Text>
        </View>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type the phrase above..."
          placeholderTextColor="#5a5a7e"
          autoCapitalize="none"
          autoCorrect={false}
        />
      </View>

      <TouchableOpacity
        style={[styles.unlockButton, !isMatch && styles.unlockButtonDisabled]}
        onPress={handleUnlock}
        disabled={!isMatch}
      >
        <Text style={styles.unlockButtonText}>Emergency Unlock</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.cancelButton}
        onPress={() => router.back()}
      >
        <Text style={styles.cancelButtonText}>Cancel</Text>
      </TouchableOpacity>

      <Text style={styles.encouragement}>
        Consider if this is truly an emergency. Your commitment to prayer is
        worth protecting.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  warningIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ff6b6b',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#8b8b9e',
    textAlign: 'center',
  },
  consequences: {
    backgroundColor: '#3a2a2e',
    borderRadius: 12,
    padding: 20,
    marginBottom: 32,
    borderWidth: 1,
    borderColor: '#5a3a3e',
  },
  consequencesTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ff6b6b',
    marginBottom: 12,
  },
  consequenceItem: {
    fontSize: 14,
    color: '#b08b8e',
    marginBottom: 8,
    lineHeight: 20,
  },
  inputSection: {
    marginBottom: 24,
  },
  inputLabel: {
    fontSize: 14,
    color: '#8b8b9e',
    marginBottom: 12,
  },
  phraseContainer: {
    backgroundColor: '#2a2a4e',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  phrase: {
    fontSize: 14,
    color: '#fff',
    fontStyle: 'italic',
    textAlign: 'center',
  },
  input: {
    backgroundColor: '#2a2a4e',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: '#fff',
    borderWidth: 1,
    borderColor: '#3a3a5e',
  },
  unlockButton: {
    backgroundColor: '#ff4444',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
  unlockButtonDisabled: {
    backgroundColor: '#5a3a3e',
  },
  unlockButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  cancelButton: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 24,
  },
  cancelButtonText: {
    color: '#8b8b9e',
    fontSize: 16,
  },
  encouragement: {
    color: '#5a5a7e',
    fontSize: 13,
    textAlign: 'center',
    lineHeight: 20,
  },
});
