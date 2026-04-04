export const Colors = {
  // Background
  bg: '#FAFAF8',
  bgCard: '#FFFFFF',
  bgDeep: '#F0FDF4',

  // Brand
  emerald: '#10B981',
  emeraldDark: '#059669',
  emeraldLight: '#D1FAE5',
  emeraldSubtle: '#ECFDF5',

  // Accent
  gold: '#F59E0B',
  goldLight: '#FEF3C7',

  // Text
  text: '#1C1917',
  textMuted: '#6B7280',
  textLight: '#9CA3AF',

  // UI
  border: '#E5E7EB',
  borderLight: '#F3F4F6',
  shadow: 'rgba(0,0,0,0.08)',

  // Habit category colors
  fitness: '#EF4444',
  mindfulness: '#8B5CF6',
  learning: '#3B82F6',
  creation: '#F97316',
  health: '#10B981',
  custom: '#6B7280',
} as const;

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const Radius = {
  sm: 8,
  md: 14,
  lg: 20,
  full: 999,
} as const;

export const Typography = {
  hero: { fontSize: 34, fontWeight: '800' as const, letterSpacing: -0.8 },
  h1: { fontSize: 28, fontWeight: '800' as const, letterSpacing: -0.5 },
  h2: { fontSize: 22, fontWeight: '700' as const, letterSpacing: -0.3 },
  h3: { fontSize: 18, fontWeight: '700' as const },
  body: { fontSize: 16, fontWeight: '400' as const },
  bodyMed: { fontSize: 16, fontWeight: '500' as const },
  caption: { fontSize: 13, fontWeight: '400' as const },
  captionMed: { fontSize: 13, fontWeight: '600' as const },
  label: { fontSize: 11, fontWeight: '700' as const, letterSpacing: 0.5 },
} as const;

export const CATEGORY_COLORS: Record<string, string> = {
  fitness: Colors.fitness,
  mindfulness: Colors.mindfulness,
  learning: Colors.learning,
  creation: Colors.creation,
  health: Colors.health,
  custom: Colors.custom,
};
