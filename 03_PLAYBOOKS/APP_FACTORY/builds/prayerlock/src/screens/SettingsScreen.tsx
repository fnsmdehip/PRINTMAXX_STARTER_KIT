import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  StatusBar,
  Switch,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Button, DurationPicker } from '../components';
import { Colors, FaithType, FAITH_STRINGS } from '../constants';
import { useApp } from '../context/AppContext';
import { autoDetectMethod, CalculationMethod, Madhab } from '../services/salahTimes';

type RootStackParamList = {
  Home: undefined;
  Settings: undefined;
  Paywall: undefined;
};

type SettingsScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Settings'>;
};

const TIME_OPTIONS = [
  '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00',
];

const FAITH_OPTIONS: { id: FaithType; label: string }[] = [
  { id: 'christianity', label: 'Christianity' },
  { id: 'islam', label: 'Islam' },
  { id: 'general', label: 'Mindfulness' },
];

const CALCULATION_METHODS: { id: CalculationMethod; label: string }[] = [
  { id: 'ISNA', label: 'ISNA (North America)' },
  { id: 'MWL', label: 'Muslim World League' },
  { id: 'Egypt', label: 'Egyptian Authority' },
  { id: 'Makkah', label: 'Umm al-Qura (Makkah)' },
  { id: 'Karachi', label: 'University of Karachi' },
];

const MADHAB_OPTIONS: { id: Madhab; label: string }[] = [
  { id: 'Shafi', label: "Shafi'i / Maliki / Hanbali" },
  { id: 'Hanafi', label: 'Hanafi' },
];

export function SettingsScreen({ navigation }: SettingsScreenProps) {
  const { settings, updateSettings, isPremium } = useApp();
  const [showTimePicker, setShowTimePicker] = useState(false);
  const [showFaithPicker, setShowFaithPicker] = useState(false);
  const [showMethodPicker, setShowMethodPicker] = useState(false);
  const [showMadhabPicker, setShowMadhabPicker] = useState(false);

  const isIslam = settings.faith === 'islam';
  const faithStrings = FAITH_STRINGS[settings.faith];

  const handleTimeSelect = (time: string) => {
    updateSettings({ lockTime: time });
    setShowTimePicker(false);
  };

  const handleDurationSelect = (duration: number) => {
    if (!isPremium && duration > 15) {
      Alert.alert(
        'Pro Feature',
        `Extended ${isIslam ? 'salah' : 'prayer'} times are available with PrayerLock Pro.`,
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'View Pro', onPress: () => navigation.navigate('Paywall') },
        ]
      );
      return;
    }
    updateSettings({ prayerDuration: duration });
  };

  const handleNotificationToggle = (value: boolean) => {
    updateSettings({ notificationsEnabled: value });
    if (value) {
      Alert.alert(
        'Notifications Enabled',
        isIslam
          ? 'You will receive a reminder at each salah time.'
          : 'You will receive a reminder at your set lock time.',
      );
    }
  };

  const handleHapticToggle = (value: boolean) => {
    updateSettings({ hapticEnabled: value });
  };

  const handleFaithSelect = (faith: FaithType) => {
    updateSettings({ faith });
    setShowFaithPicker(false);
  };

  const handleCalculationMethodSelect = (method: CalculationMethod) => {
    updateSettings({
      salahSettings: { ...settings.salahSettings, calculationMethod: method },
    });
    setShowMethodPicker(false);
  };

  const handleMadhabSelect = (madhab: Madhab) => {
    updateSettings({
      salahSettings: { ...settings.salahSettings, madhab },
    });
    setShowMadhabPicker(false);
  };

  const handleSalahToggle = (salahName: string, value: boolean) => {
    updateSettings({
      salahSettings: { ...settings.salahSettings, [`${salahName}Enabled`]: value },
    });
  };

  const handleCityChange = () => {
    Alert.prompt(
      'Set City',
      'Enter your city name for prayer time calculation',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (city?: string) => {
            if (city && city.trim()) {
              updateSettings({
                salahSettings: { ...settings.salahSettings, city: city.trim() },
              });
            }
          },
        },
      ],
      'plain-text',
      settings.salahSettings.city,
    );
  };

  const handleCountryChange = () => {
    Alert.prompt(
      'Set Country',
      'Enter your country code (e.g., US, UK, SA, PK)',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (country?: string) => {
            if (country && country.trim()) {
              const detectedMethod = autoDetectMethod(country.trim());
              updateSettings({
                salahSettings: {
                  ...settings.salahSettings,
                  country: country.trim(),
                  calculationMethod: detectedMethod,
                },
              });
            }
          },
        },
      ],
      'plain-text',
      settings.salahSettings.country,
    );
  };

  const formatTime12Hour = (time24: string) => {
    const [hours, minutes] = time24.split(':').map(Number);
    const period = hours >= 12 ? 'PM' : 'AM';
    const hours12 = hours % 12 || 12;
    return `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`;
  };

  const getFaithLabel = (faith: FaithType) => {
    return FAITH_OPTIONS.find((f) => f.id === faith)?.label || faith;
  };

  const getMethodLabel = (method: CalculationMethod) => {
    return CALCULATION_METHODS.find((m) => m.id === method)?.label || method;
  };

  const getMadhabLabel = (madhab: Madhab) => {
    return MADHAB_OPTIONS.find((m) => m.id === madhab)?.label || madhab;
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </View>

        {/* Faith Selection */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Faith Tradition</Text>
          <TouchableOpacity
            style={styles.selector}
            onPress={() => setShowFaithPicker(!showFaithPicker)}
          >
            <Text style={styles.selectorText}>{getFaithLabel(settings.faith)}</Text>
            <Text style={styles.selectorArrow}>{showFaithPicker ? '\u25B2' : '\u25BC'}</Text>
          </TouchableOpacity>

          {showFaithPicker && (
            <View style={styles.optionsGrid}>
              {FAITH_OPTIONS.map((option) => (
                <TouchableOpacity
                  key={option.id}
                  style={[
                    styles.option,
                    settings.faith === option.id && styles.selectedOption,
                  ]}
                  onPress={() => handleFaithSelect(option.id)}
                >
                  <Text
                    style={[
                      styles.optionText,
                      settings.faith === option.id && styles.selectedOptionText,
                    ]}
                  >
                    {option.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          )}
        </View>

        {/* Lock Time Section (non-Islam) */}
        {!isIslam && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Morning Lock Time</Text>
            <TouchableOpacity
              style={styles.selector}
              onPress={() => setShowTimePicker(!showTimePicker)}
            >
              <Text style={styles.selectorText}>
                {formatTime12Hour(settings.lockTime)}
              </Text>
              <Text style={styles.selectorArrow}>{showTimePicker ? '\u25B2' : '\u25BC'}</Text>
            </TouchableOpacity>

            {showTimePicker && (
              <View style={styles.optionsGrid}>
                {TIME_OPTIONS.map((time) => (
                  <TouchableOpacity
                    key={time}
                    style={[
                      styles.option,
                      settings.lockTime === time && styles.selectedOption,
                    ]}
                    onPress={() => handleTimeSelect(time)}
                  >
                    <Text
                      style={[
                        styles.optionText,
                        settings.lockTime === time && styles.selectedOptionText,
                      ]}
                    >
                      {formatTime12Hour(time)}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}
          </View>
        )}

        {/* Salah Settings (Islam only) */}
        {isIslam && (
          <>
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Location</Text>
              <TouchableOpacity style={styles.settingRow} onPress={handleCityChange}>
                <Text style={styles.settingTitle}>City</Text>
                <Text style={styles.settingValue}>{settings.salahSettings.city}</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.settingRow} onPress={handleCountryChange}>
                <Text style={styles.settingTitle}>Country</Text>
                <Text style={styles.settingValue}>{settings.salahSettings.country}</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Calculation Method</Text>
              <TouchableOpacity
                style={styles.selector}
                onPress={() => setShowMethodPicker(!showMethodPicker)}
              >
                <Text style={styles.selectorText}>
                  {getMethodLabel(settings.salahSettings.calculationMethod)}
                </Text>
                <Text style={styles.selectorArrow}>{showMethodPicker ? '\u25B2' : '\u25BC'}</Text>
              </TouchableOpacity>

              {showMethodPicker && (
                <View style={styles.optionsList}>
                  {CALCULATION_METHODS.map((method) => (
                    <TouchableOpacity
                      key={method.id}
                      style={[
                        styles.optionRow,
                        settings.salahSettings.calculationMethod === method.id && styles.selectedOptionRow,
                      ]}
                      onPress={() => handleCalculationMethodSelect(method.id)}
                    >
                      <Text
                        style={[
                          styles.optionRowText,
                          settings.salahSettings.calculationMethod === method.id && styles.selectedOptionText,
                        ]}
                      >
                        {method.label}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}
            </View>

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Madhab (Asr Calculation)</Text>
              <TouchableOpacity
                style={styles.selector}
                onPress={() => setShowMadhabPicker(!showMadhabPicker)}
              >
                <Text style={styles.selectorText}>
                  {getMadhabLabel(settings.salahSettings.madhab)}
                </Text>
                <Text style={styles.selectorArrow}>{showMadhabPicker ? '\u25B2' : '\u25BC'}</Text>
              </TouchableOpacity>

              {showMadhabPicker && (
                <View style={styles.optionsList}>
                  {MADHAB_OPTIONS.map((option) => (
                    <TouchableOpacity
                      key={option.id}
                      style={[
                        styles.optionRow,
                        settings.salahSettings.madhab === option.id && styles.selectedOptionRow,
                      ]}
                      onPress={() => handleMadhabSelect(option.id)}
                    >
                      <Text
                        style={[
                          styles.optionRowText,
                          settings.salahSettings.madhab === option.id && styles.selectedOptionText,
                        ]}
                      >
                        {option.label}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}
            </View>

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Enabled Prayers</Text>
              {['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'].map((name) => {
                const displayNames: Record<string, string> = {
                  fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha',
                };
                const key = `${name}Enabled` as keyof typeof settings.salahSettings;
                return (
                  <View key={name} style={styles.settingRow}>
                    <Text style={styles.settingTitle}>{displayNames[name]}</Text>
                    <Switch
                      value={settings.salahSettings[key] as boolean}
                      onValueChange={(value) => handleSalahToggle(name, value)}
                      trackColor={{ false: Colors.border, true: Colors.primary }}
                      thumbColor={Colors.white}
                    />
                  </View>
                );
              })}
            </View>
          </>
        )}

        {/* Prayer Duration Section (non-Islam) */}
        {!isIslam && (
          <View style={styles.section}>
            <DurationPicker
              selectedDuration={settings.prayerDuration}
              onSelect={handleDurationSelect}
              isPremium={isPremium}
            />
          </View>
        )}

        {/* Notifications Section */}
        <View style={styles.section}>
          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>
                {isIslam ? 'Salah Reminders' : 'Morning Reminder'}
              </Text>
              <Text style={styles.settingSubtitle}>
                {isIslam
                  ? 'Get notified at each salah time'
                  : "Get notified when it's prayer time"}
              </Text>
            </View>
            <Switch
              value={settings.notificationsEnabled}
              onValueChange={handleNotificationToggle}
              trackColor={{ false: Colors.border, true: Colors.primary }}
              thumbColor={Colors.white}
            />
          </View>

          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Haptic Feedback</Text>
              <Text style={styles.settingSubtitle}>
                Vibration on button presses
              </Text>
            </View>
            <Switch
              value={settings.hapticEnabled}
              onValueChange={handleHapticToggle}
              trackColor={{ false: Colors.border, true: Colors.primary }}
              thumbColor={Colors.white}
            />
          </View>
        </View>

        {/* Pro Section */}
        {!isPremium && (
          <View style={styles.proSection}>
            <Text style={styles.proTitle}>PrayerLock Pro</Text>
            <View style={styles.proFeatures}>
              <Text style={styles.proFeature}>
                Extended {isIslam ? 'salah' : 'prayer'} times (30+ min)
              </Text>
              <Text style={styles.proFeature}>Family accountability</Text>
              <Text style={styles.proFeature}>Custom prayer prompts</Text>
              <Text style={styles.proFeature}>Streak freezes</Text>
              <Text style={styles.proFeature}>Ad-free experience</Text>
            </View>
            <Button
              title="Upgrade to Pro"
              onPress={() => navigation.navigate('Paywall')}
              size="large"
              style={styles.proButton}
            />
          </View>
        )}

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <View style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
          <TouchableOpacity style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Privacy Policy</Text>
            <Text style={styles.aboutArrow}>{'\u2192'}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Terms of Service</Text>
            <Text style={styles.aboutArrow}>{'\u2192'}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Contact Support</Text>
            <Text style={styles.aboutArrow}>{'\u2192'}</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scrollContent: {
    paddingBottom: 100,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
  },
  section: {
    backgroundColor: Colors.white,
    marginHorizontal: 20,
    marginBottom: 16,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 12,
  },
  selector: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: Colors.background,
    padding: 16,
    borderRadius: 12,
  },
  selectorText: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  selectorArrow: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 12,
    gap: 8,
  },
  option: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    backgroundColor: Colors.background,
  },
  selectedOption: {
    backgroundColor: Colors.primary,
  },
  optionText: {
    fontSize: 14,
    color: Colors.text,
    fontWeight: '500',
  },
  selectedOptionText: {
    color: Colors.white,
  },
  optionsList: {
    marginTop: 12,
    gap: 4,
  },
  optionRow: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    backgroundColor: Colors.background,
  },
  selectedOptionRow: {
    backgroundColor: Colors.primary,
  },
  optionRowText: {
    fontSize: 14,
    color: Colors.text,
    fontWeight: '500',
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  settingInfo: {
    flex: 1,
    marginRight: 16,
  },
  settingTitle: {
    fontSize: 16,
    color: Colors.text,
    fontWeight: '500',
  },
  settingValue: {
    fontSize: 16,
    color: Colors.primary,
    fontWeight: '500',
  },
  settingSubtitle: {
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  proSection: {
    backgroundColor: Colors.secondary,
    marginHorizontal: 20,
    marginBottom: 16,
    borderRadius: 16,
    padding: 24,
  },
  proTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 16,
  },
  proFeatures: {
    marginBottom: 20,
  },
  proFeature: {
    fontSize: 15,
    color: 'rgba(255, 255, 255, 0.9)',
    marginBottom: 8,
    paddingLeft: 16,
  },
  proButton: {
    backgroundColor: Colors.primary,
  },
  aboutItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  aboutLabel: {
    fontSize: 16,
    color: Colors.text,
  },
  aboutValue: {
    fontSize: 16,
    color: Colors.textSecondary,
  },
  aboutArrow: {
    fontSize: 16,
    color: Colors.textSecondary,
  },
});
