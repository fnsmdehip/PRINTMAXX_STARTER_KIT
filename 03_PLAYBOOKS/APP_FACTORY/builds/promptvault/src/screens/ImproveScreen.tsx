import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';
import * as Haptics from 'expo-haptics';
import Toast from '../components/Toast';
import Paywall from '../components/Paywall';
import { useSubscriptionStore } from '../stores/subscriptionStore';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';

export default function ImproveScreen() {
  const [inputPrompt, setInputPrompt] = useState('');
  const [improvedPrompt, setImprovedPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);
  const [paywallVisible, setPaywallVisible] = useState(false);

  const { isPro } = useSubscriptionStore();

  const handleImprove = async () => {
    if (!isPro) {
      setPaywallVisible(true);
      return;
    }

    if (!inputPrompt.trim()) {
      return;
    }

    setLoading(true);
    setImprovedPrompt('');

    // Placeholder for AI API call
    // In production, replace with actual API call:
    // const response = await fetch('your-api/improve', {
    //   method: 'POST',
    //   body: JSON.stringify({ prompt: inputPrompt }),
    // });
    // const data = await response.json();
    // setImprovedPrompt(data.improvedPrompt);

    // Simulate API delay and response
    setTimeout(() => {
      const mockImproved = `Here is an improved version of your prompt:

---

${inputPrompt}

---

Enhanced with:
- Clear context and constraints
- Specific output format requirements
- Step-by-step instructions
- Expected tone and style guidance

Note: This is a placeholder. Connect your AI API (OpenAI, Claude) to get real improvements.`;

      setImprovedPrompt(mockImproved);
      setLoading(false);
    }, 1500);
  };

  const handleCopy = async () => {
    await Clipboard.setStringAsync(improvedPrompt);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setToastVisible(true);
  };

  const handleClear = () => {
    setInputPrompt('');
    setImprovedPrompt('');
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <Toast
        visible={toastVisible}
        message="Copied to clipboard"
        type="success"
        onHide={() => setToastVisible(false)}
      />

      <Paywall
        visible={paywallVisible}
        onClose={() => setPaywallVisible(false)}
        feature="Prompt Improver"
      />

      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.header}>
            <Text style={styles.title}>Prompt Improver</Text>
            <Text style={styles.subtitle}>
              Paste your prompt and get an enhanced version
            </Text>
            {!isPro && (
              <View style={styles.proBadge}>
                <MaterialCommunityIcons
                  name="star-circle"
                  size={14}
                  color={colors.primary}
                />
                <Text style={styles.proText}>Premium Feature</Text>
              </View>
            )}
          </View>

          <View style={styles.inputSection}>
            <View style={styles.labelRow}>
              <Text style={styles.label}>Your Prompt</Text>
              {inputPrompt.length > 0 && (
                <TouchableOpacity onPress={handleClear}>
                  <Text style={styles.clearText}>Clear</Text>
                </TouchableOpacity>
              )}
            </View>
            <TextInput
              style={styles.input}
              value={inputPrompt}
              onChangeText={setInputPrompt}
              placeholder="Paste your prompt here..."
              placeholderTextColor={colors.textMuted}
              multiline
              textAlignVertical="top"
            />
          </View>

          <TouchableOpacity
            style={[
              styles.improveButton,
              (!inputPrompt.trim() || loading) && styles.buttonDisabled,
            ]}
            onPress={handleImprove}
            disabled={!inputPrompt.trim() || loading}
          >
            {loading ? (
              <ActivityIndicator color={colors.background} />
            ) : (
              <>
                <MaterialCommunityIcons
                  name="magic-staff"
                  size={22}
                  color={colors.background}
                />
                <Text style={styles.improveButtonText}>Improve Prompt</Text>
              </>
            )}
          </TouchableOpacity>

          {improvedPrompt && (
            <View style={styles.resultSection}>
              <View style={styles.labelRow}>
                <Text style={styles.label}>Improved Prompt</Text>
                <TouchableOpacity onPress={handleCopy}>
                  <Text style={styles.copyText}>Copy</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.resultBox}>
                <Text style={styles.resultText}>{improvedPrompt}</Text>
              </View>
            </View>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  keyboardView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
  },
  header: {
    marginBottom: spacing.lg,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
  },
  subtitle: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  proBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    backgroundColor: colors.primary + '20',
    alignSelf: 'flex-start',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
    marginTop: spacing.sm,
  },
  proText: {
    fontSize: fontSize.xs,
    fontWeight: '600',
    color: colors.primary,
  },
  inputSection: {
    marginBottom: spacing.md,
  },
  labelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  label: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  clearText: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },
  copyText: {
    fontSize: fontSize.sm,
    color: colors.primary,
    fontWeight: '600',
  },
  input: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    fontSize: fontSize.md,
    color: colors.text,
    minHeight: 150,
  },
  improveButton: {
    flexDirection: 'row',
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  improveButtonText: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.background,
  },
  resultSection: {
    marginTop: spacing.md,
  },
  resultBox: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    borderLeftWidth: 3,
    borderLeftColor: colors.success,
  },
  resultText: {
    fontSize: fontSize.md,
    color: colors.text,
    lineHeight: 24,
  },
});
