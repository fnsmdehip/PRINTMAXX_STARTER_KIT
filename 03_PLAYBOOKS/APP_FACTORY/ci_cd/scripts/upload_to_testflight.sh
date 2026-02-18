#!/bin/bash
# upload_to_testflight.sh - Build and upload iOS app to TestFlight
# Usage: ./upload_to_testflight.sh [--skip-tests] [--changelog "Release notes"]

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
IOS_DIR="$ROOT_DIR/ios"
BUILD_DIR="$IOS_DIR/build"

# Default values
SKIP_TESTS=false
CHANGELOG="Bug fixes and improvements"
SCHEME="${SCHEME:-App}"
WORKSPACE="${WORKSPACE:-App.xcworkspace}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
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
    if ! command -v xcodebuild &> /dev/null; then
        log_error "Xcode command line tools not installed"
    fi

    if ! command -v bundle &> /dev/null; then
        log_error "Bundler not installed. Run: gem install bundler"
    fi

    # Check for required environment variables
    if [[ -z "${APP_STORE_CONNECT_API_KEY_ID:-}" ]]; then
        log_error "APP_STORE_CONNECT_API_KEY_ID not set"
    fi

    if [[ -z "${APP_STORE_CONNECT_ISSUER_ID:-}" ]]; then
        log_error "APP_STORE_CONNECT_ISSUER_ID not set"
    fi

    if [[ -z "${APP_STORE_CONNECT_API_KEY_PATH:-}" ]] && [[ -z "${APP_STORE_CONNECT_API_KEY:-}" ]]; then
        log_error "APP_STORE_CONNECT_API_KEY_PATH or APP_STORE_CONNECT_API_KEY not set"
    fi

    log_info "Prerequisites check passed"
}

# Setup API key from environment
setup_api_key() {
    if [[ -n "${APP_STORE_CONNECT_API_KEY:-}" ]]; then
        log_info "Setting up API key from environment"
        mkdir -p ~/private_keys
        echo "$APP_STORE_CONNECT_API_KEY" | base64 --decode > ~/private_keys/AuthKey_${APP_STORE_CONNECT_API_KEY_ID}.p8
        export APP_STORE_CONNECT_API_KEY_PATH=~/private_keys/AuthKey_${APP_STORE_CONNECT_API_KEY_ID}.p8
    fi
}

# Install dependencies
install_dependencies() {
    log_step "Installing dependencies"

    cd "$IOS_DIR"

    # Install Ruby dependencies
    if [[ -f "Gemfile" ]]; then
        log_info "Installing Ruby gems..."
        bundle install --quiet
    fi

    # Install CocoaPods
    if [[ -f "Podfile" ]]; then
        log_info "Installing CocoaPods dependencies..."
        bundle exec pod install --repo-update
    fi
}

# Run tests
run_tests() {
    if [[ "$SKIP_TESTS" == true ]]; then
        log_warn "Skipping tests (--skip-tests flag)"
        return
    fi

    log_step "Running tests"

    cd "$IOS_DIR"

    xcodebuild test \
        -workspace "$WORKSPACE" \
        -scheme "$SCHEME" \
        -destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' \
        -resultBundlePath "$BUILD_DIR/TestResults.xcresult" \
        CODE_SIGNING_ALLOWED=NO \
        | xcpretty --color

    log_info "Tests passed"
}

# Sync code signing
sync_signing() {
    log_step "Syncing code signing certificates"

    cd "$IOS_DIR"

    bundle exec fastlane match appstore --readonly

    log_info "Code signing synced"
}

# Build the app
build_app() {
    log_step "Building release app"

    cd "$IOS_DIR"

    # Create build directory
    mkdir -p "$BUILD_DIR"

    bundle exec fastlane ios build_release

    # Verify IPA was created
    if [[ ! -f "$BUILD_DIR/App-Release.ipa" ]]; then
        log_error "Build failed: IPA not found"
    fi

    log_info "Build completed: $BUILD_DIR/App-Release.ipa"
}

# Upload to TestFlight
upload_testflight() {
    log_step "Uploading to TestFlight"

    cd "$IOS_DIR"

    bundle exec fastlane ios upload_testflight changelog:"$CHANGELOG"

    log_info "Upload complete!"
}

# Cleanup
cleanup() {
    log_step "Cleaning up"

    # Remove API key if we created it
    if [[ -f ~/private_keys/AuthKey_${APP_STORE_CONNECT_API_KEY_ID:-}.p8 ]]; then
        rm ~/private_keys/AuthKey_${APP_STORE_CONNECT_API_KEY_ID}.p8
        log_info "Removed temporary API key"
    fi
}

# Main execution
main() {
    log_info "Starting TestFlight upload"
    log_info "Changelog: $CHANGELOG"

    # Set trap for cleanup
    trap cleanup EXIT

    check_prerequisites
    setup_api_key
    install_dependencies
    run_tests
    sync_signing
    build_app
    upload_testflight

    echo ""
    log_info "Successfully uploaded to TestFlight!"
    echo ""
    echo "Next steps:"
    echo "  1. Check App Store Connect for build processing status"
    echo "  2. Add build to TestFlight for testing once processed"
    echo "  3. Configure test groups and external testers"
}

main
