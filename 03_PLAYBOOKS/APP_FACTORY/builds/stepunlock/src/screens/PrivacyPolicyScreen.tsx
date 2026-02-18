import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { COLORS, APP_NAME } from '../utils/constants';

interface Props {
  navigation?: any;
}

const PRIVACY_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Information we collect',
      content: `${APP_NAME} collects minimal data to provide our service:

- Step count data from Apple HealthKit or Google Fit
- App usage preferences and settings
- Blocked app selections
- Streak and progress data

All data is stored locally on your device. We do not collect personal information like your name, email, or location unless you contact support.`,
    },
    {
      title: 'How we use your data',
      content: `Your data is used solely to:

- Track your daily step progress
- Manage app blocking functionality
- Calculate and display your streaks
- Sync settings across app sessions

We never sell your data to third parties.`,
    },
    {
      title: 'Health data',
      content: `Step data accessed through HealthKit or Google Fit is:

- Only read with your explicit permission
- Never shared with third parties
- Never used for advertising
- Stored only on your device`,
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
- Request data deletion

We retain minimal anonymized analytics for 2 years.`,
    },
    {
      title: 'Your rights',
      content: `You can:

- Request a copy of your data
- Request data deletion
- Opt out of analytics
- Revoke health data access

Contact support@walktounlock.app for data requests.`,
    },
    {
      title: 'Contact us',
      content: `For privacy questions:

Email: support@walktounlock.app

We respond within 48 hours.`,
    },
  ],
};

export function PrivacyPolicyScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.container}>
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
