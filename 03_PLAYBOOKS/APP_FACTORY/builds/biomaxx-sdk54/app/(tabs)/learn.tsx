import React, { useState, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Modal,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useSubscriptionStore } from '../../src/stores/subscriptionStore';
import { AffiliateRecommendation } from '../../src/components';
import { COLORS, LEARN_ARTICLES } from '../../src/utils/constants';

const CATEGORIES = [
  'All',
  'Getting Started',
  'Protocol Deep-Dives',
  'Stacking Guide',
  'Science',
];

// Sample article content - in production this would come from a CMS
const ARTICLE_CONTENT: Record<string, { content: string; affiliateProduct?: any }> = {
  'getting-started': {
    content: `Welcome to your biohacking journey! This guide will help you understand the fundamentals of optimizing your biology.

The key principles:

1. Start with the basics - Sleep, nutrition, and movement form the foundation of all optimization.

2. Track consistently - You can't improve what you don't measure. Use this app to log your protocols daily.

3. Stack intelligently - Don't try everything at once. Add one protocol at a time and measure the impact.

4. Be patient - Biological change takes time. Give each protocol at least 2-4 weeks before judging results.

Your recommended starting stack:

Week 1-2: Focus on sleep optimization
- Set consistent sleep/wake times
- Get morning sunlight within 30 minutes of waking
- Avoid screens 1 hour before bed

Week 3-4: Add intermittent fasting
- Start with a 14-hour fast (8pm to 10am)
- Gradually extend to 16 hours
- Stay hydrated during fasting windows

Week 5-6: Introduce cold exposure
- Start with 30-second cold shower finishes
- Gradually increase duration
- Focus on controlled breathing

Track everything in this app and watch your longevity score climb!`,
    affiliateProduct: {
      title: 'WHOOP 4.0 Fitness Tracker',
      description: 'Track sleep, strain, and recovery with clinical-grade accuracy.',
      category: 'Sleep Tracking',
      price: '$30/month',
      icon: 'watch-outline',
    },
  },
  'fasting-101': {
    content: `Intermittent fasting (IF) is one of the most researched and accessible biohacking protocols.

What is intermittent fasting?

IF is simply restricting your eating to a specific window of time. The most popular method is 16:8 - fasting for 16 hours and eating within an 8-hour window.

Benefits backed by research:

- Improved insulin sensitivity
- Enhanced autophagy (cellular cleanup)
- Reduced inflammation
- Better mental clarity
- Potential longevity benefits

How to start:

1. Choose your eating window
Most people find 12pm-8pm works well. This means skipping breakfast but keeping lunch and dinner.

2. Stay hydrated
Black coffee, tea, and water are allowed during fasting. They don't break your fast.

3. Break your fast gently
Don't immediately eat a huge meal. Start with something light like nuts or a small salad.

4. Track your fasts
Use the fasting timer in this app to monitor your progress and build streaks.

Common mistakes to avoid:

- Eating too little during your eating window
- Not getting enough protein (aim for 1g per lb of body weight)
- Being too strict too fast - start with 14 hours and work up`,
    affiliateProduct: {
      title: 'LMNT Electrolytes',
      description: 'Stay hydrated and energized during fasts with zero sugar electrolytes.',
      category: 'Supplements',
      price: '$45/box',
      icon: 'water-outline',
    },
  },
  'cold-exposure': {
    content: `Cold exposure is a powerful hormetic stressor that triggers numerous beneficial adaptations.

The science:

When exposed to cold, your body activates brown fat (metabolically active fat that burns calories for heat), releases norepinephrine (improving mood and focus), and triggers cold shock proteins that have neuroprotective effects.

Methods:

1. Cold showers
The easiest starting point. End your shower with 30-60 seconds of the coldest water you can handle.

2. Ice baths
Fill a tub with cold water and add ice. Aim for 50-59°F (10-15°C). Start with 2 minutes and work up to 10-15 minutes.

3. Cold plunges
Purpose-built cold plunge tubs maintain consistent temperatures and are ideal for regular practice.

Protocol recommendations:

- Beginners: 30-second cold shower finishes, 3x per week
- Intermediate: 2-3 minute cold showers or ice baths, 5x per week
- Advanced: 5-10 minute ice baths, daily

Key tips:

- Focus on your breath - slow, controlled breathing
- Don't warm up artificially after - let your body heat itself
- Morning cold exposure can replace caffeine for some people
- Track your cold exposure in this app to build your streak`,
  },
};

export default function Learn() {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedArticle, setSelectedArticle] = useState<typeof LEARN_ARTICLES[0] | null>(null);
  const [showArticle, setShowArticle] = useState(false);

  const canAccessPremiumContent = useSubscriptionStore((state) => state.canAccessPremiumContent);
  const isPremium = canAccessPremiumContent();

  const filteredArticles = useMemo(() => {
    if (selectedCategory === 'All') {
      return LEARN_ARTICLES;
    }
    return LEARN_ARTICLES.filter((a) => a.category === selectedCategory);
  }, [selectedCategory]);

  const featuredArticle = useMemo(() => {
    return LEARN_ARTICLES.find((a) => a.featured);
  }, []);

  const handleArticlePress = (article: typeof LEARN_ARTICLES[0]) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);

    if (article.isPremium && !isPremium) {
      Alert.alert(
        'Premium Content',
        'Upgrade to Premium to access this article and all premium content.',
        [{ text: 'OK' }]
      );
      return;
    }

    setSelectedArticle(article);
    setShowArticle(true);
  };

  const renderArticleCard = (article: typeof LEARN_ARTICLES[0], isFeatured = false) => {
    const isLocked = article.isPremium && !isPremium;

    return (
      <TouchableOpacity
        key={article.id}
        style={[styles.articleCard, isFeatured && styles.featuredCard]}
        onPress={() => handleArticlePress(article)}
        activeOpacity={0.8}
      >
        {isFeatured && (
          <View style={styles.featuredBadge}>
            <Text style={styles.featuredBadgeText}>FEATURED</Text>
          </View>
        )}

        <View style={styles.articleContent}>
          <View style={styles.articleHeader}>
            <Text style={styles.articleCategory}>{article.category}</Text>
            {isLocked && (
              <View style={styles.lockBadge}>
                <Ionicons name="lock-closed" size={12} color={COLORS.accent} />
                <Text style={styles.lockBadgeText}>PRO</Text>
              </View>
            )}
          </View>

          <Text style={[styles.articleTitle, isFeatured && styles.featuredTitle]}>
            {article.title}
          </Text>

          <Text style={styles.articleExcerpt} numberOfLines={2}>
            {article.excerpt}
          </Text>

          <View style={styles.articleFooter}>
            <View style={styles.readTime}>
              <Ionicons name="time-outline" size={14} color={COLORS.textMuted} />
              <Text style={styles.readTimeText}>{article.readTime} min read</Text>
            </View>
            <Ionicons
              name="arrow-forward"
              size={16}
              color={isLocked ? COLORS.textMuted : COLORS.primary}
            />
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>Learn</Text>
        <Text style={styles.subtitle}>Evidence-based guides</Text>
      </View>

      {/* Category Filter */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.categoriesContainer}
      >
        {CATEGORIES.map((category) => (
          <TouchableOpacity
            key={category}
            style={[
              styles.categoryChip,
              selectedCategory === category && styles.categoryChipActive,
            ]}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              setSelectedCategory(category);
            }}
          >
            <Text
              style={[
                styles.categoryChipText,
                selectedCategory === category && styles.categoryChipTextActive,
              ]}
            >
              {category}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Featured Article */}
        {selectedCategory === 'All' && featuredArticle && (
          <View style={styles.featuredSection}>
            {renderArticleCard(featuredArticle, true)}
          </View>
        )}

        {/* Article List */}
        <View style={styles.articleList}>
          {filteredArticles
            .filter((a) => !a.featured || selectedCategory !== 'All')
            .map((article) => renderArticleCard(article))}
        </View>

        {/* Premium CTA */}
        {!isPremium && (
          <View style={styles.premiumCta}>
            <View style={styles.premiumCtaIcon}>
              <Ionicons name="lock-open-outline" size={28} color={COLORS.primary} />
            </View>
            <Text style={styles.premiumCtaTitle}>Unlock All Articles</Text>
            <Text style={styles.premiumCtaText}>
              Get access to premium deep-dives, protocol stacking guides, and exclusive
              research summaries.
            </Text>
          </View>
        )}
      </ScrollView>

      {/* Article Modal */}
      <Modal visible={showArticle} animationType="slide" presentationStyle="pageSheet">
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setShowArticle(false);
                setSelectedArticle(null);
              }}
            >
              <Ionicons name="close" size={24} color={COLORS.text} />
            </TouchableOpacity>
          </View>

          <ScrollView
            style={styles.modalScrollView}
            contentContainerStyle={styles.modalContent}
            showsVerticalScrollIndicator={false}
          >
            {selectedArticle && (
              <>
                <Text style={styles.modalCategory}>{selectedArticle.category}</Text>
                <Text style={styles.modalTitle}>{selectedArticle.title}</Text>

                <View style={styles.modalMeta}>
                  <View style={styles.readTime}>
                    <Ionicons name="time-outline" size={14} color={COLORS.textMuted} />
                    <Text style={styles.readTimeText}>
                      {selectedArticle.readTime} min read
                    </Text>
                  </View>
                </View>

                <Text style={styles.articleBody}>
                  {ARTICLE_CONTENT[selectedArticle.id]?.content ||
                    selectedArticle.excerpt}
                </Text>

                {/* Affiliate Recommendation */}
                {ARTICLE_CONTENT[selectedArticle.id]?.affiliateProduct && (
                  <AffiliateRecommendation
                    title={ARTICLE_CONTENT[selectedArticle.id].affiliateProduct.title}
                    description={
                      ARTICLE_CONTENT[selectedArticle.id].affiliateProduct.description
                    }
                    category={ARTICLE_CONTENT[selectedArticle.id].affiliateProduct.category}
                    price={ARTICLE_CONTENT[selectedArticle.id].affiliateProduct.price}
                    icon={ARTICLE_CONTENT[selectedArticle.id].affiliateProduct.icon}
                    affiliateLink="https://example.com/affiliate" // Placeholder
                  />
                )}
              </>
            )}
          </ScrollView>
        </View>
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
    paddingTop: 8,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  categoriesContainer: {
    paddingHorizontal: 20,
    paddingBottom: 16,
  },
  categoryChip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    marginRight: 8,
  },
  categoryChipActive: {
    backgroundColor: COLORS.primary,
  },
  categoryChipText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.textSecondary,
  },
  categoryChipTextActive: {
    color: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 100,
  },
  featuredSection: {
    marginBottom: 24,
  },
  articleList: {
    gap: 12,
  },
  articleCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    overflow: 'hidden',
  },
  featuredCard: {
    borderWidth: 1,
    borderColor: COLORS.primaryDark,
  },
  featuredBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 12,
    paddingVertical: 6,
    alignSelf: 'flex-start',
  },
  featuredBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.background,
    letterSpacing: 1,
  },
  articleContent: {
    padding: 16,
  },
  articleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  articleCategory: {
    fontSize: 12,
    fontWeight: '500',
    color: COLORS.primary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  lockBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(255, 217, 61, 0.15)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 10,
  },
  lockBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.accent,
  },
  articleTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  featuredTitle: {
    fontSize: 20,
  },
  articleExcerpt: {
    fontSize: 14,
    color: COLORS.textSecondary,
    lineHeight: 20,
    marginBottom: 12,
  },
  articleFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  readTime: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  readTimeText: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
  premiumCta: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginTop: 24,
    borderWidth: 1,
    borderColor: COLORS.primaryDark,
  },
  premiumCtaIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  premiumCtaTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  premiumCtaText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    padding: 16,
    paddingTop: 8,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalScrollView: {
    flex: 1,
  },
  modalContent: {
    padding: 20,
    paddingBottom: 40,
  },
  modalCategory: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.primary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 8,
  },
  modalTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 16,
    lineHeight: 34,
  },
  modalMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
    paddingBottom: 24,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  articleBody: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 26,
  },
});
