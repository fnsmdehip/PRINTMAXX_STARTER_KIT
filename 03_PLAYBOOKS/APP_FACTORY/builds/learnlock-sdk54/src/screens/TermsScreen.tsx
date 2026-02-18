import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY, PRICING } from '../utils/constants';

const APP_NAME = 'StudyLock';

const TERMS_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Acceptance of terms',
      content: `By downloading, installing, or using ${APP_NAME}, you agree to these Terms of Service. If you do not agree, do not use the app.`,
    },
    {
      title: 'Description of service',
      content: `${APP_NAME} is a productivity app that helps you focus by blocking distracting apps during study sessions. The service includes:

- Pomodoro-style timer
- App blocking during focus sessions
- Progress and streak tracking
- Premium features via subscription`,
    },
    {
      title: 'Subscription terms',
      content: `Premium access requires a subscription:

- Monthly: $${PRICING.monthly.price}/month
- Annual: $${PRICING.annual.price}/year
- Lifetime: $${PRICING.lifetime.price} one-time

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
      title: 'User responsibilities',
      content: `You agree to:

- Use the app for its intended purpose
- Not attempt to bypass app blocking mechanisms
- Not reverse engineer or modify the app`,
    },
    {
      title: 'Educational disclaimer',
      content: `${APP_NAME} is a productivity tool and is not responsible for your academic performance. The app helps manage distractions but success depends on your effort and study habits.`,
    },
    {
      title: 'Limitation of liability',
      content: `${APP_NAME} is provided "as is" without warranties of any kind.

We are not liable for:
- Loss of data
- Missed timers or notifications
- App blocking malfunctions
- Device compatibility issues

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

Email: legal@studylock.app`,
    },
  ],
};

export function TermsScreen() {
  return (
    <SafeAreaView style={styles.container}>
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
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  title: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  lastUpdated: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xl,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  sectionContent: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    lineHeight: 22,
  },
  footer: {
    marginTop: SPACING.lg,
    paddingTop: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  footerText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
