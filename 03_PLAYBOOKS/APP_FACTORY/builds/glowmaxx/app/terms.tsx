import React from 'react';
import { ScrollView, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../src/utils/constants';

export default function TermsScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.content}>
        <Text style={styles.title}>Terms of Service</Text>
        <Text style={styles.updated}>Last updated: January 2026</Text>

        <Text style={styles.heading}>1. Acceptance of Terms</Text>
        <Text style={styles.body}>
          By downloading, installing, or using GlowMaxx, you agree to be bound by these Terms
          of Service. If you do not agree to these terms, do not use the app.
        </Text>

        <Text style={styles.heading}>2. Description of Service</Text>
        <Text style={styles.body}>
          GlowMaxx is a mobile application that provides facial exercise routines, skincare
          guidance, progress tracking, and educational content related to facial optimization
          and self-improvement.
        </Text>

        <Text style={styles.heading}>3. Medical Disclaimer</Text>
        <Text style={styles.body}>
          GlowMaxx is for informational and educational purposes only. It is NOT a substitute
          for professional medical advice, diagnosis, or treatment.
          {'\n\n'}
          The exercises and techniques provided (including mewing, facial exercises, and
          skincare routines) have not been evaluated by medical authorities. Results may vary.
          {'\n\n'}
          Always consult with a healthcare provider before starting any new health routine,
          especially if you have existing medical conditions.
        </Text>

        <Text style={styles.heading}>4. Subscription Terms</Text>
        <Text style={styles.body}>
          GlowMaxx offers subscription-based access to premium features:
          {'\n\n'}
          - Free Trial: 7 days, automatically converts to paid subscription
          {'\n'}- Monthly: $9.99/month
          {'\n'}- Annual: $49.99/year
          {'\n\n'}
          Subscriptions automatically renew unless cancelled at least 24 hours before the
          end of the current period. You can manage your subscription in your App Store or
          Google Play account settings.
        </Text>

        <Text style={styles.heading}>5. User Responsibilities</Text>
        <Text style={styles.body}>
          You agree to:
          {'\n\n'}
          - Provide accurate information
          {'\n'}- Use the app responsibly and at your own risk
          {'\n'}- Not share your account with others
          {'\n'}- Not use the app for any illegal purpose
        </Text>

        <Text style={styles.heading}>6. Content and Intellectual Property</Text>
        <Text style={styles.body}>
          All content in GlowMaxx, including text, graphics, and software, is owned by
          GlowMaxx or its licensors. You may not copy, modify, or distribute our content
          without permission.
        </Text>

        <Text style={styles.heading}>7. Limitation of Liability</Text>
        <Text style={styles.body}>
          GlowMaxx is provided "as is" without warranties of any kind. We are not liable
          for any damages arising from your use of the app, including but not limited to:
          {'\n\n'}
          - Physical injury from exercises
          {'\n'}- Skin reactions to skincare routines
          {'\n'}- Failure to achieve desired results
          {'\n'}- Data loss
        </Text>

        <Text style={styles.heading}>8. Termination</Text>
        <Text style={styles.body}>
          We reserve the right to terminate or suspend your account at any time for
          violation of these terms or for any other reason at our discretion.
        </Text>

        <Text style={styles.heading}>9. Changes to Terms</Text>
        <Text style={styles.body}>
          We may update these terms from time to time. Continued use of the app after
          changes constitutes acceptance of the new terms.
        </Text>

        <Text style={styles.heading}>10. Governing Law</Text>
        <Text style={styles.body}>
          These terms are governed by the laws of the United States. Any disputes shall
          be resolved in the courts of that jurisdiction.
        </Text>

        <Text style={styles.heading}>11. Contact</Text>
        <Text style={styles.body}>
          For questions about these terms, contact us at:
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
