import { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Animated,
  Dimensions,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import Luna from '@/components/luna/Luna';
import { paywallConfig } from '@/constants/paywall';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

// Stats to display
const appStats = {
  rating: 4.9,
  totalRatings: '10K+',
  downloads: '50K+',
  activeUsers: '25K+',
};

export default function SocialProofScreen() {
  const router = useRouter();

  // Animation values
  const headerOpacity = useRef(new Animated.Value(0)).current;
  const headerTranslateY = useRef(new Animated.Value(-20)).current;
  const ratingScale = useRef(new Animated.Value(0)).current;
  const testimonial1Opacity = useRef(new Animated.Value(0)).current;
  const testimonial1TranslateX = useRef(new Animated.Value(-30)).current;
  const testimonial2Opacity = useRef(new Animated.Value(0)).current;
  const testimonial2TranslateX = useRef(new Animated.Value(30)).current;
  const testimonial3Opacity = useRef(new Animated.Value(0)).current;
  const testimonial3TranslateX = useRef(new Animated.Value(-30)).current;
  const buttonOpacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Staggered entrance animations
    Animated.sequence([
      // Header fades in
      Animated.parallel([
        Animated.timing(headerOpacity, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.timing(headerTranslateY, {
          toValue: 0,
          duration: 400,
          useNativeDriver: true,
        }),
      ]),
      // Rating bounces in
      Animated.spring(ratingScale, {
        toValue: 1,
        tension: 50,
        friction: 7,
        useNativeDriver: true,
      }),
      // Testimonials slide in
      Animated.stagger(150, [
        Animated.parallel([
          Animated.timing(testimonial1Opacity, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(testimonial1TranslateX, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ]),
        Animated.parallel([
          Animated.timing(testimonial2Opacity, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(testimonial2TranslateX, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ]),
        Animated.parallel([
          Animated.timing(testimonial3Opacity, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(testimonial3TranslateX, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ]),
      ]),
      // Button fades in
      Animated.timing(buttonOpacity, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handleContinue = () => {
    router.push('/(onboarding)/paywall');
  };

  const testimonialAnimations = [
    { opacity: testimonial1Opacity, translateX: testimonial1TranslateX },
    { opacity: testimonial2Opacity, translateX: testimonial2TranslateX },
    { opacity: testimonial3Opacity, translateX: testimonial3TranslateX },
  ];

  // Render stars
  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating - fullStars >= 0.5;

    for (let i = 0; i < 5; i++) {
      if (i < fullStars) {
        stars.push(
          <Ionicons key={i} name="star" size={24} color={colors.warning} />
        );
      } else if (i === fullStars && hasHalfStar) {
        stars.push(
          <Ionicons key={i} name="star-half" size={24} color={colors.warning} />
        );
      } else {
        stars.push(
          <Ionicons key={i} name="star-outline" size={24} color={colors.warning} />
        );
      }
    }
    return stars;
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[colors.warning + '15', colors.background]}
        style={styles.gradient}
      />

      <SafeAreaView style={styles.safeArea}>
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Header */}
          <Animated.View
            style={[
              styles.header,
              {
                opacity: headerOpacity,
                transform: [{ translateY: headerTranslateY }],
              },
            ]}
          >
            <Luna state="celebrating" size={80} />
            <Text style={styles.title}>Loved by thousands</Text>
            <Text style={styles.subtitle}>
              Join women who are crushing their fitness goals
            </Text>
          </Animated.View>

          {/* Rating Display */}
          <Animated.View
            style={[
              styles.ratingContainer,
              {
                transform: [{ scale: ratingScale }],
              },
            ]}
          >
            <View style={styles.ratingCard}>
              <Text style={styles.ratingNumber}>{appStats.rating}</Text>
              <View style={styles.starsRow}>{renderStars(appStats.rating)}</View>
              <Text style={styles.ratingCount}>
                {appStats.totalRatings} ratings on App Store
              </Text>
            </View>

            {/* Stats row */}
            <View style={styles.statsRow}>
              <View style={styles.statItem}>
                <Ionicons name="download" size={20} color={colors.primary} />
                <Text style={styles.statNumber}>{appStats.downloads}</Text>
                <Text style={styles.statLabel}>Downloads</Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Ionicons name="people" size={20} color={colors.accent} />
                <Text style={styles.statNumber}>{appStats.activeUsers}</Text>
                <Text style={styles.statLabel}>Active users</Text>
              </View>
            </View>
          </Animated.View>

          {/* Testimonials */}
          <View style={styles.testimonialsContainer}>
            <Text style={styles.testimonialsTitle}>What users say</Text>

            {paywallConfig.reviews.map((review, index) => (
              <Animated.View
                key={index}
                style={[
                  styles.testimonialCard,
                  {
                    opacity: testimonialAnimations[index]?.opacity || testimonial1Opacity,
                    transform: [
                      {
                        translateX:
                          testimonialAnimations[index]?.translateX ||
                          testimonial1TranslateX,
                      },
                    ],
                  },
                ]}
              >
                <View style={styles.testimonialHeader}>
                  <View style={styles.testimonialStars}>
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Ionicons
                        key={star}
                        name={star <= review.rating ? 'star' : 'star-outline'}
                        size={14}
                        color={colors.warning}
                      />
                    ))}
                  </View>
                  <View style={styles.verifiedBadge}>
                    <Ionicons
                      name="checkmark-circle"
                      size={14}
                      color={colors.success}
                    />
                    <Text style={styles.verifiedText}>{review.name}</Text>
                  </View>
                </View>
                <Text style={styles.testimonialText}>"{review.text}"</Text>
              </Animated.View>
            ))}
          </View>

          {/* Trust indicators */}
          <View style={styles.trustContainer}>
            <View style={styles.trustItem}>
              <Ionicons name="shield-checkmark" size={20} color={colors.success} />
              <Text style={styles.trustText}>Secure & private</Text>
            </View>
            <View style={styles.trustItem}>
              <Ionicons name="heart" size={20} color={colors.primary} />
              <Text style={styles.trustText}>Made for women</Text>
            </View>
            <View style={styles.trustItem}>
              <Ionicons name="ribbon" size={20} color={colors.warning} />
              <Text style={styles.trustText}>Expert-designed</Text>
            </View>
          </View>
        </ScrollView>

        {/* CTA Button */}
        <Animated.View
          style={[
            styles.ctaContainer,
            {
              opacity: buttonOpacity,
            },
          ]}
        >
          <Pressable
            style={({ pressed }) => [
              styles.ctaButton,
              pressed && styles.ctaButtonPressed,
            ]}
            onPress={handleContinue}
          >
            <Text style={styles.ctaText}>Continue</Text>
            <Ionicons name="arrow-forward" size={20} color={colors.surface} />
          </Pressable>
        </Animated.View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  gradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 400,
  },
  safeArea: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: 120,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.h1,
    color: colors.text,
    textAlign: 'center',
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
  },
  ratingContainer: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  ratingCard: {
    backgroundColor: colors.surface,
    padding: spacing.xl,
    borderRadius: borderRadius.xl,
    alignItems: 'center',
    width: '100%',
    marginBottom: spacing.md,
    ...shadows.md,
  },
  ratingNumber: {
    fontSize: 56,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.sm,
  },
  starsRow: {
    flexDirection: 'row',
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
  ratingCount: {
    ...typography.caption,
    color: colors.textMuted,
  },
  statsRow: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    width: '100%',
    ...shadows.sm,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statDivider: {
    width: 1,
    backgroundColor: colors.border,
    marginHorizontal: spacing.md,
  },
  statNumber: {
    ...typography.h3,
    color: colors.text,
    marginTop: spacing.xs,
  },
  statLabel: {
    ...typography.small,
    color: colors.textMuted,
  },
  testimonialsContainer: {
    marginBottom: spacing.xl,
  },
  testimonialsTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  testimonialCard: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  testimonialHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  testimonialStars: {
    flexDirection: 'row',
    gap: 2,
  },
  verifiedBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  verifiedText: {
    ...typography.small,
    color: colors.success,
  },
  testimonialText: {
    ...typography.body,
    color: colors.text,
    fontStyle: 'italic',
    lineHeight: 22,
  },
  trustContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  trustItem: {
    alignItems: 'center',
    gap: spacing.xs,
  },
  trustText: {
    ...typography.small,
    color: colors.textMuted,
  },
  ctaContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  ctaButtonPressed: {
    opacity: 0.9,
  },
  ctaText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
});
