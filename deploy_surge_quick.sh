#!/bin/bash
# QUICK DEPLOY - Uses Surge.sh (zero auth needed)
# Run: bash deploy_surge_quick.sh

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/app_factory/output"
OUT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/OPS/DEPLOYMENT_URLS.md"

echo "# PRINTMAXX PWA Deployment URLs" > "$OUT"
echo "" >> "$OUT"
echo "| App | URL | Status |" >> "$OUT"
echo "|-----|-----|--------|" >> "$OUT"

for app in ramadan-tracker focuslock-web habitforge-web mealmaxx-web sleepmaxx-web walktounlock-web; do
    DOMAIN="${app}.surge.sh"
    echo "Deploying $app to https://$DOMAIN ..."
    cd "$BASE/$app"
    npx surge --project . --domain "$DOMAIN" 2>&1
    if [ $? -eq 0 ]; then
        echo "| $app | https://$DOMAIN | LIVE |" >> "$OUT"
        echo "SUCCESS: https://$DOMAIN"
    else
        echo "| $app | FAILED | ERROR |" >> "$OUT"
        echo "FAILED: $app"
    fi
done

echo ""
echo "Done! URLs saved to $OUT"
cat "$OUT"
open "$OUT"
