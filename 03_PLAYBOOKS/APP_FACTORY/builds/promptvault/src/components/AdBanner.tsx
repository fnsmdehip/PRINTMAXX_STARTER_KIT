import React from 'react';
import { View, Text, StyleSheet, Platform } from 'react-native';
import { useSubscriptionStore, AD_CONFIG } from '../stores/subscriptionStore';
import { colors, spacing, fontSize } from '../utils/theme';

/**
 * AdBanner Component - Freemium Ad Integration
 *
 * Shows a banner ad at the bottom of screens for free users.
 * Premium users see no ads.
 *
 * SETUP INSTRUCTIONS:
 * 1. Install: npx expo install react-native-google-mobile-ads
 * 2. Configure app.json with AdMob app IDs
 * 3. Replace placeholder with real BannerAd component
 *
 * app.json additions:
 * {
 *   "expo": {
 *     "plugins": [
 *       [
 *         "react-native-google-mobile-ads",
 *         {
 *           "androidAppId": "ca-app-pub-XXXXX~XXXXX",
 *           "iosAppId": "ca-app-pub-XXXXX~XXXXX"
 *         }
 *       ]
 *     ]
 *   }
 * }
 *
 * PRODUCTION CODE (uncomment when ready):
 *
 * import { BannerAd, BannerAdSize, TestIds } from 'react-native-google-mobile-ads';
 *
 * const adUnitId = __DEV__
 *   ? TestIds.BANNER
 *   : Platform.select({
 *       ios: AD_CONFIG.banner.ios,
 *       android: AD_CONFIG.banner.android,
 *     });
 *
 * return (
 *   <BannerAd
 *     unitId={adUnitId}
 *     size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
 *     requestOptions={{
 *       requestNonPersonalizedAdsOnly: true,
 *     }}
 *   />
 * );
 */

interface AdBannerProps {
  // Optional: specify a different ad size
  size?: 'banner' | 'large' | 'medium';
}

export default function AdBanner({ size = 'banner' }: AdBannerProps) {
  const { isPro } = useSubscriptionStore();

  // Premium users don't see ads
  if (isPro) {
    return null;
  }

  // Get banner height based on size
  const getHeight = () => {
    switch (size) {
      case 'large':
        return 100;
      case 'medium':
        return 90;
      default:
        return 50;
    }
  };

  // PLACEHOLDER: Replace with actual BannerAd when react-native-google-mobile-ads is installed
  // This placeholder shows what the ad space looks like
  return (
    <View style={[styles.container, { height: getHeight() }]}>
      <View style={styles.placeholder}>
        <Text style={styles.placeholderText}>Ad Banner</Text>
        <Text style={styles.placeholderSubtext}>
          Install react-native-google-mobile-ads to enable
        </Text>
      </View>
    </View>
  );
}

/**
 * Interstitial Ad Hook - Show between category switches
 *
 * SETUP: After installing react-native-google-mobile-ads, create this hook:
 *
 * import { useInterstitialAd, TestIds } from 'react-native-google-mobile-ads';
 *
 * export function useFreemiumInterstitial() {
 *   const { isPro } = useSubscriptionStore();
 *   const [categorySwitchCount, setCategorySwitchCount] = useState(0);
 *
 *   const adUnitId = __DEV__
 *     ? TestIds.INTERSTITIAL
 *     : Platform.select({
 *         ios: AD_CONFIG.interstitial.ios,
 *         android: AD_CONFIG.interstitial.android,
 *       });
 *
 *   const { isLoaded, load, show } = useInterstitialAd(adUnitId, {
 *     requestNonPersonalizedAdsOnly: true,
 *   });
 *
 *   useEffect(() => {
 *     if (!isPro) {
 *       load();
 *     }
 *   }, [load, isPro]);
 *
 *   const onCategorySwitch = useCallback(() => {
 *     if (isPro) return;
 *
 *     const newCount = categorySwitchCount + 1;
 *     setCategorySwitchCount(newCount);
 *
 *     // Show interstitial every N switches
 *     if (newCount % AD_CONFIG.interstitialFrequency === 0 && isLoaded) {
 *       show();
 *       load(); // Preload next
 *     }
 *   }, [categorySwitchCount, isPro, isLoaded, show, load]);
 *
 *   return { onCategorySwitch };
 * }
 */

// Placeholder interstitial tracker for free users
let categorySwitchCount = 0;

export function trackCategorySwitch(isPro: boolean): boolean {
  if (isPro) return false;

  categorySwitchCount += 1;

  // Return true when we should show an interstitial
  return categorySwitchCount % AD_CONFIG.interstitialFrequency === 0;
}

export function resetCategorySwitchCount() {
  categorySwitchCount = 0;
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.surfaceLight,
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.surfaceLight,
  },
  placeholderText: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textMuted,
  },
  placeholderSubtext: {
    fontSize: fontSize.xs,
    color: colors.textMuted,
    marginTop: 2,
  },
});
