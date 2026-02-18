# Accessibility implementation guide

React Native accessibility for iOS and Android. WCAG 2.1 compliance focus.

---

## WCAG 2.1 mobile requirements

### Level A (minimum)

**Perceivable**
- Text alternatives for images (`accessibilityLabel`)
- Captions for video content
- Info and relationships conveyed programmatically
- Meaningful sequence preserved

**Operable**
- All functionality keyboard/switch accessible
- No timing traps
- Navigable content structure
- Focus order matches visual order

**Understandable**
- Readable language settings
- Predictable navigation patterns
- Input assistance for errors

**Robust**
- Compatible with assistive tech
- Name, role, value exposed correctly

### Level AA (target)

**Additional requirements**
- Color contrast 4.5:1 for normal text
- Color contrast 3:1 for large text (18pt+ or 14pt bold)
- Text resizable to 200% without loss
- Multiple ways to find content
- Visible focus indicators
- Consistent navigation
- Error identification and suggestions

### Level AAA (aspirational)

- 7:1 contrast ratio
- Sign language for video
- Extended audio description
- No timing limits

---

## iOS accessibility features

### VoiceOver

Screen reader. Reads aloud what user touches.

**React Native props:**
```tsx
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Add to cart"
  accessibilityHint="Adds this item to your shopping cart"
  accessibilityRole="button"
>
  <Icon name="plus" />
</TouchableOpacity>
```

### Supported roles

```typescript
type AccessibilityRole =
  | 'none'
  | 'button'
  | 'link'
  | 'search'
  | 'image'
  | 'keyboardkey'
  | 'text'
  | 'adjustable'
  | 'imagebutton'
  | 'header'
  | 'summary'
  | 'alert'
  | 'checkbox'
  | 'combobox'
  | 'menu'
  | 'menubar'
  | 'menuitem'
  | 'progressbar'
  | 'radio'
  | 'radiogroup'
  | 'scrollbar'
  | 'spinbutton'
  | 'switch'
  | 'tab'
  | 'tablist'
  | 'timer'
  | 'toolbar';
```

### Accessibility states

```tsx
<TouchableOpacity
  accessibilityState={{
    disabled: isDisabled,
    selected: isSelected,
    checked: isChecked, // for checkbox/radio
    busy: isLoading,
    expanded: isExpanded, // for accordions
  }}
>
```

### iOS-specific features

**Dynamic Type**
User adjusts system font size. Your app should respect it.

```tsx
import { Text, useWindowDimensions } from 'react-native';

// Use fontScale to detect user preference
const { fontScale } = useWindowDimensions();

// Alternatively, use allowFontScaling (default true)
<Text allowFontScaling={true}>Scales with system</Text>
<Text allowFontScaling={false}>Fixed size</Text>
```

**Reduce Motion**
```tsx
import { AccessibilityInfo } from 'react-native';

AccessibilityInfo.isReduceMotionEnabled().then((enabled) => {
  // Disable or simplify animations
});
```

**Bold Text**
```tsx
AccessibilityInfo.isBoldTextEnabled().then((enabled) => {
  // Use heavier font weights
});
```

**Invert Colors / Reduce Transparency**
System handles these. Ensure your app looks acceptable.

### Focus management

```tsx
import { useRef } from 'react';
import { AccessibilityInfo, findNodeHandle } from 'react-native';

const buttonRef = useRef(null);

// Move VoiceOver focus programmatically
const focusOnButton = () => {
  const node = findNodeHandle(buttonRef.current);
  if (node) {
    AccessibilityInfo.setAccessibilityFocus(node);
  }
};
```

### Announcing changes

```tsx
// Announce to screen reader
AccessibilityInfo.announceForAccessibility('Item added to cart');

// With priority (iOS 16+)
AccessibilityInfo.announceForAccessibilityWithOptions(
  'Error: Please enter a valid email',
  { queue: false } // Interrupts current speech
);
```

---

## Android accessibility features

### TalkBack

Android's screen reader. Similar props work.

**Android-specific props:**
```tsx
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Submit order"
  accessibilityHint="Double tap to submit your order"
  accessibilityRole="button"
  // Android-specific
  importantForAccessibility="yes" // or "no", "no-hide-descendants"
>
```

### accessibilityLiveRegion

For dynamic content updates:
```tsx
<View
  accessibilityLiveRegion="polite" // or "assertive", "none"
>
  <Text>{errorMessage}</Text>
</View>
```

- `polite`: Announces when screen reader is idle
- `assertive`: Interrupts current speech
- `none`: No announcement (default)

### Android-specific detection

```tsx
// Detect TalkBack
AccessibilityInfo.isScreenReaderEnabled().then((enabled) => {
  // Same method works for both platforms
});

// Android-specific accessibility services
import { NativeModules } from 'react-native';
const { AccessibilityModule } = NativeModules;
```

### Touch exploration

TalkBack users explore by touch. Ensure:
- Touch targets are 48x48dp minimum (Android guidelines)
- Elements have proper bounds
- Overlapping touchables are avoided

---

## Testing with screen readers

### VoiceOver (iOS)

**Enable:**
Settings > Accessibility > VoiceOver > On

Or: Triple-click side button (if configured)

**Basic gestures:**
| Gesture | Action |
|---------|--------|
| Single tap | Select and speak item |
| Double tap | Activate selected item |
| Swipe right | Move to next item |
| Swipe left | Move to previous item |
| Three-finger swipe | Scroll |
| Two-finger tap | Pause/resume speech |
| Two-finger Z | Go back |

**Testing checklist:**
1. Navigate entire screen left-to-right swipes
2. Verify reading order matches visual order
3. Check all interactive elements are reachable
4. Verify labels are meaningful (not "button" or "image")
5. Test form submission flow
6. Verify error messages are announced

### TalkBack (Android)

**Enable:**
Settings > Accessibility > TalkBack > On

Or: Hold both volume buttons (if configured)

**Basic gestures:**
| Gesture | Action |
|---------|--------|
| Single tap | Select and speak item |
| Double tap | Activate selected item |
| Swipe right | Move to next item |
| Swipe left | Move to previous item |
| Two-finger swipe | Scroll |
| Swipe down then right | Global context menu |

**Testing checklist:**
1. Navigate with swipe gestures
2. Use explore by touch
3. Verify custom actions work
4. Check heading navigation (swipe up/down)
5. Test with voice commands

---

## Common patterns

### Images

```tsx
// Decorative image (ignored by screen reader)
<Image
  source={decorativePattern}
  accessible={false}
  importantForAccessibility="no"
/>

// Informative image
<Image
  source={productPhoto}
  accessible={true}
  accessibilityLabel="Red running shoes, side view"
  accessibilityRole="image"
/>

// Image as button
<TouchableOpacity
  accessibilityLabel="Share product"
  accessibilityRole="imagebutton"
>
  <Image source={shareIcon} />
</TouchableOpacity>
```

### Form inputs

```tsx
<View>
  <Text nativeID="emailLabel">Email address</Text>
  <TextInput
    accessibilityLabelledBy="emailLabel" // Android
    accessibilityLabel="Email address" // iOS fallback
    accessibilityHint="Enter your email to receive updates"
    keyboardType="email-address"
    autoComplete="email"
    textContentType="emailAddress" // iOS autofill
  />
  {error && (
    <Text
      accessibilityLiveRegion="polite"
      accessibilityRole="alert"
    >
      {error}
    </Text>
  )}
</View>
```

### Navigation

```tsx
// Tab bar
<View accessibilityRole="tablist">
  {tabs.map((tab, index) => (
    <TouchableOpacity
      key={tab.id}
      accessibilityRole="tab"
      accessibilityLabel={tab.label}
      accessibilityState={{ selected: activeTab === index }}
    >
      <Text>{tab.label}</Text>
    </TouchableOpacity>
  ))}
</View>

// Screen header
<Text
  accessibilityRole="header"
  style={styles.screenTitle}
>
  Settings
</Text>
```

### Loading states

```tsx
<View
  accessible={true}
  accessibilityLabel={isLoading ? 'Loading content' : 'Content loaded'}
  accessibilityState={{ busy: isLoading }}
>
  {isLoading ? <ActivityIndicator /> : <Content />}
</View>
```

---

## Implementation priority

1. **Labels first** - Every interactive element needs a label
2. **Roles second** - Correct roles enable proper gestures
3. **States third** - Dynamic states (selected, disabled, etc.)
4. **Hints fourth** - Additional context when label isn't enough
5. **Announcements last** - For dynamic content changes

---

## Quick reference

### Must-have props for common elements

| Element | Required props |
|---------|---------------|
| Button | `accessibilityLabel`, `accessibilityRole="button"` |
| Link | `accessibilityLabel`, `accessibilityRole="link"` |
| Image | `accessibilityLabel` or `accessible={false}` |
| Input | `accessibilityLabel`, error announcements |
| Toggle | `accessibilityRole="switch"`, `accessibilityState` |
| Tab | `accessibilityRole="tab"`, `accessibilityState.selected` |
| Header | `accessibilityRole="header"` |
| Alert | `accessibilityRole="alert"`, `accessibilityLiveRegion` |

### Minimum touch targets

| Platform | Size |
|----------|------|
| iOS | 44x44 points |
| Android | 48x48 dp |
| WCAG | 44x44 CSS pixels |

When button content is smaller, add padding:
```tsx
<TouchableOpacity
  style={{ minWidth: 44, minHeight: 44, padding: 8 }}
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
>
  <Icon size={24} />
</TouchableOpacity>
```
