import React, { useState, useRef, useCallback, useMemo, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Animated,
  Dimensions,
  Platform,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAppDispatch } from '../store/hooks';
import {
  completeOnboarding,
  setGender,
  setAge,
  setHeightCm,
  setWeightKg,
  setGoalWeight,
  setGoal,
  setActivityLevel,
  setDietPreference,
  setGoalTimeline,
  setCalculatedNutrition,
} from '../store/userSlice';
import type { Gender, Goal, ActivityLevel, DietPreference, GoalTimeline } from '../store/userSlice';
import { setDailyGoal } from '../store/nutritionSlice';
import { setPremiumStatus } from '../store/subscriptionSlice';
import { Theme } from '../utils/theme';
import { haptics } from '../utils/haptics';
import {
  calculateFullPlan,
  feetInchesToCm,
  lbsToKg,
  estimateWeeksToGoal,
  getProjectedDate,
} from '../utils/nutrition';
import { purchasePackage, getOfferings, restorePurchases, PurchaseCancelledError } from '../services/purchases';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const TOTAL_STEPS = 14;

interface OnboardingFlowProps {
  onComplete: () => void;
}

// ─── Types ────────────────────────────────────────────────────────────────────

type GoalOption = {
  key: Goal | 'healthier';
  label: string;
  icon: keyof typeof Ionicons.glyphMap;
  desc: string;
};

type ActivityOption = {
  key: ActivityLevel;
  label: string;
  desc: string;
  icon: keyof typeof Ionicons.glyphMap;
};

type DietOption = {
  key: DietPreference;
  label: string;
  icon: keyof typeof Ionicons.glyphMap;
};

type TimelineOption = {
  key: GoalTimeline;
  label: string;
  weeks: number;
};

type PlanKey = 'yearly' | 'monthly';

// ─── Constants ────────────────────────────────────────────────────────────────

const GOAL_OPTIONS: GoalOption[] = [
  { key: 'lose', label: 'Lose weight', icon: 'trending-down', desc: 'Burn fat and get lean' },
  { key: 'gain', label: 'Gain muscle', icon: 'trending-up', desc: 'Build strength and size' },
  { key: 'maintain', label: 'Maintain weight', icon: 'swap-horizontal', desc: 'Stay where you are' },
  { key: 'healthier', label: 'Eat healthier', icon: 'leaf', desc: 'Better nutrition habits' },
];

const ACTIVITY_OPTIONS: ActivityOption[] = [
  { key: 'sedentary', label: 'Sedentary', desc: 'Desk job, little exercise', icon: 'desktop-outline' },
  { key: 'light', label: 'Lightly active', desc: 'Light exercise 1-3 days/week', icon: 'walk-outline' },
  { key: 'moderate', label: 'Moderately active', desc: 'Moderate exercise 3-5 days/week', icon: 'bicycle-outline' },
  { key: 'very_active', label: 'Very active', desc: 'Hard exercise 6-7 days/week', icon: 'barbell-outline' },
];

const DIET_OPTIONS: DietOption[] = [
  { key: 'none', label: 'No preference', icon: 'restaurant-outline' },
  { key: 'vegetarian', label: 'Vegetarian', icon: 'leaf-outline' },
  { key: 'vegan', label: 'Vegan', icon: 'flower-outline' },
  { key: 'keto', label: 'Keto', icon: 'flame-outline' },
  { key: 'paleo', label: 'Paleo', icon: 'fish-outline' },
  { key: 'gluten_free', label: 'Gluten-free', icon: 'nutrition-outline' },
];

const TIMELINE_OPTIONS: TimelineOption[] = [
  { key: '1_month', label: '1 month', weeks: 4 },
  { key: '3_months', label: '3 months', weeks: 13 },
  { key: '6_months', label: '6 months', weeks: 26 },
  { key: '1_year', label: '1 year', weeks: 52 },
];

const PAYWALL_FEATURES = [
  { icon: 'camera' as const, label: 'Unlimited AI food scans' },
  { icon: 'nutrition' as const, label: 'Detailed macro tracking' },
  { icon: 'calendar' as const, label: 'Personalized meal planning' },
  { icon: 'analytics' as const, label: 'Progress insights & trends' },
];

const SHOWCASE_FEATURES = [
  { icon: 'camera' as const, title: 'AI Food Scan', desc: 'Point your camera at any meal' },
  { icon: 'barcode' as const, title: 'Barcode Scan', desc: 'Scan packaged food labels' },
  { icon: 'time' as const, title: 'Meal History', desc: 'Track everything you eat' },
  { icon: 'trending-up' as const, title: 'Progress Tracking', desc: 'Watch your journey unfold' },
  { icon: 'pie-chart' as const, title: 'Macro Breakdown', desc: 'Protein, carbs, and fat' },
];

const TESTIMONIALS = [
  { name: 'Sarah M.', text: 'Lost 22 lbs in 3 months just by scanning my meals.', stars: 5 },
  { name: 'James K.', text: 'So much easier than manually logging everything.', stars: 5 },
  { name: 'Priya R.', text: 'The AI accuracy is unreal. Saved me hours every week.', stars: 5 },
];

// ─── Main Component ───────────────────────────────────────────────────────────

const OnboardingFlow = ({ onComplete }: OnboardingFlowProps): React.JSX.Element => {
  const dispatch = useAppDispatch();
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const slideAnim = useRef(new Animated.Value(0)).current;
  const progressAnim = useRef(new Animated.Value(0)).current;

  // ── Step state ──
  const [step, setStep] = useState(0);

  // ── User data ──
  const [selectedGoal, setSelectedGoal] = useState<Goal | 'healthier' | null>(null);
  const [heightFeet, setHeightFeet] = useState(5);
  const [heightInches, setHeightInches] = useState(10);
  const [weightLbs, setWeightLbs] = useState(170);
  const [targetWeightLbs, setTargetWeightLbs] = useState(155);
  const [selectedTimeline, setSelectedTimeline] = useState<GoalTimeline>('3_months');
  const [selectedActivity, setSelectedActivity] = useState<ActivityLevel | null>(null);
  const [selectedDiet, setSelectedDiet] = useState<DietPreference>('none');

  // ── Paywall state ──
  const [selectedPlan, setSelectedPlan] = useState<PlanKey>('yearly');
  const [purchasing, setPurchasing] = useState(false);
  const [showRescue, setShowRescue] = useState(false);

  // ── Notification state ──
  const [notifRequested, setNotifRequested] = useState(false);

  // ── Calculating animation state ──
  const calcPulse = useRef(new Animated.Value(0)).current;

  // ── Derived: effective goal (map 'healthier' to 'maintain') ──
  const effectiveGoal: Goal = selectedGoal === 'healthier' ? 'maintain' : (selectedGoal as Goal) ?? 'maintain';

  // ── Calculated plan ──
  const plan = useMemo(() => {
    const heightCm = feetInchesToCm(heightFeet, heightInches);
    const weightKg = lbsToKg(weightLbs);
    // Use male as default for initial calculation; gender not collected in this flow
    return calculateFullPlan('male', 30, heightCm, weightKg, effectiveGoal, selectedActivity ?? 'moderate');
  }, [heightFeet, heightInches, weightLbs, effectiveGoal, selectedActivity]);

  const projectedWeeks = useMemo(() => {
    if (effectiveGoal === 'maintain') return 0;
    const currentKg = lbsToKg(weightLbs);
    const targetKg = lbsToKg(targetWeightLbs);
    return estimateWeeksToGoal(currentKg, targetKg, effectiveGoal);
  }, [weightLbs, targetWeightLbs, effectiveGoal]);

  const projectedDate = useMemo(() => getProjectedDate(projectedWeeks), [projectedWeeks]);

  const weeklyRate = useMemo(() => {
    if (effectiveGoal === 'lose') return 1.0; // lbs/week
    if (effectiveGoal === 'gain') return 0.5;
    return 0;
  }, [effectiveGoal]);

  // ── Macro percentages for pie chart ──
  const macroPercentages = useMemo(() => {
    const totalCals = plan.protein * 4 + plan.carbs * 4 + plan.fat * 9;
    if (totalCals === 0) return { protein: 33, carbs: 34, fat: 33 };
    return {
      protein: Math.round((plan.protein * 4 / totalCals) * 100),
      carbs: Math.round((plan.carbs * 4 / totalCals) * 100),
      fat: Math.round((plan.fat * 9 / totalCals) * 100),
    };
  }, [plan]);

  // ── Weight projection points for graph ──
  const weightProjection = useMemo(() => {
    const points: { week: number; weight: number }[] = [];
    const totalWeeks = TIMELINE_OPTIONS.find(t => t.key === selectedTimeline)?.weeks ?? 13;
    const diff = targetWeightLbs - weightLbs;
    for (let w = 0; w <= totalWeeks; w++) {
      const progress = w / totalWeeks;
      // Smooth exponential curve (fast at start, plateaus)
      const eased = 1 - Math.pow(1 - progress, 2);
      points.push({ week: w, weight: Math.round(weightLbs + diff * eased) });
    }
    return points;
  }, [weightLbs, targetWeightLbs, selectedTimeline]);

  // ── Progress bar animation ──
  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: (step + 1) / TOTAL_STEPS,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [step, progressAnim]);

  // ── Transition animation ──
  const animateTransition = useCallback(
    (direction: 'forward' | 'back', cb: () => void) => {
      const out = direction === 'forward' ? -SCREEN_WIDTH : SCREEN_WIDTH;
      const enter = direction === 'forward' ? SCREEN_WIDTH : -SCREEN_WIDTH;

      Animated.parallel([
        Animated.timing(fadeAnim, { toValue: 0, duration: 150, useNativeDriver: true }),
        Animated.timing(slideAnim, { toValue: out, duration: 150, useNativeDriver: true }),
      ]).start(() => {
        cb();
        slideAnim.setValue(enter);
        Animated.parallel([
          Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true }),
          Animated.timing(slideAnim, { toValue: 0, duration: 200, useNativeDriver: true }),
        ]).start();
      });
    },
    [fadeAnim, slideAnim],
  );

  // ── Navigation ──
  const goNext = useCallback(() => {
    haptics.light();
    animateTransition('forward', () => setStep((s: number) => Math.min(s + 1, TOTAL_STEPS - 1)));
  }, [animateTransition]);

  const goBack = useCallback(() => {
    if (step === 0) return;
    haptics.light();
    animateTransition('back', () => setStep((s: number) => Math.max(s - 1, 0)));
  }, [step, animateTransition]);

  // ── Dispatch all data to Redux + AsyncStorage ──
  const saveOnboardingData = useCallback(async () => {
    const heightCm = feetInchesToCm(heightFeet, heightInches);
    const weightKg = lbsToKg(weightLbs);
    const targetKg = lbsToKg(targetWeightLbs);

    dispatch(setGoal(effectiveGoal));
    dispatch(setHeightCm(heightCm));
    dispatch(setWeightKg(weightKg));
    dispatch(setGoalWeight(targetKg));
    dispatch(setActivityLevel(selectedActivity ?? 'moderate'));
    dispatch(setDietPreference(selectedDiet));
    dispatch(setGoalTimeline(selectedTimeline));
    dispatch(setCalculatedNutrition({
      dailyCalories: plan.dailyCalories,
      proteinGoal: plan.protein,
      carbGoal: plan.carbs,
      fatGoal: plan.fat,
    }));
    dispatch(setDailyGoal({
      calories: plan.dailyCalories,
      protein: plan.protein,
      carbs: plan.carbs,
      fat: plan.fat,
    }));
    dispatch(completeOnboarding());

    // Persist to AsyncStorage
    try {
      await AsyncStorage.setItem('@nutrisnap_onboarding', JSON.stringify({
        goal: effectiveGoal,
        heightFeet,
        heightInches,
        weightLbs,
        targetWeightLbs,
        timeline: selectedTimeline,
        activity: selectedActivity,
        diet: selectedDiet,
        plan,
        completedAt: new Date().toISOString(),
      }));
      await AsyncStorage.setItem('@nutrisnap_onboarding_complete', 'true');
    } catch (e) {
      console.warn('[Onboarding] AsyncStorage save error:', e);
    }
  }, [dispatch, heightFeet, heightInches, weightLbs, targetWeightLbs, effectiveGoal, selectedActivity, selectedDiet, selectedTimeline, plan]);

  // ── Purchase handler ──
  const handlePurchase = useCallback(async () => {
    haptics.medium();
    setPurchasing(true);
    try {
      const offerings = await getOfferings();
      if (!offerings) throw new Error('No offerings');
      const pkg = selectedPlan === 'yearly' ? offerings.annual : offerings.monthly;
      if (!pkg) throw new Error('No package');
      await purchasePackage(pkg);
      dispatch(setPremiumStatus(true));
      await saveOnboardingData();
      onComplete();
    } catch (error) {
      if (error instanceof PurchaseCancelledError) {
        // User cancelled
      } else {
        Alert.alert('Purchase Error', 'Something went wrong. Please try again.');
      }
    } finally {
      setPurchasing(false);
    }
  }, [selectedPlan, dispatch, saveOnboardingData, onComplete]);

  // ── Rescue purchase (discounted yearly) ──
  const handleRescuePurchase = useCallback(async () => {
    haptics.medium();
    setPurchasing(true);
    try {
      const offerings = await getOfferings();
      if (!offerings) throw new Error('No offerings');
      const pkg = offerings.annual;
      if (!pkg) throw new Error('No package');
      await purchasePackage(pkg);
      dispatch(setPremiumStatus(true));
      await saveOnboardingData();
      onComplete();
    } catch (error) {
      if (!(error instanceof PurchaseCancelledError)) {
        Alert.alert('Purchase Error', 'Something went wrong. Please try again.');
      }
    } finally {
      setPurchasing(false);
    }
  }, [dispatch, saveOnboardingData, onComplete]);

  // ── Skip paywall (decline) ──
  const handleDeclinePaywall = useCallback(async () => {
    haptics.light();
    if (!showRescue) {
      setShowRescue(true);
      return;
    }
    // Second decline: save data and go to app
    await saveOnboardingData();
    onComplete();
  }, [showRescue, saveOnboardingData, onComplete]);

  // ── Can advance from current step? ──
  const canAdvance = useMemo((): boolean => {
    switch (step) {
      case 0: return true; // Welcome
      case 1: return selectedGoal !== null; // Goal
      case 2: return true; // Stats (always has defaults)
      case 3: return true; // Target
      case 4: return selectedActivity !== null; // Activity
      case 5: return true; // Diet (always has default)
      case 6: return true; // Validation
      case 7: return true; // Calorie breakdown
      case 8: return true; // Social proof
      case 9: return true; // Magic moment
      case 10: return true; // Feature showcase
      case 11: return true; // Notification
      case 12: return true; // Plan ready
      case 13: return true; // Paywall
      default: return true;
    }
  }, [step, selectedGoal, selectedActivity]);

  // ─── Render Functions ───────────────────────────────────────────────────────

  // === SCREEN 0: Welcome ===
  const renderWelcome = () => (
    <View style={s.screenContainer}>
      <View style={s.welcomeIllustration}>
        <LinearGradient
          colors={['rgba(46, 213, 115, 0.15)', 'rgba(46, 213, 115, 0.03)']}
          style={s.illustrationCircle}
        >
          <Ionicons name="scan" size={72} color={Theme.colors.primary} />
          <View style={s.foodIcons}>
            <Text style={s.foodEmoji}>🥗</Text>
            <Text style={[s.foodEmoji, { marginTop: -10 }]}>🍎</Text>
            <Text style={s.foodEmoji}>🥑</Text>
          </View>
        </LinearGradient>
      </View>
      <Text style={s.heroTitle}>Track calories{'\n'}effortlessly with AI</Text>
      <Text style={s.heroSubtitle}>
        Just snap a photo of your food.{'\n'}NutriSnap identifies it instantly.
      </Text>
      <View style={s.welcomeBadges}>
        <View style={s.welcomeBadge}>
          <Ionicons name="flash" size={16} color={Theme.colors.primary} />
          <Text style={s.badgeText}>Instant AI scan</Text>
        </View>
        <View style={s.welcomeBadge}>
          <Ionicons name="checkmark-circle" size={16} color={Theme.colors.primary} />
          <Text style={s.badgeText}>95% accuracy</Text>
        </View>
        <View style={s.welcomeBadge}>
          <Ionicons name="people" size={16} color={Theme.colors.primary} />
          <Text style={s.badgeText}>50K+ users</Text>
        </View>
      </View>
      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Get Started</Text>
        <Ionicons name="arrow-forward" size={20} color="#000" />
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 1: Goal ===
  const renderGoal = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>What's your goal?</Text>
      <Text style={s.screenSubtitle}>We'll personalize your experience</Text>
      <View style={s.optionsGrid}>
        {GOAL_OPTIONS.map(opt => (
          <TouchableOpacity
            key={opt.key}
            style={[s.optionCard, selectedGoal === opt.key && s.optionCardSelected]}
            onPress={() => { haptics.selection(); setSelectedGoal(opt.key); }}
            activeOpacity={0.8}
          >
            <View style={[s.optionIconWrap, selectedGoal === opt.key && s.optionIconWrapSelected]}>
              <Ionicons name={opt.icon} size={28} color={selectedGoal === opt.key ? '#000' : Theme.colors.primary} />
            </View>
            <Text style={[s.optionLabel, selectedGoal === opt.key && s.optionLabelSelected]}>{opt.label}</Text>
            <Text style={s.optionDesc}>{opt.desc}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <TouchableOpacity
        style={[s.primaryButton, !canAdvance && s.primaryButtonDisabled]}
        onPress={goNext}
        disabled={!canAdvance}
        activeOpacity={0.85}
      >
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 2: Current Stats ===
  const renderStats = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Your current stats</Text>
      <Text style={s.screenSubtitle}>This helps us calculate your nutrition needs</Text>

      {/* Height */}
      <View style={s.inputSection}>
        <Text style={s.inputLabel}>Height</Text>
        <View style={s.pickerRow}>
          <View style={s.pickerUnit}>
            <TouchableOpacity style={s.pickerBtn} onPress={() => setHeightFeet((f: number) => Math.max(4, f - 1))}>
              <Ionicons name="remove" size={24} color={Theme.colors.primary} />
            </TouchableOpacity>
            <Text style={s.pickerValue}>{heightFeet}'</Text>
            <TouchableOpacity style={s.pickerBtn} onPress={() => setHeightFeet((f: number) => Math.min(7, f + 1))}>
              <Ionicons name="add" size={24} color={Theme.colors.primary} />
            </TouchableOpacity>
          </View>
          <View style={s.pickerUnit}>
            <TouchableOpacity style={s.pickerBtn} onPress={() => setHeightInches((i: number) => Math.max(0, i - 1))}>
              <Ionicons name="remove" size={24} color={Theme.colors.primary} />
            </TouchableOpacity>
            <Text style={s.pickerValue}>{heightInches}"</Text>
            <TouchableOpacity style={s.pickerBtn} onPress={() => setHeightInches((i: number) => Math.min(11, i + 1))}>
              <Ionicons name="add" size={24} color={Theme.colors.primary} />
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* Current Weight */}
      <View style={s.inputSection}>
        <Text style={s.inputLabel}>Current Weight</Text>
        <View style={s.weightPicker}>
          <TouchableOpacity style={s.weightBtn} onPress={() => setWeightLbs((w: number) => Math.max(80, w - 5))}>
            <Ionicons name="remove-circle" size={36} color={Theme.colors.primary} />
          </TouchableOpacity>
          <View style={s.weightDisplay}>
            <Text style={s.weightValue}>{weightLbs}</Text>
            <Text style={s.weightUnit}>lbs</Text>
          </View>
          <TouchableOpacity style={s.weightBtn} onPress={() => setWeightLbs((w: number) => Math.min(400, w + 5))}>
            <Ionicons name="add-circle" size={36} color={Theme.colors.primary} />
          </TouchableOpacity>
        </View>
      </View>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 3: Target Weight + Timeline ===
  const renderTarget = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Your target</Text>
      <Text style={s.screenSubtitle}>
        {effectiveGoal === 'lose' ? "What's your goal weight?" : effectiveGoal === 'gain' ? 'What weight do you want to reach?' : "Let's set a healthy target"}
      </Text>

      <View style={s.inputSection}>
        <Text style={s.inputLabel}>Target Weight</Text>
        <View style={s.weightPicker}>
          <TouchableOpacity style={s.weightBtn} onPress={() => setTargetWeightLbs((w: number) => Math.max(80, w - 5))}>
            <Ionicons name="remove-circle" size={36} color={Theme.colors.primary} />
          </TouchableOpacity>
          <View style={s.weightDisplay}>
            <Text style={s.weightValue}>{targetWeightLbs}</Text>
            <Text style={s.weightUnit}>lbs</Text>
          </View>
          <TouchableOpacity style={s.weightBtn} onPress={() => setTargetWeightLbs((w: number) => Math.min(400, w + 5))}>
            <Ionicons name="add-circle" size={36} color={Theme.colors.primary} />
          </TouchableOpacity>
        </View>
      </View>

      <View style={s.inputSection}>
        <Text style={s.inputLabel}>When do you want to reach it?</Text>
        <View style={s.timelineRow}>
          {TIMELINE_OPTIONS.map(opt => (
            <TouchableOpacity
              key={opt.key}
              style={[s.timelineChip, selectedTimeline === opt.key && s.timelineChipSelected]}
              onPress={() => { haptics.selection(); setSelectedTimeline(opt.key); }}
            >
              <Text style={[s.timelineChipText, selectedTimeline === opt.key && s.timelineChipTextSelected]}>
                {opt.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 4: Activity Level ===
  const renderActivity = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>How active are you?</Text>
      <Text style={s.screenSubtitle}>This affects your daily calorie needs</Text>
      <View style={s.listOptions}>
        {ACTIVITY_OPTIONS.map(opt => (
          <TouchableOpacity
            key={opt.key}
            style={[s.listOption, selectedActivity === opt.key && s.listOptionSelected]}
            onPress={() => { haptics.selection(); setSelectedActivity(opt.key); }}
            activeOpacity={0.8}
          >
            <View style={[s.listOptionIcon, selectedActivity === opt.key && s.listOptionIconSelected]}>
              <Ionicons name={opt.icon} size={24} color={selectedActivity === opt.key ? '#000' : Theme.colors.primary} />
            </View>
            <View style={s.listOptionText}>
              <Text style={[s.listOptionTitle, selectedActivity === opt.key && s.listOptionTitleSelected]}>{opt.label}</Text>
              <Text style={s.listOptionDesc}>{opt.desc}</Text>
            </View>
            {selectedActivity === opt.key && (
              <Ionicons name="checkmark-circle" size={24} color={Theme.colors.primary} />
            )}
          </TouchableOpacity>
        ))}
      </View>
      <TouchableOpacity
        style={[s.primaryButton, !canAdvance && s.primaryButtonDisabled]}
        onPress={goNext}
        disabled={!canAdvance}
        activeOpacity={0.85}
      >
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 5: Diet Preference ===
  const renderDiet = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Any dietary preferences?</Text>
      <Text style={s.screenSubtitle}>We'll tailor food suggestions for you</Text>
      <View style={s.dietGrid}>
        {DIET_OPTIONS.map(opt => (
          <TouchableOpacity
            key={opt.key}
            style={[s.dietChip, selectedDiet === opt.key && s.dietChipSelected]}
            onPress={() => { haptics.selection(); setSelectedDiet(opt.key); }}
            activeOpacity={0.8}
          >
            <Ionicons
              name={opt.icon}
              size={22}
              color={selectedDiet === opt.key ? '#000' : Theme.colors.textSecondary}
            />
            <Text style={[s.dietChipText, selectedDiet === opt.key && s.dietChipTextSelected]}>{opt.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 6: Validation (Goal Achievable + Weight Graph) ===
  const renderValidation = () => {
    const timelineWeeks = TIMELINE_OPTIONS.find(t => t.key === selectedTimeline)?.weeks ?? 13;
    const diffLbs = Math.abs(weightLbs - targetWeightLbs);
    const ratePerWeek = diffLbs / timelineWeeks;
    const isAchievable = effectiveGoal === 'maintain' || ratePerWeek <= 2.0;

    return (
      <View style={s.screenContainer}>
        <View style={s.validationBadge}>
          <LinearGradient colors={['#2ED57333', '#2ED57311']} style={s.validationBadgeInner}>
            <Ionicons name="checkmark-circle" size={48} color={Theme.colors.primary} />
          </LinearGradient>
        </View>
        <Text style={s.screenTitle}>
          {isAchievable ? 'Your goal is achievable!' : 'Ambitious but doable!'}
        </Text>
        <Text style={s.screenSubtitle}>
          {effectiveGoal === 'maintain'
            ? `We'll help you maintain ${weightLbs} lbs with balanced nutrition`
            : `${effectiveGoal === 'lose' ? 'Lose' : 'Gain'} ${diffLbs} lbs in ${TIMELINE_OPTIONS.find(t => t.key === selectedTimeline)?.label ?? '3 months'}`}
        </Text>

        {/* Weight projection graph */}
        {effectiveGoal !== 'maintain' && (
          <View style={s.graphContainer}>
            <View style={s.graphInner}>
              {/* Y-axis labels */}
              <View style={s.graphYAxis}>
                <Text style={s.graphLabel}>{weightLbs}</Text>
                <Text style={s.graphLabel}>{targetWeightLbs}</Text>
              </View>
              {/* Graph area */}
              <View style={s.graphArea}>
                <View style={s.graphLine}>
                  {weightProjection.map((pt, i) => {
                    const totalPts = weightProjection.length;
                    const minW = Math.min(weightLbs, targetWeightLbs);
                    const maxW = Math.max(weightLbs, targetWeightLbs);
                    const range = maxW - minW || 1;
                    const yPct = ((pt.weight - minW) / range);
                    const invertedY = effectiveGoal === 'lose' ? yPct : 1 - yPct;
                    return (
                      <View
                        key={i}
                        style={[
                          s.graphDot,
                          {
                            left: `${(i / (totalPts - 1)) * 100}%` as any,
                            bottom: `${(1 - invertedY) * 100}%` as any,
                            backgroundColor: i === totalPts - 1 ? Theme.colors.primary : 'rgba(46, 213, 115, 0.5)',
                            width: i === totalPts - 1 ? 10 : 4,
                            height: i === totalPts - 1 ? 10 : 4,
                          },
                        ]}
                      />
                    );
                  })}
                </View>
                {/* X-axis labels */}
                <View style={s.graphXAxis}>
                  <Text style={s.graphLabel}>Now</Text>
                  <Text style={s.graphLabel}>{TIMELINE_OPTIONS.find(t => t.key === selectedTimeline)?.label}</Text>
                </View>
              </View>
            </View>
          </View>
        )}

        <View style={s.validationStats}>
          <View style={s.validationStat}>
            <Text style={s.validationStatValue}>{plan.dailyCalories}</Text>
            <Text style={s.validationStatLabel}>Daily calories</Text>
          </View>
          <View style={s.validationStatDivider} />
          <View style={s.validationStat}>
            <Text style={s.validationStatValue}>{plan.protein}g</Text>
            <Text style={s.validationStatLabel}>Protein</Text>
          </View>
          <View style={s.validationStatDivider} />
          <View style={s.validationStat}>
            <Text style={s.validationStatValue}>
              {effectiveGoal === 'maintain' ? '--' : `${ratePerWeek.toFixed(1)}`}
            </Text>
            <Text style={s.validationStatLabel}>{effectiveGoal === 'maintain' ? 'Balanced' : 'lbs/week'}</Text>
          </View>
        </View>

        <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
          <Text style={s.primaryButtonText}>Continue</Text>
        </TouchableOpacity>
      </View>
    );
  };

  // === SCREEN 7: Calorie Breakdown / Macro Pie Chart ===
  const renderCalorieBreakdown = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Your daily nutrition</Text>
      <Text style={s.screenSubtitle}>Personalized macro split based on your goals</Text>

      {/* Pseudo pie chart using stacked bars */}
      <View style={s.pieContainer}>
        <View style={s.pieCenter}>
          <Text style={s.pieCenterValue}>{plan.dailyCalories}</Text>
          <Text style={s.pieCenterLabel}>cal/day</Text>
        </View>
        <View style={s.pieRing}>
          <View style={[s.pieSegment, { flex: macroPercentages.protein, backgroundColor: Theme.colors.protein }]} />
          <View style={[s.pieSegment, { flex: macroPercentages.carbs, backgroundColor: Theme.colors.carbs }]} />
          <View style={[s.pieSegment, { flex: macroPercentages.fat, backgroundColor: Theme.colors.fat }]} />
        </View>
      </View>

      <View style={s.macroCards}>
        <View style={[s.macroCard, { borderLeftColor: Theme.colors.protein }]}>
          <Text style={s.macroCardValue}>{plan.protein}g</Text>
          <Text style={s.macroCardLabel}>Protein</Text>
          <Text style={s.macroCardPct}>{macroPercentages.protein}%</Text>
        </View>
        <View style={[s.macroCard, { borderLeftColor: Theme.colors.carbs }]}>
          <Text style={s.macroCardValue}>{plan.carbs}g</Text>
          <Text style={s.macroCardLabel}>Carbs</Text>
          <Text style={s.macroCardPct}>{macroPercentages.carbs}%</Text>
        </View>
        <View style={[s.macroCard, { borderLeftColor: Theme.colors.fat }]}>
          <Text style={s.macroCardValue}>{plan.fat}g</Text>
          <Text style={s.macroCardLabel}>Fat</Text>
          <Text style={s.macroCardPct}>{macroPercentages.fat}%</Text>
        </View>
      </View>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 8: Social Proof ===
  const renderSocialProof = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Join 50,000+ users{'\n'}tracking smarter</Text>
      <Text style={s.screenSubtitle}>Real results from real people</Text>

      <View style={s.testimonials}>
        {TESTIMONIALS.map((t, i) => (
          <View key={i} style={s.testimonialCard}>
            <View style={s.testimonialHeader}>
              <View style={s.testimonialAvatar}>
                <Text style={s.testimonialAvatarText}>{t.name[0]}</Text>
              </View>
              <View>
                <Text style={s.testimonialName}>{t.name}</Text>
                <View style={s.starsRow}>
                  {Array.from({ length: t.stars }).map((_, si) => (
                    <Ionicons key={si} name="star" size={14} color="#FFD700" />
                  ))}
                </View>
              </View>
            </View>
            <Text style={s.testimonialText}>"{t.text}"</Text>
          </View>
        ))}
      </View>

      <View style={s.socialProofBanner}>
        <Text style={s.socialProofStat}>4.9 ★</Text>
        <View style={s.socialProofDivider} />
        <Text style={s.socialProofStat}>50K+ users</Text>
        <View style={s.socialProofDivider} />
        <Text style={s.socialProofStat}>#1 AI tracker</Text>
      </View>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 9: Magic Moment (AI scan demo) ===
  const renderMagicMoment = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>See how it works</Text>
      <Text style={s.screenSubtitle}>AI-powered food recognition in seconds</Text>

      <View style={s.demoContainer}>
        {/* Camera viewfinder mockup */}
        <View style={s.cameraFrame}>
          <LinearGradient
            colors={['rgba(46, 213, 115, 0.08)', 'rgba(46, 213, 115, 0.02)']}
            style={s.cameraInner}
          >
            {/* Food emoji in center */}
            <Text style={s.demoFoodEmoji}>🍝</Text>

            {/* Scan corners */}
            <View style={[s.scanCorner, s.scanCornerTL]} />
            <View style={[s.scanCorner, s.scanCornerTR]} />
            <View style={[s.scanCorner, s.scanCornerBL]} />
            <View style={[s.scanCorner, s.scanCornerBR]} />

            {/* Scan line animation visual */}
            <View style={s.scanLine} />
          </LinearGradient>
        </View>

        {/* Detected overlay */}
        <View style={s.detectedOverlay}>
          <View style={s.detectedHeader}>
            <Ionicons name="checkmark-circle" size={20} color={Theme.colors.primary} />
            <Text style={s.detectedTitle}>Spaghetti Bolognese</Text>
          </View>
          <View style={s.detectedMacros}>
            <View style={s.detectedMacro}>
              <Text style={s.detectedMacroValue}>520</Text>
              <Text style={s.detectedMacroLabel}>cal</Text>
            </View>
            <View style={s.detectedMacro}>
              <Text style={[s.detectedMacroValue, { color: Theme.colors.protein }]}>28g</Text>
              <Text style={s.detectedMacroLabel}>protein</Text>
            </View>
            <View style={s.detectedMacro}>
              <Text style={[s.detectedMacroValue, { color: Theme.colors.carbs }]}>62g</Text>
              <Text style={s.detectedMacroLabel}>carbs</Text>
            </View>
            <View style={s.detectedMacro}>
              <Text style={[s.detectedMacroValue, { color: Theme.colors.fat }]}>18g</Text>
              <Text style={s.detectedMacroLabel}>fat</Text>
            </View>
          </View>
        </View>
      </View>

      <Text style={s.demoCaption}>Point. Snap. Track. That simple.</Text>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 10: Feature Showcase ===
  const renderFeatureShowcase = () => (
    <View style={s.screenContainer}>
      <Text style={s.screenTitle}>Everything you need</Text>
      <Text style={s.screenSubtitle}>Powerful tools to reach your goals</Text>
      <View style={s.featureList}>
        {SHOWCASE_FEATURES.map((feat, i) => (
          <View key={i} style={s.featureItem}>
            <LinearGradient
              colors={['rgba(46, 213, 115, 0.15)', 'rgba(46, 213, 115, 0.05)']}
              style={s.featureIconBg}
            >
              <Ionicons name={feat.icon} size={26} color={Theme.colors.primary} />
            </LinearGradient>
            <View style={s.featureText}>
              <Text style={s.featureTitle}>{feat.title}</Text>
              <Text style={s.featureDesc}>{feat.desc}</Text>
            </View>
          </View>
        ))}
      </View>
      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 11: Notification Permission ===
  const renderNotification = () => (
    <View style={s.screenContainer}>
      <View style={s.notifIllustration}>
        <LinearGradient
          colors={['rgba(46, 213, 115, 0.15)', 'rgba(46, 213, 115, 0.03)']}
          style={s.notifCircle}
        >
          <Ionicons name="notifications" size={64} color={Theme.colors.primary} />
        </LinearGradient>
      </View>
      <Text style={s.screenTitle}>Stay on track</Text>
      <Text style={s.screenSubtitle}>
        Get gentle reminders to log your meals.{'\n'}
        Most users who enable reminders stick to their goals 3x better.
      </Text>

      <View style={s.notifPreview}>
        <View style={s.notifPreviewCard}>
          <Ionicons name="restaurant" size={20} color={Theme.colors.primary} />
          <View style={s.notifPreviewText}>
            <Text style={s.notifPreviewTitle}>Time to log lunch!</Text>
            <Text style={s.notifPreviewBody}>You've had 820 cal so far. 1,180 remaining.</Text>
          </View>
        </View>
      </View>

      <TouchableOpacity
        style={s.primaryButton}
        onPress={() => {
          haptics.medium();
          setNotifRequested(true);
          // In a real app, call Notifications.requestPermissionsAsync() here
          goNext();
        }}
        activeOpacity={0.85}
      >
        <Text style={s.primaryButtonText}>Enable Reminders</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={s.secondaryButton}
        onPress={() => {
          haptics.light();
          goNext();
        }}
      >
        <Text style={s.secondaryButtonText}>Maybe later</Text>
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 12: Plan Ready ===
  const renderPlanReady = () => (
    <View style={s.screenContainer}>
      <View style={s.planReadyBadge}>
        <LinearGradient
          colors={[Theme.colors.primary, '#1DB954']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={s.planReadyBadgeInner}
        >
          <Ionicons name="checkmark" size={40} color="#000" />
        </LinearGradient>
      </View>
      <Text style={s.screenTitle}>Your personalized{'\n'}nutrition plan is ready!</Text>

      <View style={s.planSummaryCard}>
        <View style={s.planSummaryRow}>
          <Text style={s.planSummaryLabel}>Daily Calories</Text>
          <Text style={s.planSummaryValue}>{plan.dailyCalories} cal</Text>
        </View>
        <View style={s.planSummaryDivider} />
        <View style={s.planSummaryRow}>
          <Text style={s.planSummaryLabel}>Protein</Text>
          <Text style={[s.planSummaryValue, { color: Theme.colors.protein }]}>{plan.protein}g</Text>
        </View>
        <View style={s.planSummaryDivider} />
        <View style={s.planSummaryRow}>
          <Text style={s.planSummaryLabel}>Carbs</Text>
          <Text style={[s.planSummaryValue, { color: Theme.colors.carbs }]}>{plan.carbs}g</Text>
        </View>
        <View style={s.planSummaryDivider} />
        <View style={s.planSummaryRow}>
          <Text style={s.planSummaryLabel}>Fat</Text>
          <Text style={[s.planSummaryValue, { color: Theme.colors.fat }]}>{plan.fat}g</Text>
        </View>
        <View style={s.planSummaryDivider} />
        <View style={s.planSummaryRow}>
          <Text style={s.planSummaryLabel}>Goal</Text>
          <Text style={s.planSummaryValue}>
            {effectiveGoal === 'lose' ? `Lose ${Math.abs(weightLbs - targetWeightLbs)} lbs` :
             effectiveGoal === 'gain' ? `Gain ${Math.abs(weightLbs - targetWeightLbs)} lbs` :
             'Maintain weight'}
          </Text>
        </View>
        {effectiveGoal !== 'maintain' && (
          <>
            <View style={s.planSummaryDivider} />
            <View style={s.planSummaryRow}>
              <Text style={s.planSummaryLabel}>Timeline</Text>
              <Text style={s.planSummaryValue}>
                {TIMELINE_OPTIONS.find(t => t.key === selectedTimeline)?.label ?? '3 months'}
              </Text>
            </View>
          </>
        )}
      </View>

      <TouchableOpacity style={s.primaryButton} onPress={goNext} activeOpacity={0.85}>
        <Text style={s.primaryButtonText}>Unlock My Plan</Text>
        <Ionicons name="lock-open" size={18} color="#000" />
      </TouchableOpacity>
    </View>
  );

  // === SCREEN 13: PAYWALL ===
  const renderPaywall = () => {
    if (showRescue) {
      return renderRescueOffer();
    }

    return (
      <ScrollView style={s.paywallScroll} contentContainerStyle={s.paywallContent} bounces={false}>
        {/* Trial Timeline */}
        <View style={s.trialTimeline}>
          <View style={s.timelineDotContainer}>
            <View style={[s.timelineDot, s.timelineDotActive]}>
              <Ionicons name="lock-open" size={16} color="#000" />
            </View>
            <Text style={s.timelineDotLabel}>Today{'\n'}FREE</Text>
          </View>
          <View style={s.timelineConnector} />
          <View style={s.timelineDotContainer}>
            <View style={s.timelineDot}>
              <Ionicons name="notifications-outline" size={16} color={Theme.colors.textSecondary} />
            </View>
            <Text style={s.timelineDotLabel}>Day 2{'\n'}Reminder</Text>
          </View>
          <View style={s.timelineConnector} />
          <View style={s.timelineDotContainer}>
            <View style={s.timelineDot}>
              <Ionicons name="card-outline" size={16} color={Theme.colors.textSecondary} />
            </View>
            <Text style={s.timelineDotLabel}>Day 3{'\n'}Billing</Text>
          </View>
        </View>

        <Text style={s.paywallNoPayment}>No payment due now</Text>

        {/* Plan cards */}
        <View style={s.planCards}>
          {/* Monthly (anchor) */}
          <TouchableOpacity
            style={[s.planCard, selectedPlan === 'monthly' && s.planCardSelected]}
            onPress={() => { haptics.selection(); setSelectedPlan('monthly'); }}
            activeOpacity={0.85}
          >
            <View style={s.planCardHeader}>
              <View style={[s.planRadio, selectedPlan === 'monthly' && s.planRadioSelected]} />
              <Text style={s.planCardTitle}>Monthly</Text>
            </View>
            <Text style={s.planCardPrice}>$9.99<Text style={s.planCardPeriod}>/month</Text></Text>
          </TouchableOpacity>

          {/* Yearly (highlighted) */}
          <TouchableOpacity
            style={[s.planCard, s.planCardYearly, selectedPlan === 'yearly' && s.planCardSelected]}
            onPress={() => { haptics.selection(); setSelectedPlan('yearly'); }}
            activeOpacity={0.85}
          >
            <View style={s.bestValueBadge}>
              <Text style={s.bestValueText}>BEST VALUE</Text>
            </View>
            <View style={s.planCardHeader}>
              <View style={[s.planRadio, selectedPlan === 'yearly' && s.planRadioSelected]} />
              <Text style={s.planCardTitle}>Annual</Text>
            </View>
            <Text style={s.planCardPrice}>$29.99<Text style={s.planCardPeriod}>/year</Text></Text>
            <Text style={s.planCardSavings}>$2.50/mo - Save 79%</Text>
          </TouchableOpacity>
        </View>

        {/* Benefits */}
        <View style={s.paywallBenefits}>
          {PAYWALL_FEATURES.map((feat, i) => (
            <View key={i} style={s.paywallBenefit}>
              <Ionicons name={feat.icon} size={20} color={Theme.colors.primary} />
              <Text style={s.paywallBenefitText}>{feat.label}</Text>
            </View>
          ))}
        </View>

        {/* CTA */}
        <TouchableOpacity
          style={[s.paywallCTA, purchasing && s.paywallCTADisabled]}
          onPress={handlePurchase}
          disabled={purchasing}
          activeOpacity={0.85}
        >
          <LinearGradient
            colors={[Theme.colors.primary, '#1DB954']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={s.paywallCTAGradient}
          >
            <Text style={s.paywallCTAText}>{purchasing ? 'Processing...' : 'Start My Free Trial'}</Text>
          </LinearGradient>
        </TouchableOpacity>

        <Text style={s.paywallCancel}>Cancel anytime. No commitment.</Text>

        {/* Social proof footer */}
        <View style={s.paywallSocialProof}>
          <Text style={s.paywallSocialText}>4.9 ★ | 50,000+ users</Text>
        </View>

        {/* Restore purchases */}
        <TouchableOpacity style={s.restoreBtn} onPress={async () => {
          const restored = await restorePurchases();
          if (restored) {
            dispatch(setPremiumStatus(true));
            await saveOnboardingData();
            onComplete();
          } else {
            Alert.alert('No purchases found', 'No active subscription was found for your account.');
          }
        }}>
          <Text style={s.restoreText}>Restore purchases</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  };

  // === RESCUE OFFER (shown after first decline) ===
  const renderRescueOffer = () => (
    <ScrollView style={s.paywallScroll} contentContainerStyle={s.paywallContent} bounces={false}>
      <View style={s.rescueHeader}>
        <Text style={s.rescueEmoji}>🎁</Text>
        <Text style={s.rescueTitle}>Wait! Special offer just for you</Text>
        <Text style={s.rescueSubtitle}>Get your personalized nutrition plan at a discount</Text>
      </View>

      <View style={s.rescueCard}>
        <Text style={s.rescueOriginalPrice}>$29.99/year</Text>
        <View style={s.rescuePriceRow}>
          <Text style={s.rescueNewPrice}>$19.99</Text>
          <Text style={s.rescuePeriod}>/year</Text>
        </View>
        <Text style={s.rescueSavings}>That's just $1.67/month</Text>
        <View style={s.rescueDivider} />
        <Text style={s.rescueTrialText}>Still includes 3-day free trial</Text>
      </View>

      <TouchableOpacity
        style={[s.paywallCTA, purchasing && s.paywallCTADisabled]}
        onPress={handleRescuePurchase}
        disabled={purchasing}
        activeOpacity={0.85}
      >
        <LinearGradient
          colors={['#FFD700', '#FFA500']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={s.paywallCTAGradient}
        >
          <Text style={[s.paywallCTAText, { color: '#000' }]}>
            {purchasing ? 'Processing...' : 'Claim This Offer'}
          </Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity
        style={s.secondaryButton}
        onPress={async () => {
          await saveOnboardingData();
          onComplete();
        }}
      >
        <Text style={s.secondaryButtonText}>No thanks, continue with free</Text>
      </TouchableOpacity>
    </ScrollView>
  );

  // ─── Screen Router ──────────────────────────────────────────────────────────

  const renderCurrentStep = () => {
    switch (step) {
      case 0: return renderWelcome();
      case 1: return renderGoal();
      case 2: return renderStats();
      case 3: return renderTarget();
      case 4: return renderActivity();
      case 5: return renderDiet();
      case 6: return renderValidation();
      case 7: return renderCalorieBreakdown();
      case 8: return renderSocialProof();
      case 9: return renderMagicMoment();
      case 10: return renderFeatureShowcase();
      case 11: return renderNotification();
      case 12: return renderPlanReady();
      case 13: return renderPaywall();
      default: return renderWelcome();
    }
  };

  // ─── Main Render ────────────────────────────────────────────────────────────

  return (
    <SafeAreaView style={s.container}>
      {/* Progress bar */}
      <View style={s.header}>
        {step > 0 && step < 13 ? (
          <TouchableOpacity style={s.backBtn} onPress={goBack} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
            <Ionicons name="chevron-back" size={24} color={Theme.colors.text} />
          </TouchableOpacity>
        ) : step === 13 ? (
          <TouchableOpacity style={s.backBtn} onPress={handleDeclinePaywall} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
            <Ionicons name="close" size={24} color={Theme.colors.textSecondary} />
          </TouchableOpacity>
        ) : (
          <View style={s.backBtnPlaceholder} />
        )}
        <View style={s.progressBarContainer}>
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
        <Text style={s.stepCounter}>{step + 1}/{TOTAL_STEPS}</Text>
      </View>

      {/* Animated content */}
      <Animated.View
        style={[
          s.content,
          {
            opacity: fadeAnim,
            transform: [{ translateX: slideAnim }],
          },
        ]}
      >
        {renderCurrentStep()}
      </Animated.View>
    </SafeAreaView>
  );
};

// ─── Styles ───────────────────────────────────────────────────────────────────

const s = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
  },
  backBtn: {
    width: 36,
    height: 36,
    justifyContent: 'center',
    alignItems: 'center',
  },
  backBtnPlaceholder: {
    width: 36,
  },
  progressBarContainer: {
    flex: 1,
    height: 4,
    backgroundColor: Theme.colors.surface,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: Theme.colors.primary,
    borderRadius: 2,
  },
  stepCounter: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    fontWeight: '500',
    minWidth: 36,
    textAlign: 'right',
  },
  content: {
    flex: 1,
  },
  screenContainer: {
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: 'center',
  },

  // ── Welcome ──
  welcomeIllustration: {
    alignItems: 'center',
    marginBottom: 32,
  },
  illustrationCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    justifyContent: 'center',
    alignItems: 'center',
  },
  foodIcons: {
    position: 'absolute',
    flexDirection: 'row',
    bottom: -10,
    gap: 8,
  },
  foodEmoji: {
    fontSize: 28,
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: Theme.colors.text,
    textAlign: 'center',
    lineHeight: 40,
    marginBottom: 12,
  },
  heroSubtitle: {
    fontSize: 16,
    color: Theme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 28,
  },
  welcomeBadges: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 12,
    marginBottom: 32,
    flexWrap: 'wrap',
  },
  welcomeBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(46, 213, 115, 0.1)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 6,
  },
  badgeText: {
    color: Theme.colors.text,
    fontSize: 13,
    fontWeight: '500',
  },

  // ── Primary button ──
  primaryButton: {
    backgroundColor: Theme.colors.primary,
    paddingVertical: 16,
    borderRadius: 14,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    marginTop: 'auto' as any,
    marginBottom: Platform.OS === 'ios' ? 16 : 24,
    minHeight: 54,
  },
  primaryButtonText: {
    color: '#000',
    fontSize: 17,
    fontWeight: '700',
  },
  primaryButtonDisabled: {
    opacity: 0.4,
  },
  secondaryButton: {
    paddingVertical: 14,
    alignItems: 'center',
    marginBottom: Platform.OS === 'ios' ? 8 : 16,
  },
  secondaryButtonText: {
    color: Theme.colors.textSecondary,
    fontSize: 15,
    fontWeight: '500',
  },

  // ── Screen titles ──
  screenTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: Theme.colors.text,
    textAlign: 'center',
    marginBottom: 8,
    lineHeight: 36,
  },
  screenSubtitle: {
    fontSize: 15,
    color: Theme.colors.textSecondary,
    textAlign: 'center',
    marginBottom: 28,
    lineHeight: 22,
  },

  // ── Goal options (2x2 grid) ──
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    justifyContent: 'center',
    marginBottom: 20,
  },
  optionCard: {
    width: (SCREEN_WIDTH - 60) / 2,
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 18,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionCardSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: 'rgba(46, 213, 115, 0.08)',
  },
  optionIconWrap: {
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: 'rgba(46, 213, 115, 0.12)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  optionIconWrapSelected: {
    backgroundColor: Theme.colors.primary,
  },
  optionLabel: {
    color: Theme.colors.text,
    fontSize: 15,
    fontWeight: '600',
    marginBottom: 4,
  },
  optionLabelSelected: {
    color: Theme.colors.primary,
  },
  optionDesc: {
    color: Theme.colors.textSecondary,
    fontSize: 12,
    textAlign: 'center',
  },

  // ── Input sections ──
  inputSection: {
    marginBottom: 24,
  },
  inputLabel: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 14,
    textAlign: 'center',
  },
  pickerRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 24,
  },
  pickerUnit: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    paddingHorizontal: 8,
    paddingVertical: 8,
    gap: 8,
  },
  pickerBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(46, 213, 115, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  pickerValue: {
    color: Theme.colors.text,
    fontSize: 24,
    fontWeight: '700',
    minWidth: 40,
    textAlign: 'center',
  },

  // ── Weight picker ──
  weightPicker: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 20,
  },
  weightBtn: {
    padding: 4,
  },
  weightDisplay: {
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    paddingHorizontal: 32,
    paddingVertical: 16,
    minWidth: 140,
  },
  weightValue: {
    color: Theme.colors.text,
    fontSize: 42,
    fontWeight: '300',
    letterSpacing: -1,
  },
  weightUnit: {
    color: Theme.colors.textSecondary,
    fontSize: 14,
    fontWeight: '500',
    marginTop: 2,
  },

  // ── Timeline chips ──
  timelineRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 10,
    flexWrap: 'wrap',
  },
  timelineChip: {
    paddingHorizontal: 18,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: Theme.colors.surface,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  timelineChipSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: 'rgba(46, 213, 115, 0.08)',
  },
  timelineChipText: {
    color: Theme.colors.textSecondary,
    fontSize: 14,
    fontWeight: '600',
  },
  timelineChipTextSelected: {
    color: Theme.colors.primary,
  },

  // ── Activity list ──
  listOptions: {
    gap: 10,
    marginBottom: 16,
  },
  listOption: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    padding: 16,
    borderWidth: 2,
    borderColor: 'transparent',
    gap: 14,
  },
  listOptionSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: 'rgba(46, 213, 115, 0.06)',
  },
  listOptionIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(46, 213, 115, 0.12)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  listOptionIconSelected: {
    backgroundColor: Theme.colors.primary,
  },
  listOptionText: {
    flex: 1,
  },
  listOptionTitle: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
  },
  listOptionTitleSelected: {
    color: Theme.colors.primary,
  },
  listOptionDesc: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    marginTop: 2,
  },

  // ── Diet grid ──
  dietGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    justifyContent: 'center',
    marginBottom: 20,
  },
  dietChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderRadius: 12,
    gap: 8,
    borderWidth: 2,
    borderColor: 'transparent',
    minWidth: (SCREEN_WIDTH - 68) / 2,
  },
  dietChipSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: 'rgba(46, 213, 115, 0.08)',
  },
  dietChipText: {
    color: Theme.colors.textSecondary,
    fontSize: 14,
    fontWeight: '600',
  },
  dietChipTextSelected: {
    color: Theme.colors.primary,
  },

  // ── Validation screen ──
  validationBadge: {
    alignItems: 'center',
    marginBottom: 24,
  },
  validationBadgeInner: {
    width: 88,
    height: 88,
    borderRadius: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  graphContainer: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  graphInner: {
    flexDirection: 'row',
    height: 120,
  },
  graphYAxis: {
    justifyContent: 'space-between',
    paddingRight: 10,
    width: 50,
  },
  graphLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 11,
    fontWeight: '500',
  },
  graphArea: {
    flex: 1,
  },
  graphLine: {
    flex: 1,
    position: 'relative',
  },
  graphDot: {
    position: 'absolute',
    borderRadius: 5,
  },
  graphXAxis: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  validationStats: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 18,
    marginBottom: 16,
  },
  validationStat: {
    flex: 1,
    alignItems: 'center',
  },
  validationStatValue: {
    color: Theme.colors.primary,
    fontSize: 22,
    fontWeight: '700',
  },
  validationStatLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 12,
    marginTop: 4,
  },
  validationStatDivider: {
    width: 1,
    height: 36,
    backgroundColor: Theme.colors.border,
  },

  // ── Calorie breakdown / pie ──
  pieContainer: {
    alignItems: 'center',
    marginBottom: 28,
  },
  pieCenter: {
    position: 'absolute',
    top: '50%',
    alignSelf: 'center',
    alignItems: 'center',
    zIndex: 2,
    marginTop: -24,
  },
  pieCenterValue: {
    color: Theme.colors.text,
    fontSize: 28,
    fontWeight: '700',
  },
  pieCenterLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
  },
  pieRing: {
    width: 200,
    height: 16,
    borderRadius: 8,
    overflow: 'hidden',
    flexDirection: 'row',
    marginTop: 56,
    marginBottom: 8,
  },
  pieSegment: {
    height: '100%',
  },
  macroCards: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 20,
  },
  macroCard: {
    flex: 1,
    backgroundColor: Theme.colors.surface,
    borderRadius: 12,
    padding: 14,
    alignItems: 'center',
    borderLeftWidth: 3,
  },
  macroCardValue: {
    color: Theme.colors.text,
    fontSize: 22,
    fontWeight: '700',
  },
  macroCardLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 12,
    marginTop: 2,
  },
  macroCardPct: {
    color: Theme.colors.textSecondary,
    fontSize: 11,
    marginTop: 4,
    fontWeight: '500',
  },

  // ── Social proof ──
  testimonials: {
    gap: 12,
    marginBottom: 20,
  },
  testimonialCard: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    padding: 16,
  },
  testimonialHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 10,
  },
  testimonialAvatar: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: 'rgba(46, 213, 115, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  testimonialAvatarText: {
    color: Theme.colors.primary,
    fontSize: 16,
    fontWeight: '700',
  },
  testimonialName: {
    color: Theme.colors.text,
    fontSize: 14,
    fontWeight: '600',
  },
  starsRow: {
    flexDirection: 'row',
    gap: 2,
    marginTop: 2,
  },
  testimonialText: {
    color: Theme.colors.textSecondary,
    fontSize: 14,
    fontStyle: 'italic',
    lineHeight: 20,
  },
  socialProofBanner: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
    backgroundColor: Theme.colors.surface,
    borderRadius: 12,
    paddingVertical: 14,
    marginBottom: 16,
  },
  socialProofStat: {
    color: Theme.colors.primary,
    fontSize: 14,
    fontWeight: '700',
  },
  socialProofDivider: {
    width: 1,
    height: 18,
    backgroundColor: Theme.colors.border,
  },

  // ── Magic moment / demo ──
  demoContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  cameraFrame: {
    width: SCREEN_WIDTH - 80,
    height: (SCREEN_WIDTH - 80) * 0.75,
    borderRadius: 20,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: Theme.colors.border,
    marginBottom: 16,
  },
  cameraInner: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  demoFoodEmoji: {
    fontSize: 72,
  },
  scanCorner: {
    position: 'absolute',
    width: 24,
    height: 24,
    borderColor: Theme.colors.primary,
  },
  scanCornerTL: {
    top: 16,
    left: 16,
    borderTopWidth: 3,
    borderLeftWidth: 3,
    borderTopLeftRadius: 4,
  },
  scanCornerTR: {
    top: 16,
    right: 16,
    borderTopWidth: 3,
    borderRightWidth: 3,
    borderTopRightRadius: 4,
  },
  scanCornerBL: {
    bottom: 16,
    left: 16,
    borderBottomWidth: 3,
    borderLeftWidth: 3,
    borderBottomLeftRadius: 4,
  },
  scanCornerBR: {
    bottom: 16,
    right: 16,
    borderBottomWidth: 3,
    borderRightWidth: 3,
    borderBottomRightRadius: 4,
  },
  scanLine: {
    position: 'absolute',
    left: 20,
    right: 20,
    height: 2,
    backgroundColor: Theme.colors.primary,
    opacity: 0.5,
    top: '45%',
  },
  detectedOverlay: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 16,
    width: SCREEN_WIDTH - 80,
  },
  detectedHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  detectedTitle: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
  },
  detectedMacros: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  detectedMacro: {
    alignItems: 'center',
  },
  detectedMacroValue: {
    color: Theme.colors.text,
    fontSize: 20,
    fontWeight: '700',
  },
  detectedMacroLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 11,
    marginTop: 2,
  },
  demoCaption: {
    color: Theme.colors.textSecondary,
    fontSize: 15,
    textAlign: 'center',
    marginBottom: 16,
    fontWeight: '500',
  },

  // ── Feature showcase ──
  featureList: {
    gap: 14,
    marginBottom: 20,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    padding: 16,
  },
  featureIconBg: {
    width: 48,
    height: 48,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureText: {
    flex: 1,
  },
  featureTitle: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
  },
  featureDesc: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    marginTop: 2,
  },

  // ── Notification ──
  notifIllustration: {
    alignItems: 'center',
    marginBottom: 28,
  },
  notifCircle: {
    width: 130,
    height: 130,
    borderRadius: 65,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notifPreview: {
    marginBottom: 28,
  },
  notifPreviewCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    padding: 16,
    gap: 14,
    borderLeftWidth: 3,
    borderLeftColor: Theme.colors.primary,
  },
  notifPreviewText: {
    flex: 1,
  },
  notifPreviewTitle: {
    color: Theme.colors.text,
    fontSize: 15,
    fontWeight: '600',
  },
  notifPreviewBody: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    marginTop: 2,
  },

  // ── Plan ready ──
  planReadyBadge: {
    alignItems: 'center',
    marginBottom: 24,
  },
  planReadyBadgeInner: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  planSummaryCard: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  planSummaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  planSummaryLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 15,
  },
  planSummaryValue: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
  },
  planSummaryDivider: {
    height: 1,
    backgroundColor: Theme.colors.border,
  },

  // ── Paywall ──
  paywallScroll: {
    flex: 1,
  },
  paywallContent: {
    paddingHorizontal: 24,
    paddingBottom: 40,
    paddingTop: 8,
  },
  trialTimeline: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'center',
    marginBottom: 20,
    paddingHorizontal: 10,
  },
  timelineDotContainer: {
    alignItems: 'center',
    width: 70,
  },
  timelineDot: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Theme.colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Theme.colors.border,
    marginBottom: 8,
  },
  timelineDotActive: {
    backgroundColor: Theme.colors.primary,
    borderColor: Theme.colors.primary,
  },
  timelineDotLabel: {
    color: Theme.colors.textSecondary,
    fontSize: 11,
    textAlign: 'center',
    fontWeight: '500',
    lineHeight: 15,
  },
  timelineConnector: {
    flex: 1,
    height: 2,
    backgroundColor: Theme.colors.border,
    marginTop: 19,
  },
  paywallNoPayment: {
    color: Theme.colors.primary,
    fontSize: 16,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 24,
  },
  planCards: {
    gap: 12,
    marginBottom: 24,
  },
  planCard: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 14,
    padding: 18,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  planCardYearly: {
    borderColor: Theme.colors.border,
  },
  planCardSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: 'rgba(46, 213, 115, 0.06)',
  },
  planCardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 4,
  },
  planRadio: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: Theme.colors.border,
  },
  planRadioSelected: {
    borderColor: Theme.colors.primary,
    backgroundColor: Theme.colors.primary,
  },
  planCardTitle: {
    color: Theme.colors.text,
    fontSize: 16,
    fontWeight: '600',
  },
  planCardPrice: {
    color: Theme.colors.text,
    fontSize: 24,
    fontWeight: '700',
    marginLeft: 34,
  },
  planCardPeriod: {
    fontSize: 14,
    fontWeight: '400',
    color: Theme.colors.textSecondary,
  },
  planCardSavings: {
    color: Theme.colors.primary,
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 34,
    marginTop: 4,
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    right: 16,
    backgroundColor: Theme.colors.primary,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    zIndex: 1,
  },
  bestValueText: {
    color: '#000',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  paywallBenefits: {
    gap: 12,
    marginBottom: 24,
  },
  paywallBenefit: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  paywallBenefitText: {
    color: Theme.colors.text,
    fontSize: 15,
    fontWeight: '500',
  },
  paywallCTA: {
    borderRadius: 14,
    overflow: 'hidden',
    marginBottom: 12,
  },
  paywallCTADisabled: {
    opacity: 0.6,
  },
  paywallCTAGradient: {
    paddingVertical: 18,
    alignItems: 'center',
    borderRadius: 14,
  },
  paywallCTAText: {
    color: '#000',
    fontSize: 18,
    fontWeight: '700',
  },
  paywallCancel: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    textAlign: 'center',
    marginBottom: 16,
  },
  paywallSocialProof: {
    alignItems: 'center',
    marginBottom: 12,
  },
  paywallSocialText: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    fontWeight: '500',
  },
  restoreBtn: {
    paddingVertical: 12,
    alignItems: 'center',
  },
  restoreText: {
    color: Theme.colors.textSecondary,
    fontSize: 13,
    textDecorationLine: 'underline',
  },

  // ── Rescue offer ──
  rescueHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  rescueEmoji: {
    fontSize: 48,
    marginBottom: 12,
  },
  rescueTitle: {
    color: Theme.colors.text,
    fontSize: 24,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 8,
  },
  rescueSubtitle: {
    color: Theme.colors.textSecondary,
    fontSize: 15,
    textAlign: 'center',
  },
  rescueCard: {
    backgroundColor: Theme.colors.surface,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 28,
    borderWidth: 2,
    borderColor: '#FFD700',
  },
  rescueOriginalPrice: {
    color: Theme.colors.textSecondary,
    fontSize: 16,
    textDecorationLine: 'line-through',
    marginBottom: 8,
  },
  rescuePriceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  rescueNewPrice: {
    color: '#FFD700',
    fontSize: 40,
    fontWeight: '700',
  },
  rescuePeriod: {
    color: Theme.colors.textSecondary,
    fontSize: 16,
    marginLeft: 4,
  },
  rescueSavings: {
    color: Theme.colors.primary,
    fontSize: 15,
    fontWeight: '600',
    marginTop: 8,
  },
  rescueDivider: {
    width: '80%',
    height: 1,
    backgroundColor: Theme.colors.border,
    marginVertical: 16,
  },
  rescueTrialText: {
    color: Theme.colors.textSecondary,
    fontSize: 14,
  },
});

export default OnboardingFlow;
