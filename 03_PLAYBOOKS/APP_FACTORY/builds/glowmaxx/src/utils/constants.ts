// App Constants
export const APP_NAME = 'GlowMaxx';
export const APP_VERSION = '1.0.0';

// Trial
export const TRIAL_DAYS = 7;

// Subscription Pricing
export const MONTHLY_PRICE = '$9.99';
export const ANNUAL_PRICE = '$49.99';
export const REVENUECAT_API_KEY_IOS = 'YOUR_IOS_API_KEY';
export const REVENUECAT_API_KEY_ANDROID = 'YOUR_ANDROID_API_KEY';
export const ENTITLEMENT_ID = 'premium';

// Defaults
export const DEFAULT_WATER_GOAL = 2500; // ml
export const DEFAULT_MEWING_GOAL = 60; // minutes
export const DEFAULT_MEWING_REMINDER_INTERVAL = 30; // minutes

// Storage Keys
export const STORAGE_KEYS = {
  USER_SETTINGS: '@glowmaxx/user_settings',
  DAILY_LOGS: '@glowmaxx/daily_logs',
  PROGRESS_PHOTOS: '@glowmaxx/progress_photos',
  MEWING_SESSIONS: '@glowmaxx/mewing_sessions',
  ACHIEVEMENTS: '@glowmaxx/achievements',
  STREAK_DATA: '@glowmaxx/streak_data',
  SUBSCRIPTION_STATE: '@glowmaxx/subscription_state',
} as const;

// Colors - Warm coral/teal theme (differentiated from cold blue competitors)
// Light Mode (default) - warm, encouraging, gender-neutral
export const COLORS = {
  primary: '#FF6B6B', // Warm coral (vs UMAX blue)
  primaryDark: '#E85555',
  primaryLight: '#FFB3B3',
  secondary: '#4ECDC4', // Teal accent
  secondaryDark: '#3BA99F',
  accent: '#FFD93D', // Gold for achievements
  background: '#FAFAFA',
  surface: '#FFFFFF',
  text: '#1A1A1A',
  textSecondary: '#6B6B6B',
  textLight: '#9CA3AF',
  error: '#EF4444',
  warning: '#F59E0B',
  success: '#10B981',
  border: '#E5E5E5',
  disabled: '#D1D5DB',
  // Debloat indicator colors (matches competitor pattern)
  debloatLow: '#10B981', // Green = good
  debloatMedium: '#F59E0B', // Yellow = moderate
  debloatHigh: '#EF4444', // Red = high
  // Gradient colors
  gradientStart: '#FF6B6B',
  gradientEnd: '#4ECDC4',
} as const;

// Dark Mode colors (premium feel, matches competitor aesthetic)
export const COLORS_DARK = {
  primary: '#FF6B6B',
  primaryDark: '#FF8585',
  primaryLight: '#FF5252',
  secondary: '#4ECDC4',
  secondaryDark: '#5FDDD4',
  accent: '#FFD93D',
  background: '#0F0F0F',
  surface: '#1A1A1A',
  text: '#FFFFFF',
  textSecondary: '#9CA3AF',
  textLight: '#6B7280',
  error: '#EF4444',
  warning: '#F59E0B',
  success: '#10B981',
  border: '#2D2D2D',
  disabled: '#4B5563',
  debloatLow: '#10B981',
  debloatMedium: '#F59E0B',
  debloatHigh: '#EF4444',
  gradientStart: '#FF6B6B',
  gradientEnd: '#4ECDC4',
} as const;

// Social proof constants (like competitors)
export const SOCIAL_PROOF = {
  userCount: '50,000+', // Start modest, update as real
  rating: '4.8',
  ratingCount: '1.2k',
  tagline: 'Trusted by 50,000+ on their glow journey',
} as const;

// Typography
export const FONTS = {
  regular: 'System',
  medium: 'System',
  bold: 'System',
} as const;

// Facial Exercise Categories with Icons
export const EXERCISE_CATEGORY_ICONS = {
  jawline: 'face-man-outline', // MDI
  cheekbones: 'star-outline',
  neck: 'arrow-up-bold-outline',
  eyes: 'eye-outline',
  forehead: 'head-outline',
  overall: 'account-circle-outline',
} as const;

// Photo Angles
export const PHOTO_ANGLES = [
  { id: 'front', label: 'Front View', instruction: 'Look straight at camera, chin parallel to ground' },
  { id: 'left', label: 'Left Profile', instruction: 'Turn head 90 degrees left, show full profile' },
  { id: 'right', label: 'Right Profile', instruction: 'Turn head 90 degrees right, show full profile' },
  { id: 'below', label: 'Below (Jawline)', instruction: 'Tilt chin up slightly, camera below eye level' },
] as const;

// Mewing Instructions
export const MEWING_INSTRUCTIONS = [
  'Rest entire tongue flat on roof of mouth',
  'Tip of tongue behind front teeth (not touching)',
  'Back third of tongue pressed up firmly',
  'Teeth lightly touching or 1-2mm apart',
  'Lips sealed, breathe through nose',
  'Maintain good posture (ears over shoulders)',
];

// Debloating Tips
export const DEBLOATING_TIPS = {
  water: [
    'Drink at least 2-3L water daily',
    'Start day with warm lemon water',
    'Avoid drinking during meals',
    'Cut alcohol 3+ days before events',
  ],
  sodium: [
    'Keep sodium under 2000mg daily',
    'Avoid processed foods',
    'Check labels on sauces and condiments',
    'Rinse canned foods before use',
  ],
  sleep: [
    'Get 7-9 hours of quality sleep',
    'Elevate head slightly to reduce puffiness',
    'Sleep on back to avoid face compression',
    'Avoid salty snacks 3+ hours before bed',
  ],
  other: [
    'Ice face in morning to reduce puffiness',
    'Facial massage for lymphatic drainage',
    'Limit carbs and sugar (cause bloating)',
    'Exercise increases blood flow to face',
  ],
};

// Skincare Steps (Morning)
export const MORNING_SKINCARE_STEPS = [
  { id: 'cleanse', name: 'Gentle Cleanse', description: 'Wash with lukewarm water or gentle cleanser' },
  { id: 'tone', name: 'Tone', description: 'Apply toner with clean hands or cotton pad' },
  { id: 'serum', name: 'Vitamin C Serum', description: 'Apply antioxidant serum for protection' },
  { id: 'moisturize', name: 'Moisturize', description: 'Lock in hydration with moisturizer' },
  { id: 'sunscreen', name: 'Sunscreen SPF 30+', description: 'Essential - prevents aging and dark spots' },
];

// Skincare Steps (Evening)
export const EVENING_SKINCARE_STEPS = [
  { id: 'cleanse1', name: 'Oil Cleanse', description: 'Remove sunscreen and makeup with oil cleanser' },
  { id: 'cleanse2', name: 'Water Cleanse', description: 'Follow up with gentle water-based cleanser' },
  { id: 'exfoliate', name: 'Exfoliate (2-3x/week)', description: 'Chemical exfoliant (AHA/BHA) or gentle scrub' },
  { id: 'treat', name: 'Treatment', description: 'Apply retinol or targeted treatments' },
  { id: 'moisturize', name: 'Moisturize', description: 'Use heavier night cream or sleeping mask' },
];

// Achievement Definitions
export const ACHIEVEMENTS = [
  { id: 'first_photo', name: 'First Step', description: 'Take your first progress photo', requirement: { type: 'photos', value: 1 } },
  { id: 'week_streak', name: 'Week Warrior', description: '7 day streak', requirement: { type: 'streak', value: 7 } },
  { id: 'month_streak', name: 'Month Master', description: '30 day streak', requirement: { type: 'streak', value: 30 } },
  { id: 'mewing_hour', name: 'Tongue Training', description: '60 minutes of mewing tracked', requirement: { type: 'mewing_minutes', value: 60 } },
  { id: 'mewing_10hrs', name: 'Mew Master', description: '10 hours of mewing tracked', requirement: { type: 'mewing_minutes', value: 600 } },
  { id: 'routine_10', name: 'Routine Regular', description: 'Complete 10 routines', requirement: { type: 'routines', value: 10 } },
  { id: 'routine_50', name: 'Glow Getter', description: 'Complete 50 routines', requirement: { type: 'routines', value: 50 } },
  { id: 'photo_week', name: 'Progress Tracker', description: 'Take photos for 4 weeks', requirement: { type: 'photos', value: 4 } },
] as const;
