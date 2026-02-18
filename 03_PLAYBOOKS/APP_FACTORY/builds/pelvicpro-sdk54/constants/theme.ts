// FemFit Theme - Soft, encouraging, feminine
export const colors = {
  primary: '#FF7B7B',      // Soft coral
  secondary: '#B8A9C9',    // Lavender
  accent: '#98D7C2',       // Mint
  background: '#FFF9F5',   // Cream
  surface: '#FFFFFF',
  text: '#2D2D2D',         // Soft black
  textLight: '#6B6B6B',
  textMuted: '#9B9B9B',
  success: '#7BC47F',
  warning: '#FFB366',
  error: '#FF6B6B',
  border: '#F0EBE7',

  // Luna specific
  lunaPrimary: '#FFB366',  // Orange tabby
  lunaSecondary: '#FFE4CC',

  // Gradients
  gradientStart: '#FF7B7B',
  gradientEnd: '#FFB366',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
};

export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 40,
  },
  h2: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 28,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  bodyBold: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 24,
  },
  caption: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 20,
  },
  small: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 16,
  },
  mono: {
    fontSize: 20,
    fontWeight: '600' as const,
    fontFamily: 'monospace',
    lineHeight: 28,
  },
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
};
