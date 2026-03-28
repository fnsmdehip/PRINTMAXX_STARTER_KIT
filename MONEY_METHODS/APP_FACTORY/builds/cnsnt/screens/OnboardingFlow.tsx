/**
 * cnsnt - Cal AI-Style Onboarding Flow (12 screens)
 *
 * 1. Welcome - "Secure Consent Management for Professionals"
 * 2. Use Case - "What will you use cnsnt for?"
 * 3. Industry - "What's your field?"
 * 4. Volume - "How many agreements do you handle monthly?"
 * 5. Pain Point - "What's your biggest challenge?"
 * 6. Validation - Personalized projection (time savings, volume)
 * 7. Feature Showcase - Digital signatures, encryption, templates, audit trail, PDF
 * 8. Security - "Bank-grade encryption" highlight
 * 9. Social Proof - "Trusted by 5,000+ professionals" with testimonials
 * 10. Notification Permission - "Get notified when agreements are signed"
 * 11. Plan Ready - "Your secure vault is ready!" personalized summary
 * 12. PAYWALL - Hard paywall with trial timeline, rescue offer
 *
 * Animated transitions, progress bar, back button, AsyncStorage persistence.
 * Uses existing theme system + purchaseService from services/purchases.
 */

import React, { useState, useRef, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Animated,
  Dimensions,
  ScrollView,
  Alert,
  Platform,
  ActivityIndicator,
  Image,
} from 'react-native';
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Real visual assets
const ASSETS = {
  logo: require('../assets/logo_fullcolor.png'),
  logoText: require('../assets/logo_text.png'),
  shield: require('../assets/icon_shield.png'),
  signature: require('../assets/icon_signature.png'),
  cloudLock: require('../assets/icon_cloud_lock.png'),
  checklist: require('../assets/icon_checklist.png'),
  pdf: require('../assets/icon_pdf.png'),
  video: require('../assets/icon_video.png'),
  splash: require('../assets/splash_showcase.png'),
  bgPaper: require('../assets/bg_paper_texture.png'),
};
import purchaseService from '../services/purchases';
import {
  Colors,
  Typography,
  Spacing,
  BorderRadius,
  Shadows,
  MIN_TOUCH_SIZE,
} from '../constants/theme';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const TOTAL_STEPS = 12;

const ONBOARDING_ANSWERS_KEY = 'cnsnt_onboarding_answers';

// ─── OPTION DATA ─────────────────────────────────────────────

const USE_CASE_OPTIONS = [
  { id: 'intimate', label: 'Intimate Consent Agreements', icon: 'heart-outline' as const, emoji: '' },
  { id: 'guest_event', label: 'Guest & Event Liability Waivers', icon: 'home-outline' as const, emoji: '' },
  { id: 'ndas', label: 'NDAs & Confidentiality', icon: 'lock-closed-outline' as const, emoji: '' },
  { id: 'service', label: 'Service & Freelance Agreements', icon: 'briefcase-outline' as const, emoji: '' },
  { id: 'property', label: 'Property & Vehicle Agreements', icon: 'car-outline' as const, emoji: '' },
  { id: 'media', label: 'Photo/Video Releases', icon: 'camera-outline' as const, emoji: '' },
];

const INDUSTRY_OPTIONS = [
  { id: 'legal', label: 'Legal', icon: 'scales-outline' as const },
  { id: 'healthcare', label: 'Healthcare', icon: 'medkit-outline' as const },
  { id: 'realestate', label: 'Real Estate', icon: 'home-outline' as const },
  { id: 'photography', label: 'Photography', icon: 'camera-outline' as const },
  { id: 'fitness', label: 'Fitness', icon: 'barbell-outline' as const },
  { id: 'events', label: 'Events', icon: 'people-outline' as const },
  { id: 'consulting', label: 'Consulting', icon: 'chatbubbles-outline' as const },
  { id: 'other', label: 'Other', icon: 'ellipsis-horizontal-outline' as const },
];

const VOLUME_OPTIONS = [
  { id: '1-5', label: '1-5', subtitle: 'Just getting started' },
  { id: '5-20', label: '5-20', subtitle: 'Growing practice' },
  { id: '20-50', label: '20-50', subtitle: 'Established business' },
  { id: '50+', label: '50+', subtitle: 'High volume' },
];

const PAIN_POINT_OPTIONS = [
  { id: 'slow', label: 'Paper forms are slow', icon: 'time-outline' as const },
  { id: 'lost', label: "Can't find old agreements", icon: 'search-outline' as const },
  { id: 'proof', label: 'No proof of consent', icon: 'shield-outline' as const },
  { id: 'digital', label: "Clients won't sign digitally", icon: 'phone-portrait-outline' as const },
  { id: 'compliance', label: 'Compliance concerns', icon: 'checkmark-circle-outline' as const },
];

const FEATURES_LIST = [
  { icon: 'create-outline' as const, title: 'Digital Signatures', desc: 'Capture legally-binding e-signatures on any device' },
  { icon: 'lock-closed-outline' as const, title: 'Encrypted Storage', desc: 'AES-256 encryption protects every document' },
  { icon: 'documents-outline' as const, title: '12+ Professional Templates', desc: 'Consent, NDAs, waivers, releases, agreements -- ready to sign' },
  { icon: 'trail-sign-outline' as const, title: 'Audit Trail', desc: 'SHA-256 tamper-proof verification for every record' },
  { icon: 'download-outline' as const, title: 'Export to PDF', desc: 'Generate court-ready PDFs with one tap' },
];

const SECURITY_FEATURES = [
  { icon: 'shield-checkmark-outline' as const, title: 'AES-256 Encryption', desc: 'Same standard used by banks and government agencies' },
  { icon: 'finger-print-outline' as const, title: 'Biometric Lock', desc: 'Face ID / Touch ID protects your vault' },
  { icon: 'checkmark-done-outline' as const, title: 'SHA-256 Verification', desc: 'Tamper-proof hashing proves document integrity' },
  { icon: 'cloud-offline-outline' as const, title: 'Local-First Storage', desc: 'Your data stays on your device by default' },
];

const TESTIMONIALS = [
  { name: 'Sarah M.', role: 'Family Lawyer', text: 'Replaced my entire paper filing system. Clients love signing on the iPad.', stars: 5 },
  { name: 'Dr. James K.', role: 'Physical Therapist', text: 'Patient intake went from 15 minutes to 2. Game changer for my practice.', stars: 5 },
  { name: 'Lisa T.', role: 'Event Coordinator', text: 'Managing 200+ waivers per event was a nightmare. Now it takes minutes.', stars: 5 },
];

// ─── TIME SAVINGS CALCULATIONS ─────────────────────────────────

function getTimeSavings(volume: string): { hours: number; perAgreement: number } {
  const map: Record<string, { hours: number; perAgreement: number }> = {
    '1-5': { hours: 2, perAgreement: 25 },
    '5-20': { hours: 6, perAgreement: 20 },
    '20-50': { hours: 14, perAgreement: 18 },
    '50+': { hours: 30, perAgreement: 15 },
  };
  return map[volume] || map['5-20'];
}

function getIndustryLabel(id: string): string {
  const found = INDUSTRY_OPTIONS.find((o) => o.id === id);
  return found ? found.label : 'your';
}

function getUseCaseLabel(id: string): string {
  const found = USE_CASE_OPTIONS.find((o) => o.id === id);
  return found ? found.label.toLowerCase() : 'agreements';
}

function getVolumeLabel(id: string): string {
  return id === '50+' ? '50+' : id;
}

// ─── INTERFACES ─────────────────────────────────────────────

interface OnboardingAnswers {
  useCase: string;
  industry: string;
  volume: string;
  painPoint: string;
}

interface OnboardingFlowProps {
  onComplete: () => void;
}

// ─── MAIN COMPONENT ─────────────────────────────────────────

const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete }) => {
  const insets = useSafeAreaInsets();
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<OnboardingAnswers>({
    useCase: '',
    industry: '',
    volume: '',
    painPoint: '',
  });
  const [selectedPlan, setSelectedPlan] = useState<'yearly' | 'monthly'>('yearly');
  const [purchasing, setPurchasing] = useState(false);
  const [showRescue, setShowRescue] = useState(false);
  const [restoring, setRestoring] = useState(false);

  const fadeAnim = useRef(new Animated.Value(1)).current;
  const slideAnim = useRef(new Animated.Value(0)).current;
  const progressAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Pulse animation for CTA buttons
  useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.03, duration: 1200, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1200, useNativeDriver: true }),
      ])
    );
    pulse.start();
    return () => pulse.stop();
  }, [pulseAnim]);

  // Progress bar animation
  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: (step + 1) / TOTAL_STEPS,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [step, progressAnim]);

  const animateTransition = useCallback(
    (nextStep: number) => {
      const goingForward = nextStep > step;
      Animated.parallel([
        Animated.timing(fadeAnim, { toValue: 0, duration: 120, useNativeDriver: true }),
        Animated.timing(slideAnim, { toValue: goingForward ? -40 : 40, duration: 120, useNativeDriver: true }),
      ]).start(() => {
        setStep(nextStep);
        slideAnim.setValue(goingForward ? 40 : -40);
        Animated.parallel([
          Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true }),
          Animated.spring(slideAnim, { toValue: 0, damping: 20, stiffness: 200, useNativeDriver: true }),
        ]).start();
      });
    },
    [step, fadeAnim, slideAnim]
  );

  const goNext = useCallback(() => {
    if (step < TOTAL_STEPS - 1) {
      animateTransition(step + 1);
    }
  }, [step, animateTransition]);

  const goBack = useCallback(() => {
    if (step > 0) {
      setShowRescue(false);
      animateTransition(step - 1);
    }
  }, [step, animateTransition]);

  const setAnswer = useCallback(
    (key: keyof OnboardingAnswers, value: string) => {
      setAnswers((prev) => ({ ...prev, [key]: value }));
    },
    []
  );

  const saveAnswers = useCallback(async () => {
    await AsyncStorage.setItem(ONBOARDING_ANSWERS_KEY, JSON.stringify(answers));
  }, [answers]);

  const handlePurchase = useCallback(
    async (plan: 'monthly' | 'yearly') => {
      setPurchasing(true);
      try {
        await saveAnswers();
        const success = await purchaseService.purchasePackage(plan);
        if (success) {
          onComplete();
        }
      } catch (e) {
        Alert.alert('Purchase Error', 'Something went wrong. Please try again.');
      } finally {
        setPurchasing(false);
      }
    },
    [saveAnswers, onComplete]
  );

  const handleRescuePurchase = useCallback(async () => {
    setPurchasing(true);
    try {
      await saveAnswers();
      const success = await purchaseService.purchasePackage('yearly');
      if (success) {
        onComplete();
      }
    } catch (e) {
      Alert.alert('Purchase Error', 'Something went wrong. Please try again.');
    } finally {
      setPurchasing(false);
    }
  }, [saveAnswers, onComplete]);

  const handleDeclinePaywall = useCallback(() => {
    if (!showRescue) {
      setShowRescue(true);
    } else {
      // User declined rescue too -- let them in with free tier
      saveAnswers().then(() => onComplete());
    }
  }, [showRescue, saveAnswers, onComplete]);

  const handleRestore = useCallback(async () => {
    setRestoring(true);
    try {
      const result = await purchaseService.restorePurchases();
      if (result === 'pro') {
        await saveAnswers();
        onComplete();
      }
    } finally {
      setRestoring(false);
    }
  }, [saveAnswers, onComplete]);

  const handleNotificationPermission = useCallback(async () => {
    // On iOS, this would call Notifications.requestPermissionsAsync()
    // For now, advance -- permission request is handled at OS level
    goNext();
  }, [goNext]);

  // ─── SCREEN RENDERERS ─────────────────────────────────────

  // SCREEN 1: Welcome
  const renderWelcome = () => (
    <View style={s.screenCenter}>
      <View style={s.welcomeIconContainer}>
        <Image source={ASSETS.logo} style={{ width: 120, height: 120, marginBottom: 8 }} resizeMode="contain" />
        <Image source={ASSETS.logoText} style={{ width: 160, height: 40 }} resizeMode="contain" />
      </View>
      <Text style={s.welcomeTitle}>Secure Consent{'\n'}Management</Text>
      <Text style={s.welcomeSubtitle}>for Professionals</Text>
      <Text style={s.welcomeDesc}>
        Create, sign, and store digital agreements with bank-grade encryption
        and tamper-proof verification.
      </Text>
      <View style={s.welcomeBadgeRow}>
        <View style={s.welcomeBadge}>
          <Ionicons name="lock-closed" size={14} color={Colors.primary} />
          <Text style={s.welcomeBadgeText}>AES-256</Text>
        </View>
        <View style={s.welcomeBadge}>
          <Ionicons name="checkmark-circle" size={14} color={Colors.success} />
          <Text style={s.welcomeBadgeText}>HIPAA Ready</Text>
        </View>
        <View style={s.welcomeBadge}>
          <Ionicons name="document-text" size={14} color={Colors.primary} />
          <Text style={s.welcomeBadgeText}>PDF Export</Text>
        </View>
      </View>
      <Animated.View style={{ transform: [{ scale: pulseAnim }], width: '100%' }}>
        <Pressable style={s.primaryButton} onPress={goNext}>
          <Text style={s.primaryButtonText}>Get Started</Text>
          <Ionicons name="arrow-forward" size={20} color="#FFF" />
        </Pressable>
      </Animated.View>
    </View>
  );

  // SCREEN 2: Use Case
  const renderUseCase = () => (
    <View style={s.screenTop}>
      <Text style={s.questionTitle}>What will you use{'\n'}cnsnt for?</Text>
      <Text style={s.questionSubtitle}>Select your primary use case</Text>
      <View style={s.optionGrid}>
        {USE_CASE_OPTIONS.map((opt) => (
          <Pressable
            key={opt.id}
            style={[s.optionCard, answers.useCase === opt.id && s.optionCardSelected]}
            onPress={() => {
              setAnswer('useCase', opt.id);
              setTimeout(goNext, 300);
            }}
          >
            <Ionicons
              name={opt.icon}
              size={28}
              color={answers.useCase === opt.id ? Colors.primary : Colors.textSecondary}
            />
            <Text style={[s.optionLabel, answers.useCase === opt.id && s.optionLabelSelected]}>
              {opt.label}
            </Text>
          </Pressable>
        ))}
      </View>
    </View>
  );

  // SCREEN 3: Industry
  const renderIndustry = () => (
    <View style={s.screenTop}>
      <Text style={s.questionTitle}>What's your field?</Text>
      <Text style={s.questionSubtitle}>We'll customize templates for your industry</Text>
      <View style={s.optionGrid}>
        {INDUSTRY_OPTIONS.map((opt) => (
          <Pressable
            key={opt.id}
            style={[s.optionCard, answers.industry === opt.id && s.optionCardSelected]}
            onPress={() => {
              setAnswer('industry', opt.id);
              setTimeout(goNext, 300);
            }}
          >
            <Ionicons
              name={opt.icon}
              size={28}
              color={answers.industry === opt.id ? Colors.primary : Colors.textSecondary}
            />
            <Text style={[s.optionLabel, answers.industry === opt.id && s.optionLabelSelected]}>
              {opt.label}
            </Text>
          </Pressable>
        ))}
      </View>
    </View>
  );

  // SCREEN 4: Volume
  const renderVolume = () => (
    <View style={s.screenTop}>
      <Text style={s.questionTitle}>How many agreements{'\n'}do you handle monthly?</Text>
      <Text style={s.questionSubtitle}>This helps us optimize your experience</Text>
      <View style={s.volumeList}>
        {VOLUME_OPTIONS.map((opt) => (
          <Pressable
            key={opt.id}
            style={[s.volumeCard, answers.volume === opt.id && s.volumeCardSelected]}
            onPress={() => {
              setAnswer('volume', opt.id);
              setTimeout(goNext, 300);
            }}
          >
            <View style={s.volumeLeft}>
              <Text style={[s.volumeNumber, answers.volume === opt.id && s.volumeNumberSelected]}>
                {opt.label}
              </Text>
              <Text style={[s.volumeSubtitle, answers.volume === opt.id && s.volumeSubtitleSelected]}>
                {opt.subtitle}
              </Text>
            </View>
            <View style={[s.radioOuter, answers.volume === opt.id && s.radioOuterSelected]}>
              {answers.volume === opt.id && <View style={s.radioInner} />}
            </View>
          </Pressable>
        ))}
      </View>
    </View>
  );

  // SCREEN 5: Pain Point
  const renderPainPoint = () => (
    <View style={s.screenTop}>
      <Text style={s.questionTitle}>What's your biggest{'\n'}challenge right now?</Text>
      <Text style={s.questionSubtitle}>We'll show you how cnsnt solves it</Text>
      <View style={s.painList}>
        {PAIN_POINT_OPTIONS.map((opt) => (
          <Pressable
            key={opt.id}
            style={[s.painCard, answers.painPoint === opt.id && s.painCardSelected]}
            onPress={() => {
              setAnswer('painPoint', opt.id);
              setTimeout(goNext, 300);
            }}
          >
            <View style={[s.painIconBg, answers.painPoint === opt.id && s.painIconBgSelected]}>
              <Ionicons
                name={opt.icon}
                size={22}
                color={answers.painPoint === opt.id ? '#FFF' : Colors.primary}
              />
            </View>
            <Text style={[s.painLabel, answers.painPoint === opt.id && s.painLabelSelected]}>
              {opt.label}
            </Text>
            <Ionicons
              name={answers.painPoint === opt.id ? 'checkmark-circle' : 'chevron-forward'}
              size={20}
              color={answers.painPoint === opt.id ? Colors.primary : Colors.textTertiary}
            />
          </Pressable>
        ))}
      </View>
    </View>
  );

  // SCREEN 6: Validation
  const renderValidation = () => {
    const savings = getTimeSavings(answers.volume || '5-20');
    const industryName = getIndustryLabel(answers.industry || 'consulting');
    const volumeLabel = getVolumeLabel(answers.volume || '5-20');

    return (
      <View style={s.screenCenter}>
        <View style={s.validationIconContainer}>
          <Ionicons name="checkmark-circle" size={72} color={Colors.success} />
        </View>
        <Text style={s.validationTitle}>Great fit.</Text>
        <Text style={s.validationDesc}>
          cnsnt handles {volumeLabel} agreements/month for{' '}
          {industryName.toLowerCase()} professionals like you.
        </Text>

        <View style={s.projectionCard}>
          <View style={s.projectionRow}>
            <View style={s.projectionItem}>
              <Text style={s.projectionNumber}>~{savings.hours}h</Text>
              <Text style={s.projectionLabel}>saved per month</Text>
            </View>
            <View style={s.projectionDivider} />
            <View style={s.projectionItem}>
              <Text style={s.projectionNumber}>{savings.perAgreement}min</Text>
              <Text style={s.projectionLabel}>per agreement</Text>
            </View>
          </View>
          <View style={s.projectionFooter}>
            <Ionicons name="trending-down" size={16} color={Colors.success} />
            <Text style={s.projectionFooterText}>
              vs 30+ min average with paper forms
            </Text>
          </View>
        </View>

        <Pressable style={s.primaryButton} onPress={goNext}>
          <Text style={s.primaryButtonText}>See How It Works</Text>
          <Ionicons name="arrow-forward" size={20} color="#FFF" />
        </Pressable>
      </View>
    );
  };

  // SCREEN 7: Feature Showcase
  const renderFeatures = () => (
    <View style={s.screenTop}>
      <Text style={s.questionTitle}>Everything you need{'\n'}in one vault</Text>
      <Text style={s.questionSubtitle}>Built for professionals who value security</Text>
      <ScrollView style={s.featureScroll} showsVerticalScrollIndicator={false}>
        {FEATURES_LIST.map((feat, i) => (
          <View key={i} style={s.featureCard}>
            <View style={s.featureIconBg}>
              <Ionicons name={feat.icon} size={24} color={Colors.primary} />
            </View>
            <View style={s.featureContent}>
              <Text style={s.featureTitle}>{feat.title}</Text>
              <Text style={s.featureDesc}>{feat.desc}</Text>
            </View>
          </View>
        ))}
        <View style={{ height: 100 }} />
      </ScrollView>
      <View style={s.stickyBottom}>
        <Pressable style={s.primaryButton} onPress={goNext}>
          <Text style={s.primaryButtonText}>Continue</Text>
          <Ionicons name="arrow-forward" size={20} color="#FFF" />
        </Pressable>
      </View>
    </View>
  );

  // SCREEN 8: Security
  const renderSecurity = () => (
    <View style={s.screenTop}>
      <View style={s.securityHeader}>
        <View style={s.securityShieldBg}>
          <Ionicons name="shield-checkmark" size={48} color={Colors.primary} />
        </View>
        <Text style={s.securityTitle}>Bank-Grade{'\n'}Security</Text>
        <Text style={s.questionSubtitle}>
          Your consent records deserve the highest protection
        </Text>
      </View>
      <View style={s.securityList}>
        {SECURITY_FEATURES.map((feat, i) => (
          <View key={i} style={s.securityCard}>
            <View style={s.securityCardIcon}>
              <Ionicons name={feat.icon} size={22} color={Colors.primary} />
            </View>
            <View style={s.securityCardContent}>
              <Text style={s.securityCardTitle}>{feat.title}</Text>
              <Text style={s.securityCardDesc}>{feat.desc}</Text>
            </View>
          </View>
        ))}
      </View>
      <Pressable style={s.primaryButton} onPress={goNext}>
        <Text style={s.primaryButtonText}>Continue</Text>
        <Ionicons name="arrow-forward" size={20} color="#FFF" />
      </Pressable>
    </View>
  );

  // SCREEN 9: Social Proof
  const renderSocialProof = () => (
    <View style={s.screenTop}>
      <View style={s.socialHeader}>
        <Text style={s.socialBigNumber}>5,000+</Text>
        <Text style={s.socialBigLabel}>professionals trust cnsnt</Text>
      </View>
      <View style={s.starsRow}>
        {[1, 2, 3, 4, 5].map((i) => (
          <Ionicons key={i} name="star" size={24} color="#F59E0B" />
        ))}
        <Text style={s.starsText}>4.8 average rating</Text>
      </View>
      <View style={s.testimonialList}>
        {TESTIMONIALS.map((t, i) => (
          <View key={i} style={s.testimonialCard}>
            <View style={s.testimonialHeader}>
              <View style={s.testimonialAvatar}>
                <Text style={s.testimonialAvatarText}>{t.name[0]}</Text>
              </View>
              <View>
                <Text style={s.testimonialName}>{t.name}</Text>
                <Text style={s.testimonialRole}>{t.role}</Text>
              </View>
            </View>
            <Text style={s.testimonialText}>"{t.text}"</Text>
            <View style={s.testimonialStars}>
              {Array.from({ length: t.stars }).map((_, j) => (
                <Ionicons key={j} name="star" size={14} color="#F59E0B" />
              ))}
            </View>
          </View>
        ))}
      </View>
      <Pressable style={s.primaryButton} onPress={goNext}>
        <Text style={s.primaryButtonText}>Continue</Text>
        <Ionicons name="arrow-forward" size={20} color="#FFF" />
      </Pressable>
    </View>
  );

  // SCREEN 10: Notification Permission
  const renderNotifications = () => (
    <View style={s.screenCenter}>
      <View style={s.notifIconContainer}>
        <View style={s.notifBell}>
          <Ionicons name="notifications" size={56} color={Colors.primary} />
        </View>
        <View style={s.notifBadge}>
          <Text style={s.notifBadgeText}>1</Text>
        </View>
      </View>
      <Text style={s.notifTitle}>Never miss a{'\n'}signed agreement</Text>
      <Text style={s.notifDesc}>
        Get instant notifications when clients sign your documents, when
        agreements expire, and when action is needed.
      </Text>
      <View style={s.notifExamples}>
        <View style={s.notifExample}>
          <Ionicons name="checkmark-circle" size={18} color={Colors.success} />
          <Text style={s.notifExampleText}>Agreement signed by client</Text>
        </View>
        <View style={s.notifExample}>
          <Ionicons name="time" size={18} color={Colors.warning} />
          <Text style={s.notifExampleText}>Agreement expiring in 7 days</Text>
        </View>
        <View style={s.notifExample}>
          <Ionicons name="document" size={18} color={Colors.primary} />
          <Text style={s.notifExampleText}>New template available</Text>
        </View>
      </View>
      <Pressable style={s.primaryButton} onPress={handleNotificationPermission}>
        <Ionicons name="notifications-outline" size={20} color="#FFF" />
        <Text style={s.primaryButtonText}>Enable Notifications</Text>
      </Pressable>
      <Pressable style={s.textButton} onPress={goNext}>
        <Text style={s.textButtonText}>Maybe later</Text>
      </Pressable>
    </View>
  );

  // SCREEN 11: Plan Ready
  const renderPlanReady = () => {
    const industryName = getIndustryLabel(answers.industry || 'consulting');
    const useCaseName = getUseCaseLabel(answers.useCase || 'business');
    const savings = getTimeSavings(answers.volume || '5-20');

    return (
      <View style={s.screenCenter}>
        <View style={s.readyIconContainer}>
          <Ionicons name="checkmark-done-circle" size={80} color={Colors.success} />
        </View>
        <Text style={s.readyTitle}>Your secure vault{'\n'}is ready!</Text>
        <View style={s.readySummaryCard}>
          <View style={s.readySummaryRow}>
            <Ionicons name="briefcase-outline" size={18} color={Colors.primary} />
            <Text style={s.readySummaryText}>{industryName} industry</Text>
          </View>
          <View style={s.readySummaryRow}>
            <Ionicons name="document-text-outline" size={18} color={Colors.primary} />
            <Text style={s.readySummaryText}>Optimized for {useCaseName}</Text>
          </View>
          <View style={s.readySummaryRow}>
            <Ionicons name="speedometer-outline" size={18} color={Colors.primary} />
            <Text style={s.readySummaryText}>~{savings.hours}h/month time savings</Text>
          </View>
          <View style={s.readySummaryRow}>
            <Ionicons name="shield-checkmark-outline" size={18} color={Colors.primary} />
            <Text style={s.readySummaryText}>Bank-grade encryption included</Text>
          </View>
          <View style={s.readySummaryRow}>
            <Ionicons name="documents-outline" size={18} color={Colors.primary} />
            <Text style={s.readySummaryText}>Industry templates preloaded</Text>
          </View>
        </View>
        <Animated.View style={{ transform: [{ scale: pulseAnim }], width: '100%' }}>
          <Pressable style={s.primaryButton} onPress={goNext}>
            <Text style={s.primaryButtonText}>Activate My Vault</Text>
            <Ionicons name="arrow-forward" size={20} color="#FFF" />
          </Pressable>
        </Animated.View>
      </View>
    );
  };

  // SCREEN 12: PAYWALL
  const renderPaywall = () => {
    if (showRescue) {
      return renderRescueOffer();
    }

    return (
      <ScrollView
        style={s.paywallScroll}
        contentContainerStyle={s.paywallScrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Trial Timeline */}
        <View style={s.trialTimeline}>
          <View style={s.timelineStep}>
            <View style={[s.timelineDot, s.timelineDotActive]}>
              <Ionicons name="lock-open" size={16} color="#FFF" />
            </View>
            <Text style={s.timelineLabel}>Today</Text>
            <Text style={s.timelineDesc}>Full access free</Text>
          </View>
          <View style={s.timelineLine} />
          <View style={s.timelineStep}>
            <View style={[s.timelineDot, s.timelineDotMid]}>
              <Ionicons name="notifications-outline" size={16} color={Colors.primary} />
            </View>
            <Text style={s.timelineLabel}>Day 2</Text>
            <Text style={s.timelineDesc}>Reminder</Text>
          </View>
          <View style={s.timelineLine} />
          <View style={s.timelineStep}>
            <View style={[s.timelineDot, s.timelineDotEnd]}>
              <Ionicons name="card-outline" size={16} color={Colors.textSecondary} />
            </View>
            <Text style={s.timelineLabel}>Day 3</Text>
            <Text style={s.timelineDesc}>Billing starts</Text>
          </View>
        </View>

        <Text style={s.paywallNoPay}>No payment due now</Text>

        {/* Free tier note */}
        <View style={s.freeTierNote}>
          <Ionicons name="information-circle-outline" size={16} color={Colors.textSecondary} />
          <Text style={s.freeTierNoteText}>Free: 3 records total, text-only, basic templates</Text>
        </View>

        {/* Plan Cards */}
        <View style={s.planCards}>
          {/* Monthly (anchor) */}
          <Pressable
            style={[s.planCard, selectedPlan === 'monthly' && s.planCardSelected]}
            onPress={() => setSelectedPlan('monthly')}
          >
            <View style={s.planRadioRow}>
              <View style={[s.radioOuter, selectedPlan === 'monthly' && s.radioOuterSelected]}>
                {selectedPlan === 'monthly' && <View style={s.radioInner} />}
              </View>
              <Text style={s.planName}>Monthly</Text>
            </View>
            <Text style={s.planPrice}>$4.99<Text style={s.planPricePer}>/mo</Text></Text>
          </Pressable>

          {/* Yearly (highlighted) */}
          <Pressable
            style={[s.planCard, s.planCardYearly, selectedPlan === 'yearly' && s.planCardSelected]}
            onPress={() => setSelectedPlan('yearly')}
          >
            <View style={s.bestValueBadge}>
              <Text style={s.bestValueText}>BEST VALUE</Text>
            </View>
            <View style={s.planRadioRow}>
              <View style={[s.radioOuter, selectedPlan === 'yearly' && s.radioOuterSelected]}>
                {selectedPlan === 'yearly' && <View style={s.radioInner} />}
              </View>
              <Text style={s.planName}>Yearly</Text>
              <View style={s.saveBadge}>
                <Text style={s.saveBadgeText}>Save 69%</Text>
              </View>
            </View>
            <Text style={s.planPrice}>
              $29.99<Text style={s.planPricePer}>/yr</Text>
            </Text>
            <Text style={s.planPriceMonthly}>$2.50/mo</Text>
          </Pressable>
        </View>

        {/* Benefits */}
        <View style={s.benefitsList}>
          {[
            { icon: 'infinite-outline' as const, text: 'Unlimited consent records' },
            { icon: 'videocam-outline' as const, text: 'VIDEO consent recording (GPS + timestamp)' },
            { icon: 'documents-outline' as const, text: 'All 11+ premium templates' },
            { icon: 'download-outline' as const, text: 'PDF export with digital signatures' },
            { icon: 'analytics-outline' as const, text: 'Audit trail export' },
            { icon: 'color-palette-outline' as const, text: 'Custom agreement branding' },
          ].map((b, i) => (
            <View key={i} style={s.benefitRow}>
              <Ionicons name={b.icon} size={18} color={Colors.success} />
              <Text style={s.benefitText}>{b.text}</Text>
            </View>
          ))}
        </View>

        {/* CTA */}
        <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
          <Pressable
            style={[s.ctaButton, purchasing && s.ctaButtonDisabled]}
            onPress={() => handlePurchase(selectedPlan)}
            disabled={purchasing}
          >
            {purchasing ? (
              <ActivityIndicator color="#FFF" />
            ) : (
              <Text style={s.ctaButtonText}>Start My Free Trial</Text>
            )}
          </Pressable>
        </Animated.View>

        <Text style={s.cancelText}>Subscription automatically renews unless canceled at least 24 hours before the end of the current period. Manage subscriptions in your Apple ID account settings. Cancel anytime.</Text>

        {/* Social proof */}
        <View style={s.paywallSocial}>
          <View style={s.paywallStars}>
            {[1, 2, 3, 4, 5].map((i) => (
              <Ionicons key={i} name="star" size={14} color="#F59E0B" />
            ))}
          </View>
          <Text style={s.paywallSocialText}>4.8 stars | 5,000+ professionals</Text>
        </View>

        {/* Restore */}
        <Pressable style={s.restoreButton} onPress={handleRestore} disabled={restoring}>
          <Text style={s.restoreText}>
            {restoring ? 'Restoring...' : 'Restore Purchase'}
          </Text>
        </Pressable>
      </ScrollView>
    );
  };

  // RESCUE OFFER (shown when user declines paywall)
  const renderRescueOffer = () => (
    <View style={s.screenCenter}>
      <View style={s.rescueIconBg}>
        <Ionicons name="gift-outline" size={56} color={Colors.primary} />
      </View>
      <Text style={s.rescueTitle}>Wait! Special offer{'\n'}just for you</Text>
      <Text style={s.rescueDesc}>
        Get cnsnt Pro for an entire year at our lowest price ever.
      </Text>

      <View style={s.rescueCard}>
        <Text style={s.rescuePriceStrike}>$29.99/yr</Text>
        <Text style={s.rescuePrice}>$19.99<Text style={s.rescuePricePer}>/yr</Text></Text>
        <Text style={s.rescuePriceMonthly}>Just $1.67/mo</Text>
        <View style={s.rescueSaveBadge}>
          <Text style={s.rescueSaveBadgeText}>SAVE 79%</Text>
        </View>
      </View>

      <View style={s.benefitsList}>
        {[
          { icon: 'infinite-outline' as const, text: 'Unlimited consent records' },
          { icon: 'videocam-outline' as const, text: 'VIDEO consent recording' },
          { icon: 'documents-outline' as const, text: 'All 11+ premium templates' },
          { icon: 'download-outline' as const, text: 'PDF export with signatures' },
        ].map((b, i) => (
          <View key={i} style={s.benefitRow}>
            <Ionicons name={b.icon} size={18} color={Colors.success} />
            <Text style={s.benefitText}>{b.text}</Text>
          </View>
        ))}
      </View>

      <Animated.View style={{ transform: [{ scale: pulseAnim }], width: '100%' }}>
        <Pressable
          style={[s.ctaButton, purchasing && s.ctaButtonDisabled]}
          onPress={handleRescuePurchase}
          disabled={purchasing}
        >
          {purchasing ? (
            <ActivityIndicator color="#FFF" />
          ) : (
            <Text style={s.ctaButtonText}>Claim This Deal</Text>
          )}
        </Pressable>
      </Animated.View>

      <Pressable style={s.textButton} onPress={() => { saveAnswers().then(() => onComplete()); }}>
        <Text style={s.textButtonText}>No thanks, continue with free tier</Text>
      </Pressable>
    </View>
  );

  // ─── SCREEN ROUTER ─────────────────────────────────────────

  const renderCurrentScreen = () => {
    switch (step) {
      case 0: return renderWelcome();
      case 1: return renderUseCase();
      case 2: return renderIndustry();
      case 3: return renderVolume();
      case 4: return renderPainPoint();
      case 5: return renderValidation();
      case 6: return renderFeatures();
      case 7: return renderSecurity();
      case 8: return renderSocialProof();
      case 9: return renderNotifications();
      case 10: return renderPlanReady();
      case 11: return renderPaywall();
      default: return renderWelcome();
    }
  };

  // ─── RENDER ─────────────────────────────────────────────────

  return (
    <SafeAreaView style={s.container}>
      {/* Progress bar */}
      <View style={[s.progressContainer, { marginTop: 4 }]}>
        {step > 0 && step < TOTAL_STEPS - 1 && (
          <Pressable
            style={s.backButton}
            onPress={goBack}
            hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
          >
            <Ionicons name="chevron-back" size={24} color={Colors.textPrimary} />
          </Pressable>
        )}
        <View style={s.progressBarBg}>
          <Animated.View
            style={[
              s.progressBarFill,
              {
                width: progressAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: ['0%', '100%'],
                }),
              },
            ]}
          />
        </View>
        {step === TOTAL_STEPS - 1 && !showRescue && (
          <Pressable
            style={s.closeButton}
            onPress={handleDeclinePaywall}
            hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
          >
            <Ionicons name="close" size={24} color={Colors.textSecondary} />
          </Pressable>
        )}
      </View>

      {/* Animated content */}
      <Animated.View
        style={[
          s.contentWrapper,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        {renderCurrentScreen()}
      </Animated.View>
    </SafeAreaView>
  );
};

export default OnboardingFlow;

// ─── STYLES ─────────────────────────────────────────────────

const s = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  contentWrapper: {
    flex: 1,
  },

  // Progress bar
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.sm,
    gap: Spacing.sm,
  },
  progressBarBg: {
    flex: 1,
    height: 4,
    backgroundColor: Colors.border,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: Colors.primary,
    borderRadius: 2,
  },
  backButton: {
    width: MIN_TOUCH_SIZE,
    height: MIN_TOUCH_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButton: {
    width: MIN_TOUCH_SIZE,
    height: MIN_TOUCH_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Screen layouts
  screenCenter: {
    flex: 1,
    paddingHorizontal: Spacing.xl,
    justifyContent: 'center',
    alignItems: 'center',
  },
  screenTop: {
    flex: 1,
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.lg,
  },

  // Welcome screen
  welcomeIconContainer: {
    marginBottom: Spacing.xl,
  },
  welcomeIconOuter: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcomeIconInner: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: Colors.primaryMuted,
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcomeTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.xs,
  },
  welcomeSubtitle: {
    ...Typography.h2,
    color: Colors.primary,
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },
  welcomeDesc: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.md,
  },
  welcomeBadgeRow: {
    flexDirection: 'row',
    gap: Spacing.sm,
    marginBottom: Spacing.xxl,
  },
  welcomeBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: Colors.surface,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.round,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  welcomeBadgeText: {
    ...Typography.caption,
    color: Colors.textSecondary,
    fontWeight: '600',
  },

  // Question screens
  questionTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    marginBottom: Spacing.sm,
  },
  questionSubtitle: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginBottom: Spacing.xl,
  },

  // Option grid (Use Case, Industry)
  optionGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.md,
  },
  optionCard: {
    width: (SCREEN_WIDTH - Spacing.xl * 2 - Spacing.md) / 2 - 1,
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    paddingVertical: Spacing.lg,
    paddingHorizontal: Spacing.md,
    alignItems: 'center',
    gap: Spacing.sm,
    ...Shadows.sm,
  },
  optionCardSelected: {
    borderColor: Colors.primary,
    backgroundColor: Colors.primaryLight,
  },
  optionLabel: {
    ...Typography.label,
    color: Colors.textPrimary,
    textAlign: 'center',
  },
  optionLabelSelected: {
    color: Colors.primary,
    fontWeight: '700',
  },

  // Volume list
  volumeList: {
    gap: Spacing.md,
  },
  volumeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    paddingVertical: Spacing.lg,
    paddingHorizontal: Spacing.xl,
    ...Shadows.sm,
  },
  volumeCardSelected: {
    borderColor: Colors.primary,
    backgroundColor: Colors.primaryLight,
  },
  volumeLeft: {
    gap: 2,
  },
  volumeNumber: {
    ...Typography.h2,
    color: Colors.textPrimary,
  },
  volumeNumberSelected: {
    color: Colors.primary,
  },
  volumeSubtitle: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  volumeSubtitleSelected: {
    color: Colors.primaryDark,
  },

  // Radio buttons
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: Colors.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioOuterSelected: {
    borderColor: Colors.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: Colors.primary,
  },

  // Pain point list
  painList: {
    gap: Spacing.md,
  },
  painCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    paddingVertical: Spacing.lg,
    paddingHorizontal: Spacing.lg,
    gap: Spacing.md,
    ...Shadows.sm,
  },
  painCardSelected: {
    borderColor: Colors.primary,
    backgroundColor: Colors.primaryLight,
  },
  painIconBg: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  painIconBgSelected: {
    backgroundColor: Colors.primary,
  },
  painLabel: {
    ...Typography.body,
    color: Colors.textPrimary,
    flex: 1,
  },
  painLabelSelected: {
    color: Colors.primaryDark,
    fontWeight: '600',
  },

  // Validation screen
  validationIconContainer: {
    marginBottom: Spacing.lg,
  },
  validationTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.md,
  },
  validationDesc: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.md,
  },
  projectionCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.xl,
    padding: Spacing.xl,
    width: '100%',
    marginBottom: Spacing.xl,
    ...Shadows.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  projectionRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  projectionItem: {
    alignItems: 'center',
  },
  projectionNumber: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.primary,
    letterSpacing: -1,
  },
  projectionLabel: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  projectionDivider: {
    width: 1,
    height: 50,
    backgroundColor: Colors.border,
  },
  projectionFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginTop: Spacing.lg,
    paddingTop: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  projectionFooterText: {
    ...Typography.caption,
    color: Colors.success,
    fontWeight: '500',
  },

  // Feature showcase
  featureScroll: {
    flex: 1,
  },
  featureCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    marginBottom: Spacing.md,
    gap: Spacing.lg,
    ...Shadows.sm,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  featureIconBg: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    ...Typography.label,
    color: Colors.textPrimary,
    fontWeight: '600',
    marginBottom: 2,
  },
  featureDesc: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  stickyBottom: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    paddingHorizontal: Spacing.xl,
    paddingBottom: Spacing.xl,
    paddingTop: Spacing.lg,
    backgroundColor: Colors.background,
  },

  // Security screen
  securityHeader: {
    alignItems: 'center',
    marginBottom: Spacing.xl,
  },
  securityShieldBg: {
    width: 96,
    height: 96,
    borderRadius: 48,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  securityTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.sm,
  },
  securityList: {
    gap: Spacing.md,
    marginBottom: Spacing.xl,
  },
  securityCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    gap: Spacing.md,
    ...Shadows.sm,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  securityCardIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  securityCardContent: {
    flex: 1,
  },
  securityCardTitle: {
    ...Typography.label,
    color: Colors.textPrimary,
    fontWeight: '600',
    marginBottom: 2,
  },
  securityCardDesc: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },

  // Social proof
  socialHeader: {
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  socialBigNumber: {
    fontSize: 48,
    fontWeight: '800',
    color: Colors.primary,
    letterSpacing: -2,
  },
  socialBigLabel: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  starsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    marginBottom: Spacing.xl,
  },
  starsText: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginLeft: Spacing.sm,
  },
  testimonialList: {
    gap: Spacing.md,
    marginBottom: Spacing.xl,
  },
  testimonialCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    ...Shadows.sm,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  testimonialHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
    marginBottom: Spacing.sm,
  },
  testimonialAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.primaryMuted,
    justifyContent: 'center',
    alignItems: 'center',
  },
  testimonialAvatarText: {
    ...Typography.label,
    color: Colors.primary,
    fontWeight: '700',
  },
  testimonialName: {
    ...Typography.label,
    color: Colors.textPrimary,
    fontWeight: '600',
  },
  testimonialRole: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  testimonialText: {
    ...Typography.bodySmall,
    color: Colors.textPrimary,
    fontStyle: 'italic',
    marginBottom: Spacing.xs,
  },
  testimonialStars: {
    flexDirection: 'row',
    gap: 2,
  },

  // Notification screen
  notifIconContainer: {
    marginBottom: Spacing.xl,
    position: 'relative',
  },
  notifBell: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notifBadge: {
    position: 'absolute',
    top: 8,
    right: 8,
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: Colors.error,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: Colors.background,
  },
  notifBadgeText: {
    ...Typography.caption,
    color: '#FFF',
    fontWeight: '700',
    fontSize: 12,
  },
  notifTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.md,
  },
  notifDesc: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.md,
  },
  notifExamples: {
    gap: Spacing.md,
    marginBottom: Spacing.xxl,
    width: '100%',
  },
  notifExample: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
    backgroundColor: Colors.surface,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.lg,
    borderRadius: BorderRadius.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  notifExampleText: {
    ...Typography.bodySmall,
    color: Colors.textPrimary,
  },

  // Plan Ready screen
  readyIconContainer: {
    marginBottom: Spacing.lg,
  },
  readyTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.xl,
  },
  readySummaryCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.xl,
    padding: Spacing.xl,
    width: '100%',
    marginBottom: Spacing.xl,
    gap: Spacing.lg,
    ...Shadows.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  readySummaryRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
  },
  readySummaryText: {
    ...Typography.body,
    color: Colors.textPrimary,
  },

  // Paywall screen
  paywallScroll: {
    flex: 1,
  },
  paywallScrollContent: {
    paddingHorizontal: Spacing.xl,
    paddingBottom: Spacing.xxxl,
  },

  // Trial timeline
  trialTimeline: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'center',
    paddingVertical: Spacing.xl,
    paddingHorizontal: Spacing.md,
  },
  timelineStep: {
    alignItems: 'center',
    width: 80,
  },
  timelineDot: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 6,
  },
  timelineDotActive: {
    backgroundColor: Colors.success,
  },
  timelineDotMid: {
    backgroundColor: Colors.primaryLight,
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  timelineDotEnd: {
    backgroundColor: Colors.surfaceElevated,
    borderWidth: 2,
    borderColor: Colors.border,
  },
  timelineLine: {
    height: 2,
    flex: 1,
    backgroundColor: Colors.border,
    marginTop: 17,
  },
  timelineLabel: {
    ...Typography.label,
    color: Colors.textPrimary,
    fontWeight: '600',
  },
  timelineDesc: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },

  paywallNoPay: {
    ...Typography.h3,
    color: Colors.success,
    textAlign: 'center',
    marginBottom: Spacing.lg,
    fontWeight: '700',
  },

  freeTierNote: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginBottom: Spacing.xl,
    paddingVertical: Spacing.sm,
    paddingHorizontal: Spacing.md,
    backgroundColor: Colors.surfaceElevated,
    borderRadius: BorderRadius.md,
  },
  freeTierNoteText: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },

  // Plan cards
  planCards: {
    gap: Spacing.md,
    marginBottom: Spacing.xl,
  },
  planCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    padding: Spacing.lg,
    ...Shadows.sm,
  },
  planCardYearly: {
    borderColor: Colors.primaryMuted,
    position: 'relative',
    overflow: 'visible',
  },
  planCardSelected: {
    borderColor: Colors.primary,
    backgroundColor: Colors.primaryLight,
  },
  planRadioRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
    marginBottom: Spacing.sm,
  },
  planName: {
    ...Typography.h3,
    color: Colors.textPrimary,
  },
  planPrice: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.textPrimary,
    marginLeft: 36,
  },
  planPricePer: {
    fontSize: 16,
    fontWeight: '400',
    color: Colors.textSecondary,
  },
  planPriceMonthly: {
    ...Typography.caption,
    color: Colors.success,
    fontWeight: '600',
    marginLeft: 36,
    marginTop: 2,
  },
  bestValueBadge: {
    position: 'absolute',
    top: -12,
    right: 16,
    backgroundColor: Colors.primary,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: BorderRadius.round,
    zIndex: 1,
  },
  bestValueText: {
    ...Typography.overline,
    color: '#FFF',
    fontSize: 10,
    letterSpacing: 1,
  },
  saveBadge: {
    backgroundColor: Colors.successLight,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: BorderRadius.round,
    marginLeft: 'auto',
  },
  saveBadgeText: {
    ...Typography.caption,
    color: Colors.success,
    fontWeight: '700',
    fontSize: 11,
  },

  // Benefits list
  benefitsList: {
    gap: Spacing.md,
    marginBottom: Spacing.xl,
    width: '100%',
  },
  benefitRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
  },
  benefitText: {
    ...Typography.body,
    color: Colors.textPrimary,
  },

  // CTA button
  ctaButton: {
    backgroundColor: Colors.primary,
    borderRadius: BorderRadius.lg,
    paddingVertical: 18,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    ...Shadows.md,
  },
  ctaButtonDisabled: {
    opacity: 0.6,
  },
  ctaButtonText: {
    ...Typography.button,
    color: '#FFF',
    fontSize: 18,
    fontWeight: '700',
  },

  cancelText: {
    ...Typography.caption,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginTop: Spacing.md,
    marginBottom: Spacing.md,
  },

  // Social proof on paywall
  paywallSocial: {
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  paywallStars: {
    flexDirection: 'row',
    gap: 2,
    marginBottom: 4,
  },
  paywallSocialText: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },

  // Restore
  restoreButton: {
    alignItems: 'center',
    paddingVertical: Spacing.md,
  },
  restoreText: {
    ...Typography.caption,
    color: Colors.textLink,
    textDecorationLine: 'underline',
  },

  // Primary button (non-paywall)
  primaryButton: {
    backgroundColor: Colors.primary,
    borderRadius: BorderRadius.lg,
    paddingVertical: 16,
    paddingHorizontal: Spacing.xl,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: Spacing.sm,
    width: '100%',
    ...Shadows.md,
  },
  primaryButtonText: {
    ...Typography.button,
    color: '#FFF',
    fontWeight: '700',
  },

  // Text button
  textButton: {
    paddingVertical: Spacing.md,
    alignItems: 'center',
  },
  textButtonText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    textDecorationLine: 'underline',
  },

  // Rescue offer
  rescueIconBg: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: Colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.xl,
  },
  rescueTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: Spacing.md,
  },
  rescueDesc: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: Spacing.xl,
  },
  rescueCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.xl,
    padding: Spacing.xl,
    width: '100%',
    marginBottom: Spacing.xl,
    alignItems: 'center',
    ...Shadows.md,
    borderWidth: 2,
    borderColor: Colors.primary,
    position: 'relative',
  },
  rescuePriceStrike: {
    ...Typography.body,
    color: Colors.textTertiary,
    textDecorationLine: 'line-through',
    marginBottom: 4,
  },
  rescuePrice: {
    fontSize: 40,
    fontWeight: '800',
    color: Colors.primary,
    letterSpacing: -1,
  },
  rescuePricePer: {
    fontSize: 18,
    fontWeight: '400',
    color: Colors.textSecondary,
  },
  rescuePriceMonthly: {
    ...Typography.bodySmall,
    color: Colors.success,
    fontWeight: '600',
    marginTop: 2,
    marginBottom: Spacing.sm,
  },
  rescueSaveBadge: {
    backgroundColor: Colors.success,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: BorderRadius.round,
  },
  rescueSaveBadgeText: {
    ...Typography.overline,
    color: '#FFF',
    fontSize: 11,
  },
});
