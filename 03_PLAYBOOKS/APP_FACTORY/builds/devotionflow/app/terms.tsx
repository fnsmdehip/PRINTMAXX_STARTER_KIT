import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, spacing, typography } from '@/constants/theme';

export default function TermsScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.lastUpdated}>Last Updated: January 2025</Text>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>1. Acceptance of Terms</Text>
          <Text style={styles.paragraph}>
            By downloading, installing, or using DevotionFlow, you agree to be bound by these
            Terms of Service. If you do not agree to these terms, please do not use the app.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>2. Description of Service</Text>
          <Text style={styles.paragraph}>
            DevotionFlow provides daily Christian devotionals, Bible verses, prayer journaling,
            and streak tracking features. Content is provided for spiritual growth and personal
            reflection purposes.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>3. Subscription and Payments</Text>
          <Text style={styles.paragraph}>
            DevotionFlow offers subscription plans through the Apple App Store and Google Play Store.
            By subscribing, you agree to:
          </Text>
          <Text style={styles.bulletPoint}>
            - Pay the subscription fee at the frequency selected
          </Text>
          <Text style={styles.bulletPoint}>
            - Automatic renewal unless cancelled at least 24 hours before the end of the current period
          </Text>
          <Text style={styles.bulletPoint}>
            - Manage subscriptions through your App Store or Play Store account
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>4. Free Trial</Text>
          <Text style={styles.paragraph}>
            If eligible, you may be offered a free trial. The trial provides full access to premium
            features. If you do not cancel before the trial ends, you will be charged for the
            subscription.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>5. User Content</Text>
          <Text style={styles.paragraph}>
            You retain ownership of any content you create (prayer journal entries, reflections).
            This content is stored locally on your device. We do not access, share, or sell your
            personal content.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>6. Intellectual Property</Text>
          <Text style={styles.paragraph}>
            All devotional content, app design, and branding are owned by DevotionFlow. Bible
            verses are in the public domain or used under appropriate licenses. You may not
            reproduce, distribute, or create derivative works without permission.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>7. Disclaimer</Text>
          <Text style={styles.paragraph}>
            DevotionFlow is provided for spiritual growth and personal reflection. It is not a
            substitute for professional counseling, therapy, or medical advice. If you are
            experiencing a crisis, please contact a qualified professional or emergency services.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>8. Limitation of Liability</Text>
          <Text style={styles.paragraph}>
            DevotionFlow is provided "as is" without warranties of any kind. We are not liable
            for any damages arising from your use of the app, including but not limited to
            direct, indirect, incidental, or consequential damages.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>9. Changes to Terms</Text>
          <Text style={styles.paragraph}>
            We reserve the right to modify these terms at any time. Continued use of the app
            after changes constitutes acceptance of the new terms.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>10. Termination</Text>
          <Text style={styles.paragraph}>
            We may terminate or suspend your access to DevotionFlow at any time, without prior
            notice, for conduct that violates these terms or is harmful to other users or the
            service.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>11. Governing Law</Text>
          <Text style={styles.paragraph}>
            These terms are governed by and construed in accordance with the laws of the United
            States, without regard to conflict of law principles.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>12. Contact</Text>
          <Text style={styles.paragraph}>
            For questions about these terms, please contact us at:
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
