import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width } = Dimensions.get('window');

interface UserStats {
  streak_count: number;
  total_verses_read: number;
  total_prayers: number;
  total_shares: number;
  last_check_in: string | null;
}

interface Milestone {
  days: number;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  title: string;
  description: string;
}

const STATS_KEY = 'scripture_streak_stats';

const milestones: Milestone[] = [
  { days: 7, icon: 'leaf', color: '#4ade80', title: '1 Week', description: 'You made it a week!' },
  { days: 30, icon: 'flower', color: '#60a5fa', title: '1 Month', description: 'A full month of devotion!' },
  { days: 90, icon: 'rose', color: '#f472b6', title: '3 Months', description: 'Incredible dedication!' },
  { days: 365, icon: 'trophy', color: '#fbbf24', title: '1 Year', description: 'True spiritual discipline!' },
];

export default function ProgressScreen() {
  const [stats, setStats] = useState<UserStats>({
    streak_count: 0,
    total_verses_read: 0,
    total_prayers: 0,
    total_shares: 0,
    last_check_in: null,
  });
  
  // Animations
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const streakAnim = useRef(new Animated.Value(0)).current;
  const statAnims = useRef([0, 1, 2, 3].map(() => new Animated.Value(0))).current;

  useEffect(() => {
    loadStats();
    
    // Entrance animations
    Animated.timing(fadeAnim, { toValue: 1, duration: 400, useNativeDriver: true }).start();
    Animated.spring(streakAnim, { toValue: 1, tension: 50, friction: 6, useNativeDriver: true, delay: 100 }).start();
    
    // Staggered stat cards
    statAnims.forEach((anim, i) => {
      Animated.timing(anim, {
        toValue: 1,
        duration: 300,
        delay: 300 + i * 80,
        useNativeDriver: true,
      }).start();
    });
  }, []);

  const loadStats = async () => {
    try {
      const statsData = await AsyncStorage.getItem(STATS_KEY);
      if (statsData) {
        setStats(JSON.parse(statsData));
      }
    } catch (e) {
      console.log('Error loading stats:', e);
    }
  };

  const nextMilestone = milestones.find(m => m.days > stats.streak_count) || milestones[milestones.length - 1];
  const progressToNext = (stats.streak_count / nextMilestone.days) * 100;

  // Weekly view
  const weekDays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  const today = new Date().getDay();

  const statsData = [
    { icon: 'book', color: '#60a5fa', value: stats.total_verses_read, label: 'Verses Read' },
    { icon: 'heart', color: '#f472b6', value: stats.total_prayers, label: 'Prayers' },
    { icon: 'share-social', color: '#34d399', value: stats.total_shares, label: 'Shares' },
    { icon: 'flame', color: '#f97316', value: stats.streak_count, label: 'Best Streak' },
  ];

  return (
    <LinearGradient
      colors={['#1a1a2e', '#0f0f23', '#1a1a2e']}
      style={styles.container}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <Animated.View style={{ opacity: fadeAnim }}>
          <Text style={styles.title}>Your Progress</Text>
        </Animated.View>

        {/* Current Streak Card */}
        <Animated.View 
          style={[
            styles.streakCard,
            {
              opacity: streakAnim,
              transform: [{
                scale: streakAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: [0.9, 1],
                })
              }]
            }
          ]}
        >
          <LinearGradient
            colors={['#e9456025', '#e9456008']}
            style={styles.streakGradient}
          >
            <View style={styles.streakIconContainer}>
              <Ionicons name="flame" size={44} color="#e94560" />
            </View>
            <Text style={styles.streakNumber}>{stats.streak_count}</Text>
            <Text style={styles.streakLabel}>Day Streak</Text>
            
            {/* Progress to next milestone */}
            <View style={styles.milestoneProgress}>
              <View style={styles.progressBarBg}>
                <Animated.View 
                  style={[
                    styles.progressBarFill, 
                    { width: `${Math.min(progressToNext, 100)}%` }
                  ]} 
                />
              </View>
              <View style={styles.milestoneTarget}>
                <Ionicons name={nextMilestone.icon} size={16} color={nextMilestone.color} />
                <Text style={styles.milestoneText}>
                  {stats.streak_count}/{nextMilestone.days} days to {nextMilestone.title}
                </Text>
              </View>
            </View>
          </LinearGradient>
        </Animated.View>

        {/* Weekly Calendar */}
        <View style={styles.weekCard}>
          <View style={styles.weekHeader}>
            <Ionicons name="calendar" size={20} color="#ffffff60" />
            <Text style={styles.weekTitle}>This Week</Text>
          </View>
          <View style={styles.weekDays}>
            {weekDays.map((day, index) => {
              const isToday = index === today;
              const isPast = index < today;
              const isCompleted = isPast && stats.streak_count >= (today - index);
              
              return (
                <View key={index} style={styles.dayContainer}>
                  <Text style={[styles.dayLabel, isToday && styles.dayLabelToday]}>{day}</Text>
                  <View style={[
                    styles.dayCircle,
                    isToday && styles.dayCircleToday,
                    isCompleted && styles.dayCircleCompleted,
                  ]}>
                    {isCompleted && <Ionicons name="checkmark" size={18} color="#ffffff" />}
                    {isToday && !isCompleted && (
                      <View style={styles.todayDot} />
                    )}
                  </View>
                </View>
              );
            })}
          </View>
        </View>

        {/* Stats Grid */}
        <View style={styles.sectionHeader}>
          <Ionicons name="stats-chart" size={20} color="#ffffff60" />
          <Text style={styles.sectionTitle}>All-Time Stats</Text>
        </View>
        <View style={styles.statsGrid}>
          {statsData.map((stat, index) => (
            <Animated.View
              key={index}
              style={[
                styles.statCard,
                {
                  opacity: statAnims[index],
                  transform: [{
                    translateY: statAnims[index].interpolate({
                      inputRange: [0, 1],
                      outputRange: [20, 0],
                    })
                  }]
                }
              ]}
            >
              <View style={[styles.statIconContainer, { backgroundColor: stat.color + '20' }]}>
                <Ionicons name={stat.icon as any} size={24} color={stat.color} />
              </View>
              <Text style={styles.statNumber}>{stat.value}</Text>
              <Text style={styles.statLabel}>{stat.label}</Text>
            </Animated.View>
          ))}
        </View>

        {/* Milestones */}
        <View style={styles.sectionHeader}>
          <Ionicons name="ribbon" size={20} color="#ffffff60" />
          <Text style={styles.sectionTitle}>Milestones</Text>
        </View>
        <View style={styles.milestonesContainer}>
          {milestones.map((milestone, index) => {
            const isUnlocked = stats.streak_count >= milestone.days;
            return (
              <View 
                key={index} 
                style={[
                  styles.milestoneCard,
                  isUnlocked && styles.milestoneCardUnlocked,
                ]}
              >
                <View style={[
                  styles.milestoneIconContainer,
                  { backgroundColor: isUnlocked ? milestone.color + '25' : '#ffffff10' }
                ]}>
                  <Ionicons 
                    name={milestone.icon} 
                    size={28} 
                    color={isUnlocked ? milestone.color : '#ffffff30'} 
                  />
                </View>
                <View style={styles.milestoneContent}>
                  <Text style={[styles.milestoneTitle, !isUnlocked && styles.locked]}>
                    {milestone.title}
                  </Text>
                  <Text style={[styles.milestoneDesc, !isUnlocked && styles.locked]}>
                    {isUnlocked ? milestone.description : `${milestone.days - stats.streak_count} days to go`}
                  </Text>
                </View>
                {isUnlocked && (
                  <View style={styles.unlockedBadge}>
                    <Ionicons name="checkmark" size={18} color="#ffffff" />
                  </View>
                )}
              </View>
            );
          })}
        </View>

        {/* Encouragement */}
        <View style={styles.encouragementCard}>
          <View style={styles.encouragementIconContainer}>
            <Ionicons name="sparkles" size={32} color="#fbbf24" />
          </View>
          <Text style={styles.encouragementText}>
            {stats.streak_count === 0
              ? "Start your journey today! Complete today's tasks to begin your streak."
              : stats.streak_count < 7
              ? "Great start! Keep going to build a lasting habit."
              : stats.streak_count < 30
              ? "You're building real consistency! Keep it up!"
              : "Amazing dedication! You're an inspiration!"}
          </Text>
        </View>
      </ScrollView>
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
  streakCard: {
    borderRadius: 24,
    overflow: 'hidden',
    marginBottom: 24,
  },
  streakGradient: {
    padding: 32,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e9456030',
    borderRadius: 24,
  },
  streakIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#e9456020',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  streakNumber: {
    fontSize: 72,
    fontWeight: '900',
    color: '#e94560',
    lineHeight: 80,
  },
  streakLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff60',
    marginBottom: 24,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  milestoneProgress: {
    width: '100%',
  },
  progressBarBg: {
    height: 10,
    backgroundColor: '#ffffff15',
    borderRadius: 5,
    overflow: 'hidden',
    marginBottom: 12,
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#e94560',
    borderRadius: 5,
  },
  milestoneTarget: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  milestoneText: {
    fontSize: 14,
    color: '#ffffff60',
    textAlign: 'center',
  },
  weekCard: {
    backgroundColor: '#ffffff08',
    borderRadius: 20,
    padding: 20,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#ffffff08',
  },
  weekHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
  },
  weekTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff',
  },
  weekDays: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  dayContainer: {
    alignItems: 'center',
  },
  dayLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#ffffff40',
    marginBottom: 10,
  },
  dayLabelToday: {
    color: '#e94560',
  },
  dayCircle: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#ffffff08',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  dayCircleToday: {
    borderColor: '#e94560',
    backgroundColor: '#e9456015',
  },
  dayCircleCompleted: {
    backgroundColor: '#4ade80',
    borderColor: '#4ade80',
  },
  todayDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#e94560',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 24,
  },
  statCard: {
    width: (width - 48 - 12) / 2,
    backgroundColor: '#ffffff08',
    borderRadius: 18,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ffffff08',
  },
  statIconContainer: {
    width: 52,
    height: 52,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: '800',
    color: '#ffffff',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 13,
    color: '#ffffff50',
    fontWeight: '600',
  },
  milestonesContainer: {
    gap: 12,
    marginBottom: 24,
  },
  milestoneCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff08',
    borderRadius: 18,
    padding: 16,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  milestoneCardUnlocked: {
    backgroundColor: '#4ade8010',
    borderColor: '#4ade8025',
  },
  milestoneIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  milestoneContent: {
    flex: 1,
  },
  milestoneTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 3,
  },
  milestoneDesc: {
    fontSize: 13,
    color: '#ffffff60',
  },
  locked: {
    opacity: 0.4,
  },
  unlockedBadge: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#4ade80',
    justifyContent: 'center',
    alignItems: 'center',
  },
  encouragementCard: {
    backgroundColor: '#fbbf2410',
    borderRadius: 22,
    padding: 24,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fbbf2420',
  },
  encouragementIconContainer: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#fbbf2415',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  encouragementText: {
    fontSize: 16,
    color: '#ffffff80',
    textAlign: 'center',
    lineHeight: 24,
  },
});
