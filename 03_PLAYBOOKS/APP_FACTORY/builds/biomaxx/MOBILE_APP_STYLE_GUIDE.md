# BioMaxx Mobile App Style Guide

**Purpose:** Design system for the React Native app UI covering colors, typography, components, animations, and patterns.

---

## Design Philosophy

**Earthy Premium Dark Mode**

Unlike generic health apps (sterile white/blue) or typical biohacking apps (cold/techy), BioMaxx uses:
- Emerald green for longevity/life
- Warm amber for energy/vitality
- Deep slate backgrounds for premium feel
- Gold accents for achievements
- Organic, natural feeling despite being tech-forward

---

## Color System

### Primary Palette
```typescript
const COLORS = {
  // Core brand colors
  primary: '#10B981',        // Deep emerald green - longevity, growth
  primaryDark: '#059669',    // Hover/pressed states
  primaryLight: '#6EE7B7',   // Highlights, backgrounds

  // Secondary/accent
  secondary: '#F59E0B',      // Warm amber - energy, vitality
  secondaryDark: '#D97706',
  accent: '#FFD93D',         // Gold - achievements, premium

  // Backgrounds (dark mode only)
  background: '#0F172A',     // Deep slate - main background
  surface: '#1E293B',        // Elevated surface
  surfaceLight: '#334155',   // Cards, elevated elements
  surfaceHighlight: '#475569', // Hover states

  // Text
  text: '#F8FAFC',           // Off-white primary text
  textSecondary: '#94A3B8',  // Secondary text
  textMuted: '#64748B',      // Muted/disabled text

  // Semantic colors
  success: '#10B981',        // Green (same as primary)
  warning: '#F59E0B',        // Amber (same as secondary)
  error: '#EF4444',          // Red
  info: '#3B82F6',           // Blue

  // Protocol-specific colors
  fasting: '#8B5CF6',        // Purple
  cold: '#06B6D4',           // Cyan
  heat: '#EF4444',           // Red
  light: '#F59E0B',          // Amber
  supplements: '#10B981',    // Green
  movement: '#3B82F6',       // Blue
  sleep: '#6366F1',          // Indigo

  // Borders
  border: '#334155',
  borderLight: '#475569',
};
```

### Gradient Usage
```typescript
// Primary gradient (CTAs, highlights)
background: LinearGradient(['#10B981', '#059669'])

// Premium/achievement gradient
background: LinearGradient(['#FFD93D', '#F59E0B'])

// Protocol ring gradient (varies by category)
fasting: LinearGradient(['#8B5CF6', '#A78BFA'])
cold: LinearGradient(['#06B6D4', '#22D3EE'])
```

---

## Typography

### Font Stack
```typescript
fontFamily: {
  regular: 'SF Pro Display', // System default on iOS
  medium: 'SF Pro Display Medium',
  bold: 'SF Pro Display Bold',
  fallback: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto',
}
```

### Scale
| Use | Size | Weight | Line Height | Letter Spacing |
|-----|------|--------|-------------|----------------|
| Hero stat | 48px | 700 | 1.0 | -1px |
| Screen title | 28px | 700 | 1.2 | -0.5px |
| Section header | 20px | 600 | 1.3 | 0 |
| Card title | 18px | 600 | 1.3 | 0 |
| Body | 16px | 400 | 1.5 | 0 |
| Secondary | 14px | 400 | 1.4 | 0 |
| Caption | 12px | 500 | 1.3 | 0.5px |
| Badge | 11px | 600 | 1.0 | 1px |

### Implementation
```typescript
const typography = {
  heroStat: {
    fontSize: 48,
    fontWeight: '700',
    lineHeight: 48,
    letterSpacing: -1,
    color: COLORS.text,
  },
  screenTitle: {
    fontSize: 28,
    fontWeight: '700',
    lineHeight: 34,
    letterSpacing: -0.5,
    color: COLORS.text,
  },
  sectionHeader: {
    fontSize: 20,
    fontWeight: '600',
    lineHeight: 26,
    color: COLORS.text,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    lineHeight: 23,
    color: COLORS.text,
  },
  body: {
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 24,
    color: COLORS.text,
  },
  secondary: {
    fontSize: 14,
    fontWeight: '400',
    lineHeight: 20,
    color: COLORS.textSecondary,
  },
  caption: {
    fontSize: 12,
    fontWeight: '500',
    lineHeight: 16,
    letterSpacing: 0.5,
    color: COLORS.textMuted,
  },
};
```

---

## Component Patterns

### Cards

**Standard Card**
```typescript
card: {
  backgroundColor: COLORS.surface,
  borderRadius: 16,
  padding: 16,
  borderWidth: 1,
  borderColor: COLORS.border,
},
```

**Elevated Card (for featured content)**
```typescript
elevatedCard: {
  backgroundColor: COLORS.surfaceLight,
  borderRadius: 20,
  padding: 20,
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 4 },
  shadowOpacity: 0.2,
  shadowRadius: 12,
  elevation: 8,
},
```

**Protocol Card**
```typescript
protocolCard: {
  backgroundColor: COLORS.surface,
  borderRadius: 16,
  padding: 16,
  flexDirection: 'row',
  alignItems: 'center',
  borderWidth: 1,
  borderColor: COLORS.border,
},
protocolIcon: {
  width: 48,
  height: 48,
  borderRadius: 12,
  backgroundColor: COLORS.primaryLight + '20', // 20% opacity
  alignItems: 'center',
  justifyContent: 'center',
},
```

### Progress Rings

**Circular Progress (Protocol Ring)**
```typescript
import { AnimatedCircularProgress } from 'react-native-circular-progress';

<AnimatedCircularProgress
  size={100}
  width={8}
  fill={percentComplete}
  tintColor={protocolColor}
  backgroundColor={COLORS.surfaceLight}
  rotation={0}
  lineCap="round"
>
  {(fill) => (
    <View style={styles.ringContent}>
      <Ionicons name={protocolIcon} size={24} color={protocolColor} />
      <Text style={styles.ringPercent}>{Math.round(fill)}%</Text>
    </View>
  )}
</AnimatedCircularProgress>
```

**Mini Progress Ring (Dashboard Grid)**
```typescript
<AnimatedCircularProgress
  size={64}
  width={5}
  fill={percentComplete}
  tintColor={protocolColor}
  backgroundColor={COLORS.border}
  lineCap="round"
/>
```

### Buttons

**Primary Button**
```typescript
primaryButton: {
  backgroundColor: COLORS.primary,
  paddingVertical: 16,
  paddingHorizontal: 24,
  borderRadius: 12,
  alignItems: 'center',
  justifyContent: 'center',
  flexDirection: 'row',
  gap: 8,
},
primaryButtonText: {
  fontSize: 16,
  fontWeight: '600',
  color: '#FFFFFF',
},
```

**Secondary Button**
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

**Ghost Button (text only)**
```typescript
ghostButton: {
  padding: 12,
},
ghostButtonText: {
  fontSize: 14,
  fontWeight: '600',
  color: COLORS.primary,
},
```

**Start Session Button**
```typescript
startButton: {
  backgroundColor: COLORS.primary,
  width: 64,
  height: 64,
  borderRadius: 32,
  alignItems: 'center',
  justifyContent: 'center',
  shadowColor: COLORS.primary,
  shadowOffset: { width: 0, height: 4 },
  shadowOpacity: 0.3,
  shadowRadius: 8,
},
```

### Streak Badge
```typescript
streakBadge: {
  flexDirection: 'row',
  alignItems: 'center',
  backgroundColor: COLORS.secondary + '20',
  paddingVertical: 6,
  paddingHorizontal: 12,
  borderRadius: 20,
  gap: 4,
},
streakIcon: {
  // Flame icon
},
streakText: {
  fontSize: 14,
  fontWeight: '700',
  color: COLORS.secondary,
},
```

### Timer Display
```typescript
timerContainer: {
  alignItems: 'center',
  justifyContent: 'center',
  padding: 32,
},
timerText: {
  fontSize: 64,
  fontWeight: '700',
  color: COLORS.text,
  fontVariant: ['tabular-nums'],
  letterSpacing: -2,
},
timerLabel: {
  fontSize: 14,
  color: COLORS.textSecondary,
  marginTop: 8,
},
```

---

## Navigation

### Bottom Tab Bar
```typescript
tabBar: {
  backgroundColor: COLORS.surface,
  borderTopWidth: 1,
  borderTopColor: COLORS.border,
  paddingTop: 8,
  paddingBottom: insets.bottom + 8,
  height: 60 + insets.bottom,
},
tabBarLabel: {
  fontSize: 11,
  fontWeight: '500',
},
tabBarIcon: {
  // Size: 24
},
```

**Tab Icons (Ionicons):**
| Tab | Active | Inactive |
|-----|--------|----------|
| Dashboard | grid | grid-outline |
| Protocols | flask | flask-outline |
| Learn | book | book-outline |
| Profile | person | person-outline |

### Header
```typescript
header: {
  paddingHorizontal: 20,
  paddingTop: insets.top + 10,
  paddingBottom: 16,
  backgroundColor: COLORS.background,
},
headerTitle: {
  fontSize: 28,
  fontWeight: '700',
  color: COLORS.text,
},
headerSubtitle: {
  fontSize: 14,
  color: COLORS.textSecondary,
  marginTop: 4,
},
```

---

## Animation Patterns

### Haptic Feedback
```typescript
import * as Haptics from 'expo-haptics';

// Light tap (button press, selection)
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);

// Medium tap (start session)
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

// Selection (toggle, picker)
Haptics.selectionAsync();

// Success (complete session, achievement)
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
```

### Button Press
```typescript
<TouchableOpacity
  activeOpacity={0.8}
  onPress={handlePress}
  style={[styles.button, pressed && styles.buttonPressed]}
>
```

### Progress Ring Animation
```typescript
<AnimatedCircularProgress
  duration={800}
  easing={Easing.out(Easing.cubic)}
/>
```

### Screen Transitions
```typescript
// expo-router default with custom
<Stack
  screenOptions={{
    headerShown: false,
    animation: 'slide_from_right',
    contentStyle: { backgroundColor: COLORS.background },
  }}
/>
```

### Number Count-Up
```typescript
import Animated, { withTiming } from 'react-native-reanimated';

// Animate stat numbers on mount
useEffect(() => {
  value.value = withTiming(targetValue, { duration: 1000 });
}, []);
```

---

## Protocol-Specific Styling

### Category Colors
```typescript
const protocolColors = {
  fasting: '#8B5CF6',    // Purple - discipline, mental
  cold: '#06B6D4',       // Cyan - ice, cool
  heat: '#EF4444',       // Red - fire, warmth
  light: '#F59E0B',      // Amber - light, energy
  supplements: '#10B981', // Green - health, nature
  movement: '#3B82F6',   // Blue - activity
  sleep: '#6366F1',      // Indigo - night, rest
};
```

### Category Icons (Ionicons)
```typescript
const protocolIcons = {
  fasting: 'timer-outline',
  cold: 'snow-outline',
  heat: 'flame-outline',
  light: 'sunny-outline',
  supplements: 'medical-outline',
  movement: 'fitness-outline',
  sleep: 'moon-outline',
};
```

### Protocol Card Variants
```typescript
// Each protocol card has subtle tint based on category
protocolCardFasting: {
  borderLeftWidth: 3,
  borderLeftColor: protocolColors.fasting,
},
```

---

## Layout Patterns

### Screen Structure
```typescript
<SafeAreaView style={styles.container} edges={['top']}>
  <View style={styles.header}>
    <Text style={styles.title}>Dashboard</Text>
    <StreakBadge streak={12} />
  </View>

  <ScrollView
    style={styles.scrollView}
    contentContainerStyle={styles.scrollContent}
    showsVerticalScrollIndicator={false}
  >
    {/* Content */}
  </ScrollView>
</SafeAreaView>
```

### Dashboard Grid (2x3 for 6 protocols)
```typescript
grid: {
  flexDirection: 'row',
  flexWrap: 'wrap',
  gap: 12,
  justifyContent: 'space-between',
},
gridItem: {
  width: (SCREEN_WIDTH - 52) / 2, // 20px padding + 12px gap
  aspectRatio: 1,
  backgroundColor: COLORS.surface,
  borderRadius: 16,
  padding: 12,
  alignItems: 'center',
  justifyContent: 'center',
},
```

### List Items
```typescript
listItem: {
  flexDirection: 'row',
  alignItems: 'center',
  paddingVertical: 16,
  borderBottomWidth: 1,
  borderBottomColor: COLORS.border,
},
```

---

## Accessibility

### Touch Targets
- Minimum 44x44 points for all interactive elements
- Protocol cards: full card is tappable

### Color Contrast
- All text meets WCAG AA standards on dark backgrounds
- Primary green (#10B981) provides 4.5:1 contrast on slate (#0F172A)

### Screen Reader
```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Start fasting session"
  accessibilityRole="button"
>
```

---

## Spacing System

```typescript
const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  xxxl: 32,
};

// Common patterns
screenPadding: 20,
cardPadding: 16,
sectionGap: 24,
itemGap: 12,
```

---

## Competitor Comparison

| Element | Zero | Biohackr | BioMaxx |
|---------|------|----------|---------|
| Primary Color | White/Blue | Blue/Purple | Emerald Green |
| Background | Light/Dark | Dark | Dark (only) |
| Vibe | Clinical | Techy | Earthy Premium |
| Progress | Timer | Streaks | Rings + Score |
| Unique Element | Meal photos | AI coach | Protocol stacking |
