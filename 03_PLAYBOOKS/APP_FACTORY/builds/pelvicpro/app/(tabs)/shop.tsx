import { View, Text, StyleSheet, ScrollView, Pressable, Linking } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';

// Affiliate link placeholders - replace with actual affiliate URLs
const AFFILIATE_PRODUCTS = {
  supplements: [
    {
      id: 'collagen',
      name: 'Collagen Peptides',
      brand: 'Vital Proteins',
      description: 'Supports skin, hair, nails & joint health. Perfect for active women.',
      price: '$27.00',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'nutrition',
    },
    {
      id: 'protein',
      name: "Women's Protein Powder",
      brand: 'Orgain',
      description: 'Plant-based protein. 21g per serving. Great for post-workout recovery.',
      price: '$29.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'nutrition',
    },
    {
      id: 'preworkout',
      name: 'Pre-Workout (Stim-Free)',
      brand: 'Alani Nu',
      description: 'Clean energy without jitters. Designed for women.',
      price: '$39.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'flash',
    },
    {
      id: 'creatine',
      name: 'Creatine Monohydrate',
      brand: 'Transparent Labs',
      description: 'Build strength & muscle. Safe for women. No bloating formula.',
      price: '$34.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'barbell',
    },
    {
      id: 'magnesium',
      name: 'Magnesium Glycinate',
      brand: 'NOW Foods',
      description: 'Supports muscle recovery & sleep. Essential for active women.',
      price: '$18.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'moon',
    },
  ],
  equipment: [
    {
      id: 'bands',
      name: 'Fabric Booty Bands (3-Pack)',
      brand: 'Gymbee',
      description: 'Non-slip resistance bands for glute activation.',
      price: '$16.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'fitness',
    },
    {
      id: 'hippad',
      name: 'Barbell Hip Thrust Pad',
      brand: 'Squat Sponge',
      description: 'Extra thick padding for heavy hip thrusts.',
      price: '$29.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'fitness',
    },
    {
      id: 'anklestraps',
      name: 'Cable Machine Ankle Straps',
      brand: 'DMoose',
      description: 'Padded straps for kickbacks and leg work.',
      price: '$14.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'fitness',
    },
    {
      id: 'mat',
      name: 'Extra Thick Yoga Mat',
      brand: 'Gaiam',
      description: '6mm cushioning for floor exercises.',
      price: '$29.98',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'fitness',
    },
    {
      id: 'dumbbells',
      name: 'Neoprene Dumbbell Set',
      brand: 'Amazon Basics',
      description: '3-5-8 lb set. Perfect for home workouts.',
      price: '$31.99',
      url: 'AFFILIATE_LINK_PLACEHOLDER',
      icon: 'barbell',
    },
  ],
};

const openLink = (url: string) => {
  Linking.openURL(url).catch(err => console.error('Failed to open URL:', err));
};

export default function ShopScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.title}>Shop</Text>
          <Text style={styles.subtitle}>
            Our favorite products for your fitness journey
          </Text>
        </View>

        {/* Affiliate Disclosure */}
        <View style={styles.disclosureCard}>
          <Ionicons name="information-circle" size={20} color={colors.primary} />
          <Text style={styles.disclosureText}>
            We may earn a small commission from purchases made through these links at no extra cost to you.
          </Text>
        </View>

        {/* Supplements Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="nutrition" size={24} color={colors.primary} />
            <Text style={styles.sectionTitle}>Supplements</Text>
          </View>
          <Text style={styles.sectionSubtitle}>
            Recommended for women's fitness goals
          </Text>

          {AFFILIATE_PRODUCTS.supplements.map((product) => (
            <Pressable
              key={product.id}
              style={({ pressed }) => [
                styles.productCard,
                pressed && styles.productCardPressed,
              ]}
              onPress={() => openLink(product.url)}
            >
              <View style={styles.productIcon}>
                <Ionicons
                  name={product.icon as any}
                  size={28}
                  color={colors.primary}
                />
              </View>
              <View style={styles.productInfo}>
                <Text style={styles.productBrand}>{product.brand}</Text>
                <Text style={styles.productName}>{product.name}</Text>
                <Text style={styles.productDescription}>{product.description}</Text>
                <Text style={styles.productPrice}>{product.price}</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color={colors.textMuted} />
            </Pressable>
          ))}
        </View>

        {/* Equipment Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="barbell" size={24} color={colors.primary} />
            <Text style={styles.sectionTitle}>Equipment</Text>
          </View>
          <Text style={styles.sectionSubtitle}>
            Essential gear for home & gym
          </Text>

          {AFFILIATE_PRODUCTS.equipment.map((product) => (
            <Pressable
              key={product.id}
              style={({ pressed }) => [
                styles.productCard,
                pressed && styles.productCardPressed,
              ]}
              onPress={() => openLink(product.url)}
            >
              <View style={styles.productIcon}>
                <Ionicons
                  name={product.icon as any}
                  size={28}
                  color={colors.primary}
                />
              </View>
              <View style={styles.productInfo}>
                <Text style={styles.productBrand}>{product.brand}</Text>
                <Text style={styles.productName}>{product.name}</Text>
                <Text style={styles.productDescription}>{product.description}</Text>
                <Text style={styles.productPrice}>{product.price}</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color={colors.textMuted} />
            </Pressable>
          ))}
        </View>

        <View style={styles.bottomPadding} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: spacing.lg,
  },
  header: {
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  subtitle: {
    ...typography.body,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  disclosureCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.sm,
    backgroundColor: colors.primary + '10',
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.lg,
  },
  disclosureText: {
    ...typography.small,
    color: colors.textLight,
    flex: 1,
    lineHeight: 18,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.xs,
  },
  sectionTitle: {
    ...typography.h2,
    color: colors.text,
  },
  sectionSubtitle: {
    ...typography.caption,
    color: colors.textMuted,
    marginBottom: spacing.md,
  },
  productCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  productCardPressed: {
    opacity: 0.8,
    transform: [{ scale: 0.98 }],
  },
  productIcon: {
    width: 56,
    height: 56,
    borderRadius: borderRadius.md,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  productInfo: {
    flex: 1,
  },
  productBrand: {
    ...typography.small,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  productName: {
    ...typography.bodyBold,
    color: colors.text,
    marginTop: 2,
  },
  productDescription: {
    ...typography.small,
    color: colors.textLight,
    marginTop: spacing.xs,
    lineHeight: 16,
  },
  productPrice: {
    ...typography.bodyBold,
    color: colors.primary,
    marginTop: spacing.xs,
  },
  bottomPadding: {
    height: 100,
  },
});
