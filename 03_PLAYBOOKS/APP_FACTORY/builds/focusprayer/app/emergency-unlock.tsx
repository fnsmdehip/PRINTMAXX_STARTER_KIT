/**
 * Emergency Unlock Screen
 * Friction-heavy bypass for genuine emergencies
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useDevotionStore } from '@/stores/devotionStore';
import { COLORS, EMERGENCY_UNLOCK_PHRASE } from '@/utils/constants';

export default function EmergencyUnlockScreen() {
  const router = useRouter();
  const { emergencyUnlock, streak } = useDevotionStore();

  const [inputText, setInputText] = useState('');
  const [hasConfirmed, setHasConfirmed] = useState(false);

  const isMatch = inputText.toLowerCase().trim() === EMERGENCY_UNLOCK_PHRASE.toLowerCase();

  function handleFirstConfirm() {
    Alert.alert(
      'Are you sure?',
      `This will reset your ${streak.currentStreak}-day streak to 0. This action cannot be undone.`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'I Understand',
          style: 'destructive',
          onPress: () => setHasConfirmed(true),
        },
      ]
    );
  }

  async function handleEmergencyUnlock() {
    if (!isMatch) return;

    await emergencyUnlock();

    Alert.alert(
      'Apps Unlocked',
      'Your apps have been unlocked. Your streak has been reset.',
      [
        {
          text: 'OK',
          onPress: () => router.replace('/(tabs)'),
        },
      ]
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Text style={styles.backButtonText}>&#8592; Back</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.content}>
        {/* Warning Icon */}
        <View style={styles.warningIcon}>
          <Text style={styles.warningIconText}>&#9888;</Text>
        </View>

        {/* Title */}
        <Text style={styles.title}>Emergency Unlock</Text>

        {/* Warning Message */}
        <View style={styles.warningBox}>
          <Text style={styles.warningTitle}>Before you continue:</Text>
          <Text style={styles.warningText}>
            This feature is for genuine emergencies only. Using it will:
          </Text>
          <View style={styles.consequencesList}>
            <Text style={styles.consequenceItem}>
              &#8226; Reset your {streak.currentStreak}-day streak to 0
            </Text>
            <Text style={styles.consequenceItem}>
              &#8226; Be logged in your history
            </Text>
            <Text style={styles.consequenceItem}>
              &#8226; Unlock all blocked apps for the day
            </Text>
          </View>
        </View>

        {!hasConfirmed ? (
          // First confirmation
          <TouchableOpacity
            style={styles.continueButton}
            onPress={handleFirstConfirm}
            activeOpacity={0.8}
          >
            <Text style={styles.continueButtonText}>I Have an Emergency</Text>
          </TouchableOpacity>
        ) : (
          // Type to confirm
          <View style={styles.confirmSection}>
            <Text style={styles.confirmLabel}>
              Type the following phrase to confirm:
            </Text>
            <Text style={styles.confirmPhrase}>"{EMERGENCY_UNLOCK_PHRASE}"</Text>

            <TextInput
              style={styles.input}
              value={inputText}
              onChangeText={setInputText}
              placeholder="Type here..."
              placeholderTextColor={COLORS.disabled}
              autoCapitalize="none"
              autoCorrect={false}
            />

            <TouchableOpacity
              style={[
                styles.unlockButton,
                !isMatch && styles.unlockButtonDisabled,
              ]}
              onPress={handleEmergencyUnlock}
              disabled={!isMatch}
              activeOpacity={0.8}
            >
              <Text
                style={[
                  styles.unlockButtonText,
                  !isMatch && styles.unlockButtonTextDisabled,
                ]}
              >
                Unlock Apps
              </Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Alternative */}
        <View style={styles.alternativeSection}>
          <Text style={styles.alternativeTitle}>Not an emergency?</Text>
          <Text style={styles.alternativeText}>
            Your devotion only takes {'\n'}a few minutes. Consider completing it instead.
          </Text>
          <TouchableOpacity
            style={styles.returnButton}
            onPress={() => router.back()}
          >
            <Text style={styles.returnButtonText}>Return to Devotion</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    padding: 20,
    paddingTop: 10,
  },
  backButton: {
    alignSelf: 'flex-start',
  },
  backButtonText: {
    color: COLORS.primary,
    fontSize: 16,
  },
  content: {
    flex: 1,
    padding: 20,
    alignItems: 'center',
  },
  warningIcon: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.warning + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  warningIconText: {
    fontSize: 40,
    color: COLORS.warning,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 20,
  },
  warningBox: {
    backgroundColor: COLORS.error + '10',
    borderRadius: 12,
    padding: 20,
    width: '100%',
    marginBottom: 24,
  },
  warningTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.error,
    marginBottom: 8,
  },
  warningText: {
    fontSize: 15,
    color: COLORS.text,
    marginBottom: 12,
  },
  consequencesList: {
    gap: 6,
  },
  consequenceItem: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  continueButton: {
    backgroundColor: COLORS.warning,
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    marginBottom: 32,
  },
  continueButtonText: {
    color: COLORS.surface,
    fontSize: 16,
    fontWeight: '700',
  },
  confirmSection: {
    width: '100%',
    marginBottom: 32,
  },
  confirmLabel: {
    fontSize: 15,
    color: COLORS.text,
    marginBottom: 8,
  },
  confirmPhrase: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.error,
    marginBottom: 16,
    fontStyle: 'italic',
  },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: COLORS.text,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.disabled,
  },
  unlockButton: {
    backgroundColor: COLORS.error,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
  },
  unlockButtonDisabled: {
    backgroundColor: COLORS.disabled,
  },
  unlockButtonText: {
    color: COLORS.surface,
    fontSize: 16,
    fontWeight: '700',
  },
  unlockButtonTextDisabled: {
    color: COLORS.textSecondary,
  },
  alternativeSection: {
    alignItems: 'center',
    marginTop: 'auto',
    paddingBottom: 20,
  },
  alternativeTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  alternativeText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 16,
  },
  returnButton: {
    borderWidth: 2,
    borderColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  returnButtonText: {
    color: COLORS.primary,
    fontSize: 16,
    fontWeight: '600',
  },
});
