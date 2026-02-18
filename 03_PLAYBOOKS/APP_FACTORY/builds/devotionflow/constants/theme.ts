// DevotionFlow Theme - Warm, peaceful, spiritual
export const colors = {
  primary: '#8B7355',      // Warm brown
  secondary: '#D4A574',    // Soft gold
  accent: '#6B8E7B',       // Sage green
  background: '#F5F0E8',   // Warm cream
  surface: '#FFFFFF',
  text: '#2D2A26',         // Warm black
  textLight: '#5C5752',
  textMuted: '#8C8780',
  success: '#6B8E7B',      // Sage
  warning: '#D4A574',      // Gold
  error: '#B85C5C',        // Muted red
  border: '#E8E2D8',

  // Devotion specific
  prayerPrimary: '#7B6BA5',    // Soft purple for prayer
  prayerSecondary: '#E8E0F0',
  versePrimary: '#5C7A8A',     // Calm blue for verses
  verseSecondary: '#E0EBF0',

  // Gradients
  gradientStart: '#8B7355',
  gradientEnd: '#D4A574',
  sunriseStart: '#D4A574',
  sunriseEnd: '#F5E6D3',
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
  verse: {
    fontSize: 18,
    fontWeight: '400' as const,
    fontStyle: 'italic' as const,
    lineHeight: 28,
  },
  verseReference: {
    fontSize: 14,
    fontWeight: '600' as const,
    lineHeight: 20,
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
