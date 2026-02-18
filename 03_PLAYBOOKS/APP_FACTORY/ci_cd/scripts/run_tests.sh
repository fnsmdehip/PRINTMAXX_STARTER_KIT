#!/bin/bash
# run_tests.sh - Run tests for iOS, Android, or shared code
# Usage: ./run_tests.sh [ios|android|shared|all] [--coverage] [--ci]

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
ANDROID_DIR="$ROOT_DIR/android"
SHARED_DIR="$ROOT_DIR/src"

# Default values
PLATFORM="${1:-all}"
COVERAGE=false
CI_MODE=false
FAILED_TESTS=()

# Parse arguments
for arg in "${@:2}"; do
    case $arg in
        --coverage)
            COVERAGE=true
            ;;
        --ci)
            CI_MODE=true
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

log_step() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Run iOS tests
run_ios_tests() {
    if [[ ! -d "$IOS_DIR" ]]; then
        log_warn "iOS directory not found, skipping iOS tests"
        return 0
    fi

    log_step "Running iOS Tests"

    cd "$IOS_DIR"

    # Install dependencies
    if [[ -f "Podfile" ]]; then
        log_info "Installing CocoaPods..."
        pod install --silent
    fi

    local SCHEME="${SCHEME:-App}"
    local WORKSPACE="${WORKSPACE:-App.xcworkspace}"
    local PROJECT="${PROJECT:-App.xcodeproj}"
    local DESTINATION="platform=iOS Simulator,name=iPhone 15,OS=latest"

    # Determine workspace or project
    local BUILD_TARGET
    if [[ -f "$WORKSPACE" ]]; then
        BUILD_TARGET="-workspace $WORKSPACE"
    else
        BUILD_TARGET="-project $PROJECT"
    fi

    # Build test command
    local TEST_CMD="xcodebuild test $BUILD_TARGET -scheme $SCHEME -destination '$DESTINATION' CODE_SIGNING_ALLOWED=NO"

    # Add coverage if requested
    if [[ "$COVERAGE" == true ]]; then
        TEST_CMD="$TEST_CMD -enableCodeCoverage YES"
    fi

    # Run tests
    if eval "$TEST_CMD" 2>&1 | xcpretty --color; then
        log_info "iOS tests passed"
    else
        log_error "iOS tests failed"
        FAILED_TESTS+=("iOS")
        return 1
    fi
}

# Run Android tests
run_android_tests() {
    if [[ ! -d "$ANDROID_DIR" ]]; then
        log_warn "Android directory not found, skipping Android tests"
        return 0
    fi

    log_step "Running Android Tests"

    cd "$ANDROID_DIR"

    # Make gradlew executable
    chmod +x gradlew

    # Build test command
    local TEST_CMD="./gradlew testDebugUnitTest --no-daemon"

    # Add coverage if requested
    if [[ "$COVERAGE" == true ]]; then
        TEST_CMD="./gradlew testDebugUnitTest jacocoTestReport --no-daemon"
    fi

    # Run tests
    if eval "$TEST_CMD"; then
        log_info "Android tests passed"
    else
        log_error "Android tests failed"
        FAILED_TESTS+=("Android")
        return 1
    fi

    # Print coverage report location
    if [[ "$COVERAGE" == true ]] && [[ -d "app/build/reports/jacoco" ]]; then
        log_info "Coverage report: app/build/reports/jacoco/testDebugUnitTest/html/index.html"
    fi
}

# Run shared/JavaScript tests
run_shared_tests() {
    if [[ ! -d "$SHARED_DIR" ]] && [[ ! -f "$ROOT_DIR/package.json" ]]; then
        log_warn "Shared directory not found, skipping shared tests"
        return 0
    fi

    log_step "Running Shared Code Tests"

    cd "$ROOT_DIR"

    # Check for package.json
    if [[ ! -f "package.json" ]]; then
        log_warn "No package.json found, skipping shared tests"
        return 0
    fi

    # Install dependencies
    log_info "Installing npm dependencies..."
    npm ci --silent

    # Build test command
    local TEST_CMD="npm test"

    # Add CI and coverage flags
    if [[ "$CI_MODE" == true ]]; then
        TEST_CMD="npm test -- --ci"
    fi

    if [[ "$COVERAGE" == true ]]; then
        TEST_CMD="npm test -- --coverage"
    fi

    if [[ "$CI_MODE" == true ]] && [[ "$COVERAGE" == true ]]; then
        TEST_CMD="npm test -- --ci --coverage"
    fi

    # Run tests
    if eval "$TEST_CMD"; then
        log_info "Shared tests passed"
    else
        log_error "Shared tests failed"
        FAILED_TESTS+=("Shared")
        return 1
    fi

    # Print coverage report location
    if [[ "$COVERAGE" == true ]] && [[ -d "coverage" ]]; then
        log_info "Coverage report: coverage/lcov-report/index.html"
    fi
}

# Run lint checks
run_lint() {
    log_step "Running Lint Checks"

    local lint_failed=false

    # iOS lint (SwiftLint)
    if [[ -d "$IOS_DIR" ]] && command -v swiftlint &> /dev/null; then
        log_info "Running SwiftLint..."
        cd "$IOS_DIR"
        if ! swiftlint lint --quiet; then
            log_warn "SwiftLint found issues"
            lint_failed=true
        fi
    fi

    # Android lint
    if [[ -d "$ANDROID_DIR" ]]; then
        log_info "Running Android Lint..."
        cd "$ANDROID_DIR"
        if ! ./gradlew lintDebug --no-daemon -q; then
            log_warn "Android Lint found issues"
            lint_failed=true
        fi
    fi

    # TypeScript/JavaScript lint
    if [[ -f "$ROOT_DIR/package.json" ]]; then
        log_info "Running ESLint..."
        cd "$ROOT_DIR"
        if ! npm run lint --silent 2>/dev/null; then
            log_warn "ESLint found issues"
            lint_failed=true
        fi
    fi

    if [[ "$lint_failed" == true ]]; then
        log_warn "Some lint checks failed"
    else
        log_info "All lint checks passed"
    fi
}

# Print summary
print_summary() {
    echo ""
    log_step "Test Summary"

    if [[ ${#FAILED_TESTS[@]} -eq 0 ]]; then
        echo -e "${GREEN}All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}Failed tests:${NC}"
        for test in "${FAILED_TESTS[@]}"; do
            echo -e "  - $test"
        done
        return 1
    fi
}

# Main execution
main() {
    log_info "Running tests for: $PLATFORM"
    [[ "$COVERAGE" == true ]] && log_info "Coverage: enabled"
    [[ "$CI_MODE" == true ]] && log_info "CI mode: enabled"

    case $PLATFORM in
        ios)
            run_ios_tests
            ;;
        android)
            run_android_tests
            ;;
        shared)
            run_shared_tests
            ;;
        lint)
            run_lint
            ;;
        all)
            run_lint || true
            run_shared_tests || true
            run_ios_tests || true
            run_android_tests || true
            ;;
        *)
            log_error "Unknown platform: $PLATFORM"
            echo "Usage: $0 [ios|android|shared|lint|all] [--coverage] [--ci]"
            exit 1
            ;;
    esac

    print_summary
}

main
