# Accessible color palette

WCAG AA compliant color combinations for React Native apps.

---

## Quick reference

### Text on backgrounds

| Background | Safe text colors | Contrast ratio |
|------------|------------------|----------------|
| White (#FFFFFF) | #1C1C1E (black), #3A3A3C, #007AFF | 17:1, 10:1, 4.5:1 |
| Light gray (#F2F2F7) | #1C1C1E, #3A3A3C | 15:1, 9:1 |
| Dark (#1C1C1E) | #FFFFFF, #F2F2F7, #0A84FF | 17:1, 15:1, 5.5:1 |
| Blue (#007AFF) | #FFFFFF | 4.5:1 |
| Red (#FF3B30) | #FFFFFF, #1C1C1E | 4.5:1, 5.9:1 |
| Green (#34C759) | #1C1C1E | 5.7:1 |
| Orange (#FF9500) | #1C1C1E | 4.8:1 |

---

## Primary palette

### Light mode

```typescript
const lightColors = {
  // Backgrounds
  background: '#FFFFFF',          // Main background
  backgroundSecondary: '#F2F2F7', // Cards, sections
  backgroundTertiary: '#E5E5EA',  // Disabled states

  // Text
  textPrimary: '#1C1C1E',         // Body text (17:1 on white)
  textSecondary: '#3A3A3C',       // Secondary text (10:1 on white)
  textTertiary: '#636366',        // Captions (5.7:1 on white)
  textDisabled: '#8E8E93',        // Disabled (3.9:1 - use larger text)

  // Interactive
  primary: '#007AFF',             // Links, buttons (4.5:1 on white)
  primaryDark: '#0056B3',         // Pressed state (7.6:1 on white)

  // Semantic
  error: '#D70015',               // Error states (9:1 on white)
  errorLight: '#FFEAE9',          // Error background
  success: '#248A3D',             // Success (5.6:1 on white)
  successLight: '#E8F5E9',        // Success background
  warning: '#B25000',             // Warning (5.9:1 on white)
  warningLight: '#FFF4E5',        // Warning background

  // Borders
  border: '#C7C7CC',              // Default border
  borderFocused: '#007AFF',       // Focus state
  borderError: '#D70015',         // Error border
};
```

### Dark mode

```typescript
const darkColors = {
  // Backgrounds
  background: '#1C1C1E',          // Main background
  backgroundSecondary: '#2C2C2E', // Cards, sections
  backgroundTertiary: '#3A3A3C',  // Disabled states

  // Text
  textPrimary: '#FFFFFF',         // Body text (17:1 on dark)
  textSecondary: '#EBEBF5',       // Secondary text (14:1 on dark)
  textTertiary: '#EBEBF599',      // Captions (60% opacity)
  textDisabled: '#EBEBF54D',      // Disabled (30% opacity)

  // Interactive
  primary: '#0A84FF',             // Links, buttons (5.5:1 on dark)
  primaryDark: '#409CFF',         // Pressed state

  // Semantic
  error: '#FF453A',               // Error states
  errorLight: '#3A2020',          // Error background
  success: '#30D158',             // Success
  successLight: '#1C3A1F',        // Success background
  warning: '#FF9F0A',             // Warning
  warningLight: '#3A2F1C',        // Warning background

  // Borders
  border: '#38383A',              // Default border
  borderFocused: '#0A84FF',       // Focus state
  borderError: '#FF453A',         // Error border
};
```

---

## Color combinations

### Buttons

**Primary button:**
```typescript
// Light mode
{
  backgroundColor: '#007AFF',
  color: '#FFFFFF', // 4.5:1 contrast
}

// Dark mode
{
  backgroundColor: '#0A84FF',
  color: '#FFFFFF', // 4.5:1 contrast
}
```

**Secondary button:**
```typescript
// Light mode
{
  backgroundColor: '#E5E5EA',
  color: '#1C1C1E', // 12:1 contrast
}

// Dark mode
{
  backgroundColor: '#3A3A3C',
  color: '#FFFFFF', // 8.5:1 contrast
}
```

**Danger button:**
```typescript
// Light mode
{
  backgroundColor: '#D70015',
  color: '#FFFFFF', // 4.6:1 contrast
}

// Dark mode
{
  backgroundColor: '#FF453A',
  color: '#1C1C1E', // 5.3:1 contrast
}
```

**Ghost button:**
```typescript
// Light mode
{
  backgroundColor: 'transparent',
  borderColor: '#007AFF',
  color: '#007AFF', // 4.5:1 on white
}

// Dark mode
{
  backgroundColor: 'transparent',
  borderColor: '#0A84FF',
  color: '#0A84FF', // 5.5:1 on dark
}
```

### Links

```typescript
// Light mode (on white)
{
  color: '#0056B3', // 7.6:1 - better than default blue
  textDecorationLine: 'underline', // Visual distinction
}

// Within text
{
  color: '#007AFF', // 4.5:1
  // Underline helps distinguish from surrounding text
}

// Visited state (if tracking)
{
  color: '#68217A', // Purple, 7.1:1
}
```

### Form elements

**Input field:**
```typescript
// Light mode
{
  backgroundColor: '#FFFFFF',
  borderColor: '#C7C7CC', // 1.7:1 - visible but subtle
  color: '#1C1C1E', // 17:1
  placeholderColor: '#8E8E93', // 3.9:1 (AA for 18pt+)
}

// Focused
{
  borderColor: '#007AFF',
  borderWidth: 2,
}

// Error
{
  borderColor: '#D70015',
  borderWidth: 2,
}
```

**Labels:**
```typescript
// Light mode
{
  color: '#1C1C1E', // 17:1
}

// Required indicator
{
  color: '#D70015', // 9:1
}
```

### Status indicators

**Error:**
```typescript
// Light mode
{
  backgroundColor: '#FFEAE9',
  borderLeftColor: '#D70015',
  iconColor: '#D70015',
  textColor: '#1C1C1E',
}

// Dark mode
{
  backgroundColor: '#3A2020',
  borderLeftColor: '#FF453A',
  iconColor: '#FF453A',
  textColor: '#FFFFFF',
}
```

**Success:**
```typescript
// Light mode
{
  backgroundColor: '#E8F5E9',
  borderLeftColor: '#248A3D',
  iconColor: '#248A3D',
  textColor: '#1C1C1E',
}
```

**Warning:**
```typescript
// Light mode
{
  backgroundColor: '#FFF4E5',
  borderLeftColor: '#B25000',
  iconColor: '#B25000',
  textColor: '#1C1C1E',
}
```

**Info:**
```typescript
// Light mode
{
  backgroundColor: '#E3F2FD',
  borderLeftColor: '#0056B3',
  iconColor: '#0056B3',
  textColor: '#1C1C1E',
}
```

---

## Color blindness considerations

### Types and prevalence

| Type | Prevalence | Affected colors |
|------|------------|-----------------|
| Deuteranopia (green-blind) | 6% of males | Red/green confusion |
| Protanopia (red-blind) | 2% of males | Red appears dark |
| Tritanopia (blue-blind) | 0.01% | Blue/yellow confusion |

### Safe combinations

**Always pair color with another indicator:**
- Icon + color
- Pattern + color
- Text label + color
- Shape + color

**Instead of red/green:**
```typescript
// Bad: relies on red/green distinction
const error = '#FF0000';
const success = '#00FF00';

// Better: distinct hues + icons
const error = '#D70015';   // Red with icon
const success = '#0A84FF'; // Blue with checkmark

// Or use shapes
// Error: X icon + red
// Success: Checkmark icon + blue/green
```

**Problematic combinations to avoid:**
- Red + green without other indicators
- Red + brown
- Blue + purple
- Light green + yellow

### Testing tools

- **Sim Daltonism** (Mac app) - Live color blindness simulation
- **Color Oracle** (Mac/Windows) - System-wide simulation
- **Figma plugins** - Stark, Color Blind
- **Chrome DevTools** - Rendering > Emulate vision deficiencies

---

## Implementation

### Theme provider

```typescript
import { useColorScheme } from 'react-native';

const colors = {
  light: lightColors,
  dark: darkColors,
};

export function useThemeColors() {
  const colorScheme = useColorScheme();
  return colors[colorScheme ?? 'light'];
}
```

### Usage in components

```typescript
function MyComponent() {
  const colors = useThemeColors();

  return (
    <View style={{ backgroundColor: colors.background }}>
      <Text style={{ color: colors.textPrimary }}>
        Hello World
      </Text>
    </View>
  );
}
```

### Contrast check utility

```typescript
// Calculate relative luminance
function getLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Calculate contrast ratio
function getContrastRatio(color1: string, color2: string): number {
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Check if passes WCAG AA
function passesWCAG_AA(
  foreground: string,
  background: string,
  isLargeText: boolean = false
): boolean {
  const ratio = getContrastRatio(foreground, background);
  return isLargeText ? ratio >= 3 : ratio >= 4.5;
}

// Usage
passesWCAG_AA('#007AFF', '#FFFFFF'); // true (4.5:1)
passesWCAG_AA('#8E8E93', '#FFFFFF'); // false (3.9:1)
passesWCAG_AA('#8E8E93', '#FFFFFF', true); // true (large text)
```

---

## Quick checklist

Before using any color combination:

- [ ] Contrast ratio >= 4.5:1 for normal text
- [ ] Contrast ratio >= 3:1 for large text (18pt+ or 14pt bold)
- [ ] Contrast ratio >= 3:1 for UI components
- [ ] Information not conveyed by color alone
- [ ] Tested with color blindness simulator
- [ ] Works in both light and dark mode
- [ ] Focus states clearly visible
- [ ] Error states distinguishable from success

---

## Resources

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Contrast Checker](https://coolors.co/contrast-checker)
- [Apple Human Interface Guidelines - Color](https://developer.apple.com/design/human-interface-guidelines/color)
- [Material Design Color System](https://m3.material.io/styles/color)
- [Who Can Use](https://whocanuse.com/) - See how colors work for different vision types
