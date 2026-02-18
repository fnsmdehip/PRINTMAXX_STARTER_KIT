import React, { useRef, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  TextInputProps,
  AccessibilityInfo,
  Platform,
} from 'react-native';

interface AccessibleInputProps extends Omit<TextInputProps, 'accessibilityLabel'> {
  // Required
  label: string;

  // Optional accessibility
  hint?: string;
  errorMessage?: string;
  required?: boolean;

  // Display
  helperText?: string;
  showLabel?: boolean;

  // Refs
  inputRef?: React.RefObject<TextInput>;

  testID?: string;
}

export function AccessibleInput({
  label,
  hint,
  errorMessage,
  required = false,
  helperText,
  showLabel = true,
  inputRef,
  testID,
  style,
  ...textInputProps
}: AccessibleInputProps) {
  const internalRef = useRef<TextInput>(null);
  const ref = inputRef || internalRef;
  const [isFocused, setIsFocused] = useState(false);

  // Generate unique IDs for accessibility relationships
  const labelId = `${label.replace(/\s+/g, '-')}-label`;
  const errorId = `${label.replace(/\s+/g, '-')}-error`;
  const helperId = `${label.replace(/\s+/g, '-')}-helper`;

  // Build accessibility label
  let accessibilityLabel = label;
  if (required) {
    accessibilityLabel += ', required';
  }
  if (errorMessage) {
    accessibilityLabel += `, error: ${errorMessage}`;
  }

  // Announce errors when they appear
  React.useEffect(() => {
    if (errorMessage) {
      AccessibilityInfo.announceForAccessibility(`Error: ${errorMessage}`);
    }
  }, [errorMessage]);

  const hasError = !!errorMessage;

  return (
    <View style={styles.container}>
      {/* Visible label */}
      {showLabel && (
        <Text
          nativeID={labelId}
          style={[styles.label, hasError && styles.labelError]}
        >
          {label}
          {required && <Text style={styles.required}> *</Text>}
        </Text>
      )}

      {/* Input field */}
      <TextInput
        ref={ref}
        accessible={true}
        accessibilityLabel={accessibilityLabel}
        accessibilityHint={hint}
        accessibilityState={{
          disabled: textInputProps.editable === false,
        }}
        // Android: link to visible label
        {...(Platform.OS === 'android' && { accessibilityLabelledBy: labelId })}
        // Error state
        aria-invalid={hasError}
        style={[
          styles.input,
          isFocused && styles.inputFocused,
          hasError && styles.inputError,
          textInputProps.editable === false && styles.inputDisabled,
          style,
        ]}
        onFocus={(e) => {
          setIsFocused(true);
          textInputProps.onFocus?.(e);
        }}
        onBlur={(e) => {
          setIsFocused(false);
          textInputProps.onBlur?.(e);
        }}
        testID={testID}
        {...textInputProps}
      />

      {/* Helper text */}
      {helperText && !hasError && (
        <Text
          nativeID={helperId}
          style={styles.helperText}
        >
          {helperText}
        </Text>
      )}

      {/* Error message */}
      {hasError && (
        <View
          accessibilityRole="alert"
          accessibilityLiveRegion="polite"
        >
          <Text
            nativeID={errorId}
            style={styles.errorText}
          >
            {errorMessage}
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },

  label: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1C1C1E',
    marginBottom: 8,
  },

  labelError: {
    color: '#FF3B30',
  },

  required: {
    color: '#FF3B30',
  },

  input: {
    height: 48, // Meets minimum touch target
    borderWidth: 1,
    borderColor: '#C7C7CC',
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    color: '#1C1C1E',
    backgroundColor: '#FFFFFF',
  },

  inputFocused: {
    borderColor: '#007AFF',
    borderWidth: 2,
  },

  inputError: {
    borderColor: '#FF3B30',
    borderWidth: 2,
  },

  inputDisabled: {
    backgroundColor: '#F2F2F7',
    color: '#8E8E93',
  },

  helperText: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 4,
  },

  errorText: {
    fontSize: 14,
    color: '#FF3B30',
    marginTop: 4,
  },
});

// Usage examples:
/*
// Basic input
<AccessibleInput
  label="Email address"
  hint="We'll never share your email"
  keyboardType="email-address"
  autoComplete="email"
  textContentType="emailAddress"
  value={email}
  onChangeText={setEmail}
/>

// Required field with error
<AccessibleInput
  label="Password"
  required={true}
  secureTextEntry={true}
  autoComplete="password"
  textContentType="password"
  value={password}
  onChangeText={setPassword}
  errorMessage={passwordError}
/>

// With helper text
<AccessibleInput
  label="Username"
  helperText="3-20 characters, letters and numbers only"
  autoCapitalize="none"
  autoCorrect={false}
  value={username}
  onChangeText={setUsername}
/>

// Disabled input
<AccessibleInput
  label="Account ID"
  value={accountId}
  editable={false}
/>

// Hidden label (for search bars, etc.)
<AccessibleInput
  label="Search products"
  showLabel={false}
  placeholder="Search..."
  returnKeyType="search"
  onSubmitEditing={handleSearch}
/>
*/
