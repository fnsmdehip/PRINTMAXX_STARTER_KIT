import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Stack } from 'expo-router';
import {
  colors,
  spacing,
  borderRadius,
  typography,
} from '@/constants/theme';

const APP_NAME = 'FemFit';

const PRIVACY_CONTENT = {
  lastUpdated: 'January 21, 2026',
  sections: [
    {
      title: 'Information we collect',
      content: `${APP_NAME} collects minimal data to provide our service:

- Exercise completion data and progress
- Workout history and statistics
- App preferences and settings

All data is stored locally on your device. We do not collect personal health information beyond what you voluntarily track.`,
    },
    {
      title: 'How we use your data',
      content: `Your data is used solely to:

- Track your workout progress
- Calculate and display statistics
- Personalize your exercise experience

We never sell your data to third parties.`,
    },
    {
      title: 'Health information',
      content: `${APP_NAME} is a general fitness app. While it includes pelvic floor exercises, it is not a medical device and does not diagnose or treat any condition.

Exercise data is stored locally and never shared without your consent.`,
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

- Export your workout data
- Delete your progress at any time
- Opt out of analytics

Contact support@femfit.app for data requests.`,
    },
    {
      title: 'Contact us',
      content: `For privacy questions:

Email: support@femfit.app

We respond within 48 hours.`,
    },
  ],
};

export default function PrivacyScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <Stack.Screen
        options={{
          title: 'Privacy Policy',
          headerTitleStyle: { color: colors.text },
        }}
      />

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
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
  lastUpdated: {
    ...typography.caption,
    color: colors.textMuted,
    marginBottom: spacing.xl,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  sectionContent: {
    ...typography.body,
    color: colors.textLight,
    lineHeight: 22,
  },
  footer: {
    marginTop: spacing.lg,
    paddingTop: spacing.lg,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  footerText: {
    ...typography.caption,
    color: colors.textMuted,
    textAlign: 'center',
  },
});
