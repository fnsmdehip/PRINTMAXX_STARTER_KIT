import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import * as Haptics from 'expo-haptics';

import { usePhotoStore } from '../../src/stores/photoStore';
import { useUserStore } from '../../src/stores/userStore';
import { PhotoCompare } from '../../src/components/PhotoCompare';
import { ProgressPhoto } from '../../src/types';
import { COLORS, PHOTO_ANGLES } from '../../src/utils/constants';
import { getTodayDateString, formatDate, getDaysAgoString } from '../../src/utils/dateUtils';

export default function ProgressScreen() {
  const { photos, addPhoto, getTotalPhotoCount, getWeeklyPhotoCount, getPhotosByAngle } =
    usePhotoStore();
  const { streak } = useUserStore();

  const [showHistory, setShowHistory] = useState(false);

  const handleAddPhoto = async (angle: ProgressPhoto['angle']) => {
    const angleInfo = PHOTO_ANGLES.find((a) => a.id === angle);

    // Ask user to choose camera or library
    Alert.alert(
      'Add Progress Photo',
      angleInfo?.instruction || 'Take a photo',
      [
        {
          text: 'Camera',
          onPress: async () => {
            const { status } = await ImagePicker.requestCameraPermissionsAsync();
            if (status !== 'granted') {
              Alert.alert('Permission Required', 'Camera permission is needed to take photos.');
              return;
            }

            const result = await ImagePicker.launchCameraAsync({
              allowsEditing: true,
              aspect: [1, 1],
              quality: 0.8,
            });

            if (!result.canceled && result.assets[0]) {
              Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
              addPhoto({
                uri: result.assets[0].uri,
                date: getTodayDateString(),
                angle,
              });
            }
          },
        },
        {
          text: 'Library',
          onPress: async () => {
            const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
            if (status !== 'granted') {
              Alert.alert('Permission Required', 'Photo library permission is needed.');
              return;
            }

            const result = await ImagePicker.launchImageLibraryAsync({
              allowsEditing: true,
              aspect: [1, 1],
              quality: 0.8,
            });

            if (!result.canceled && result.assets[0]) {
              Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
              addPhoto({
                uri: result.assets[0].uri,
                date: getTodayDateString(),
                angle,
              });
            }
          },
        },
        { text: 'Cancel', style: 'cancel' },
      ]
    );
  };

  const totalPhotos = getTotalPhotoCount();
  const weeklyPhotos = getWeeklyPhotoCount();

  // Get photos grouped by date
  const photosByDate = photos.reduce((acc, photo) => {
    if (!acc[photo.date]) {
      acc[photo.date] = [];
    }
    acc[photo.date].push(photo);
    return acc;
  }, {} as Record<string, ProgressPhoto[]>);

  const sortedDates = Object.keys(photosByDate).sort(
    (a, b) => new Date(b).getTime() - new Date(a).getTime()
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Progress</Text>
        <Text style={styles.subtitle}>Track your transformation</Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Stats */}
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{totalPhotos}</Text>
            <Text style={styles.statLabel}>Total Photos</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{weeklyPhotos}</Text>
            <Text style={styles.statLabel}>This Week</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{streak.totalDaysCompleted}</Text>
            <Text style={styles.statLabel}>Days Tracked</Text>
          </View>
        </View>

        {/* Photo Comparison */}
        <PhotoCompare photos={photos} onAddPhoto={handleAddPhoto} />

        {/* Photo History Toggle */}
        <TouchableOpacity
          style={styles.historyToggle}
          onPress={() => setShowHistory(!showHistory)}
        >
          <Text style={styles.historyToggleText}>
            {showHistory ? 'Hide History' : 'Show Photo History'}
          </Text>
          <Ionicons
            name={showHistory ? 'chevron-up' : 'chevron-down'}
            size={20}
            color={COLORS.primary}
          />
        </TouchableOpacity>

        {/* Photo History */}
        {showHistory && (
          <View style={styles.historySection}>
            {sortedDates.length === 0 ? (
              <View style={styles.emptyState}>
                <Ionicons name="images-outline" size={48} color={COLORS.textLight} />
                <Text style={styles.emptyText}>No photos yet</Text>
                <Text style={styles.emptySubtext}>
                  Start taking progress photos to track your journey
                </Text>
              </View>
            ) : (
              sortedDates.map((date) => (
                <View key={date} style={styles.dateGroup}>
                  <Text style={styles.dateHeader}>{getDaysAgoString(date)}</Text>
                  <View style={styles.photoRow}>
                    {photosByDate[date].map((photo) => (
                      <View key={photo.id} style={styles.photoThumb}>
                        <Image source={{ uri: photo.uri }} style={styles.thumbImage} />
                        <Text style={styles.thumbLabel}>
                          {PHOTO_ANGLES.find((a) => a.id === photo.angle)?.label || photo.angle}
                        </Text>
                      </View>
                    ))}
                  </View>
                </View>
              ))
            )}
          </View>
        )}

        {/* Tips */}
        <View style={styles.tipsCard}>
          <View style={styles.tipsHeader}>
            <Ionicons name="bulb-outline" size={20} color={COLORS.warning} />
            <Text style={styles.tipsTitle}>Photo Tips</Text>
          </View>
          <View style={styles.tipsList}>
            <Text style={styles.tipItem}>
              - Same lighting every time (natural daylight is best)
            </Text>
            <Text style={styles.tipItem}>
              - Same distance from camera
            </Text>
            <Text style={styles.tipItem}>
              - Neutral expression, relaxed face
            </Text>
            <Text style={styles.tipItem}>
              - Take photos weekly at the same time
            </Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 40,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  statLabel: {
    fontSize: 11,
    color: COLORS.textSecondary,
    marginTop: 4,
    textAlign: 'center',
  },
  historyToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    gap: 8,
  },
  historyToggleText: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.primary,
  },
  historySection: {
    marginBottom: 20,
  },
  dateGroup: {
    marginBottom: 20,
  },
  dateHeader: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  photoRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  photoThumb: {
    alignItems: 'center',
  },
  thumbImage: {
    width: 80,
    height: 80,
    borderRadius: 8,
    backgroundColor: COLORS.border,
  },
  thumbLabel: {
    fontSize: 10,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginTop: 12,
  },
  emptySubtext: {
    fontSize: 13,
    color: COLORS.textLight,
    marginTop: 4,
    textAlign: 'center',
  },
  tipsCard: {
    backgroundColor: '#FFF8E1',
    borderRadius: 16,
    padding: 16,
  },
  tipsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  tipsList: {},
  tipItem: {
    fontSize: 13,
    color: COLORS.text,
    lineHeight: 22,
  },
});
