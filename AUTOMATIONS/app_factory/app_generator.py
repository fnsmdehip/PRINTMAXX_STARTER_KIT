#!/usr/bin/env python3
"""App Factory App Generator.

Generates complete Expo/React Native apps from opportunity specs using the
scripture-streak base template as a reference pattern.

Takes an opportunity spec (niche, name, pricing, features) and outputs a
ready-to-build Expo app with:
  - app.json configured with correct bundle ID, name, scheme
  - package.json with dependencies
  - Onboarding flow with niche-specific questions
  - Paywall with pricing tiers
  - Main streak/habit tracking screen
  - Color theme matched to niche

Usage:
  python3 AUTOMATIONS/app_factory/app_generator.py --generate --niche "fitness" --name "FitStreak"
  python3 AUTOMATIONS/app_factory/app_generator.py --generate --from-csv --top 3
  python3 AUTOMATIONS/app_factory/app_generator.py --list-templates
  python3 AUTOMATIONS/app_factory/app_generator.py --help
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_DIR = AUTOMATIONS / "app_factory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BUILDS_DIR = PROJECT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
TEMPLATE_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/app factory/app-factory/base-template/scripture-streak")
OPPORTUNITIES_CSV = LEDGER / "APP_FACTORY_OPPORTUNITIES.csv"
BUILDS_LOG = LEDGER / "APP_FACTORY_BUILDS.csv"
LOGFILE = LOG_DIR / "app_generator.log"

BUNDLE_ID_PREFIX = "com.fnsmdehip"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_DIR / "app_generator.log", "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Niche Configuration Database
# ---------------------------------------------------------------------------
NICHE_CONFIGS: dict[str, dict[str, Any]] = {
    "health_fitness": {
        "display_name": "Health & Fitness",
        "app_suffix": "streak",
        "colors": {
            "primary": "#FF6B35",
            "secondary": "#004E89",
            "background": "#0A0A1A",
            "surface": "#1A1A2E",
            "accent": "#FF6B35",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "What's your main fitness goal?", "options": ["Lose weight", "Build muscle", "Stay active", "Train for event"]},
            {"question": "How often do you work out?", "options": ["Never", "1-2x/week", "3-4x/week", "5+/week"]},
            {"question": "What motivates you most?", "options": ["Looking better", "Feeling better", "Competition", "Health"]},
            {"question": "Preferred workout time?", "options": ["Morning", "Afternoon", "Evening", "Varies"]},
        ],
        "paywall_benefits": [
            "Unlimited streak tracking with detailed stats",
            "Custom workout reminders",
            "Progress photos & body measurements",
            "Advanced analytics & trends",
            "Community challenges",
        ],
        "default_habits": ["Workout", "Drink 8 glasses of water", "10K steps", "Stretch 10 min", "Eat clean"],
        "category": "Health & Fitness",
        "keywords": ["fitness tracker", "workout streak", "habit tracker", "daily exercise", "gym tracker"],
    },
    "wellness": {
        "display_name": "Wellness",
        "app_suffix": "streak",
        "colors": {
            "primary": "#7B68EE",
            "secondary": "#4A90D9",
            "background": "#0D0D1A",
            "surface": "#1A1A30",
            "accent": "#9B59B6",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "What brings you here?", "options": ["Reduce stress", "Better sleep", "More mindful", "Inner peace"]},
            {"question": "Have you meditated before?", "options": ["Never", "A few times", "Regularly", "Daily practice"]},
            {"question": "When do you prefer to practice?", "options": ["Morning", "Afternoon", "Before bed", "Throughout day"]},
            {"question": "How much time can you commit?", "options": ["5 min", "10 min", "15 min", "20+ min"]},
        ],
        "paywall_benefits": [
            "Unlimited meditation streak tracking",
            "Guided breathing exercises",
            "Sleep quality tracking",
            "Mood journal with insights",
            "Calming notification reminders",
        ],
        "default_habits": ["Meditate 10 min", "Deep breathing", "Gratitude journal", "Digital detox 1hr", "Nature walk"],
        "category": "Health & Fitness",
        "keywords": ["meditation tracker", "mindfulness app", "wellness streak", "calm daily", "stress relief"],
    },
    "religious_spiritual": {
        "display_name": "Religious/Spiritual",
        "app_suffix": "streak",
        "colors": {
            "primary": "#D4AF37",
            "secondary": "#8B6914",
            "background": "#1a1a2e",
            "surface": "#16213e",
            "accent": "#D4AF37",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "What's your faith tradition?", "options": ["Christian", "Muslim", "Jewish", "Buddhist", "Hindu", "Other"]},
            {"question": "Current spiritual practice?", "options": ["Just starting", "Occasional", "Regular", "Daily"]},
            {"question": "What do you want to build?", "options": ["Prayer habit", "Scripture reading", "Meditation", "All of the above"]},
            {"question": "Best time for practice?", "options": ["Early morning", "Midday", "Evening", "Before bed"]},
        ],
        "paywall_benefits": [
            "Unlimited spiritual streak tracking",
            "Daily scripture & prayer reminders",
            "Reading plans & progress tracking",
            "Reflection journal",
            "Community accountability",
        ],
        "default_habits": ["Daily prayer", "Scripture reading", "Reflection", "Gratitude", "Acts of kindness"],
        "category": "Lifestyle",
        "keywords": ["prayer tracker", "bible streak", "spiritual discipline", "faith habit", "daily devotion"],
    },
    "productivity": {
        "display_name": "Productivity",
        "app_suffix": "lock",
        "colors": {
            "primary": "#00C853",
            "secondary": "#2196F3",
            "background": "#121212",
            "surface": "#1E1E1E",
            "accent": "#00C853",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "Biggest productivity challenge?", "options": ["Focus", "Procrastination", "Organization", "Time management"]},
            {"question": "Work style?", "options": ["Student", "Remote worker", "Office", "Freelancer"]},
            {"question": "How many habits to track?", "options": ["1-3", "4-6", "7-10", "10+"]},
            {"question": "Preferred tracking method?", "options": ["Simple streak", "Detailed log", "Timer-based", "Checklist"]},
        ],
        "paywall_benefits": [
            "Unlimited habit tracking",
            "Focus timer with Pomodoro",
            "Detailed analytics & streaks",
            "Custom categories & tags",
            "Export data & insights",
        ],
        "default_habits": ["Deep work 2hr", "Read 30 min", "No social media before noon", "Exercise", "Journal"],
        "category": "Productivity",
        "keywords": ["habit tracker", "productivity app", "streak counter", "daily routine", "focus timer"],
    },
    "education": {
        "display_name": "Education",
        "app_suffix": "streak",
        "colors": {
            "primary": "#FF9800",
            "secondary": "#F44336",
            "background": "#1A1A2E",
            "surface": "#16213E",
            "accent": "#FF9800",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "What are you learning?", "options": ["Language", "Coding", "Music", "Academic subject", "Professional skill"]},
            {"question": "Current level?", "options": ["Complete beginner", "Some experience", "Intermediate", "Advanced"]},
            {"question": "Daily study time available?", "options": ["5-10 min", "15-30 min", "30-60 min", "1hr+"]},
            {"question": "Learning style?", "options": ["Visual", "Reading", "Practice", "Mixed"]},
        ],
        "paywall_benefits": [
            "Unlimited study streak tracking",
            "Spaced repetition reminders",
            "Progress analytics & trends",
            "Custom study plans",
            "Achievement badges & milestones",
        ],
        "default_habits": ["Study 30 min", "Practice exercises", "Review notes", "Read chapter", "Quiz yourself"],
        "category": "Education",
        "keywords": ["study tracker", "learning streak", "education app", "daily study", "student habit"],
    },
    "food_health": {
        "display_name": "Food & Health",
        "app_suffix": "streak",
        "colors": {
            "primary": "#4CAF50",
            "secondary": "#2196F3",
            "background": "#0A1628",
            "surface": "#152238",
            "accent": "#4CAF50",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "Primary health goal?", "options": ["Lose weight", "Eat healthier", "Stay hydrated", "Intermittent fasting"]},
            {"question": "Biggest challenge?", "options": ["Remembering to drink water", "Tracking meals", "Staying consistent", "Motivation"]},
            {"question": "How do you want to track?", "options": ["Simple check-in", "Detailed logging", "Photo journal", "Quick taps"]},
            {"question": "Reminder frequency?", "options": ["Hourly", "3x/day", "Custom times", "No reminders"]},
        ],
        "paywall_benefits": [
            "Unlimited nutrition streak tracking",
            "Water intake reminders & tracking",
            "Fasting timer with custom schedules",
            "Meal photo journal",
            "Weekly health insights",
        ],
        "default_habits": ["Drink 8 glasses water", "Eat 5 servings vegetables", "No processed food", "Cook at home", "Meal prep Sunday"],
        "category": "Health & Fitness",
        "keywords": ["water tracker", "nutrition streak", "fasting app", "healthy eating", "diet tracker"],
    },
    "mental_health": {
        "display_name": "Mental Health",
        "app_suffix": "streak",
        "colors": {
            "primary": "#E91E63",
            "secondary": "#9C27B0",
            "background": "#1A0A1E",
            "surface": "#2A1A2E",
            "accent": "#E91E63",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "What would help you most?", "options": ["Mood tracking", "Gratitude practice", "Anxiety management", "Self-care routine"]},
            {"question": "How are you feeling today?", "options": ["Great", "Good", "Okay", "Struggling"]},
            {"question": "What time works for check-ins?", "options": ["Morning", "Afternoon", "Evening", "Multiple times"]},
            {"question": "Privacy is important to you?", "options": ["Very important", "Somewhat", "Not concerned"]},
        ],
        "paywall_benefits": [
            "Unlimited mood tracking & journal",
            "Gratitude prompts & exercises",
            "Anxiety coping tools",
            "Mood patterns & insights",
            "Private & encrypted entries",
        ],
        "default_habits": ["Mood check-in", "3 things grateful for", "5 min meditation", "Call a friend", "Go outside 15 min"],
        "category": "Health & Fitness",
        "keywords": ["mood tracker", "gratitude journal", "mental health app", "self care", "anxiety relief"],
    },
    "finance": {
        "display_name": "Finance",
        "app_suffix": "tracker",
        "colors": {
            "primary": "#00BFA5",
            "secondary": "#1DE9B6",
            "background": "#0D1117",
            "surface": "#161B22",
            "accent": "#00BFA5",
            "text": "#FFFFFF",
        },
        "onboarding_questions": [
            {"question": "Financial goal?", "options": ["Save money", "Pay off debt", "Build wealth", "Budget better"]},
            {"question": "Current saving habit?", "options": ["None", "Occasional", "Monthly", "Weekly"]},
            {"question": "Biggest money challenge?", "options": ["Overspending", "No budget", "Impulse buying", "Low income"]},
            {"question": "Track by?", "options": ["Daily check-in", "Per transaction", "Weekly review", "Monthly"]},
        ],
        "paywall_benefits": [
            "Unlimited financial habit tracking",
            "Savings streak with milestones",
            "No-spend day challenges",
            "Budget category tracking",
            "Weekly financial insights",
        ],
        "default_habits": ["Track spending", "No impulse buys", "Save $5", "Review budget", "No-spend day"],
        "category": "Finance",
        "keywords": ["savings tracker", "budget habit", "money streak", "financial discipline", "no spend"],
    },
}


# ---------------------------------------------------------------------------
# Pricing Templates (from battle-tested research)
# ---------------------------------------------------------------------------
PRICING_TEMPLATES = {
    "standard": {
        "monthly_price": 4.99,
        "yearly_price": 29.99,
        "trial_days": 3,
        "show_weekly": False,
    },
    "premium": {
        "monthly_price": 9.99,
        "yearly_price": 49.99,
        "trial_days": 7,
        "show_weekly": True,
        "weekly_price": 3.99,
    },
    "budget": {
        "monthly_price": 2.99,
        "yearly_price": 19.99,
        "trial_days": 3,
        "show_weekly": False,
    },
}


# ---------------------------------------------------------------------------
# App Generator
# ---------------------------------------------------------------------------
def slugify(name: str) -> str:
    """Convert app name to URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def generate_bundle_id(name: str) -> str:
    """Generate unique bundle ID."""
    slug = slugify(name).replace('-', '')
    return f"{BUNDLE_ID_PREFIX}.{slug}"


def generate_app_json(name: str, slug: str, bundle_id: str, config: dict, pricing: dict) -> dict:
    """Generate app.json for Expo project."""
    colors = config["colors"]
    return {
        "expo": {
            "name": name,
            "slug": slug,
            "version": "1.0.0",
            "orientation": "portrait",
            "icon": "./assets/icon.png",
            "userInterfaceStyle": "dark",
            "newArchEnabled": False,
            "plugins": [
                "expo-router",
                "expo-secure-store",
                [
                    "expo-notifications",
                    {
                        "icon": "./assets/notification-icon.png",
                        "color": colors["primary"]
                    }
                ]
            ],
            "splash": {
                "image": "./assets/splash-icon.png",
                "resizeMode": "contain",
                "backgroundColor": colors["background"]
            },
            "ios": {
                "supportsTablet": True,
                "bundleIdentifier": bundle_id,
                "infoPlist": {
                    "ITSAppUsesNonExemptEncryption": False,
                    "NSCameraUsageDescription": f"Take progress photos for your {config['display_name'].lower()} streak",
                    "NSPhotoLibraryUsageDescription": f"Save and share your {config['display_name'].lower()} progress",
                    "UIBackgroundModes": ["remote-notification"]
                },
                "config": {
                    "usesNonExemptEncryption": False
                }
            },
            "android": {
                "adaptiveIcon": {
                    "foregroundImage": "./assets/adaptive-icon.png",
                    "backgroundColor": colors["background"]
                },
                "package": bundle_id,
                "edgeToEdgeEnabled": True
            },
            "web": {
                "favicon": "./assets/favicon.png"
            },
            "scheme": slug,
            "extra": {
                "eas": {
                    "projectId": ""
                }
            }
        }
    }


def generate_package_json(name: str, slug: str) -> dict:
    """Generate package.json with required dependencies."""
    return {
        "name": slug,
        "version": "1.0.0",
        "main": "expo-router/entry",
        "scripts": {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web",
            "build:ios": "eas build --platform ios --profile production",
            "submit:ios": "eas submit --platform ios",
            "lint": "npx tsc --noEmit"
        },
        "dependencies": {
            "expo": "~52.0.0",
            "expo-router": "~4.0.0",
            "expo-secure-store": "~14.0.0",
            "expo-notifications": "~0.29.0",
            "expo-haptics": "~14.0.0",
            "expo-status-bar": "~2.0.0",
            "expo-font": "~13.0.0",
            "expo-linear-gradient": "~14.0.0",
            "react": "18.3.1",
            "react-native": "0.76.6",
            "react-native-reanimated": "~3.16.0",
            "react-native-gesture-handler": "~2.20.0",
            "react-native-safe-area-context": "4.12.0",
            "react-native-screens": "~4.4.0",
            "react-native-svg": "15.8.0",
            "@react-native-async-storage/async-storage": "1.23.1",
            "react-native-purchases": "^8.0.0",
            "date-fns": "^3.0.0"
        },
        "devDependencies": {
            "@types/react": "~18.3.0",
            "typescript": "~5.3.0"
        },
        "private": True
    }


def generate_onboarding_screen(config: dict, niche_key: str) -> str:
    """Generate TypeScript onboarding screen component."""
    questions = config["onboarding_questions"]
    colors = config["colors"]
    display_name = config["display_name"]

    questions_json = json.dumps(questions, indent=2)

    return f'''import React, {{ useState }} from 'react';
import {{ View, Text, TouchableOpacity, StyleSheet, Dimensions, ScrollView }} from 'react-native';
import {{ router }} from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

const {{ width }} = Dimensions.get('window');

const QUESTIONS = {questions_json};

const COLORS = {{
  primary: '{colors["primary"]}',
  secondary: '{colors["secondary"]}',
  background: '{colors["background"]}',
  surface: '{colors["surface"]}',
  accent: '{colors["accent"]}',
  text: '{colors["text"]}',
}};

export default function OnboardingScreen() {{
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({{ }});

  const handleAnswer = async (answer: string) => {{
    const newAnswers = {{ ...answers, [currentStep]: answer }};
    setAnswers(newAnswers);

    if (currentStep < QUESTIONS.length - 1) {{
      setCurrentStep(currentStep + 1);
    }} else {{
      // Save answers and go to paywall
      await AsyncStorage.setItem('onboarding_answers', JSON.stringify(newAnswers));
      await AsyncStorage.setItem('onboarding_complete', 'true');
      router.replace('/paywall');
    }}
  }};

  const question = QUESTIONS[currentStep];
  const progress = (currentStep + 1) / QUESTIONS.length;

  return (
    <View style={{{{ flex: 1, backgroundColor: COLORS.background }}}}>
      <ScrollView contentContainerStyle={{{{ flexGrow: 1, padding: 24, paddingTop: 60 }}}}>
        {{/* Progress bar */}}
        <View style={{{{ height: 4, backgroundColor: COLORS.surface, borderRadius: 2, marginBottom: 40 }}}}>
          <View style={{{{ height: 4, backgroundColor: COLORS.primary, borderRadius: 2, width: `${{progress * 100}}%` }}}} />
        </View>

        {{/* Step counter */}}
        <Text style={{{{ color: COLORS.primary, fontSize: 14, marginBottom: 12, fontWeight: '600' }}}}>
          Step {{currentStep + 1}} of {{QUESTIONS.length}}
        </Text>

        {{/* Question */}}
        <Text style={{{{ color: COLORS.text, fontSize: 28, fontWeight: 'bold', marginBottom: 32, lineHeight: 36 }}}}>
          {{question.question}}
        </Text>

        {{/* Options */}}
        {{question.options.map((option: string, index: number) => (
          <TouchableOpacity
            key={{index}}
            onPress={{() => handleAnswer(option)}}
            style={{{{
              backgroundColor: answers[currentStep] === option ? COLORS.primary : COLORS.surface,
              padding: 18,
              borderRadius: 12,
              marginBottom: 12,
              borderWidth: 1,
              borderColor: answers[currentStep] === option ? COLORS.primary : COLORS.surface,
            }}}}
          >
            <Text style={{{{ color: COLORS.text, fontSize: 16, fontWeight: '500' }}}}>{{option}}</Text>
          </TouchableOpacity>
        ))}}
      </ScrollView>
    </View>
  );
}}
'''


def generate_paywall_screen(config: dict, pricing: dict) -> str:
    """Generate TypeScript paywall screen component."""
    colors = config["colors"]
    benefits = config["paywall_benefits"]
    display_name = config["display_name"]
    benefits_json = json.dumps(benefits, indent=2)

    monthly = pricing.get("monthly_price", 4.99)
    yearly = pricing.get("yearly_price", 29.99)
    trial_days = pricing.get("trial_days", 3)
    yearly_monthly = round(yearly / 12, 2)

    return f'''import React, {{ useState }} from 'react';
import {{ View, Text, TouchableOpacity, StyleSheet, Dimensions, ScrollView, Alert }} from 'react-native';
import {{ router }} from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

const {{ width }} = Dimensions.get('window');

const BENEFITS = {benefits_json};

const COLORS = {{
  primary: '{colors["primary"]}',
  background: '{colors["background"]}',
  surface: '{colors["surface"]}',
  text: '{colors["text"]}',
}};

// IMPORTANT: This is a placeholder paywall UI.
// Before shipping, you MUST integrate RevenueCat (react-native-purchases)
// with real product IDs from App Store Connect.
// See: https://docs.revenuecat.com/docs/reactnative

export default function PaywallScreen() {{
  const [selectedPlan, setSelectedPlan] = useState<'yearly' | 'monthly'>('yearly');

  const handlePurchase = async () => {{
    // NOT IMPLEMENTED - connect RevenueCat before shipping
    // Replace this with:
    // import Purchases from 'react-native-purchases';
    // const {{ customerInfo }} = await Purchases.purchasePackage(package);
    Alert.alert(
      'NOT IMPLEMENTED',
      'Connect RevenueCat with real product IDs before shipping. See src/lib/purchases.ts',
      [
        {{ text: 'OK', onPress: () => {{}} }},
        {{
          text: 'Continue (Dev Mode)',
          onPress: async () => {{
            await AsyncStorage.setItem('subscription_active', 'dev_mode');
            router.replace('/(tabs)');
          }},
        }},
      ]
    );
  }};

  const handleRestore = async () => {{
    // NOT IMPLEMENTED - connect RevenueCat before shipping
    Alert.alert('NOT IMPLEMENTED', 'Connect RevenueCat to restore purchases');
  }};

  const handleSkip = () => {{
    // Allow limited free access
    router.replace('/(tabs)');
  }};

  return (
    <View style={{{{ flex: 1, backgroundColor: COLORS.background }}}}>
      <ScrollView contentContainerStyle={{{{ flexGrow: 1, padding: 24, paddingTop: 60 }}}}>
        <Text style={{{{ color: COLORS.text, fontSize: 32, fontWeight: 'bold', textAlign: 'center', marginBottom: 8 }}}}>
          Unlock Everything
        </Text>
        <Text style={{{{ color: '#AAA', fontSize: 16, textAlign: 'center', marginBottom: 32 }}}}>
          Start your {trial_days}-day free trial
        </Text>

        {{/* Benefits */}}
        {{BENEFITS.map((benefit: string, i: number) => (
          <View key={{i}} style={{{{ flexDirection: 'row', alignItems: 'center', marginBottom: 16, paddingHorizontal: 8 }}}}>
            <Text style={{{{ color: COLORS.primary, fontSize: 20, marginRight: 12 }}}}>\\u2713</Text>
            <Text style={{{{ color: COLORS.text, fontSize: 15, flex: 1 }}}}>{{benefit}}</Text>
          </View>
        ))}}

        {{/* Plan selection */}}
        <View style={{{{ marginTop: 24 }}}}>
          {{/* Yearly */}}
          <TouchableOpacity
            onPress={{() => setSelectedPlan('yearly')}}
            style={{{{
              backgroundColor: selectedPlan === 'yearly' ? COLORS.surface : 'transparent',
              borderWidth: 2,
              borderColor: selectedPlan === 'yearly' ? COLORS.primary : '#333',
              borderRadius: 16,
              padding: 20,
              marginBottom: 12,
              position: 'relative',
            }}}}
          >
            <View style={{{{
              position: 'absolute', top: -10, right: 16,
              backgroundColor: COLORS.primary, borderRadius: 8, paddingHorizontal: 10, paddingVertical: 3,
            }}}}>
              <Text style={{{{ color: '#FFF', fontSize: 11, fontWeight: 'bold' }}}}>BEST VALUE</Text>
            </View>
            <View style={{{{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}}}>
              <View>
                <Text style={{{{ color: COLORS.text, fontSize: 18, fontWeight: 'bold' }}}}>Yearly</Text>
                <Text style={{{{ color: '#AAA', fontSize: 13 }}}}>${{'{yearly_monthly}'}}/month</Text>
              </View>
              <Text style={{{{ color: COLORS.text, fontSize: 22, fontWeight: 'bold' }}}}>${{'{yearly}'}}/yr</Text>
            </View>
          </TouchableOpacity>

          {{/* Monthly */}}
          <TouchableOpacity
            onPress={{() => setSelectedPlan('monthly')}}
            style={{{{
              backgroundColor: selectedPlan === 'monthly' ? COLORS.surface : 'transparent',
              borderWidth: 2,
              borderColor: selectedPlan === 'monthly' ? COLORS.primary : '#333',
              borderRadius: 16,
              padding: 20,
              marginBottom: 24,
            }}}}
          >
            <View style={{{{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}}}>
              <Text style={{{{ color: COLORS.text, fontSize: 18, fontWeight: 'bold' }}}}>Monthly</Text>
              <Text style={{{{ color: COLORS.text, fontSize: 22, fontWeight: 'bold' }}}}>${{'{monthly}'}}/mo</Text>
            </View>
          </TouchableOpacity>
        </View>

        {{/* CTA */}}
        <TouchableOpacity
          onPress={{handlePurchase}}
          style={{{{
            backgroundColor: COLORS.primary,
            borderRadius: 16,
            padding: 18,
            alignItems: 'center',
            marginBottom: 12,
          }}}}
        >
          <Text style={{{{ color: '#FFF', fontSize: 18, fontWeight: 'bold' }}}}>
            Start Free Trial
          </Text>
          <Text style={{{{ color: 'rgba(255,255,255,0.7)', fontSize: 12, marginTop: 4 }}}}>
            {trial_days}-day free trial, cancel anytime
          </Text>
        </TouchableOpacity>

        {{/* Subscription terms (Apple 3.1.1/3.1.2 compliance) */}}
        <Text style={{{{ color: '#666', fontSize: 11, textAlign: 'center', marginBottom: 8, lineHeight: 16 }}}}>
          Payment will be charged to your Apple ID account at the confirmation of purchase.
          Subscription automatically renews unless it is canceled at least 24 hours before the end
          of the current period. Your account will be charged for renewal within 24 hours prior to
          the end of the current period. You can manage and cancel your subscriptions by going to
          your account settings on the App Store after purchase.
        </Text>

        <View style={{{{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginBottom: 16 }}}}>
          <TouchableOpacity onPress={{handleRestore}}>
            <Text style={{{{ color: '#666', fontSize: 13 }}}}>Restore Purchases</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={{handleSkip}}>
            <Text style={{{{ color: '#666', fontSize: 13 }}}}>Continue with limited access</Text>
          </TouchableOpacity>
        </View>

        <View style={{{{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginBottom: 40 }}}}>
          <TouchableOpacity onPress={{() => {{/* Link to privacy policy */}}}}>
            <Text style={{{{ color: '#555', fontSize: 11 }}}}>Privacy Policy</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={{() => {{/* Link to terms */}}}}>
            <Text style={{{{ color: '#555', fontSize: 11 }}}}>Terms of Use</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
}}
'''


def generate_main_screen(config: dict, niche_key: str) -> str:
    """Generate the main streak/habit tracking screen."""
    colors = config["colors"]
    habits = config["default_habits"]
    display_name = config["display_name"]
    habits_json = json.dumps(habits)

    return f'''import React, {{ useState, useEffect }} from 'react';
import {{ View, Text, TouchableOpacity, ScrollView, Dimensions }} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const {{ width }} = Dimensions.get('window');

const DEFAULT_HABITS = {habits_json};

const COLORS = {{
  primary: '{colors["primary"]}',
  background: '{colors["background"]}',
  surface: '{colors["surface"]}',
  accent: '{colors["accent"]}',
  text: '{colors["text"]}',
}};

interface HabitState {{
  name: string;
  completed: boolean;
  streak: number;
}}

export default function HomeScreen() {{
  const [habits, setHabits] = useState<HabitState[]>(
    DEFAULT_HABITS.map(h => ({{ name: h, completed: false, streak: 0 }}))
  );
  const [totalStreak, setTotalStreak] = useState(0);

  useEffect(() => {{
    loadHabits();
  }}, []);

  const loadHabits = async () => {{
    try {{
      const saved = await AsyncStorage.getItem('habits_state');
      if (saved) {{
        const parsed = JSON.parse(saved);
        setHabits(parsed.habits || habits);
        setTotalStreak(parsed.totalStreak || 0);
      }}
    }} catch {{}}
  }};

  const toggleHabit = async (index: number) => {{
    const updated = [...habits];
    updated[index].completed = !updated[index].completed;
    if (updated[index].completed) {{
      updated[index].streak += 1;
    }} else {{
      updated[index].streak = Math.max(0, updated[index].streak - 1);
    }}
    setHabits(updated);

    const allDone = updated.every(h => h.completed);
    const newTotal = allDone ? totalStreak + 1 : totalStreak;
    setTotalStreak(newTotal);

    await AsyncStorage.setItem('habits_state', JSON.stringify({{
      habits: updated,
      totalStreak: newTotal,
      lastUpdate: new Date().toISOString(),
    }}));
  }};

  const completedCount = habits.filter(h => h.completed).length;

  return (
    <View style={{{{ flex: 1, backgroundColor: COLORS.background }}}}>
      <ScrollView contentContainerStyle={{{{ padding: 24, paddingTop: 60 }}}}>
        {{/* Header */}}
        <Text style={{{{ color: COLORS.text, fontSize: 28, fontWeight: 'bold', marginBottom: 4 }}}}>
          Today
        </Text>
        <Text style={{{{ color: '#AAA', fontSize: 14, marginBottom: 24 }}}}>
          {{completedCount}}/{{habits.length}} completed
        </Text>

        {{/* Streak counter */}}
        <View style={{{{
          backgroundColor: COLORS.surface,
          borderRadius: 20,
          padding: 24,
          alignItems: 'center',
          marginBottom: 32,
        }}}}>
          <Text style={{{{ color: COLORS.primary, fontSize: 48, fontWeight: 'bold' }}}}>
            {{totalStreak}}
          </Text>
          <Text style={{{{ color: '#AAA', fontSize: 14 }}}}>Day Streak</Text>
        </View>

        {{/* Habits */}}
        {{habits.map((habit, index) => (
          <TouchableOpacity
            key={{index}}
            onPress={{() => toggleHabit(index)}}
            style={{{{
              backgroundColor: COLORS.surface,
              borderRadius: 16,
              padding: 18,
              marginBottom: 12,
              flexDirection: 'row',
              alignItems: 'center',
              borderWidth: habit.completed ? 1 : 0,
              borderColor: COLORS.primary,
            }}}}
          >
            <View style={{{{
              width: 28, height: 28, borderRadius: 14,
              backgroundColor: habit.completed ? COLORS.primary : 'transparent',
              borderWidth: 2,
              borderColor: habit.completed ? COLORS.primary : '#444',
              alignItems: 'center', justifyContent: 'center',
              marginRight: 14,
            }}}}>
              {{habit.completed && (
                <Text style={{{{ color: '#FFF', fontSize: 16, fontWeight: 'bold' }}}}>\\u2713</Text>
              )}}
            </View>
            <View style={{{{ flex: 1 }}}}>
              <Text style={{{{
                color: COLORS.text,
                fontSize: 16,
                fontWeight: '500',
                textDecorationLine: habit.completed ? 'line-through' : 'none',
                opacity: habit.completed ? 0.6 : 1,
              }}}}>
                {{habit.name}}
              </Text>
            </View>
            <Text style={{{{ color: COLORS.primary, fontSize: 13, fontWeight: '600' }}}}>
              {{habit.streak}}\\uD83D\\uDD25
            </Text>
          </TouchableOpacity>
        ))}}
      </ScrollView>
    </View>
  );
}}
'''


def generate_tsconfig() -> dict:
    """Generate tsconfig.json."""
    return {
        "extends": "expo/tsconfig.base",
        "compilerOptions": {
            "strict": True,
            "paths": {
                "@/*": ["./src/*"]
            }
        }
    }


def generate_app(
    name: str,
    niche_key: str,
    pricing_tier: str = "standard",
    dry_run: bool = False,
) -> Path | None:
    """Generate a complete app from a niche configuration.

    Returns the output directory path, or None on failure.
    """
    config = NICHE_CONFIGS.get(niche_key)
    if not config:
        log(f"ERROR: Unknown niche '{niche_key}'. Available: {list(NICHE_CONFIGS.keys())}")
        return None

    pricing = PRICING_TEMPLATES.get(pricing_tier, PRICING_TEMPLATES["standard"])
    slug = slugify(name)
    bundle_id = generate_bundle_id(name)
    output_dir = safe_path(BUILDS_DIR / slug)

    if dry_run:
        log(f"DRY RUN: Would generate app '{name}' ({slug})")
        log(f"  Niche: {config['display_name']}")
        log(f"  Bundle ID: {bundle_id}")
        log(f"  Pricing: ${pricing.get('monthly_price')}/mo, ${pricing.get('yearly_price')}/yr")
        log(f"  Output: {output_dir}")
        return output_dir

    if output_dir.exists():
        log(f"WARNING: {output_dir} already exists. Skipping to avoid overwrite.")
        log(f"  Delete it manually if you want to regenerate.")
        return None

    log(f"Generating app: {name} ({niche_key})")

    # Create directory structure
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
    (output_dir / "src" / "lib").mkdir(parents=True, exist_ok=True)
    (output_dir / "app" / "(tabs)").mkdir(parents=True, exist_ok=True)
    (output_dir / "assets").mkdir(parents=True, exist_ok=True)

    # 1. app.json
    app_json = generate_app_json(name, slug, bundle_id, config, pricing)
    with open(output_dir / "app.json", "w") as f:
        json.dump(app_json, f, indent=2)
    log(f"  Created app.json")

    # 2. package.json
    pkg_json = generate_package_json(name, slug)
    with open(output_dir / "package.json", "w") as f:
        json.dump(pkg_json, f, indent=2)
    log(f"  Created package.json")

    # 3. tsconfig.json
    with open(output_dir / "tsconfig.json", "w") as f:
        json.dump(generate_tsconfig(), f, indent=2)
    log(f"  Created tsconfig.json")

    # 4. babel.config.js
    with open(output_dir / "babel.config.js", "w") as f:
        f.write("module.exports = function (api) {\n  api.cache(true);\n  return {\n    presets: ['babel-preset-expo'],\n  };\n};\n")

    # 5. Onboarding screen
    with open(output_dir / "app" / "onboarding.tsx", "w") as f:
        f.write(generate_onboarding_screen(config, niche_key))
    log(f"  Created onboarding screen ({len(config['onboarding_questions'])} questions)")

    # 6. Paywall screen
    with open(output_dir / "app" / "paywall.tsx", "w") as f:
        f.write(generate_paywall_screen(config, pricing))
    log(f"  Created paywall screen (${pricing.get('monthly_price')}/mo)")

    # 7. Main streak screen
    with open(output_dir / "app" / "(tabs)" / "index.tsx", "w") as f:
        f.write(generate_main_screen(config, niche_key))
    log(f"  Created main streak screen ({len(config['default_habits'])} default habits)")

    # 8. Layout files
    with open(output_dir / "app" / "_layout.tsx", "w") as f:
        f.write(f'''import {{ Stack }} from 'expo-router';
import {{ StatusBar }} from 'expo-status-bar';

export default function RootLayout() {{
  return (
    <>
      <StatusBar style="light" />
      <Stack screenOptions={{{{ headerShown: false }}}}>
        <Stack.Screen name="onboarding" />
        <Stack.Screen name="paywall" />
        <Stack.Screen name="(tabs)" />
      </Stack>
    </>
  );
}}
''')

    with open(output_dir / "app" / "(tabs)" / "_layout.tsx", "w") as f:
        f.write(f'''import {{ Tabs }} from 'expo-router';
import {{ Text }} from 'react-native';

export default function TabLayout() {{
  return (
    <Tabs
      screenOptions={{{{
        headerShown: false,
        tabBarStyle: {{
          backgroundColor: '{config["colors"]["background"]}',
          borderTopColor: '{config["colors"]["surface"]}',
        }},
        tabBarActiveTintColor: '{config["colors"]["primary"]}',
        tabBarInactiveTintColor: '#666',
      }}}}
    >
      <Tabs.Screen
        name="index"
        options={{{{
          title: 'Today',
          tabBarIcon: ({{ color }}) => <Text style={{{{ color, fontSize: 20 }}}}>\\u2705</Text>,
        }}}}
      />
      <Tabs.Screen
        name="stats"
        options={{{{
          title: 'Stats',
          tabBarIcon: ({{ color }}) => <Text style={{{{ color, fontSize: 20 }}}}>\\uD83D\\uDCCA</Text>,
        }}}}
      />
      <Tabs.Screen
        name="settings"
        options={{{{
          title: 'Settings',
          tabBarIcon: ({{ color }}) => <Text style={{{{ color, fontSize: 20 }}}}>\\u2699\\uFE0F</Text>,
        }}}}
      />
    </Tabs>
  );
}}
''')

    # 9. Stats placeholder
    with open(output_dir / "app" / "(tabs)" / "stats.tsx", "w") as f:
        f.write(f'''import React from 'react';
import {{ View, Text, ScrollView }} from 'react-native';

export default function StatsScreen() {{
  return (
    <View style={{{{ flex: 1, backgroundColor: '{config["colors"]["background"]}', padding: 24, paddingTop: 60 }}}}>
      <Text style={{{{ color: '#FFF', fontSize: 28, fontWeight: 'bold', marginBottom: 24 }}}}>Statistics</Text>
      <View style={{{{ backgroundColor: '{config["colors"]["surface"]}', borderRadius: 16, padding: 24, alignItems: 'center' }}}}>
        <Text style={{{{ color: '#AAA', fontSize: 16 }}}}>Track your progress here</Text>
        <Text style={{{{ color: '#666', fontSize: 13, marginTop: 8 }}}}>Stats will appear after a few days of use</Text>
      </View>
    </View>
  );
}}
''')

    # 10. Settings placeholder
    with open(output_dir / "app" / "(tabs)" / "settings.tsx", "w") as f:
        f.write(f'''import React from 'react';
import {{ View, Text, TouchableOpacity, Linking }} from 'react-native';

export default function SettingsScreen() {{
  return (
    <View style={{{{ flex: 1, backgroundColor: '{config["colors"]["background"]}', padding: 24, paddingTop: 60 }}}}>
      <Text style={{{{ color: '#FFF', fontSize: 28, fontWeight: 'bold', marginBottom: 24 }}}}>Settings</Text>
      <TouchableOpacity
        style={{{{ backgroundColor: '{config["colors"]["surface"]}', borderRadius: 12, padding: 16, marginBottom: 12 }}}}
        onPress={{() => Linking.openURL('https://printmaxx.io/privacy')}}
      >
        <Text style={{{{ color: '#FFF', fontSize: 16 }}}}>Privacy Policy</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={{{{ backgroundColor: '{config["colors"]["surface"]}', borderRadius: 12, padding: 16, marginBottom: 12 }}}}
        onPress={{() => Linking.openURL('https://printmaxx.io/terms')}}
      >
        <Text style={{{{ color: '#FFF', fontSize: 16 }}}}>Terms of Service</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={{{{ backgroundColor: '{config["colors"]["surface"]}', borderRadius: 12, padding: 16, marginBottom: 12 }}}}
      >
        <Text style={{{{ color: '#FFF', fontSize: 16 }}}}>Restore Purchases</Text>
      </TouchableOpacity>
    </View>
  );
}}
''')

    # 11. Entry point index
    with open(output_dir / "app" / "index.tsx", "w") as f:
        f.write(f'''import {{ useEffect }} from 'react';
import {{ router }} from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Index() {{
  useEffect(() => {{
    checkOnboarding();
  }}, []);

  const checkOnboarding = async () => {{
    const complete = await AsyncStorage.getItem('onboarding_complete');
    if (complete === 'true') {{
      router.replace('/(tabs)');
    }} else {{
      router.replace('/onboarding');
    }}
  }};

  return null;
}}
''')

    # 12. env.template
    with open(output_dir / "env.template", "w") as f:
        f.write(f"""# {name} Environment Variables
# Copy to .env and fill in real values

REVENUECAT_API_KEY=
REVENUECAT_APPLE_API_KEY=
REVENUECAT_GOOGLE_API_KEY=

# App Store Connect
APPLE_TEAM_ID=
APPLE_APP_ID=

# Analytics (optional)
MIXPANEL_TOKEN=
""")

    # 13. .gitignore
    with open(output_dir / ".gitignore", "w") as f:
        f.write("node_modules/\n.expo/\ndist/\n*.jks\n*.p8\n*.p12\n*.key\n*.mobileprovision\n*.orig.*\nweb-build/\n.env\n")

    # Log the build
    _log_build(name, slug, bundle_id, niche_key, config, pricing, str(output_dir))

    log(f"App generation complete: {output_dir}")
    log(f"  Next: cd {output_dir} && npm install && npx expo start")
    return output_dir


def _log_build(name: str, slug: str, bundle_id: str, niche_key: str, config: dict, pricing: dict, output_dir: str) -> None:
    """Log the build to BUILDS CSV."""
    builds_path = safe_path(BUILDS_LOG)
    fields = ["timestamp", "name", "slug", "bundle_id", "niche", "pricing_tier",
              "monthly_price", "yearly_price", "output_dir", "status"]

    row = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "slug": slug,
        "bundle_id": bundle_id,
        "niche": niche_key,
        "pricing_tier": "standard",
        "monthly_price": str(pricing.get("monthly_price", "")),
        "yearly_price": str(pricing.get("yearly_price", "")),
        "output_dir": output_dir,
        "status": "GENERATED",
    }

    write_header = not builds_path.exists()
    with open(builds_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory App Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/app_generator.py --generate --niche health_fitness --name "FitStreak"
  python3 AUTOMATIONS/app_factory/app_generator.py --generate --niche wellness --name "CalmStreak" --pricing premium
  python3 AUTOMATIONS/app_factory/app_generator.py --generate --from-csv --top 3
  python3 AUTOMATIONS/app_factory/app_generator.py --list-niches
        """,
    )
    parser.add_argument("--generate", action="store_true", help="Generate an app")
    parser.add_argument("--list-niches", action="store_true", help="List available niche configurations")
    parser.add_argument("--niche", help="Niche key (e.g., health_fitness, wellness)")
    parser.add_argument("--name", help="App name (e.g., FitStreak)")
    parser.add_argument("--pricing", default="standard", choices=["standard", "premium", "budget"], help="Pricing tier")
    parser.add_argument("--from-csv", action="store_true", help="Generate from top opportunities CSV")
    parser.add_argument("--top", type=int, default=1, help="Number of top opportunities to generate (with --from-csv)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")

    args = parser.parse_args()

    if args.list_niches:
        print("\nAvailable Niche Configurations:")
        print("-" * 60)
        for key, conf in NICHE_CONFIGS.items():
            print(f"  {key:25s} -> {conf['display_name']}")
            print(f"    {'':25s}    Default habits: {len(conf['default_habits'])}, Keywords: {len(conf['keywords'])}")
        print(f"\nPricing tiers: {list(PRICING_TEMPLATES.keys())}")
        return

    if not args.generate:
        parser.print_help()
        return

    if args.from_csv:
        # Generate from top opportunities
        if not OPPORTUNITIES_CSV.exists():
            log("ERROR: Run opportunity_scanner.py --scan first to create opportunities CSV")
            return

        with open(OPPORTUNITIES_CSV, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = sorted(
                [r for r in reader if r.get("status") == "NEW" and r.get("template_fit") == "HIGH"],
                key=lambda r: -float(r.get("score", 0))
            )

        if not rows:
            log("No eligible opportunities found (status=NEW, template_fit=HIGH)")
            return

        for row in rows[:args.top]:
            niche_raw = row.get("niche", "General").lower().replace(" & ", "_").replace(" ", "_")
            # Map to our niche keys
            niche_map = {
                "health_&_fitness": "health_fitness",
                "health_fitness": "health_fitness",
                "wellness": "wellness",
                "religious/spiritual": "religious_spiritual",
                "religious_spiritual": "religious_spiritual",
                "productivity": "productivity",
                "education": "education",
                "food_&_health": "food_health",
                "food_health": "food_health",
                "mental_health": "mental_health",
                "finance": "finance",
            }
            niche_key = niche_map.get(niche_raw, "productivity")
            kw = row.get("keyword", row.get("title", "habit"))
            app_name = _keyword_to_app_name(kw, niche_key)
            generate_app(app_name, niche_key, args.pricing, dry_run=args.dry_run)

    else:
        if not args.niche:
            log("ERROR: --niche is required. Use --list-niches to see options.")
            return
        if not args.name:
            log("ERROR: --name is required.")
            return

        generate_app(args.name, args.niche, args.pricing, dry_run=args.dry_run)


def _keyword_to_app_name(keyword: str, niche_key: str) -> str:
    """Convert a keyword to a reasonable app name."""
    # Clean the keyword
    kw = keyword.strip().title()
    suffix = NICHE_CONFIGS.get(niche_key, {}).get("app_suffix", "streak")

    # If keyword already has a good name shape, use it
    if len(kw.split()) <= 2:
        return f"{kw} {suffix.title()}"

    # Take first two meaningful words
    words = [w for w in kw.split() if w.lower() not in ("the", "a", "an", "and", "or", "for")]
    return f"{' '.join(words[:2])} {suffix.title()}"


if __name__ == "__main__":
    main()
