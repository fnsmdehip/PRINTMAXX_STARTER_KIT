import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { router } from 'expo-router';
import { COLORS, SPACING, TYPOGRAPHY } from '../src/utils/constants';

const APP_NAME = 'LearnLock';

const PRIVACY_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Information we collect',
      content: `${APP_NAME} collects minimal data to provide our service:

- Study session timing and completion data
- Blocked app selections
- Streak and progress information
- App preferences and settings

All data is stored locally on your device. We do not collect personal information.`,
    },
    {
      title: 'How we use your data',
      content: `Your data is used solely to:

- Track your study sessions
- Manage app blocking functionality
- Calculate and display streaks
- Remember your timer preferences

We never sell your data to third parties.`,
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
      title: 'Data retention',
      content: `Your data remains on your device until you:

- Delete the app
- Clear app data
- Request data deletion`,
    },
    {
      title: 'Your rights',
      content: `You can:

- Export your study statistics
- Request data deletion
- Opt out of analytics

Contact support@learnlock.app for data requests.`,
    },
    {
      title: 'Contact us',
      content: `For privacy questions:

Email: support@learnlock.app

We respond within 48 hours.`,
    },
  ],
};

export default function PrivacyPolicyScreen() {
  const handleBack = () => {
    if (router.canGoBack()) {
      router.back();
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleBack} style={styles.backButton}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
      </View>
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
    backgroundColor: COLORS.background,
  },
  header: {
    padding: SPACING.lg,
    paddingBottom: 0,
  },
  backButton: {
    alignSelf: 'flex-start',
  },
  backText: {
    ...TYPOGRAPHY.body,
    color: COLORS.primary,
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
