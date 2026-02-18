/**
 * Terms of Service Screen
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

export default function TermsScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>&#8592; Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Terms of Service</Text>
      </View>

      <ScrollView style={styles.content}>
        <Text style={styles.lastUpdated}>Last updated: January 2025</Text>

        <Text style={styles.sectionTitle}>1. Acceptance of Terms</Text>
        <Text style={styles.paragraph}>
          By downloading, installing, or using FocusPrayer, you agree to be bound
          by these Terms of Service. If you do not agree to these terms, please
          do not use the app.
        </Text>

        <Text style={styles.sectionTitle}>2. Description of Service</Text>
        <Text style={styles.paragraph}>
          FocusPrayer is a mobile application designed to help users establish
          consistent prayer and scripture reading habits by blocking distracting
          apps until a daily devotion is completed.
        </Text>

        <Text style={styles.sectionTitle}>3. User Accounts</Text>
        <Text style={styles.paragraph}>
          FocusPrayer does not require account creation. Your data is stored
          locally on your device and through your Apple ID or Google account
          for subscription management.
        </Text>

        <Text style={styles.sectionTitle}>4. Subscription Terms</Text>
        <Text style={styles.paragraph}>
          FocusPrayer offers the following subscription options:
        </Text>
        <Text style={styles.listItem}>
          • Monthly subscription at $9.99/month
        </Text>
        <Text style={styles.listItem}>
          • Annual subscription at $49.99/year
        </Text>
        <Text style={styles.listItem}>
          • 3-day free trial for new users
        </Text>
        <Text style={styles.paragraph}>
          Subscriptions automatically renew unless canceled at least 24 hours
          before the end of the current period. You can manage subscriptions
          in your App Store or Google Play account settings.
        </Text>

        <Text style={styles.sectionTitle}>5. App Blocking Feature</Text>
        <Text style={styles.paragraph}>
          The app blocking feature requires device permissions to function.
          FocusPrayer uses Screen Time API (iOS) or Usage Stats API (Android)
          solely for the purpose of blocking selected apps. We do not collect
          or transmit usage data.
        </Text>

        <Text style={styles.sectionTitle}>6. Emergency Unlock</Text>
        <Text style={styles.paragraph}>
          The emergency unlock feature allows users to bypass app blocking in
          genuine emergencies. Using this feature resets your streak and is
          logged locally. We encourage users to complete their devotion when
          possible.
        </Text>

        <Text style={styles.sectionTitle}>7. Intellectual Property</Text>
        <Text style={styles.paragraph}>
          All content, features, and functionality of FocusPrayer are owned
          by us and are protected by copyright, trademark, and other intellectual
          property laws. Scripture passages are provided through public Bible APIs.
        </Text>

        <Text style={styles.sectionTitle}>8. Limitation of Liability</Text>
        <Text style={styles.paragraph}>
          FocusPrayer is provided "as is" without warranties of any kind. We are
          not liable for any damages arising from the use or inability to use the
          app, including but not limited to missed appointments or emergencies
          due to app blocking.
        </Text>

        <Text style={styles.sectionTitle}>9. Modifications</Text>
        <Text style={styles.paragraph}>
          We reserve the right to modify these terms at any time. Continued use
          of the app after changes constitutes acceptance of the new terms.
        </Text>

        <Text style={styles.sectionTitle}>10. Termination</Text>
        <Text style={styles.paragraph}>
          We may terminate or suspend your access to the app at any time, without
          prior notice, for conduct that we believe violates these terms or is
          harmful to other users, us, or third parties.
        </Text>

        <Text style={styles.sectionTitle}>11. Governing Law</Text>
        <Text style={styles.paragraph}>
          These terms shall be governed by and construed in accordance with the
          laws of the United States, without regard to conflict of law principles.
        </Text>

        <Text style={styles.sectionTitle}>12. Contact</Text>
        <Text style={styles.paragraph}>
          For questions about these Terms of Service, please contact us at:
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
