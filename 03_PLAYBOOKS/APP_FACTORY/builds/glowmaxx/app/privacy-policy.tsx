import React from 'react';
import { ScrollView, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../src/utils/constants';

export default function PrivacyPolicyScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.content}>
        <Text style={styles.title}>Privacy Policy</Text>
        <Text style={styles.updated}>Last updated: January 2026</Text>

        <Text style={styles.heading}>1. Information We Collect</Text>
        <Text style={styles.body}>
          GlowMaxx collects the following information to provide our services:
          {'\n\n'}
          - Profile information (gender, age preferences)
          {'\n'}- Usage data (routines completed, progress tracked)
          {'\n'}- Photos you choose to save (stored locally on your device)
          {'\n'}- Subscription status
        </Text>

        <Text style={styles.heading}>2. How We Use Your Information</Text>
        <Text style={styles.body}>
          We use your information to:
          {'\n\n'}
          - Personalize your experience with gender-specific routines
          {'\n'}- Track your progress and streaks
          {'\n'}- Send notifications and reminders (if enabled)
          {'\n'}- Process subscriptions through RevenueCat
          {'\n'}- Improve our app and services
        </Text>

        <Text style={styles.heading}>3. Data Storage</Text>
        <Text style={styles.body}>
          Your progress photos and daily logs are stored locally on your device. We do not upload
          your photos to our servers. Subscription data is processed securely through RevenueCat
          and Apple/Google payment systems.
        </Text>

        <Text style={styles.heading}>4. Third-Party Services</Text>
        <Text style={styles.body}>
          We use the following third-party services:
          {'\n\n'}
          - RevenueCat for subscription management
          {'\n'}- Apple App Store / Google Play for payments
          {'\n'}- Expo for app notifications
        </Text>

        <Text style={styles.heading}>5. Your Rights</Text>
        <Text style={styles.body}>
          You have the right to:
          {'\n\n'}
          - Access your personal data
          {'\n'}- Delete your account and data
          {'\n'}- Opt out of notifications
          {'\n'}- Request data portability
          {'\n\n'}
          To exercise these rights, contact us at support@glowmaxx.app
        </Text>

        <Text style={styles.heading}>6. Data Security</Text>
        <Text style={styles.body}>
          We implement industry-standard security measures to protect your information.
          However, no method of transmission over the internet is 100% secure.
        </Text>

        <Text style={styles.heading}>7. Children's Privacy</Text>
        <Text style={styles.body}>
          GlowMaxx is not intended for users under 13 years of age. We do not knowingly
          collect information from children under 13.
        </Text>

        <Text style={styles.heading}>8. Changes to This Policy</Text>
        <Text style={styles.body}>
          We may update this privacy policy from time to time. We will notify you of any
          changes by posting the new policy in the app.
        </Text>

        <Text style={styles.heading}>9. Contact Us</Text>
        <Text style={styles.body}>
          If you have questions about this privacy policy, please contact us at:
          {'\n\n'}
          Email: support@glowmaxx.app
        </Text>
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
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  updated: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 24,
  },
  heading: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 20,
    marginBottom: 12,
  },
  body: {
    fontSize: 15,
    color: COLORS.textSecondary,
    lineHeight: 24,
  },
});
