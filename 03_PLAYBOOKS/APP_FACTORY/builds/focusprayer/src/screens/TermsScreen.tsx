import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { COLORS, MONTHLY_PRICE, ANNUAL_PRICE } from '../utils/constants';

const APP_NAME = 'PrayerLock';

const TERMS_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Acceptance of terms',
      content: `By downloading, installing, or using ${APP_NAME}, you agree to these Terms of Service. If you do not agree, do not use the app.`,
    },
    {
      title: 'Description of service',
      content: `${APP_NAME} is a faith-based productivity app that blocks access to selected apps until you complete your daily devotion. The service includes:

- Prayer timer functionality
- Scripture reading integration
- App blocking
- Progress tracking`,
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
      content: `New users receive a 3-day free trial of premium features. If you do not cancel before the trial ends, your subscription will begin and you will be charged.`,
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
      title: 'Religious content disclaimer',
      content: `${APP_NAME} provides Christian devotional content for spiritual encouragement. This is not a substitute for professional counseling or medical advice.

Bible verses are sourced from public domain translations.`,
    },
    {
      title: 'Limitation of liability',
      content: `${APP_NAME} is provided "as is" without warranties of any kind.

We are not liable for:
- Loss of data
- Missed notifications
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

Email: legal@prayerlock.app`,
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
    padding: 20,
    paddingBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  lastUpdated: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 24,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  sectionContent: {
    fontSize: 15,
    color: COLORS.textSecondary,
    lineHeight: 22,
  },
  footer: {
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: COLORS.disabled,
  },
  footerText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
