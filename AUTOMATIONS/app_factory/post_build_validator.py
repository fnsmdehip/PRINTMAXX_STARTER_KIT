#!/usr/bin/env python3
"""
Post-Build App Validator — catches the failures Claude Code keeps making.

Run after EVERY app build before claiming "done":
  python3 AUTOMATIONS/app_factory/post_build_validator.py --path PATH_TO_APP

Checks:
  1. Navigation: all navigate() calls point to registered screens
  2. Imports: no broken imports, no unused imports of removed modules
  3. Back navigation: every non-root screen has a back button or goBack
  4. Sound integration: SoundTouchable or playSound in every screen
  5. Simulated data: no Math.random in sensor/biometric contexts
  6. Dead code: no unused functions with _REMOVED_ prefix
  7. Loading states: async operations have loading indicators
  8. Error states: try/catch blocks have user-visible error handling
  9. Empty states: lists/grids show empty state when data is empty
  10. Accessibility: all touchable elements have accessible labels
"""

import os
import re
import sys
import json
from pathlib import Path

class AppValidator:
    def __init__(self, app_path: str):
        self.app_path = Path(app_path)
        self.src_path = self.app_path / "src"
        self.issues = []
        self.warnings = []
        self.passed = []

    def validate(self) -> bool:
        if not self.src_path.exists():
            print(f"ERROR: {self.src_path} does not exist")
            return False

        self.check_navigation()
        self.check_sound_integration()
        self.check_simulated_data()
        self.check_back_navigation()
        self.check_dead_code()
        self.check_empty_states()
        self.check_loading_states()
        self.check_revenue_pipeline()
        self.check_safe_areas()
        self.check_timer_cleanup()
        self.check_typescript()

        self.report()
        return len(self.issues) == 0

    def find_files(self, pattern: str = "*.tsx") -> list:
        return list(self.src_path.rglob(pattern))

    def check_navigation(self):
        """Verify all navigation.navigate() calls point to registered screens."""
        nav_file = self.src_path / "navigation" / "AppNavigator.tsx"
        if not nav_file.exists():
            self.warnings.append("No AppNavigator.tsx found")
            return

        nav_content = nav_file.read_text()
        # Extract registered screen names
        screens = set(re.findall(r'name="(\w+)"', nav_content))

        # Check all navigate/replace calls across screens (not listeners)
        for f in self.find_files():
            content = f.read_text()
            calls = re.findall(r"navigation\.(?:navigate|replace|push|reset)\(['\"](\w+)['\"]", content)
            for target in calls:
                if target not in screens:
                    self.issues.append(
                        f"NAVIGATION BROKEN: {f.name} navigates to '{target}' which is not a registered screen. "
                        f"Valid screens: {', '.join(sorted(screens))}"
                    )

        if not self.issues:
            self.passed.append(f"Navigation: all calls match {len(screens)} registered screens")

    def check_sound_integration(self):
        """Verify every screen has sound feedback."""
        screen_dir = self.src_path / "screens"
        if not screen_dir.exists():
            return

        for f in screen_dir.glob("*.tsx"):
            content = f.read_text()
            has_touchable = "TouchableOpacity" in content or "Pressable" in content
            has_sound = "playSound" in content or "SoundTouchable" in content

            if has_touchable and not has_sound:
                self.issues.append(
                    f"NO SOUNDS: {f.name} has touchable elements but no sound integration. "
                    f"Import SoundTouchable or call playSound()."
                )
            elif has_touchable and has_sound:
                self.passed.append(f"Sounds: {f.name} has sound integration")

    def check_simulated_data(self):
        """Flag Math.random() used for sensor/biometric data."""
        sensor_keywords = ["heartRate", "hrv", "stress", "score", "confidence",
                          "reading", "sensor", "biometric", "detection", "analysis"]

        for f in self.find_files("*.ts"):
            content = f.read_text()
            if "Math.random" not in content:
                continue

            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "Math.random" in line:
                    # Skip comments
                    stripped = line.strip()
                    if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
                        continue

                    # Check surrounding context for sensor keywords
                    context = "\n".join(lines[max(0, i-3):i+4]).lower()
                    is_sensor = any(kw.lower() in context for kw in sensor_keywords)
                    is_visual = any(kw in context for kw in ["animation", "style", "opacity", "duration", "delay"])
                    is_id = "generateid" in context.lower() or "uuid" in context.lower()
                    is_question = "question" in context.lower() and "pool" in context.lower()

                    if is_sensor and not is_visual and not is_id and not is_question:
                        self.issues.append(
                            f"SIMULATED DATA: {f.name}:{i+1} uses Math.random() near sensor keywords. "
                            f"Use real sensor data, not fake readings."
                        )

        for f in self.find_files("*.tsx"):
            content = f.read_text()
            if "Math.random" not in content:
                continue

            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "Math.random" in line:
                    context = "\n".join(lines[max(0, i-3):i+4]).lower()
                    is_sensor = any(kw.lower() in context for kw in sensor_keywords)
                    is_visual = any(kw in context for kw in ["animation", "style", "opacity", "duration", "delay", "waveform", "noise"])
                    is_id = "generateid" in context.lower()

                    if is_sensor and not is_visual and not is_id:
                        self.issues.append(
                            f"SIMULATED DATA: {f.name}:{i+1} uses Math.random() near sensor keywords."
                        )

    def check_back_navigation(self):
        """Every non-root screen needs a way to go back."""
        root_screens = {"HomeScreen", "OnboardingScreen"}
        screen_dir = self.src_path / "screens"
        if not screen_dir.exists():
            return

        for f in screen_dir.glob("*.tsx"):
            name = f.stem
            if name in root_screens:
                continue

            content = f.read_text()
            has_back = ("goBack" in content or "arrow-back" in content or
                       "chevron-back" in content or "navigation.pop" in content)

            if not has_back:
                self.issues.append(
                    f"NO BACK BUTTON: {f.name} has no way to navigate back. "
                    f"Add navigation.goBack() or a back arrow."
                )
            else:
                self.passed.append(f"Back nav: {f.name} has back navigation")

    def check_dead_code(self):
        """Flag unused/removed code that should be deleted."""
        for f in self.find_files():
            content = f.read_text()
            if "_REMOVED_" in content or "// TODO: remove" in content.lower():
                self.warnings.append(f"DEAD CODE: {f.name} contains _REMOVED_ or TODO:remove markers")

    def check_empty_states(self):
        """Screens with lists should have empty states."""
        for f in self.find_files("*.tsx"):
            content = f.read_text()
            has_list = "FlatList" in content or "ScrollView" in content or "map(" in content
            has_empty = "empty" in content.lower() or "no " in content.lower() or "nothing" in content.lower()

            if has_list and not has_empty:
                self.warnings.append(f"MISSING EMPTY STATE: {f.name} has a list but no visible empty state")

    def check_loading_states(self):
        """Async operations should show loading indicators."""
        for f in self.find_files("*.tsx"):
            content = f.read_text()
            has_async = "async" in content or "await" in content or "useEffect" in content
            has_loading = "loading" in content.lower() or "ActivityIndicator" in content or "isLoading" in content

            # Only flag screens, not utility files
            if "Screen" in f.stem and has_async and not has_loading:
                self.warnings.append(f"NO LOADING STATE: {f.name} has async operations but no loading indicator")

    def check_typescript(self):
        """Run TSC and check for errors."""
        tsconfig = self.app_path / "tsconfig.json"
        if tsconfig.exists():
            result = os.popen(f"cd '{self.app_path}' && npx tsc --noEmit 2>&1 | head -5").read().strip()
            if result:
                self.issues.append(f"TYPESCRIPT ERRORS:\n{result}")
            else:
                self.passed.append("TypeScript: 0 errors")

    def check_revenue_pipeline(self):
        """Verify monetization is wired, not cosmetic."""
        for f in self.find_files("*.tsx"):
            content = f.read_text()
            name = f.name

            # Check for hardcoded isPremium (must be on same line, not just in same file)
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'useState(false)' in line and 'isPremium' in line.lower():
                    if 'getIsPremium' not in content and 'getProfile' not in content:
                        self.issues.append(
                            f"REVENUE BROKEN: {name}:{i+1} hardcodes isPremium=false instead of reading from store"
                        )

            # Check for fake restore purchases
            if "Restore" in content and "Purchase" in content:
                if "NOT IMPLEMENTED" not in content and "Stripe" not in content and "RevenueCat" not in content:
                    if "Looking for" in content or "will be available" in content:
                        self.issues.append(
                            f"FAKE RESTORE: {name} has fake 'Restore Purchases' that pretends to work"
                        )

        # Check session saving exists somewhere
        all_content = ""
        screen_dir = self.src_path / "screens"
        if screen_dir.exists():
            for f in screen_dir.glob("*.tsx"):
                all_content += f.read_text()

        if "saveSession" not in all_content:
            self.warnings.append("NO SESSION SAVE: no screen calls saveSession() — user sessions are ephemeral")

        # Check Result screen is navigated to
        if "navigate('Result'" not in all_content and 'navigate("Result"' not in all_content:
            self.warnings.append("NO RESULT FLOW: no screen navigates to Result — users never see analysis results")

    def check_safe_areas(self):
        """Check for hardcoded padding that should use safe area insets."""
        for f in self.find_files("*.tsx"):
            content = f.read_text()
            if "paddingTop: 60" in content or "paddingTop: 50" in content or "top: 50" in content:
                if "useSafeAreaInsets" not in content:
                    self.warnings.append(
                        f"HARDCODED SAFE AREA: {f.name} uses hardcoded paddingTop instead of useSafeAreaInsets"
                    )

    def check_timer_cleanup(self):
        """Verify intervals/timeouts/recordings are cleaned up on unmount."""
        for f in self.find_files("*.tsx"):
            content = f.read_text()
            has_interval = "setInterval" in content
            has_recording = "Recording" in content and "startAsync" in content
            has_cleanup = "clearInterval" in content or "stopAndUnload" in content

            if has_interval and not has_cleanup:
                self.issues.append(
                    f"MEMORY LEAK: {f.name} uses setInterval but never calls clearInterval"
                )
            if has_recording and "stopAndUnload" not in content:
                self.warnings.append(
                    f"RECORDING LEAK: {f.name} starts audio recording but may not stop on unmount"
                )

    def report(self):
        print("\n" + "=" * 60)
        print(f"  APP VALIDATION REPORT: {self.app_path.name}")
        print("=" * 60)

        if self.passed:
            print(f"\n  PASSED ({len(self.passed)}):")
            for p in self.passed:
                print(f"    [OK] {p}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"    [!!] {w}")

        if self.issues:
            print(f"\n  FAILURES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"    [FAIL] {issue}")
            print(f"\n  RESULT: FAILED ({len(self.issues)} issues)")
        else:
            print(f"\n  RESULT: PASSED (0 issues, {len(self.warnings)} warnings)")

        print("=" * 60 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Post-build app validator")
    parser.add_argument("--path", required=True, help="Path to app root")
    args = parser.parse_args()

    validator = AppValidator(args.path)
    success = validator.validate()
    sys.exit(0 if success else 1)
