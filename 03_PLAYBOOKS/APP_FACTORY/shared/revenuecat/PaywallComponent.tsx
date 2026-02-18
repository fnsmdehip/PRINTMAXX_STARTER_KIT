/**
 * PaywallComponent
 * Generic, customizable paywall for subscription conversion
 */

import React, { useState, useCallback, useMemo } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
  SafeAreaView,
  Dimensions,
  type ViewStyle,
  type TextStyle,
} from 'react-native';
import type { PurchasesPackage } from 'react-native-purchases';
import { usePurchase } from './usePurchase';
import type { PaywallProps, PaywallTheme, PackageDisplayInfo } from './types';

/**
 * Default paywall theme
 */
const defaultTheme: Required<PaywallTheme> = {
  backgroundColor: '#FFFFFF',
  textColor: '#1A1A1A',
  subtextColor: '#666666',
  accentColor: '#3B82F6',
  successColor: '#22C55E',
  buttonTextColor: '#FFFFFF',
  borderColor: '#E5E5E5',
  recommendedBackground: '#EFF6FF',
};

/**
 * Default features list
 */
const defaultFeatures = [
  'Unlimited access to all features',
  'Ad-free experience',
  'Priority support',
  'Exclusive content',
];

/**
 * Paywall Component
 *
 * A complete, customizable paywall for converting free users to subscribers.
 *
 * @example
 * ```tsx
 * function App() {
 *   const [showPaywall, setShowPaywall] = useState(false);
 *
 *   return (
 *     <>
 *       <MainContent />
 *       <Modal visible={showPaywall} animationType="slide">
 *         <Paywall
 *           onPurchaseComplete={() => setShowPaywall(false)}
 *           onClose={() => setShowPaywall(false)}
 *           title="Unlock Premium"
 *           subtitle="Get access to all features"
 *           features={[
 *             'Unlimited usage',
 *             'All premium features',
 *             'Priority support',
 *           ]}
 *           theme={{
 *             accentColor: '#8B5CF6',
 *           }}
 *         />
 *       </Modal>
 *     </>
 *   );
 * }
 * ```
 */
export function Paywall({
  onPurchaseComplete,
  onClose,
  title = 'Unlock Premium',
  subtitle = 'Get full access to all features',
  features = defaultFeatures,
  showRestore = true,
  theme: customTheme,
  source = 'paywall',
}: PaywallProps): JSX.Element {
  const theme = useMemo(
    () => ({ ...defaultTheme, ...customTheme }),
    [customTheme]
  );

  const {
    packages,
    purchasePackage,
    restorePurchases,
    isPurchasing,
    isRestoring,
    isLoadingPackages,
    packagesError,
  } = usePurchase();

  const [selectedPackage, setSelectedPackage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  /**
   * Get the recommended package (annual) or first available
   */
  const recommendedPackageId = useMemo(() => {
    const annual = packages.find((p) => p.isRecommended);
    return annual?.identifier || packages[0]?.identifier || null;
  }, [packages]);

  /**
   * Set initial selection to recommended package
   */
  React.useEffect(() => {
    if (recommendedPackageId && !selectedPackage) {
      setSelectedPackage(recommendedPackageId);
    }
  }, [recommendedPackageId, selectedPackage]);

  /**
   * Handle purchase
   */
  const handlePurchase = useCallback(async () => {
    if (!selectedPackage) return;

    const pkg = packages.find((p) => p.identifier === selectedPackage);
    if (!pkg) return;

    setError(null);

    const result = await purchasePackage(pkg.package);

    if (result.success) {
      onPurchaseComplete();
    } else if (!result.userCancelled) {
      setError(result.error || 'Purchase failed. Please try again.');
    }
  }, [selectedPackage, packages, purchasePackage, onPurchaseComplete]);

  /**
   * Handle restore
   */
  const handleRestore = useCallback(async () => {
    setError(null);

    const result = await restorePurchases();

    if (result.success && result.purchasesRestored) {
      onPurchaseComplete();
    } else if (result.success && !result.purchasesRestored) {
      setError('No previous purchases found.');
    } else {
      setError(result.error || 'Restore failed. Please try again.');
    }
  }, [restorePurchases, onPurchaseComplete]);

  /**
   * Dynamic styles based on theme
   */
  const dynamicStyles = useMemo(
    () =>
      StyleSheet.create({
        container: {
          backgroundColor: theme.backgroundColor,
        },
        title: {
          color: theme.textColor,
        },
        subtitle: {
          color: theme.subtextColor,
        },
        feature: {
          color: theme.textColor,
        },
        checkmark: {
          color: theme.successColor,
        },
        packageOption: {
          borderColor: theme.borderColor,
        },
        packageOptionSelected: {
          borderColor: theme.accentColor,
          backgroundColor: theme.recommendedBackground,
        },
        packageTitle: {
          color: theme.textColor,
        },
        packagePrice: {
          color: theme.textColor,
        },
        packageSublabel: {
          color: theme.successColor,
        },
        recommendedBadge: {
          backgroundColor: theme.accentColor,
        },
        purchaseButton: {
          backgroundColor: theme.accentColor,
        },
        purchaseButtonText: {
          color: theme.buttonTextColor,
        },
        restoreButton: {
          color: theme.subtextColor,
        },
        errorText: {
          color: '#EF4444',
        },
        termsText: {
          color: theme.subtextColor,
        },
      }),
    [theme]
  );

  /**
   * Render loading state
   */
  if (isLoadingPackages) {
    return (
      <SafeAreaView style={[styles.safeArea, dynamicStyles.container]}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={theme.accentColor} />
          <Text style={[styles.loadingText, dynamicStyles.subtitle]}>
            Loading options...
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  /**
   * Render error state
   */
  if (packagesError && packages.length === 0) {
    return (
      <SafeAreaView style={[styles.safeArea, dynamicStyles.container]}>
        <View style={styles.errorContainer}>
          <Text style={[styles.errorTitle, dynamicStyles.title]}>
            Unable to load subscription options
          </Text>
          <Text style={[styles.errorMessage, dynamicStyles.subtitle]}>
            {packagesError}
          </Text>
          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Text style={[styles.closeButtonText, { color: theme.accentColor }]}>
              Close
            </Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={[styles.safeArea, dynamicStyles.container]}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Close button */}
        <TouchableOpacity
          style={styles.closeIconButton}
          onPress={onClose}
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
        >
          <Text style={[styles.closeIcon, dynamicStyles.subtitle]}>X</Text>
        </TouchableOpacity>

        {/* Header */}
        <View style={styles.header}>
          <Text style={[styles.title, dynamicStyles.title]}>{title}</Text>
          <Text style={[styles.subtitle, dynamicStyles.subtitle]}>
            {subtitle}
          </Text>
        </View>

        {/* Features */}
        <View style={styles.featuresContainer}>
          {features.map((feature, index) => (
            <FeatureItem
              key={index}
              text={feature}
              checkColor={theme.successColor}
              textColor={theme.textColor}
            />
          ))}
        </View>

        {/* Packages */}
        <View style={styles.packagesContainer}>
          {packages.map((pkg) => (
            <PackageOption
              key={pkg.identifier}
              package={pkg}
              isSelected={selectedPackage === pkg.identifier}
              onSelect={() => setSelectedPackage(pkg.identifier)}
              theme={theme}
              disabled={isPurchasing || isRestoring}
            />
          ))}
        </View>

        {/* Trial info */}
        {selectedPackage && (
          <TrialInfo
            packages={packages}
            selectedPackageId={selectedPackage}
            textColor={theme.subtextColor}
          />
        )}

        {/* Error message */}
        {error && (
          <Text style={[styles.errorText, dynamicStyles.errorText]}>
            {error}
          </Text>
        )}

        {/* Purchase button */}
        <TouchableOpacity
          style={[
            styles.purchaseButton,
            dynamicStyles.purchaseButton,
            (isPurchasing || isRestoring || !selectedPackage) &&
              styles.purchaseButtonDisabled,
          ]}
          onPress={handlePurchase}
          disabled={isPurchasing || isRestoring || !selectedPackage}
        >
          {isPurchasing ? (
            <ActivityIndicator color={theme.buttonTextColor} />
          ) : (
            <Text style={[styles.purchaseButtonText, dynamicStyles.purchaseButtonText]}>
              Continue
            </Text>
          )}
        </TouchableOpacity>

        {/* Restore button */}
        {showRestore && (
          <TouchableOpacity
            style={styles.restoreButtonContainer}
            onPress={handleRestore}
            disabled={isPurchasing || isRestoring}
          >
            {isRestoring ? (
              <ActivityIndicator size="small" color={theme.subtextColor} />
            ) : (
              <Text style={[styles.restoreButtonText, dynamicStyles.restoreButton]}>
                Restore Purchases
              </Text>
            )}
          </TouchableOpacity>
        )}

        {/* Terms */}
        <Text style={[styles.termsText, dynamicStyles.termsText]}>
          Cancel anytime. Subscription auto-renews until cancelled.
          {'\n'}
          By continuing, you agree to our Terms of Service and Privacy Policy.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

/**
 * Feature item component
 */
interface FeatureItemProps {
  text: string;
  checkColor: string;
  textColor: string;
}

function FeatureItem({ text, checkColor, textColor }: FeatureItemProps): JSX.Element {
  return (
    <View style={styles.featureItem}>
      <Text style={[styles.checkmark, { color: checkColor }]}>&#10003;</Text>
      <Text style={[styles.featureText, { color: textColor }]}>{text}</Text>
    </View>
  );
}

/**
 * Package option component
 */
interface PackageOptionProps {
  package: PackageDisplayInfo;
  isSelected: boolean;
  onSelect: () => void;
  theme: Required<PaywallTheme>;
  disabled: boolean;
}

function PackageOption({
  package: pkg,
  isSelected,
  onSelect,
  theme,
  disabled,
}: PackageOptionProps): JSX.Element {
  return (
    <TouchableOpacity
      style={[
        styles.packageOption,
        { borderColor: isSelected ? theme.accentColor : theme.borderColor },
        isSelected && { backgroundColor: theme.recommendedBackground },
      ]}
      onPress={onSelect}
      disabled={disabled}
    >
      {pkg.isRecommended && (
        <View style={[styles.recommendedBadge, { backgroundColor: theme.accentColor }]}>
          <Text style={styles.recommendedBadgeText}>BEST VALUE</Text>
        </View>
      )}

      <View style={styles.packageContent}>
        <View style={styles.packageHeader}>
          <Text style={[styles.packageTitle, { color: theme.textColor }]}>
            {pkg.title}
          </Text>
          {pkg.savingsPercent && (
            <Text style={[styles.savingsBadge, { color: theme.successColor }]}>
              Save {pkg.savingsPercent}%
            </Text>
          )}
        </View>

        <View style={styles.packagePricing}>
          <Text style={[styles.packagePrice, { color: theme.textColor }]}>
            {pkg.priceString}
            <Text style={styles.packagePeriod}>{pkg.durationLabel}</Text>
          </Text>
        </View>

        {pkg.trial && (
          <Text style={[styles.trialBadge, { color: theme.successColor }]}>
            {pkg.trial.displayString}
          </Text>
        )}
      </View>

      {/* Selection indicator */}
      <View
        style={[
          styles.selectionIndicator,
          {
            borderColor: isSelected ? theme.accentColor : theme.borderColor,
            backgroundColor: isSelected ? theme.accentColor : 'transparent',
          },
        ]}
      >
        {isSelected && <View style={styles.selectionIndicatorInner} />}
      </View>
    </TouchableOpacity>
  );
}

/**
 * Trial info component
 */
interface TrialInfoProps {
  packages: PackageDisplayInfo[];
  selectedPackageId: string;
  textColor: string;
}

function TrialInfo({
  packages,
  selectedPackageId,
  textColor,
}: TrialInfoProps): JSX.Element | null {
  const selectedPkg = packages.find((p) => p.identifier === selectedPackageId);

  if (!selectedPkg?.trial) {
    return null;
  }

  return (
    <View style={styles.trialInfoContainer}>
      <Text style={[styles.trialInfoText, { color: textColor }]}>
        Start your {selectedPkg.trial.displayString}. You won't be charged until the
        trial ends.
      </Text>
    </View>
  );
}

/**
 * Styles
 */
const { width: screenWidth } = Dimensions.get('window');

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 48,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  errorTitle: {
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 8,
  },
  errorMessage: {
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 24,
  },
  closeButton: {
    padding: 12,
  },
  closeButtonText: {
    fontSize: 16,
    fontWeight: '600',
  },
  closeIconButton: {
    position: 'absolute',
    top: 0,
    right: 0,
    padding: 8,
    zIndex: 10,
  },
  closeIcon: {
    fontSize: 20,
    fontWeight: '600',
  },
  header: {
    marginTop: 32,
    marginBottom: 24,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
  },
  featuresContainer: {
    marginBottom: 24,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    paddingHorizontal: 8,
  },
  checkmark: {
    fontSize: 18,
    fontWeight: '600',
    marginRight: 12,
    width: 24,
  },
  featureText: {
    fontSize: 16,
    flex: 1,
  },
  packagesContainer: {
    marginBottom: 16,
  },
  packageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    position: 'relative',
  },
  recommendedBadge: {
    position: 'absolute',
    top: -12,
    left: 16,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  recommendedBadgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  packageContent: {
    flex: 1,
  },
  packageHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  packageTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  savingsBadge: {
    fontSize: 12,
    fontWeight: '600',
    marginLeft: 8,
  },
  packagePricing: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  packagePrice: {
    fontSize: 20,
    fontWeight: '700',
  },
  packagePeriod: {
    fontSize: 14,
    fontWeight: '400',
  },
  trialBadge: {
    fontSize: 13,
    fontWeight: '500',
    marginTop: 4,
  },
  selectionIndicator: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 12,
  },
  selectionIndicatorInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#FFFFFF',
  },
  trialInfoContainer: {
    marginBottom: 16,
    paddingHorizontal: 8,
  },
  trialInfoText: {
    fontSize: 14,
    textAlign: 'center',
  },
  errorText: {
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 16,
  },
  purchaseButton: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    minHeight: 56,
  },
  purchaseButtonDisabled: {
    opacity: 0.6,
  },
  purchaseButtonText: {
    fontSize: 18,
    fontWeight: '600',
  },
  restoreButtonContainer: {
    alignItems: 'center',
    paddingVertical: 12,
    minHeight: 44,
    justifyContent: 'center',
  },
  restoreButtonText: {
    fontSize: 14,
    fontWeight: '500',
  },
  termsText: {
    fontSize: 11,
    textAlign: 'center',
    marginTop: 16,
    lineHeight: 16,
  },
});

export default Paywall;
