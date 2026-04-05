import React, { useCallback, useRef, useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  FlatList,

  Pressable,
  Alert,
  Linking,
  Platform,
  ViewToken,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { Camera } from 'expo-camera';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
  withSequence,
  withDelay,
  withSpring,
  interpolate,
  Easing,
  FadeIn,
  FadeInDown,
  FadeInUp,
  ZoomIn,
} from 'react-native-reanimated';

import { colors, spacing, typography, radii } from '../theme';
import { OnboardingStep } from '../utils/types';
import { saveProfile } from '../store';
import { DISCLAIMER_SHORT } from '../legal/disclaimer';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

const MONTHLY_LINK = 'https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F';
const ANNUAL_LINK = 'https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G';

const STEPS: OnboardingStep[] = [
  'welcome',
  'howItWorks',
  'scienceBehind',
  'fingerDemo',
  'faceDemo',
  'voiceDemo',
  'multiModal',
  'accuracy',
  'partyMode', // use cases
  'disclaimer',
  'permissions',
  'baseline',
  'premium',
  'ready',
];

const PREMIUM_INDEX = STEPS.indexOf('premium');

// ---------------------------------------------------------------------------
// Animated subcomponents
// ---------------------------------------------------------------------------

function PulsingGlow() {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(0.4);

  useEffect(() => {
    scale.value = withRepeat(
      withTiming(1.35, { duration: 2000, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
    opacity.value = withRepeat(
      withTiming(0.8, { duration: 2000, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
  }, []);

  const glowStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={[styles.glowCircle, glowStyle]}>
      <LinearGradient
        colors={[colors.accent.primary + '40', colors.accent.secondary + '20', 'transparent']}
        style={styles.glowGradient}
        start={{ x: 0.5, y: 0.5 }}
        end={{ x: 1, y: 1 }}
      />
    </Animated.View>
  );
}

function AnimatedCheckmark() {
  const scale = useSharedValue(0);
  useEffect(() => {
    scale.value = withDelay(300, withSpring(1, { damping: 8, stiffness: 120 }));
  }, []);
  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  return (
    <Animated.View style={[styles.checkCircle, animStyle]}>
      <LinearGradient
        colors={[colors.accent.primary, colors.accent.secondary]}
        style={styles.checkGradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Ionicons name="checkmark-sharp" size={64} color={colors.text.primary} />
      </LinearGradient>
    </Animated.View>
  );
}

function ConvergingLines() {
  const progress = useSharedValue(0);
  useEffect(() => {
    progress.value = withRepeat(
      withTiming(1, { duration: 2500, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
  }, []);

  const line1 = useAnimatedStyle(() => ({
    transform: [{ translateX: interpolate(progress.value, [0, 1], [-40, 0]) }],
    opacity: interpolate(progress.value, [0, 0.5, 1], [0.3, 1, 0.3]),
  }));
  const line2 = useAnimatedStyle(() => ({
    transform: [{ translateX: interpolate(progress.value, [0, 1], [40, 0]) }],
    opacity: interpolate(progress.value, [0, 0.5, 1], [0.3, 1, 0.3]),
  }));
  const line3 = useAnimatedStyle(() => ({
    transform: [{ translateY: interpolate(progress.value, [0, 1], [30, 0]) }],
    opacity: interpolate(progress.value, [0, 0.5, 1], [0.3, 1, 0.3]),
  }));

  return (
    <View style={styles.convergingContainer}>
      <Animated.View style={[styles.convergeLine, { backgroundColor: colors.accent.primary }, line1]} />
      <Animated.View style={[styles.convergeLine, { backgroundColor: colors.accent.secondary }, line2]} />
      <Animated.View style={[styles.convergeLine, { backgroundColor: colors.accent.tertiary }, line3]} />
      <View style={styles.convergeCenter}>
        <LinearGradient
          colors={[colors.accent.primary, colors.accent.secondary]}
          style={styles.convergeCenterGrad}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        />
      </View>
    </View>
  );
}

function WaveformVisual() {
  const bars = Array.from({ length: 24 }, (_, i) => i);
  return (
    <View style={styles.waveformContainer}>
      {bars.map((i) => (
        <WaveBar key={i} index={i} />
      ))}
    </View>
  );
}

function WaveBar({ index }: { index: number }) {
  const height = useSharedValue(8);
  useEffect(() => {
    const baseHeight = 12 + Math.sin(index * 0.6) * 20;
    height.value = withRepeat(
      withDelay(
        index * 60,
        withTiming(baseHeight + Math.random() * 30, {
          duration: 400 + Math.random() * 300,
          easing: Easing.inOut(Easing.ease),
        }),
      ),
      -1,
      true,
    );
  }, []);

  const barStyle = useAnimatedStyle(() => ({
    height: height.value,
  }));

  return (
    <Animated.View
      style={[
        {
          width: 4,
          borderRadius: 2,
          backgroundColor: index % 3 === 0 ? colors.accent.primary : colors.accent.secondary,
          marginHorizontal: 2,
        },
        barStyle,
      ]}
    />
  );
}

// ---------------------------------------------------------------------------
// Icon badge used in cards
// ---------------------------------------------------------------------------

function IconBadge({
  name,
  color,
  size = 32,
}: {
  name: React.ComponentProps<typeof Ionicons>['name'];
  color: string;
  size?: number;
}) {
  return (
    <View style={[styles.iconBadge, { borderColor: color + '30' }]}>
      <Ionicons name={name} size={size} color={color} />
    </View>
  );
}

// ---------------------------------------------------------------------------
// Individual Screen Renderers
// ---------------------------------------------------------------------------

function WelcomeScreen({ onNext }: { onNext: () => void }) {
  return (
    <Pressable style={styles.screenContainer} onPress={onNext}>
      <View style={styles.centered}>
        <PulsingGlow />
        <Animated.View entering={ZoomIn.duration(800)}>
          <Ionicons name="eye-outline" size={72} color={colors.accent.primary} />
        </Animated.View>
        <Animated.Text entering={FadeInDown.delay(400).duration(600)} style={styles.heroTitle}>
          TruthScope
        </Animated.Text>
        <Animated.Text entering={FadeInDown.delay(700).duration(600)} style={styles.heroTagline}>
          See Beyond Words
        </Animated.Text>
        <Animated.Text entering={FadeIn.delay(1200).duration(800)} style={styles.tapHint}>
          Tap to begin
        </Animated.Text>
      </View>
    </Pressable>
  );
}

function HowItWorksScreen() {
  const cards: {
    icon: React.ComponentProps<typeof Ionicons>['name'];
    title: string;
    desc: string;
    color: string;
  }[] = [
    {
      icon: 'fitness-outline',
      title: 'Measure',
      desc: 'Camera-based pulse detection reads your heart rate and variability in real time.',
      color: colors.accent.primary,
    },
    {
      icon: 'pulse-outline',
      title: 'Analyze',
      desc: 'Voice stress analysis detects micro-tremors and pitch changes invisible to the ear.',
      color: colors.accent.secondary,
    },
    {
      icon: 'eye-outline',
      title: 'Detect',
      desc: 'AI-powered facial analysis tracks 50+ landmarks, blinks, and micro-expressions.',
      color: colors.accent.tertiary,
    },
  ];

  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>How It Works</Text>
      <Text style={styles.sectionSubtitle}>Three biometric channels. One truth score.</Text>
      <View style={styles.cardsRow}>
        {cards.map((card, i) => (
          <Animated.View
            key={card.title}
            entering={FadeInUp.delay(200 + i * 200).duration(500)}
            style={styles.howCard}
          >
            <LinearGradient
              colors={[card.color + '15', 'transparent']}
              style={styles.howCardGrad}
              start={{ x: 0.5, y: 0 }}
              end={{ x: 0.5, y: 1 }}
            />
            <IconBadge name={card.icon} color={card.color} />
            <Text style={[styles.howCardTitle, { color: card.color }]}>{card.title}</Text>
            <Text style={styles.howCardDesc}>{card.desc}</Text>
          </Animated.View>
        ))}
      </View>
    </View>
  );
}

function ScienceScreen() {
  const points = [
    { icon: 'heart-outline' as const, text: 'PPG (photoplethysmography) reads blood volume changes through your camera' },
    { icon: 'mic-outline' as const, text: 'Voice stress analysis measures jitter, shimmer, and tremor patterns' },
    { icon: 'scan-outline' as const, text: 'Facial landmark AI tracks 50+ points for micro-expression detection' },
  ];
  return (
    <View style={styles.screenContainer}>
      <Animated.View entering={FadeInDown.duration(500)}>
        <LinearGradient
          colors={[colors.accent.primary + '20', colors.accent.secondary + '20']}
          style={styles.scienceBadge}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Ionicons name="flask-outline" size={28} color={colors.accent.primary} />
          <Text style={styles.scienceBadgeText}>Real Biometric Analysis</Text>
        </LinearGradient>
      </Animated.View>

      <Text style={styles.sectionTitle}>The Science</Text>
      <Text style={styles.bodyText}>
        TruthScope measures real biometric signals similar to those used in
        professional settings, adapted for your phone's sensors. Less precise
        than dedicated equipment, but real science, not a prank app.
      </Text>

      {points.map((p, i) => (
        <Animated.View key={i} entering={FadeInDown.delay(300 + i * 200).duration(400)} style={styles.scienceRow}>
          <View style={styles.scienceDot}>
            <Ionicons name={p.icon} size={20} color={colors.accent.primary} />
          </View>
          <Text style={styles.scienceText}>{p.text}</Text>
        </Animated.View>
      ))}
    </View>
  );
}

function FingerDemoScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Finger Pulse Mode</Text>

      <Animated.View entering={ZoomIn.delay(200).duration(600)} style={styles.demoVisual}>
        <LinearGradient
          colors={[colors.accent.primary + '15', colors.bg.card]}
          style={styles.demoCircle}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
        >
          <Ionicons name="finger-print-outline" size={80} color={colors.accent.primary} />
        </LinearGradient>
      </Animated.View>

      <Text style={styles.bodyText}>
        Place your fingertip gently over the rear camera lens with the flash on.
        The camera reads subtle color changes in your skin caused by blood flow,
        measuring your heart rate and variability in real time.
      </Text>

      <View style={styles.tipBox}>
        <Ionicons name="bulb-outline" size={18} color={colors.accent.warning} />
        <Text style={styles.tipText}>
          Hold steady for best results. Works best in a dimly lit environment.
        </Text>
      </View>
    </View>
  );
}

function FaceDemoScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Face Scan Mode</Text>

      <Animated.View entering={ZoomIn.delay(200).duration(600)} style={styles.demoVisual}>
        <LinearGradient
          colors={[colors.accent.secondary + '15', colors.bg.card]}
          style={styles.demoCircle}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
        >
          <Ionicons name="happy-outline" size={80} color={colors.accent.secondary} />
          {/* Landmark dots */}
          {[
            { top: 35, left: 45 },
            { top: 35, right: 45 },
            { top: 60, left: 55 },
            { top: 60, right: 55 },
            { top: 80, left: 65 },
            { top: 80, right: 65 },
          ].map((pos, i) => (
            <View key={i} style={[styles.landmarkDot, pos]} />
          ))}
        </LinearGradient>
      </Animated.View>

      <Text style={styles.bodyText}>
        Our AI tracks 50+ facial landmarks, micro-expressions, blink patterns,
        and gaze stability using your front camera. Subtle shifts betray what
        words try to hide.
      </Text>
    </View>
  );
}

function VoiceDemoScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Voice Analysis Mode</Text>

      <Animated.View entering={FadeIn.delay(200).duration(600)} style={styles.demoVisual}>
        <WaveformVisual />
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(400).duration(500)}>
        <Text style={styles.bodyText}>
          Vocal stress analysis detects tremors, pitch shifts, and response
          patterns invisible to the human ear. Your voice carries signals your
          conscious mind cannot suppress.
        </Text>
      </Animated.View>
    </View>
  );
}

function MultiModalScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Multi-Modal Fusion</Text>
      <Text style={styles.sectionSubtitle}>Combine all three for maximum accuracy</Text>

      <Animated.View entering={FadeIn.delay(300).duration(800)}>
        <ConvergingLines />
      </Animated.View>

      <View style={styles.multiIcons}>
        {[
          { icon: 'fitness-outline' as const, label: 'Pulse', color: colors.accent.primary },
          { icon: 'mic-outline' as const, label: 'Voice', color: colors.accent.secondary },
          { icon: 'eye-outline' as const, label: 'Face', color: colors.accent.tertiary },
        ].map((item, i) => (
          <Animated.View key={item.label} entering={FadeInUp.delay(500 + i * 150).duration(400)} style={styles.multiItem}>
            <Ionicons name={item.icon} size={28} color={item.color} />
            <Text style={[styles.multiLabel, { color: item.color }]}>{item.label}</Text>
          </Animated.View>
        ))}
      </View>

      <Animated.Text entering={FadeIn.delay(1000).duration(600)} style={styles.bodyText}>
        Cross-referencing three independent biometric channels produces results no
        single sensor can match. This is what makes TruthScope unique.
      </Animated.Text>
    </View>
  );
}

function AccuracyScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>How Accurate Is It?</Text>

      <Animated.View entering={FadeInDown.delay(200).duration(500)} style={styles.accuracyCard}>
        <Text style={styles.accuracyLabel}>Professional Polygraph</Text>
        <View style={styles.accuracyBarBg}>
          <LinearGradient
            colors={[colors.accent.warning, colors.accent.warning + '80']}
            style={[styles.accuracyBarFill, { width: '80%' }]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
          />
        </View>
        <Text style={styles.accuracyValue}>70 - 90%</Text>
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(400).duration(500)} style={styles.accuracyCard}>
        <Text style={styles.accuracyLabel}>TruthScope (Phone Sensors)</Text>
        <View style={styles.accuracyBarBg}>
          <LinearGradient
            colors={[colors.accent.primary, colors.accent.secondary]}
            style={[styles.accuracyBarFill, { width: '55%' }]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
          />
        </View>
        <Text style={styles.accuracyValue}>55 - 70% (stress detection)</Text>
      </Animated.View>

      <Animated.Text entering={FadeIn.delay(700).duration(600)} style={styles.bodyTextSmall}>
        TruthScope detects physiological stress, not deception directly. Stress
        correlates with but does not prove deception. Results are probabilistic
        confidence scores influenced by lighting, movement, noise, and individual
        physiology. For entertainment only. Never use as proof.
      </Animated.Text>
    </View>
  );
}

function UseCasesScreen() {
  const cases = [
    { icon: 'game-controller-outline' as const, label: 'Party Games' },
    { icon: 'videocam-outline' as const, label: 'Stream Content' },
    { icon: 'people-outline' as const, label: 'Friend Challenges' },
    { icon: 'compass-outline' as const, label: 'Self-Discovery' },
    { icon: 'flame-outline' as const, label: 'Truth or Dare' },
    { icon: 'heart-outline' as const, label: 'Couples Night' },
  ];

  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>What Will You Use It For?</Text>

      <View style={styles.useCaseGrid}>
        {cases.map((c, i) => (
          <Animated.View
            key={c.label}
            entering={FadeInUp.delay(150 + i * 100).duration(400)}
            style={styles.useCaseCard}
          >
            <LinearGradient
              colors={[colors.bg.elevated, colors.bg.card]}
              style={styles.useCaseInner}
              start={{ x: 0.5, y: 0 }}
              end={{ x: 0.5, y: 1 }}
            >
              <Ionicons name={c.icon} size={32} color={colors.accent.primary} />
              <Text style={styles.useCaseLabel}>{c.label}</Text>
            </LinearGradient>
          </Animated.View>
        ))}
      </View>
    </View>
  );
}

function DisclaimerScreen({
  acknowledged,
  onAcknowledge,
}: {
  acknowledged: boolean;
  onAcknowledge: () => void;
}) {
  return (
    <View style={styles.screenContainer}>
      <View style={styles.disclaimerIcon}>
        <Ionicons name="shield-checkmark-outline" size={40} color={colors.accent.warning} />
      </View>
      <Text style={styles.sectionTitle}>Before We Start</Text>

      <View style={styles.disclaimerBox}>
        <Text style={styles.disclaimerText}>{DISCLAIMER_SHORT}</Text>
      </View>

      <Pressable
        onPress={onAcknowledge}
        style={[styles.acknowledgeBtn, acknowledged && styles.acknowledgeBtnActive]}
      >
        <View style={styles.checkbox}>
          {acknowledged && <Ionicons name="checkmark" size={16} color={colors.bg.primary} />}
        </View>
        <Text style={styles.acknowledgeText}>
          I understand and agree to use TruthScope responsibly
        </Text>
      </Pressable>
    </View>
  );
}

function PermissionsScreen({ onRequest }: { onRequest: () => void }) {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Permissions</Text>
      <Text style={styles.sectionSubtitle}>TruthScope needs access to your sensors</Text>

      <Animated.View entering={FadeInDown.delay(200).duration(400)} style={styles.permRow}>
        <View style={[styles.permIcon, { backgroundColor: colors.accent.primary + '15' }]}>
          <Ionicons name="camera-outline" size={28} color={colors.accent.primary} />
        </View>
        <View style={styles.permTextBlock}>
          <Text style={styles.permTitle}>Camera</Text>
          <Text style={styles.permDesc}>
            Finger pulse detection (rear) and facial analysis (front). No photos are stored.
          </Text>
        </View>
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(400).duration(400)} style={styles.permRow}>
        <View style={[styles.permIcon, { backgroundColor: colors.accent.secondary + '15' }]}>
          <Ionicons name="mic-outline" size={28} color={colors.accent.secondary} />
        </View>
        <View style={styles.permTextBlock}>
          <Text style={styles.permTitle}>Microphone</Text>
          <Text style={styles.permDesc}>
            Voice stress analysis in real time. Audio is processed locally and never leaves your device.
          </Text>
        </View>
      </Animated.View>

      <TouchableOpacity style={styles.permButton} onPress={onRequest} activeOpacity={0.8}>
        <LinearGradient
          colors={[colors.accent.primary, colors.accent.secondary]}
          style={styles.permButtonGrad}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
        >
          <Text style={styles.permButtonText}>Allow Access</Text>
        </LinearGradient>
      </TouchableOpacity>

      <Text style={styles.privacyNote}>
        All data stays on your device. We never upload biometric data.
      </Text>
    </View>
  );
}

function BaselineScreen() {
  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Let's Calibrate to You</Text>

      <Animated.View entering={ZoomIn.delay(200).duration(600)} style={styles.baselineVisual}>
        <LinearGradient
          colors={[colors.accent.primary + '10', colors.bg.card]}
          style={styles.baselineCircle}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
        >
          <Ionicons name="body-outline" size={64} color={colors.accent.primary} />
        </LinearGradient>
      </Animated.View>

      <Text style={styles.bodyText}>
        Everyone has a unique resting physiology. We need 30 seconds of your calm
        baseline to accurately detect deviations during a session.
      </Text>

      <View style={styles.baselineTips}>
        {[
          'Sit comfortably and stay still',
          'Breathe normally -- don\'t hold your breath',
          'Look forward and relax your face',
        ].map((tip, i) => (
          <Animated.View key={i} entering={FadeInDown.delay(400 + i * 150).duration(400)} style={styles.baselineTipRow}>
            <Text style={styles.baselineTipNum}>{i + 1}</Text>
            <Text style={styles.baselineTipText}>{tip}</Text>
          </Animated.View>
        ))}
      </View>
    </View>
  );
}

function PremiumScreen() {
  const handlePurchase = (link: string) => {
    Linking.openURL(link).catch(() => {
      Alert.alert('Error', 'Could not open the payment page. Please try again.');
    });
  };

  return (
    <View style={styles.screenContainer}>
      <Text style={styles.premiumTitle}>Unlock Full Power</Text>

      {/* Premium features */}
      <View style={styles.premiumFeatures}>
        {[
          { icon: 'infinite-outline' as const, text: 'Unlimited sessions' },
          { icon: 'albums-outline' as const, text: 'All question packs' },
          { icon: 'layers-outline' as const, text: 'Multi-modal analysis' },
          { icon: 'time-outline' as const, text: 'Session history & trends' },
          { icon: 'share-social-outline' as const, text: 'Share & export results' },
        ].map((f, i) => (
          <Animated.View key={i} entering={FadeInDown.delay(100 + i * 80).duration(300)} style={styles.featureRow}>
            <Ionicons name={f.icon} size={20} color={colors.accent.primary} />
            <Text style={styles.featureText}>{f.text}</Text>
          </Animated.View>
        ))}
      </View>

      {/* Plan cards */}
      <View style={styles.planCards}>
        {/* Monthly anchor */}
        <TouchableOpacity
          style={styles.planCard}
          onPress={() => handlePurchase(MONTHLY_LINK)}
          activeOpacity={0.8}
        >
          <Text style={styles.planName}>Monthly</Text>
          <Text style={styles.planPrice}>$4.99</Text>
          <Text style={styles.planPeriod}>/month</Text>
        </TouchableOpacity>

        {/* Annual highlighted */}
        <TouchableOpacity
          style={styles.planCardHighlighted}
          onPress={() => handlePurchase(ANNUAL_LINK)}
          activeOpacity={0.8}
        >
          <View style={styles.saveBadge}>
            <Text style={styles.saveBadgeText}>SAVE 50%</Text>
          </View>
          <LinearGradient
            colors={[colors.accent.primary + '15', colors.accent.secondary + '10']}
            style={styles.planCardHighlightedInner}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Text style={styles.planName}>Annual</Text>
            <Text style={styles.planPriceHighlighted}>$29.99</Text>
            <Text style={styles.planPeriod}>/year</Text>
            <Text style={styles.planEquiv}>Just $2.50/mo</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Free tier info */}
      <View style={styles.freeTierBox}>
        <Text style={styles.freeTierTitle}>Free includes:</Text>
        <Text style={styles.freeTierItem}>3 sessions per day</Text>
        <Text style={styles.freeTierItem}>Finger pulse mode only</Text>
        <Text style={styles.freeTierItem}>Basic question pack</Text>
      </View>

      <Text style={styles.noPaymentText}>No payment due now</Text>

      <TouchableOpacity
        onPress={() => Alert.alert('Restore', 'Looking for previous purchases...', [{ text: 'OK' }])}
      >
        <Text style={styles.restoreText}>Restore Purchases</Text>
      </TouchableOpacity>
    </View>
  );
}

function ReadyScreen({ onStart }: { onStart: () => void }) {
  return (
    <View style={styles.screenContainer}>
      <View style={styles.centered}>
        <AnimatedCheckmark />
        <Animated.Text entering={FadeInDown.delay(600).duration(500)} style={styles.readyTitle}>
          You're Ready
        </Animated.Text>
        <Animated.Text entering={FadeIn.delay(900).duration(500)} style={styles.readySubtitle}>
          All set. Time to see beyond words.
        </Animated.Text>
        <Animated.View entering={FadeInUp.delay(1100).duration(500)} style={{ width: '100%' }}>
          <TouchableOpacity onPress={onStart} activeOpacity={0.8}>
            <LinearGradient
              colors={[colors.accent.primary, colors.accent.secondary]}
              style={styles.startButton}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            >
              <Text style={styles.startButtonText}>Start Your First Session</Text>
              <Ionicons name="arrow-forward" size={22} color={colors.text.primary} />
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>
      </View>
    </View>
  );
}

// ---------------------------------------------------------------------------
// Main Onboarding Screen
// ---------------------------------------------------------------------------

interface OnboardingScreenProps {
  navigation: any;
}

export default function OnboardingScreen({ navigation }: OnboardingScreenProps) {
  const flatListRef = useRef<FlatList>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [disclaimerAcknowledged, setDisclaimerAcknowledged] = useState(false);
  const [permissionsGranted, setPermissionsGranted] = useState(false);

  const viewabilityConfig = useRef({ viewAreaCoveragePercentThreshold: 50 }).current;

  const onViewableItemsChanged = useRef(
    ({ viewableItems }: { viewableItems: ViewToken[] }) => {
      if (viewableItems.length > 0 && viewableItems[0].index !== null) {
        setCurrentIndex(viewableItems[0].index);
      }
    },
  ).current;

  const goTo = useCallback(
    (index: number) => {
      if (index >= 0 && index < STEPS.length) {
        flatListRef.current?.scrollToIndex({ index, animated: true });
      }
    },
    [],
  );

  const goNext = useCallback(() => {
    // Block advancing past disclaimer if not acknowledged
    if (STEPS[currentIndex] === 'disclaimer' && !disclaimerAcknowledged) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
      Alert.alert('Required', 'Please acknowledge the disclaimer before continuing.');
      return;
    }
    goTo(currentIndex + 1);
  }, [currentIndex, disclaimerAcknowledged, goTo]);

  const goSkip = useCallback(() => {
    goTo(PREMIUM_INDEX);
  }, [goTo]);

  const requestPermissions = useCallback(async () => {
    try {
      const { status: cameraStatus } = await Camera.requestCameraPermissionsAsync();
      const { status: micStatus } = await Camera.requestMicrophonePermissionsAsync();
      const granted = cameraStatus === 'granted' && micStatus === 'granted';
      setPermissionsGranted(granted);
      if (granted) {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        goNext();
      } else {
        Alert.alert(
          'Permissions Required',
          'TruthScope needs camera and microphone access to analyze biometric signals. You can enable them in Settings.',
          [
            { text: 'Open Settings', onPress: () => Linking.openSettings() },
            { text: 'Continue Anyway', onPress: goNext },
          ],
        );
      }
    } catch {
      goNext();
    }
  }, [goNext]);

  const handleComplete = useCallback(async () => {
    await saveProfile({ hasCompletedOnboarding: true });
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    navigation.replace('Home');
  }, [navigation]);

  const handleAcknowledge = useCallback(() => {
    setDisclaimerAcknowledged((prev) => !prev);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  }, []);

  const renderItem = useCallback(
    ({ item, index: idx }: { item: OnboardingStep; index: number }) => {
      switch (item) {
        case 'welcome':
          return <WelcomeScreen onNext={goNext} />;
        case 'howItWorks':
          return <HowItWorksScreen />;
        case 'scienceBehind':
          return <ScienceScreen />;
        case 'fingerDemo':
          return <FingerDemoScreen />;
        case 'faceDemo':
          return <FaceDemoScreen />;
        case 'voiceDemo':
          return <VoiceDemoScreen />;
        case 'multiModal':
          return <MultiModalScreen />;
        case 'accuracy':
          return <AccuracyScreen />;
        case 'partyMode': // use cases
          return <UseCasesScreen />;
        case 'disclaimer':
          return (
            <DisclaimerScreen
              acknowledged={disclaimerAcknowledged}
              onAcknowledge={handleAcknowledge}
            />
          );
        case 'permissions':
          return <PermissionsScreen onRequest={requestPermissions} />;
        case 'baseline':
          return <BaselineScreen />;
        case 'premium':
          return <PremiumScreen />;
        case 'ready':
          return <ReadyScreen onStart={handleComplete} />;
        default:
          return <View style={styles.screenContainer} />;
      }
    },
    [disclaimerAcknowledged, handleAcknowledge, goNext, requestPermissions, handleComplete],
  );

  const isFirstScreen = currentIndex === 0;
  const isLastScreen = currentIndex === STEPS.length - 1;
  const isPremiumScreen = STEPS[currentIndex] === 'premium';
  const isReadyScreen = STEPS[currentIndex] === 'ready';
  const isWelcome = STEPS[currentIndex] === 'welcome';
  const showSkip = !isWelcome && !isPremiumScreen && !isReadyScreen && currentIndex < PREMIUM_INDEX;
  const showNext =
    !isWelcome &&
    !isReadyScreen &&
    STEPS[currentIndex] !== 'permissions'; // permissions has its own button

  return (
    <View style={styles.container}>
      <FlatList
        ref={flatListRef}
        data={STEPS}
        renderItem={renderItem}
        keyExtractor={(item) => item}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        scrollEnabled={STEPS[currentIndex] !== 'welcome'} // welcome = tap only
        bounces={false}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={viewabilityConfig}
        getItemLayout={(_, index) => ({
          length: SCREEN_WIDTH,
          offset: SCREEN_WIDTH * index,
          index,
        })}
      />

      {/* Bottom controls overlay */}
      {!isWelcome && (
        <View style={styles.bottomBar}>
          {/* Progress dots */}
          <View style={styles.dotsContainer}>
            {STEPS.map((_, i) => {
              const isActive = i === currentIndex;
              return (
                <View
                  key={i}
                  style={[
                    styles.dot,
                    isActive && styles.dotActive,
                    i < currentIndex && styles.dotCompleted,
                  ]}
                />
              );
            })}
          </View>

          {/* Action buttons */}
          <View style={styles.buttonRow}>
            {showSkip && (
              <TouchableOpacity onPress={goSkip} style={styles.skipBtn}>
                <Text style={styles.skipText}>Skip</Text>
              </TouchableOpacity>
            )}

            {showNext && (
              <TouchableOpacity onPress={goNext} activeOpacity={0.8} style={styles.nextBtnWrap}>
                <LinearGradient
                  colors={[colors.accent.primary, colors.accent.secondary]}
                  style={styles.nextBtn}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  <Text style={styles.nextBtnText}>
                    {isPremiumScreen ? 'Start Free Trial' : 'Continue'}
                  </Text>
                  <Ionicons name="arrow-forward" size={18} color={colors.text.primary} />
                </LinearGradient>
              </TouchableOpacity>
            )}

            {isPremiumScreen && (
              <TouchableOpacity onPress={goNext} activeOpacity={0.8} style={styles.nextBtnWrap}>
                <LinearGradient
                  colors={[colors.accent.primary, colors.accent.secondary]}
                  style={styles.nextBtn}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  <Text style={styles.nextBtnText}>Continue Free</Text>
                  <Ionicons name="arrow-forward" size={18} color={colors.text.primary} />
                </LinearGradient>
              </TouchableOpacity>
            )}
          </View>
        </View>
      )}
    </View>
  );
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg.primary,
  },
  screenContainer: {
    width: SCREEN_WIDTH,
    flex: 1,
    paddingHorizontal: spacing.lg,
    paddingTop: SCREEN_HEIGHT * 0.1,
    paddingBottom: 140,
    justifyContent: 'flex-start',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
  },

  // Welcome
  glowCircle: {
    position: 'absolute',
    width: 260,
    height: 260,
    borderRadius: 130,
  },
  glowGradient: {
    width: '100%',
    height: '100%',
    borderRadius: 130,
  },
  heroTitle: {
    ...typography.hero,
    fontSize: 48,
    color: colors.text.primary,
    marginTop: spacing.xl,
    letterSpacing: 2,
  },
  heroTagline: {
    ...typography.h2,
    color: colors.accent.primary,
    marginTop: spacing.sm,
    letterSpacing: 4,
    textTransform: 'uppercase',
    fontSize: 14,
    fontWeight: '500',
  },
  tapHint: {
    ...typography.caption,
    color: colors.text.tertiary,
    marginTop: spacing.xxl,
    letterSpacing: 1,
  },

  // Section titles
  sectionTitle: {
    ...typography.h1,
    color: colors.text.primary,
    marginBottom: spacing.sm,
  },
  sectionSubtitle: {
    ...typography.body,
    color: colors.text.secondary,
    marginBottom: spacing.lg,
  },
  bodyText: {
    ...typography.body,
    color: colors.text.secondary,
    marginVertical: spacing.md,
    lineHeight: 24,
  },
  bodyTextSmall: {
    ...typography.caption,
    color: colors.text.tertiary,
    marginTop: spacing.lg,
    lineHeight: 20,
    textAlign: 'center',
  },

  // How It Works cards
  cardsRow: {
    gap: spacing.md,
    marginTop: spacing.md,
  },
  howCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    padding: spacing.lg,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  howCardGrad: {
    ...StyleSheet.absoluteFillObject,
  },
  howCardTitle: {
    ...typography.h3,
    marginTop: spacing.sm,
  },
  howCardDesc: {
    ...typography.caption,
    color: colors.text.secondary,
    marginTop: spacing.xs,
    lineHeight: 18,
  },

  // Icon badge
  iconBadge: {
    width: 56,
    height: 56,
    borderRadius: 28,
    borderWidth: 1.5,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.bg.secondary,
  },

  // Science
  scienceBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radii.full,
    marginBottom: spacing.lg,
    gap: spacing.sm,
  },
  scienceBadgeText: {
    ...typography.caption,
    color: colors.accent.primary,
    fontWeight: '600',
  },
  scienceRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginTop: spacing.md,
    gap: spacing.md,
  },
  scienceDot: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.accent.primary + '10',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scienceText: {
    ...typography.caption,
    color: colors.text.secondary,
    flex: 1,
    lineHeight: 20,
    paddingTop: 2,
  },

  // Demo visual
  demoVisual: {
    alignItems: 'center',
    marginVertical: spacing.xl,
  },
  demoCircle: {
    width: 180,
    height: 180,
    borderRadius: 90,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: colors.accent.primary + '20',
  },
  landmarkDot: {
    position: 'absolute',
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.accent.secondary,
    opacity: 0.8,
  },

  // Tip box
  tipBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.accent.warning + '10',
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.sm,
    marginTop: spacing.md,
  },
  tipText: {
    ...typography.caption,
    color: colors.accent.warning,
    flex: 1,
    lineHeight: 18,
  },

  // Waveform
  waveformContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: 80,
  },

  // Multi-modal converging lines
  convergingContainer: {
    width: 200,
    height: 200,
    alignSelf: 'center',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: spacing.lg,
  },
  convergeLine: {
    position: 'absolute',
    width: 100,
    height: 2,
    borderRadius: 1,
  },
  convergeCenter: {
    width: 32,
    height: 32,
    borderRadius: 16,
    overflow: 'hidden',
  },
  convergeCenterGrad: {
    width: '100%',
    height: '100%',
  },
  multiIcons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: spacing.lg,
  },
  multiItem: {
    alignItems: 'center',
    gap: spacing.xs,
  },
  multiLabel: {
    ...typography.caption,
    fontWeight: '600',
  },

  // Accuracy
  accuracyCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    marginTop: spacing.md,
  },
  accuracyLabel: {
    ...typography.bodyBold,
    color: colors.text.primary,
    marginBottom: spacing.sm,
  },
  accuracyBarBg: {
    height: 8,
    backgroundColor: colors.bg.elevated,
    borderRadius: 4,
    overflow: 'hidden',
  },
  accuracyBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  accuracyValue: {
    ...typography.caption,
    color: colors.text.secondary,
    marginTop: spacing.xs,
    textAlign: 'right',
  },

  // Use cases grid
  useCaseGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
    marginTop: spacing.lg,
  },
  useCaseCard: {
    width: (SCREEN_WIDTH - spacing.lg * 2 - spacing.md) / 2,
    borderRadius: radii.lg,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  useCaseInner: {
    paddingVertical: spacing.lg,
    paddingHorizontal: spacing.md,
    alignItems: 'center',
    gap: spacing.sm,
  },
  useCaseLabel: {
    ...typography.caption,
    color: colors.text.primary,
    fontWeight: '600',
    textAlign: 'center',
  },

  // Disclaimer
  disclaimerIcon: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.accent.warning + '10',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  disclaimerBox: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.accent.warning + '20',
    marginVertical: spacing.md,
  },
  disclaimerText: {
    ...typography.caption,
    color: colors.text.secondary,
    lineHeight: 20,
  },
  acknowledgeBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    padding: spacing.md,
    borderRadius: radii.md,
    backgroundColor: colors.bg.card,
    marginTop: spacing.md,
  },
  acknowledgeBtnActive: {
    borderColor: colors.accent.success,
    borderWidth: 1,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: colors.accent.primary,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.bg.secondary,
  },
  acknowledgeText: {
    ...typography.caption,
    color: colors.text.primary,
    flex: 1,
    lineHeight: 18,
  },

  // Permissions
  permRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.md,
    marginTop: spacing.lg,
  },
  permIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  permTextBlock: {
    flex: 1,
  },
  permTitle: {
    ...typography.bodyBold,
    color: colors.text.primary,
  },
  permDesc: {
    ...typography.caption,
    color: colors.text.secondary,
    marginTop: spacing.xs,
    lineHeight: 18,
  },
  permButton: {
    marginTop: spacing.xl,
    borderRadius: radii.md,
    overflow: 'hidden',
  },
  permButtonGrad: {
    paddingVertical: spacing.md,
    alignItems: 'center',
    borderRadius: radii.md,
  },
  permButtonText: {
    ...typography.bodyBold,
    color: colors.text.primary,
  },
  privacyNote: {
    ...typography.small,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginTop: spacing.md,
  },

  // Baseline
  baselineVisual: {
    alignItems: 'center',
    marginVertical: spacing.xl,
  },
  baselineCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: colors.accent.primary + '15',
  },
  baselineTips: {
    marginTop: spacing.lg,
    gap: spacing.md,
  },
  baselineTipRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  baselineTipNum: {
    ...typography.h3,
    color: colors.accent.primary,
    width: 28,
    textAlign: 'center',
  },
  baselineTipText: {
    ...typography.body,
    color: colors.text.secondary,
    flex: 1,
  },

  // Premium
  premiumTitle: {
    ...typography.h1,
    color: colors.text.primary,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  premiumFeatures: {
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  featureText: {
    ...typography.body,
    color: colors.text.primary,
  },
  planCards: {
    flexDirection: 'row',
    gap: spacing.md,
    marginBottom: spacing.md,
  },
  planCard: {
    flex: 1,
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    padding: spacing.lg,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  planCardHighlighted: {
    flex: 1,
    borderRadius: radii.lg,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: colors.accent.primary,
    position: 'relative',
  },
  planCardHighlightedInner: {
    padding: spacing.lg,
    alignItems: 'center',
  },
  saveBadge: {
    position: 'absolute',
    top: -1,
    right: -1,
    backgroundColor: colors.accent.primary,
    paddingHorizontal: spacing.sm,
    paddingVertical: 3,
    borderBottomLeftRadius: radii.sm,
    borderTopRightRadius: radii.md,
    zIndex: 10,
  },
  saveBadgeText: {
    ...typography.small,
    color: colors.bg.primary,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  planName: {
    ...typography.caption,
    color: colors.text.secondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: spacing.xs,
  },
  planPrice: {
    ...typography.h1,
    color: colors.text.primary,
  },
  planPriceHighlighted: {
    ...typography.h1,
    color: colors.accent.primary,
  },
  planPeriod: {
    ...typography.caption,
    color: colors.text.tertiary,
  },
  planEquiv: {
    ...typography.small,
    color: colors.accent.primary,
    marginTop: spacing.xs,
    fontWeight: '600',
  },
  freeTierBox: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    marginTop: spacing.sm,
  },
  freeTierTitle: {
    ...typography.caption,
    color: colors.text.secondary,
    fontWeight: '600',
    marginBottom: spacing.xs,
  },
  freeTierItem: {
    ...typography.small,
    color: colors.text.tertiary,
    marginTop: 2,
  },
  noPaymentText: {
    ...typography.caption,
    color: colors.accent.success,
    textAlign: 'center',
    marginTop: spacing.md,
  },
  restoreText: {
    ...typography.small,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginTop: spacing.sm,
    textDecorationLine: 'underline',
  },

  // Ready
  readyTitle: {
    ...typography.h1,
    color: colors.text.primary,
    marginTop: spacing.xl,
    textAlign: 'center',
  },
  readySubtitle: {
    ...typography.body,
    color: colors.text.secondary,
    marginTop: spacing.sm,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  checkCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    overflow: 'hidden',
  },
  checkGradient: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.md + 2,
    borderRadius: radii.md,
    gap: spacing.sm,
  },
  startButtonText: {
    ...typography.bodyBold,
    color: colors.text.primary,
    letterSpacing: 0.5,
  },

  // Bottom bar
  bottomBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    paddingBottom: Platform.OS === 'ios' ? 40 : 24,
    paddingTop: spacing.md,
    paddingHorizontal: spacing.lg,
    backgroundColor: colors.bg.primary + 'F0',
  },
  dotsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 6,
    marginBottom: spacing.md,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.bg.elevated,
  },
  dotActive: {
    width: 24,
    backgroundColor: colors.accent.primary,
  },
  dotCompleted: {
    backgroundColor: colors.accent.primary + '50',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  skipBtn: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
  },
  skipText: {
    ...typography.caption,
    color: colors.text.tertiary,
  },
  nextBtnWrap: {
    flex: 1,
    marginLeft: spacing.md,
    borderRadius: radii.md,
    overflow: 'hidden',
  },
  nextBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm + 4,
    borderRadius: radii.md,
    gap: spacing.sm,
  },
  nextBtnText: {
    ...typography.bodyBold,
    color: colors.text.primary,
  },
});
