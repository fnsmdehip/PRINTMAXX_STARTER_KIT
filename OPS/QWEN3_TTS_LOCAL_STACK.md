# Qwen3 TTS Local Stack (Apple Silicon)

## Why this matters

Use local Qwen3-TTS as a low-cost voice layer for:

1. Longform faceless YouTube narration.
2. Auto-generated clip voiceovers from one master script.
3. Multi-persona voice lanes without recurring per-minute SaaS billing.
4. Draft audio for offers, VSLs, ads, outreach follow-ups, and product demos.

## Installed stack

- Python env: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.venv-qwen3-tts`
- Model: `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- Core packages:
  - `qwen-tts`
  - `qwen-omni-utils`
  - `torch`, `torchaudio`, `torchvision`
- Verified output:
  - `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/output/qwen_tts/smoke_test.wav`

## One-time setup

```bash
bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/setup_qwen3_tts_local.sh
```

Optional model pre-download:

```bash
DOWNLOAD_MODEL=1 bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/setup_qwen3_tts_local.sh
```

Optional SoX install during setup:

```bash
INSTALL_SOX=1 bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/setup_qwen3_tts_local.sh
```

Optional ffmpeg install during setup:

```bash
INSTALL_FFMPEG=1 bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/setup_qwen3_tts_local.sh
```

## Longform render command

```bash
bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/qwen3_tts_longform.sh \
  --text-file /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/CONTENT/social/printmaxxer/PIPELINE_TWEETS_2026-02-17.md \
  --speaker aiden \
  --language English \
  --chunk-chars 650 \
  --max-new-tokens 1024 \
  --out /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/output/qwen_tts/youtube_longform.wav
```

Outputs:

- Merged narration WAV.
- Per-chunk segment WAV files in `output/qwen_tts/segments/`.
- Manifest JSON with chunk durations and paths.
- SRT subtitle file with timing (`<out>.srt`).
- ffmpeg loudness-normalized master audio (target: -16 LUFS, -1.5 dBTP).

Optional flags:

```bash
# Disable loudness normalization (if you want raw model output)
--no-normalize-loudness

# Disable subtitles
--no-srt
```

When `DOWNLOAD_MODEL=1` is used, model files are mirrored locally to:

- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/models/Qwen3-TTS-12Hz-1.7B-CustomVoice`

`qwen3_tts_longform.py` automatically prefers that local path (offline-safe).

## Approved script auto-render sidecar

Runner:

- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/approved_script_voice_runner.py`
- Wrapper: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/approved_voice_runner.sh`

Data sources:

1. QA queue (frontmatter gate): `OPS/CONTENT_QA_QUEUE/QA_*.md`
2. Manual queue CSV: `OPS/VOICEOVER_APPROVED_QUEUE.csv`

Only rows with `status=APPROVED` are rendered.

Dry run:

```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/approved_script_voice_runner.py --dry-run
```

Live run:

```bash
bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/approved_voice_runner.sh --max-jobs 2 --max-blocks-per-source 1
```

Cron:

- Live crontab marker: `PRINTMAXX_VOICE_RENDER`
- Schedule: hourly at `:20`
- Log: `AUTOMATIONS/logs/voice_render.log`
- Render ledger: `LEDGER/VOICE_RENDER_RUNS.csv`

## ElevenLabs fallback (failure-only)

Fallback runs only if local Qwen render fails.

Required env vars:

```bash
export ELEVENLABS_API_KEY="..."
export ELEVENLABS_VOICE_ID="..."
# optional
export ELEVENLABS_MODEL_ID="eleven_multilingual_v2"
```

Fallback artifacts are tagged in manifest/ledger as `elevenlabs_fallback`.

## Integration pattern (YouTube -> clips)

1. Render master narration with `qwen3_tts_longform.py`.
2. Pair each segment with B-roll or generated visuals.
3. Assemble longform cut (8-20 minutes).
4. Re-use segment WAVs to generate shorts/reels without re-rendering.
5. Push to your clip scheduler pipeline.

## Notes

- First run downloads model weights to `HF_HOME` (default: `.hf-cache` in repo if using wrapper script).
- You may see `sox` warnings; synthesis still works, but installing SoX improves certain audio utility paths.
- For maximum reliability on Apple Silicon, start with `--device-map cpu --dtype float32`.
