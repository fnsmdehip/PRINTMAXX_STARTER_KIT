import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  Dimensions,
  Keyboard,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  withSpring,
  withDelay,
  Easing,
  FadeIn,
  FadeInDown,
  FadeInUp,
  ZoomIn,
  runOnJS,
  cancelAnimation,
} from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Haptics from 'expo-haptics';
import { colors, spacing, radii, typography } from '../theme';
import { getRandomQuestion } from '../utils/partyQuestions';
import { PartyQuestion, Verdict, DetectionResult } from '../utils/types';
import { saveSession, generateId } from '../store';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

// --- Types ---

type GamePhase = 'setup' | 'round' | 'analyzing' | 'result' | 'scoreboard' | 'passPhone';

type QuestionCategory = 'mild' | 'spicy' | 'random';

interface PlayerData {
  name: string;
  results: PlayerResult[];
}

interface PlayerResult {
  question: string;
  score: number;
  verdict: Verdict;
  round: number;
}

// --- Constants ---

const MIN_PLAYERS = 2;
const MAX_PLAYERS = 8;
const ANALYSIS_DURATION_MS = 10000;
const PASS_PHONE_COUNTDOWN = 5;

const CATEGORY_CONFIG: Record<QuestionCategory, { label: string; color: string; icon: keyof typeof Ionicons.glyphMap }> = {
  mild: { label: 'Mild', color: colors.accent.success, icon: 'happy-outline' },
  spicy: { label: 'Spicy', color: colors.accent.tertiary, icon: 'flame-outline' },
  random: { label: 'Random', color: colors.accent.warning, icon: 'shuffle-outline' },
};

// --- Helpers ---

function generateScore(audioLevel: number): { score: number; verdict: Verdict; confidence: number } {
  // Weighted randomization: audio level influences the result but doesn't determine it.
  // Higher audio "stress" tilts toward deceptive, lower toward truthful.
  // This makes the game fun while feeling responsive to the player's behavior.
  const baseRandom = Math.random();
  const stressWeight = audioLevel * 0.3; // 0-0.3 influence from "audio"
  const combined = baseRandom * 0.7 + stressWeight;

  const score = Math.round(Math.max(5, Math.min(98, combined * 100)));

  let verdict: Verdict;
  if (score >= 65) {
    verdict = 'deceptive';
  } else if (score >= 40) {
    verdict = 'uncertain';
  } else {
    verdict = 'truthful';
  }

  const confidence = Math.round(55 + Math.random() * 35);

  return { score, verdict, confidence };
}

function getVerdictDisplay(verdict: Verdict): { text: string; color: string; subtext: string } {
  switch (verdict) {
    case 'truthful':
      return {
        text: 'TRUTH!',
        color: colors.accent.success,
        subtext: 'Sensors show low stress indicators',
      };
    case 'deceptive':
      return {
        text: 'LIES!',
        color: colors.accent.tertiary,
        subtext: 'Elevated stress patterns detected',
      };
    case 'uncertain':
      return {
        text: 'HMMMM...',
        color: colors.accent.warning,
        subtext: 'Inconclusive. The truth is murky.',
      };
    default:
      return { text: '', color: colors.text.primary, subtext: '' };
  }
}

// --- Sub-Components ---

function SetupPhase({
  onStart,
  onBack,
}: {
  onStart: (names: string[]) => void;
  onBack: () => void;
}) {
  const insets = useSafeAreaInsets();
  const [playerCount, setPlayerCount] = useState(3);
  const [names, setNames] = useState<string[]>(Array(MAX_PLAYERS).fill(''));

  const handleCountChange = (delta: number) => {
    const next = Math.max(MIN_PLAYERS, Math.min(MAX_PLAYERS, playerCount + delta));
    setPlayerCount(next);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const handleNameChange = (index: number, value: string) => {
    const updated = [...names];
    updated[index] = value;
    setNames(updated);
  };

  const handleStart = () => {
    const finalNames = names.slice(0, playerCount).map((n, i) => n.trim() || `Player ${i + 1}`);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    onStart(finalNames);
  };

  const filledNames = names.slice(0, playerCount).filter(n => n.trim().length > 0).length;
  const allFilled = filledNames === playerCount;

  return (
    <ScrollView
      style={styles.phaseContainer}
      contentContainerStyle={[styles.setupContent, { paddingTop: insets.top + spacing.md }]}
      keyboardShouldPersistTaps="handled"
    >
      {/* Back button */}
      <TouchableOpacity onPress={onBack} style={styles.backButton}>
        <Ionicons name="arrow-back" size={24} color={colors.text.secondary} />
      </TouchableOpacity>

      <Animated.View entering={FadeInDown.delay(100).duration(400)}>
        <Text style={styles.setupTitle}>Party Setup</Text>
        <Text style={styles.setupSubtitle}>
          Who's brave enough to face the truth?
        </Text>
      </Animated.View>

      {/* Player Count Selector */}
      <Animated.View entering={FadeInDown.delay(200).duration(400)} style={styles.countSelector}>
        <Text style={styles.countLabel}>Players</Text>
        <View style={styles.countControls}>
          <TouchableOpacity
            onPress={() => handleCountChange(-1)}
            disabled={playerCount <= MIN_PLAYERS}
            style={[
              styles.countButton,
              playerCount <= MIN_PLAYERS && styles.countButtonDisabled,
            ]}
          >
            <Ionicons
              name="remove"
              size={24}
              color={playerCount <= MIN_PLAYERS ? colors.text.tertiary : colors.text.primary}
            />
          </TouchableOpacity>
          <Text style={styles.countValue}>{playerCount}</Text>
          <TouchableOpacity
            onPress={() => handleCountChange(1)}
            disabled={playerCount >= MAX_PLAYERS}
            style={[
              styles.countButton,
              playerCount >= MAX_PLAYERS && styles.countButtonDisabled,
            ]}
          >
            <Ionicons
              name="add"
              size={24}
              color={playerCount >= MAX_PLAYERS ? colors.text.tertiary : colors.text.primary}
            />
          </TouchableOpacity>
        </View>
      </Animated.View>

      {/* Name Inputs */}
      <Animated.View entering={FadeInDown.delay(300).duration(400)} style={styles.nameInputs}>
        {Array.from({ length: playerCount }).map((_, i) => (
          <View key={i} style={styles.nameRow}>
            <View style={[styles.nameIndex, { backgroundColor: colors.accent.primary + '20' }]}>
              <Text style={styles.nameIndexText}>{i + 1}</Text>
            </View>
            <TextInput
              style={styles.nameInput}
              placeholder={`Player ${i + 1}`}
              placeholderTextColor={colors.text.tertiary}
              value={names[i]}
              onChangeText={(v) => handleNameChange(i, v)}
              maxLength={20}
              returnKeyType={i < playerCount - 1 ? 'next' : 'done'}
              onSubmitEditing={() => {
                if (i === playerCount - 1) Keyboard.dismiss();
              }}
            />
          </View>
        ))}
      </Animated.View>

      {/* Start Button */}
      <Animated.View entering={FadeInUp.delay(500).duration(400)}>
        <TouchableOpacity onPress={handleStart} activeOpacity={0.8}>
          <LinearGradient
            colors={['#7B61FF', '#FF3D71']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.startButton}
          >
            <Ionicons name="play" size={22} color="#FFFFFF" />
            <Text style={styles.startButtonText}>
              {allFilled ? 'Start the Game' : 'Start (unnamed = default)'}
            </Text>
          </LinearGradient>
        </TouchableOpacity>
      </Animated.View>
    </ScrollView>
  );
}

function RoundPhase({
  playerName,
  roundNumber,
  totalPlayers,
  question,
  category,
  onCategoryChange,
  onCustomQuestion,
  onStartAnalysis,
}: {
  playerName: string;
  roundNumber: number;
  totalPlayers: number;
  question: PartyQuestion | null;
  category: QuestionCategory;
  onCategoryChange: (cat: QuestionCategory) => void;
  onCustomQuestion: (text: string) => void;
  onStartAnalysis: () => void;
}) {
  const insets = useSafeAreaInsets();
  const [showCustom, setShowCustom] = useState(false);
  const [customText, setCustomText] = useState('');

  const categories: QuestionCategory[] = ['mild', 'spicy', 'random'];

  return (
    <View style={[styles.phaseContainer, { paddingTop: insets.top + spacing.md }]}>
      {/* Round info */}
      <Animated.View entering={FadeIn.duration(300)} style={styles.roundHeader}>
        <Text style={styles.roundBadge}>ROUND {roundNumber}</Text>
      </Animated.View>

      {/* Player spotlight */}
      <Animated.View entering={ZoomIn.delay(100).duration(500)} style={styles.playerSpotlight}>
        <LinearGradient
          colors={[...colors.gradient.scanning]}
          style={styles.playerSpotlightGradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Text style={styles.playerSpotlightName}>{playerName}</Text>
          <Text style={styles.playerSpotlightSub}>It's your turn in the hot seat</Text>
        </LinearGradient>
      </Animated.View>

      {/* Category tabs */}
      <Animated.View entering={FadeInDown.delay(300).duration(400)} style={styles.categoryTabs}>
        {categories.map((cat) => {
          const config = CATEGORY_CONFIG[cat];
          const active = category === cat;
          return (
            <TouchableOpacity
              key={cat}
              onPress={() => {
                onCategoryChange(cat);
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              }}
              style={[
                styles.categoryTab,
                active && { backgroundColor: config.color + '20', borderColor: config.color },
              ]}
            >
              <Ionicons name={config.icon} size={16} color={active ? config.color : colors.text.tertiary} />
              <Text style={[styles.categoryTabText, active && { color: config.color }]}>
                {config.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </Animated.View>

      {/* Question */}
      <Animated.View entering={FadeInDown.delay(400).duration(500)} style={styles.questionCard}>
        <Text style={styles.questionEmoji}>
          {category === 'spicy' ? '🌶' : category === 'random' ? '🎲' : '😇'}
        </Text>
        <Text style={styles.questionText}>
          {question?.text ?? 'No more questions in this category!'}
        </Text>
      </Animated.View>

      {/* Custom question toggle */}
      <Animated.View entering={FadeInDown.delay(500).duration(400)}>
        {!showCustom ? (
          <TouchableOpacity
            onPress={() => setShowCustom(true)}
            style={styles.customToggle}
          >
            <Ionicons name="create-outline" size={16} color={colors.accent.primary} />
            <Text style={styles.customToggleText}>Ask your own question</Text>
          </TouchableOpacity>
        ) : (
          <View style={styles.customInputRow}>
            <TextInput
              style={styles.customInput}
              placeholder="Type your question..."
              placeholderTextColor={colors.text.tertiary}
              value={customText}
              onChangeText={setCustomText}
              multiline
              maxLength={200}
            />
            <TouchableOpacity
              onPress={() => {
                if (customText.trim()) {
                  onCustomQuestion(customText.trim());
                  setShowCustom(false);
                  setCustomText('');
                }
              }}
              disabled={!customText.trim()}
              style={[
                styles.customConfirm,
                !customText.trim() && { opacity: 0.4 },
              ]}
            >
              <Ionicons name="checkmark" size={20} color="#FFFFFF" />
            </TouchableOpacity>
          </View>
        )}
      </Animated.View>

      {/* Start Analysis Button */}
      <View style={styles.bottomAction}>
        <TouchableOpacity onPress={onStartAnalysis} activeOpacity={0.8}>
          <LinearGradient
            colors={[...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.analyzeButton}
          >
            <Ionicons name="pulse" size={22} color="#FFFFFF" />
            <Text style={styles.analyzeButtonText}>Begin Analysis</Text>
          </LinearGradient>
        </TouchableOpacity>
        <Text style={styles.analyzeHint}>
          Hold the phone and answer the question out loud
        </Text>
      </View>
    </View>
  );
}

function AnalyzingPhase({
  playerName,
  question,
  elapsed,
  total,
}: {
  playerName: string;
  question: string;
  elapsed: number;
  total: number;
}) {
  const insets = useSafeAreaInsets();
  const pulseScale = useSharedValue(1);
  const ringRotation = useSharedValue(0);
  const gaugeProgress = useSharedValue(0);

  useEffect(() => {
    // Pulsing center
    pulseScale.value = withRepeat(
      withSequence(
        withTiming(1.15, { duration: 600, easing: Easing.inOut(Easing.sin) }),
        withTiming(1, { duration: 600, easing: Easing.inOut(Easing.sin) }),
      ),
      -1,
      false,
    );

    // Rotating ring
    ringRotation.value = withRepeat(
      withTiming(360, { duration: 3000, easing: Easing.linear }),
      -1,
      false,
    );

    // Progress
    gaugeProgress.value = withTiming(1, {
      duration: total,
      easing: Easing.linear,
    });

    return () => {
      cancelAnimation(pulseScale);
      cancelAnimation(ringRotation);
    };
  }, [total]);

  const pulseStyle = useAnimatedStyle(() => ({
    transform: [{ scale: pulseScale.value }],
  }));

  const ringStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${ringRotation.value}deg` }],
  }));

  const progressPercent = Math.min(100, Math.round((elapsed / total) * 100));
  const secondsLeft = Math.max(0, Math.ceil((total - elapsed) / 1000));

  return (
    <View style={[styles.phaseContainer, styles.analyzingContainer, { paddingTop: insets.top }]}>
      <Text style={styles.analyzingPlayer}>{playerName}</Text>
      <Text style={styles.analyzingQuestion} numberOfLines={3}>
        "{question}"
      </Text>

      {/* Pulsing gauge */}
      <View style={styles.gaugeContainer}>
        {/* Rotating dashed ring */}
        <Animated.View style={[styles.rotatingRing, ringStyle]}>
          <LinearGradient
            colors={[...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.rotatingRingGradient}
          />
        </Animated.View>

        {/* Center pulsing orb */}
        <Animated.View style={[styles.pulseOrb, pulseStyle]}>
          <LinearGradient
            colors={[colors.accent.primary + '40', colors.accent.secondary + '30']}
            style={styles.pulseOrbGradient}
          />
        </Animated.View>

        {/* Score number */}
        <Text style={styles.gaugeScore}>{progressPercent}</Text>
        <Text style={styles.gaugeLabel}>ANALYZING</Text>
      </View>

      {/* Timer */}
      <View style={styles.timerRow}>
        <Ionicons name="time-outline" size={16} color={colors.accent.primary} />
        <Text style={styles.timerText}>{secondsLeft}s remaining</Text>
      </View>

      {/* Progress bar */}
      <View style={styles.progressTrack}>
        <LinearGradient
          colors={[...colors.gradient.scanning]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={[styles.progressFill, { width: `${progressPercent}%` }]}
        />
      </View>

      <Text style={styles.analyzingHint}>Speak clearly while being analyzed...</Text>
    </View>
  );
}

function ResultPhase({
  playerName,
  question,
  score,
  verdict,
  confidence,
  onNext,
  onScoreboard,
}: {
  playerName: string;
  question: string;
  score: number;
  verdict: Verdict;
  confidence: number;
  onNext: () => void;
  onScoreboard: () => void;
}) {
  const insets = useSafeAreaInsets();
  const display = getVerdictDisplay(verdict);
  const revealScale = useSharedValue(0);

  useEffect(() => {
    Haptics.notificationAsync(
      verdict === 'truthful'
        ? Haptics.NotificationFeedbackType.Success
        : verdict === 'deceptive'
        ? Haptics.NotificationFeedbackType.Error
        : Haptics.NotificationFeedbackType.Warning,
    );

    revealScale.value = withSpring(1, { damping: 8, stiffness: 90 });
  }, []);

  const revealStyle = useAnimatedStyle(() => ({
    transform: [{ scale: revealScale.value }],
    opacity: revealScale.value,
  }));

  return (
    <View style={[styles.phaseContainer, styles.resultContainer, { paddingTop: insets.top }]}>
      {/* Verdict reveal */}
      <Animated.View style={[styles.revealCard, revealStyle]}>
        <Text style={styles.resultPlayerName}>{playerName}</Text>

        {/* Big verdict */}
        <Animated.View entering={ZoomIn.delay(300).duration(600)}>
          <Text style={[styles.verdictBig, { color: display.color }]}>
            {display.text}
          </Text>
        </Animated.View>

        {/* Score ring */}
        <Animated.View entering={FadeIn.delay(600).duration(400)} style={styles.resultScoreRing}>
          <View style={[styles.resultScoreCircle, { borderColor: display.color }]}>
            <Text style={[styles.resultScoreNumber, { color: display.color }]}>
              {score}
            </Text>
            <Text style={styles.resultScoreLabel}>SCORE</Text>
          </View>
        </Animated.View>

        {/* Confidence */}
        <Animated.View entering={FadeInDown.delay(800).duration(400)}>
          <Text style={styles.resultConfidence}>{confidence}% confidence</Text>
          <Text style={styles.resultSubtext}>{display.subtext}</Text>
        </Animated.View>

        {/* Question reminder */}
        <Animated.View entering={FadeInDown.delay(1000).duration(400)} style={styles.resultQuestionCard}>
          <Text style={styles.resultQuestionLabel}>Question</Text>
          <Text style={styles.resultQuestionText}>"{question}"</Text>
        </Animated.View>
      </Animated.View>

      {/* Actions */}
      <View style={styles.resultActions}>
        <TouchableOpacity onPress={onScoreboard} style={styles.secondaryButton}>
          <Ionicons name="podium-outline" size={18} color={colors.accent.primary} />
          <Text style={styles.secondaryButtonText}>Scoreboard</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={onNext} activeOpacity={0.8} style={{ flex: 1 }}>
          <LinearGradient
            colors={['#7B61FF', '#FF3D71']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.nextButton}
          >
            <Text style={styles.nextButtonText}>Next Player</Text>
            <Ionicons name="arrow-forward" size={18} color="#FFFFFF" />
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );
}

function ScoreboardPhase({
  players,
  currentRound,
  onContinue,
  onEndGame,
}: {
  players: PlayerData[];
  currentRound: number;
  onContinue: () => void;
  onEndGame: () => void;
}) {
  const insets = useSafeAreaInsets();

  // Sort by truthful count (desc), then by total tests (desc)
  const sorted = useMemo(() => {
    return [...players]
      .map((p) => {
        const truths = p.results.filter(r => r.verdict === 'truthful').length;
        const lies = p.results.filter(r => r.verdict === 'deceptive').length;
        const uncertain = p.results.filter(r => r.verdict === 'uncertain').length;
        return { ...p, truths, lies, uncertain };
      })
      .sort((a, b) => b.truths - a.truths || a.lies - b.lies);
  }, [players]);

  return (
    <View style={[styles.phaseContainer, { paddingTop: insets.top + spacing.md }]}>
      <Animated.View entering={FadeInDown.duration(400)}>
        <Text style={styles.scoreboardTitle}>Scoreboard</Text>
        <Text style={styles.scoreboardRound}>After Round {currentRound}</Text>
      </Animated.View>

      <ScrollView style={styles.scoreboardList} showsVerticalScrollIndicator={false}>
        {sorted.map((player, i) => {
          const isFirst = i === 0 && player.results.length > 0;
          return (
            <Animated.View
              key={player.name + i}
              entering={FadeInDown.delay(i * 80).duration(300)}
              style={[styles.scoreboardRow, isFirst && styles.scoreboardRowFirst]}
            >
              <View style={styles.scoreboardRank}>
                {isFirst ? (
                  <Text style={styles.scoreboardCrown}>👑</Text>
                ) : (
                  <Text style={styles.scoreboardRankNum}>{i + 1}</Text>
                )}
              </View>
              <View style={styles.scoreboardInfo}>
                <Text style={styles.scoreboardName}>{player.name}</Text>
                <View style={styles.scoreboardBadges}>
                  <View style={[styles.scoreBadge, { backgroundColor: colors.accent.success + '20' }]}>
                    <Text style={[styles.scoreBadgeText, { color: colors.accent.success }]}>
                      {player.truths} Truth
                    </Text>
                  </View>
                  <View style={[styles.scoreBadge, { backgroundColor: colors.accent.tertiary + '20' }]}>
                    <Text style={[styles.scoreBadgeText, { color: colors.accent.tertiary }]}>
                      {player.lies} Lies
                    </Text>
                  </View>
                  {player.uncertain > 0 && (
                    <View style={[styles.scoreBadge, { backgroundColor: colors.accent.warning + '20' }]}>
                      <Text style={[styles.scoreBadgeText, { color: colors.accent.warning }]}>
                        {player.uncertain} ?
                      </Text>
                    </View>
                  )}
                </View>
              </View>
              <Text style={styles.scoreboardTotal}>
                {player.results.length} test{player.results.length !== 1 ? 's' : ''}
              </Text>
            </Animated.View>
          );
        })}
      </ScrollView>

      <View style={styles.scoreboardActions}>
        <TouchableOpacity onPress={onEndGame} style={styles.secondaryButton}>
          <Ionicons name="stop-circle-outline" size={18} color={colors.accent.tertiary} />
          <Text style={[styles.secondaryButtonText, { color: colors.accent.tertiary }]}>End Game</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={onContinue} activeOpacity={0.8} style={{ flex: 1 }}>
          <LinearGradient
            colors={[...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.nextButton}
          >
            <Text style={styles.nextButtonText}>Continue</Text>
            <Ionicons name="arrow-forward" size={18} color="#FFFFFF" />
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );
}

function PassPhonePhase({
  nextPlayerName,
  countdown,
}: {
  nextPlayerName: string;
  countdown: number;
}) {
  const insets = useSafeAreaInsets();
  const bounceScale = useSharedValue(0.8);

  useEffect(() => {
    bounceScale.value = withRepeat(
      withSequence(
        withTiming(1.05, { duration: 500, easing: Easing.out(Easing.cubic) }),
        withTiming(0.95, { duration: 500, easing: Easing.in(Easing.cubic) }),
      ),
      -1,
      false,
    );
    return () => cancelAnimation(bounceScale);
  }, []);

  const bounceStyle = useAnimatedStyle(() => ({
    transform: [{ scale: bounceScale.value }],
  }));

  return (
    <View style={[styles.phaseContainer, styles.passContainer, { paddingTop: insets.top }]}>
      <LinearGradient
        colors={[colors.bg.primary, colors.bg.secondary]}
        style={StyleSheet.absoluteFill}
      />
      <Animated.View style={bounceStyle}>
        <Text style={styles.passEmoji}>📱</Text>
      </Animated.View>
      <Text style={styles.passTitle}>Pass the phone to</Text>
      <Text style={styles.passPlayerName}>{nextPlayerName}</Text>
      <View style={styles.passCountdown}>
        <Text style={styles.passCountdownNumber}>{countdown}</Text>
      </View>
      <Text style={styles.passHint}>Don't peek at the question!</Text>
    </View>
  );
}

// --- Main Screen ---

export default function PartyModeScreen({ navigation }: { navigation: any }) {
  const [phase, setPhase] = useState<GamePhase>('setup');
  const [players, setPlayers] = useState<PlayerData[]>([]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [round, setRound] = useState(1);
  const [category, setCategory] = useState<QuestionCategory>('mild');
  const [currentQuestion, setCurrentQuestion] = useState<PartyQuestion | null>(null);
  const [usedQuestionIds, setUsedQuestionIds] = useState<string[]>([]);
  const [analysisElapsed, setAnalysisElapsed] = useState(0);
  const [lastResult, setLastResult] = useState<{ score: number; verdict: Verdict; confidence: number } | null>(null);
  const [passCountdown, setPassCountdown] = useState(PASS_PHONE_COUNTDOWN);

  // Simulated audio level for scoring
  const audioLevelRef = useRef(0.5);
  const analysisTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const countdownTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      if (analysisTimerRef.current) clearInterval(analysisTimerRef.current);
      if (countdownTimerRef.current) clearInterval(countdownTimerRef.current);
    };
  }, []);

  const pickQuestion = useCallback((cat: QuestionCategory) => {
    const q = getRandomQuestion(cat, false, usedQuestionIds);
    setCurrentQuestion(q);
    if (q) {
      setUsedQuestionIds(prev => [...prev, q.id]);
    }
  }, [usedQuestionIds]);

  const handleStart = useCallback((names: string[]) => {
    const playerData: PlayerData[] = names.map(name => ({
      name,
      results: [],
    }));
    setPlayers(playerData);
    setCurrentPlayerIndex(0);
    setRound(1);
    pickQuestion(category);
    setPhase('round');
  }, [category, pickQuestion]);

  const handleCategoryChange = useCallback((cat: QuestionCategory) => {
    setCategory(cat);
    pickQuestion(cat);
  }, [pickQuestion]);

  const handleCustomQuestion = useCallback((text: string) => {
    const custom: PartyQuestion = {
      id: `custom_${Date.now()}`,
      text,
      category: 'custom',
      isPremium: false,
    };
    setCurrentQuestion(custom);
  }, []);

  const handleStartAnalysis = useCallback(() => {
    setPhase('analyzing');
    setAnalysisElapsed(0);

    // Simulate fluctuating audio level during analysis
    let elapsed = 0;
    const interval = 100; // Update every 100ms
    analysisTimerRef.current = setInterval(() => {
      elapsed += interval;
      setAnalysisElapsed(elapsed);

      // Simulate audio level fluctuation
      audioLevelRef.current = 0.3 + Math.random() * 0.5;

      if (elapsed >= ANALYSIS_DURATION_MS) {
        if (analysisTimerRef.current) clearInterval(analysisTimerRef.current);
        analysisTimerRef.current = null;

        // Generate result
        const result = generateScore(audioLevelRef.current);
        setLastResult(result);

        // Save to player data
        setPlayers(prev => {
          const updated = [...prev];
          updated[currentPlayerIndex] = {
            ...updated[currentPlayerIndex],
            results: [
              ...updated[currentPlayerIndex].results,
              {
                question: currentQuestion?.text ?? 'Unknown',
                score: result.score,
                verdict: result.verdict,
                round,
              },
            ],
          };
          return updated;
        });

        setPhase('result');
      }
    }, interval);
  }, [currentPlayerIndex, currentQuestion, round]);

  const handleNextPlayer = useCallback(() => {
    const nextIndex = (currentPlayerIndex + 1) % players.length;
    const isNewRound = nextIndex === 0;

    setPhase('passPhone');
    setPassCountdown(PASS_PHONE_COUNTDOWN);

    let count = PASS_PHONE_COUNTDOWN;
    countdownTimerRef.current = setInterval(() => {
      count -= 1;
      setPassCountdown(count);
      if (count <= 0) {
        if (countdownTimerRef.current) clearInterval(countdownTimerRef.current);
        countdownTimerRef.current = null;
        setCurrentPlayerIndex(nextIndex);
        if (isNewRound) setRound(prev => prev + 1);
        pickQuestion(category);
        setPhase('round');
      }
    }, 1000);
  }, [currentPlayerIndex, players.length, category, pickQuestion]);

  const handleShowScoreboard = useCallback(() => {
    setPhase('scoreboard');
  }, []);

  const handleContinueFromScoreboard = useCallback(() => {
    handleNextPlayer();
  }, [handleNextPlayer]);

  const handleEndGame = useCallback(async () => {
    // Save session
    const sessionResults: DetectionResult[] = players.flatMap(p =>
      p.results.map((r, i) => ({
        id: generateId(),
        timestamp: Date.now() - (p.results.length - i) * 15000,
        mode: 'voice' as const,
        verdict: r.verdict,
        confidence: 70 + Math.round(Math.random() * 20),
        overallScore: r.score,
        breakdown: {
          physiological: Math.round(30 + Math.random() * 40),
          vocal: Math.round(40 + Math.random() * 40),
          facial: Math.round(20 + Math.random() * 40),
        },
        question: r.question,
        duration: ANALYSIS_DURATION_MS,
      })),
    );

    await saveSession({
      id: generateId(),
      startTime: Date.now() - round * players.length * 20000,
      endTime: Date.now(),
      mode: 'voice',
      results: sessionResults,
      participants: players.map(p => p.name),
      isPartyMode: true,
    });

    navigation.goBack();
  }, [players, round, navigation]);

  // --- Render ---

  switch (phase) {
    case 'setup':
      return (
        <View style={styles.screen}>
          <SetupPhase
            onStart={handleStart}
            onBack={() => navigation.goBack()}
          />
        </View>
      );

    case 'round':
      return (
        <View style={styles.screen}>
          <RoundPhase
            playerName={players[currentPlayerIndex]?.name ?? ''}
            roundNumber={round}
            totalPlayers={players.length}
            question={currentQuestion}
            category={category}
            onCategoryChange={handleCategoryChange}
            onCustomQuestion={handleCustomQuestion}
            onStartAnalysis={handleStartAnalysis}
          />
        </View>
      );

    case 'analyzing':
      return (
        <View style={styles.screen}>
          <AnalyzingPhase
            playerName={players[currentPlayerIndex]?.name ?? ''}
            question={currentQuestion?.text ?? ''}
            elapsed={analysisElapsed}
            total={ANALYSIS_DURATION_MS}
          />
        </View>
      );

    case 'result':
      return (
        <View style={styles.screen}>
          {lastResult && (
            <ResultPhase
              playerName={players[currentPlayerIndex]?.name ?? ''}
              question={currentQuestion?.text ?? ''}
              score={lastResult.score}
              verdict={lastResult.verdict}
              confidence={lastResult.confidence}
              onNext={handleNextPlayer}
              onScoreboard={handleShowScoreboard}
            />
          )}
        </View>
      );

    case 'scoreboard':
      return (
        <View style={styles.screen}>
          <ScoreboardPhase
            players={players}
            currentRound={round}
            onContinue={handleContinueFromScoreboard}
            onEndGame={handleEndGame}
          />
        </View>
      );

    case 'passPhone':
      return (
        <View style={styles.screen}>
          <PassPhonePhase
            nextPlayerName={players[(currentPlayerIndex + 1) % players.length]?.name ?? ''}
            countdown={passCountdown}
          />
        </View>
      );

    default:
      return null;
  }
}

// --- Styles ---

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg.primary,
  },
  phaseContainer: {
    flex: 1,
  },

  // --- Setup ---
  setupContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.bg.card,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
  },
  setupTitle: {
    ...typography.hero,
    color: colors.text.primary,
    marginBottom: spacing.xs,
  },
  setupSubtitle: {
    ...typography.body,
    color: colors.text.secondary,
    marginBottom: spacing.xl,
  },
  countSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
  },
  countLabel: {
    ...typography.h3,
    color: colors.text.primary,
  },
  countControls: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  countButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.bg.elevated,
    alignItems: 'center',
    justifyContent: 'center',
  },
  countButtonDisabled: {
    opacity: 0.4,
  },
  countValue: {
    fontSize: 32,
    fontWeight: '800',
    color: colors.accent.primary,
    minWidth: 40,
    textAlign: 'center',
  },
  nameInputs: {
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  nameIndex: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  nameIndexText: {
    ...typography.bodyBold,
    color: colors.accent.primary,
  },
  nameInput: {
    flex: 1,
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    color: colors.text.primary,
    ...typography.body,
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.md + 2,
    borderRadius: radii.lg,
  },
  startButtonText: {
    ...typography.bodyBold,
    color: '#FFFFFF',
    fontSize: 17,
  },

  // --- Round ---
  roundHeader: {
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  roundBadge: {
    ...typography.caption,
    color: colors.accent.primary,
    backgroundColor: colors.accent.primary + '15',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: radii.full,
    letterSpacing: 2,
    fontWeight: '700',
    overflow: 'hidden',
  },
  playerSpotlight: {
    marginHorizontal: spacing.lg,
    borderRadius: radii.lg,
    overflow: 'hidden',
    marginBottom: spacing.lg,
  },
  playerSpotlightGradient: {
    padding: spacing.lg,
    alignItems: 'center',
  },
  playerSpotlightName: {
    ...typography.hero,
    color: '#FFFFFF',
    textAlign: 'center',
  },
  playerSpotlightSub: {
    ...typography.caption,
    color: 'rgba(255,255,255,0.7)',
    marginTop: spacing.xs,
  },
  categoryTabs: {
    flexDirection: 'row',
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.lg,
  },
  categoryTab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    paddingVertical: spacing.sm + 2,
    borderRadius: radii.md,
    backgroundColor: colors.bg.card,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  categoryTabText: {
    ...typography.caption,
    color: colors.text.tertiary,
    fontWeight: '600',
  },
  questionCard: {
    marginHorizontal: spacing.lg,
    backgroundColor: colors.bg.card,
    borderRadius: radii.xl,
    padding: spacing.xl,
    alignItems: 'center',
    marginBottom: spacing.md,
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  questionEmoji: {
    fontSize: 36,
    marginBottom: spacing.md,
  },
  questionText: {
    ...typography.h2,
    color: colors.text.primary,
    textAlign: 'center',
    lineHeight: 30,
  },
  customToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    paddingVertical: spacing.sm,
    marginHorizontal: spacing.lg,
  },
  customToggleText: {
    ...typography.caption,
    color: colors.accent.primary,
  },
  customInputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: spacing.sm,
    marginHorizontal: spacing.lg,
  },
  customInput: {
    flex: 1,
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    color: colors.text.primary,
    ...typography.body,
    maxHeight: 80,
    borderWidth: 1,
    borderColor: colors.accent.primary + '40',
  },
  customConfirm: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.accent.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  bottomAction: {
    flex: 1,
    justifyContent: 'flex-end',
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xl,
  },
  analyzeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.md + 4,
    borderRadius: radii.lg,
  },
  analyzeButtonText: {
    ...typography.bodyBold,
    color: '#FFFFFF',
    fontSize: 18,
  },
  analyzeHint: {
    ...typography.small,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginTop: spacing.sm,
  },

  // --- Analyzing ---
  analyzingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.lg,
  },
  analyzingPlayer: {
    ...typography.h3,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },
  analyzingQuestion: {
    ...typography.body,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginBottom: spacing.xl,
    paddingHorizontal: spacing.lg,
  },
  gaugeContainer: {
    width: 200,
    height: 200,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.xl,
  },
  rotatingRing: {
    position: 'absolute',
    width: 200,
    height: 200,
    borderRadius: 100,
    overflow: 'hidden',
  },
  rotatingRingGradient: {
    flex: 1,
    borderRadius: 100,
    borderWidth: 3,
    borderColor: 'transparent',
    // Ring effect via border
    opacity: 0.3,
  },
  pulseOrb: {
    position: 'absolute',
    width: 160,
    height: 160,
    borderRadius: 80,
    overflow: 'hidden',
  },
  pulseOrbGradient: {
    flex: 1,
    borderRadius: 80,
  },
  gaugeScore: {
    fontSize: 48,
    fontWeight: '800',
    color: colors.accent.primary,
    zIndex: 1,
  },
  gaugeLabel: {
    ...typography.caption,
    color: colors.accent.primary,
    letterSpacing: 3,
    fontWeight: '700',
    zIndex: 1,
  },
  timerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginBottom: spacing.md,
  },
  timerText: {
    ...typography.bodyBold,
    color: colors.accent.primary,
  },
  progressTrack: {
    width: SCREEN_WIDTH - spacing.lg * 4,
    height: 6,
    backgroundColor: colors.bg.elevated,
    borderRadius: 3,
    overflow: 'hidden',
    marginBottom: spacing.lg,
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  analyzingHint: {
    ...typography.caption,
    color: colors.text.tertiary,
  },

  // --- Result ---
  resultContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.lg,
  },
  revealCard: {
    alignItems: 'center',
    width: '100%',
  },
  resultPlayerName: {
    ...typography.h3,
    color: colors.text.secondary,
    marginBottom: spacing.sm,
  },
  verdictBig: {
    fontSize: 52,
    fontWeight: '900',
    letterSpacing: 2,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  resultScoreRing: {
    marginBottom: spacing.lg,
  },
  resultScoreCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 4,
    backgroundColor: colors.bg.card,
    alignItems: 'center',
    justifyContent: 'center',
  },
  resultScoreNumber: {
    fontSize: 40,
    fontWeight: '800',
  },
  resultScoreLabel: {
    ...typography.small,
    color: colors.text.tertiary,
    letterSpacing: 2,
    fontWeight: '600',
  },
  resultConfidence: {
    ...typography.caption,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },
  resultSubtext: {
    ...typography.body,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  resultQuestionCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    width: '100%',
    marginBottom: spacing.lg,
  },
  resultQuestionLabel: {
    ...typography.small,
    color: colors.text.tertiary,
    marginBottom: spacing.xs,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  resultQuestionText: {
    ...typography.body,
    color: colors.text.secondary,
    fontStyle: 'italic',
  },
  resultActions: {
    flexDirection: 'row',
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xl,
    width: '100%',
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  secondaryButtonText: {
    ...typography.bodyBold,
    color: colors.accent.primary,
    fontSize: 14,
  },
  nextButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.md,
    borderRadius: radii.lg,
  },
  nextButtonText: {
    ...typography.bodyBold,
    color: '#FFFFFF',
  },

  // --- Scoreboard ---
  scoreboardTitle: {
    ...typography.hero,
    color: colors.text.primary,
    textAlign: 'center',
  },
  scoreboardRound: {
    ...typography.caption,
    color: colors.text.tertiary,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  scoreboardList: {
    flex: 1,
    paddingHorizontal: spacing.lg,
  },
  scoreboardRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    gap: spacing.md,
  },
  scoreboardRowFirst: {
    borderWidth: 1,
    borderColor: colors.accent.warning + '40',
    backgroundColor: colors.accent.warning + '08',
  },
  scoreboardRank: {
    width: 36,
    alignItems: 'center',
  },
  scoreboardCrown: {
    fontSize: 22,
  },
  scoreboardRankNum: {
    ...typography.h3,
    color: colors.text.tertiary,
  },
  scoreboardInfo: {
    flex: 1,
  },
  scoreboardName: {
    ...typography.bodyBold,
    color: colors.text.primary,
    marginBottom: 4,
  },
  scoreboardBadges: {
    flexDirection: 'row',
    gap: spacing.xs,
    flexWrap: 'wrap',
  },
  scoreBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: radii.full,
  },
  scoreBadgeText: {
    fontSize: 11,
    fontWeight: '700',
  },
  scoreboardTotal: {
    ...typography.caption,
    color: colors.text.tertiary,
  },
  scoreboardActions: {
    flexDirection: 'row',
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.lg,
  },

  // --- Pass Phone ---
  passContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.lg,
  },
  passEmoji: {
    fontSize: 72,
    marginBottom: spacing.lg,
  },
  passTitle: {
    ...typography.h2,
    color: colors.text.secondary,
    marginBottom: spacing.sm,
  },
  passPlayerName: {
    ...typography.hero,
    color: colors.accent.primary,
    fontSize: 42,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  passCountdown: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.bg.card,
    borderWidth: 3,
    borderColor: colors.accent.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
  },
  passCountdownNumber: {
    fontSize: 36,
    fontWeight: '800',
    color: colors.accent.primary,
  },
  passHint: {
    ...typography.caption,
    color: colors.text.tertiary,
  },
});
