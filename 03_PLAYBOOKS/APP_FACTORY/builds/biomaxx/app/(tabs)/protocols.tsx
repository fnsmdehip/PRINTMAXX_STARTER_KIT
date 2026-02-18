import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Modal,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useProtocolStore } from '../../src/stores/protocolStore';
import { useSubscriptionStore } from '../../src/stores/subscriptionStore';
import { ProtocolCard, Timer } from '../../src/components';
import { COLORS, DEFAULT_PROTOCOLS, PROTOCOL_CATEGORIES } from '../../src/utils/constants';
import { Protocol } from '../../src/types';

const CATEGORY_LABELS: Record<string, string> = {
  fasting: 'Fasting',
  cold: 'Cold Therapy',
  heat: 'Heat Therapy',
  light: 'Light Therapy',
  supplements: 'Supplements',
  movement: 'Movement',
  sleep: 'Sleep',
};

export default function Protocols() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [activeProtocol, setActiveProtocol] = useState<Protocol | null>(null);
  const [showTimer, setShowTimer] = useState(false);
  const [showLogModal, setShowLogModal] = useState(false);

  const activeSession = useProtocolStore((state) => state.activeSession);
  const startSession = useProtocolStore((state) => state.startSession);
  const pauseSession = useProtocolStore((state) => state.pauseSession);
  const resumeSession = useProtocolStore((state) => state.resumeSession);
  const endSession = useProtocolStore((state) => state.endSession);
  const logProtocol = useProtocolStore((state) => state.logProtocol);
  const getTodayLog = useProtocolStore((state) => state.getTodayLog);
  const getProtocolStreak = useProtocolStore((state) => state.getProtocolStreak);

  const canAccessPremiumContent = useSubscriptionStore((state) => state.canAccessPremiumContent);
  const isPremium = canAccessPremiumContent();

  const protocols = DEFAULT_PROTOCOLS as unknown as Protocol[];

  const filteredProtocols = selectedCategory
    ? protocols.filter((p) => p.category === selectedCategory)
    : protocols;

  const handleStartSession = useCallback(
    (protocol: Protocol) => {
      if (protocol.isPremium && !isPremium) {
        Alert.alert(
          'Premium Feature',
          'Upgrade to Premium to access this protocol.',
          [{ text: 'OK' }]
        );
        return;
      }

      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
      setActiveProtocol(protocol);
      startSession(protocol.id);
      setShowTimer(true);
    },
    [isPremium, startSession]
  );

  const handleLog = useCallback(
    (protocol: Protocol) => {
      if (protocol.isPremium && !isPremium) {
        Alert.alert(
          'Premium Feature',
          'Upgrade to Premium to access this protocol.',
          [{ text: 'OK' }]
        );
        return;
      }

      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
      setActiveProtocol(protocol);

      if (protocol.unit === 'count' || protocol.unit === 'boolean') {
        setShowLogModal(true);
      } else {
        // For hours/minutes, show quick input
        Alert.prompt(
          `Log ${protocol.name}`,
          `Enter ${protocol.unit} (goal: ${protocol.dailyGoal})`,
          [
            { text: 'Cancel', style: 'cancel' },
            {
              text: 'Log',
              onPress: (value) => {
                const numValue = parseFloat(value || '0');
                if (!isNaN(numValue) && numValue > 0) {
                  logProtocol(protocol.id, numValue);
                  Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
                }
              },
            },
          ],
          'plain-text',
          '',
          'numeric'
        );
      }
    },
    [isPremium, logProtocol]
  );

  const handleEndSession = useCallback(() => {
    const duration = endSession();
    setShowTimer(false);
    setActiveProtocol(null);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    if (duration > 0) {
      Alert.alert(
        'Session Complete',
        `Great work! You completed ${duration} minutes.`,
        [{ text: 'Nice!' }]
      );
    }
  }, [endSession]);

  const handleQuickLog = (value: number) => {
    if (activeProtocol) {
      logProtocol(activeProtocol.id, value);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setShowLogModal(false);
      setActiveProtocol(null);
    }
  };

  const handleProtocolPress = (protocol: Protocol) => {
    if (protocol.isPremium && !isPremium) {
      Alert.alert(
        'Premium Protocol',
        `${protocol.name} is a premium protocol. Upgrade to access all protocols and features.`,
        [{ text: 'OK' }]
      );
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>Protocols</Text>
        <Text style={styles.subtitle}>Build your daily practice</Text>
      </View>

      {/* Category Filter */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.categoriesContainer}
      >
        <TouchableOpacity
          style={[
            styles.categoryChip,
            !selectedCategory && styles.categoryChipActive,
          ]}
          onPress={() => {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            setSelectedCategory(null);
          }}
        >
          <Text
            style={[
              styles.categoryChipText,
              !selectedCategory && styles.categoryChipTextActive,
            ]}
          >
            All
          </Text>
        </TouchableOpacity>
        {PROTOCOL_CATEGORIES.map((category) => (
          <TouchableOpacity
            key={category}
            style={[
              styles.categoryChip,
              selectedCategory === category && styles.categoryChipActive,
            ]}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              setSelectedCategory(category);
            }}
          >
            <Text
              style={[
                styles.categoryChipText,
                selectedCategory === category && styles.categoryChipTextActive,
              ]}
            >
              {CATEGORY_LABELS[category]}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Protocol List */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {filteredProtocols.map((protocol) => (
          <ProtocolCard
            key={protocol.id}
            protocol={protocol}
            streak={getProtocolStreak(protocol.id)}
            todayValue={getTodayLog(protocol.id)}
            isPremiumUser={isPremium}
            onPress={() => handleProtocolPress(protocol)}
            onStartSession={() => handleStartSession(protocol)}
            onLog={() => handleLog(protocol)}
          />
        ))}
      </ScrollView>

      {/* Timer Modal */}
      <Modal visible={showTimer} animationType="slide" presentationStyle="pageSheet">
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <TouchableOpacity
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              }}
            >
              <View style={styles.modalHandle} />
            </TouchableOpacity>
            <Text style={styles.modalTitle}>{activeProtocol?.name}</Text>
            <Text style={styles.modalSubtitle}>{activeProtocol?.description}</Text>
          </View>

          {activeSession && activeProtocol && (
            <Timer
              isRunning={true}
              isPaused={activeSession.isPaused}
              startTime={activeSession.startTime}
              targetMinutes={
                activeProtocol.unit === 'hours'
                  ? activeProtocol.dailyGoal * 60
                  : activeProtocol.dailyGoal
              }
              onPause={pauseSession}
              onResume={resumeSession}
              onEnd={handleEndSession}
            />
          )}

          <View style={styles.modalFooter}>
            <TouchableOpacity
              style={styles.cancelButton}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setShowTimer(false);
                useProtocolStore.setState({ activeSession: null });
                setActiveProtocol(null);
              }}
            >
              <Text style={styles.cancelButtonText}>Cancel Session</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* Quick Log Modal */}
      <Modal visible={showLogModal} animationType="fade" transparent>
        <View style={styles.logModalOverlay}>
          <View style={styles.logModalContent}>
            <Text style={styles.logModalTitle}>
              Log {activeProtocol?.name}
            </Text>
            <Text style={styles.logModalSubtitle}>
              Goal: {activeProtocol?.dailyGoal} {activeProtocol?.unit}
            </Text>

            <View style={styles.logOptions}>
              {[1, 2, 3, 5].map((value) => (
                <TouchableOpacity
                  key={value}
                  style={styles.logOption}
                  onPress={() => handleQuickLog(value)}
                >
                  <Text style={styles.logOptionText}>+{value}</Text>
                </TouchableOpacity>
              ))}
            </View>

            <TouchableOpacity
              style={styles.logCancelButton}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setShowLogModal(false);
                setActiveProtocol(null);
              }}
            >
              <Text style={styles.logCancelText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 8,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  categoriesContainer: {
    paddingHorizontal: 20,
    paddingBottom: 16,
    gap: 8,
  },
  categoryChip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    marginRight: 8,
  },
  categoryChipActive: {
    backgroundColor: COLORS.primary,
  },
  categoryChipText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.textSecondary,
  },
  categoryChipTextActive: {
    color: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 100,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingTop: 20,
  },
  modalHeader: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  modalHandle: {
    width: 40,
    height: 4,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: 2,
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  modalSubtitle: {
    fontSize: 15,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  modalFooter: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  cancelButton: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  cancelButtonText: {
    fontSize: 15,
    color: COLORS.error,
    fontWeight: '500',
  },
  logModalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  logModalContent: {
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    padding: 24,
    width: '100%',
    maxWidth: 320,
  },
  logModalTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 4,
  },
  logModalSubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 24,
  },
  logOptions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  logOption: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logOptionText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.primary,
  },
  logCancelButton: {
    paddingVertical: 12,
    alignItems: 'center',
  },
  logCancelText: {
    fontSize: 15,
    color: COLORS.textMuted,
  },
});
