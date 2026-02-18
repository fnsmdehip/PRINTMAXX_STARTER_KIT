import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Dimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { ProgressPhoto } from '../types';
import { COLORS, PHOTO_ANGLES } from '../utils/constants';
import { formatDate } from '../utils/dateUtils';

interface PhotoCompareProps {
  photos: ProgressPhoto[];
  onAddPhoto: (angle: ProgressPhoto['angle']) => void;
}

const { width } = Dimensions.get('window');
const PHOTO_SIZE = (width - 64) / 2;

export function PhotoCompare({ photos, onAddPhoto }: PhotoCompareProps) {
  const [selectedAngle, setSelectedAngle] = useState<ProgressPhoto['angle']>('front');

  const filteredPhotos = photos
    .filter((p) => p.angle === selectedAngle)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  const latestPhoto = filteredPhotos[0];
  const oldestPhoto = filteredPhotos.length > 1 ? filteredPhotos[filteredPhotos.length - 1] : null;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Progress Photos</Text>
      <Text style={styles.subtitle}>
        Compare your transformation over time
      </Text>

      {/* Angle selector */}
      <View style={styles.angleSelector}>
        {PHOTO_ANGLES.map((angle) => (
          <TouchableOpacity
            key={angle.id}
            style={[
              styles.angleButton,
              selectedAngle === angle.id && styles.angleButtonActive,
            ]}
            onPress={() => setSelectedAngle(angle.id as ProgressPhoto['angle'])}
          >
            <Text
              style={[
                styles.angleText,
                selectedAngle === angle.id && styles.angleTextActive,
              ]}
            >
              {angle.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Photo comparison */}
      <View style={styles.photoGrid}>
        {/* Before (oldest) */}
        <View style={styles.photoContainer}>
          <Text style={styles.photoLabel}>Before</Text>
          {oldestPhoto ? (
            <Image source={{ uri: oldestPhoto.uri }} style={styles.photo} />
          ) : (
            <View style={styles.photoPlaceholder}>
              <Ionicons name="image-outline" size={32} color={COLORS.textLight} />
              <Text style={styles.placeholderText}>
                {filteredPhotos.length === 0 ? 'No photos yet' : 'Need 2+ photos'}
              </Text>
            </View>
          )}
          {oldestPhoto && (
            <Text style={styles.photoDate}>{formatDate(oldestPhoto.date)}</Text>
          )}
        </View>

        {/* After (latest) */}
        <View style={styles.photoContainer}>
          <Text style={styles.photoLabel}>After</Text>
          {latestPhoto ? (
            <Image source={{ uri: latestPhoto.uri }} style={styles.photo} />
          ) : (
            <TouchableOpacity
              style={styles.photoPlaceholder}
              onPress={() => onAddPhoto(selectedAngle)}
            >
              <Ionicons name="camera-outline" size={32} color={COLORS.primary} />
              <Text style={[styles.placeholderText, { color: COLORS.primary }]}>
                Take photo
              </Text>
            </TouchableOpacity>
          )}
          {latestPhoto && (
            <Text style={styles.photoDate}>{formatDate(latestPhoto.date)}</Text>
          )}
        </View>
      </View>

      {/* Add photo button */}
      <TouchableOpacity
        style={styles.addButton}
        onPress={() => onAddPhoto(selectedAngle)}
      >
        <Ionicons name="camera" size={20} color={COLORS.surface} />
        <Text style={styles.addButtonText}>Take New Progress Photo</Text>
      </TouchableOpacity>

      {/* Tip */}
      <View style={styles.tipContainer}>
        <Ionicons name="bulb-outline" size={16} color={COLORS.warning} />
        <Text style={styles.tipText}>
          For best comparison: same lighting, same angle, same distance from camera
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 16,
  },
  angleSelector: {
    flexDirection: 'row',
    marginBottom: 16,
    gap: 8,
  },
  angleButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: COLORS.background,
    alignItems: 'center',
  },
  angleButtonActive: {
    backgroundColor: COLORS.primary,
  },
  angleText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  angleTextActive: {
    color: COLORS.surface,
  },
  photoGrid: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  photoContainer: {
    flex: 1,
    alignItems: 'center',
  },
  photoLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  photo: {
    width: PHOTO_SIZE,
    height: PHOTO_SIZE,
    borderRadius: 12,
    backgroundColor: COLORS.background,
  },
  photoPlaceholder: {
    width: PHOTO_SIZE,
    height: PHOTO_SIZE,
    borderRadius: 12,
    backgroundColor: COLORS.background,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
  },
  placeholderText: {
    fontSize: 12,
    color: COLORS.textLight,
    marginTop: 8,
  },
  photoDate: {
    fontSize: 11,
    color: COLORS.textSecondary,
    marginTop: 6,
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    padding: 14,
    borderRadius: 12,
    gap: 8,
    marginBottom: 12,
  },
  addButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.surface,
  },
  tipContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#FFF8E1',
    padding: 12,
    borderRadius: 12,
    gap: 8,
  },
  tipText: {
    flex: 1,
    fontSize: 12,
    color: COLORS.text,
    lineHeight: 16,
  },
});
