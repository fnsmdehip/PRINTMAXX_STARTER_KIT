# GlowMaxx Mobile App Style Guide

**Purpose:** Design system for the React Native app UI, covering animations, scroll behavior, component patterns, and asset appearance.

---

## Design Philosophy

**Warm, Encouraging, Premium**

Unlike competitors (UMAX = cold/blue/masculine), GlowMaxx uses:
- Warm coral/teal palette for approachability
- Encouraging copy (progress, not judgment)
- Premium feel through dark mode + subtle animations
- Gender-inclusive design with toggle

---

## Color System

### Light Mode (Default)
```typescript
const COLORS = {
  primary: '#FF6B6B',        // Warm coral - CTAs, highlights
  primaryDark: '#E85555',    // Hover/pressed states
  primaryLight: '#FFB3B3',   // Backgrounds, highlights
  secondary: '#4ECDC4',      // Teal accent
  secondaryDark: '#3BA99F',
  accent: '#FFD93D',         // Gold - achievements, badges
  background: '#FAFAFA',     // Page background
  surface: '#FFFFFF',        // Card backgrounds
  text: '#1A1A1A',           // Primary text
  textSecondary: '#6B6B6B',  // Secondary text
  textLight: '#9CA3AF',      // Muted text
  border: '#E5E5E5',         // Borders, dividers

  // Semantic colors
  success: '#10B981',        // Green - positive
  warning: '#F59E0B',        // Amber - caution
  error: '#EF4444',          // Red - negative

  // Debloat indicators
  debloatLow: '#10B981',     // Good
  debloatMedium: '#F59E0B',  // Moderate
  debloatHigh: '#EF4444',    // High
};
```

### Dark Mode
```typescript
const COLORS_DARK = {
  primary: '#FF6B6B',
  primaryDark: '#FF8585',
  background: '#0F0F0F',     // True black
  surface: '#1A1A1A',        // Elevated surface
  text: '#FFFFFF',
  textSecondary: '#9CA3AF',
  border: '#2D2D2D',
};
```

### Gradient Usage
```typescript
// Primary gradient for CTAs
background: linear-gradient(135deg, #FF6B6B, #4ECDC4);

// Achievement/badge gradient
background: linear-gradient(135deg, #FFD93D, #FF6B6B);
```

---

## Typography

### Font Stack
```typescript
fontFamily: 'SF Pro Display', 'Inter', -apple-system, sans-serif
```

### Scale
| Use | Size | Weight | Line Height |
|-----|------|--------|-------------|
| Hero title | 32-40px | 700 (Bold) | 1.1 |
| Screen title | 28px | 700 | 1.2 |
| Section header | 20-24px | 600 (SemiBold) | 1.3 |
| Card title | 18px | 600 | 1.3 |
| Body | 16px | 400 (Regular) | 1.5 |
| Secondary | 14px | 400 | 1.4 |
| Caption | 12px | 400 | 1.3 |
| Stat number | 24-48px | 700 | 1.0 |

### Implementation
```typescript
const styles = StyleSheet.create({
  heroTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.text,
    lineHeight: 35,
  },
  screenTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  sectionHeader: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  body: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 24,
  },
  caption: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
```

---

## Component Patterns

### Cards

**Standard Card**
```typescript
const cardStyle = {
  backgroundColor: COLORS.surface,
  borderRadius: 16,
  padding: 16,
  // No shadow in light mode for cleaner look
  // Shadow in dark mode for elevation
};

// Dark mode shadow
shadowColor: '#000',
shadowOffset: { width: 0, height: 2 },
shadowOpacity: 0.1,
shadowRadius: 8,
elevation: 3,
```

**Interactive Card**
```typescript
// Add subtle scale on press
<TouchableOpacity
  activeOpacity={0.8}
  style={styles.card}
>
```

**Feature Card with Icon**
```typescript
<View style={styles.featureCard}>
  <View style={styles.iconContainer}>
    <Ionicons name="water-outline" size={24} color={COLORS.primary} />
  </View>
  <View style={styles.cardContent}>
    <Text style={styles.cardTitle}>Water Intake</Text>
    <Text style={styles.cardSubtitle}>Track daily hydration</Text>
  </View>
  <Ionicons name="chevron-forward" size={20} color={COLORS.textLight} />
</View>

// iconContainer style
iconContainer: {
  width: 48,
  height: 48,
  borderRadius: 12,
  backgroundColor: COLORS.primaryLight,
  alignItems: 'center',
  justifyContent: 'center',
},
```

### Buttons

**Primary Button (CTA)**
```typescript
primaryButton: {
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: COLORS.primary,
  paddingVertical: 16,
  paddingHorizontal: 24,
  borderRadius: 12,
  gap: 8,
},
primaryButtonText: {
  fontSize: 18,
  fontWeight: '600',
  color: '#FFFFFF',
},
```

**Secondary Button (Outline)**
```typescript
secondaryButton: {
  backgroundColor: 'transparent',
  borderWidth: 2,
  borderColor: COLORS.primary,
  paddingVertical: 14,
  paddingHorizontal: 24,
  borderRadius: 12,
},
secondaryButtonText: {
  fontSize: 16,
  fontWeight: '600',
  color: COLORS.primary,
},
```

**Gradient Button**
```typescript
import { LinearGradient } from 'expo-linear-gradient';

<TouchableOpacity>
  <LinearGradient
    colors={[COLORS.primary, COLORS.secondary]}
    start={{ x: 0, y: 0 }}
    end={{ x: 1, y: 1 }}
    style={styles.gradientButton}
  >
    <Text style={styles.gradientButtonText}>Get Started</Text>
  </LinearGradient>
</TouchableOpacity>
```

### Progress Indicators

**Progress Ring**
```typescript
import { AnimatedCircularProgress } from 'react-native-circular-progress';

<AnimatedCircularProgress
  size={120}
  width={10}
  fill={percentage}
  tintColor={COLORS.primary}
  backgroundColor={COLORS.border}
  rotation={0}
  lineCap="round"
>
  {(fill) => (
    <Text style={styles.progressText}>{Math.round(fill)}%</Text>
  )}
</AnimatedCircularProgress>
```

**Progress Bar**
```typescript
progressBarContainer: {
  height: 8,
  backgroundColor: COLORS.border,
  borderRadius: 4,
  overflow: 'hidden',
},
progressBarFill: {
  height: '100%',
  backgroundColor: COLORS.primary,
  borderRadius: 4,
},
```

**Streak Display**
```typescript
<View style={styles.streakBadge}>
  <Ionicons name="flame" size={20} color={COLORS.accent} />
  <Text style={styles.streakNumber}>{streak}</Text>
  <Text style={styles.streakLabel}>day streak</Text>
</View>

streakBadge: {
  flexDirection: 'row',
  alignItems: 'center',
  backgroundColor: '#FFF8E1',
  paddingVertical: 8,
  paddingHorizontal: 16,
  borderRadius: 20,
  gap: 4,
},
```

### Form Elements

**Text Input**
```typescript
input: {
  backgroundColor: COLORS.surface,
  borderWidth: 1,
  borderColor: COLORS.border,
  borderRadius: 12,
  paddingVertical: 14,
  paddingHorizontal: 16,
  fontSize: 16,
  color: COLORS.text,
},
inputFocused: {
  borderColor: COLORS.primary,
  borderWidth: 2,
},
```

**Selection Chips (Gender, Options)**
```typescript
chip: {
  paddingVertical: 12,
  paddingHorizontal: 20,
  borderRadius: 20,
  borderWidth: 2,
  borderColor: COLORS.border,
  backgroundColor: COLORS.surface,
},
chipSelected: {
  borderColor: COLORS.primary,
  backgroundColor: COLORS.primary,
},
chipText: {
  fontSize: 14,
  fontWeight: '600',
  color: COLORS.text,
},
chipTextSelected: {
  color: '#FFFFFF',
},
```

---

## Animation Patterns

### Micro-interactions

**Button Press**
```typescript
import * as Haptics from 'expo-haptics';

const handlePress = () => {
  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  // Action
};
```

**Card Tap**
```typescript
<TouchableOpacity
  activeOpacity={0.9}
  onPress={() => {
    Haptics.selectionAsync();
    // Navigate
  }}
>
```

**Success Feedback**
```typescript
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
```

### Screen Transitions

Using expo-router with default slide animations:
```typescript
// _layout.tsx
<Stack
  screenOptions={{
    headerShown: false,
    animation: 'slide_from_right', // iOS-style
  }}
/>
```

### Number Count-Up Animation
```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming
} from 'react-native-reanimated';

// Animate stat numbers on mount
useEffect(() => {
  count.value = withTiming(targetValue, { duration: 1000 });
}, []);
```

### Progress Ring Animation
```typescript
// Animate progress on scroll into view
<AnimatedCircularProgress
  duration={800}
  easing={Easing.out(Easing.ease)}
/>
```

### Skeleton Loading
```typescript
import { MotiView } from 'moti';

<MotiView
  from={{ opacity: 0.5 }}
  animate={{ opacity: 1 }}
  transition={{ loop: true, type: 'timing', duration: 1000 }}
  style={styles.skeleton}
/>

skeleton: {
  backgroundColor: COLORS.border,
  borderRadius: 8,
},
```

---

## Scroll Behavior

### Pull to Refresh
```typescript
<ScrollView
  refreshControl={
    <RefreshControl
      refreshing={refreshing}
      onRefresh={onRefresh}
      tintColor={COLORS.primary}
      colors={[COLORS.primary]} // Android
    />
  }
>
```

### Sticky Headers
```typescript
<SectionList
  stickySectionHeadersEnabled={true}
  renderSectionHeader={({ section }) => (
    <View style={styles.stickyHeader}>
      <Text style={styles.sectionTitle}>{section.title}</Text>
    </View>
  )}
/>

stickyHeader: {
  backgroundColor: COLORS.background,
  paddingVertical: 8,
  paddingHorizontal: 20,
},
```

### Bottom Tab Safe Area
```typescript
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const insets = useSafeAreaInsets();

scrollContent: {
  paddingBottom: insets.bottom + 80, // Tab bar height
},
```

### Smooth Scrolling
```typescript
<FlatList
  showsVerticalScrollIndicator={false}
  decelerationRate="fast"
  snapToInterval={CARD_HEIGHT + GAP}
  snapToAlignment="start"
/>
```

---

## Icon System

### Icon Library
Using `@expo/vector-icons` with Ionicons (iOS-native feel):

```typescript
import { Ionicons } from '@expo/vector-icons';

// Outline for inactive, filled for active
<Ionicons
  name={focused ? 'home' : 'home-outline'}
  size={24}
  color={focused ? COLORS.primary : COLORS.textSecondary}
/>
```

### Tab Bar Icons
| Tab | Active | Inactive |
|-----|--------|----------|
| Home | home | home-outline |
| Progress | camera | camera-outline |
| Learn | book | book-outline |
| Profile | person | person-outline |

### Common Feature Icons
| Feature | Icon |
|---------|------|
| Water | water-outline |
| Sleep | moon-outline |
| Sodium | restaurant-outline |
| Mewing | happy-outline |
| Timer | time-outline |
| Streak | flame |
| Achievement | trophy-outline |
| Settings | settings-outline |
| Back | chevron-back |
| Forward | chevron-forward |
| Add | add-circle-outline |
| Check | checkmark-circle |

### Icon Sizing
| Context | Size |
|---------|------|
| Tab bar | 24px |
| Card icon | 24px |
| Feature icon (in circle) | 24-32px |
| Large display | 48-64px |
| Small indicator | 16-18px |

---

## Asset Appearance

### App Icon
- 1024x1024 for App Store
- Warm coral gradient background
- Simple, recognizable symbol (glow/sparkle)
- No text in icon

### Placeholder Images
```typescript
placeholderImage: {
  backgroundColor: COLORS.border,
  borderRadius: 12,
  alignItems: 'center',
  justifyContent: 'center',
},
```

### Photo Thumbnails
```typescript
thumbnail: {
  width: 80,
  height: 80,
  borderRadius: 8,
  backgroundColor: COLORS.border,
},
thumbnailLarge: {
  width: 150,
  height: 150,
  borderRadius: 12,
},
```

### Achievement Badges
```typescript
badge: {
  width: 64,
  height: 64,
  borderRadius: 32,
  backgroundColor: COLORS.accent,
  alignItems: 'center',
  justifyContent: 'center',
},
badgeLocked: {
  backgroundColor: COLORS.border,
  opacity: 0.5,
},
```

---

## Layout Patterns

### Screen Structure
```typescript
<SafeAreaView style={styles.container} edges={['top']}>
  {/* Header */}
  <View style={styles.header}>
    <Text style={styles.title}>Screen Title</Text>
    <Text style={styles.subtitle}>Supporting text</Text>
  </View>

  {/* Scrollable Content */}
  <ScrollView
    style={styles.scrollView}
    contentContainerStyle={styles.scrollContent}
    showsVerticalScrollIndicator={false}
  >
    {/* Content */}
  </ScrollView>
</SafeAreaView>

container: {
  flex: 1,
  backgroundColor: COLORS.background,
},
header: {
  paddingHorizontal: 20,
  paddingTop: 10,
  paddingBottom: 16,
},
scrollView: {
  flex: 1,
},
scrollContent: {
  padding: 20,
  paddingTop: 0,
  paddingBottom: 40,
},
```

### Grid Layout
```typescript
grid: {
  flexDirection: 'row',
  flexWrap: 'wrap',
  gap: 12,
},
gridItem: {
  width: (SCREEN_WIDTH - 52) / 2, // 20px padding + 12px gap
},
```

### Stat Row
```typescript
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
```

---

## Dark Mode Implementation

```typescript
import { useColorScheme } from 'react-native';

const colorScheme = useColorScheme();
const colors = colorScheme === 'dark' ? COLORS_DARK : COLORS;

// Or use context
const ThemeContext = createContext(COLORS);

export function useTheme() {
  return useContext(ThemeContext);
}
```

---

## Accessibility

### Touch Targets
- Minimum 44x44 points for all interactive elements
- Add padding to small icons in touchable areas

### Text Scaling
```typescript
<Text
  style={styles.body}
  allowFontScaling={true}
  maxFontSizeMultiplier={1.3}
>
```

### Screen Reader
```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Add progress photo"
  accessibilityHint="Opens camera or photo library"
>
```

---

## Competitor Comparison

| Element | UMAX | LooksMax AI | GlowMaxx |
|---------|------|-------------|----------|
| Primary Color | Blue | Purple/Pink | Warm Coral |
| Background | True Black | Dark Gray | Light (dark option) |
| Vibe | Cold, Masculine | Data-focused | Warm, Encouraging |
| Cards | Sharp corners | Rounded | Soft rounded (16px) |
| Animations | Minimal | Loading states | Micro-interactions |
| Progress | Scores | Ratings | Rings + Streaks |
