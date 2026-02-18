import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import PromptCard from '../components/PromptCard';
import Toast from '../components/Toast';
import { usePromptStore } from '../stores/promptStore';
import { useFavoriteStore } from '../stores/favoriteStore';
import { colors, spacing, fontSize, borderRadius } from '../utils/theme';
import { Prompt } from '../types';

type RootStackParamList = {
  Favorites: undefined;
  PromptDetail: { promptId: string };
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'Favorites'>;

export default function FavoritesScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { prompts } = usePromptStore();
  const { favoriteIds, clearAllFavorites } = useFavoriteStore();

  const [toastVisible, setToastVisible] = useState(false);

  const favoritePrompts = prompts.filter((p) => favoriteIds.includes(p.id));

  const showCopySuccess = useCallback(() => {
    setToastVisible(true);
  }, []);

  const handlePromptPress = (prompt: Prompt) => {
    navigation.navigate('PromptDetail', { promptId: prompt.id });
  };

  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.titleRow}>
        <Text style={styles.title}>Favorites</Text>
        <Text style={styles.count}>{favoritePrompts.length}</Text>
      </View>
      {favoritePrompts.length > 0 && (
        <TouchableOpacity
          style={styles.clearButton}
          onPress={clearAllFavorites}
        >
          <MaterialCommunityIcons
            name="delete-outline"
            size={20}
            color={colors.error}
          />
          <Text style={styles.clearText}>Clear All</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <MaterialCommunityIcons
        name="heart-outline"
        size={64}
        color={colors.textMuted}
      />
      <Text style={styles.emptyTitle}>No favorites yet</Text>
      <Text style={styles.emptyText}>
        Tap the heart icon on any prompt to save it here for quick access.
      </Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <Toast
        visible={toastVisible}
        message="Copied to clipboard"
        type="success"
        onHide={() => setToastVisible(false)}
      />

      <FlatList
        data={favoritePrompts}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <PromptCard
            prompt={item}
            onPress={() => handlePromptPress(item)}
            showCopySuccess={showCopySuccess}
          />
        )}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={renderEmpty}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingTop: spacing.md,
    marginBottom: spacing.lg,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
  },
  count: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.textMuted,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  clearButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  clearText: {
    fontSize: fontSize.sm,
    color: colors.error,
  },
  listContent: {
    paddingHorizontal: spacing.md,
    paddingBottom: spacing.xxl,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingTop: spacing.xxl,
    paddingHorizontal: spacing.xl,
  },
  emptyTitle: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.text,
    marginTop: spacing.md,
  },
  emptyText: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
    marginTop: spacing.sm,
    lineHeight: 22,
  },
});
