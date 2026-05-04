#!/usr/bin/env python3
"""
PRINTMAXX Health App Factory Pipeline
======================================
App factory DAG that scaffolds health-tracking React Native apps using
react-native-health-connect (matinzd/react-native-health-connect) as the
Android Health Connect bridge. Generates calorie tracker, sleep tracker,
and fitness streak variants from a single parameterized template with
RevenueCat IAP and AdMob wired in from base.

Usage:
    python3 health_app_factory.py --run
    python3 health_app_factory.py --status
    python3 health_app_factory.py --dry-run
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import traceback
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"Path {resolved} is outside PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task_name):
        return []

    def capture_skill_from_result(task_name, result):
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
LOG_FILE = LOG_DIR / "health_app_factory.log"
OUTPUT_DIR = AUTOMATIONS_DIR / "health_app_factory"
STATUS_FILE = OUTPUT_DIR / "pipeline_status.json"
SKILLS_LOG = OUTPUT_DIR / "skills_log.csv"

HEALTH_CONNECT_VERSION = "2.1.0"
REVENUECAT_VERSION = "7.27.0"
ADMOB_VERSION = "0.29.0"
RN_VERSION = "0.76.5"

APP_VARIANTS = [
    {
        "name": "calorie_tracker",
        "display_name": "CalorieTrack Pro",
        "bundle_id_suffix": "calorietrack",
        "health_permissions": [
            "ActiveCaloriesBurned",
            "TotalCaloriesBurned",
            "NutritionCaloriesConsumed",
            "BasalMetabolicRate",
            "Weight",
            "Height",
            "BodyFat",
        ],
        "primary_metric": "calories",
        "color_scheme": {"primary": "#FF6B35", "secondary": "#FFD166", "bg": "#1A1A2E"},
        "admob_ad_unit_type": "rewarded",
        "revenuecat_entitlement": "pro_calories",
        "screen_count": 5,
    },
    {
        "name": "sleep_tracker",
        "display_name": "SleepCycle Pro",
        "bundle_id_suffix": "sleeptrack",
        "health_permissions": [
            "SleepSession",
            "SleepStage",
            "HeartRate",
            "RespiratoryRate",
            "OxygenSaturation",
            "RestingHeartRate",
        ],
        "primary_metric": "sleep_duration",
        "color_scheme": {"primary": "#6C63FF", "secondary": "#A8DADC", "bg": "#0D0D1A"},
        "admob_ad_unit_type": "interstitial",
        "revenuecat_entitlement": "pro_sleep",
        "screen_count": 4,
    },
    {
        "name": "fitness_streak",
        "display_name": "FitStreak Pro",
        "bundle_id_suffix": "fitstreak",
        "health_permissions": [
            "Steps",
            "Distance",
            "ActiveCaloriesBurned",
            "ExerciseSession",
            "HeartRate",
            "Vo2Max",
            "Power",
        ],
        "primary_metric": "streak_days",
        "color_scheme": {"primary": "#00C49A", "secondary": "#00B4D8", "bg": "#0A1628"},
        "admob_ad_unit_type": "banner",
        "revenuecat_entitlement": "pro_fitness",
        "screen_count": 6,
    },
]

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging():
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = safe_path(LOG_FILE)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_path), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("health_app_factory")


logger = None

# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------

def load_status():
    status_path = safe_path(STATUS_FILE)
    if status_path.exists():
        try:
            with open(str(status_path), "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"pipeline_runs": [], "variants": {}, "last_run": None}


def save_status(status_data):
    status_path = safe_path(STATUS_FILE)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(status_path), "w") as f:
        json.dump(status_data, f, indent=2, default=str)


def update_variant_status(status_data, variant_name, stage, state, detail=""):
    if variant_name not in status_data["variants"]:
        status_data["variants"][variant_name] = {}
    status_data["variants"][variant_name][stage] = {
        "state": state,
        "timestamp": datetime.utcnow().isoformat(),
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Skills CSV log
# ---------------------------------------------------------------------------

def log_skill(task_name, skill_name, outcome, detail=""):
    skills_path = safe_path(SKILLS_LOG)
    skills_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not skills_path.exists()
    with open(str(skills_path), "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "task", "skill", "outcome", "detail"])
        writer.writerow([datetime.utcnow().isoformat(), task_name, skill_name, outcome, detail])


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def gen_package_json(variant, dry_run=False):
    """Generate package.json for a React Native app variant."""
    pkg = {
        "name": variant["name"].replace("_", "-"),
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "android": "react-native run-android",
            "ios": "react-native run-ios",
            "lint": "eslint .",
            "start": "react-native start",
            "test": "jest",
            "build:android": "cd android && ./gradlew assembleRelease",
            "build:android:bundle": "cd android && ./gradlew bundleRelease",
        },
        "dependencies": {
            "react": "18.3.1",
            "react-native": RN_VERSION,
            "react-native-health-connect": HEALTH_CONNECT_VERSION,
            "react-native-purchases": REVENUECAT_VERSION,
            f"react-native-google-mobile-ads": ADMOB_VERSION,
            "@react-navigation/native": "^6.1.18",
            "@react-navigation/bottom-tabs": "^6.6.1",
            "@react-navigation/stack": "^6.4.1",
            "react-native-safe-area-context": "^4.12.0",
            "react-native-screens": "^3.35.0",
            "react-native-vector-icons": "^10.2.0",
            "react-native-async-storage": "^1.23.1",
            "react-native-reanimated": "^3.16.2",
            "react-native-gesture-handler": "^2.21.0",
            "date-fns": "^3.6.0",
        },
        "devDependencies": {
            "@babel/core": "^7.25.0",
            "@babel/preset-env": "^7.25.0",
            "@babel/runtime": "^7.25.0",
            "@react-native/eslint-config": "^0.76.5",
            "@react-native/metro-config": "^0.76.5",
            "@react-native/typescript-config": "^0.76.5",
            "@types/react": "^18.3.1",
            "@types/react-native": "^0.73.0",
            "eslint": "^8.57.0",
            "jest": "^29.7.0",
            "typescript": "5.0.4",
        },
        "jest": {
            "preset": "react-native",
        },
        "engines": {"node": ">=18"},
    }
    return json.dumps(pkg, indent=2)


def gen_android_manifest_permissions(variant):
    """Generate AndroidManifest.xml Health Connect permission entries."""
    perm_lines = []
    for perm in variant["health_permissions"]:
        perm_lines.append(
            f'    <uses-permission android:name="android.permission.health.READ_{perm.upper()}" />'
        )
        perm_lines.append(
            f'    <uses-permission android:name="android.permission.health.WRITE_{perm.upper()}" />'
        )
    return "\n".join(perm_lines)


def gen_android_manifest(variant):
    """Generate AndroidManifest.xml content."""
    permissions = gen_android_manifest_permissions(variant)
    bundle_id = f"com.printmaxx.{variant['bundle_id_suffix']}"
    return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{bundle_id}">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.VIBRATE" />
{permissions}

    <!-- Health Connect availability check -->
    <queries>
        <package android:name="com.google.android.apps.healthdata" />
        <intent>
            <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" />
        </intent>
    </queries>

    <application
        android:name=".MainApplication"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:allowBackup="false"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:label="@string/app_name"
            android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|screenSize|smallestScreenSize|uiMode"
            android:launchMode="singleTask"
            android:windowSoftInputMode="adjustResize"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <!-- Health Connect permission handler -->
            <intent-filter>
                <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" />
            </intent-filter>
        </activity>

        <!-- AdMob App ID - replace with real ID before release -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-3940256099942544~3347511713" />
    </application>
</manifest>
"""


def gen_health_connect_module(variant):
    """Generate the HealthConnect integration TypeScript module."""
    perms_ts = ",\n    ".join(
        [f'{{ accessType: "read", recordType: "{p}" }}' for p in variant["health_permissions"]]
        + [f'{{ accessType: "write", recordType: "{p}" }}' for p in variant["health_permissions"]]
    )

    read_calls = []
    for perm in variant["health_permissions"]:
        read_calls.append(f"""
  async read{perm}(startTime: string, endTime: string) {{
    try {{
      const records = await readRecords('{perm}', {{
        timeRangeFilter: {{
          operator: 'between',
          startTime,
          endTime,
        }},
      }});
      return records.records;
    }} catch (error) {{
      console.error('Error reading {perm}:', error);
      return [];
    }}
  }},""")

    return f"""/**
 * Health Connect integration for {variant['display_name']}
 * Uses react-native-health-connect v{HEALTH_CONNECT_VERSION}
 * https://github.com/matinzd/react-native-health-connect
 */
import {{
  initialize,
  requestPermission,
  readRecords,
  insertRecords,
  getSdkStatus,
  SdkAvailabilityStatus,
}} from 'react-native-health-connect';

export const HEALTH_PERMISSIONS = [
    {perms_ts}
] as const;

export const HealthConnectService = {{
  async checkAvailability(): Promise<boolean> {{
    try {{
      const status = await getSdkStatus();
      return status === SdkAvailabilityStatus.SDK_AVAILABLE;
    }} catch {{
      return false;
    }}
  }},

  async init(): Promise<boolean> {{
    try {{
      const available = await this.checkAvailability();
      if (!available) {{
        console.warn('Health Connect SDK not available on this device');
        return false;
      }}
      return await initialize();
    }} catch (error) {{
      console.error('Failed to initialize Health Connect:', error);
      return false;
    }}
  }},

  async requestPermissions(): Promise<boolean> {{
    try {{
      const granted = await requestPermission(HEALTH_PERMISSIONS as any);
      return granted.length === HEALTH_PERMISSIONS.length;
    }} catch (error) {{
      console.error('Failed to request Health Connect permissions:', error);
      return false;
    }}
  }},
{"".join(read_calls)}
}};

export default HealthConnectService;
"""


def gen_revenuecat_module(variant):
    """Generate RevenueCat IAP integration module."""
    return f"""/**
 * RevenueCat IAP integration for {variant['display_name']}
 * Uses react-native-purchases v{REVENUECAT_VERSION}
 */
import Purchases, {{
  PurchasesPackage,
  CustomerInfo,
  LOG_LEVEL,
}} from 'react-native-purchases';

const REVENUECAT_API_KEY_ANDROID = 'goog_REPLACE_WITH_REAL_KEY';
const ENTITLEMENT_ID = '{variant['revenuecat_entitlement']}';

export const RevenueCatService = {{
  async init(): Promise<void> {{
    try {{
      if (__DEV__) {{
        await Purchases.setLogLevel(LOG_LEVEL.DEBUG);
      }}
      await Purchases.configure({{
        apiKey: REVENUECAT_API_KEY_ANDROID,
      }});
    }} catch (error) {{
      console.error('RevenueCat init failed:', error);
    }}
  }},

  async getOfferings(): Promise<PurchasesPackage[]> {{
    try {{
      const offerings = await Purchases.getOfferings();
      return offerings.current?.availablePackages ?? [];
    }} catch (error) {{
      console.error('Failed to get offerings:', error);
      return [];
    }}
  }},

  async purchasePackage(pkg: PurchasesPackage): Promise<boolean> {{
    try {{
      const {{ customerInfo }} = await Purchases.purchasePackage(pkg);
      return this.hasProAccess(customerInfo);
    }} catch (error: any) {{
      if (!error.userCancelled) {{
        console.error('Purchase failed:', error);
      }}
      return false;
    }}
  }},

  async restorePurchases(): Promise<boolean> {{
    try {{
      const customerInfo = await Purchases.restorePurchases();
      return this.hasProAccess(customerInfo);
    }} catch (error) {{
      console.error('Restore failed:', error);
      return false;
    }}
  }},

  async checkProAccess(): Promise<boolean> {{
    try {{
      const customerInfo = await Purchases.getCustomerInfo();
      return this.hasProAccess(customerInfo);
    }} catch (error) {{
      console.error('Failed to check pro access:', error);
      return false;
    }}
  }},

  hasProAccess(customerInfo: CustomerInfo): boolean {{
    return typeof customerInfo.entitlements.active[ENTITLEMENT_ID] !== 'undefined';
  }},
}};

export default RevenueCatService;
"""


def gen_admob_module(variant):
    """Generate AdMob integration module."""
    ad_type = variant["admob_ad_unit_type"]

    if ad_type == "banner":
        ad_component = """import { BannerAd, BannerAdSize, TestIds } from 'react-native-google-mobile-ads';

export const AdBanner: React.FC = () => {
  const adUnitId = __DEV__ ? TestIds.BANNER : 'ca-app-pub-REPLACE~REPLACE';
  return (
    <BannerAd
      unitId={adUnitId}
      size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
      requestOptions={{ requestNonPersonalizedAdsOnly: true }}
    />
  );
};"""
    elif ad_type == "interstitial":
        ad_component = """import {
  InterstitialAd,
  AdEventType,
  TestIds,
} from 'react-native-google-mobile-ads';

const adUnitId = __DEV__ ? TestIds.INTERSTITIAL : 'ca-app-pub-REPLACE~REPLACE';
const interstitial = InterstitialAd.createForAdRequest(adUnitId, {
  requestNonPersonalizedAdsOnly: true,
});

export const AdInterstitialService = {
  load(): void {
    interstitial.load();
  },
  show(): void {
    if (interstitial.loaded) {
      interstitial.show();
    }
  },
  onLoaded(cb: () => void) {
    return interstitial.addAdEventListener(AdEventType.LOADED, cb);
  },
};"""
    else:  # rewarded
        ad_component = """import {
  RewardedAd,
  RewardedAdEventType,
  TestIds,
} from 'react-native-google-mobile-ads';

const adUnitId = __DEV__ ? TestIds.REWARDED : 'ca-app-pub-REPLACE~REPLACE';
const rewarded = RewardedAd.createForAdRequest(adUnitId, {
  requestNonPersonalizedAdsOnly: true,
});

export const AdRewardedService = {
  load(): void {
    rewarded.load();
  },
  show(onEarned: (amount: number) => void): void {
    if (rewarded.loaded) {
      rewarded.show();
    }
    rewarded.addAdEventListener(RewardedAdEventType.EARNED_REWARD, (reward) => {
      onEarned(reward.amount);
    });
  },
};"""

    return f"""/**
 * AdMob integration for {variant['display_name']}
 * Uses react-native-google-mobile-ads v{ADMOB_VERSION}
 * Ad unit type: {ad_type}
 */
import React from 'react';
import mobileAds, {{ MaxAdContentRating }} from 'react-native-google-mobile-ads';

export async function initAdMob(): Promise<void> {{
  try {{
    await mobileAds().initialize();
    await mobileAds().setRequestConfiguration({{
      maxAdContentRating: MaxAdContentRating.PG,
      tagForChildDirectedTreatment: false,
      tagForUnderAgeOfConsent: false,
    }});
  }} catch (error) {{
    console.error('AdMob init failed:', error);
  }}
}}

{ad_component}
"""


def gen_app_tsx(variant):
    """Generate root App.tsx."""
    colors = variant["color_scheme"]
    return f"""/**
 * {variant['display_name']} — Root App Component
 * Generated by PRINTMAXX Health App Factory
 */
import React, {{ useEffect, useState }} from 'react';
import {{
  SafeAreaView,
  StatusBar,
  StyleSheet,
  View,
  Text,
  ActivityIndicator,
}} from 'react-native';
import HealthConnectService from './src/services/HealthConnectService';
import RevenueCatService from './src/services/RevenueCatService';
import {{ initAdMob }} from './src/services/AdMobService';
import MainNavigator from './src/navigation/MainNavigator';

export default function App() {{
  const [isReady, setIsReady] = useState(false);
  const [initError, setInitError] = useState<string | null>(null);

  useEffect(() => {{
    (async () => {{
      try {{
        await Promise.all([
          RevenueCatService.init(),
          initAdMob(),
        ]);
        const hcOk = await HealthConnectService.init();
        if (hcOk) {{
          await HealthConnectService.requestPermissions();
        }}
      }} catch (e: any) {{
        setInitError(e?.message ?? 'Initialization failed');
      }} finally {{
        setIsReady(true);
      }}
    }})();
  }}, []);

  if (!isReady) {{
    return (
      <View style={{styles.loading}}>
        <ActivityIndicator size="large" color="{colors['primary']}" />
      </View>
    );
  }}

  if (initError) {{
    return (
      <View style={{styles.loading}}>
        <Text style={{styles.errorText}}>{{initError}}</Text>
      </View>
    );
  }}

  return (
    <SafeAreaView style={{styles.root}}>
      <StatusBar barStyle="light-content" backgroundColor="{colors['bg']}" />
      <MainNavigator />
    </SafeAreaView>
  );
}}

const styles = StyleSheet.create({{
  root: {{ flex: 1, backgroundColor: '{colors['bg']}' }},
  loading: {{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '{colors['bg']}' }},
  errorText: {{ color: '#FF4444', fontSize: 14, textAlign: 'center', padding: 16 }},
}});
"""


def gen_tsconfig(variant):
    """Generate tsconfig.json."""
    return json.dumps(
        {
            "extends": "@react-native/typescript-config/tsconfig.json",
            "compilerOptions": {
                "strict": True,
                "baseUrl": ".",
                "paths": {
                    "@services/*": ["src/services/*"],
                    "@screens/*": ["src/screens/*"],
                    "@components/*": ["src/components/*"],
                    "@hooks/*": ["src/hooks/*"],
                    "@utils/*": ["src/utils/*"],
                },
            },
        },
        indent=2,
    )


def gen_babel_config(variant):
    """Generate babel.config.js."""
    return """module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./src'],
        extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json', '.native.js'],
        alias: {
          '@services': './src/services',
          '@screens': './src/screens',
          '@components': './src/components',
          '@hooks': './src/hooks',
          '@utils': './src/utils',
        },
      },
    ],
    'react-native-reanimated/plugin',
  ],
};
"""


def gen_gradle_app(variant):
    """Generate android/app/build.gradle content."""
    bundle_id = f"com.printmaxx.{variant['bundle_id_suffix']}"
    return f"""apply plugin: "com.android.application"
apply plugin: "org.jetbrains.kotlin.android"
apply plugin: "com.facebook.react"

android {{
    ndkVersion rootProject.ext.ndkVersion
    buildToolsVersion rootProject.ext.buildToolsVersion
    compileSdk rootProject.ext.compileSdkVersion

    namespace "{bundle_id}"
    defaultConfig {{
        applicationId "{bundle_id}"
        minSdkVersion 26
        targetSdkVersion rootProject.ext.targetSdkVersion
        versionCode 1
        versionName "1.0"
    }}

    signingConfigs {{
        debug {{
            storeFile file('debug.keystore')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }}
        release {{
            if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {{
                storeFile file(MYAPP_UPLOAD_STORE_FILE)
                storePassword MYAPP_UPLOAD_STORE_PASSWORD
                keyAlias MYAPP_UPLOAD_KEY_ALIAS
                keyPassword MYAPP_UPLOAD_KEY_PASSWORD
            }}
        }}
    }}

    buildTypes {{
        debug {{
            signingConfig signingConfigs.debug
        }}
        release {{
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"
        }}
    }}
}}

dependencies {{
    implementation("com.facebook.react:react-android")
    implementation("androidx.health.connect:connect-client:1.1.0-rc01")
    implementation("com.google.android.gms:play-services-ads:23.1.0")
    if (hermesEnabled.toBoolean()) {{
        implementation("com.facebook.react:hermes-android")
    }} else {{
        implementation jscFlavor
    }}
}}

apply from: file("../../node_modules/@react-native-community/cli-platform-android/native_modules.gradle")
applyNativeModulesAppBuildGradle(project)
"""


def gen_readme(variant):
    """Generate README.md content."""
    perms_list = "\n".join(f"- `{p}`" for p in variant["health_permissions"])
    return f"""# {variant['display_name']}

> Generated by PRINTMAXX Health App Factory

## Overview

A React Native health tracking app for Android using Health Connect.

**Primary metric:** `{variant['primary_metric']}`

## Health Connect Permissions

{perms_list}

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react-native-health-connect | {HEALTH_CONNECT_VERSION} | Android Health Connect bridge |
| react-native-purchases | {REVENUECAT_VERSION} | RevenueCat IAP |
| react-native-google-mobile-ads | {ADMOB_VERSION} | AdMob ads |

## Setup

```bash
npm install
cd android && ./gradlew assembleDebug
```

## Before Release

1. Replace AdMob App ID in `AndroidManifest.xml`
2. Replace RevenueCat API key in `src/services/RevenueCatService.ts`
3. Replace AdMob ad unit IDs in `src/services/AdMobService.ts`
4. Configure signing keystore in `android/gradle.properties`
"""


# ---------------------------------------------------------------------------
# File scaffolding
# ---------------------------------------------------------------------------

FILE_GENERATORS = {
    "package.json": gen_package_json,
    "App.tsx": gen_app_tsx,
    "tsconfig.json": gen_tsconfig,
    "babel.config.js": gen_babel_config,
    "android/app/build.gradle": gen_gradle_app,
    "android/app/src/main/AndroidManifest.xml": gen_android_manifest,
    "src/services/HealthConnectService.ts": gen_health_connect_module,
    "src/services/RevenueCatService.ts": gen_revenuecat_module,
    "src/services/AdMobService.ts": gen_admob_module,
    "README.md": gen_readme,
}

PLACEHOLDER_DIRS = [
    "src/screens",
    "src/components",
    "src/hooks",
    "src/utils",
    "src/navigation",
    "android/app/src/main/res/values",
    "android/app/src/main/res/mipmap-hdpi",
]


def scaffold_variant(variant, output_root, dry_run=False):
    """Scaffold all files for one app variant."""
    app_dir = output_root / variant["name"]
    generated = []
    errors = []

    for rel_path, generator_fn in FILE_GENERATORS.items():
        try:
            content = generator_fn(variant)
            target = safe_path(app_dir / rel_path)
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                with open(str(target), "w", encoding="utf-8") as fh:
                    fh.write(content)
            generated.append(rel_path)
        except Exception as exc:
            errors.append((rel_path, str(exc)))

    for rel_dir in PLACEHOLDER_DIRS:
        try:
            target_dir = safe_path(app_dir / rel_dir)
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                gitkeep = safe_path(target_dir / ".gitkeep")
                gitkeep.touch()
        except Exception as exc:
            errors.append((rel_dir, str(exc)))

    return generated, errors


# ---------------------------------------------------------------------------
# npm install (optional, skipped if node not available)
# ---------------------------------------------------------------------------

def run_npm_install(app_dir, dry_run=False):
    """Run npm install inside the scaffolded app directory."""
    if dry_run:
        return True, "dry-run: skipped npm install"
    try:
        result = subprocess.run(
            ["npm", "install", "--legacy-peer-deps"],
            cwd=str(app_dir),
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            return True, "npm install succeeded"
        return False, result.stderr[:500]
    except FileNotFoundError:
        return False, "npm not found — skipping install"
    except subprocess.TimeoutExpired:
        return False, "npm install timed out"
    except Exception as exc:
        return False, str(exc)


# ---------------------------------------------------------------------------
# Health Connect version check via GitHub API
# ---------------------------------------------------------------------------

def fetch_latest_hc_version():
    """Fetch latest react-native-health-connect version from npm registry."""
    url = "https://registry.npmjs.org/react-native-health-connect/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "printmaxx-factory/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("version", HEALTH_CONNECT_VERSION)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        return HEALTH_CONNECT_VERSION


# ---------------------------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------------------------

def stage_preflight(status_data, dry_run=False):
    """Preflight: verify environment and fetch latest package versions."""
    logger.info("=== Stage: Preflight ===")
    issues = []

    # Check node available
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
        node_ver = r.stdout.strip()
        logger.info(f"Node: {node_ver}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        issues.append("node not found in PATH")
        logger.warning("node not found — npm install will be skipped")

    # Check npm available
    try:
        r = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=10)
        npm_ver = r.stdout.strip()
        logger.info(f"npm: {npm_ver}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        issues.append("npm not found in PATH")

    # Fetch latest HC version
    latest_hc = fetch_latest_hc_version()
    if latest_hc != HEALTH_CONNECT_VERSION:
        logger.info(f"Note: Latest react-native-health-connect is {latest_hc} (using {HEALTH_CONNECT_VERSION})")

    status_data["preflight"] = {
        "state": "ok" if not issues else "warning",
        "issues": issues,
        "timestamp": datetime.utcnow().isoformat(),
        "latest_hc_version": latest_hc,
    }
    return True


def stage_scaffold(status_data, dry_run=False):
    """Scaffold all app variants."""
    logger.info("=== Stage: Scaffold ===")
    output_root = safe_path(OUTPUT_DIR / "apps")
    if not dry_run:
        output_root.mkdir(parents=True, exist_ok=True)

    all_ok = True
    for variant in APP_VARIANTS:
        logger.info(f"Scaffolding variant: {variant['display_name']}")
        try:
            skills = recall_skills_for_task(f"scaffold_{variant['name']}")
            generated, errors = scaffold_variant(variant, output_root, dry_run=dry_run)
            log_skill(f"scaffold_{variant['name']}", "scaffold_variant", "ok", f"{len(generated)} files")

            if errors:
                for path, err in errors:
                    logger.error(f"  Error writing {path}: {err}")
                update_variant_status(status_data, variant["name"], "scaffold", "error",
                                      f"{len(errors)} errors")
                all_ok = False
            else:
                logger.info(f"  Generated {len(generated)} files for {variant['name']}")
                update_variant_status(status_data, variant["name"], "scaffold", "ok",
                                      f"{len(generated)} files written")
                capture_skill_from_result(f"scaffold_{variant['name']}", {"files": generated})
        except Exception as exc:
            logger.error(f"  Fatal error scaffolding {variant['name']}: {exc}")
            logger.debug(traceback.format_exc())
            update_variant_status(status_data, variant["name"], "scaffold", "error", str(exc))
            all_ok = False

    return all_ok


def stage_npm_install(status_data, dry_run=False):
    """Run npm install for each variant."""
    logger.info("=== Stage: npm install ===")
    output_root = safe_path(OUTPUT_DIR / "apps")

    for variant in APP_VARIANTS:
        app_dir = safe_path(output_root / variant["name"])
        pkg_json = safe_path(app_dir / "package.json")
        if not pkg_json.exists() and not dry_run:
            logger.warning(f"  Skipping {variant['name']}: package.json not found")
            update_variant_status(status_data, variant["name"], "npm_install", "skipped",
                                  "package.json missing")
            continue

        logger.info(f"  Running npm install for {variant['name']} ...")
        ok, detail = run_npm_install(app_dir, dry_run=dry_run)
        state = "ok" if ok else "warning"
        update_variant_status(status_data, variant["name"], "npm_install", state, detail)
        if ok:
            logger.info(f"  {variant['name']}: {detail}")
        else:
            logger.warning(f"  {variant['name']}: {detail}")

    return True


def stage_manifest_report(status_data, dry_run=False):
    """Write a CSV manifest of all generated files."""
    logger.info("=== Stage: Manifest Report ===")
    manifest_path = safe_path(OUTPUT_DIR / "generated_manifest.csv")
    output_root = safe_path(OUTPUT_DIR / "apps")

    rows = []
    for variant in APP_VARIANTS:
        app_dir = safe_path(output_root / variant["name"])
        if app_dir.exists():
            for fpath in sorted(app_dir.rglob("*")):
                if fpath.is_file():
                    rel = fpath.relative_to(app_dir)
                    rows.append({
                        "variant": variant["name"],
                        "display_name": variant["display_name"],
                        "file": str(rel),
                        "size_bytes": fpath.stat().st_size,
                        "generated_at": datetime.utcnow().isoformat(),
                    })

    if not dry_run and rows:
        with open(str(manifest_path), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["variant", "display_name", "file",
                                                    "size_bytes", "generated_at"])
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"Manifest written: {manifest_path} ({len(rows)} files)")
    elif dry_run:
        logger.info(f"[dry-run] Would write manifest with {len(rows)} entries")

    status_data["manifest"] = {
        "state": "ok",
        "file_count": len(rows),
        "timestamp": datetime.utcnow().isoformat(),
    }
    return True


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

PIPELINE_STAGES = [
    ("preflight", stage_preflight),
    ("scaffold", stage_scaffold),
    ("npm_install", stage_npm_install),
    ("manifest_report", stage_manifest_report),
]


def run_pipeline(dry_run=False):
    """Execute the full health app factory pipeline."""
    logger.info("=" * 60)
    logger.info(f"PRINTMAXX Health App Factory — {'DRY RUN' if dry_run else 'RUN'}")
    logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    logger.info(f"Variants: {[v['name'] for v in APP_VARIANTS]}")
    logger.info("=" * 60)

    status_data = load_status()
    run_record = {
        "started_at": datetime.utcnow().isoformat(),
        "dry_run": dry_run,
        "stages": {},
    }

    overall_ok = True
    for stage_name, stage_fn in PIPELINE_STAGES:
        logger.info(f"\n--- {stage_name} ---")
        try:
            ok = stage_fn(status_data, dry_run=dry_run)
            run_record["stages"][stage_name] = "ok" if ok else "warning"
            if not ok:
                overall_ok = False
        except Exception as exc:
            logger.error(f"Stage {stage_name} raised: {exc}")
            logger.debug(traceback.format_exc())
            run_record["stages"][stage_name] = f"error: {exc}"
            overall_ok = False

    run_record["completed_at"] = datetime.utcnow().isoformat()
    run_record["result"] = "ok" if overall_ok else "partial"
    status_data["last_run"] = run_record
    status_data["pipeline_runs"].append(run_record)
    # Keep last 50 run records
    status_data["pipeline_runs"] = status_data["pipeline_runs"][-50:]

    try:
        save_status(status_data)
    except Exception as exc:
        logger.error(f"Failed to save status: {exc}")

    logger.info(f"\nPipeline complete — result: {run_record['result']}")
    return overall_ok


def print_status():
    """Print human-readable pipeline status."""
    status_data = load_status()

    print("\n=== PRINTMAXX Health App Factory — Pipeline Status ===\n")

    last = status_data.get("last_run")
    if last:
        print(f"Last run:    {last.get('started_at', 'unknown')}")
        print(f"Result:      {last.get('result', 'unknown')}")
        print(f"Dry run:     {last.get('dry_run', False)}")
        print(f"Stages:      {json.dumps(last.get('stages', {}), indent=2)}")
    else:
        print("No pipeline runs recorded yet.")

    variants = status_data.get("variants", {})
    if variants:
        print("\nVariant Status:")
        for vname, stages in variants.items():
            print(f"\n  {vname}:")
            for stage, info in stages.items():
                print(f"    {stage}: {info.get('state')} — {info.get('detail', '')}")

    manifest = status_data.get("manifest")
    if manifest:
        print(f"\nManifest: {manifest.get('file_count', 0)} files @ {manifest.get('timestamp', '')}")

    print(f"\nTotal pipeline runs: {len(status_data.get('pipeline_runs', []))}")
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Health App Factory — scaffolds React Native health-tracking apps"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full pipeline (scaffold + npm install + manifest)",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print pipeline status from last run",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate pipeline without writing files or running npm",
    )
    return parser.parse_args()


def main():
    global logger
    logger = setup_logging()

    args = parse_args()

    try:
        if args.status:
            print_status()
            sys.exit(0)
        elif args.dry_run:
            ok = run_pipeline(dry_run=True)
            sys.exit(0 if ok else 1)
        elif args.run:
            ok = run_pipeline(dry_run=False)
            sys.exit(0 if ok else 1)
    except KeyboardInterrupt:
        if logger:
            logger.info("Interrupted by user")
        sys.exit(130)
    except Exception as exc:
        if logger:
            logger.error(f"Fatal: {exc}")
            logger.debug(traceback.format_exc())
        else:
            print(f"Fatal: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()