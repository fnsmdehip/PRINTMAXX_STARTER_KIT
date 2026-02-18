import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  TouchableOpacity,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Button } from '../components';
import { Colors, FaithType } from '../constants';
import { useApp } from '../context/AppContext';

type RootStackParamList = {
  Onboarding: undefined;
  Main: undefined;
  Paywall: undefined;
};

type OnboardingScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Onboarding'>;
};

interface FaithOption {
  id: FaithType;
  label: string;
  icon: string;
  description: string;
}

const FAITH_OPTIONS: FaithOption[] = [
  {
    id: 'christianity',
    label: 'Christianity',
    icon: '\u271D',
    description: 'Bible verses, prayer prompts, morning devotional lock',
  },
  {
    id: 'islam',
    label: 'Islam',
    icon: '\u262A',
    description: 'Salah times, Quran verses, 5-prayer daily tracker',
  },
  {
    id: 'general',
    label: 'Mindfulness',
    icon: '\u2728',
    description: 'Meditation prompts, reflection time, morning ritual',
  },
];

export function OnboardingScreen({ navigation }: OnboardingScreenProps) {
  const { completeOnboarding } = useApp();
  const [selectedFaith, setSelectedFaith] = useState<FaithType | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState<'welcome' | 'faith'>('welcome');

  const handleContinue = async () => {
    if (step === 'welcome') {
      setStep('faith');
      return;
    }

    if (!selectedFaith) return;

    setIsLoading(true);
    try {
      await completeOnboarding(selectedFaith);
    } catch {
      setIsLoading(false);
    }
  };

  if (step === 'welcome') {
    return (
      <LinearGradient
        colors={[Colors.gradientStart, Colors.gradientEnd]}
        style={styles.container}
      >
        <StatusBar barStyle="light-content" />
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.welcomeContent}>
            <Text style={styles.appIcon}>{'🙏'}</Text>
            <Text style={styles.welcomeTitle}>PrayerLock</Text>
            <Text style={styles.welcomeSubtitle}>
              Put prayer first. Phone second.
            </Text>

            <View style={styles.welcomeFeatures}>
              <View style={styles.featureItem}>
                <Text style={styles.featureBullet}>{'\u25CF'}</Text>
                <Text style={styles.featureText}>
                  Lock your phone until you pray
                </Text>
              </View>
              <View style={styles.featureItem}>
                <Text style={styles.featureBullet}>{'\u25CF'}</Text>
                <Text style={styles.featureText}>
                  Build a daily prayer streak
                </Text>
              </View>
              <View style={styles.featureItem}>
                <Text style={styles.featureBullet}>{'\u25CF'}</Text>
                <Text style={styles.featureText}>
                  Daily verses and prayer prompts
                </Text>
              </View>
            </View>
          </View>

          <View style={styles.bottomActions}>
            <Button
              title="Get Started"
              onPress={handleContinue}
              size="large"
            />
          </View>
        </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient
      colors={[Colors.gradientStart, Colors.gradientEnd]}
      style={styles.container}
    >
      <StatusBar barStyle="light-content" />
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.faithContent}>
          <Text style={styles.faithTitle}>Choose your path</Text>
          <Text style={styles.faithSubtitle}>
            We'll personalize your experience
          </Text>

          <View style={styles.faithOptions}>
            {FAITH_OPTIONS.map((option) => (
              <TouchableOpacity
                key={option.id}
                style={[
                  styles.faithCard,
                  selectedFaith === option.id && styles.faithCardSelected,
                ]}
                onPress={() => setSelectedFaith(option.id)}
                activeOpacity={0.7}
              >
                <Text style={styles.faithIcon}>{option.icon}</Text>
                <View style={styles.faithCardInfo}>
                  <Text style={[
                    styles.faithLabel,
                    selectedFaith === option.id && styles.faithLabelSelected,
                  ]}>
                    {option.label}
                  </Text>
                  <Text style={styles.faithDescription}>
                    {option.description}
                  </Text>
                </View>
                <View style={[
                  styles.radioOuter,
                  selectedFaith === option.id && styles.radioOuterSelected,
                ]}>
                  {selectedFaith === option.id && <View style={styles.radioInner} />}
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.bottomActions}>
          <Button
            title="Continue"
            onPress={handleContinue}
            size="large"
            loading={isLoading}
            disabled={!selectedFaith}
            style={!selectedFaith ? styles.disabledButton : undefined}
          />
          <Text style={styles.changeNote}>
            You can change this later in settings
          </Text>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: 20,
  },
  welcomeContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  appIcon: {
    fontSize: 72,
    marginBottom: 24,
  },
  welcomeTitle: {
    fontSize: 40,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 12,
  },
  welcomeSubtitle: {
    fontSize: 18,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    marginBottom: 48,
  },
  welcomeFeatures: {
    width: '100%',
    gap: 16,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  featureBullet: {
    color: Colors.primary,
    fontSize: 10,
    marginRight: 12,
  },
  featureText: {
    fontSize: 17,
    color: 'rgba(255, 255, 255, 0.9)',
    lineHeight: 24,
  },
  faithContent: {
    flex: 1,
    paddingTop: 60,
  },
  faithTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 8,
    textAlign: 'center',
  },
  faithSubtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.7)',
    textAlign: 'center',
    marginBottom: 40,
  },
  faithOptions: {
    gap: 12,
  },
  faithCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  faithCardSelected: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderColor: Colors.primary,
  },
  faithIcon: {
    fontSize: 32,
    marginRight: 16,
  },
  faithCardInfo: {
    flex: 1,
  },
  faithLabel: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.white,
    marginBottom: 4,
  },
  faithLabelSelected: {
    color: Colors.primary,
  },
  faithDescription: {
    fontSize: 13,
    color: 'rgba(255, 255, 255, 0.6)',
    lineHeight: 18,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 12,
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
  bottomActions: {
    marginBottom: 40,
    gap: 12,
  },
  disabledButton: {
    opacity: 0.5,
  },
  changeNote: {
    textAlign: 'center',
    fontSize: 13,
    color: 'rgba(255, 255, 255, 0.5)',
  },
});
