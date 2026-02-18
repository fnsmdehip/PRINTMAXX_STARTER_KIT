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
import SearchBar from '../components/SearchBar';
import CategoryChips from '../components/CategoryChip';
import PromptCard from '../components/PromptCard';
import Toast from '../components/Toast';
import CreatePromptModal from '../components/CreatePromptModal';
import AdBanner, { trackCategorySwitch } from '../components/AdBanner';
import { usePromptStore } from '../stores/promptStore';
import { useSubscriptionStore } from '../stores/subscriptionStore';
import { colors, spacing, fontSize } from '../utils/theme';
import { Prompt } from '../types';

type RootStackParamList = {
  Home: undefined;
  PromptDetail: { promptId: string };
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'Home'>;

export default function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const {
    filteredPrompts,
    selectedCategory,
    searchQuery,
    setSelectedCategory,
    setSearchQuery,
  } = usePromptStore();
  const { isPro } = useSubscriptionStore();

  const [toastVisible, setToastVisible] = useState(false);
  const [createModalVisible, setCreateModalVisible] = useState(false);

  // Track category switches for interstitial ads (free users only)
  const handleCategorySelect = useCallback((category: string | null) => {
    setSelectedCategory(category);

    // Check if we should show an interstitial ad
    const shouldShowAd = trackCategorySwitch(isPro);
    if (shouldShowAd) {
      // TODO: When react-native-google-mobile-ads is installed,
      // show interstitial here using the useFreemiumInterstitial hook
      console.log('Would show interstitial ad here');
    }
  }, [isPro, setSelectedCategory]);

  const showCopySuccess = useCallback(() => {
    setToastVisible(true);
  }, []);

  const handlePromptPress = (prompt: Prompt) => {
    navigation.navigate('PromptDetail', { promptId: prompt.id });
  };

  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.titleRow}>
        <View>
          <Text style={styles.title}>PromptVault</Text>
          <Text style={styles.subtitle}>
            {filteredPrompts.length} prompts available
          </Text>
        </View>
        <TouchableOpacity
          style={styles.addButton}
          onPress={() => setCreateModalVisible(true)}
        >
          <MaterialCommunityIcons name="plus" size={24} color={colors.text} />
        </TouchableOpacity>
      </View>

      <SearchBar value={searchQuery} onChangeText={setSearchQuery} />

      <CategoryChips
        selectedCategory={selectedCategory}
        onSelectCategory={handleCategorySelect}
      />
    </View>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <MaterialCommunityIcons
        name="file-search-outline"
        size={64}
        color={colors.textMuted}
      />
      <Text style={styles.emptyTitle}>No prompts found</Text>
      <Text style={styles.emptyText}>
        Try adjusting your search or category filter
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
        data={filteredPrompts}
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

      <CreatePromptModal
        visible={createModalVisible}
        onClose={() => setCreateModalVisible(false)}
      />

      {/* Ad banner for free users - shows at bottom of screen */}
      <AdBanner />
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
    marginBottom: spacing.md,
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: spacing.md,
    marginBottom: spacing.md,
  },
  title: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
  },
  subtitle: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    marginTop: 2,
  },
  addButton: {
    backgroundColor: colors.primary,
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
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
  },
});
