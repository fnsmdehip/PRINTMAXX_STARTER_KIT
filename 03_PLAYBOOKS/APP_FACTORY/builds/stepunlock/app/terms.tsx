import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { COLORS, APP_NAME, MONTHLY_PRICE, ANNUAL_PRICE } from '../src/utils/constants';

const TERMS_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Acceptance of terms',
      content: `By downloading, installing, or using ${APP_NAME}, you agree to these Terms of Service. If you do not agree, do not use the app.`,
    },
    {
      title: 'Description of service',
      content: `${APP_NAME} is a productivity app that blocks access to selected apps until you reach your daily step goal. The service includes:

- Step tracking integration
- App blocking functionality
- Progress tracking and streaks
- Premium features via subscription`,
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
      content: `Refunds are handled by Apple or Google according to their respective policies. We cannot process refunds directly.

For billing issues, contact Apple Support or Google Play Support.`,
    },
    {
      title: 'User responsibilities',
      content: `You agree to:

- Use the app for its intended purpose
- Not attempt to bypass app blocking mechanisms
- Not reverse engineer or modify the app
- Not use the app for illegal purposes`,
    },
    {
      title: 'Health disclaimer',
      content: `${APP_NAME} is not a medical device. Step tracking is for informational purposes only.

Consult a healthcare provider before starting any exercise program. We are not responsible for injuries that may occur while trying to reach step goals.`,
    },
    {
      title: 'Limitation of liability',
      content: `${APP_NAME} is provided "as is" without warranties of any kind.

We are not liable for:
- Loss of data
- Missed notifications or reminders
- App blocking malfunctions
- Device compatibility issues

Maximum liability is limited to the amount paid for the service.`,
    },
    {
      title: 'Changes to terms',
      content: `We may update these terms at any time. Continued use of the app after changes constitutes acceptance of the new terms.

Material changes will be communicated via app notification or email.`,
    },
    {
      title: 'Termination',
      content: `We may terminate or suspend your access to the service at any time for violation of these terms, without prior notice.

You may stop using the service at any time by deleting the app.`,
    },
    {
      title: 'Governing law',
      content: `These terms are governed by the laws of the State of Delaware, United States.

Any disputes will be resolved in the courts of Delaware.`,
    },
    {
      title: 'Contact',
      content: `For questions about these terms:

Email: legal@stepunlock.app

We respond within 5 business days.`,
    },
  ],
};

export default function TermsScreen() {
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
    borderTopColor: COLORS.border,
  },
  footerText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
