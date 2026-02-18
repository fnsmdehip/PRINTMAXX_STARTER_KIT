import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Modal,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import { useUserStore } from '../../src/stores/userStore';
import { GUIDE_SECTIONS, getGuidesByCategory } from '../../src/data/guides';
import { GuideSection } from '../../src/types';
import { COLORS } from '../../src/utils/constants';

type Category = GuideSection['category'];

const CATEGORIES: { id: Category; label: string; icon: keyof typeof Ionicons.glyphMap }[] = [
  { id: 'mewing', label: 'Mewing', icon: 'happy-outline' },
  { id: 'softmaxxing', label: 'Softmaxxing', icon: 'sparkles-outline' },
  { id: 'skincare', label: 'Skincare', icon: 'water-outline' },
  { id: 'debloating', label: 'Debloating', icon: 'fitness-outline' },
  { id: 'leanmaxxing', label: 'Leanmaxxing', icon: 'barbell-outline' },
  { id: 'hardmaxxing', label: 'Hardmaxxing', icon: 'construct-outline' },
];

export default function LearnScreen() {
  const [selectedCategory, setSelectedCategory] = useState<Category>('mewing');
  const [selectedGuide, setSelectedGuide] = useState<GuideSection | null>(null);

  const { subscription } = useUserStore();
  const canAccessPremium = subscription.isSubscribed || subscription.isInTrial;

  const guides = getGuidesByCategory(selectedCategory);

  const handleGuidePress = (guide: GuideSection) => {
    if (guide.isPremium && !canAccessPremium) {
      router.push('/paywall');
      return;
    }
    setSelectedGuide(guide);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Learn</Text>
        <Text style={styles.subtitle}>Master the fundamentals</Text>
      </View>

      {/* Category tabs */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.categoryScroll}
        contentContainerStyle={styles.categoryContent}
      >
        {CATEGORIES.map((cat) => (
          <TouchableOpacity
            key={cat.id}
            style={[
              styles.categoryTab,
              selectedCategory === cat.id && styles.categoryTabActive,
            ]}
            onPress={() => setSelectedCategory(cat.id)}
          >
            <Ionicons
              name={cat.icon}
              size={18}
              color={selectedCategory === cat.id ? COLORS.surface : COLORS.textSecondary}
            />
            <Text
              style={[
                styles.categoryText,
                selectedCategory === cat.id && styles.categoryTextActive,
              ]}
            >
              {cat.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Guides list */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {guides.map((guide) => (
          <TouchableOpacity
            key={guide.id}
            style={styles.guideCard}
            onPress={() => handleGuidePress(guide)}
          >
            <View style={styles.guideHeader}>
              <Text style={styles.guideTitle}>{guide.title}</Text>
              {guide.isPremium && !canAccessPremium && (
                <View style={styles.premiumBadge}>
                  <Ionicons name="lock-closed" size={12} color={COLORS.surface} />
                  <Text style={styles.premiumText}>PRO</Text>
                </View>
              )}
            </View>
            <Text style={styles.guidePreview} numberOfLines={2}>
              {guide.content.substring(0, 100)}...
            </Text>
            <View style={styles.guideFooter}>
              <Text style={styles.readMore}>Read more</Text>
              <Ionicons name="arrow-forward" size={16} color={COLORS.primary} />
            </View>
          </TouchableOpacity>
        ))}

        {/* Affiliate callout for premium content */}
        {selectedCategory === 'skincare' && (
          <View style={styles.affiliateCard}>
            <Text style={styles.affiliateTitle}>Recommended Products</Text>
            <Text style={styles.affiliateText}>
              Get the skincare products we recommend for best results.
            </Text>
            <TouchableOpacity style={styles.affiliateButton}>
              <Text style={styles.affiliateButtonText}>View Recommendations</Text>
              <Ionicons name="open-outline" size={16} color={COLORS.primary} />
            </TouchableOpacity>
          </View>
        )}

        {selectedCategory === 'leanmaxxing' && (
          <View style={styles.affiliateCard}>
            <Text style={styles.affiliateTitle}>Supplement Stack</Text>
            <Text style={styles.affiliateText}>
              Supplements that support fat loss and facial definition.
            </Text>
            <TouchableOpacity style={styles.affiliateButton}>
              <Text style={styles.affiliateButtonText}>View Supplements</Text>
              <Ionicons name="open-outline" size={16} color={COLORS.primary} />
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* Guide Modal */}
      <Modal
        visible={!!selectedGuide}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={() => setSelectedGuide(null)}
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setSelectedGuide(null)}
            >
              <Ionicons name="close" size={28} color={COLORS.text} />
            </TouchableOpacity>
            <Text style={styles.modalTitle}>{selectedGuide?.title}</Text>
          </View>
          <ScrollView
            style={styles.modalContent}
            contentContainerStyle={styles.modalContentContainer}
          >
            <Text style={styles.modalBody}>{selectedGuide?.content}</Text>
          </ScrollView>
        </SafeAreaView>
      </Modal>
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
  categoryScroll: {
    maxHeight: 50,
    marginBottom: 16,
  },
  categoryContent: {
    paddingHorizontal: 20,
    gap: 8,
  },
  categoryTab: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    gap: 6,
  },
  categoryTabActive: {
    backgroundColor: COLORS.primary,
  },
  categoryText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.textSecondary,
  },
  categoryTextActive: {
    color: COLORS.surface,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 40,
  },
  guideCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
  },
  guideHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  guideTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.text,
    flex: 1,
    marginRight: 8,
  },
  premiumBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.secondary,
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 12,
    gap: 4,
  },
  premiumText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: COLORS.surface,
  },
  guidePreview: {
    fontSize: 14,
    color: COLORS.textSecondary,
    lineHeight: 20,
    marginBottom: 12,
  },
  guideFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  readMore: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  affiliateCard: {
    backgroundColor: COLORS.primaryLight,
    borderRadius: 16,
    padding: 16,
    marginTop: 8,
  },
  affiliateTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  affiliateText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  affiliateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  affiliateButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  modalClose: {
    marginRight: 16,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    flex: 1,
  },
  modalContent: {
    flex: 1,
  },
  modalContentContainer: {
    padding: 20,
  },
  modalBody: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 26,
  },
});
