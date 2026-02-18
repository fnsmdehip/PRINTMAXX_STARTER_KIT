import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import { router } from 'expo-router';

import { COLORS, MONTHLY_PRICE } from '../../src/utils/constants';
import { GoalSelector } from '../../src/components/GoalSelector';
import { Button } from '../../src/components/Button';
import { useUserStore } from '../../src/stores/userStore';
import { restorePurchases } from '../../src/services/subscriptionService';

export default function SettingsScreen() {
  const [showGoalSelector, setShowGoalSelector] = useState(false);
  const [isRestoring, setIsRestoring] = useState(false);

  const {
    settings,
    subscription,
    setStepGoal,
    updateSettings,
  } = useUserStore();

  const handleEmergencyUnlock = () => {
    router.push('/emergency-unlock');
  };

  const handleRestorePurchases = async () => {
    setIsRestoring(true);
    const result = await restorePurchases();
    setIsRestoring(false);

    if (result.success) {
      Alert.alert('Restored', 'Your subscription has been restored.');
    } else {
      Alert.alert('No subscription found', result.error || 'No active subscription to restore.');
    }
  };

  const handleManageApps = () => {
    // Navigate to app selection screen
    Alert.alert(
      'Manage blocked apps',
      'This would open the app selection screen. Feature coming soon.'
    );
  };

  const handlePaywall = () => {
    router.push('/paywall');
  };

  const handlePrivacyPolicy = () => {
    router.push('/privacy-policy');
  };

  const handleTerms = () => {
    router.push('/terms');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Subscription Status */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <View style={styles.subscriptionCard}>
            {subscription.isSubscribed ? (
              <>
                <Text style={styles.subscriptionStatus}>Premium Active</Text>
                <Text style={styles.subscriptionDetail}>
                  Expires: {subscription.expirationDate || 'Never'}
                </Text>
              </>
            ) : subscription.isInTrial ? (
              <>
                <Text style={styles.subscriptionStatus}>Free Trial</Text>
                <Text style={styles.subscriptionDetail}>
                  {subscription.trialDaysRemaining} days remaining
                </Text>
                <Button
                  title={`Subscribe - ${MONTHLY_PRICE}/mo`}
                  onPress={handlePaywall}
                  style={styles.subscribeButton}
                />
              </>
            ) : (
              <>
                <Text style={styles.subscriptionStatus}>Trial Expired</Text>
                <Button
                  title={`Subscribe - ${MONTHLY_PRICE}/mo`}
                  onPress={handlePaywall}
                  style={styles.subscribeButton}
                />
              </>
            )}
            <TouchableOpacity
              onPress={handleRestorePurchases}
              disabled={isRestoring}
            >
              <Text style={styles.restoreLink}>
                {isRestoring ? 'Restoring...' : 'Restore purchases'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Step Goal */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Step goal</Text>
          <TouchableOpacity
            style={styles.settingRow}
            onPress={() => setShowGoalSelector(!showGoalSelector)}
          >
            <Text style={styles.settingLabel}>Daily goal</Text>
            <View style={styles.settingValue}>
              <Text style={styles.settingValueText}>
                {settings.stepGoal.toLocaleString()} steps
              </Text>
              <Text style={styles.chevron}>{showGoalSelector ? '▲' : '▼'}</Text>
            </View>
          </TouchableOpacity>
          {showGoalSelector && (
            <GoalSelector
              value={settings.stepGoal}
              onChange={(value) => {
                setStepGoal(value);
              }}
            />
          )}
        </View>

        {/* Blocked Apps */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Blocked apps</Text>
          <TouchableOpacity
            style={styles.settingRow}
            onPress={handleManageApps}
          >
            <Text style={styles.settingLabel}>Manage blocked apps</Text>
            <View style={styles.settingValue}>
              <Text style={styles.settingValueText}>
                {settings.blockedApps.length} app{settings.blockedApps.length !== 1 ? 's' : ''}
              </Text>
              <Text style={styles.chevron}>›</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Notifications */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          <View style={styles.settingRow}>
            <Text style={styles.settingLabel}>Enable notifications</Text>
            <Switch
              value={settings.notificationsEnabled}
              onValueChange={(value) =>
                updateSettings({ notificationsEnabled: value })
              }
              trackColor={{ false: COLORS.border, true: COLORS.primary }}
            />
          </View>
        </View>

        {/* Emergency Unlock */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Emergency</Text>
          <View style={styles.settingRow}>
            <Text style={styles.settingLabel}>Allow emergency unlock</Text>
            <Switch
              value={settings.emergencyUnlockEnabled}
              onValueChange={(value) =>
                updateSettings({ emergencyUnlockEnabled: value })
              }
              trackColor={{ false: COLORS.border, true: COLORS.primary }}
            />
          </View>
          {settings.emergencyUnlockEnabled && (
            <TouchableOpacity
              style={styles.emergencyButton}
              onPress={handleEmergencyUnlock}
            >
              <Text style={styles.emergencyButtonText}>
                Use emergency unlock
              </Text>
            </TouchableOpacity>
          )}
          <Text style={styles.settingHint}>
            Emergency unlock lets you access apps without hitting your goal.
            This resets your streak.
          </Text>
        </View>

        {/* Support */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <TouchableOpacity style={styles.settingRow}>
            <Text style={styles.settingLabel}>Help center</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.settingRow}>
            <Text style={styles.settingLabel}>Contact support</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.settingRow}
            onPress={handlePrivacyPolicy}
          >
            <Text style={styles.settingLabel}>Privacy policy</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.settingRow}
            onPress={handleTerms}
          >
            <Text style={styles.settingLabel}>Terms of service</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
        </View>

        {/* App Version */}
        <Text style={styles.version}>StepUnlock v1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: 20,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  subscriptionCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
  },
  subscriptionStatus: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  subscriptionDetail: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  subscribeButton: {
    marginBottom: 12,
  },
  restoreLink: {
    fontSize: 14,
    color: COLORS.primary,
    textAlign: 'center',
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.surface,
    padding: 16,
    borderRadius: 12,
    marginBottom: 2,
  },
  settingLabel: {
    fontSize: 16,
    color: COLORS.text,
  },
  settingValue: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingValueText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginRight: 8,
  },
  chevron: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  settingHint: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 8,
    paddingHorizontal: 4,
  },
  emergencyButton: {
    backgroundColor: '#FFEBEE',
    padding: 12,
    borderRadius: 8,
    marginTop: 8,
    alignItems: 'center',
  },
  emergencyButtonText: {
    color: COLORS.error,
    fontWeight: '500',
  },
  version: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 20,
  },
});
