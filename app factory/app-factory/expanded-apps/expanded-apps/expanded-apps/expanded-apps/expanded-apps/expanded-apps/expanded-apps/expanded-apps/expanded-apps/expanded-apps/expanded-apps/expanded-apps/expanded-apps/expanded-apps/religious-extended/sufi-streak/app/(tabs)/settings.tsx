import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
  Share,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  getNotificationSettings,
  saveNotificationSettings,
  requestNotificationPermissions,
  NotificationSettings,
} from '../../src/lib/notifications';
import { setAdFreeStatus, checkIsAdFree } from '../../src/components/AdBanner';

const STATS_KEY = 'scripture_streak_stats';

interface SettingItem {
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  title: string;
  subtitle?: string;
  onPress?: () => void;
  value?: boolean;
  onValueChange?: (value: boolean) => void;
  disabled?: boolean;
  rightElement?: React.ReactNode;
}

export default function SettingsScreen() {
  const router = useRouter();
  const [notificationSettings, setNotificationSettings] = useState<NotificationSettings>({
    enabled: true,
    hour: 7,
    minute: 0,
  });
  const [isAdFree, setIsAdFree] = useState(false);
  const [stats, setStats] = useState({ streak_count: 0 });
  
  // Animations
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    loadSettings();
    Animated.timing(fadeAnim, { toValue: 1, duration: 400, useNativeDriver: true }).start();
  }, []);

  const loadSettings = async () => {
    const settings = await getNotificationSettings();
    setNotificationSettings(settings);
    
    const adFree = await checkIsAdFree();
    setIsAdFree(adFree);

    const statsData = await AsyncStorage.getItem(STATS_KEY);
    if (statsData) {
      setStats(JSON.parse(statsData));
    }
  };

  const handleNotificationToggle = async (enabled: boolean) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    if (enabled) {
      const hasPermission = await requestNotificationPermissions();
      if (!hasPermission) {
        Alert.alert(
          'Notifications Disabled',
          'Please enable notifications in your device settings to receive daily reminders.',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Open Settings', onPress: () => Linking.openSettings() },
          ]
        );
        return;
      }
    }

    const newSettings = { ...notificationSettings, enabled };
    setNotificationSettings(newSettings);
    await saveNotificationSettings(newSettings);
  };

  const handleTimeChange = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    Alert.alert(
      'Set Reminder Time',
      'Choose when you want your daily reminder:',
      [
        { text: '6:00 AM', onPress: () => updateTime(6, 0) },
        { text: '7:00 AM', onPress: () => updateTime(7, 0) },
        { text: '8:00 AM', onPress: () => updateTime(8, 0) },
        { text: '9:00 AM', onPress: () => updateTime(9, 0) },
        { text: '12:00 PM', onPress: () => updateTime(12, 0) },
        { text: 'Cancel', style: 'cancel' },
      ]
    );
  };

  const updateTime = async (hour: number, minute: number) => {
    const newSettings = { ...notificationSettings, hour, minute };
    setNotificationSettings(newSettings);
    await saveNotificationSettings(newSettings);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  };

  const formatTime = (hour: number, minute: number) => {
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
    return `${displayHour}:${minute.toString().padStart(2, '0')} ${period}`;
  };

  const handleRemoveAds = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    router.push('/paywall');
  };

  const handleRestorePurchases = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Alert.alert('Checking...', 'Looking for previous purchases...');
    setTimeout(() => {
      Alert.alert('No Purchases Found', 'No previous purchases were found to restore.');
    }, 1500);
  };

  const handleRateApp = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Linking.openURL('https://apps.apple.com/app/id123456789');
  };

  const handleShareApp = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    try {
      await Share.share({
        message: "I'm building my daily Bible habit with Scripture Streak! 📖🔥 Join me: https://apps.apple.com/app/scripture-streak",
      });
    } catch (error) {
      console.log('Share error:', error);
    }
  };

  const handleSupport = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Linking.openURL('mailto:support@scripturestreak.com?subject=Scripture%20Streak%20Support');
  };

  const handlePrivacyPolicy = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Linking.openURL('https://scripturestreak.com/privacy');
  };

  const handleTerms = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Linking.openURL('https://scripturestreak.com/terms');
  };

  const handleResetPaywall = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    router.push('/paywall');
  };

  const SettingRow = ({ icon, color, title, subtitle, onPress, disabled, rightElement }: SettingItem) => (
    <TouchableOpacity
      style={[styles.settingItem, disabled && styles.settingItemDisabled]}
      onPress={onPress}
      disabled={disabled || !onPress}
      activeOpacity={onPress ? 0.7 : 1}
    >
      <View style={[styles.settingIconContainer, { backgroundColor: color + '20' }]}>
        <Ionicons name={icon} size={20} color={disabled ? color + '50' : color} />
      </View>
      <View style={styles.settingContent}>
        <Text style={[styles.settingTitle, disabled && styles.settingTextDisabled]}>{title}</Text>
        {subtitle && (
          <Text style={[styles.settingSubtitle, disabled && styles.settingTextDisabled]}>{subtitle}</Text>
        )}
      </View>
      {rightElement || (onPress && <Ionicons name="chevron-forward" size={20} color="#ffffff30" />)}
    </TouchableOpacity>
  );

  return (
    <LinearGradient
      colors={['#1a1a2e', '#0f0f23', '#1a1a2e']}
      style={styles.container}
    >
      <Animated.ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        style={{ opacity: fadeAnim }}
      >
        {/* Header */}
        <Text style={styles.title}>Settings</Text>

        {/* User Card */}
        <View style={styles.userCard}>
          <View style={styles.userAvatar}>
            <Ionicons name="person" size={28} color="#e94560" />
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>Believer</Text>
            <View style={styles.statusBadge}>
              <Ionicons 
                name={isAdFree ? "checkmark-circle" : "gift"} 
                size={14} 
                color={isAdFree ? "#4ade80" : "#fbbf24"} 
              />
              <Text style={[styles.userStatus, { color: isAdFree ? "#4ade80" : "#fbbf24" }]}>
                {isAdFree ? 'Ad-Free Member' : 'Free User'}
              </Text>
            </View>
          </View>
          <View style={styles.userStats}>
            <Ionicons name="flame" size={20} color="#e94560" />
            <Text style={styles.userStatsValue}>{stats.streak_count}</Text>
          </View>
        </View>

        {/* Remove Ads Banner */}
        {!isAdFree && (
          <TouchableOpacity style={styles.upgradeCard} onPress={handleRemoveAds} activeOpacity={0.8}>
            <LinearGradient
              colors={['#e94560', '#c23a51']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.upgradeGradient}
            >
              <View style={styles.upgradeIconContainer}>
                <Ionicons name="sparkles" size={28} color="#ffffff" />
              </View>
              <View style={styles.upgradeContent}>
                <Text style={styles.upgradeTitle}>Go Premium</Text>
                <Text style={styles.upgradeSubtitle}>Ad-free for just $1.99</Text>
              </View>
              <Ionicons name="arrow-forward" size={24} color="#ffffff" />
            </LinearGradient>
          </TouchableOpacity>
        )}

        {/* Notifications Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="notifications" size={18} color="#ffffff50" />
            <Text style={styles.sectionTitle}>Notifications</Text>
          </View>
          <View style={styles.sectionContent}>
            <SettingRow
              icon="notifications"
              color="#fbbf24"
              title="Daily Reminders"
              subtitle="Don't break your streak"
              rightElement={
                <Switch
                  value={notificationSettings.enabled}
                  onValueChange={handleNotificationToggle}
                  trackColor={{ false: '#ffffff15', true: '#e9456050' }}
                  thumbColor={notificationSettings.enabled ? '#e94560' : '#ffffff40'}
                />
              }
            />
            <View style={styles.divider} />
            <SettingRow
              icon="time"
              color="#60a5fa"
              title="Reminder Time"
              subtitle={formatTime(notificationSettings.hour, notificationSettings.minute)}
              onPress={handleTimeChange}
              disabled={!notificationSettings.enabled}
            />
          </View>
        </View>

        {/* Purchases Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="card" size={18} color="#ffffff50" />
            <Text style={styles.sectionTitle}>Purchases</Text>
          </View>
          <View style={styles.sectionContent}>
            <SettingRow
              icon="refresh"
              color="#34d399"
              title="Restore Purchases"
              subtitle="Restore on a new device"
              onPress={handleRestorePurchases}
            />
          </View>
        </View>

        {/* Support Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="heart" size={18} color="#ffffff50" />
            <Text style={styles.sectionTitle}>Support</Text>
          </View>
          <View style={styles.sectionContent}>
            <SettingRow
              icon="star"
              color="#fbbf24"
              title="Rate App"
              subtitle="Help us reach more believers"
              onPress={handleRateApp}
            />
            <View style={styles.divider} />
            <SettingRow
              icon="share-social"
              color="#60a5fa"
              title="Share App"
              subtitle="Tell your friends about us"
              onPress={handleShareApp}
            />
            <View style={styles.divider} />
            <SettingRow
              icon="mail"
              color="#f472b6"
              title="Contact Support"
              subtitle="We're here to help"
              onPress={handleSupport}
            />
          </View>
        </View>

        {/* Legal Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="document-text" size={18} color="#ffffff50" />
            <Text style={styles.sectionTitle}>Legal</Text>
          </View>
          <View style={styles.sectionContent}>
            <SettingRow
              icon="shield-checkmark"
              color="#34d399"
              title="Privacy Policy"
              onPress={handlePrivacyPolicy}
            />
            <View style={styles.divider} />
            <SettingRow
              icon="document"
              color="#a78bfa"
              title="Terms of Service"
              onPress={handleTerms}
            />
          </View>
        </View>

        {/* Debug Button - Remove in production */}
        <TouchableOpacity style={styles.debugButton} onPress={handleResetPaywall}>
          <Ionicons name="construct" size={16} color="#ffffff30" />
          <Text style={styles.debugText}>Reset to Paywall (Debug)</Text>
        </TouchableOpacity>

        {/* Version */}
        <Text style={styles.version}>Scripture Streak v1.0.0</Text>
      </Animated.ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 120,
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: '#ffffff',
    marginBottom: 24,
  },
  userCard: {
    backgroundColor: '#ffffff08',
    borderRadius: 22,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#ffffff08',
  },
  userAvatar: {
    width: 56,
    height: 56,
    borderRadius: 18,
    backgroundColor: '#e9456020',
    justifyContent: 'center',
    alignItems: 'center',
  },
  userInfo: {
    flex: 1,
    marginLeft: 16,
  },
  userName: {
    fontSize: 20,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 4,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  userStatus: {
    fontSize: 14,
    fontWeight: '600',
  },
  userStats: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e9456015',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 14,
    gap: 6,
  },
  userStatsValue: {
    fontSize: 22,
    fontWeight: '800',
    color: '#e94560',
  },
  upgradeCard: {
    borderRadius: 18,
    overflow: 'hidden',
    marginBottom: 28,
  },
  upgradeGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
  },
  upgradeIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 14,
    backgroundColor: 'rgba(255,255,255,0.15)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  upgradeContent: {
    flex: 1,
  },
  upgradeTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 2,
  },
  upgradeSubtitle: {
    fontSize: 14,
    color: '#ffffff90',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
    marginLeft: 4,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#ffffff50',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  sectionContent: {
    backgroundColor: '#ffffff08',
    borderRadius: 18,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#ffffff06',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  settingItemDisabled: {
    opacity: 0.5,
  },
  settingIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: 13,
    color: '#ffffff50',
  },
  settingTextDisabled: {
    color: '#ffffff40',
  },
  divider: {
    height: 1,
    backgroundColor: '#ffffff08',
    marginLeft: 70,
  },
  debugButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
    marginBottom: 16,
    gap: 8,
  },
  debugText: {
    fontSize: 14,
    color: '#ffffff30',
  },
  version: {
    textAlign: 'center',
    fontSize: 13,
    color: '#ffffff25',
    marginTop: 8,
  },
});
