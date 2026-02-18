import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Colors } from '../constants';
import { useApp } from '../context/AppContext';
import { fetchSalahTimes, formatSalahTime, getNextSalah, SalahTimes, SALAH_PRAYERS } from '../services/salahTimes';
import { getSalahCompletionCount } from '../utils/storage';

interface SalahTrackerProps {
  onPrayerPress: (salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha') => void;
}

export function SalahTracker({ onPrayerPress }: SalahTrackerProps) {
  const { settings, salahStatus } = useApp();
  const [salahTimes, setSalahTimes] = useState<SalahTimes | null>(null);
  const [nextPrayer, setNextPrayer] = useState<{ name: string; time: string } | null>(null);

  useEffect(() => {
    const loadTimes = async () => {
      const { salahSettings } = settings;
      const times = await fetchSalahTimes(
        salahSettings.city,
        salahSettings.country,
        salahSettings.calculationMethod,
        salahSettings.madhab
      );
      if (times) {
        setSalahTimes(times);
        setNextPrayer(getNextSalah(times));
      }
    };
    loadTimes();
  }, [settings]);

  const completedCount = getSalahCompletionCount(salahStatus);

  const getStatusColor = (salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha'): string => {
    if (salahStatus[salahName]) return Colors.success;
    if (nextPrayer && nextPrayer.name === salahName) return Colors.primary;
    return Colors.border;
  };

  const getStatusIcon = (salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha'): string => {
    if (salahStatus[salahName]) return '\u2713';
    if (nextPrayer && nextPrayer.name === salahName) return '\u25CF';
    return '\u25CB';
  };

  const enabledPrayers = SALAH_PRAYERS.filter((p) => {
    const key = `${p.name}Enabled` as keyof typeof settings.salahSettings;
    return settings.salahSettings[key] !== false;
  });

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Today's Salah</Text>
        <Text style={styles.counter}>{completedCount}/5</Text>
      </View>

      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${(completedCount / 5) * 100}%` }]} />
      </View>

      <View style={styles.prayerList}>
        {enabledPrayers.map((prayer) => {
          const isCompleted = salahStatus[prayer.name];
          const isNext = nextPrayer?.name === prayer.name;
          const timeStr = salahTimes ? formatSalahTime(salahTimes[prayer.name]) : '--:--';

          return (
            <TouchableOpacity
              key={prayer.name}
              style={[
                styles.prayerItem,
                isCompleted && styles.prayerCompleted,
                isNext && !isCompleted && styles.prayerNext,
              ]}
              onPress={() => !isCompleted && onPrayerPress(prayer.name)}
              disabled={isCompleted}
              activeOpacity={isCompleted ? 1 : 0.7}
            >
              <View style={[styles.statusDot, { backgroundColor: getStatusColor(prayer.name) }]}>
                <Text style={styles.statusIcon}>{getStatusIcon(prayer.name)}</Text>
              </View>
              <View style={styles.prayerInfo}>
                <Text style={[styles.prayerName, isCompleted && styles.prayerNameDone]}>
                  {prayer.displayName}
                </Text>
                <Text style={styles.prayerTime}>{timeStr}</Text>
              </View>
              {isNext && !isCompleted && (
                <View style={styles.nextBadge}>
                  <Text style={styles.nextBadgeText}>Next</Text>
                </View>
              )}
              {isCompleted && (
                <Text style={styles.doneText}>Done</Text>
              )}
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
  },
  counter: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.primary,
  },
  progressBar: {
    height: 4,
    backgroundColor: Colors.border,
    borderRadius: 2,
    marginBottom: 16,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: Colors.success,
    borderRadius: 2,
  },
  prayerList: {
    gap: 8,
  },
  prayerItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: 12,
    backgroundColor: Colors.background,
  },
  prayerCompleted: {
    backgroundColor: 'rgba(76, 175, 80, 0.08)',
  },
  prayerNext: {
    backgroundColor: 'rgba(245, 166, 35, 0.08)',
    borderWidth: 1,
    borderColor: 'rgba(245, 166, 35, 0.2)',
  },
  statusDot: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  statusIcon: {
    color: Colors.white,
    fontSize: 14,
    fontWeight: '700',
  },
  prayerInfo: {
    flex: 1,
  },
  prayerName: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  prayerNameDone: {
    color: Colors.success,
  },
  prayerTime: {
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  nextBadge: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
  },
  nextBadgeText: {
    color: Colors.white,
    fontSize: 12,
    fontWeight: '600',
  },
  doneText: {
    fontSize: 13,
    color: Colors.success,
    fontWeight: '600',
  },
});
