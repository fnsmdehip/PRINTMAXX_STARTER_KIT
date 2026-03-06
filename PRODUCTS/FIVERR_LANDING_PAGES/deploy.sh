#!/bin/bash
# Deploy Fiverr landing pages to surge.sh
# Each gig page gets its own subdomain
# Usage: bash deploy.sh [--all | --page <name>]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Define page-to-subdomain mappings
declare -A PAGES
PAGES=(
  ["index.html"]="printmaxx-services.surge.sh"
  ["website-design.html"]="printmaxx-website-design.surge.sh"
  ["landing-page.html"]="printmaxx-landing-page.surge.sh"
  ["cold-email.html"]="printmaxx-cold-email.surge.sh"
  ["web-scraping.html"]="printmaxx-web-scraping.surge.sh"
  ["automation.html"]="printmaxx-automation.surge.sh"
  ["seo-pages.html"]="printmaxx-seo-pages.surge.sh"
  ["content-writing.html"]="printmaxx-content-writing.surge.sh"
  ["app-development.html"]="printmaxx-app-development.surge.sh"
  ["ai-chatbot.html"]="printmaxx-ai-chatbot.surge.sh"
  ["data-analysis.html"]="printmaxx-data-analysis.surge.sh"
)

deploy_page() {
  local file="$1"
  local domain="$2"

  if [ ! -f "$file" ]; then
    echo "ERROR: $file not found"
    return 1
  fi

  # Create temp directory for single-page deploy
  local tmpdir=$(mktemp -d)
  cp "$file" "$tmpdir/index.html"

  echo "deploying $file -> $domain"
  npx surge "$tmpdir" "$domain"
  local status=$?

  rm -rf "$tmpdir"

  if [ $status -eq 0 ]; then
    echo "  deployed: https://$domain"
  else
    echo "  FAILED: $file"
  fi

  return $status
}

deploy_all() {
  echo "deploying all pages..."
  echo ""

  local success=0
  local failed=0

  for file in "${!PAGES[@]}"; do
    deploy_page "$file" "${PAGES[$file]}"
    if [ $? -eq 0 ]; then
      ((success++))
    else
      ((failed++))
    fi
    echo ""
  done

  echo "---"
  echo "done. $success deployed, $failed failed."
  echo ""
  echo "portfolio homepage: https://printmaxx-services.surge.sh"
  echo ""
  echo "all URLs:"
  for file in "${!PAGES[@]}"; do
    echo "  https://${PAGES[$file]}"
  done
}

deploy_single() {
  local name="$1"
  local file="${name}.html"

  if [ -z "${PAGES[$file]}" ]; then
    # Try with index
    if [ "$name" = "index" ] && [ -n "${PAGES[index.html]}" ]; then
      file="index.html"
    else
      echo "ERROR: unknown page '$name'"
      echo ""
      echo "available pages:"
      for f in "${!PAGES[@]}"; do
        echo "  ${f%.html}"
      done
      return 1
    fi
  fi

  deploy_page "$file" "${PAGES[$file]}"
}

# Parse arguments
case "${1:-}" in
  --all|-a|"")
    deploy_all
    ;;
  --page|-p)
    if [ -z "${2:-}" ]; then
      echo "usage: $0 --page <name>"
      echo "example: $0 --page website-design"
      exit 1
    fi
    deploy_single "$2"
    ;;
  --list|-l)
    echo "available pages and domains:"
    echo ""
    for file in "${!PAGES[@]}"; do
      printf "  %-25s -> %s\n" "${file%.html}" "${PAGES[$file]}"
    done
    ;;
  --help|-h)
    echo "usage:"
    echo "  $0              deploy all pages"
    echo "  $0 --all        deploy all pages"
    echo "  $0 --page NAME  deploy single page"
    echo "  $0 --list       list all pages and domains"
    echo ""
    echo "examples:"
    echo "  $0 --page website-design"
    echo "  $0 --page cold-email"
    echo "  $0 --page index"
    ;;
  *)
    # Assume it's a page name
    deploy_single "$1"
    ;;
esac
