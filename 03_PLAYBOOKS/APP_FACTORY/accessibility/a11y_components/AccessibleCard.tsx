import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
  AccessibilityRole,
} from 'react-native';

interface AccessibleCardProps {
  // Content
  children: React.ReactNode;

  // Accessibility
  label?: string;
  hint?: string;
  role?: AccessibilityRole;

  // Interaction
  onPress?: () => void;
  disabled?: boolean;
  selected?: boolean;

  // Styling
  style?: ViewStyle;
  testID?: string;
}

export function AccessibleCard({
  children,
  label,
  hint,
  role = 'button',
  onPress,
  disabled = false,
  selected = false,
  style,
  testID,
}: AccessibleCardProps) {
  const isInteractive = !!onPress;

  // For interactive cards, wrap in TouchableOpacity
  if (isInteractive) {
    return (
      <TouchableOpacity
        accessible={true}
        accessibilityLabel={label}
        accessibilityHint={hint}
        accessibilityRole={role}
        accessibilityState={{
          disabled,
          selected,
        }}
        onPress={onPress}
        disabled={disabled}
        activeOpacity={0.7}
        style={[
          styles.card,
          selected && styles.cardSelected,
          disabled && styles.cardDisabled,
          style,
        ]}
        testID={testID}
      >
        {children}
      </TouchableOpacity>
    );
  }

  // For non-interactive cards, use View
  return (
    <View
      accessible={!!label}
      accessibilityLabel={label}
      accessibilityRole="summary"
      style={[styles.card, style]}
      testID={testID}
    >
      {children}
    </View>
  );
}

// Card sub-components for consistent structure

interface CardHeaderProps {
  title: string;
  subtitle?: string;
  rightElement?: React.ReactNode;
  style?: ViewStyle;
}

export function CardHeader({
  title,
  subtitle,
  rightElement,
  style,
}: CardHeaderProps) {
  return (
    <View style={[styles.cardHeader, style]}>
      <View style={styles.cardHeaderText}>
        <Text
          accessibilityRole="header"
          style={styles.cardTitle}
        >
          {title}
        </Text>
        {subtitle && (
          <Text style={styles.cardSubtitle}>
            {subtitle}
          </Text>
        )}
      </View>
      {rightElement && (
        <View style={styles.cardHeaderRight}>
          {rightElement}
        </View>
      )}
    </View>
  );
}

interface CardContentProps {
  children: React.ReactNode;
  style?: ViewStyle;
}

export function CardContent({ children, style }: CardContentProps) {
  return (
    <View style={[styles.cardContent, style]}>
      {children}
    </View>
  );
}

interface CardFooterProps {
  children: React.ReactNode;
  style?: ViewStyle;
}

export function CardFooter({ children, style }: CardFooterProps) {
  return (
    <View style={[styles.cardFooter, style]}>
      {children}
    </View>
  );
}

// Specialized card variants

interface ProductCardProps {
  title: string;
  price: string;
  image: React.ReactNode;
  rating?: number;
  reviewCount?: number;
  onPress: () => void;
  style?: ViewStyle;
  testID?: string;
}

export function ProductCard({
  title,
  price,
  image,
  rating,
  reviewCount,
  onPress,
  style,
  testID,
}: ProductCardProps) {
  // Build comprehensive label for screen readers
  let accessibilityLabel = `${title}, ${price}`;
  if (rating !== undefined && reviewCount !== undefined) {
    accessibilityLabel += `, ${rating} out of 5 stars, ${reviewCount} reviews`;
  }

  return (
    <AccessibleCard
      label={accessibilityLabel}
      hint="Double tap to view product details"
      onPress={onPress}
      style={[styles.productCard, style]}
      testID={testID}
    >
      <View style={styles.productImageContainer}>
        {image}
      </View>
      <CardContent>
        <Text style={styles.productTitle} numberOfLines={2}>
          {title}
        </Text>
        <Text style={styles.productPrice}>{price}</Text>
        {rating !== undefined && reviewCount !== undefined && (
          <View style={styles.ratingContainer}>
            <Text style={styles.ratingText}>
              {rating} stars ({reviewCount} reviews)
            </Text>
          </View>
        )}
      </CardContent>
    </AccessibleCard>
  );
}

interface ListItemCardProps {
  title: string;
  description?: string;
  leftElement?: React.ReactNode;
  rightElement?: React.ReactNode;
  onPress?: () => void;
  disabled?: boolean;
  style?: ViewStyle;
  testID?: string;
}

export function ListItemCard({
  title,
  description,
  leftElement,
  rightElement,
  onPress,
  disabled = false,
  style,
  testID,
}: ListItemCardProps) {
  const accessibilityLabel = description
    ? `${title}, ${description}`
    : title;

  return (
    <AccessibleCard
      label={accessibilityLabel}
      hint={onPress ? 'Double tap to select' : undefined}
      onPress={onPress}
      disabled={disabled}
      style={[styles.listItemCard, style]}
      testID={testID}
    >
      {leftElement && (
        <View style={styles.listItemLeft}>
          {leftElement}
        </View>
      )}
      <View style={styles.listItemContent}>
        <Text style={styles.listItemTitle}>{title}</Text>
        {description && (
          <Text style={styles.listItemDescription}>{description}</Text>
        )}
      </View>
      {rightElement && (
        <View style={styles.listItemRight}>
          {rightElement}
        </View>
      )}
    </AccessibleCard>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    overflow: 'hidden',
  },

  cardSelected: {
    borderWidth: 2,
    borderColor: '#007AFF',
  },

  cardDisabled: {
    opacity: 0.5,
  },

  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },

  cardHeaderText: {
    flex: 1,
  },

  cardHeaderRight: {
    marginLeft: 12,
  },

  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1C1C1E',
  },

  cardSubtitle: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 2,
  },

  cardContent: {
    padding: 16,
  },

  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#F2F2F7',
    gap: 12,
  },

  // Product card
  productCard: {
    width: '100%',
  },

  productImageContainer: {
    aspectRatio: 1,
    backgroundColor: '#F2F2F7',
  },

  productTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1C1C1E',
  },

  productPrice: {
    fontSize: 18,
    fontWeight: '600',
    color: '#007AFF',
    marginTop: 4,
  },

  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },

  ratingText: {
    fontSize: 14,
    color: '#8E8E93',
  },

  // List item card
  listItemCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    minHeight: 64,
  },

  listItemLeft: {
    marginRight: 12,
  },

  listItemContent: {
    flex: 1,
  },

  listItemTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1C1C1E',
  },

  listItemDescription: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 2,
  },

  listItemRight: {
    marginLeft: 12,
  },
});

// Usage examples:
/*
// Basic interactive card
<AccessibleCard
  label="Order #12345, shipped on January 15"
  hint="Double tap to view order details"
  onPress={() => navigateToOrder('12345')}
>
  <CardHeader title="Order #12345" subtitle="Shipped" />
  <CardContent>
    <Text>3 items</Text>
  </CardContent>
</AccessibleCard>

// Non-interactive card
<AccessibleCard label="Monthly summary">
  <CardHeader title="January 2024" />
  <CardContent>
    <Text>Revenue: $1,234</Text>
  </CardContent>
</AccessibleCard>

// Product card
<ProductCard
  title="Nike Air Max 90"
  price="$129.99"
  image={<ProductImage source={productImage} productName="Nike Air Max 90" />}
  rating={4.5}
  reviewCount={123}
  onPress={() => navigateToProduct(productId)}
/>

// List item card
<ListItemCard
  title="John Smith"
  description="Last active 2 hours ago"
  leftElement={<Avatar source={avatarUrl} name="John Smith" />}
  rightElement={<ChevronIcon />}
  onPress={() => navigateToProfile(userId)}
/>
*/
