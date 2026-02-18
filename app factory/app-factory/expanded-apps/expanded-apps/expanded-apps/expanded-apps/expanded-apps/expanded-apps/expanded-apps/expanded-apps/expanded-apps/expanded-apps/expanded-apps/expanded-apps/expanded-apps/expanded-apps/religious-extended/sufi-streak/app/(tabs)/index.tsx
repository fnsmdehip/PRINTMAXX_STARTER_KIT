import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
  Share,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { Audio } from 'expo-av';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import ConfettiCannon from 'react-native-confetti-cannon';
import { getTodayVerse, Verse } from '../../src/lib/verses';

const { width, height } = Dimensions.get('window');

interface CheckInState {
  read_verse: boolean;
  prayed: boolean;
  shared: boolean;
}

interface UserStats {
  streak_count: number;
  total_verses_read: number;
  total_prayers: number;
  total_shares: number;
  last_check_in: string | null;
}

const STORAGE_KEYS = {
  CHECK_IN: 'scripture_streak_checkin_',
  STATS: 'scripture_streak_stats',
};

export default function TodayScreen() {
  const [todayVerse, setTodayVerse] = useState<Verse | null>(null);
  const [checkIn, setCheckIn] = useState<CheckInState>({
    read_verse: false,
    prayed: false,
    shared: false,
  });
  const [stats, setStats] = useState<UserStats>({
    streak_count: 0,
    total_verses_read: 0,
    total_prayers: 0,
    total_shares: 0,
    last_check_in: null,
  });
  const [showConfetti, setShowConfetti] = useState(false);
  const [justCompleted, setJustCompleted] = useState(false);
  
  // Animation refs
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const streakAnim = useRef(new Animated.Value(0)).current;
  const taskAnims = useRef([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]).current;
  const confettiRef = useRef<any>(null);

  const getTodayKey = () => {
    const today = new Date().toISOString().split('T')[0];
    return STORAGE_KEYS.CHECK_IN + today;
  };

  // Play completion sound (optional - works without sound files)
  const playSound = async (type: 'check' | 'complete') => {
    // Sounds are optional - app works without them
    // To add sounds: place check.mp3 and complete.mp3 in assets/sounds/
    // Then uncomment the code below:
    /*
    try {
      const soundFile = type === 'complete' 
        ? require('../../assets/sounds/complete.mp3')
        : require('../../assets/sounds/check.mp3');
      
      const { sound } = await Audio.Sound.createAsync(soundFile);
      await sound.playAsync();
      sound.setOnPlaybackStatusUpdate((status) => {
        if (status.isLoaded && status.didJustFinish) {
          sound.unloadAsync();
        }
      });
    } catch (e) {
      console.log('Sound not available');
    }
    */
  };

  // Load data on mount
  useEffect(() => {
    setTodayVerse(getTodayVerse());
    loadData();
    
    // Staggered task card animations
    taskAnims.forEach((anim, index) => {
      Animated.timing(anim, {
        toValue: 1,
        duration: 400,
        delay: 100 + index * 100,
        useNativeDriver: true,
      }).start();
    });
  }, []);

  const loadData = async () => {
    try {
      const checkInData = await AsyncStorage.getItem(getTodayKey());
      if (checkInData) {
        setCheckIn(JSON.parse(checkInData));
      }

      const statsData = await AsyncStorage.getItem(STORAGE_KEYS.STATS);
      if (statsData) {
        setStats(JSON.parse(statsData));
      }
    } catch (e) {
      console.log('Error loading data:', e);
    }
  };

  // Animate streak counter
  useEffect(() => {
    Animated.spring(streakAnim, {
      toValue: 1,
      tension: 50,
      friction: 7,
      useNativeDriver: true,
    }).start();
  }, [stats.streak_count]);

  const allTasksComplete = checkIn.read_verse && checkIn.prayed && checkIn.shared;

  // Celebrate when all tasks done
  useEffect(() => {
    if (allTasksComplete && !justCompleted) {
      setJustCompleted(true);
      setShowConfetti(true);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      playSound('complete');
      
      // Fire confetti
      if (confettiRef.current) {
        confettiRef.current.start();
      }
      
      Animated.sequence([
        Animated.timing(scaleAnim, { toValue: 1.15, duration: 200, useNativeDriver: true }),
        Animated.spring(scaleAnim, { toValue: 1, tension: 100, friction: 5, useNativeDriver: true }),
      ]).start();
      
      // Hide confetti after animation
      setTimeout(() => setShowConfetti(false), 4000);
    }
  }, [allTasksComplete]);

  const handleTaskPress = async (taskId: keyof CheckInState, index: number) => {
    const newValue = !checkIn[taskId];
    const newCheckIn = { ...checkIn, [taskId]: newValue };
    
    // Haptic + sound feedback
    if (newValue) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
      playSound('check');
      
      // Bounce animation on the task
      Animated.sequence([
        Animated.timing(taskAnims[index], { toValue: 1.05, duration: 100, useNativeDriver: true }),
        Animated.spring(taskAnims[index], { toValue: 1, tension: 100, friction: 5, useNativeDriver: true }),
      ]).start();
    } else {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    
    setCheckIn(newCheckIn);
    await AsyncStorage.setItem(getTodayKey(), JSON.stringify(newCheckIn));
    
    // Update stats
    const newStats = { ...stats };
    const today = new Date().toISOString().split('T')[0];
    
    if (newValue) {
      if (taskId === 'read_verse') newStats.total_verses_read++;
      if (taskId === 'prayed') newStats.total_prayers++;
      if (taskId === 'shared') newStats.total_shares++;
    }
    
    // Check if all tasks now complete - update streak
    const allDone = newCheckIn.read_verse && newCheckIn.prayed && newCheckIn.shared;
    if (allDone && stats.last_check_in !== today) {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];
      
      if (stats.last_check_in === yesterdayStr) {
        newStats.streak_count++;
      } else if (!stats.last_check_in || stats.last_check_in < yesterdayStr) {
        newStats.streak_count = 1;
      }
      newStats.last_check_in = today;
    }
    
    setStats(newStats);
    await AsyncStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(newStats));
  };

  const handleShare = async () => {
    if (!todayVerse) return;
    
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    
    try {
      await Share.share({
        message: `"${todayVerse.text}"\n\n— ${todayVerse.reference}\n\n📖 Scripture Streak App`,
      });
      
      if (!checkIn.shared) {
        handleTaskPress('shared', 2);
      }
    } catch (error) {
      console.log('Share error:', error);
    }
  };

  const completedCount = [checkIn.read_verse, checkIn.prayed, checkIn.shared].filter(Boolean).length;

  const tasks = [
    { 
      id: 'read_verse' as const, 
      icon: 'book-outline' as const,
      iconComplete: 'book' as const,
      title: "Read Today's Verse", 
      subtitle: "Meditate on God's Word",
      color: '#60a5fa',
    },
    { 
      id: 'prayed' as const, 
      icon: 'heart-outline' as const,
      iconComplete: 'heart' as const,
      title: 'Pray', 
      subtitle: 'Spend time with God',
      color: '#f472b6',
    },
    { 
      id: 'shared' as const, 
      icon: 'share-social-outline' as const,
      iconComplete: 'share-social' as const,
      title: 'Share Your Faith', 
      subtitle: "Share today's verse",
      color: '#34d399',
    },
  ];

  return (
    <LinearGradient
      colors={['#1a1a2e', '#16213e', '#0f0f23']}
      style={styles.container}
    >
      {/* Confetti */}
      {showConfetti && (
        <ConfettiCannon
          ref={confettiRef}
          count={150}
          origin={{ x: width / 2, y: -20 }}
          fadeOut
          explosionSpeed={400}
          fallSpeed={2500}
          colors={['#e94560', '#4ade80', '#60a5fa', '#f472b6', '#fbbf24']}
        />
      )}
      
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header with streak */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good {getTimeOfDay()}</Text>
            <Text style={styles.subGreeting}>Let's grow in faith today</Text>
          </View>
          <Animated.View
            style={[
              styles.streakContainer,
              {
                transform: [
                  { scale: scaleAnim },
                  {
                    scale: streakAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [0.5, 1],
                    }),
                  },
                ],
              },
            ]}
          >
            <Ionicons name="flame" size={28} color="#e94560" />
            <Text style={styles.streakCount}>{stats.streak_count}</Text>
            <Text style={styles.streakLabel}>Day Streak</Text>
          </Animated.View>
        </View>

        {/* Progress ring */}
        <View style={styles.progressContainer}>
          <View style={styles.progressOuter}>
            <View style={[styles.progressSegment, completedCount >= 1 && styles.progressSegmentFilled, { transform: [{ rotate: '0deg' }] }]} />
            <View style={[styles.progressSegment, completedCount >= 2 && styles.progressSegmentFilled, { transform: [{ rotate: '120deg' }] }]} />
            <View style={[styles.progressSegment, completedCount >= 3 && styles.progressSegmentFilled, { transform: [{ rotate: '240deg' }] }]} />
            <View style={styles.progressInner}>
              <Text style={styles.progressText}>{completedCount}/3</Text>
              <Text style={styles.progressLabel}>Tasks</Text>
            </View>
          </View>
        </View>

        {/* Today's verse card */}
        {todayVerse && (
          <Animated.View style={styles.verseCard}>
            <View style={styles.verseIconContainer}>
              <Ionicons name="book" size={24} color="#e94560" />
            </View>
            <View style={styles.verseHeader}>
              <View style={styles.themeBadge}>
                <Text style={styles.verseTheme}>{todayVerse.theme.toUpperCase()}</Text>
              </View>
              <Text style={styles.verseReference}>{todayVerse.reference}</Text>
            </View>
            <Text style={styles.verseText}>"{todayVerse.text}"</Text>
            <TouchableOpacity style={styles.shareButton} onPress={handleShare} activeOpacity={0.8}>
              <LinearGradient
                colors={['#e94560', '#c23a51']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={styles.shareGradient}
              >
                <Ionicons name="share-social" size={20} color="#ffffff" />
                <Text style={styles.shareText}>Share Verse</Text>
              </LinearGradient>
            </TouchableOpacity>
          </Animated.View>
        )}

        {/* Tasks */}
        <Text style={styles.tasksTitle}>Today's Tasks</Text>
        <View style={styles.tasksContainer}>
          {tasks.map((task, index) => {
            const isComplete = checkIn[task.id];
            return (
              <Animated.View
                key={task.id}
                style={{
                  opacity: taskAnims[index],
                  transform: [
                    {
                      translateY: taskAnims[index].interpolate({
                        inputRange: [0, 1],
                        outputRange: [30, 0],
                      }),
                    },
                    { scale: taskAnims[index] },
                  ],
                }}
              >
                <TouchableOpacity
                  style={[styles.taskCard, isComplete && styles.taskCardComplete]}
                  onPress={() => handleTaskPress(task.id, index)}
                  activeOpacity={0.7}
                >
                  <View style={styles.taskLeft}>
                    <View style={[styles.taskIconContainer, { backgroundColor: task.color + '20' }]}>
                      <Ionicons 
                        name={isComplete ? task.iconComplete : task.icon} 
                        size={26} 
                        color={isComplete ? '#4ade80' : task.color} 
                      />
                    </View>
                    <View style={styles.taskTextContainer}>
                      <Text style={[styles.taskTitle, isComplete && styles.taskTitleComplete]}>
                        {task.title}
                      </Text>
                      <Text style={styles.taskSubtitle}>{task.subtitle}</Text>
                    </View>
                  </View>
                  <View style={[styles.taskCheck, isComplete && styles.taskCheckComplete]}>
                    {isComplete && <Ionicons name="checkmark" size={18} color="#ffffff" />}
                  </View>
                </TouchableOpacity>
              </Animated.View>
            );
          })}
        </View>

        {/* Completion message */}
        {allTasksComplete && (
          <Animated.View 
            style={[
              styles.completionCard,
              { transform: [{ scale: scaleAnim }] }
            ]}
          >
            <View style={styles.completionIconContainer}>
              <Ionicons name="trophy" size={48} color="#fbbf24" />
            </View>
            <Text style={styles.completionTitle}>Day Complete!</Text>
            <Text style={styles.completionText}>
              You've completed all your spiritual disciplines for today.
              Your streak is now {stats.streak_count} {stats.streak_count === 1 ? 'day' : 'days'}!
            </Text>
            <View style={styles.completionStats}>
              <View style={styles.completionStat}>
                <Ionicons name="book" size={20} color="#60a5fa" />
                <Text style={styles.completionStatText}>{stats.total_verses_read}</Text>
              </View>
              <View style={styles.completionStat}>
                <Ionicons name="heart" size={20} color="#f472b6" />
                <Text style={styles.completionStatText}>{stats.total_prayers}</Text>
              </View>
              <View style={styles.completionStat}>
                <Ionicons name="share-social" size={20} color="#34d399" />
                <Text style={styles.completionStatText}>{stats.total_shares}</Text>
              </View>
            </View>
          </Animated.View>
        )}
      </ScrollView>
    </LinearGradient>
  );
}

function getTimeOfDay(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Morning';
  if (hour < 17) return 'Afternoon';
  return 'Evening';
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
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 28,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '800',
    color: '#ffffff',
  },
  subGreeting: {
    fontSize: 15,
    color: '#ffffff60',
    marginTop: 4,
  },
  streakContainer: {
    alignItems: 'center',
    backgroundColor: '#e9456015',
    borderRadius: 20,
    padding: 14,
    borderWidth: 2,
    borderColor: '#e9456030',
    minWidth: 80,
  },
  streakCount: {
    fontSize: 26,
    fontWeight: '900',
    color: '#e94560',
    marginTop: 2,
  },
  streakLabel: {
    fontSize: 10,
    color: '#ffffff60',
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  progressContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  progressOuter: {
    width: 130,
    height: 130,
    borderRadius: 65,
    backgroundColor: '#ffffff08',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  progressSegment: {
    position: 'absolute',
    width: 130,
    height: 130,
    borderRadius: 65,
    borderWidth: 6,
    borderColor: '#ffffff15',
    borderTopColor: 'transparent',
    borderRightColor: 'transparent',
  },
  progressSegmentFilled: {
    borderColor: '#e94560',
    borderTopColor: 'transparent',
    borderRightColor: 'transparent',
  },
  progressInner: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#1a1a2e',
    justifyContent: 'center',
    alignItems: 'center',
  },
  progressText: {
    fontSize: 32,
    fontWeight: '900',
    color: '#ffffff',
  },
  progressLabel: {
    fontSize: 12,
    color: '#ffffff50',
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  verseCard: {
    backgroundColor: '#ffffff08',
    borderRadius: 24,
    padding: 24,
    marginBottom: 32,
    borderWidth: 1,
    borderColor: '#ffffff10',
    position: 'relative',
    overflow: 'hidden',
  },
  verseIconContainer: {
    position: 'absolute',
    top: 16,
    right: 16,
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#e9456015',
    justifyContent: 'center',
    alignItems: 'center',
  },
  verseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 12,
  },
  themeBadge: {
    backgroundColor: '#e9456020',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
  },
  verseTheme: {
    fontSize: 10,
    color: '#e94560',
    fontWeight: '800',
    letterSpacing: 1,
  },
  verseReference: {
    fontSize: 14,
    color: '#ffffff60',
    fontWeight: '600',
  },
  verseText: {
    fontSize: 20,
    color: '#ffffff',
    fontStyle: 'italic',
    lineHeight: 32,
    marginBottom: 24,
    paddingRight: 40,
  },
  shareButton: {
    borderRadius: 14,
    overflow: 'hidden',
  },
  shareGradient: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 16,
    gap: 10,
  },
  shareText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  tasksTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#ffffff',
    marginBottom: 16,
  },
  tasksContainer: {
    gap: 14,
  },
  taskCard: {
    backgroundColor: '#ffffff08',
    borderRadius: 18,
    padding: 18,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  taskCardComplete: {
    backgroundColor: '#4ade8010',
    borderColor: '#4ade8030',
  },
  taskLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    flex: 1,
  },
  taskIconContainer: {
    width: 52,
    height: 52,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  taskTextContainer: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 3,
  },
  taskTitleComplete: {
    textDecorationLine: 'line-through',
    color: '#ffffff50',
  },
  taskSubtitle: {
    fontSize: 13,
    color: '#ffffff50',
  },
  taskCheck: {
    width: 30,
    height: 30,
    borderRadius: 15,
    borderWidth: 2,
    borderColor: '#ffffff25',
    justifyContent: 'center',
    alignItems: 'center',
  },
  taskCheckComplete: {
    backgroundColor: '#4ade80',
    borderColor: '#4ade80',
  },
  completionCard: {
    backgroundColor: '#4ade8010',
    borderRadius: 24,
    padding: 28,
    alignItems: 'center',
    marginTop: 24,
    borderWidth: 2,
    borderColor: '#4ade8025',
  },
  completionIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#fbbf2415',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  completionTitle: {
    fontSize: 26,
    fontWeight: '900',
    color: '#4ade80',
    marginBottom: 10,
  },
  completionText: {
    fontSize: 15,
    color: '#ffffff70',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 20,
  },
  completionStats: {
    flexDirection: 'row',
    gap: 24,
  },
  completionStat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  completionStatText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff80',
  },
});
