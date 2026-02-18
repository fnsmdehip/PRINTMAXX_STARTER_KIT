#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${ROOT}/.venv-qwen3-tts"

if [[ ! -x "${VENV}/bin/python" ]]; then
  echo "Missing ${VENV}. Run: ${ROOT}/scripts/setup_qwen3_tts_local.sh" >&2
  exit 1
fi

export HF_HOME="${HF_HOME:-${ROOT}/.hf-cache}"
exec "${VENV}/bin/python" "${ROOT}/AUTOMATIONS/qwen3_tts_longform.py" "$@"

