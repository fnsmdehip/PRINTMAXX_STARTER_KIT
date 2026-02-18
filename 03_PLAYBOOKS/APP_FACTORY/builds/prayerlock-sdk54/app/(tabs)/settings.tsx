import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Switch, Linking } from 'react-native';
import { router } from 'expo-router';
import { useUserStore } from '../../src/stores/userStore';
import Slider from '@react-native-community/slider';
import { MoreApps } from '../../src/components/MoreApps';

export default function Settings() {
  const settings = useUserStore((state) => state.settings);
  const updateSettings = useUserStore((state) => state.updateSettings);
  const isSubscribed = useUserStore((state) => state.isSubscribed);
  const trialEndsAt = useUserStore((state) => state.trialEndsAt);

  const trialDaysLeft = trialEndsAt
    ? Math.max(0, Math.ceil((trialEndsAt - Date.now()) / (1000 * 60 * 60 * 24)))
    : 0;

  return (
    <ScrollView style={styles.container}>
      {!isSubscribed && trialDaysLeft > 0 && (
        <View style={styles.trialBanner}>
          <Text style={styles.trialText}>
            {trialDaysLeft} day{trialDaysLeft !== 1 ? 's' : ''} left in trial
          </Text>
          <TouchableOpacity
            style={styles.upgradeButton}
            onPress={() => router.push('/paywall')}
          >
            <Text style={styles.upgradeText}>Upgrade</Text>
          </TouchableOpacity>
        </View>
      )}

      <Text style={styles.sectionTitle}>Devotional Settings</Text>

      <View style={styles.settingCard}>
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Prayer Duration</Text>
          <Text style={styles.settingValue}>{settings.devotionDurationMinutes} min</Text>
        </View>
        <View style={styles.sliderContainer}>
          <Slider
            style={styles.slider}
            minimumValue={5}
            maximumValue={60}
            step={5}
            value={settings.devotionDurationMinutes}
            onValueChange={(value) => updateSettings({ devotionDurationMinutes: value })}
            minimumTrackTintColor="#6c63ff"
            maximumTrackTintColor="#3a3a5e"
            thumbTintColor="#6c63ff"
          />
        </View>
      </View>

      <View style={styles.settingCard}>
        <View style={styles.settingRow}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Require Prayer Timer</Text>
            <Text style={styles.settingDescription}>
              Must complete prayer time to unlock
            </Text>
          </View>
          <Switch
            value={settings.requireTimer}
            onValueChange={(value) => updateSettings({ requireTimer: value })}
            trackColor={{ false: '#3a3a5e', true: '#6c63ff' }}
            thumbColor="#fff"
          />
        </View>
      </View>

      <View style={styles.settingCard}>
        <View style={styles.settingRow}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Require Scripture</Text>
            <Text style={styles.settingDescription}>
              Must read daily verse to unlock
            </Text>
          </View>
          <Switch
            value={settings.requireScripture}
            onValueChange={(value) => updateSettings({ requireScripture: value })}
            trackColor={{ false: '#3a3a5e', true: '#6c63ff' }}
            thumbColor="#fff"
          />
        </View>
      </View>

      <View style={styles.settingCard}>
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Daily Reset Time</Text>
          <Text style={styles.settingValue}>{settings.dailyResetTime}</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Emergency</Text>

      <TouchableOpacity
        style={styles.emergencyButton}
        onPress={() => router.push('/emergency-unlock')}
      >
        <Text style={styles.emergencyIcon}>🚨</Text>
        <View style={styles.emergencyInfo}>
          <Text style={styles.emergencyLabel}>Emergency Unlock</Text>
          <Text style={styles.emergencyDescription}>
            Bypass today's devotional (resets streak)
          </Text>
        </View>
      </TouchableOpacity>

      <Text style={styles.sectionTitle}>Account</Text>

      {isSubscribed ? (
        <View style={styles.settingCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Subscription Active</Text>
              <Text style={styles.settingDescription}>
                Thank you for supporting PrayerLock
              </Text>
            </View>
            <Text style={styles.checkmark}>✓</Text>
          </View>
        </View>
      ) : (
        <TouchableOpacity
          style={styles.subscribeButton}
          onPress={() => router.push('/paywall')}
        >
          <Text style={styles.subscribeText}>Subscribe to PrayerLock Pro</Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => Linking.openURL('https://printmaxx.com/privacy')}
      >
        <Text style={styles.linkText}>Privacy Policy</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => Linking.openURL('https://printmaxx.com/terms')}
      >
        <Text style={styles.linkText}>Terms of Service</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => {
          // In production, wire to RevenueCat restore
          console.log('Restore purchases');
        }}
      >
        <Text style={styles.linkText}>Restore Purchases</Text>
      </TouchableOpacity>

      <MoreApps />

      <View style={styles.footer}>
        <Text style={styles.version}>PrayerLock v1.0.0</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 20,
  },
  trialBanner: {
    backgroundColor: '#6c63ff',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  trialText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '500',
  },
  upgradeButton: {
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  upgradeText: {
    color: '#6c63ff',
    fontWeight: '600',
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#8b8b9e',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  settingCard: {
    backgroundColor: '#2a2a4e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  settingInfo: {
    flex: 1,
    marginRight: 12,
  },
  settingLabel: {
    fontSize: 16,
    color: '#fff',
    fontWeight: '500',
  },
  settingDescription: {
    fontSize: 13,
    color: '#8b8b9e',
    marginTop: 4,
  },
  settingValue: {
    fontSize: 16,
    color: '#6c63ff',
    fontWeight: '600',
  },
  sliderContainer: {
    marginTop: 12,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  emergencyButton: {
    backgroundColor: '#3a2a2e',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#5a3a3e',
  },
  emergencyIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  emergencyInfo: {
    flex: 1,
  },
  emergencyLabel: {
    fontSize: 16,
    color: '#ff6b6b',
    fontWeight: '500',
  },
  emergencyDescription: {
    fontSize: 13,
    color: '#8b7b7e',
    marginTop: 4,
  },
  subscribeButton: {
    backgroundColor: '#6c63ff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginBottom: 24,
  },
  subscribeText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  checkmark: {
    color: '#4caf50',
    fontSize: 20,
  },
  linkButton: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a4e',
  },
  linkText: {
    color: '#8b8b9e',
    fontSize: 16,
  },
  footer: {
    paddingVertical: 32,
    alignItems: 'center',
  },
  version: {
    color: '#5a5a7e',
    fontSize: 14,
  },
});
