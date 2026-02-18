// FemFit Paywall Configuration

export const paywallConfig = {
  // RevenueCat product identifiers
  products: {
    weekly: 'femfit_weekly_799',
    annual: 'femfit_annual_5999',
  },

  // Pricing display
  pricing: {
    weekly: {
      price: '$7.99',
      period: 'week',
      trialDays: 3,
    },
    annual: {
      price: '$59.99',
      period: 'year',
      savings: '63%',
      pricePerWeek: '$1.15',
    },
  },

  // Feature list for paywall
  features: [
    {
      icon: 'dumbbell',
      title: 'Unlimited Workouts',
      description: 'Track every session with no limits',
    },
    {
      icon: 'chart-line',
      title: 'Progress Tracking',
      description: 'See your strength gains over time',
    },
    {
      icon: 'fire',
      title: 'Streak Tracking',
      description: 'Stay motivated with daily streaks',
    },
    {
      icon: 'cat',
      title: 'Luna the Cat',
      description: 'Your personal cheerleader',
    },
    {
      icon: 'book-open',
      title: '50+ Exercises',
      description: 'Women-focused exercise library',
    },
  ],

  // Social proof - real user feedback
  reviews: [
    {
      name: 'Verified User',
      text: 'Finally an app that gets what women want from fitness tracking!',
      rating: 5,
    },
    {
      name: 'Verified User',
      text: 'The mascot makes me actually want to work out. So cute!',
      rating: 5,
    },
    {
      name: 'Verified User',
      text: 'Clean design, easy to use. Love the glute exercises!',
      rating: 5,
    },
  ],

  // Trial configuration
  trial: {
    enabled: true,
    days: 3,
    workoutLimit: 3, // Alternative: limit by workouts instead of days
  },

  // CTA text
  cta: {
    trial: 'Start 3-Day Free Trial',
    purchase: 'Continue with FemFit',
    restore: 'Restore Purchases',
  },
};

// Paywall trigger points
export const paywallTriggers = {
  afterOnboarding: true,
  afterTrialExpires: true,
  afterWorkoutLimit: true,
  workoutLimitCount: 3,
};
