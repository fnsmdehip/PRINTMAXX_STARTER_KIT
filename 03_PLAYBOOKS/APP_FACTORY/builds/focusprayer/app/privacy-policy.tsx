/**
 * Privacy Policy Screen
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { COLORS } from '@/utils/constants';

export default function PrivacyPolicyScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>&#8592; Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Privacy Policy</Text>
      </View>

      <ScrollView style={styles.content}>
        <Text style={styles.lastUpdated}>Last updated: January 2025</Text>

        <Text style={styles.sectionTitle}>Introduction</Text>
        <Text style={styles.paragraph}>
          FocusPrayer ("we", "our", or "us") respects your privacy and is committed to
          protecting your personal data. This privacy policy explains how we collect,
          use, and safeguard your information when you use our mobile application.
        </Text>

        <Text style={styles.sectionTitle}>Information We Collect</Text>
        <Text style={styles.paragraph}>
          We collect minimal information necessary to provide our services:
        </Text>
        <Text style={styles.listItem}>
          • Device preferences and settings (stored locally on your device)
        </Text>
        <Text style={styles.listItem}>
          • Streak and devotion completion data (stored locally on your device)
        </Text>
        <Text style={styles.listItem}>
          • Subscription status (managed through Apple App Store / Google Play)
        </Text>

        <Text style={styles.sectionTitle}>How We Use Your Information</Text>
        <Text style={styles.paragraph}>
          Your data is used to:
        </Text>
        <Text style={styles.listItem}>
          • Provide and maintain the app functionality
        </Text>
        <Text style={styles.listItem}>
          • Track your prayer streaks and devotion progress
        </Text>
        <Text style={styles.listItem}>
          • Manage your subscription status
        </Text>

        <Text style={styles.sectionTitle}>Data Storage</Text>
        <Text style={styles.paragraph}>
          All your personal data (settings, streaks, devotion history) is stored
          locally on your device. We do not transmit this data to any external servers.
          Your subscription information is managed securely through Apple or Google's
          payment infrastructure.
        </Text>

        <Text style={styles.sectionTitle}>Third-Party Services</Text>
        <Text style={styles.paragraph}>
          We use the following third-party services:
        </Text>
        <Text style={styles.listItem}>
          • RevenueCat for subscription management
        </Text>
        <Text style={styles.listItem}>
          • Bible API for daily scripture passages
        </Text>
        <Text style={styles.listItem}>
          • Apple/Google for app distribution and payments
        </Text>

        <Text style={styles.sectionTitle}>Your Rights</Text>
        <Text style={styles.paragraph}>
          You have the right to:
        </Text>
        <Text style={styles.listItem}>
          • Access your data stored in the app
        </Text>
        <Text style={styles.listItem}>
          • Delete your data by uninstalling the app
        </Text>
        <Text style={styles.listItem}>
          • Opt-out of notifications through device settings
        </Text>

        <Text style={styles.sectionTitle}>Children's Privacy</Text>
        <Text style={styles.paragraph}>
          Our app is not intended for children under 13. We do not knowingly collect
          personal information from children under 13.
        </Text>

        <Text style={styles.sectionTitle}>Changes to This Policy</Text>
        <Text style={styles.paragraph}>
          We may update this privacy policy from time to time. We will notify you of
          any changes by posting the new policy in the app.
        </Text>

        <Text style={styles.sectionTitle}>Contact Us</Text>
        <Text style={styles.paragraph}>
          If you have questions about this privacy policy, please contact us at:
          support@printmaxx.com
        </Text>

        <View style={styles.spacer} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    backgroundColor: COLORS.surface,
    paddingTop: 20,
    paddingBottom: 16,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.background,
  },
  backButton: {
    color: COLORS.primary,
    fontSize: 16,
    marginBottom: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  lastUpdated: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 20,
    marginBottom: 12,
  },
  paragraph: {
    fontSize: 15,
    color: COLORS.textSecondary,
    lineHeight: 22,
    marginBottom: 12,
  },
  listItem: {
    fontSize: 15,
    color: COLORS.textSecondary,
    lineHeight: 22,
    marginLeft: 8,
    marginBottom: 6,
  },
  spacer: {
    height: 40,
  },
});
