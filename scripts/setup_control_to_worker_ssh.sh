#!/bin/bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <user@worker-host> <worker_project_path>" >&2
  echo "example: $0 macbookpro@192.168.1.44 /Users/macbookpro/PRINTMAXX_STARTER_KITttttt" >&2
  exit 1
fi

DEST_HOST="$1"
DEST_PATH="${2%/}"
KEY_PATH="$HOME/.ssh/printmaxx_worker_ed25519"
SSH_CONFIG="$HOME/.ssh/config"
HOST_ALIAS="printmaxx-worker"

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

if [[ ! -f "$KEY_PATH" ]]; then
  ssh-keygen -t ed25519 -f "$KEY_PATH" -N "" -C "printmaxx-control->worker"
fi

PUBKEY="$(cat "$KEY_PATH.pub")"
ssh "$DEST_HOST" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && grep -qxF '$PUBKEY' ~/.ssh/authorized_keys || echo '$PUBKEY' >> ~/.ssh/authorized_keys"

if [[ ! -f "$SSH_CONFIG" ]] || ! grep -q "Host $HOST_ALIAS" "$SSH_CONFIG"; then
  cat >> "$SSH_CONFIG" <<EOF

Host $HOST_ALIAS
  HostName ${DEST_HOST#*@}
  User ${DEST_HOST%@*}
  IdentityFile $KEY_PATH
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 4
EOF
  chmod 600 "$SSH_CONFIG"
fi

if [[ -z "$DEST_PATH" || "$DEST_PATH" == "/" || "$DEST_PATH" == "/Users" || "$DEST_PATH" == "/Users/" ]]; then
  echo "refusing_unsafe_dest_path=$DEST_PATH" >&2
  exit 2
fi
if [[ "$DEST_PATH" != *"PRINTMAXX"* ]]; then
  echo "refusing_dest_path_missing_PRINTMAXX_marker=$DEST_PATH" >&2
  exit 2
fi

cat <<EOF
ssh_link_ready=1 alias=$HOST_ALIAS

next_steps:
  1) sync repo to worker:
     bash scripts/sync_to_worker.sh $HOST_ALIAS $DEST_PATH

  2) run worker prep (official openclaw + worker role):
     ssh $HOST_ALIAS "cd $DEST_PATH && bash scripts/setup_openclaw_worker_stack.sh"

  3) finish onboarding interactively on worker:
     ssh -t $HOST_ALIAS "cd $DEST_PATH && bash scripts/setup_openclaw_worker_stack.sh --run-onboard"

  4) open a tunnel for remote control from this machine:
     ssh -N -L 18789:127.0.0.1:18789 $HOST_ALIAS
EOF
