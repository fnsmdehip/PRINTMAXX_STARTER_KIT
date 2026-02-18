import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, spacing, typography } from '@/constants/theme';

export default function PrivacyScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.lastUpdated}>Last Updated: January 2025</Text>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>1. Information We Collect</Text>
          <Text style={styles.paragraph}>
            DevotionFlow collects minimal information to provide our service:
          </Text>
          <Text style={styles.bulletPoint}>
            - Usage data (devotionals read, streaks, app interactions)
          </Text>
          <Text style={styles.bulletPoint}>
            - Prayer journal entries (stored locally on your device)
          </Text>
          <Text style={styles.bulletPoint}>
            - Notification preferences
          </Text>
          <Text style={styles.bulletPoint}>
            - Subscription information (processed by Apple/Google)
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>2. How We Use Your Information</Text>
          <Text style={styles.paragraph}>
            We use your information to:
          </Text>
          <Text style={styles.bulletPoint}>
            - Provide and improve our devotional service
          </Text>
          <Text style={styles.bulletPoint}>
            - Track your reading streak and progress
          </Text>
          <Text style={styles.bulletPoint}>
            - Send daily devotional reminders (with your permission)
          </Text>
          <Text style={styles.bulletPoint}>
            - Process subscription payments
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>3. Data Storage</Text>
          <Text style={styles.paragraph}>
            Your prayer journal entries and personal reflections are stored locally on your device.
            We do not have access to this content. Subscription data is managed by Apple App Store
            or Google Play Store.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>4. Third-Party Services</Text>
          <Text style={styles.paragraph}>
            We use the following third-party services:
          </Text>
          <Text style={styles.bulletPoint}>
            - RevenueCat (subscription management)
          </Text>
          <Text style={styles.bulletPoint}>
            - Apple/Google (payment processing)
          </Text>
          <Text style={styles.bulletPoint}>
            - Expo (app framework and updates)
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>5. Your Rights</Text>
          <Text style={styles.paragraph}>
            You have the right to:
          </Text>
          <Text style={styles.bulletPoint}>
            - Access your data stored on our servers
          </Text>
          <Text style={styles.bulletPoint}>
            - Request deletion of your account
          </Text>
          <Text style={styles.bulletPoint}>
            - Opt out of notifications at any time
          </Text>
          <Text style={styles.bulletPoint}>
            - Export your prayer journal (device-only feature)
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>6. Children's Privacy</Text>
          <Text style={styles.paragraph}>
            DevotionFlow is intended for users 13 years and older. We do not knowingly collect
            information from children under 13.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>7. Changes to This Policy</Text>
          <Text style={styles.paragraph}>
            We may update this privacy policy from time to time. We will notify you of any
            changes by posting the new policy on this page and updating the "Last Updated" date.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>8. Contact Us</Text>
          <Text style={styles.paragraph}>
            If you have questions about this privacy policy, please contact us at:
          </Text>
          <Text style={styles.email}>support@devotionflow.app</Text>
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
    marginBottom: spacing.lg,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  paragraph: {
    ...typography.body,
    color: colors.textLight,
    lineHeight: 24,
    marginBottom: spacing.sm,
  },
  bulletPoint: {
    ...typography.body,
    color: colors.textLight,
    lineHeight: 24,
    marginLeft: spacing.md,
    marginBottom: spacing.xs,
  },
  email: {
    ...typography.body,
    color: colors.primary,
    marginTop: spacing.sm,
  },
});
