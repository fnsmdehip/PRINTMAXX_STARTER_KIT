import { View, Text, StyleSheet, ScrollView, Pressable, Switch, Alert } from 'react-native';
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
import Luna from '@/components/luna/Luna';
import { MoreApps } from '@/components/MoreApps';

export default function SettingsScreen() {
  const router = useRouter();
  const {
    profile,
    setProfile,
    lunaEnabled,
    toggleLuna,
    isSubscribed,
    totalWorkouts,
    joinedDate,
  } = useUserStore();

  const handleUnitToggle = () => {
    setProfile({ unit: profile.unit === 'lb' ? 'kg' : 'lb' });
  };

  const handleRestorePurchases = () => {
    // RevenueCat restore purchases would go here
    Alert.alert(
      'Restore Purchases',
      'This will restore any previous purchases. Continue?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Restore',
          onPress: () => {
            // Call RevenueCat restorePurchases()
            Alert.alert('Done', 'Purchases restored successfully');
          },
        },
      ]
    );
  };

  const memberSince = new Date(joinedDate).toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
  });

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Profile</Text>
          <View style={styles.profileCard}>
            <View style={styles.profileAvatar}>
              <Ionicons name="person" size={32} color={colors.primary} />
            </View>
            <View style={styles.profileInfo}>
              <Text style={styles.profileName}>
                {profile.name || 'FemFit User'}
              </Text>
              <Text style={styles.profileStats}>
                Member since {memberSince} - {totalWorkouts} workouts
              </Text>
            </View>
          </View>
        </View>

        {/* Luna Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Luna</Text>
          <View style={styles.lunaCard}>
            <View style={styles.lunaPreview}>
              <Luna state={lunaEnabled ? 'idle' : 'sleeping'} size={60} />
            </View>
            <View style={styles.lunaInfo}>
              <Text style={styles.settingLabel}>Show Luna</Text>
              <Text style={styles.settingDescription}>
                {lunaEnabled
                  ? "Luna's here to cheer you on!"
                  : "Luna's taking a nap. She'll wait for you."}
              </Text>
            </View>
            <Switch
              value={lunaEnabled}
              onValueChange={toggleLuna}
              trackColor={{ false: colors.border, true: colors.primary + '50' }}
              thumbColor={lunaEnabled ? colors.primary : colors.textMuted}
            />
          </View>
        </View>

        {/* Preferences Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Preferences</Text>

          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Weight Unit</Text>
              <Text style={styles.settingDescription}>
                Currently using {profile.unit === 'lb' ? 'pounds (lb)' : 'kilograms (kg)'}
              </Text>
            </View>
            <Pressable style={styles.unitToggle} onPress={handleUnitToggle}>
              <Text
                style={[
                  styles.unitOption,
                  profile.unit === 'lb' && styles.unitOptionActive,
                ]}
              >
                lb
              </Text>
              <Text
                style={[
                  styles.unitOption,
                  profile.unit === 'kg' && styles.unitOptionActive,
                ]}
              >
                kg
              </Text>
            </Pressable>
          </View>

          <Pressable
            style={styles.settingRow}
            onPress={() => {
              // Would open weekly goal picker
              Alert.alert('Weekly Goal', 'Set your target workouts per week');
            }}
          >
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Weekly Goal</Text>
              <Text style={styles.settingDescription}>
                {profile.weeklyGoal} workouts per week
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </Pressable>
        </View>

        {/* Subscription Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>

          <View style={styles.subscriptionCard}>
            <View style={styles.subscriptionStatus}>
              <Ionicons
                name={isSubscribed ? 'checkmark-circle' : 'close-circle'}
                size={24}
                color={isSubscribed ? colors.success : colors.textMuted}
              />
              <Text style={styles.subscriptionText}>
                {isSubscribed ? 'FemFit Premium' : 'Free Trial'}
              </Text>
            </View>
            {!isSubscribed && (
              <Pressable
                style={styles.upgradeButton}
                onPress={() => router.push('/paywall')}
              >
                <Text style={styles.upgradeButtonText}>Upgrade</Text>
              </Pressable>
            )}
          </View>

          <Pressable style={styles.settingRow} onPress={handleRestorePurchases}>
            <Text style={styles.settingLabel}>Restore Purchases</Text>
            <Ionicons name="refresh" size={20} color={colors.textMuted} />
          </Pressable>
        </View>

        {/* Support Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>

          <Pressable
            style={styles.settingRow}
            onPress={() => {
              // Would open email or support page
            }}
          >
            <View style={styles.settingInfo}>
              <Ionicons name="mail" size={20} color={colors.textLight} />
              <Text style={[styles.settingLabel, { marginLeft: spacing.sm }]}>
                Contact Us
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </Pressable>

          <Pressable
            style={styles.settingRow}
            onPress={() => router.push('/privacy')}
          >
            <View style={styles.settingInfo}>
              <Ionicons name="shield-checkmark" size={20} color={colors.textLight} />
              <Text style={[styles.settingLabel, { marginLeft: spacing.sm }]}>
                Privacy Policy
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </Pressable>

          <Pressable
            style={styles.settingRow}
            onPress={() => router.push('/terms')}
          >
            <View style={styles.settingInfo}>
              <Ionicons name="document-text" size={20} color={colors.textLight} />
              <Text style={[styles.settingLabel, { marginLeft: spacing.sm }]}>
                Terms of Service
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </Pressable>
        </View>

        {/* More Apps */}
        <MoreApps />

        {/* App Version */}
        <Text style={styles.version}>FemFit v1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.caption,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: spacing.md,
  },
  profileCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  profileAvatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary + '20',
    alignItems: 'center',
    justifyContent: 'center',
  },
  profileInfo: {
    flex: 1,
    marginLeft: spacing.md,
  },
  profileName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  profileStats: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  lunaCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  lunaPreview: {
    marginRight: spacing.md,
  },
  lunaInfo: {
    flex: 1,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  settingInfo: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingLabel: {
    ...typography.body,
    color: colors.text,
  },
  settingDescription: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  unitToggle: {
    flexDirection: 'row',
    backgroundColor: colors.background,
    borderRadius: borderRadius.sm,
    overflow: 'hidden',
  },
  unitOption: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    ...typography.caption,
    color: colors.textMuted,
    fontWeight: '600',
  },
  unitOptionActive: {
    backgroundColor: colors.primary,
    color: colors.surface,
  },
  subscriptionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  subscriptionStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  subscriptionText: {
    ...typography.bodyBold,
    color: colors.text,
  },
  upgradeButton: {
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.md,
  },
  upgradeButtonText: {
    ...typography.caption,
    color: colors.surface,
    fontWeight: '600',
  },
  version: {
    ...typography.caption,
    color: colors.textMuted,
    textAlign: 'center',
    marginTop: spacing.lg,
  },
});
