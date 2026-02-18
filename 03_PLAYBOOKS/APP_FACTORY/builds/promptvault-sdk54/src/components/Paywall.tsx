import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Modal,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';
import { useSubscriptionStore, PRICING } from '../stores/subscriptionStore';

interface PaywallProps {
  visible: boolean;
  onClose: () => void;
  feature?: string;
}

// Premium features - Freemium model
// Free: All prompts with ads
// Premium: No ads + power features
const PREMIUM_FEATURES = [
  { icon: 'close-circle-outline', text: 'Remove all ads', highlight: true },
  { icon: 'magic-staff', text: 'AI Prompt Improver' },
  { icon: 'plus-circle-outline', text: 'Create custom prompts' },
  { icon: 'cloud-sync', text: 'Cloud sync across devices' },
  { icon: 'folder-multiple', text: 'Unlimited folders' },
  { icon: 'history', text: 'Prompt history' },
  { icon: 'export', text: 'Export to Notion/Sheets' },
];

export default function Paywall({ visible, onClose, feature }: PaywallProps) {
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'annual'>('annual');
  const [loading, setLoading] = useState(false);
  const { startTrial, restorePurchases } = useSubscriptionStore();

  const handlePurchase = async () => {
    setLoading(true);

    // Placeholder for RevenueCat purchase
    // In production:
    // const plan = selectedPlan === 'annual' ? PRICING.annual : PRICING.monthly;
    // try {
    //   const purchaserInfo = await Purchases.purchasePackage(plan);
    //   if (purchaserInfo.entitlements.active['pro']) {
    //     onClose();
    //   }
    // } catch (e) {
    //   if (!e.userCancelled) Alert.alert('Error', e.message);
    // }

    setTimeout(() => {
      setLoading(false);
      Alert.alert(
        'RevenueCat Integration Required',
        'This is a placeholder. Connect RevenueCat to enable purchases.',
        [{ text: 'OK' }]
      );
    }, 1000);
  };

  const handleStartTrial = () => {
    startTrial();
    Alert.alert('Trial Started', 'You have 7 days of Pro access. Enjoy!');
    onClose();
  };

  const handleRestore = async () => {
    setLoading(true);
    const restored = await restorePurchases();
    setLoading(false);

    if (restored) {
      Alert.alert('Success', 'Your purchases have been restored.');
      onClose();
    } else {
      Alert.alert('No Purchases Found', 'No previous purchases were found.');
    }
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        <TouchableOpacity style={styles.closeButton} onPress={onClose}>
          <MaterialCommunityIcons name="close" size={28} color={colors.text} />
        </TouchableOpacity>

        <ScrollView
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.header}>
            <MaterialCommunityIcons
              name="star-circle"
              size={48}
              color={colors.primary}
            />
            <Text style={styles.title}>Go Premium</Text>
            <Text style={styles.subtitle}>
              Remove ads and unlock power features
            </Text>
            {feature && (
              <Text style={styles.featureHint}>
                "{feature}" requires Premium
              </Text>
            )}
          </View>

          {/* Free tier reminder */}
          <View style={styles.freeReminder}>
            <MaterialCommunityIcons
              name="check-circle"
              size={18}
              color={colors.success}
            />
            <Text style={styles.freeReminderText}>
              You already have free access to all 1,050+ prompts
            </Text>
          </View>

          <View style={styles.features}>
            {PREMIUM_FEATURES.map((f, i) => (
              <View key={i} style={[styles.featureRow, f.highlight && styles.featureRowHighlight]}>
                <MaterialCommunityIcons
                  name={f.icon as any}
                  size={20}
                  color={f.highlight ? colors.success : colors.primary}
                />
                <Text style={[styles.featureText, f.highlight && styles.featureTextHighlight]}>
                  {f.text}
                </Text>
              </View>
            ))}
          </View>

          <View style={styles.plans}>
            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPlan === 'annual' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('annual')}
            >
              {PRICING.annual.savings && (
                <View style={styles.savingsBadge}>
                  <Text style={styles.savingsText}>
                    BEST VALUE
                  </Text>
                </View>
              )}
              <Text style={styles.planName}>Annual</Text>
              <Text style={styles.planPrice}>{PRICING.annual.price}</Text>
              <Text style={styles.planPeriod}>per year</Text>
              <Text style={styles.planBreakdown}>
                Just {PRICING.annual.monthlyEquivalent}/month
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPlan === 'monthly' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('monthly')}
            >
              <Text style={styles.planName}>Monthly</Text>
              <Text style={styles.planPrice}>{PRICING.monthly.price}</Text>
              <Text style={styles.planPeriod}>per month</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.purchaseButton, loading && styles.buttonDisabled]}
            onPress={handlePurchase}
            disabled={loading}
          >
            <Text style={styles.purchaseButtonText}>
              {loading ? 'Processing...' : 'Remove Ads & Go Premium'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.trialButton}
            onPress={handleStartTrial}
          >
            <Text style={styles.trialButtonText}>
              Try Premium Free for 7 Days
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.restoreButton}
            onPress={handleRestore}
          >
            <Text style={styles.restoreText}>Restore Purchases</Text>
          </TouchableOpacity>

          <Text style={styles.terms}>
            {selectedPlan === 'annual' ? '$19.99/year' : '$2.99/month'} after trial.
            Cancel anytime. Payment charged to your iTunes Account.
          </Text>
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  closeButton: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    zIndex: 10,
    padding: spacing.sm,
  },
  content: {
    padding: spacing.lg,
    paddingTop: spacing.xxl,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
    marginTop: spacing.md,
  },
  subtitle: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    marginTop: spacing.xs,
    textAlign: 'center',
  },
  featureHint: {
    fontSize: fontSize.sm,
    color: colors.primary,
    marginTop: spacing.sm,
    fontWeight: '500',
  },
  freeReminder: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.success + '15',
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.md,
    gap: spacing.sm,
  },
  freeReminderText: {
    fontSize: fontSize.sm,
    color: colors.success,
    flex: 1,
  },
  features: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.xl,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
    gap: spacing.md,
  },
  featureText: {
    fontSize: fontSize.md,
    color: colors.text,
  },
  featureRowHighlight: {
    backgroundColor: colors.success + '10',
    marginHorizontal: -spacing.md,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.sm,
    marginBottom: spacing.sm,
  },
  featureTextHighlight: {
    fontWeight: '600',
    color: colors.success,
  },
  plans: {
    flexDirection: 'row',
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  planCard: {
    flex: 1,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
    position: 'relative',
  },
  planCardSelected: {
    borderColor: colors.primary,
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: colors.success,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  savingsText: {
    fontSize: fontSize.xs,
    fontWeight: '700',
    color: colors.background,
  },
  planName: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.textSecondary,
    marginTop: spacing.sm,
  },
  planPrice: {
    fontSize: fontSize.xxl,
    fontWeight: '700',
    color: colors.text,
    marginTop: spacing.xs,
  },
  planPeriod: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },
  planBreakdown: {
    fontSize: fontSize.xs,
    color: colors.success,
    marginTop: spacing.xs,
    fontWeight: '500',
  },
  purchaseButton: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  purchaseButtonText: {
    fontSize: fontSize.lg,
    fontWeight: '700',
    color: colors.text,
  },
  trialButton: {
    backgroundColor: colors.surface,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    marginBottom: spacing.md,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  trialButtonText: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.primary,
  },
  restoreButton: {
    alignItems: 'center',
    paddingVertical: spacing.sm,
    marginBottom: spacing.lg,
  },
  restoreText: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
    textDecorationLine: 'underline',
  },
  terms: {
    fontSize: fontSize.xs,
    color: colors.textMuted,
    textAlign: 'center',
    lineHeight: 16,
  },
});
