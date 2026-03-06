#!/bin/bash
# deploy MCPHub to surge.sh
# usage: bash deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOMAIN="mcphub.surge.sh"

echo "deploying MCPHub to $DOMAIN..."

# check if surge is installed
if ! command -v surge &> /dev/null; then
  echo "surge not found. installing..."
  npm install -g surge
fi

# deploy the directory (index.html, submit.html, servers.json)
cd "$SCRIPT_DIR"
surge . "$DOMAIN"

echo ""
echo "done. live at https://$DOMAIN"
echo ""
echo "files deployed:"
echo "  - index.html (landing page)"
echo "  - submit.html (submission form)"
echo "  - servers.json (server database)"
