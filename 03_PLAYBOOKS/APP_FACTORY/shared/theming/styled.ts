/**
 * Styled Components Setup
 * Type-safe styling utilities with theme access
 */

import type { CSSProperties } from 'react';
import type { Theme } from './themes';

// CSS property value types
type CSSValue = string | number;

// Style object type
export type StyleObject = CSSProperties;

// Variant definition type
export interface VariantDefinition<V extends string = string> {
  base?: StyleObject;
  variants: Record<V, StyleObject>;
  defaultVariant?: V;
}

// Component variants type
export type ComponentVariants<T extends VariantDefinition> = {
  variant?: keyof T['variants'];
};

/**
 * Create a style function that has access to theme
 */
export function createThemedStyle<P extends object = object>(
  styleFn: (theme: Theme, props: P) => StyleObject
): (theme: Theme, props: P) => StyleObject {
  return styleFn;
}

/**
 * Create variant styles for a component
 */
export function createVariants<V extends string>(
  definition: VariantDefinition<V>
): VariantDefinition<V> {
  return definition;
}

/**
 * Get variant style from definition
 */
export function getVariantStyle<V extends string>(
  definition: VariantDefinition<V>,
  variant?: V
): StyleObject {
  const selectedVariant = variant ?? definition.defaultVariant;

  if (!selectedVariant) {
    return definition.base ?? {};
  }

  return {
    ...definition.base,
    ...definition.variants[selectedVariant],
  };
}

/**
 * Merge multiple style objects
 */
export function mergeStyles(...styles: (StyleObject | undefined | null | false)[]): StyleObject {
  return styles.reduce<StyleObject>((merged, style) => {
    if (!style) return merged;
    return { ...merged, ...style };
  }, {});
}

/**
 * Create a conditional style
 */
export function conditionalStyle(
  condition: boolean,
  trueStyle: StyleObject,
  falseStyle?: StyleObject
): StyleObject {
  return condition ? trueStyle : (falseStyle ?? {});
}

/**
 * Helper to access theme colors with dot notation
 */
export function themeColor(
  theme: Theme,
  path: string
): string | undefined {
  const parts = path.split('.');
  let value: unknown = theme.colors;

  for (const part of parts) {
    if (value && typeof value === 'object' && part in value) {
      value = (value as Record<string, unknown>)[part];
    } else {
      return undefined;
    }
  }

  return typeof value === 'string' ? value : undefined;
}

/**
 * Helper to create CSS custom properties from theme
 */
export function createCSSVariables(theme: Theme): Record<string, string> {
  const variables: Record<string, string> = {};

  // Flatten colors
  function flattenObject(obj: object, prefix: string = ''): void {
    for (const [key, value] of Object.entries(obj)) {
      const varName = prefix ? `${prefix}-${key}` : key;

      if (typeof value === 'string') {
        variables[`--color-${varName}`] = value;
      } else if (typeof value === 'object' && value !== null) {
        flattenObject(value, varName);
      }
    }
  }

  flattenObject(theme.colors, '');

  // Add spacing
  for (const [key, value] of Object.entries(theme.spacing)) {
    variables[`--spacing-${key}`] = value;
  }

  // Add radii
  for (const [key, value] of Object.entries(theme.radii)) {
    variables[`--radius-${key}`] = value;
  }

  // Add shadows
  for (const [key, value] of Object.entries(theme.shadows)) {
    variables[`--shadow-${key}`] = value;
  }

  // Add font sizes
  for (const [key, value] of Object.entries(theme.fontSizes)) {
    variables[`--font-size-${key}`] = value;
  }

  return variables;
}

/**
 * Convert CSS variables object to style string
 */
export function cssVariablesToString(variables: Record<string, string>): string {
  return Object.entries(variables)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n');
}

/**
 * Create responsive style object
 */
export function responsive<T extends CSSValue>(
  values: {
    base?: T;
    sm?: T;
    md?: T;
    lg?: T;
    xl?: T;
  },
  property: keyof CSSProperties
): Record<string, StyleObject> {
  const styles: Record<string, StyleObject> = {};

  if (values.base !== undefined) {
    styles.base = { [property]: values.base };
  }
  if (values.sm !== undefined) {
    styles['@media (min-width: 640px)'] = { [property]: values.sm };
  }
  if (values.md !== undefined) {
    styles['@media (min-width: 768px)'] = { [property]: values.md };
  }
  if (values.lg !== undefined) {
    styles['@media (min-width: 1024px)'] = { [property]: values.lg };
  }
  if (values.xl !== undefined) {
    styles['@media (min-width: 1280px)'] = { [property]: values.xl };
  }

  return styles;
}

/**
 * Button variant definitions
 */
export const buttonVariants = createVariants({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 600,
    borderRadius: '0.5rem',
    cursor: 'pointer',
    transition: 'all 200ms ease',
  },
  variants: {
    primary: {
      // Colors set by theme
    },
    secondary: {},
    ghost: {},
    outline: {},
    danger: {},
  },
  defaultVariant: 'primary',
});

/**
 * Input variant definitions
 */
export const inputVariants = createVariants({
  base: {
    width: '100%',
    borderWidth: '1px',
    borderStyle: 'solid',
    borderRadius: '0.5rem',
    transition: 'all 200ms ease',
  },
  variants: {
    default: {},
    filled: {},
    flushed: {
      borderRadius: 0,
      borderTop: 'none',
      borderLeft: 'none',
      borderRight: 'none',
    },
  },
  defaultVariant: 'default',
});

/**
 * Card variant definitions
 */
export const cardVariants = createVariants({
  base: {
    borderRadius: '0.75rem',
    overflow: 'hidden',
  },
  variants: {
    elevated: {
      // Shadow set by theme
    },
    outlined: {
      borderWidth: '1px',
      borderStyle: 'solid',
    },
    filled: {},
  },
  defaultVariant: 'elevated',
});

/**
 * Size scale definitions
 */
export const sizeScale = {
  xs: { height: '1.5rem', fontSize: '0.75rem', padding: '0 0.5rem' },
  sm: { height: '2rem', fontSize: '0.875rem', padding: '0 0.75rem' },
  md: { height: '2.5rem', fontSize: '1rem', padding: '0 1rem' },
  lg: { height: '3rem', fontSize: '1.125rem', padding: '0 1.25rem' },
  xl: { height: '3.5rem', fontSize: '1.25rem', padding: '0 1.5rem' },
} as const;

export type Size = keyof typeof sizeScale;
