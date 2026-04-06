import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  View, Text, StyleSheet, TextInput, ScrollView, Dimensions, Keyboard,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { LinearGradient } from 'expo-linear-gradient';
import { Audio } from 'expo-av';
import Animated, {
  useSharedValue, useAnimatedStyle, withTiming, withRepeat, withSequence,
  withSpring, withDelay, Easing, FadeIn, FadeInDown, ZoomIn, runOnJS,
} from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Haptics from 'expo-haptics';
import { playSound, playVerdictReveal } from '../sounds/SoundEngine';
import { colors, spacing, radii, typography } from '../theme';
import { getRandomQuestion } from '../utils/partyQuestions';
import { PartyQuestion, Verdict, DetectionResult } from '../utils/types';
import { saveSession, generateId } from '../store';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

type GamePhase = 'setup' | 'round' | 'analyzing' | 'result' | 'scoreboard' | 'passPhone';
type QuestionCategory = 'mild' | 'spicy' | 'random';

interface PlayerData { name: string; results: PlayerResult[]; }
interface PlayerResult { question: string; score: number; verdict: Verdict; round: number; }

const MIN_PLAYERS = 2;
const MAX_PLAYERS = 8;
const ANALYSIS_DURATION_MS = 10000;
const PASS_PHONE_COUNTDOWN = 5;

const CATEGORY_CONFIG: Record<QuestionCategory, { label: string; color: string; icon: keyof typeof Ionicons.glyphMap }> = {
  mild: { label: 'Mild', color: colors.accent.success, icon: 'happy-outline' },
  spicy: { label: 'Spicy', color: colors.accent.tertiary, icon: 'flame-outline' },
  random: { label: 'Random', color: colors.accent.warning, icon: 'shuffle-outline' },
};

function generateScore(audioSamples: number[]): { score: number; verdict: Verdict; confidence: number } {
  // Score derived from REAL audio metering data only
  if (audioSamples.length < 3) {
    return { score: 50, verdict: 'uncertain', confidence: 30 };
  }
  const mean = audioSamples.reduce((a, b) => a + b, 0) / audioSamples.length;
  const variance = audioSamples.reduce((a, b) => a + (b - mean) ** 2, 0) / audioSamples.length;
  const stdDev = Math.sqrt(variance);
  const varianceScore = Math.min(50, stdDev * 150);
  const energyScore = Math.min(50, mean * 80);
  const score = Math.round(Math.max(5, Math.min(98, varianceScore + energyScore)));
  let verdict: Verdict;
  if (score >= 60) verdict = 'deceptive';
  else if (score <= 35) verdict = 'truthful';
  else verdict = 'uncertain';
  const confidence = Math.min(90, 30 + audioSamples.length * 2);
  return { score, verdict, confidence };
}

export default function PartyModeScreen({ navigation }: { navigation: any }) {
  const insets = useSafeAreaInsets();
  const [phase, setPhase] = useState<GamePhase>('setup');
  const [players, setPlayers] = useState<PlayerData[]>([{ name: '', results: [] }, { name: '', results: [] }]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [currentRound, setCurrentRound] = useState(1);
  const [totalRounds, setTotalRounds] = useState(3);
  const [category, setCategory] = useState<QuestionCategory>('mild');
  const [currentQuestion, setCurrentQuestion] = useState<PartyQuestion | null>(null);
  const [usedQuestionIds, setUsedQuestionIds] = useState<string[]>([]);
  const [passCountdown, setPassCountdown] = useState(PASS_PHONE_COUNTDOWN);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [lastResult, setLastResult] = useState<{ score: number; verdict: Verdict } | null>(null);

  const audioSamples = useRef<number[]>([]);
  const recordingRef = useRef<Audio.Recording | null>(null);
  const analysisTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const passTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const pulseAnim = useSharedValue(1);

  const currentPlayer = players[currentPlayerIndex];

  const addPlayer = () => {
    if (players.length < MAX_PLAYERS) {
      playSound('tap');
      setPlayers([...players, { name: '', results: [] }]);
    }
  };

  const removePlayer = (index: number) => {
    if (players.length > MIN_PLAYERS) {
      playSound('tap');
      setPlayers(players.filter((_, i) => i !== index));
    }
  };

  const updatePlayerName = (index: number, name: string) => {
    const updated = [...players];
    updated[index] = { ...updated[index], name };
    setPlayers(updated);
  };

  const startGame = () => {
    const named = players.map((p, i) => ({ ...p, name: p.name.trim() || `Player ${i + 1}` }));
    setPlayers(named);
    playSound('scanStart');
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setCurrentPlayerIndex(0);
    setCurrentRound(1);
    pickQuestion();
    setPhase('passPhone');
    startPassCountdown();
  };

  const pickQuestion = () => {
    const q = getRandomQuestion(category === 'random' ? undefined : category, false, usedQuestionIds);
    if (q) {
      setCurrentQuestion(q);
      setUsedQuestionIds(prev => [...prev, q.id]);
    }
  };

  const startPassCountdown = () => {
    setPassCountdown(PASS_PHONE_COUNTDOWN);
    passTimerRef.current = setInterval(() => {
      setPassCountdown(prev => {
        if (prev <= 1) {
          if (passTimerRef.current) clearInterval(passTimerRef.current);
          setPhase('round');
          return 0;
        }
        playSound('countdown');
        return prev - 1;
      });
    }, 1000);
  };

  const startAnalysis = async () => {
    playSound('analyzeStart');
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setPhase('analyzing');
    setAnalysisProgress(0);
    audioSamples.current = [];

    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
      const recording = new Audio.Recording();
      await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      recording.setOnRecordingStatusUpdate((status) => {
        if (status.isRecording && status.metering !== undefined) {
          const level = Math.max(0, (status.metering + 60) / 60);
          audioSamples.current.push(level);
        }
      });
      await recording.startAsync();
      recordingRef.current = recording;
    } catch {
      // Mic unavailable, will score with empty samples
    }

    let elapsed = 0;
    analysisTimerRef.current = setInterval(() => {
      elapsed += 200;
      setAnalysisProgress(Math.min(1, elapsed / ANALYSIS_DURATION_MS));
      if (elapsed >= ANALYSIS_DURATION_MS) {
        if (analysisTimerRef.current) clearInterval(analysisTimerRef.current);
        finishAnalysis();
      }
    }, 200);
  };

  const finishAnalysis = async () => {
    if (recordingRef.current) {
      try { await recordingRef.current.stopAndUnloadAsync(); } catch {}
      recordingRef.current = null;
    }

    const { score, verdict, confidence } = generateScore(audioSamples.current);
    if (verdict !== 'scanning') playVerdictReveal(verdict);
    Haptics.notificationAsync(
      verdict === 'truthful' ? Haptics.NotificationFeedbackType.Success
      : verdict === 'deceptive' ? Haptics.NotificationFeedbackType.Error
      : Haptics.NotificationFeedbackType.Warning
    );

    setLastResult({ score, verdict });

    const updated = [...players];
    updated[currentPlayerIndex].results.push({
      question: currentQuestion?.text ?? '',
      score, verdict, round: currentRound,
    });
    setPlayers(updated);
    setPhase('result');
  };

  const nextTurn = () => {
    playSound('playerSwitch');
    const nextPlayer = currentPlayerIndex + 1;
    if (nextPlayer >= players.length) {
      if (currentRound >= totalRounds) {
        playSound('roundComplete');
        setPhase('scoreboard');
        saveGameSession();
        return;
      }
      setCurrentRound(prev => prev + 1);
      setCurrentPlayerIndex(0);
    } else {
      setCurrentPlayerIndex(nextPlayer);
    }
    pickQuestion();
    setPhase('passPhone');
    startPassCountdown();
  };

  const saveGameSession = async () => {
    const results: DetectionResult[] = players.flatMap(p =>
      p.results.map(r => ({
        id: generateId(), timestamp: Date.now(), mode: 'voice' as const,
        verdict: r.verdict, confidence: 60, overallScore: r.score,
        breakdown: { physiological: 0, vocal: r.score, facial: 0 },
        question: r.question, duration: ANALYSIS_DURATION_MS / 1000,
      }))
    );
    await saveSession({
      id: generateId(), startTime: Date.now() - totalRounds * players.length * 15000,
      endTime: Date.now(), mode: 'voice', results, participants: players.map(p => p.name),
      isPartyMode: true,
    });
  };

  useEffect(() => {
    return () => {
      if (analysisTimerRef.current) clearInterval(analysisTimerRef.current);
      if (passTimerRef.current) clearInterval(passTimerRef.current);
      if (recordingRef.current) {
        recordingRef.current.stopAndUnloadAsync().catch(() => {});
      }
    };
  }, []);

  const getVerdictColor = (v: Verdict) =>
    v === 'truthful' ? colors.accent.success : v === 'deceptive' ? colors.accent.tertiary : colors.accent.warning;

  // --- RENDER ---

  if (phase === 'setup') {
    return (
      <ScrollView style={styles.screen} contentContainerStyle={[styles.setupContent, { paddingTop: insets.top + spacing.md }]}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => { playSound('swipe'); navigation.goBack(); }} style={styles.backButton} sound="tap">
            <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Party Mode</Text>
          <View style={{ width: 40 }} />
        </View>

        <Text style={styles.sectionLabel}>Players ({players.length}/{MAX_PLAYERS})</Text>
        {players.map((player, i) => (
          <View key={i} style={styles.playerRow}>
            <View style={styles.playerNumber}><Text style={styles.playerNumberText}>{i + 1}</Text></View>
            <TextInput style={styles.playerInput} placeholder={`Player ${i + 1}`}
              placeholderTextColor={colors.text.tertiary} value={player.name}
              onChangeText={(text) => updatePlayerName(i, text)} />
            {players.length > MIN_PLAYERS && (
              <TouchableOpacity onPress={() => removePlayer(i)} sound="tap">
                <Ionicons name="close-circle" size={24} color={colors.text.tertiary} />
              </TouchableOpacity>
            )}
          </View>
        ))}
        {players.length < MAX_PLAYERS && (
          <TouchableOpacity onPress={addPlayer} style={styles.addPlayerButton} sound="tap">
            <Ionicons name="add-circle-outline" size={20} color={colors.accent.primary} />
            <Text style={styles.addPlayerText}>Add Player</Text>
          </TouchableOpacity>
        )}

        <Text style={[styles.sectionLabel, { marginTop: spacing.lg }]}>Question Category</Text>
        <View style={styles.categoryRow}>
          {(['mild', 'spicy', 'random'] as QuestionCategory[]).map((cat) => {
            const conf = CATEGORY_CONFIG[cat];
            const active = category === cat;
            return (
              <TouchableOpacity key={cat} style={[styles.categoryChip, active && { backgroundColor: conf.color + '20', borderColor: conf.color }]}
                onPress={() => setCategory(cat)} sound="toggle">
                <Ionicons name={conf.icon} size={16} color={active ? conf.color : colors.text.tertiary} />
                <Text style={[styles.categoryLabel, active && { color: conf.color }]}>{conf.label}</Text>
              </TouchableOpacity>
            );
          })}
        </View>

        <Text style={[styles.sectionLabel, { marginTop: spacing.lg }]}>Rounds</Text>
        <View style={styles.roundsRow}>
          {[1, 2, 3, 5].map((n) => (
            <TouchableOpacity key={n} style={[styles.roundChip, totalRounds === n && styles.roundChipActive]}
              onPress={() => setTotalRounds(n)} sound="toggle">
              <Text style={[styles.roundChipText, totalRounds === n && styles.roundChipTextActive]}>{n}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <TouchableOpacity onPress={startGame} style={styles.startGameButton} sound="scanStart" haptic="heavy">
          <LinearGradient colors={['#7B61FF', '#FF3D71', '#FFAA00']} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
            style={styles.startGameGradient}>
            <Text style={styles.startGameText}>Start Game</Text>
          </LinearGradient>
        </TouchableOpacity>

        <View style={{ height: insets.bottom + spacing.xl }} />
      </ScrollView>
    );
  }

  if (phase === 'passPhone') {
    return (
      <View style={[styles.screen, styles.centered, { paddingTop: insets.top }]}>
        <Animated.View entering={ZoomIn.duration(300)}>
          <Text style={styles.passTitle}>Pass to</Text>
          <Text style={styles.passName}>{players[currentPlayerIndex]?.name}</Text>
          <Text style={styles.passCountdown}>{passCountdown}</Text>
          <Text style={styles.passSubtitle}>Round {currentRound} of {totalRounds}</Text>
        </Animated.View>
      </View>
    );
  }

  if (phase === 'round') {
    return (
      <View style={[styles.screen, styles.centered, { paddingTop: insets.top }]}>
        <Animated.View entering={FadeInDown.duration(400)} style={styles.roundContainer}>
          <Text style={styles.roundLabel}>Round {currentRound} / {totalRounds}</Text>
          <Text style={styles.playerName}>{currentPlayer?.name}</Text>
          <View style={styles.questionCard}>
            <Ionicons name="help-circle" size={24} color={colors.accent.primary} />
            <Text style={styles.questionText}>{currentQuestion?.text ?? 'No question available'}</Text>
          </View>
          <Text style={styles.roundInstruction}>Answer the question out loud, then tap Analyze.</Text>
          <TouchableOpacity onPress={startAnalysis} style={styles.analyzeButton} sound="analyzeStart" haptic="heavy">
            <LinearGradient colors={[...colors.gradient.scanning]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
              style={styles.analyzeGradient}>
              <Ionicons name="mic" size={24} color="#FFFFFF" />
              <Text style={styles.analyzeText}>Analyze Response</Text>
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>
      </View>
    );
  }

  if (phase === 'analyzing') {
    return (
      <View style={[styles.screen, styles.centered, { paddingTop: insets.top }]}>
        <Animated.View entering={FadeIn.duration(300)} style={styles.analyzingContainer}>
          <Ionicons name="mic" size={48} color={colors.accent.primary} />
          <Text style={styles.analyzingTitle}>Analyzing...</Text>
          <Text style={styles.analyzingSubtitle}>Speak your answer clearly</Text>
          <View style={styles.progressTrack}>
            <View style={[styles.progressFill, { width: `${analysisProgress * 100}%` }]} />
          </View>
          <Text style={styles.analyzingPercent}>{Math.round(analysisProgress * 100)}%</Text>
        </Animated.View>
      </View>
    );
  }

  if (phase === 'result' && lastResult) {
    const resultColor = getVerdictColor(lastResult.verdict);
    return (
      <View style={[styles.screen, styles.centered, { paddingTop: insets.top }]}>
        <Animated.View entering={ZoomIn.duration(400)} style={styles.resultContainer}>
          <Text style={[styles.resultScore, { color: resultColor }]}>{lastResult.score}</Text>
          <Text style={[styles.resultVerdict, { color: resultColor }]}>{lastResult.verdict.toUpperCase()}</Text>
          <Text style={styles.resultPlayer}>{currentPlayer?.name}</Text>
          <TouchableOpacity onPress={nextTurn} style={styles.nextButton} sound="playerSwitch" haptic="medium">
            <LinearGradient colors={['#7B61FF', '#FF3D71']} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
              style={styles.nextGradient}>
              <Text style={styles.nextText}>
                {currentPlayerIndex + 1 >= players.length && currentRound >= totalRounds ? 'See Scoreboard' : 'Next Player'}
              </Text>
              <Ionicons name="arrow-forward" size={20} color="#FFFFFF" />
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>
      </View>
    );
  }

  if (phase === 'scoreboard') {
    const sorted = [...players].sort((a, b) => {
      const avgA = a.results.length > 0 ? a.results.reduce((s, r) => s + r.score, 0) / a.results.length : 0;
      const avgB = b.results.length > 0 ? b.results.reduce((s, r) => s + r.score, 0) / b.results.length : 0;
      return avgB - avgA;
    });

    return (
      <ScrollView style={styles.screen} contentContainerStyle={[styles.scoreboardContent, { paddingTop: insets.top + spacing.md }]}>
        <Text style={styles.scoreboardTitle}>Final Scoreboard</Text>
        {sorted.map((player, i) => {
          const avgScore = player.results.length > 0
            ? Math.round(player.results.reduce((s, r) => s + r.score, 0) / player.results.length) : 0;
          const medal = i === 0 ? '🏆' : i === 1 ? '🥈' : i === 2 ? '🥉' : '';
          return (
            <Animated.View key={i} entering={FadeInDown.delay(i * 100).duration(300)}>
              <View style={styles.scoreboardRow}>
                <Text style={styles.scoreboardRank}>{medal || `${i + 1}`}</Text>
                <View style={styles.scoreboardInfo}>
                  <Text style={styles.scoreboardName}>{player.name}</Text>
                  <Text style={styles.scoreboardRounds}>{player.results.length} rounds</Text>
                </View>
                <Text style={[styles.scoreboardScore, { color: avgScore >= 60 ? colors.accent.tertiary : avgScore <= 35 ? colors.accent.success : colors.accent.warning }]}>
                  {avgScore}
                </Text>
              </View>
            </Animated.View>
          );
        })}
        <TouchableOpacity onPress={() => { playSound('success'); navigation.navigate('Home'); }}
          style={styles.doneButton} sound="success" haptic="success">
          <Text style={styles.doneText}>Done</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => { setPhase('setup'); setPlayers(players.map(p => ({ ...p, results: [] }))); setUsedQuestionIds([]); }}
          style={styles.replayButton} sound="tap">
          <Text style={styles.replayText}>Play Again</Text>
        </TouchableOpacity>
        <View style={{ height: insets.bottom + spacing.xl }} />
      </ScrollView>
    );
  }

  return <View style={styles.screen} />;
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg.primary },
  centered: { alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.lg },
  setupContent: { paddingHorizontal: spacing.lg },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.xl },
  backButton: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.bg.card, alignItems: 'center', justifyContent: 'center' },
  headerTitle: { ...typography.h1, color: colors.text.primary },
  sectionLabel: { ...typography.caption, color: colors.text.tertiary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: spacing.sm },
  playerRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.sm },
  playerNumber: { width: 32, height: 32, borderRadius: 16, backgroundColor: colors.accent.primary + '20', alignItems: 'center', justifyContent: 'center' },
  playerNumberText: { ...typography.bodyBold, color: colors.accent.primary, fontSize: 14 },
  playerInput: { flex: 1, ...typography.body, color: colors.text.primary, backgroundColor: colors.bg.card, borderRadius: radii.sm, paddingHorizontal: spacing.md, paddingVertical: spacing.sm },
  addPlayerButton: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingVertical: spacing.sm },
  addPlayerText: { ...typography.body, color: colors.accent.primary },
  categoryRow: { flexDirection: 'row', gap: spacing.sm },
  categoryChip: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, paddingVertical: spacing.sm, borderRadius: radii.sm, backgroundColor: colors.bg.card, borderWidth: 1, borderColor: 'transparent' },
  categoryLabel: { ...typography.caption, color: colors.text.tertiary },
  roundsRow: { flexDirection: 'row', gap: spacing.sm },
  roundChip: { width: 48, height: 48, borderRadius: radii.sm, backgroundColor: colors.bg.card, alignItems: 'center', justifyContent: 'center' },
  roundChipActive: { backgroundColor: colors.accent.primary + '20' },
  roundChipText: { ...typography.bodyBold, color: colors.text.secondary },
  roundChipTextActive: { color: colors.accent.primary },
  startGameButton: { borderRadius: radii.lg, overflow: 'hidden', marginTop: spacing.xl },
  startGameGradient: { paddingVertical: spacing.md, alignItems: 'center' },
  startGameText: { ...typography.h3, color: '#FFFFFF', fontWeight: '800' },
  passTitle: { ...typography.h2, color: colors.text.secondary, textAlign: 'center' },
  passName: { ...typography.hero, color: colors.accent.primary, textAlign: 'center', marginVertical: spacing.md },
  passCountdown: { fontSize: 80, fontWeight: '800', color: colors.text.primary, textAlign: 'center' },
  passSubtitle: { ...typography.body, color: colors.text.tertiary, textAlign: 'center', marginTop: spacing.md },
  roundContainer: { width: '100%', alignItems: 'center', gap: spacing.lg },
  roundLabel: { ...typography.caption, color: colors.text.tertiary, textTransform: 'uppercase', letterSpacing: 2 },
  playerName: { ...typography.h1, color: colors.accent.primary },
  questionCard: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: colors.bg.card, borderRadius: radii.lg, padding: spacing.lg, width: '100%' },
  questionText: { ...typography.body, color: colors.text.primary, flex: 1, fontSize: 18 },
  roundInstruction: { ...typography.caption, color: colors.text.tertiary, textAlign: 'center' },
  analyzeButton: { borderRadius: radii.lg, overflow: 'hidden', width: '100%' },
  analyzeGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: spacing.md },
  analyzeText: { ...typography.bodyBold, color: '#FFFFFF', fontSize: 17 },
  analyzingContainer: { alignItems: 'center', gap: spacing.md },
  analyzingTitle: { ...typography.h2, color: colors.accent.primary },
  analyzingSubtitle: { ...typography.body, color: colors.text.secondary },
  progressTrack: { width: SCREEN_WIDTH * 0.6, height: 6, backgroundColor: colors.bg.tertiary, borderRadius: 3, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: colors.accent.primary, borderRadius: 3 },
  analyzingPercent: { ...typography.mono, color: colors.text.tertiary },
  resultContainer: { alignItems: 'center', gap: spacing.md },
  resultScore: { fontSize: 80, fontWeight: '800', letterSpacing: -4 },
  resultVerdict: { ...typography.h2, letterSpacing: 6 },
  resultPlayer: { ...typography.body, color: colors.text.secondary },
  nextButton: { borderRadius: radii.lg, overflow: 'hidden', width: SCREEN_WIDTH * 0.7, marginTop: spacing.lg },
  nextGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: spacing.md },
  nextText: { ...typography.bodyBold, color: '#FFFFFF' },
  scoreboardContent: { paddingHorizontal: spacing.lg },
  scoreboardTitle: { ...typography.hero, color: colors.text.primary, textAlign: 'center', marginBottom: spacing.xl },
  scoreboardRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, gap: spacing.md, marginBottom: spacing.sm },
  scoreboardRank: { fontSize: 24, width: 40, textAlign: 'center' },
  scoreboardInfo: { flex: 1 },
  scoreboardName: { ...typography.bodyBold, color: colors.text.primary },
  scoreboardRounds: { ...typography.small, color: colors.text.tertiary },
  scoreboardScore: { fontSize: 28, fontWeight: '800' },
  doneButton: { backgroundColor: colors.accent.primary, borderRadius: radii.lg, paddingVertical: spacing.md, alignItems: 'center', marginTop: spacing.xl },
  doneText: { ...typography.bodyBold, color: '#FFFFFF' },
  replayButton: { alignItems: 'center', paddingVertical: spacing.md },
  replayText: { ...typography.body, color: colors.text.secondary },
});
