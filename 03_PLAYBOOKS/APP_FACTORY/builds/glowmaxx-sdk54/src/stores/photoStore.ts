import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ProgressPhoto } from '../types';
import { STORAGE_KEYS } from '../utils/constants';
import { getTodayDateString } from '../utils/dateUtils';

interface PhotoStore {
  photos: ProgressPhoto[];
  addPhoto: (photo: Omit<ProgressPhoto, 'id'>) => void;
  deletePhoto: (photoId: string) => void;
  getPhotosByDate: (date: string) => ProgressPhoto[];
  getPhotosByAngle: (angle: ProgressPhoto['angle']) => ProgressPhoto[];
  getLatestPhotos: () => { front?: ProgressPhoto; left?: ProgressPhoto; right?: ProgressPhoto; below?: ProgressPhoto };
  getTotalPhotoCount: () => number;
  getWeeklyPhotoCount: () => number;
}

export const usePhotoStore = create<PhotoStore>()(
  persist(
    (set, get) => ({
      photos: [],

      addPhoto: (photoData) => {
        const newPhoto: ProgressPhoto = {
          ...photoData,
          id: Date.now().toString(),
        };
        set((state) => ({
          photos: [...state.photos, newPhoto],
        }));
      },

      deletePhoto: (photoId) => {
        set((state) => ({
          photos: state.photos.filter((p) => p.id !== photoId),
        }));
      },

      getPhotosByDate: (date) => {
        return get().photos.filter((p) => p.date === date);
      },

      getPhotosByAngle: (angle) => {
        return get()
          .photos.filter((p) => p.angle === angle)
          .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      },

      getLatestPhotos: () => {
        const { photos } = get();
        const latest: {
          front?: ProgressPhoto;
          left?: ProgressPhoto;
          right?: ProgressPhoto;
          below?: ProgressPhoto;
        } = {};

        // Sort by date descending
        const sorted = [...photos].sort(
          (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
        );

        for (const photo of sorted) {
          if (!latest[photo.angle]) {
            latest[photo.angle] = photo;
          }
          // Stop when all angles are found
          if (latest.front && latest.left && latest.right && latest.below) {
            break;
          }
        }

        return latest;
      },

      getTotalPhotoCount: () => {
        return get().photos.length;
      },

      getWeeklyPhotoCount: () => {
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        const oneWeekAgoString = oneWeekAgo.toISOString().split('T')[0];

        return get().photos.filter((p) => p.date >= oneWeekAgoString).length;
      },
    }),
    {
      name: STORAGE_KEYS.PROGRESS_PHOTOS,
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
