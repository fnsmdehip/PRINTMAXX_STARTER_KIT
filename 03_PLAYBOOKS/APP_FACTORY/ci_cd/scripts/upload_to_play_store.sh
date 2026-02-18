#!/bin/bash
# upload_to_play_store.sh - Build and upload Android app to Play Store
# Usage: ./upload_to_play_store.sh [--track internal|alpha|beta|production] [--skip-tests]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
ANDROID_DIR="$ROOT_DIR/android"
BUILD_DIR="$ANDROID_DIR/app/build/outputs"

# Default values
SKIP_TESTS=false
TRACK="internal"
CHANGELOG="Bug fixes and improvements"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --track)
            TRACK="$2"
            shift 2
            ;;
        --changelog)
            CHANGELOG="$2"
            shift 2
            ;;
        *)
            shift
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
    exit 1
}

log_step() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites"

    # Check for required tools
    if ! command -v java &> /dev/null; then
        log_error "Java not installed"
    fi

    if ! command -v bundle &> /dev/null; then
        log_error "Bundler not installed. Run: gem install bundler"
    fi

    # Check for required environment variables
    if [[ -z "${ANDROID_KEYSTORE_BASE64:-}" ]] && [[ ! -f "$ANDROID_DIR/app/release-keystore.jks" ]]; then
        log_error "No keystore found. Set ANDROID_KEYSTORE_BASE64 or provide release-keystore.jks"
    fi

    if [[ -z "${KEYSTORE_PASSWORD:-}" ]]; then
        log_error "KEYSTORE_PASSWORD not set"
    fi

    if [[ -z "${KEY_ALIAS:-}" ]]; then
        log_error "KEY_ALIAS not set"
    fi

    if [[ -z "${KEY_PASSWORD:-}" ]]; then
        log_error "KEY_PASSWORD not set"
    fi

    if [[ -z "${PLAY_STORE_SERVICE_ACCOUNT_JSON:-}" ]] && [[ ! -f "$ANDROID_DIR/play-store-key.json" ]]; then
        log_error "No Play Store credentials. Set PLAY_STORE_SERVICE_ACCOUNT_JSON or provide play-store-key.json"
    fi

    log_info "Prerequisites check passed"
}

# Setup signing credentials
setup_signing() {
    log_step "Setting up signing credentials"

    cd "$ANDROID_DIR"

    # Decode keystore if provided as base64
    if [[ -n "${ANDROID_KEYSTORE_BASE64:-}" ]]; then
        log_info "Decoding keystore from environment"
        echo "$ANDROID_KEYSTORE_BASE64" | base64 --decode > app/release-keystore.jks
    fi

    # Decode Play Store credentials if provided as base64
    if [[ -n "${PLAY_STORE_SERVICE_ACCOUNT_JSON:-}" ]]; then
        log_info "Decoding Play Store credentials from environment"
        echo "$PLAY_STORE_SERVICE_ACCOUNT_JSON" | base64 --decode > play-store-key.json
    fi

    export KEYSTORE_FILE="release-keystore.jks"
    export SUPPLY_JSON_KEY="play-store-key.json"

    log_info "Signing credentials configured"
}

# Install dependencies
install_dependencies() {
    log_step "Installing dependencies"

    cd "$ANDROID_DIR"

    # Install Ruby dependencies
    if [[ -f "Gemfile" ]]; then
        log_info "Installing Ruby gems..."
        bundle install --quiet
    fi

    # Make gradlew executable
    chmod +x gradlew

    log_info "Dependencies installed"
}

# Run tests
run_tests() {
    if [[ "$SKIP_TESTS" == true ]]; then
        log_warn "Skipping tests (--skip-tests flag)"
        return
    fi

    log_step "Running tests"

    cd "$ANDROID_DIR"

    ./gradlew testReleaseUnitTest --no-daemon

    log_info "Tests passed"
}

# Build the app
build_app() {
    log_step "Building release AAB"

    cd "$ANDROID_DIR"

    bundle exec fastlane android build_release

    # Verify AAB was created
    AAB_FILE=$(find "$BUILD_DIR/bundle/release" -name "*.aab" -type f 2>/dev/null | head -1)
    if [[ -z "$AAB_FILE" ]]; then
        log_error "Build failed: AAB not found"
    fi

    log_info "Build completed: $AAB_FILE"
}

# Upload to Play Store
upload_play_store() {
    log_step "Uploading to Play Store ($TRACK track)"

    cd "$ANDROID_DIR"

    bundle exec fastlane android upload_play_store track:"$TRACK" changelog:"$CHANGELOG"

    log_info "Upload complete!"
}

# Cleanup sensitive files
cleanup() {
    log_step "Cleaning up"

    cd "$ANDROID_DIR"

    # Remove keystore if we decoded it
    if [[ -n "${ANDROID_KEYSTORE_BASE64:-}" ]] && [[ -f "app/release-keystore.jks" ]]; then
        rm -f app/release-keystore.jks
        log_info "Removed temporary keystore"
    fi

    # Remove Play Store credentials if we decoded them
    if [[ -n "${PLAY_STORE_SERVICE_ACCOUNT_JSON:-}" ]] && [[ -f "play-store-key.json" ]]; then
        rm -f play-store-key.json
        log_info "Removed temporary Play Store credentials"
    fi
}

# Get version info
get_version_info() {
    local gradle_file="$ANDROID_DIR/app/build.gradle"

    VERSION_NAME=$(grep 'versionName' "$gradle_file" | head -1 | sed 's/[^0-9.]//g')
    VERSION_CODE=$(grep 'versionCode' "$gradle_file" | head -1 | sed 's/[^0-9]//g')

    log_info "Version: $VERSION_NAME ($VERSION_CODE)"
}

# Main execution
main() {
    log_info "Starting Play Store upload"
    log_info "Track: $TRACK"
    log_info "Changelog: $CHANGELOG"

    # Set trap for cleanup
    trap cleanup EXIT

    check_prerequisites
    setup_signing
    install_dependencies
    get_version_info
    run_tests
    build_app
    upload_play_store

    echo ""
    log_info "Successfully uploaded to Play Store ($TRACK track)!"
    echo ""
    echo "Version: $VERSION_NAME ($VERSION_CODE)"
    echo ""
    echo "Next steps:"
    case $TRACK in
        internal)
            echo "  1. Go to Play Console to add internal testers"
            echo "  2. Testers will receive the update automatically"
            ;;
        alpha|beta)
            echo "  1. Go to Play Console to manage testers"
            echo "  2. Promote to production when ready"
            ;;
        production)
            echo "  1. Monitor the rollout in Play Console"
            echo "  2. Consider staged rollout for safety"
            ;;
    esac
}

main
