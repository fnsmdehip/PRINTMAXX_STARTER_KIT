# Screen reader testing guide

Practical testing steps for VoiceOver and TalkBack.

---

## VoiceOver testing (iOS)

### Setup

**Enable VoiceOver:**
1. Settings > Accessibility > VoiceOver > On
2. Or: Settings > Accessibility > Accessibility Shortcut > VoiceOver
   - Then triple-click side button to toggle

**Recommended settings:**
- Speaking Rate: 50-70% (faster for testing)
- Verbosity: Medium
- Typing: Direct Touch Typing (for testing keyboards)

### Basic gestures

| Gesture | Action |
|---------|--------|
| Tap | Select and announce item |
| Double tap | Activate selected item |
| Triple tap | Double-tap the item |
| Swipe right | Move to next element |
| Swipe left | Move to previous element |
| Swipe up | Increase value / Previous rotor option |
| Swipe down | Decrease value / Next rotor option |
| Two-finger tap | Pause/resume speech |
| Two-finger swipe up | Read all from top |
| Two-finger swipe down | Read all from current position |
| Three-finger swipe left/right | Scroll |
| Two-finger Z-gesture | Go back |

### The rotor

The rotor provides quick navigation options.

**Access:** Two-finger rotation gesture (like turning a dial)

**Rotor options:**
- Headings - Jump between headers
- Links - Navigate links
- Form Controls - Jump to form fields
- Containers - Navigate between sections
- Characters - Read character by character
- Words - Read word by word

**Use swipe up/down** to move between rotor items.

### Testing checklist

**Navigation flow:**
- [ ] Open app, VoiceOver announces screen title
- [ ] Swipe right through all elements
- [ ] Order matches visual layout
- [ ] Nothing gets skipped
- [ ] No duplicate announcements
- [ ] Back button accessible and labeled

**Labels:**
- [ ] Every button has meaningful label (not "button" or "image")
- [ ] Every image has description or is hidden
- [ ] Every input has label
- [ ] Labels are concise but complete

**State announcements:**
- [ ] "Selected" announced for selected items
- [ ] "Disabled" announced for disabled items
- [ ] "Checked/unchecked" for checkboxes
- [ ] "On/off" for switches

**Roles:**
- [ ] Buttons announced as "button"
- [ ] Links announced as "link"
- [ ] Headings work with rotor navigation
- [ ] Tabs announced as "tab"

**Forms:**
- [ ] Can navigate to all inputs
- [ ] Can enter text
- [ ] Errors announced when they occur
- [ ] Can submit form

**Dynamic content:**
- [ ] Loading states announced
- [ ] Success/error messages announced
- [ ] List updates announced (sparingly)

**Modals and dialogs:**
- [ ] Focus moves to modal when opened
- [ ] Cannot navigate outside modal
- [ ] Close button accessible
- [ ] Focus returns to trigger when closed

### Testing script

Run through this exact flow:

1. **Launch and navigate**
   - Open app
   - Note what's announced
   - Swipe right through home screen
   - Note all announcements

2. **Complete a task**
   - Navigate to a key feature
   - Complete a user flow (e.g., add to cart, submit form)
   - Note any blockers or confusing moments

3. **Test forms**
   - Navigate to a form
   - Tab through all fields
   - Enter data in each field
   - Trigger validation error
   - Submit form

4. **Test navigation**
   - Move between tabs/screens
   - Test back navigation
   - Test drawer/menu if present

5. **Document issues**
   - Screen name
   - Element description
   - What was announced
   - What should be announced
   - Severity

---

## TalkBack testing (Android)

### Setup

**Enable TalkBack:**
1. Settings > Accessibility > TalkBack > On
2. Or: Hold both volume buttons for 3 seconds (if enabled)

**Recommended settings:**
- Speech rate: Slightly faster for testing
- Verbosity: Default or Custom
- Tutorial: Complete it first if unfamiliar

### Basic gestures

| Gesture | Action |
|---------|--------|
| Tap | Select and announce item |
| Double tap | Activate selected item |
| Swipe right | Move to next element |
| Swipe left | Move to previous element |
| Swipe up then down | Global context menu |
| Swipe down then up | Local context menu |
| Swipe down then right | Open TalkBack menu |
| Two-finger swipe | Scroll |
| Two-finger tap | Pause/resume |

### Reading controls

Access via swipe down then up (local context menu):
- Characters
- Words
- Lines
- Paragraphs
- Headings
- Links
- Controls

Then swipe up/down to move between items of that type.

### Testing checklist

**Navigation:**
- [ ] App opens with meaningful announcement
- [ ] Can explore by touch (tap and drag)
- [ ] Can navigate with swipes
- [ ] Logical reading order

**Labels:**
- [ ] Content descriptions present
- [ ] No "unlabeled" announcements
- [ ] Icons and images described

**State:**
- [ ] Selected/unselected announced
- [ ] Disabled announced
- [ ] Expandable announced

**Actions:**
- [ ] Custom actions available where needed
- [ ] Long press actions accessible
- [ ] Context menus accessible

**Forms:**
- [ ] Can navigate to all fields
- [ ] Can enter text
- [ ] Keyboard accessible
- [ ] Errors announced

**Live regions:**
- [ ] Dynamic updates announced
- [ ] Polite vs assertive appropriate

### Testing script

1. **Explore screen**
   - Touch and hold anywhere
   - Drag finger around screen
   - Note what's announced at each position

2. **Linear navigation**
   - Start at top
   - Swipe right repeatedly
   - Note everything announced

3. **Heading navigation**
   - Open reading controls (swipe down then up)
   - Select "Headings"
   - Swipe down/up to jump between headings

4. **Complete task**
   - Navigate to key feature
   - Complete entire flow with TalkBack
   - Note blockers

5. **Test keyboard** (if physical keyboard attached)
   - Tab through elements
   - Enter/Space to activate
   - Arrow keys in lists

---

## Common issues and fixes

### Issue: Button announced as just "button"

**Problem:** No accessibilityLabel

**Fix:**
```tsx
// Before
<TouchableOpacity>
  <Icon name="plus" />
</TouchableOpacity>

// After
<TouchableOpacity
  accessibilityLabel="Add item"
  accessibilityRole="button"
>
  <Icon name="plus" />
</TouchableOpacity>
```

### Issue: Image announced as "image"

**Problem:** Missing description

**Fix:**
```tsx
// Before
<Image source={productImage} />

// After - if informative
<Image
  source={productImage}
  accessibilityLabel="Red sneakers, side view"
/>

// After - if decorative
<Image
  source={decorativeImage}
  accessible={false}
/>
```

### Issue: Input has no label

**Problem:** Missing accessibilityLabel

**Fix:**
```tsx
// Before
<TextInput placeholder="Email" />

// After
<TextInput
  accessibilityLabel="Email address"
  placeholder="Email"
/>
```

### Issue: State not announced

**Problem:** Missing accessibilityState

**Fix:**
```tsx
// Before
<TouchableOpacity style={selected && styles.selected}>

// After
<TouchableOpacity
  accessibilityState={{ selected }}
  style={selected && styles.selected}
>
```

### Issue: List items confusing

**Problem:** Each element announced separately

**Fix:**
```tsx
// Before - three separate announcements
<View>
  <Image source={avatar} />
  <Text>{name}</Text>
  <Text>{status}</Text>
</View>

// After - single announcement
<View
  accessible={true}
  accessibilityLabel={`${name}, ${status}`}
>
  <Image source={avatar} accessible={false} />
  <Text>{name}</Text>
  <Text>{status}</Text>
</View>
```

### Issue: Focus jumps unexpectedly

**Problem:** Focus not managed on navigation

**Fix:**
```tsx
useEffect(() => {
  if (isVisible) {
    const node = findNodeHandle(titleRef.current);
    if (node) {
      AccessibilityInfo.setAccessibilityFocus(node);
    }
  }
}, [isVisible]);
```

### Issue: Error not announced

**Problem:** No live region

**Fix:**
```tsx
// Before
{error && <Text style={styles.error}>{error}</Text>}

// After
{error && (
  <View accessibilityLiveRegion="assertive">
    <Text style={styles.error}>{error}</Text>
  </View>
)}

// Or announce programmatically
useEffect(() => {
  if (error) {
    AccessibilityInfo.announceForAccessibility(`Error: ${error}`);
  }
}, [error]);
```

### Issue: Modal content accessible behind modal

**Problem:** Focus not trapped

**Fix:**
```tsx
// Use Modal component (traps focus by default)
<Modal visible={isOpen}>
  <View>
    <Text ref={titleRef}>Modal Title</Text>
    {/* Modal content */}
  </View>
</Modal>

// Or use accessibilityViewIsModal (iOS)
<View accessibilityViewIsModal={true}>
  {/* Modal content */}
</View>
```

### Issue: Custom gesture not accessible

**Problem:** Swipe/pinch gesture has no alternative

**Fix:**
```tsx
// Provide button alternative
<View>
  {/* Swipeable item */}
  <SwipeableRow onSwipeLeft={handleDelete}>
    <ListItem />
  </SwipeableRow>

  {/* Accessible alternative (shown for screen reader users) */}
  {screenReaderEnabled && (
    <TouchableOpacity
      accessibilityLabel="Delete item"
      onPress={handleDelete}
    >
      <Text>Delete</Text>
    </TouchableOpacity>
  )}
</View>
```

---

## Testing tools

### iOS

- **Accessibility Inspector** (Xcode > Open Developer Tool)
  - Inspect elements
  - View labels, roles, values
  - Simulate VoiceOver navigation

- **VoiceOver rotor** (use in simulator)
  - Settings > Accessibility > VoiceOver
  - Two-finger rotation gesture

### Android

- **Accessibility Scanner** (Google Play)
  - Scans for issues
  - Suggests fixes
  - Screenshots with highlights

- **Layout Inspector** (Android Studio)
  - View accessibility properties
  - Check content descriptions

### Cross-platform

- **eslint-plugin-react-native-a11y**
  - Lint rules for accessibility
  - Catches missing labels

- **@testing-library/react-native**
  - Query by accessibility label
  - Test accessible interactions

```tsx
import { render, screen } from '@testing-library/react-native';

test('button has accessible label', () => {
  render(<MyButton />);
  expect(screen.getByLabelText('Submit form')).toBeTruthy();
});
```

---

## Documentation template

Use this when reporting issues:

```
Screen: [Screen name]
Element: [Element description]
Issue: [What's wrong]
Expected: [What should happen]
Actual: [What actually happens]
Severity: [Critical/Major/Minor]
Platform: [iOS/Android/Both]
Steps to reproduce:
1. [Step 1]
2. [Step 2]
Screenshot: [If applicable]
Suggested fix: [If known]
```
