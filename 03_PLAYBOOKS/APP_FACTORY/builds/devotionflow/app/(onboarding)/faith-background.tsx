import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { useUserStore, FaithBackground } from '@/store/userStore';

interface FaithOption {
  id: FaithBackground;
  title: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
}

const faithOptions: FaithOption[] = [
  {
    id: 'new',
    title: 'New to faith',
    description: 'I am exploring Christianity or recently started my journey',
    icon: 'sparkles',
  },
  {
    id: 'growing',
    title: 'Growing in faith',
    description: 'I have a foundation and want to go deeper',
    icon: 'leaf',
  },
  {
    id: 'mature',
    title: 'Mature believer',
    description: 'I have walked with God for many years',
    icon: 'shield-checkmark',
  },
  {
    id: 'returning',
    title: 'Returning to faith',
    description: 'I am reconnecting with my spiritual life',
    icon: 'refresh',
  },
];

export default function FaithBackgroundScreen() {
  const router = useRouter();
  const { setProfile } = useUserStore();
  const [selected, setSelected] = useState<FaithBackground | null>(null);

  const handleContinue = () => {
    if (selected) {
      setProfile({ faithBackground: selected });
      router.push('/(onboarding)/notifications');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.step}>Step 1 of 3</Text>
          <Text style={styles.title}>Where are you on your faith journey?</Text>
          <Text style={styles.subtitle}>
            This helps us personalize your devotional experience
          </Text>
        </View>

        {/* Options */}
        <View style={styles.options}>
          {faithOptions.map((option) => (
            <Pressable
              key={option.id}
              style={[
                styles.optionCard,
                selected === option.id && styles.optionCardSelected,
              ]}
              onPress={() => setSelected(option.id)}
            >
              <View
                style={[
                  styles.optionIcon,
                  selected === option.id && styles.optionIconSelected,
                ]}
              >
                <Ionicons
                  name={option.icon}
                  size={28}
                  color={selected === option.id ? colors.surface : colors.primary}
                />
              </View>
              <View style={styles.optionText}>
                <Text
                  style={[
                    styles.optionTitle,
                    selected === option.id && styles.optionTitleSelected,
                  ]}
                >
                  {option.title}
                </Text>
                <Text style={styles.optionDescription}>{option.description}</Text>
              </View>
              <View style={styles.radioContainer}>
                <View
                  style={[
                    styles.radioOuter,
                    selected === option.id && styles.radioOuterSelected,
                  ]}
                >
                  {selected === option.id && <View style={styles.radioInner} />}
                </View>
              </View>
            </Pressable>
          ))}
        </View>
      </ScrollView>

      {/* CTA Button */}
      <View style={styles.ctaContainer}>
        <Pressable
          style={({ pressed }) => [
            styles.ctaButton,
            !selected && styles.ctaButtonDisabled,
            pressed && selected && styles.ctaButtonPressed,
          ]}
          onPress={handleContinue}
          disabled={!selected}
        >
          <Text style={styles.ctaText}>Continue</Text>
          <Ionicons name="arrow-forward" size={20} color={colors.surface} />
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: 120,
  },
  header: {
    marginBottom: spacing.xl,
  },
  step: {
    ...typography.caption,
    color: colors.primary,
    marginBottom: spacing.sm,
    fontWeight: '600',
  },
  title: {
    ...typography.h1,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
  },
  options: {
    gap: spacing.md,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    ...shadows.sm,
  },
  optionCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  optionIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  optionIconSelected: {
    backgroundColor: colors.primary,
  },
  optionText: {
    flex: 1,
  },
  optionTitle: {
    ...typography.bodyBold,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  optionTitleSelected: {
    color: colors.primary,
  },
  optionDescription: {
    ...typography.caption,
    color: colors.textMuted,
  },
  radioContainer: {
    marginLeft: spacing.sm,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  radioOuterSelected: {
    borderColor: colors.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.primary,
  },
  ctaContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  ctaButtonDisabled: {
    backgroundColor: colors.textMuted,
  },
  ctaButtonPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
  ctaText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
});
