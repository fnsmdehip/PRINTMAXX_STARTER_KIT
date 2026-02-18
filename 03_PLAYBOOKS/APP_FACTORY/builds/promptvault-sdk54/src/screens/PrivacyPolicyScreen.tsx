import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, spacing, fontSize, borderRadius } from '../utils/theme';

const APP_NAME = 'PromptVault';

const PRIVACY_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Information we collect',
      content: `${APP_NAME} collects minimal data to provide our service:

- Favorite prompts and custom prompts you create
- App preferences and settings
- Usage patterns for improving the app

All data is stored locally on your device. We do not collect personal information.`,
    },
    {
      title: 'How we use your data',
      content: `Your data is used solely to:

- Save your favorite prompts
- Store custom prompts you create
- Remember your preferences

We never sell your data to third parties.`,
    },
    {
      title: 'AI features',
      content: `When you use AI improvement features:

- Your prompts are sent to AI providers for processing
- We do not store the content of your prompts on our servers
- AI providers have their own privacy policies

You can use the app without AI features if preferred.`,
    },
    {
      title: 'Subscription data',
      content: `If you subscribe, payment is processed by Apple or Google. We receive:

- Subscription status (active/expired)
- Subscription type (monthly/annual)
- Anonymous transaction identifiers

We never see your payment details.`,
    },
    {
      title: 'Analytics',
      content: `We collect anonymous usage analytics to improve the app:

- Screen views
- Feature usage
- Crash reports

This data cannot identify you personally.`,
    },
    {
      title: 'Your rights',
      content: `You can:

- Export your prompts and favorites
- Delete all your data by uninstalling
- Opt out of analytics

Contact support@promptvault.app for data requests.`,
    },
    {
      title: 'Contact us',
      content: `For privacy questions:

Email: support@promptvault.app

We respond within 48 hours.`,
    },
  ],
};

export default function PrivacyPolicyScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Privacy policy</Text>
        <Text style={styles.lastUpdated}>
          Last updated: {PRIVACY_CONTENT.lastUpdated}
        </Text>

        {PRIVACY_CONTENT.sections.map((section, index) => (
          <View key={index} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            <Text style={styles.sectionContent}>{section.content}</Text>
          </View>
        ))}

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            By using {APP_NAME}, you agree to this privacy policy.
          </Text>
        </View>
      </ScrollView>
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
    paddingBottom: spacing.xxl,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.sm,
  },
  lastUpdated: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
    marginBottom: spacing.xl,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: fontSize.xl,
    fontWeight: '600',
    color: colors.text,
    marginBottom: spacing.sm,
  },
  sectionContent: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    lineHeight: 24,
  },
  footer: {
    marginTop: spacing.lg,
    paddingTop: spacing.lg,
    borderTopWidth: 1,
    borderTopColor: colors.surfaceLight,
  },
  footerText: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
    textAlign: 'center',
  },
});
