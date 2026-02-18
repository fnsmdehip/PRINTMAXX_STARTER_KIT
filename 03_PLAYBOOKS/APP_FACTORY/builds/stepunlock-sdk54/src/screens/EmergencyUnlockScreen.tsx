import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TextInput,
  Alert,
} from 'react-native';
import { COLORS } from '../utils/constants';
import { Button } from '../components/Button';
import { useStepStore } from '../stores/stepStore';
import { useUserStore } from '../stores/userStore';
import { unblockApps } from '../services/blockerService';

interface Props {
  navigation: any;
}

const CONFIRMATION_PHRASE = 'I am skipping my walk';

export function EmergencyUnlockScreen({ navigation }: Props) {
  const [inputPhrase, setInputPhrase] = useState('');
  const [isUnlocking, setIsUnlocking] = useState(false);

  const { markTodayCompleted } = useStepStore();
  const { resetStreak } = useUserStore();

  const isPhraseCorrect =
    inputPhrase.toLowerCase().trim() === CONFIRMATION_PHRASE.toLowerCase();

  const handleEmergencyUnlock = async () => {
    if (!isPhraseCorrect) {
      Alert.alert('Incorrect phrase', 'Please type the confirmation phrase exactly.');
      return;
    }

    Alert.alert(
      'Confirm emergency unlock',
      'This will unlock all apps but reset your streak to 0. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Yes, unlock',
          style: 'destructive',
          onPress: performUnlock,
        },
      ]
    );
  };

  const performUnlock = async () => {
    setIsUnlocking(true);

    // Unblock apps
    await unblockApps();

    // Mark today as completed (with emergency flag)
    markTodayCompleted(true);

    // Reset streak
    resetStreak();

    setIsUnlocking(false);

    Alert.alert(
      'Apps unlocked',
      'Your apps are now accessible. Your streak has been reset.',
      [{ text: 'OK', onPress: () => navigation.goBack() }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Warning Icon */}
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>⚠️</Text>
        </View>

        {/* Title */}
        <Text style={styles.title}>Emergency unlock</Text>

        {/* Warning */}
        <View style={styles.warningCard}>
          <Text style={styles.warningTitle}>Before you continue:</Text>
          <Text style={styles.warningText}>
            - Your current streak will reset to 0
          </Text>
          <Text style={styles.warningText}>
            - This bypass will be logged
          </Text>
          <Text style={styles.warningText}>
            - All apps will unlock immediately
          </Text>
        </View>

        {/* Instructions */}
        <Text style={styles.instructions}>
          To confirm, type the phrase below:
        </Text>
        <Text style={styles.phrase}>"{CONFIRMATION_PHRASE}"</Text>

        {/* Input */}
        <TextInput
          style={styles.input}
          placeholder="Type the phrase here"
          placeholderTextColor={COLORS.textSecondary}
          value={inputPhrase}
          onChangeText={setInputPhrase}
          autoCapitalize="none"
          autoCorrect={false}
        />

        {/* Buttons */}
        <View style={styles.buttons}>
          <Button
            title="Cancel"
            onPress={() => navigation.goBack()}
            variant="outline"
            style={styles.cancelButton}
          />
          <Button
            title={isUnlocking ? 'Unlocking...' : 'Unlock apps'}
            onPress={handleEmergencyUnlock}
            disabled={!isPhraseCorrect || isUnlocking}
            style={{
              ...styles.unlockButton,
              ...(!isPhraseCorrect ? styles.unlockButtonDisabled : {}),
            }}
          />
        </View>

        {/* Hint */}
        <Text style={styles.hint}>
          This feature is for genuine emergencies only.
          Consider waiting a bit longer to hit your step goal.
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  iconContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  icon: {
    fontSize: 64,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 24,
  },
  warningCard: {
    backgroundColor: '#FFEBEE',
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  warningTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.error,
    marginBottom: 12,
  },
  warningText: {
    fontSize: 14,
    color: COLORS.error,
    marginBottom: 4,
  },
  instructions: {
    fontSize: 16,
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 8,
  },
  phrase: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 16,
  },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: 24,
    textAlign: 'center',
  },
  buttons: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  cancelButton: {
    flex: 1,
  },
  unlockButton: {
    flex: 1,
    backgroundColor: COLORS.error,
  },
  unlockButtonDisabled: {
    opacity: 0.5,
  },
  hint: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
  },
});
