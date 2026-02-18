import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { router } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';

const features = [
  { icon: '🔒', title: 'Block distracting apps', description: 'Until devotional is complete' },
  { icon: '⏱️', title: 'Customizable prayer timer', description: '5-60 minute sessions' },
  { icon: '📖', title: 'Daily scripture reading', description: 'Fresh verses every day' },
  { icon: '🔥', title: 'Streak tracking', description: 'Stay motivated' },
  { icon: '📊', title: 'Progress statistics', description: 'See your growth' },
];

export default function Paywall() {
  const setIsSubscribed = useUserStore((state) => state.setIsSubscribed);
  const trialEndsAt = useUserStore((state) => state.trialEndsAt);

  const trialExpired = trialEndsAt ? Date.now() > trialEndsAt : true;

  const handleSubscribe = (plan: 'monthly' | 'annual') => {
    // In production, this would use RevenueCat
    // For now, simulate subscription
    setIsSubscribed(true);
    router.replace('/(tabs)');
  };

  const handleRestore = () => {
    // In production, restore purchases via RevenueCat
    console.log('Restore purchases');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>🙏</Text>
        <Text style={styles.title}>PrayerLock Pro</Text>
        <Text style={styles.subtitle}>
          {trialExpired
            ? 'Your trial has ended'
            : 'Unlock the full experience'}
        </Text>
      </View>

      <View style={styles.features}>
        {features.map((feature, index) => (
          <View key={index} style={styles.featureItem}>
            <Text style={styles.featureIcon}>{feature.icon}</Text>
            <View style={styles.featureText}>
              <Text style={styles.featureTitle}>{feature.title}</Text>
              <Text style={styles.featureDescription}>{feature.description}</Text>
            </View>
          </View>
        ))}
      </View>

      <View style={styles.plans}>
        <TouchableOpacity
          style={styles.planCard}
          onPress={() => handleSubscribe('annual')}
        >
          <View style={styles.popularBadge}>
            <Text style={styles.popularText}>BEST VALUE</Text>
          </View>
          <Text style={styles.planName}>Annual</Text>
          <Text style={styles.planPrice}>$49.99/year</Text>
          <Text style={styles.planSavings}>Save 58%</Text>
          <Text style={styles.planPer}>Just $4.17/month</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.planCard, styles.planCardSecondary]}
          onPress={() => handleSubscribe('monthly')}
        >
          <Text style={styles.planName}>Monthly</Text>
          <Text style={styles.planPrice}>$9.99/month</Text>
          <Text style={styles.planPer}>Cancel anytime</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.restoreButton} onPress={handleRestore}>
        <Text style={styles.restoreText}>Restore Purchases</Text>
      </TouchableOpacity>

      <View style={styles.legal}>
        <Text style={styles.legalText}>
          Subscriptions automatically renew unless cancelled at least 24 hours
          before the end of the current period. You can cancel anytime through
          your App Store settings.
        </Text>
        <View style={styles.legalLinks}>
          <TouchableOpacity>
            <Text style={styles.legalLink}>Terms of Use</Text>
          </TouchableOpacity>
          <Text style={styles.legalSeparator}>|</Text>
          <TouchableOpacity>
            <Text style={styles.legalLink}>Privacy Policy</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  content: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  icon: {
    fontSize: 64,
    marginBottom: 16,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#8b8b9e',
  },
  features: {
    marginBottom: 32,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: 16,
    width: 40,
    textAlign: 'center',
  },
  featureText: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 2,
  },
  featureDescription: {
    fontSize: 14,
    color: '#8b8b9e',
  },
  plans: {
    marginBottom: 24,
  },
  planCard: {
    backgroundColor: '#6c63ff',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 12,
    position: 'relative',
  },
  planCardSecondary: {
    backgroundColor: '#2a2a4e',
  },
  popularBadge: {
    position: 'absolute',
    top: -12,
    backgroundColor: '#ffd700',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  popularText: {
    color: '#000',
    fontSize: 12,
    fontWeight: 'bold',
  },
  planName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 8,
    marginTop: 8,
  },
  planPrice: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  planSavings: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    fontWeight: '600',
    marginBottom: 4,
  },
  planPer: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
  },
  restoreButton: {
    alignItems: 'center',
    paddingVertical: 16,
    marginBottom: 24,
  },
  restoreText: {
    color: '#6c63ff',
    fontSize: 16,
  },
  legal: {
    alignItems: 'center',
  },
  legalText: {
    color: '#5a5a7e',
    fontSize: 12,
    textAlign: 'center',
    lineHeight: 18,
    marginBottom: 16,
  },
  legalLinks: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legalLink: {
    color: '#8b8b9e',
    fontSize: 12,
  },
  legalSeparator: {
    color: '#5a5a7e',
    marginHorizontal: 8,
  },
});
