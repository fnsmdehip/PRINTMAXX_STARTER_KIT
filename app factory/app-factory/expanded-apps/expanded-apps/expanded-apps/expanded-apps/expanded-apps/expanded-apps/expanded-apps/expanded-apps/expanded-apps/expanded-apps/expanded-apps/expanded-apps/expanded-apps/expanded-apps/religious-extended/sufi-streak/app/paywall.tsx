import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
  Alert,
  ActivityIndicator,
  Animated,
  TextInput,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { Ionicons } from '@expo/vector-icons';
import { setAdFreeStatus } from '../src/components/AdBanner';
import {
  getReferralStatus,
  ReferralStatus,
  DISCOUNT_PERCENT,
  REGULAR_PRICE,
  DISCOUNTED_PRICE,
} from '../src/lib/referrals';
import { applyPromoCode, getAppliedPromoCode, PromoCode } from '../src/lib/promo-codes';
// TODO: Uncomment when RevenueCat is configured
// import { makePurchase, getOfferings, restorePurchases } from '../src/lib/purchases';

const { width } = Dimensions.get('window');

interface Feature {
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  title: string;
  description: string;
}

const features: Feature[] = [
  { icon: 'ban', color: '#ef4444', title: 'Ad-Free Experience', description: 'No interruptions while you read' },
  { icon: 'notifications', color: '#fbbf24', title: 'Daily Reminders', description: 'Stay consistent with your practice' },
  { icon: 'flame', color: '#f97316', title: 'Streak Tracking', description: 'Build lasting spiritual habits' },
  { icon: 'book', color: '#60a5fa', title: 'Daily Verses', description: 'Fresh inspiration every day' },
];

export default function PaywallScreen() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<'lifetime' | 'monthly'>('lifetime');
  const [referralStatus, setReferralStatus] = useState<ReferralStatus | null>(null);
  const [promoCode, setPromoCode] = useState<PromoCode | null>(null);
  const [promoInput, setPromoInput] = useState('');
  const [showPromoInput, setShowPromoInput] = useState(false);
  const [promoLoading, setPromoLoading] = useState(false);
  
  // Animations
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const featureAnims = useRef(features.map(() => new Animated.Value(0))).current;
  const discountPulse = useRef(new Animated.Value(1)).current;
  
  useEffect(() => {
    // Load referral status
    getReferralStatus().then(setReferralStatus);
    // Load any applied promo code
    getAppliedPromoCode().then(setPromoCode);
    
    // Entrance animation
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 400, useNativeDriver: true }),
      Animated.spring(slideAnim, { toValue: 0, tension: 50, friction: 8, useNativeDriver: true }),
    ]).start();
    
    // Staggered feature animations
    featureAnims.forEach((anim, i) => {
      Animated.timing(anim, {
        toValue: 1,
        duration: 300,
        delay: 200 + i * 80,
        useNativeDriver: true,
      }).start();
    });
  }, []);
  
  // Pulse animation for discount badge
  useEffect(() => {
    if (referralStatus?.discountUnlocked) {
      const pulse = Animated.loop(
        Animated.sequence([
          Animated.timing(discountPulse, { toValue: 1.1, duration: 800, useNativeDriver: true }),
          Animated.timing(discountPulse, { toValue: 1, duration: 800, useNativeDriver: true }),
        ])
      );
      pulse.start();
      return () => pulse.stop();
    }
  }, [referralStatus?.discountUnlocked]);
  
  const hasDiscount = referralStatus?.discountUnlocked || (promoCode?.isActive && promoCode?.discount > 0);
  const lifetimePrice = hasDiscount ? DISCOUNTED_PRICE : REGULAR_PRICE;
  const discountSource = promoCode?.isActive ? `Church Partner (${promoCode.affiliateName})` : 'Referral Reward';
  
  const handleApplyPromo = async () => {
    if (!promoInput.trim()) return;
    
    setPromoLoading(true);
    const result = await applyPromoCode(promoInput);
    setPromoLoading(false);
    
    if (result.success && result.promoCode) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setPromoCode(result.promoCode);
      setShowPromoInput(false);
      Alert.alert(
        '🎉 Promo Code Applied!',
        `You got ${result.promoCode.discount * 100}% off from ${result.promoCode.affiliateName}!`
      );
    } else {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      Alert.alert('Invalid Code', result.error || 'This promo code is not valid.');
    }
  };

  const handlePurchase = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setIsLoading(true);

    // ===========================================
    // TODO: REPLACE WITH REAL REVENUECAT PURCHASE
    // ===========================================
    // const offerings = await getOfferings();
    // if (offerings?.current) {
    //   const pkg = selectedPlan === 'lifetime' 
    //     ? offerings.current.lifetime 
    //     : offerings.current.monthly;
    //   const result = await makePurchase(pkg);
    //   if (result?.customerInfo.entitlements.active['premium']) {
    //     await setAdFreeStatus(true);
    //     router.replace('/(tabs)');
    //   }
    // }
    // ===========================================

    // DEMO MODE: Simulate purchase for testing
    setTimeout(async () => {
      await setAdFreeStatus(true);
      setIsLoading(false);
      Alert.alert(
        'Demo Mode',
        'In production, this connects to RevenueCat for real purchases. Ad-free mode enabled for testing.',
        [{ text: 'OK', onPress: () => router.replace('/(tabs)') }]
      );
    }, 1500);
  };

  const handleRestore = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setIsLoading(true);
    
    // TODO: REPLACE WITH REAL REVENUECAT RESTORE
    setTimeout(() => {
      setIsLoading(false);
      Alert.alert('No Purchases Found', 'No previous purchases to restore.');
    }, 1000);
  };

  const handleContinueFree = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.replace('/(tabs)');
  };

  return (
    <LinearGradient
      colors={['#1a1a2e', '#0f0f23', '#1a1a2e']}
      style={styles.container}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <Animated.View 
          style={[
            styles.header,
            { 
              opacity: fadeAnim,
              transform: [{ translateY: slideAnim }]
            }
          ]}
        >
          <View style={styles.iconContainer}>
            <LinearGradient
              colors={['#e9456030', '#e9456010']}
              style={styles.iconGradient}
            >
              <Ionicons name="sparkles" size={48} color="#e94560" />
            </LinearGradient>
          </View>
          <Text style={styles.title}>Go Premium</Text>
          <Text style={styles.subtitle}>
            Support the app and enjoy an uninterrupted spiritual journey
          </Text>
        </Animated.View>

        {/* Features */}
        <View style={styles.featuresContainer}>
          {features.map((feature, index) => (
            <Animated.View 
              key={index} 
              style={[
                styles.featureItem,
                {
                  opacity: featureAnims[index],
                  transform: [{
                    translateX: featureAnims[index].interpolate({
                      inputRange: [0, 1],
                      outputRange: [-20, 0],
                    })
                  }]
                }
              ]}
            >
              <View style={[styles.featureIconContainer, { backgroundColor: feature.color + '20' }]}>
                <Ionicons name={feature.icon} size={24} color={feature.color} />
              </View>
              <View style={styles.featureContent}>
                <Text style={styles.featureTitle}>{feature.title}</Text>
                <Text style={styles.featureDescription}>{feature.description}</Text>
              </View>
              <Ionicons name="checkmark-circle" size={22} color="#4ade80" />
            </Animated.View>
          ))}
        </View>

        {/* Discount Banner */}
        {hasDiscount && (
          <Animated.View style={[styles.discountBanner, { transform: [{ scale: discountPulse }] }]}>
            <LinearGradient
              colors={['#4ade80', '#22c55e']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.discountGradient}
            >
              <Ionicons name="gift" size={20} color="#ffffff" />
              <Text style={styles.discountText}>
                🎉 {DISCOUNT_PERCENT}% OFF - {discountSource}
              </Text>
            </LinearGradient>
          </Animated.View>
        )}
        
        {/* Promo Code */}
        {!hasDiscount && (
          <View style={styles.promoContainer}>
            {!showPromoInput ? (
              <TouchableOpacity 
                style={styles.promoToggle}
                onPress={() => setShowPromoInput(true)}
              >
                <Ionicons name="pricetag-outline" size={16} color="#ffffff60" />
                <Text style={styles.promoToggleText}>Have a promo code?</Text>
              </TouchableOpacity>
            ) : (
              <View style={styles.promoInputContainer}>
                <TextInput
                  style={styles.promoInput}
                  placeholder="Enter code..."
                  placeholderTextColor="#ffffff40"
                  value={promoInput}
                  onChangeText={setPromoInput}
                  autoCapitalize="characters"
                  autoCorrect={false}
                />
                <TouchableOpacity 
                  style={[styles.promoApplyButton, promoLoading && { opacity: 0.6 }]}
                  onPress={handleApplyPromo}
                  disabled={promoLoading}
                >
                  {promoLoading ? (
                    <ActivityIndicator color="#ffffff" size="small" />
                  ) : (
                    <Text style={styles.promoApplyText}>Apply</Text>
                  )}
                </TouchableOpacity>
              </View>
            )}
          </View>
        )}

        {/* Pricing Options */}
        <View style={styles.pricingContainer}>
          {/* Lifetime */}
          <TouchableOpacity
            style={[styles.planCard, selectedPlan === 'lifetime' && styles.planCardSelected]}
            onPress={() => {
              setSelectedPlan('lifetime');
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            }}
            activeOpacity={0.8}
          >
            <View style={[styles.bestValueBadge, hasDiscount && styles.discountedBadge]}>
              <Ionicons name={hasDiscount ? "gift" : "star"} size={10} color="#000" />
              <Text style={styles.bestValueText}>{hasDiscount ? `${DISCOUNT_PERCENT}% OFF` : 'BEST VALUE'}</Text>
            </View>
            <Text style={styles.planTitle}>Lifetime</Text>
            <View style={styles.priceRow}>
              {hasDiscount && (
                <Text style={styles.originalPrice}>{REGULAR_PRICE}</Text>
              )}
              <Text style={[styles.price, hasDiscount && styles.discountedPrice]}>{lifetimePrice}</Text>
              <Text style={styles.priceSubtext}>once</Text>
            </View>
            <Text style={styles.planDescription}>Pay once, yours forever</Text>
            {selectedPlan === 'lifetime' && (
              <View style={styles.checkmark}>
                <Ionicons name="checkmark" size={16} color="#ffffff" />
              </View>
            )}
          </TouchableOpacity>

          {/* Monthly */}
          <TouchableOpacity
            style={[styles.planCard, styles.planCardSmall, selectedPlan === 'monthly' && styles.planCardSelected]}
            onPress={() => {
              setSelectedPlan('monthly');
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            }}
            activeOpacity={0.8}
          >
            <Text style={styles.planTitleSmall}>Monthly</Text>
            <Text style={styles.priceSmall}>$0.99</Text>
            <Text style={styles.perMonth}>/month</Text>
            {selectedPlan === 'monthly' && (
              <View style={styles.checkmarkSmall}>
                <Ionicons name="checkmark" size={14} color="#ffffff" />
              </View>
            )}
          </TouchableOpacity>
        </View>

        {/* CTA */}
        <TouchableOpacity
          style={[styles.ctaButton, isLoading && styles.ctaButtonDisabled]}
          onPress={handlePurchase}
          disabled={isLoading}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={['#e94560', '#c23a51']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.ctaGradient}
          >
            {isLoading ? (
              <ActivityIndicator color="#ffffff" size="small" />
            ) : (
              <View style={styles.ctaContent}>
              <Text style={styles.ctaText}>
                {selectedPlan === 'lifetime' ? 'Get Lifetime Access' : 'Start Subscription'}
              </Text>
              <View style={[styles.ctaPriceTag, hasDiscount && selectedPlan === 'lifetime' && { backgroundColor: '#4ade8040' }]}>
                <Text style={styles.ctaPrice}>
                  {selectedPlan === 'lifetime' ? lifetimePrice : '$0.99/mo'}
                </Text>
              </View>
              </View>
            )}
          </LinearGradient>
        </TouchableOpacity>

        {/* Restore */}
        <TouchableOpacity style={styles.restoreButton} onPress={handleRestore} disabled={isLoading}>
          <Ionicons name="refresh" size={16} color="#ffffff60" />
          <Text style={styles.restoreText}>Restore Purchases</Text>
        </TouchableOpacity>

        {/* Continue Free */}
        <TouchableOpacity style={styles.skipButton} onPress={handleContinueFree}>
          <Text style={styles.skipText}>Continue with Ads</Text>
          <Ionicons name="arrow-forward" size={16} color="#ffffff40" />
        </TouchableOpacity>

        {/* Legal - REQUIRED FOR APP STORE */}
        <View style={styles.legalContainer}>
          <Text style={styles.legalText}>
            {selectedPlan === 'monthly' 
              ? 'Subscription automatically renews unless cancelled at least 24 hours before the end of the current period. Payment will be charged to your Apple ID account. '
              : ''
            }
            By continuing, you agree to our{' '}
            <Text style={styles.legalLink}>Terms of Service</Text>
            {' '}and{' '}
            <Text style={styles.legalLink}>Privacy Policy</Text>.
          </Text>
        </View>
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  iconContainer: {
    marginBottom: 20,
  },
  iconGradient: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e9456030',
  },
  title: {
    fontSize: 34,
    fontWeight: '800',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#ffffff60',
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 10,
  },
  featuresContainer: {
    backgroundColor: '#ffffff06',
    borderRadius: 20,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#ffffff08',
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#ffffff08',
  },
  featureIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 2,
  },
  featureDescription: {
    fontSize: 13,
    color: '#ffffff50',
  },
  pricingContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  planCard: {
    flex: 2,
    backgroundColor: '#ffffff08',
    borderRadius: 18,
    padding: 20,
    borderWidth: 2,
    borderColor: 'transparent',
    position: 'relative',
  },
  planCardSmall: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  planCardSelected: {
    borderColor: '#e94560',
    backgroundColor: '#e9456012',
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    left: 16,
    backgroundColor: '#4ade80',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  bestValueText: {
    color: '#000000',
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  planTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 8,
    marginTop: 8,
  },
  planTitleSmall: {
    fontSize: 14,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 4,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 4,
  },
  price: {
    fontSize: 32,
    fontWeight: '800',
    color: '#e94560',
  },
  priceSubtext: {
    fontSize: 14,
    color: '#ffffff60',
    marginLeft: 4,
  },
  priceSmall: {
    fontSize: 22,
    fontWeight: '800',
    color: '#e94560',
  },
  perMonth: {
    fontSize: 12,
    color: '#ffffff50',
    marginTop: 2,
  },
  planDescription: {
    fontSize: 13,
    color: '#ffffff50',
  },
  checkmark: {
    position: 'absolute',
    top: 12,
    right: 12,
    width: 26,
    height: 26,
    borderRadius: 13,
    backgroundColor: '#e94560',
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmarkSmall: {
    position: 'absolute',
    top: 8,
    right: 8,
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: '#e94560',
    justifyContent: 'center',
    alignItems: 'center',
  },
  ctaButton: {
    borderRadius: 18,
    overflow: 'hidden',
    marginBottom: 16,
  },
  ctaButtonDisabled: {
    opacity: 0.7,
  },
  ctaGradient: {
    paddingVertical: 20,
    alignItems: 'center',
  },
  ctaContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  ctaText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '700',
  },
  ctaPriceTag: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  ctaPrice: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '700',
  },
  discountBanner: {
    borderRadius: 14,
    overflow: 'hidden',
    marginBottom: 20,
  },
  discountGradient: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 12,
    gap: 8,
  },
  discountText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  discountedBadge: {
    backgroundColor: '#4ade80',
  },
  originalPrice: {
    fontSize: 18,
    color: '#ffffff40',
    textDecorationLine: 'line-through',
    marginRight: 8,
  },
  discountedPrice: {
    color: '#4ade80',
  },
  restoreButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 14,
    gap: 8,
    marginBottom: 8,
  },
  restoreText: {
    color: '#ffffff60',
    fontSize: 15,
    fontWeight: '600',
  },
  skipButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 14,
    gap: 6,
    marginBottom: 20,
  },
  skipText: {
    color: '#ffffff40',
    fontSize: 15,
  },
  legalContainer: {
    paddingHorizontal: 16,
  },
  legalText: {
    fontSize: 11,
    color: '#ffffff30',
    textAlign: 'center',
    lineHeight: 16,
  },
  legalLink: {
    textDecorationLine: 'underline',
  },
  promoContainer: {
    marginBottom: 20,
  },
  promoToggle: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 8,
  },
  promoToggleText: {
    color: '#ffffff60',
    fontSize: 14,
  },
  promoInputContainer: {
    flexDirection: 'row',
    gap: 10,
  },
  promoInput: {
    flex: 1,
    backgroundColor: '#ffffff10',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '600',
    letterSpacing: 1,
  },
  promoApplyButton: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    paddingHorizontal: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  promoApplyText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '700',
  },
});
