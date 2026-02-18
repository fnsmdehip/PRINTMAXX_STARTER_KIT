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
const MONTHLY_PRICE = '$7.99';
const ANNUAL_PRICE = '$49.99';

const TERMS_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Acceptance of terms',
      content: `By downloading, installing, or using ${APP_NAME}, you agree to these Terms of Service. If you do not agree, do not use the app.`,
    },
    {
      title: 'Description of service',
      content: `${APP_NAME} is an AI prompt library app that helps you discover, save, and improve prompts. The service includes:

- Curated prompt library
- Favorites and collections
- AI prompt improvement (premium)
- Custom prompt creation`,
    },
    {
      title: 'Subscription terms',
      content: `Premium access requires a subscription:

- Monthly: ${MONTHLY_PRICE}/month
- Annual: ${ANNUAL_PRICE}/year

Subscriptions automatically renew unless cancelled at least 24 hours before the end of the current period.

Payment is charged to your Apple ID or Google Play account at confirmation of purchase.

Manage or cancel subscriptions in your device settings.`,
    },
    {
      title: 'Free trial',
      content: `New users receive a 7-day free trial of premium features. If you do not cancel before the trial ends, your subscription will begin and you will be charged.`,
    },
    {
      title: 'Refund policy',
      content: `Refunds are handled by Apple or Google according to their respective policies. We cannot process refunds directly.`,
    },
    {
      title: 'User content',
      content: `You retain ownership of any custom prompts you create. By using the app, you grant us a license to store and display your content within the app.

You are responsible for the content you create. Do not create prompts that are illegal, harmful, or violate others' rights.`,
    },
    {
      title: 'AI features disclaimer',
      content: `AI-powered features use third-party AI services. Results may vary and are not guaranteed.

We are not responsible for AI-generated content. Always review AI suggestions before use.`,
    },
    {
      title: 'Intellectual property',
      content: `The curated prompt library is owned by ${APP_NAME}. You may use prompts for personal or commercial purposes but may not redistribute the library.`,
    },
    {
      title: 'Limitation of liability',
      content: `${APP_NAME} is provided "as is" without warranties of any kind.

We are not liable for:
- Results from using prompts
- AI-generated content
- Loss of data

Maximum liability is limited to the amount paid for the service.`,
    },
    {
      title: 'Changes to terms',
      content: `We may update these terms at any time. Continued use of the app after changes constitutes acceptance of the new terms.`,
    },
    {
      title: 'Governing law',
      content: `These terms are governed by the laws of the State of Delaware, United States.`,
    },
    {
      title: 'Contact',
      content: `For questions about these terms:

Email: legal@promptvault.app`,
    },
  ],
};

export default function TermsScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Terms of service</Text>
        <Text style={styles.lastUpdated}>
          Last updated: {TERMS_CONTENT.lastUpdated}
        </Text>

        {TERMS_CONTENT.sections.map((section, index) => (
          <View key={index} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            <Text style={styles.sectionContent}>{section.content}</Text>
          </View>
        ))}

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            By using {APP_NAME}, you agree to these terms.
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
