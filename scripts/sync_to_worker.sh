#!/bin/bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <user@worker-host> <remote_path>"
  exit 1
fi

SRC="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/"
DEST_HOST="$1"
DEST_PATH="${2%/}"

# Safety: prevent accidental remote wipes.
if [[ -z "$DEST_PATH" || "$DEST_PATH" == "/" || "$DEST_PATH" == "/Users" || "$DEST_PATH" == "/Users/" ]]; then
  echo "refusing_unsafe_dest_path=$DEST_PATH" >&2
  exit 2
fi
if [[ "$DEST_PATH" =~ ^/Users/[^/]+$ ]]; then
  echo "refusing_dest_path_is_home_dir=$DEST_PATH" >&2
  exit 2
fi
if [[ "$DEST_PATH" != *"PRINTMAXX"* ]]; then
  echo "refusing_dest_path_missing_PRINTMAXX_marker=$DEST_PATH" >&2
  exit 2
fi

rsync -az \
  --exclude ".git/" \
  --exclude "SECRETS/" \
  --exclude ".env" \
  --exclude ".env.*" \
  --exclude "output/" \
  --exclude "cal ai/" \
  --exclude ".guardrails/" \
  --exclude "logs/" \
  --exclude "__pycache__/" \
  "$SRC" "$DEST_HOST:$DEST_PATH"

echo "sync_complete host=$DEST_HOST path=$DEST_PATH"
