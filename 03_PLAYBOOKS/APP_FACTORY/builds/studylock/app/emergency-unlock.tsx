import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useStudyStore } from '../src/stores/studyStore';
import { COLORS } from '../src/utils/constants';
import Button from '../src/components/Button';

export default function EmergencyUnlockScreen() {
  const router = useRouter();
  const { endSession, resetTimer } = useStudyStore();

  const handleEmergencyUnlock = () => {
    Alert.alert(
      'Emergency Unlock',
      'This will end your current session WITHOUT saving your progress. Your streak may be affected. Are you sure?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Unlock Now',
          style: 'destructive',
          onPress: () => {
            // End session without completing
            endSession(false);
            resetTimer();
            router.replace('/');
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.closeButton}
          onPress={() => router.back()}
        >
          <Ionicons name="close" size={24} color={COLORS.text} />
        </TouchableOpacity>
      </View>

      <View style={styles.content}>
        <View style={styles.iconContainer}>
          <Ionicons name="warning" size={64} color={COLORS.error} />
        </View>

        <Text style={styles.title}>Emergency Unlock</Text>
        <Text style={styles.subtitle}>
          Use this only if you truly need to access your phone urgently.
        </Text>

        <View style={styles.warningBox}>
          <Ionicons name="alert-circle" size={24} color={COLORS.warning} />
          <View style={styles.warningContent}>
            <Text style={styles.warningTitle}>What you will lose:</Text>
            <Text style={styles.warningItem}>- Current session progress</Text>
            <Text style={styles.warningItem}>- Study time will not be recorded</Text>
            <Text style={styles.warningItem}>- Streak may be affected</Text>
          </View>
        </View>

        <View style={styles.buttons}>
          <Button
            title="Go Back to Session"
            onPress={() => router.back()}
            variant="outline"
            size="large"
            fullWidth
          />
          <Button
            title="Emergency Unlock"
            onPress={handleEmergencyUnlock}
            variant="danger"
            size="large"
            fullWidth
          />
        </View>

        <Text style={styles.helpText}>
          If you're experiencing a real emergency, your safety is always more important
          than your study streak.
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
  header: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  iconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: COLORS.error + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 32,
  },
  warningBox: {
    flexDirection: 'row',
    backgroundColor: COLORS.warning + '15',
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.warning + '30',
    marginBottom: 32,
    width: '100%',
  },
  warningContent: {
    flex: 1,
    marginLeft: 12,
  },
  warningTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  warningItem: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  buttons: {
    width: '100%',
    gap: 12,
    marginBottom: 24,
  },
  helpText: {
    fontSize: 12,
    color: COLORS.textMuted,
    textAlign: 'center',
    lineHeight: 18,
  },
});
