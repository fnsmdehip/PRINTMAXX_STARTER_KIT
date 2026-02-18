#!/bin/bash
# bump_version.sh - Increment version across iOS and Android
# Usage: ./bump_version.sh [major|minor|patch] [--commit]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
IOS_DIR="$ROOT_DIR/ios"
ANDROID_DIR="$ROOT_DIR/android"

# Default values
BUMP_TYPE="${1:-patch}"
COMMIT_CHANGES=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --commit)
            COMMIT_CHANGES=true
            shift
            ;;
        major|minor|patch)
            BUMP_TYPE="$arg"
            shift
            ;;
        *)
            ;;
    esac
done

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get current iOS version
get_ios_version() {
    local plist_path="$IOS_DIR/App/Info.plist"
    if [[ -f "$plist_path" ]]; then
        /usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" "$plist_path" 2>/dev/null || echo "1.0.0"
    else
        echo "1.0.0"
    fi
}

# Get current iOS build number
get_ios_build() {
    local plist_path="$IOS_DIR/App/Info.plist"
    if [[ -f "$plist_path" ]]; then
        /usr/libexec/PlistBuddy -c "Print CFBundleVersion" "$plist_path" 2>/dev/null || echo "1"
    else
        echo "1"
    fi
}

# Get current Android version
get_android_version() {
    local gradle_path="$ANDROID_DIR/app/build.gradle"
    if [[ -f "$gradle_path" ]]; then
        grep 'versionName' "$gradle_path" | head -1 | sed 's/[^0-9.]//g'
    else
        echo "1.0.0"
    fi
}

# Get current Android version code
get_android_version_code() {
    local gradle_path="$ANDROID_DIR/app/build.gradle"
    if [[ -f "$gradle_path" ]]; then
        grep 'versionCode' "$gradle_path" | head -1 | sed 's/[^0-9]//g'
    else
        echo "1"
    fi
}

# Calculate new version
bump_version() {
    local current="$1"
    local type="$2"

    IFS='.' read -r major minor patch <<< "$current"

    case $type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Update iOS version
update_ios_version() {
    local version="$1"
    local build="$2"
    local plist_path="$IOS_DIR/App/Info.plist"

    if [[ -f "$plist_path" ]]; then
        /usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $version" "$plist_path"
        /usr/libexec/PlistBuddy -c "Set :CFBundleVersion $build" "$plist_path"
        log_info "Updated iOS version to $version ($build)"
    else
        log_warn "iOS Info.plist not found at $plist_path"
    fi
}

# Update Android version
update_android_version() {
    local version="$1"
    local code="$2"
    local gradle_path="$ANDROID_DIR/app/build.gradle"

    if [[ -f "$gradle_path" ]]; then
        # Update versionName
        sed -i '' "s/versionName \"[^\"]*\"/versionName \"$version\"/" "$gradle_path"
        # Update versionCode
        sed -i '' "s/versionCode [0-9]*/versionCode $code/" "$gradle_path"
        log_info "Updated Android version to $version ($code)"
    else
        log_warn "Android build.gradle not found at $gradle_path"
    fi
}

# Main script
main() {
    log_info "Bumping version ($BUMP_TYPE)"

    # Get current versions
    local ios_version=$(get_ios_version)
    local ios_build=$(get_ios_build)
    local android_version=$(get_android_version)
    local android_code=$(get_android_version_code)

    log_info "Current iOS version: $ios_version ($ios_build)"
    log_info "Current Android version: $android_version ($android_code)"

    # Calculate new version (use iOS as source of truth)
    local new_version=$(bump_version "$ios_version" "$BUMP_TYPE")
    local new_build=$((ios_build + 1))
    local new_code=$((android_code + 1))

    log_info "New version: $new_version"
    log_info "New iOS build: $new_build"
    log_info "New Android code: $new_code"

    # Update versions
    if [[ -d "$IOS_DIR" ]]; then
        update_ios_version "$new_version" "$new_build"
    fi

    if [[ -d "$ANDROID_DIR" ]]; then
        update_android_version "$new_version" "$new_code"
    fi

    # Commit changes if requested
    if [[ "$COMMIT_CHANGES" == true ]]; then
        log_info "Committing version bump..."

        git add -A
        git commit -m "Bump version to $new_version

- iOS build: $new_build
- Android code: $new_code"

        log_info "Changes committed"
    fi

    echo ""
    log_info "Version bump complete!"
    echo "  Version: $new_version"
    echo "  iOS Build: $new_build"
    echo "  Android Code: $new_code"
}

main
