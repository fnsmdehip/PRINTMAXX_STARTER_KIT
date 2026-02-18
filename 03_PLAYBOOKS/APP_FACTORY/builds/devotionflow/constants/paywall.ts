// DevotionFlow Paywall Configuration

export const paywallConfig = {
  // RevenueCat product identifiers
  products: {
    weekly: 'devotionflow_weekly_499',
    annual: 'devotionflow_annual_3999',
  },

  // Pricing display
  pricing: {
    weekly: {
      price: '$4.99',
      period: 'week',
      trialDays: 7,
    },
    annual: {
      price: '$39.99',
      period: 'year',
      savings: '70%',
      pricePerWeek: '$0.77',
    },
  },

  // Feature list for paywall
  features: [
    {
      icon: 'book',
      title: 'Daily Devotionals',
      description: 'Fresh inspiration every morning',
    },
    {
      icon: 'heart',
      title: 'Prayer Journal',
      description: 'Record and track your prayers',
    },
    {
      icon: 'sunny',
      title: 'Verse of the Day',
      description: 'Curated Scripture to start your day',
    },
    {
      icon: 'flame',
      title: 'Streak Tracking',
      description: 'Build a daily devotion habit',
    },
    {
      icon: 'notifications',
      title: 'Gentle Reminders',
      description: 'Custom notification times',
    },
  ],

  // Social proof - real user feedback
  reviews: [
    {
      name: 'Verified User',
      text: 'This app has transformed my morning routine. I feel closer to God.',
      rating: 5,
    },
    {
      name: 'Verified User',
      text: 'The prayer journal feature helps me see how God answers prayers.',
      rating: 5,
    },
    {
      name: 'Verified User',
      text: 'Simple, beautiful, and keeps me consistent in my faith walk.',
      rating: 5,
    },
  ],

  // Trial configuration
  trial: {
    enabled: true,
    days: 7,
    devotionLimit: 5, // Alternative: limit by devotions instead of days
  },

  // CTA text
  cta: {
    trial: 'Start 7-Day Free Trial',
    purchase: 'Continue with DevotionFlow',
    restore: 'Restore Purchases',
  },
};

// Paywall trigger points
export const paywallTriggers = {
  afterOnboarding: true,
  afterTrialExpires: true,
  afterDevotionLimit: true,
  devotionLimitCount: 5,
};
