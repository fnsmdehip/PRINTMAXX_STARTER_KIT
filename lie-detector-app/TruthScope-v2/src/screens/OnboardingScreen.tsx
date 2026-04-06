import React, { useCallback, useRef, useState, useEffect } from 'react';
import {
  View, Text, StyleSheet, Dimensions, FlatList, Alert, Linking, ViewToken,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { playSound } from '../sounds/SoundEngine';
import { Camera } from 'expo-camera';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue, useAnimatedStyle, withRepeat, withTiming, withSequence,
  withDelay, withSpring, interpolate, Easing, FadeIn, FadeInDown, ZoomIn,
} from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors, spacing, typography, radii } from '../theme';
import { OnboardingStep } from '../utils/types';
import { saveProfile } from '../store';
import { DISCLAIMER_SHORT, PRIVACY_POLICY_URL, TERMS_URL } from '../legal/disclaimer';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

const MONTHLY_LINK = 'https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F';
const ANNUAL_LINK = 'https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G';

const STEPS: OnboardingStep[] = [
  'welcome', 'howItWorks', 'scienceBehind', 'fingerDemo', 'faceDemo',
  'voiceDemo', 'multiModal', 'accuracy', 'partyMode', 'disclaimer',
  'permissions', 'baseline', 'premium', 'ready',
];

const PREMIUM_INDEX = STEPS.indexOf('premium');

function PulsingGlow() {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(0.4);
  useEffect(() => {
    scale.value = withRepeat(withTiming(1.35, { duration: 2000, easing: Easing.inOut(Easing.ease) }), -1, true);
    opacity.value = withRepeat(withTiming(0.8, { duration: 2000, easing: Easing.inOut(Easing.ease) }), -1, true);
  }, []);
  const glowStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }], opacity: opacity.value }));
  return (
    <Animated.View style={[styles.glowCircle, glowStyle]}>
      <LinearGradient colors={[colors.accent.primary + '40', colors.accent.secondary + '20', 'transparent']}
        style={styles.glowGradient} start={{ x: 0.5, y: 0.5 }} end={{ x: 1, y: 1 }} />
    </Animated.View>
  );
}

function AnimatedCheckmark() {
  const scale = useSharedValue(0);
  useEffect(() => { scale.value = withDelay(300, withSpring(1, { damping: 8, stiffness: 120 })); }, []);
  const animStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
  return (
    <Animated.View style={[styles.checkCircle, animStyle]}>
      <LinearGradient colors={[colors.accent.primary, colors.accent.secondary]}
        style={styles.checkGradient} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}>
        <Ionicons name="checkmark-sharp" size={64} color={colors.text.primary} />
      </LinearGradient>
    </Animated.View>
  );
}

interface StepContentProps { step: OnboardingStep; isActive: boolean; }

function StepContent({ step, isActive }: StepContentProps) {
  if (!isActive) return <View style={styles.stepContainer} />;

  const content: Record<OnboardingStep, { icon: keyof typeof Ionicons.glyphMap; title: string; body: string; visual?: React.ReactNode }> = {
    welcome: { icon: 'shield-checkmark', title: 'Welcome to TruthScope', body: 'The real biometric lie detector. No fakes, no simulations. Real sensors, real science.' },
    howItWorks: { icon: 'hardware-chip', title: 'How It Works', body: 'TruthScope measures your heart rate, voice patterns, and facial behavior using your phone\'s built-in sensors. Changes in these signals can indicate stress.' },
    scienceBehind: { icon: 'flask', title: 'The Science', body: 'Based on decades of deception research. Heart rate variability, vocal micro-tremors, and facial micro-expressions are all measurable indicators of cognitive load.' },
    fingerDemo: { icon: 'finger-print', title: 'Finger Pulse', body: 'Place your finger over the camera. The flash measures blood volume changes to detect your heartbeat and stress responses. This is the same technology used in medical pulse oximeters.' },
    faceDemo: { icon: 'scan', title: 'Face Scan', body: 'The front camera tracks your blink rate, gaze patterns, and micro-expressions. Genuine emotions produce symmetric expressions. Concealed emotions create brief asymmetries.' },
    voiceDemo: { icon: 'mic', title: 'Voice Analysis', body: 'Your microphone captures vocal characteristics that change under stress: pitch variation, micro-tremors (8-12 Hz), and response timing patterns.' },
    multiModal: { icon: 'layers', title: 'Multi-Modal', body: 'Combine all three sensors for maximum detection accuracy (up to ~70%). Multiple independent signals cross-validate each other for more reliable results.' },
    accuracy: { icon: 'stats-chart', title: 'Honest Accuracy', body: 'Single mode: 55-65%. Multi-modal: up to 70%. Professional polygraphs: 80-90%. We are transparent about what phone sensors can and cannot do. This is entertainment-grade, not forensic.' },
    partyMode: { icon: 'people', title: 'Party Mode', body: 'Pass the phone around. Ask questions. Real microphone metering scores each answer. The perfect party game and icebreaker.' },
    disclaimer: { icon: 'alert-circle', title: 'Important Disclaimer', body: DISCLAIMER_SHORT + '\n\nYou must acknowledge this to continue.' },
    permissions: { icon: 'key', title: 'Permissions', body: 'TruthScope needs camera and microphone access to measure real biometric signals. All processing happens locally on your device. No data is sent to any server.' },
    baseline: { icon: 'pulse', title: 'Calibration', body: 'For the most accurate results, complete a 30-second baseline calibration on your first session. This measures your resting heart rate and voice for comparison.' },
    premium: { icon: 'diamond', title: 'Unlock Full Power', body: 'Multi-Modal detection, premium party questions, and priority support.' },
    ready: { icon: 'rocket', title: 'You\'re Ready', body: 'Start detecting. Remember: TruthScope is for entertainment and education. Have fun with it.' },
  };

  const c = content[step];
  return (
    <View style={styles.stepContainer}>
      {step === 'welcome' && <PulsingGlow />}
      {step === 'ready' && <AnimatedCheckmark />}
      {step !== 'welcome' && step !== 'ready' && (
        <Animated.View entering={FadeIn.delay(200).duration(400)} style={styles.iconWrapper}>
          <LinearGradient colors={[colors.accent.primary + '20', 'transparent']} style={styles.iconGradientBg}>
            <Ionicons name={c.icon} size={48} color={colors.accent.primary} />
          </LinearGradient>
        </Animated.View>
      )}
      <Animated.Text entering={FadeInDown.delay(100).duration(400)} style={styles.stepTitle}>{c.title}</Animated.Text>
      <Animated.Text entering={FadeInDown.delay(200).duration(400)} style={styles.stepBody}>{c.body}</Animated.Text>
    </View>
  );
}

export default function OnboardingScreen({ navigation }: { navigation: any }) {
  const insets = useSafeAreaInsets();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [disclaimerAccepted, setDisclaimerAccepted] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  const currentStep = STEPS[currentIndex];
  const isLastStep = currentIndex === STEPS.length - 1;

  const onViewableItemsChanged = useCallback(({ viewableItems }: { viewableItems: ViewToken[] }) => {
    if (viewableItems.length > 0 && viewableItems[0].index !== null) {
      setCurrentIndex(viewableItems[0].index);
    }
  }, []);

  const viewabilityConfig = useRef({ viewAreaCoveragePercentThreshold: 60 }).current;

  const goNext = useCallback(() => {
    if (currentStep === 'disclaimer' && !disclaimerAccepted) {
      Alert.alert('Disclaimer Required', 'You must acknowledge the disclaimer to continue using TruthScope.', [
        { text: 'Read Again', style: 'cancel' },
        { text: 'I Understand', onPress: () => { setDisclaimerAccepted(true); playSound('permissionGranted'); advance(); } },
      ]);
      return;
    }

    if (currentStep === 'permissions') {
      Camera.requestCameraPermissionsAsync().then(() => {
        playSound('permissionGranted');
        advance();
      });
      return;
    }

    if (isLastStep) {
      playSound('success');
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      saveProfile({ hasCompletedOnboarding: true });
      navigation.reset({ index: 0, routes: [{ name: 'Home' }] });
      return;
    }

    advance();
  }, [currentIndex, currentStep, disclaimerAccepted, isLastStep, navigation]);

  const advance = () => {
    playSound('swipe');
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const nextIndex = Math.min(currentIndex + 1, STEPS.length - 1);
    flatListRef.current?.scrollToIndex({ index: nextIndex, animated: true });
  };

  const goBack = () => {
    playSound('swipe');
    if (currentIndex > 0) {
      flatListRef.current?.scrollToIndex({ index: currentIndex - 1, animated: true });
    }
  };

  const handlePremium = (plan: 'monthly' | 'annual') => {
    playSound('premium');
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    const link = plan === 'annual' ? ANNUAL_LINK : MONTHLY_LINK;
    Linking.openURL(link);
  };

  const renderItem = ({ item, index }: { item: OnboardingStep; index: number }) => (
    <View style={{ width: SCREEN_WIDTH }}>
      <StepContent step={item} isActive={Math.abs(index - currentIndex) <= 1} />
      {item === 'premium' && (
        <View style={styles.premiumCards}>
          <TouchableOpacity onPress={() => handlePremium('annual')} style={styles.premiumCard} sound="premium" haptic="medium">
            <LinearGradient colors={[...colors.gradient.premium]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}
              style={styles.premiumCardGradient}>
              <View style={styles.bestValueBadge}><Text style={styles.bestValueText}>BEST VALUE</Text></View>
              <Text style={styles.premiumPrice}>$29.99</Text>
              <Text style={styles.premiumPeriod}>per year</Text>
              <Text style={styles.premiumSavings}>$2.50/mo - Save 50%</Text>
            </LinearGradient>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => handlePremium('monthly')} style={styles.premiumCard} sound="tap">
            <View style={styles.premiumCardBasic}>
              <Text style={styles.premiumPrice}>$4.99</Text>
              <Text style={styles.premiumPeriod}>per month</Text>
            </View>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );

  return (
    <View style={[styles.screen, { paddingTop: insets.top }]}>
      <FlatList
        ref={flatListRef}
        data={STEPS}
        renderItem={renderItem}
        keyExtractor={(item) => item}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={viewabilityConfig}
        getItemLayout={(_, index) => ({ length: SCREEN_WIDTH, offset: SCREEN_WIDTH * index, index })}
      />

      {/* Bottom controls */}
      <View style={[styles.bottomBar, { paddingBottom: insets.bottom + spacing.md }]}>
        {/* Progress dots */}
        <View style={styles.dots}>
          {STEPS.map((_, i) => (
            <View key={i} style={[styles.dot, i === currentIndex && styles.dotActive]} />
          ))}
        </View>

        <View style={styles.buttonRow}>
          {currentIndex > 0 && (
            <TouchableOpacity onPress={goBack} style={styles.backBtn} sound="swipe">
              <Ionicons name="arrow-back" size={20} color={colors.text.secondary} />
            </TouchableOpacity>
          )}

          {currentStep === 'premium' && (
            <TouchableOpacity onPress={advance} style={styles.skipBtn} sound="tap">
              <Text style={styles.skipText}>Skip for now</Text>
            </TouchableOpacity>
          )}

          <TouchableOpacity onPress={goNext} style={styles.nextBtn} sound="tap" haptic="light">
            <LinearGradient colors={[...colors.gradient.scanning]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
              style={styles.nextGradient}>
              <Text style={styles.nextText}>
                {isLastStep ? 'Get Started' : currentStep === 'disclaimer' ? 'I Understand' : 'Next'}
              </Text>
              {!isLastStep && <Ionicons name="arrow-forward" size={18} color="#FFFFFF" />}
            </LinearGradient>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg.primary },
  stepContainer: { width: SCREEN_WIDTH, flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.xl },
  glowCircle: { width: 200, height: 200, borderRadius: 100, position: 'absolute' },
  glowGradient: { flex: 1, borderRadius: 100 },
  checkCircle: { width: 120, height: 120, borderRadius: 60, marginBottom: spacing.lg },
  checkGradient: { flex: 1, borderRadius: 60, alignItems: 'center', justifyContent: 'center' },
  iconWrapper: { marginBottom: spacing.lg },
  iconGradientBg: { width: 96, height: 96, borderRadius: 48, alignItems: 'center', justifyContent: 'center' },
  stepTitle: { ...typography.hero, color: colors.text.primary, textAlign: 'center', marginBottom: spacing.md },
  stepBody: { ...typography.body, color: colors.text.secondary, textAlign: 'center', lineHeight: 24, maxWidth: 340 },
  premiumCards: { paddingHorizontal: spacing.xl, gap: spacing.sm, marginTop: spacing.lg },
  premiumCard: { borderRadius: radii.lg, overflow: 'hidden' },
  premiumCardGradient: { padding: spacing.lg, alignItems: 'center' },
  premiumCardBasic: { backgroundColor: colors.bg.card, padding: spacing.lg, alignItems: 'center', borderRadius: radii.lg },
  bestValueBadge: { backgroundColor: '#FFFFFF30', paddingHorizontal: 12, paddingVertical: 4, borderRadius: radii.full, marginBottom: spacing.sm },
  bestValueText: { color: '#FFFFFF', fontSize: 10, fontWeight: '800', letterSpacing: 1 },
  premiumPrice: { fontSize: 32, fontWeight: '800', color: '#FFFFFF' },
  premiumPeriod: { ...typography.body, color: 'rgba(255,255,255,0.8)' },
  premiumSavings: { ...typography.caption, color: 'rgba(255,255,255,0.6)', marginTop: 4 },
  bottomBar: { paddingHorizontal: spacing.lg, paddingTop: spacing.md },
  dots: { flexDirection: 'row', justifyContent: 'center', gap: 6, marginBottom: spacing.md },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.bg.elevated },
  dotActive: { backgroundColor: colors.accent.primary, width: 24 },
  buttonRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  backBtn: { width: 44, height: 44, borderRadius: 22, backgroundColor: colors.bg.card, alignItems: 'center', justifyContent: 'center' },
  skipBtn: { paddingHorizontal: spacing.md, paddingVertical: spacing.sm },
  skipText: { ...typography.caption, color: colors.text.tertiary },
  nextBtn: { flex: 1, borderRadius: radii.lg, overflow: 'hidden' },
  nextGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: 14 },
  nextText: { ...typography.bodyBold, color: '#FFFFFF' },
});
