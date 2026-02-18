import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  ScrollView,
  Switch,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import { requestPermissions, scheduleDailyReminder, notificationPresets } from '@/lib/notifications';

export default function NotificationsScreen() {
  const router = useRouter();
  const { setProfile } = useUserStore();
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [selectedTime, setSelectedTime] = useState(notificationPresets[1]); // 7:00 AM default
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);

    try {
      if (notificationsEnabled) {
        const granted = await requestPermissions();
        if (granted) {
          await scheduleDailyReminder(selectedTime.hour, selectedTime.minute);
          setProfile({
            notificationsEnabled: true,
            notificationTime: { hour: selectedTime.hour, minute: selectedTime.minute },
          });
        } else {
          Alert.alert(
            'Notifications Disabled',
            'You can enable notifications later in Settings.',
            [{ text: 'OK' }]
          );
          setProfile({ notificationsEnabled: false });
        }
      } else {
        setProfile({ notificationsEnabled: false });
      }

      router.push('/(onboarding)/paywall');
    } catch (error) {
      console.error('Notification setup error:', error);
      router.push('/(onboarding)/paywall');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = () => {
    setProfile({ notificationsEnabled: false });
    router.push('/(onboarding)/paywall');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.step}>Step 2 of 3</Text>
          <Text style={styles.title}>Daily reminders</Text>
          <Text style={styles.subtitle}>
            A gentle nudge to keep your devotional practice consistent
          </Text>
        </View>

        {/* Main illustration */}
        <View style={styles.illustration}>
          <View style={styles.bellContainer}>
            <Ionicons name="notifications" size={64} color={colors.primary} />
          </View>
        </View>

        {/* Toggle */}
        <View style={styles.toggleCard}>
          <View style={styles.toggleInfo}>
            <Ionicons name="sunny" size={24} color={colors.secondary} />
            <Text style={styles.toggleText}>Enable morning reminders</Text>
          </View>
          <Switch
            value={notificationsEnabled}
            onValueChange={setNotificationsEnabled}
            trackColor={{ false: colors.border, true: colors.primary + '60' }}
            thumbColor={notificationsEnabled ? colors.primary : colors.textMuted}
          />
        </View>

        {/* Time selection */}
        {notificationsEnabled && (
          <View style={styles.timeSection}>
            <Text style={styles.timeSectionTitle}>Choose your reminder time</Text>
            <View style={styles.timeOptions}>
              {notificationPresets.map((preset) => (
                <Pressable
                  key={preset.label}
                  style={[
                    styles.timeOption,
                    selectedTime.label === preset.label && styles.timeOptionSelected,
                  ]}
                  onPress={() => setSelectedTime(preset)}
                >
                  <Text
                    style={[
                      styles.timeOptionText,
                      selectedTime.label === preset.label && styles.timeOptionTextSelected,
                    ]}
                  >
                    {preset.label}
                  </Text>
                </Pressable>
              ))}
            </View>
          </View>
        )}

        {/* Info note */}
        <View style={styles.infoNote}>
          <Ionicons name="information-circle" size={20} color={colors.textMuted} />
          <Text style={styles.infoNoteText}>
            You can change your reminder settings anytime in your profile
          </Text>
        </View>
      </ScrollView>

      {/* CTA Buttons */}
      <View style={styles.ctaContainer}>
        <Pressable
          style={({ pressed }) => [
            styles.ctaButton,
            pressed && styles.ctaButtonPressed,
            isLoading && styles.ctaButtonDisabled,
          ]}
          onPress={handleContinue}
          disabled={isLoading}
        >
          <Text style={styles.ctaText}>
            {isLoading ? 'Setting up...' : 'Continue'}
          </Text>
          <Ionicons name="arrow-forward" size={20} color={colors.surface} />
        </Pressable>
        <Pressable style={styles.skipButton} onPress={handleSkip}>
          <Text style={styles.skipText}>Maybe later</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: 180,
  },
  header: {
    marginBottom: spacing.xl,
  },
  step: {
    ...typography.caption,
    color: colors.primary,
    marginBottom: spacing.sm,
    fontWeight: '600',
  },
  title: {
    ...typography.h1,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
  },
  illustration: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  bellContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
  },
  toggleCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.lg,
    ...shadows.sm,
  },
  toggleInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  toggleText: {
    ...typography.bodyBold,
    color: colors.text,
  },
  timeSection: {
    marginBottom: spacing.lg,
  },
  timeSectionTitle: {
    ...typography.bodyBold,
    color: colors.text,
    marginBottom: spacing.md,
  },
  timeOptions: {
    gap: spacing.sm,
  },
  timeOption: {
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    borderWidth: 2,
    borderColor: colors.border,
  },
  timeOptionSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  timeOptionText: {
    ...typography.body,
    color: colors.text,
    textAlign: 'center',
  },
  timeOptionTextSelected: {
    color: colors.primary,
    fontWeight: '600',
  },
  infoNote: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    padding: spacing.md,
    backgroundColor: colors.border + '50',
    borderRadius: borderRadius.md,
  },
  infoNoteText: {
    ...typography.caption,
    color: colors.textMuted,
    flex: 1,
  },
  ctaContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  ctaButtonDisabled: {
    opacity: 0.7,
  },
  ctaButtonPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
  ctaText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
  skipButton: {
    alignItems: 'center',
    paddingVertical: spacing.md,
  },
  skipText: {
    ...typography.body,
    color: colors.textMuted,
  },
});
