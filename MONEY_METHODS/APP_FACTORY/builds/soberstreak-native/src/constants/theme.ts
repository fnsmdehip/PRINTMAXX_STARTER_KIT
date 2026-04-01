// SoberStreak theme — calm, trustworthy, privacy-first
// Dark navy base: conveys depth, safety, seriousness without being clinical
export const Colors = {
  background: '#0A1628',       // deep navy — safe space
  surface: '#112240',          // lifted card
  surfaceAlt: '#1B3A5C',       // secondary card
  primary: '#4ECDC4',          // teal — healing, growth
  primaryDark: '#2AA39B',
  accent: '#FFD166',           // warm gold — milestone celebration
  accentAlt: '#FF6B6B',        // red for danger/urge states
  success: '#06D6A0',          // streak milestone green
  text: '#E8F4FD',
  textSecondary: '#8BA4C0',
  textTertiary: '#4A6585',
  border: '#1E3A52',
  privacyBadge: '#1B3A5C',
  white: '#FFFFFF',
  overlay: 'rgba(0,0,0,0.6)',
};

export const Fonts = {
  heading: 'System',
  body: 'System',
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const Radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 999,
};

export const Typography = {
  h1: { fontSize: 32, fontWeight: '700' as const, color: Colors.text },
  h2: { fontSize: 24, fontWeight: '700' as const, color: Colors.text },
  h3: { fontSize: 20, fontWeight: '600' as const, color: Colors.text },
  body: { fontSize: 16, fontWeight: '400' as const, color: Colors.text },
  bodySecondary: { fontSize: 16, fontWeight: '400' as const, color: Colors.textSecondary },
  label: { fontSize: 13, fontWeight: '500' as const, color: Colors.textTertiary },
  tiny: { fontSize: 11, fontWeight: '400' as const, color: Colors.textTertiary },
};
