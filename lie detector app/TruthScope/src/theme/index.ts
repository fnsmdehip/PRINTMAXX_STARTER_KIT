export const colors = {
  bg: {
    primary: '#0A0A0F',
    secondary: '#12121A',
    tertiary: '#1A1A25',
    card: '#16161F',
    elevated: '#1E1E2A',
  },
  accent: {
    primary: '#00E5FF',
    secondary: '#7B61FF',
    tertiary: '#FF3D71',
    success: '#00E096',
    warning: '#FFAA00',
    danger: '#FF3D71',
  },
  text: {
    primary: '#FFFFFF',
    secondary: '#A0A0B8',
    tertiary: '#6B6B80',
    accent: '#00E5FF',
  },
  gradient: {
    truthful: ['#00E096', '#00C853'] as const,
    deceptive: ['#FF3D71', '#FF1744'] as const,
    uncertain: ['#FFAA00', '#FF8F00'] as const,
    scanning: ['#00E5FF', '#7B61FF'] as const,
    premium: ['#7B61FF', '#B388FF'] as const,
  },
  pulse: {
    line: '#00E5FF',
    fill: 'rgba(0, 229, 255, 0.1)',
    baseline: '#2A2A3A',
  },
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const radii = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 999,
} as const;

export const typography = {
  hero: { fontSize: 36, fontWeight: '800' as const, letterSpacing: -1 },
  h1: { fontSize: 28, fontWeight: '700' as const, letterSpacing: -0.5 },
  h2: { fontSize: 22, fontWeight: '700' as const },
  h3: { fontSize: 18, fontWeight: '600' as const },
  body: { fontSize: 16, fontWeight: '400' as const, lineHeight: 24 },
  bodyBold: { fontSize: 16, fontWeight: '600' as const, lineHeight: 24 },
  caption: { fontSize: 13, fontWeight: '500' as const },
  small: { fontSize: 11, fontWeight: '400' as const },
  mono: { fontSize: 14, fontWeight: '500' as const, fontFamily: 'Courier' },
} as const;
