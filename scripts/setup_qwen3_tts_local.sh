#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${ROOT}/.venv-qwen3-tts"
UV_CACHE_DIR="${ROOT}/.uv-cache"
HF_HOME_DIR="${ROOT}/.hf-cache"
MODEL_ID="${MODEL_ID:-Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice}"
MODEL_LOCAL_DIR="${MODEL_LOCAL_DIR:-${ROOT}/models/Qwen3-TTS-12Hz-1.7B-CustomVoice}"
DOWNLOAD_MODEL="${DOWNLOAD_MODEL:-0}"
INSTALL_SOX="${INSTALL_SOX:-0}"
INSTALL_FFMPEG="${INSTALL_FFMPEG:-0}"

echo "[qwen3-tts] root=${ROOT}"
echo "[qwen3-tts] creating/updating venv: ${VENV}"
uv --cache-dir "${UV_CACHE_DIR}" venv "${VENV}"

echo "[qwen3-tts] installing python deps"
uv --cache-dir "${UV_CACHE_DIR}" pip install --python "${VENV}/bin/python" \
  qwen-tts qwen-omni-utils torchvision

if ! command -v sox >/dev/null 2>&1; then
  if [[ "${INSTALL_SOX}" == "1" ]]; then
    echo "[qwen3-tts] installing SoX via Homebrew"
    brew install sox
  else
    echo "[qwen3-tts] warning: SoX not found (optional but recommended)."
    echo "[qwen3-tts] install with: brew install sox"
  fi
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  if [[ "${INSTALL_FFMPEG}" == "1" ]]; then
    echo "[qwen3-tts] installing ffmpeg via Homebrew"
    brew install ffmpeg
  else
    echo "[qwen3-tts] warning: ffmpeg not found (needed for loudness normalization + subtitle pipeline)."
    echo "[qwen3-tts] install with: brew install ffmpeg"
  fi
fi

if [[ "${DOWNLOAD_MODEL}" == "1" ]]; then
  echo "[qwen3-tts] pre-downloading model: ${MODEL_ID}"
  MODEL_ID="${MODEL_ID}" MODEL_LOCAL_DIR="${MODEL_LOCAL_DIR}" HF_HOME="${HF_HOME_DIR}" "${VENV}/bin/python" - <<'PY'
import os
import torch
from huggingface_hub import snapshot_download
from qwen_tts import Qwen3TTSModel

model_id = os.environ.get("MODEL_ID", "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice")
model_local_dir = os.environ.get("MODEL_LOCAL_DIR", "")
if model_local_dir:
    snapshot_download(
        repo_id=model_id,
        local_dir=model_local_dir,
        local_dir_use_symlinks=False,
    )
    source = model_local_dir
else:
    source = model_id

tts = Qwen3TTSModel.from_pretrained(
    source,
    device_map="cpu",
    dtype=torch.float32,
    attn_implementation="eager",
)
speakers = tts.get_supported_speakers() or []
speaker = speakers[0] if speakers else "aiden"
tts.generate_custom_voice(
    text="Model warmup test.",
    language="English",
    speaker=speaker,
    instruct="Speak naturally.",
    max_new_tokens=256,
)
print(f"downloaded={model_id}")
if model_local_dir:
    print(f"local_model_dir={model_local_dir}")
PY
fi

echo "[qwen3-tts] setup complete"
echo "[qwen3-tts] run:"
echo "  HF_HOME=${HF_HOME_DIR} ${ROOT}/scripts/qwen3_tts_longform.sh --text 'Hello from local Qwen3-TTS'"
echo "  ${ROOT}/scripts/approved_voice_runner.sh --dry-run"
