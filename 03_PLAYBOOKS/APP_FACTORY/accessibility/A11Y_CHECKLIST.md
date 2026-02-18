# Accessibility checklist

Use this checklist during development and QA. Each screen should pass all applicable items.

---

## Color contrast

### Text contrast ratios (WCAG AA)

| Element | Minimum ratio |
|---------|---------------|
| Normal text (< 18pt) | 4.5:1 |
| Large text (>= 18pt or 14pt bold) | 3:1 |
| UI components and graphics | 3:1 |
| Decorative elements | No requirement |

### Testing tools

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/) (desktop app)
- iOS: Settings > Accessibility > Display > Increase Contrast
- Android: Settings > Accessibility > High contrast text

### Checklist

- [ ] Body text meets 4.5:1 against background
- [ ] Headings meet 3:1 against background
- [ ] Button text meets 4.5:1 against button background
- [ ] Links are distinguishable from surrounding text
- [ ] Error states visible without color alone
- [ ] Success/warning states visible without color alone
- [ ] Icons have sufficient contrast
- [ ] Placeholder text meets 4.5:1 (or use labels instead)
- [ ] Focus indicators visible (3:1 minimum)

---

## Touch target sizes

### Minimum sizes

| Platform | Minimum size |
|----------|--------------|
| iOS | 44 x 44 points |
| Android | 48 x 48 dp |
| WCAG 2.1 | 44 x 44 CSS pixels |

### Implementation

```tsx
// Increase touch area without visual change
<TouchableOpacity
  style={{ width: 24, height: 24 }}
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
>
  <Icon size={24} />
</TouchableOpacity>

// Or use padding
<TouchableOpacity
  style={{ minWidth: 44, minHeight: 44, padding: 10 }}
>
  <Icon size={24} />
</TouchableOpacity>
```

### Checklist

- [ ] All buttons >= 44x44
- [ ] All interactive icons >= 44x44 (with hitSlop if needed)
- [ ] Form inputs >= 44 height
- [ ] Tab bar items >= 44x44
- [ ] List item touch areas span full width
- [ ] Adjacent targets have 8px minimum spacing
- [ ] No overlapping touch areas

---

## Focus management

### Requirements

- Logical focus order (matches visual order)
- All interactive elements focusable
- Focus visible on current element
- Focus trapped in modals
- Focus moves to new content (dialogs, screens)

### Implementation

```tsx
// Move focus programmatically
import { AccessibilityInfo, findNodeHandle } from 'react-native';

const ref = useRef(null);

useEffect(() => {
  if (isDialogOpen) {
    const node = findNodeHandle(ref.current);
    if (node) {
      AccessibilityInfo.setAccessibilityFocus(node);
    }
  }
}, [isDialogOpen]);
```

### Checklist

- [ ] Tab order matches visual reading order
- [ ] Focus indicator visible on all platforms
- [ ] Modal/dialog traps focus
- [ ] Modal close returns focus to trigger
- [ ] New screen focuses on title or first element
- [ ] Toast/snackbar doesn't steal focus
- [ ] Skip links available for repetitive navigation (web)
- [ ] No keyboard traps

---

## Error announcements

### Requirements

- Errors announced to screen readers
- Error messages associated with inputs
- Clear error descriptions
- Suggestions for fixing errors

### Implementation

```tsx
// Announce error immediately
useEffect(() => {
  if (error) {
    AccessibilityInfo.announceForAccessibility(`Error: ${error}`);
  }
}, [error]);

// Associate error with input
<View>
  <TextInput
    accessibilityLabel={`Email${error ? `, error: ${error}` : ''}`}
    aria-invalid={!!error}
  />
  <View accessibilityLiveRegion="polite">
    <Text>{error}</Text>
  </View>
</View>
```

### Checklist

- [ ] Form errors announced when they occur
- [ ] Error text readable by screen reader
- [ ] Error associated with field (via label or live region)
- [ ] Error suggestions provided when possible
- [ ] Success messages announced
- [ ] Network errors announced
- [ ] Validation happens on blur, not on every keystroke

---

## Dynamic content updates

### Live regions

```tsx
// Polite: waits for screen reader to finish
<View accessibilityLiveRegion="polite">
  <Text>{cartCount} items in cart</Text>
</View>

// Assertive: interrupts immediately
<View accessibilityLiveRegion="assertive">
  <Text>Connection lost</Text>
</View>
```

### Checklist

- [ ] Loading states announced
- [ ] Content updates announced (polite)
- [ ] Errors announced (assertive)
- [ ] Cart/counter updates announced
- [ ] Navigation transitions announced
- [ ] Pull-to-refresh status announced
- [ ] Infinite scroll new content announced
- [ ] Timer/countdown updates announced (sparingly)

---

## Form accessibility

### Checklist

- [ ] All inputs have visible labels
- [ ] Labels associated with inputs (accessibilityLabel or nativeID)
- [ ] Required fields marked (visual + programmatic)
- [ ] Password fields have proper type
- [ ] Auto-complete enabled where appropriate
- [ ] Error messages clear and helpful
- [ ] Successful submission confirmed
- [ ] Cancel/back actions easily accessible
- [ ] Multi-step forms show progress

### Input configuration

```tsx
<TextInput
  accessibilityLabel="Email address"
  accessibilityHint="Enter your work email"
  keyboardType="email-address"
  autoComplete="email"
  textContentType="emailAddress" // iOS
  autoCapitalize="none"
  autoCorrect={false}
/>
```

---

## Images and icons

### Checklist

- [ ] Informative images have alt text
- [ ] Decorative images hidden (accessible={false})
- [ ] Icon-only buttons have labels
- [ ] Complex images have long descriptions
- [ ] Charts have text alternatives
- [ ] Image loading states handled

### Pattern

```tsx
// Informative
<Image
  source={chart}
  accessibilityLabel="Sales chart showing 40% growth"
  accessibilityRole="image"
/>

// Decorative
<Image
  source={pattern}
  accessible={false}
  importantForAccessibility="no"
/>

// Icon button
<TouchableOpacity
  accessibilityLabel="Add to favorites"
  accessibilityRole="button"
>
  <HeartIcon />
</TouchableOpacity>
```

---

## Navigation

### Checklist

- [ ] Screen titles announced on navigation
- [ ] Back button labeled
- [ ] Tab bar items labeled
- [ ] Current tab indicated (accessibilityState.selected)
- [ ] Drawer/menu accessible
- [ ] Nested navigation clear
- [ ] Deep links announce destination

### React Navigation setup

```tsx
<Stack.Screen
  name="ProductDetail"
  component={ProductDetailScreen}
  options={{
    headerTitle: 'Product Details',
    // This title is announced by screen readers
  }}
/>
```

---

## Media

### Checklist

- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Auto-play disabled or easily stopped
- [ ] Volume controls accessible
- [ ] Progress controls accessible
- [ ] No audio over 3 seconds auto-plays

---

## Motion and animations

### Checklist

- [ ] Respect reduceMotion preference
- [ ] No auto-playing animations > 5 seconds
- [ ] Pause/stop controls for animations
- [ ] No content that flashes > 3 times per second
- [ ] Parallax/motion effects optional

### Implementation

```tsx
const reduceMotion = useReduceMotion();

<Animated.View
  style={{
    opacity: reduceMotion ? 1 : animatedOpacity,
  }}
/>
```

---

## Testing protocol

### Before each release

1. **Automated tests**
   - Run accessibility linting (eslint-plugin-react-native-a11y)
   - Check contrast ratios
   - Verify touch targets programmatically

2. **Manual VoiceOver test (iOS)**
   - Navigate entire app with swipes
   - Complete all user flows
   - Verify all labels meaningful
   - Test with eyes closed

3. **Manual TalkBack test (Android)**
   - Navigate entire app with swipes
   - Test explore by touch
   - Complete all user flows

4. **Keyboard navigation (if applicable)**
   - Tab through all interactive elements
   - Verify focus visible
   - Test Enter/Space activation

5. **Visual tests**
   - Test with large font scale (200%)
   - Test with bold text enabled
   - Test in dark mode
   - Test with inverted colors
   - Test with reduced motion

---

## Severity levels

| Level | Description | Resolution |
|-------|-------------|------------|
| Critical | Blocks user from completing task | Must fix before release |
| Major | Significant difficulty, workaround exists | Fix in current sprint |
| Minor | Inconvenient but doesn't block | Fix in next sprint |
| Enhancement | Improvement opportunity | Add to backlog |

### Examples

**Critical:**
- Button has no accessible label
- Modal cannot be closed with screen reader
- Form cannot be submitted

**Major:**
- Contrast ratio slightly below 4.5:1
- Touch target 40px instead of 44px
- Focus order confusing

**Minor:**
- Hint text could be more helpful
- Animation doesn't respect reduce motion

**Enhancement:**
- Could add skip navigation link
- Headings could be more descriptive
