import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import Paywall from '../components/Paywall';
import { useSubscriptionStore } from '../stores/subscriptionStore';
import { useFavoriteStore } from '../stores/favoriteStore';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';

interface SettingRowProps {
  icon: string;
  title: string;
  subtitle?: string;
  onPress: () => void;
  rightElement?: React.ReactNode;
  destructive?: boolean;
}

function SettingRow({
  icon,
  title,
  subtitle,
  onPress,
  rightElement,
  destructive,
}: SettingRowProps) {
  return (
    <TouchableOpacity style={styles.row} onPress={onPress}>
      <View
        style={[
          styles.iconContainer,
          destructive && { backgroundColor: colors.error + '20' },
        ]}
      >
        <MaterialCommunityIcons
          name={icon as any}
          size={22}
          color={destructive ? colors.error : colors.primary}
        />
      </View>
      <View style={styles.rowContent}>
        <Text style={[styles.rowTitle, destructive && { color: colors.error }]}>
          {title}
        </Text>
        {subtitle && <Text style={styles.rowSubtitle}>{subtitle}</Text>}
      </View>
      {rightElement || (
        <MaterialCommunityIcons
          name="chevron-right"
          size={24}
          color={colors.textMuted}
        />
      )}
    </TouchableOpacity>
  );
}

export default function SettingsScreen() {
  const [paywallVisible, setPaywallVisible] = useState(false);
  const { isPro, trialActive, trialEndsAt, cancelSubscription } =
    useSubscriptionStore();
  const { clearAllFavorites, favoriteIds } = useFavoriteStore();

  const handleUpgrade = () => {
    setPaywallVisible(true);
  };

  const handleRestorePurchases = async () => {
    // Placeholder for RevenueCat restore
    Alert.alert(
      'RevenueCat Required',
      'Connect RevenueCat to enable purchase restoration.'
    );
  };

  const handleManageSubscription = () => {
    // Open subscription management
    if (Platform.OS === 'ios') {
      Linking.openURL('https://apps.apple.com/account/subscriptions');
    } else {
      Linking.openURL(
        'https://play.google.com/store/account/subscriptions'
      );
    }
  };

  const handleClearFavorites = () => {
    if (favoriteIds.length === 0) {
      Alert.alert('No Favorites', 'You have no favorites to clear.');
      return;
    }

    Alert.alert(
      'Clear Favorites',
      `Are you sure you want to remove all ${favoriteIds.length} favorites?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: clearAllFavorites,
        },
      ]
    );
  };

  const handleContact = () => {
    Linking.openURL('mailto:support@promptvault.app');
  };

  const handlePrivacy = () => {
    Linking.openURL('https://promptvault.app/privacy');
  };

  const handleTerms = () => {
    Linking.openURL('https://promptvault.app/terms');
  };

  const handleRateApp = () => {
    // Replace with actual App Store/Play Store link
    Alert.alert(
      'Rate PromptVault',
      'Would you like to rate us on the App Store?',
      [
        { text: 'Not Now', style: 'cancel' },
        {
          text: 'Rate',
          onPress: () => Linking.openURL('https://apps.apple.com/app/id123456'),
        },
      ]
    );
  };

  const formatTrialEnd = () => {
    if (!trialEndsAt) return '';
    const date = new Date(trialEndsAt);
    const days = Math.ceil(
      (date.getTime() - Date.now()) / (1000 * 60 * 60 * 24)
    );
    return `${days} days remaining`;
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <Paywall
        visible={paywallVisible}
        onClose={() => setPaywallVisible(false)}
      />

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Settings</Text>

        {/* Subscription Status */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <View style={styles.card}>
            {isPro ? (
              <>
                <View style={styles.proStatus}>
                  <MaterialCommunityIcons
                    name="crown"
                    size={24}
                    color={colors.warning}
                  />
                  <View style={styles.proInfo}>
                    <Text style={styles.proTitle}>Pro Member</Text>
                    {trialActive && (
                      <Text style={styles.trialText}>
                        Trial: {formatTrialEnd()}
                      </Text>
                    )}
                  </View>
                </View>
                <TouchableOpacity
                  style={styles.manageButton}
                  onPress={handleManageSubscription}
                >
                  <Text style={styles.manageButtonText}>
                    Manage Subscription
                  </Text>
                </TouchableOpacity>
              </>
            ) : (
              <>
                <View style={styles.freeStatus}>
                  <Text style={styles.freeTitle}>Free Plan</Text>
                  <Text style={styles.freeSubtitle}>
                    All prompts free with ads
                  </Text>
                </View>
                <TouchableOpacity
                  style={styles.upgradeButton}
                  onPress={handleUpgrade}
                >
                  <MaterialCommunityIcons
                    name="star-circle"
                    size={18}
                    color={colors.background}
                  />
                  <Text style={styles.upgradeButtonText}>Remove Ads - $2.99/mo</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </View>

        {/* Account */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <View style={styles.card}>
            <SettingRow
              icon="restore"
              title="Restore Purchases"
              onPress={handleRestorePurchases}
            />
            <SettingRow
              icon="heart-remove"
              title="Clear All Favorites"
              subtitle={`${favoriteIds.length} favorites`}
              onPress={handleClearFavorites}
              destructive
            />
          </View>
        </View>

        {/* Support */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <View style={styles.card}>
            <SettingRow
              icon="email-outline"
              title="Contact Support"
              onPress={handleContact}
            />
            <SettingRow
              icon="star-outline"
              title="Rate PromptVault"
              onPress={handleRateApp}
            />
          </View>
        </View>

        {/* Legal */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Legal</Text>
          <View style={styles.card}>
            <SettingRow
              icon="shield-check-outline"
              title="Privacy Policy"
              onPress={handlePrivacy}
            />
            <SettingRow
              icon="file-document-outline"
              title="Terms of Service"
              onPress={handleTerms}
            />
          </View>
        </View>

        <Text style={styles.version}>PromptVault v1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

// Need Platform import
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    padding: spacing.lg,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.lg,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: spacing.sm,
    marginLeft: spacing.xs,
  },
  card: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.surfaceLight,
  },
  iconContainer: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: colors.primary + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  rowContent: {
    flex: 1,
  },
  rowTitle: {
    fontSize: fontSize.md,
    fontWeight: '500',
    color: colors.text,
  },
  rowSubtitle: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
    marginTop: 2,
  },
  proStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    gap: spacing.md,
  },
  proInfo: {
    flex: 1,
  },
  proTitle: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.text,
  },
  trialText: {
    fontSize: fontSize.sm,
    color: colors.warning,
    marginTop: 2,
  },
  manageButton: {
    margin: spacing.md,
    marginTop: 0,
    backgroundColor: colors.surfaceLight,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    alignItems: 'center',
  },
  manageButtonText: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
  },
  freeStatus: {
    padding: spacing.md,
  },
  freeTitle: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.text,
  },
  freeSubtitle: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
    marginTop: 2,
  },
  upgradeButton: {
    flexDirection: 'row',
    backgroundColor: colors.primary,
    margin: spacing.md,
    marginTop: 0,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
  upgradeButtonText: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.background,
  },
  version: {
    textAlign: 'center',
    fontSize: fontSize.sm,
    color: colors.textMuted,
    marginTop: spacing.lg,
    marginBottom: spacing.xl,
  },
});
