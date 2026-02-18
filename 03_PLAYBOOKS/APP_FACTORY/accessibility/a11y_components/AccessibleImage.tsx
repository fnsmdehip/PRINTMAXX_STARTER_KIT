import React from 'react';
import {
  Image,
  ImageProps,
  View,
  StyleSheet,
  ViewStyle,
} from 'react-native';

interface AccessibleImageProps extends Omit<ImageProps, 'accessible' | 'accessibilityLabel'> {
  // Required: describe the image content for screen readers
  alt: string;

  // Set to true for purely decorative images
  decorative?: boolean;

  // Container styling
  containerStyle?: ViewStyle;

  testID?: string;
}

export function AccessibleImage({
  alt,
  decorative = false,
  containerStyle,
  testID,
  style,
  ...imageProps
}: AccessibleImageProps) {
  // Decorative images should be hidden from screen readers
  if (decorative) {
    return (
      <Image
        accessible={false}
        importantForAccessibility="no"
        accessibilityElementsHidden={true}
        style={style}
        testID={testID}
        {...imageProps}
      />
    );
  }

  // Informative images need proper labeling
  return (
    <View style={containerStyle}>
      <Image
        accessible={true}
        accessibilityLabel={alt}
        accessibilityRole="image"
        style={style}
        testID={testID}
        {...imageProps}
      />
    </View>
  );
}

// Specialized components for common patterns

interface ProductImageProps {
  source: ImageProps['source'];
  productName: string;
  angle?: string;
  style?: ImageProps['style'];
  testID?: string;
}

export function ProductImage({
  source,
  productName,
  angle = '',
  style,
  testID,
}: ProductImageProps) {
  const alt = angle
    ? `${productName}, ${angle} view`
    : productName;

  return (
    <AccessibleImage
      source={source}
      alt={alt}
      style={[styles.productImage, style]}
      resizeMode="contain"
      testID={testID}
    />
  );
}

interface AvatarProps {
  source: ImageProps['source'];
  name: string;
  size?: 'small' | 'medium' | 'large';
  style?: ImageProps['style'];
  testID?: string;
}

export function Avatar({
  source,
  name,
  size = 'medium',
  style,
  testID,
}: AvatarProps) {
  const sizeStyles = {
    small: styles.avatarSmall,
    medium: styles.avatarMedium,
    large: styles.avatarLarge,
  };

  return (
    <AccessibleImage
      source={source}
      alt={`${name}'s profile picture`}
      style={[styles.avatar, sizeStyles[size], style]}
      testID={testID}
    />
  );
}

interface IconImageProps {
  source: ImageProps['source'];
  label: string;
  size?: number;
  style?: ImageProps['style'];
  testID?: string;
}

export function IconImage({
  source,
  label,
  size = 24,
  style,
  testID,
}: IconImageProps) {
  return (
    <AccessibleImage
      source={source}
      alt={label}
      style={[{ width: size, height: size }, style]}
      testID={testID}
    />
  );
}

interface BackgroundImageProps {
  source: ImageProps['source'];
  children: React.ReactNode;
  style?: ViewStyle;
  imageStyle?: ImageProps['style'];
  testID?: string;
}

export function BackgroundImage({
  source,
  children,
  style,
  imageStyle,
  testID,
}: BackgroundImageProps) {
  // Background images are decorative - content inside provides meaning
  return (
    <View style={[styles.backgroundContainer, style]}>
      <Image
        source={source}
        accessible={false}
        importantForAccessibility="no"
        accessibilityElementsHidden={true}
        style={[styles.backgroundImage, imageStyle]}
        testID={testID}
      />
      <View style={styles.backgroundContent}>
        {children}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  productImage: {
    width: '100%',
    aspectRatio: 1,
  },

  avatar: {
    borderRadius: 999,
  },

  avatarSmall: {
    width: 32,
    height: 32,
  },

  avatarMedium: {
    width: 48,
    height: 48,
  },

  avatarLarge: {
    width: 80,
    height: 80,
  },

  backgroundContainer: {
    position: 'relative',
  },

  backgroundImage: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    resizeMode: 'cover',
  },

  backgroundContent: {
    position: 'relative',
    zIndex: 1,
  },
});

// Usage examples:
/*
// Informative image
<AccessibleImage
  source={{ uri: 'https://example.com/chart.png' }}
  alt="Sales chart showing 40% growth in Q4 2024"
/>

// Decorative image (ignored by screen readers)
<AccessibleImage
  source={require('./decorative-pattern.png')}
  decorative={true}
/>

// Product image
<ProductImage
  source={{ uri: product.imageUrl }}
  productName="Nike Air Max 90"
  angle="side"
/>

// User avatar
<Avatar
  source={{ uri: user.avatarUrl }}
  name="John Smith"
  size="large"
/>

// Icon
<IconImage
  source={require('./settings-icon.png')}
  label="Settings"
  size={24}
/>

// Background image with content
<BackgroundImage source={require('./hero-bg.jpg')}>
  <Text>Hero content goes here</Text>
</BackgroundImage>
*/
