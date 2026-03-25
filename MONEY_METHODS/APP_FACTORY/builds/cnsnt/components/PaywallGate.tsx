/**
 * Paywall Gate component.
 * Wraps premium features and shows upgrade prompt for free users.
 * Checks RevenueCat entitlements in real-time, not just a local boolean.
 */

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Pressable, Alert, Modal, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius, Shadows, PRO_MONTHLY_PRICE, PRO_YEARLY_PRICE, Assets } from '../constants/theme';
import purchaseService from '../services/purchases';

interface PaywallGateProps {
  feature: 'recording' | 'templates' | 'create_record';
  children: React.ReactNode;
  /** Optional override. If omitted, PaywallGate checks RevenueCat directly. */
  isAllowed?: boolean;
}

const FEATURE_DESCRIPTIONS: Record<string, { title: string; description: string }> = {
  recording: {
    title: 'Audio Recording',
    description: 'Record audio alongside your signed documents for complete records.',
  },
  templates: {
    title: 'Premium Templates',
    description: 'Access NDA, GDPR, research, and property record templates.',
  },
  create_record: {
    title: 'Unlimited Records',
    description: 'Create unlimited consent records. Free tier allows 5 records.',
  },
};

const PaywallGate: React.FC<PaywallGateProps> = ({
  feature,
  children,
  isAllowed: isAllowedProp,
}) => {
  const [showModal, setShowModal] = useState(false);
  const [purchasing, setPurchasing] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [entitlementChecked, setEntitlementChecked] = useState(false);
  const [allowed, setAllowed] = useState(isAllowedProp ?? false);

  // Check RevenueCat entitlements on mount if no prop override
  useEffect(() => {
    if (isAllowedProp !== undefined) {
      setAllowed(isAllowedProp);
      setEntitlementChecked(true);
      return;
    }

    let mounted = true;
    (async () => {
      try {
        const canAccess = await purchaseService.canAccess(
          feature === 'create_record' ? 'create_record' : feature
        );
        if (mounted) {
          setAllowed(canAccess);
          setEntitlementChecked(true);
        }
      } catch {
        if (mounted) {
          setAllowed(false);
          setEntitlementChecked(true);
        }
      }
    })();

    return () => { mounted = false; };
  }, [feature, isAllowedProp]);

  // Update if prop changes
  useEffect(() => {
    if (isAllowedProp !== undefined) {
      setAllowed(isAllowedProp);
    }
  }, [isAllowedProp]);

  if (!entitlementChecked) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="small" color={Colors.primary} />
      </View>
    );
  }

  if (allowed) {
    return <>{children}</>;
  }

  const featureInfo = FEATURE_DESCRIPTIONS[feature];

  const handleUpgrade = async () => {
    setPurchasing(true);
    try {
      const success = await purchaseService.purchasePro();
      if (success) {
        setAllowed(true);
        setShowModal(false);
        Alert.alert('Welcome to Pro!', 'You now have full access to all features.');
      } else {
        Alert.alert(
          'Purchase Incomplete',
          'The purchase could not be completed. Please try again or check your App Store account.'
        );
      }
    } catch {
      Alert.alert(
        'Purchase Error',
        'Something went wrong during the purchase. Please try again.'
      );
    } finally {
      setPurchasing(false);
    }
  };

  const handleRestore = async () => {
    setRestoring(true);
    try {
      const entitlement = await purchaseService.restorePurchases();
      if (entitlement === 'pro') {
        setAllowed(true);
        Alert.alert('Restored', 'Pro subscription restored successfully!');
        setShowModal(false);
      } else {
        Alert.alert('No Purchase Found', 'No active Pro subscription was found.');
      }
    } catch {
      Alert.alert('Restore Error', 'Could not restore purchases. Please try again.');
    } finally {
      setRestoring(false);
    }
  };

  return (
    <>
      <Pressable style={styles.lockedContainer} onPress={() => setShowModal(true)}>
        <View style={styles.lockedOverlay}>
          <Ionicons name="lock-closed-outline" size={32} color={Colors.textSecondary} style={{ marginBottom: Spacing.sm }} />
          <Text style={styles.lockedTitle}>Pro Feature</Text>
          <Text style={styles.lockedSubtitle}>Tap to learn more</Text>
        </View>
      </Pressable>

      <Modal
        visible={showModal}
        animationType="slide"
        transparent
        onRequestClose={() => setShowModal(false)}
      >
        <View style={styles.modalBackdrop}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Upgrade to Pro</Text>
            <Text style={styles.featureTitle}>{featureInfo.title}</Text>
            <Text style={styles.featureDescription}>
              {featureInfo.description}
            </Text>

            <View style={styles.pricingBox}>
              <Text style={styles.price}>{PRO_YEARLY_PRICE}</Text>
              <Text style={styles.priceUnit}>/year</Text>
            </View>
            <Text style={styles.pricingAlt}>or {PRO_MONTHLY_PRICE}/month</Text>

            <View style={styles.benefitsList}>
              <Text style={styles.benefit}>
                {'\u2713'} Unlimited consent records
              </Text>
              <Text style={styles.benefit}>
                {'\u2713'} Audio recording
              </Text>
              <Text style={styles.benefit}>
                {'\u2713'} All premium templates
              </Text>
              <Text style={styles.benefit}>
                {'\u2713'} PDF export with SHA-256 hash
              </Text>
              <Text style={styles.benefit}>
                {'\u2713'} Cloud backup
              </Text>
            </View>

            <Pressable
              style={[styles.upgradeButton, purchasing && styles.buttonDisabled]}
              onPress={handleUpgrade}
              disabled={purchasing || restoring}
            >
              <Text style={styles.upgradeButtonText}>
                {purchasing ? 'Processing...' : 'Upgrade to Pro'}
              </Text>
            </Pressable>

            <Pressable onPress={handleRestore} disabled={purchasing || restoring}>
              <Text style={styles.restoreText}>
                {restoring ? 'Restoring...' : 'Restore Purchases'}
              </Text>
            </Pressable>

            <Text style={styles.legalTerms}>
              Subscription automatically renews unless canceled at least 24 hours before the end of the current period. Manage subscriptions in your Apple ID account settings.
            </Text>

            <Pressable
              style={styles.closeButton}
              onPress={() => setShowModal(false)}
            >
              <Text style={styles.closeButtonText}>Maybe Later</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    backgroundColor: Colors.surfaceElevated,
    borderRadius: BorderRadius.lg,
    padding: Spacing.xl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 80,
  },
  lockedContainer: {
    backgroundColor: Colors.surfaceElevated,
    borderRadius: BorderRadius.lg,
    padding: Spacing.xl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 120,
    borderWidth: 1,
    borderColor: Colors.border,
    borderStyle: 'dashed',
  },
  lockedOverlay: {
    alignItems: 'center',
  },
  lockedTitle: {
    ...Typography.h3,
    color: Colors.textSecondary,
  },
  lockedSubtitle: {
    ...Typography.caption,
    color: Colors.textTertiary,
    marginTop: Spacing.xs,
  },
  modalBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: Colors.surface,
    borderTopLeftRadius: BorderRadius.xl,
    borderTopRightRadius: BorderRadius.xl,
    padding: Spacing.xl,
    paddingBottom: Spacing.xxxl,
    alignItems: 'center',
  },
  modalTitle: {
    ...Typography.h2,
    color: Colors.textPrimary,
    marginBottom: Spacing.lg,
  },
  featureTitle: {
    ...Typography.h3,
    color: Colors.primary,
    marginBottom: Spacing.sm,
  },
  featureDescription: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    fontWeight: '300',
    lineHeight: 24,
    marginBottom: Spacing.xl,
  },
  pricingBox: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: Spacing.xl,
  },
  price: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.primary,
    fontVariant: ['tabular-nums'],
  },
  priceUnit: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginLeft: Spacing.xs,
  },
  pricingAlt: {
    ...Typography.caption,
    color: Colors.textTertiary,
    marginBottom: Spacing.lg,
  },
  benefitsList: {
    alignSelf: 'stretch',
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.lg,
  },
  benefit: {
    ...Typography.body,
    color: Colors.textPrimary,
    marginBottom: Spacing.sm,
  },
  upgradeButton: {
    backgroundColor: Colors.primary,
    paddingHorizontal: Spacing.xxxl,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.lg,
    ...Shadows.md,
  },
  upgradeButtonText: {
    ...Typography.button,
    color: Colors.textInverse,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  restoreText: {
    ...Typography.bodySmall,
    color: Colors.textLink,
    marginBottom: Spacing.lg,
  },
  legalTerms: {
    ...Typography.caption,
    color: Colors.textTertiary,
    textAlign: 'center',
    marginBottom: Spacing.md,
    paddingHorizontal: Spacing.lg,
    fontSize: 11,
    lineHeight: 16,
  },
  closeButton: {
    paddingVertical: Spacing.sm,
  },
  closeButtonText: {
    ...Typography.body,
    color: Colors.textTertiary,
  },
});

export default PaywallGate;
