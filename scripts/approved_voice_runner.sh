#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/Library/Frameworks/Python.framework/Versions/3.12/bin/python3}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3 not found" >&2
  exit 1
fi

export HF_HOME="${HF_HOME:-${ROOT}/.hf-cache}"

exec "${PYTHON_BIN}" "${ROOT}/AUTOMATIONS/approved_script_voice_runner.py" "$@"
