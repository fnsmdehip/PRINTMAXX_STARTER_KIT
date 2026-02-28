# Local Video Generation Setup Guide — Mac M1 Max 64GB

**Hardware:** MacBook Pro M1 Max, 64GB unified memory, 24-core GPU
**Last Updated:** 2026-02-27

---

## TL;DR: What Actually Works on Mac Right Now

| Model | Quality | Speed | RAM Needed | Mac Status | Recommended |
|-------|---------|-------|-----------|------------|-------------|
| **Wan2.1 T2V-1.3B** | Good (480p) | ~5 min/2s clip | 8-16GB | WORKS via ComfyUI GGUF | YES — best effort:quality ratio |
| **Wan2.1 T2V-14B** | Excellent | ~30-60 min/5s | 32-48GB | WORKS via GGUF (slow) | YES if quality matters |
| **LTX-Video 2** | Very Good (4K) | ~15 min/video | 42GB model | WORKS via MLX native app | YES — native Mac app exists |
| **HunyuanVideo** | Excellent | ~24h/video | 90GB+ swap | BARELY — way too slow | NO |
| **CogVideoX** | Good | 20x slower than CUDA | 16-24GB | MPS FALLBACK only | NO — too slow |
| **Stable Video Diffusion** | Decent | Variable | 8-16GB | ComfyUI support | MAYBE — older model |
| **Open-Sora** | Moderate | Untested | Unknown | No Mac port | NO |

**Bottom line:** Use Wan2.1 1.3B for fast iteration, Wan2.1 14B for hero shots, LTX-2 native app for highest quality. Everything else is too slow on Mac.

---

## 1. ComfyUI Setup (Primary Interface)

ComfyUI is the recommended interface for running video gen models on Mac. It handles model management, workflow building, and rendering.

### Install ComfyUI Desktop (Easiest)

```bash
# Download from https://www.comfy.org/download
# Select macOS Apple Silicon version
# Install and launch — it handles Python/PyTorch setup
```

### Manual Install (More Control)

```bash
# Install pyenv for Python version management
brew install pyenv
pyenv install 3.10.5
pyenv local 3.10.5

# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Create venv
python -m venv venv
source venv/bin/activate

# Install PyTorch with MPS support
# IMPORTANT: Use PyTorch 2.4.1 for video models (2.5+ has noise issues)
pip install torch==2.4.1 torchvision==0.19.1 --index-url https://download.pytorch.org/whl/cpu

# Install ComfyUI requirements
pip install -r requirements.txt

# Launch
python main.py --force-fp16
```

### Critical Mac-Specific Settings

```bash
# Add to your .zshrc or run before launching
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
```

The `MPS_HIGH_WATERMARK_RATIO=0.0` prevents Metal from reserving too much VRAM and lets the unified memory be used more efficiently.

---

## 2. Wan2.1 Setup (Recommended Primary Model)

### Why Wan2.1

- Alibaba's open-source video gen model (Apache 2.0 license)
- 1.3B variant runs fast on Mac (8GB VRAM)
- 14B variant produces near-Sora quality
- Strong ComfyUI integration (native nodes since Feb 2025)
- Active community with Mac-specific forks

### Install Wan2.1 1.3B (Fast Mode)

```bash
# In ComfyUI, install the GGUF loader node
# ComfyUI Manager > Install Missing Custom Nodes > search "gguf"

# Download 1.3B GGUF model (~2.5GB)
cd ComfyUI/models/diffusion_models/
wget https://huggingface.co/city96/Wan2.1-T2V-1.3B-gguf/resolve/main/wan2.1-t2v-1.3b-Q8_0.gguf

# Download required T5 encoder and VAE
cd ../text_encoders/
wget https://huggingface.co/comfyanonymous/wan_2.1_comfyui/resolve/main/umt5_xxl_encoder_fp8_e4m3fn.safetensors

cd ../vae/
wget https://huggingface.co/comfyanonymous/wan_2.1_comfyui/resolve/main/wan_2.1_vae.safetensors
```

### Install Wan2.1 14B (Quality Mode)

```bash
# Download 14B GGUF model (~14-28GB depending on quantization)
cd ComfyUI/models/diffusion_models/
wget https://huggingface.co/city96/Wan2.1-T2V-14B-gguf/resolve/main/wan2.1-t2v-14b-Q4_K_S.gguf
# Q4_K_S is ~8GB, Q8_0 is ~15GB — use Q4 for speed, Q8 for quality
```

### Mac-Specific Fork (Alternative)

```bash
# Fork with MPS optimizations
git clone https://github.com/R3D347HR4Y/Wan2.1-Mac.git
cd Wan2.1-Mac
pip install -r requirements.txt

# Run with MPS backend
python generate.py --prompt "your prompt" --device mps
```

### Expected Performance (M1 Max 64GB)

| Model | Resolution | Length | Time | Quality |
|-------|-----------|--------|------|---------|
| 1.3B Q8 | 480x848 | 2s | ~3-5 min | Good for shorts/B-roll |
| 1.3B Q8 | 480x848 | 5s | ~8-12 min | Good |
| 14B Q4 | 480x848 | 2s | ~15-25 min | Excellent |
| 14B Q4 | 720x1280 | 5s | ~45-90 min | Near-Sora quality |

---

## 3. LTX-Video 2 Setup (Alternative — Native Mac App)

### Native macOS App (Easiest Option)

```bash
# Download from: https://james-see.github.io/ltx-video-mac/
# Or clone and build:
git clone https://github.com/james-see/ltx-video-mac.git
cd ltx-video-mac
# Open in Xcode and build

# First run downloads ~42GB model from HuggingFace (15-30 min)
```

### LTX-2 via ComfyUI

```bash
# Install LTX-Video custom nodes
cd ComfyUI/custom_nodes/
git clone https://github.com/Lightricks/ComfyUI-LTXVideo.git
pip install -r ComfyUI-LTXVideo/requirements.txt

# Download model
cd ../models/checkpoints/
# Get from https://huggingface.co/Lightricks/LTX-Video
```

### LTX-2 Key Features
- Native 4K resolution output
- Synchronized audio+video generation
- Open weights (fully open-source as of Jan 2026)
- MLX optimization for Apple Silicon

---

## 4. Text-to-Speech (TTS) for Narration

### Tier List for YouTube Narration

| Model | Quality | Speed | Voice Clone | Mac Native | License |
|-------|---------|-------|------------|------------|---------|
| **Qwen3-TTS** | Excellent | Fast (MLX) | YES (3s clip) | YES (MLX) | Open |
| **Orpheus TTS** | Excellent | Real-time | YES | PARTIAL (MPS issues) | Apache 2.0 |
| **XTTS-v2** | Very Good | Moderate | YES (6s clip) | YES | Non-commercial |
| **Bark** | Good | 2x slower | NO | YES | MIT |
| **Piper** | Good | Very Fast | NO | YES (ONNX) | MIT |
| **StyleTTS 2** | Very Good | Fast | NO | YES | MIT |

### Recommended: Qwen3-TTS (Best Quality + Mac Native)

```bash
# Clone the Mac-optimized version
git clone https://github.com/kapi2800/qwen3-tts-apple-silicon.git
cd qwen3-tts-apple-silicon

# Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install ffmpeg  # Already installed

# Run TTS
python tts.py --text "Your narration text here" --output narration.wav

# Voice cloning (needs 5-10s clean audio clip)
python tts.py --text "Your narration text here" --voice-ref reference.wav --output narration.wav
```

Features:
- Pro Model (1.7B): Best quality, voice cloning, voice design
- Lite Model (0.6B): Faster, less RAM
- 3-second voice cloning (clone any voice from 3s audio)
- Runs on MLX (Apple's ML framework) — native Metal acceleration
- Outperforms ElevenLabs in quality benchmarks

### Backup: Piper TTS (Fastest, Lowest Resource)

```bash
# Install via pip
pip install piper-tts

# Download a voice model
mkdir -p ~/piper/voices/en/
# Browse voices at: https://piper.ttstool.com
# Download .onnx and .onnx.json files

# Generate speech
echo "Your narration text" | piper --model ~/piper/voices/en/amy-medium.onnx --output narration.wav
```

Piper is extremely fast (real-time on CPU) but sounds more robotic. Good for drafts/previews, not final narration.

### Backup: Bark (Creative/Emotional)

```bash
pip install git+https://github.com/suno-ai/bark.git

python -c "
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write
preload_models()
audio = generate_audio('Your narration text here')
write('narration.wav', SAMPLE_RATE, audio)
"
```

Bark can generate laughter, sighs, music, sound effects in addition to speech. Useful for more creative/emotional narration.

---

## 5. Video Editing Automation

### Already Installed

- `ffmpeg` (brew) — core video processing
- `ffmpeg-python` (pip) — Python wrapper
- `opencv-python` (pip) — frame manipulation
- `openai-whisper` (pip) — transcription
- `yt-dlp` (pip) — video downloading
- `pillow` (pip) — image processing
- `torch` + `torchvision` (pip) — ML inference

### Additional Recommended

```bash
# MoviePy for high-level video editing
pip install moviepy

# Subtitle handling
pip install pysrt srt

# Audio processing
pip install pydub soundfile librosa

# Image generation for thumbnails
pip install diffusers transformers accelerate
```

### FFmpeg Quick Reference for YouTube Factory

```bash
# Concatenate video clips with crossfade
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v]; \
   [0:a][1:a]acrossfade=d=0.5[a]" \
  -map "[v]" -map "[a]" output.mp4

# Add narration over video (mix audio)
ffmpeg -i video.mp4 -i narration.wav \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3[a]" \
  -map 0:v -map "[a]" -c:v copy output.mp4

# Add text overlay (title card)
ffmpeg -i video.mp4 -vf \
  "drawtext=text='YOUR TITLE':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,3)'" \
  output.mp4

# Create vertical short from horizontal (center crop + zoom)
ffmpeg -i horizontal.mp4 -vf \
  "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920" \
  -c:a copy short.mp4

# Add background music (lower volume)
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" output.mp4

# Burn subtitles from SRT
ffmpeg -i video.mp4 -vf \
  "subtitles=subs.srt:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2'" \
  output.mp4
```

---

## 6. Recommended Pipeline Architecture

```
Script (Claude API)
    |
    v
TTS Narration (Qwen3-TTS via MLX)
    |
    v
Video Generation (Wan2.1 1.3B via ComfyUI)
    |     \
    |      > B-roll clips (5-10 per video)
    |     /
    v
Stock Footage / Screen Recording (supplementary)
    |
    v
FFmpeg Assembly (concatenate, overlay, transitions)
    |
    v
Whisper Transcription -> SRT Subtitles
    |
    v
Final Render (ffmpeg: narration + video + music + subs)
    |
    +--> Long-form (8-15 min YouTube)
    +--> Shorts (15-60s clips, vertical crop)
```

### Generation Time Budget (M1 Max 64GB, per 10-min video)

| Step | Time | Notes |
|------|------|-------|
| Script generation | 1-2 min | Claude API |
| TTS narration (10 min audio) | 3-5 min | Qwen3-TTS MLX |
| Video gen (20 x 5s clips) | 60-100 min | Wan2.1 1.3B |
| Stock footage download | 2-5 min | Pexels/Pixabay API |
| Assembly + render | 5-10 min | FFmpeg |
| Subtitle burn-in | 2-3 min | Whisper + FFmpeg |
| **Total per video** | **~90-120 min** | With 1.3B model |
| **Total per video (14B)** | **~8-12 hours** | Higher quality |

---

## 7. Free Stock Footage Sources

| Source | API | License | Best For |
|--------|-----|---------|----------|
| **Pexels** | YES (free) | Free commercial | Nature, people, abstract |
| **Pixabay** | YES (free) | CC0 | General B-roll |
| **Coverr** | NO | Free commercial | Lifestyle, urban |
| **Mixkit** | NO | Free commercial | Transitions, backgrounds |
| **Archive.org** | YES | Various | Historical, documentary |

```bash
# Pexels API example
pip install pexelsapi
# API key: free at pexels.com/api
```

---

## 8. Background Music Sources (Royalty-Free)

| Source | Cost | License | Notes |
|--------|------|---------|-------|
| **YouTube Audio Library** | Free | Free for YouTube | Best selection |
| **Pixabay Music** | Free | CC0 | Download directly |
| **Free Music Archive** | Free | CC | Check specific license |
| **Uppbeat** | Free tier | Free w/ credit | 10 downloads/mo |
| **Epidemic Sound** | $15/mo | Full commercial | Best quality |

---

## 9. Quick Start Commands

```bash
# 1. Install ComfyUI Desktop
# Download from https://www.comfy.org/download

# 2. Install Qwen3-TTS
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
git clone https://github.com/kapi2800/qwen3-tts-apple-silicon.git tools/qwen3-tts
cd tools/qwen3-tts && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 3. Install MoviePy
pip3 install moviepy pydub srt

# 4. Test the full pipeline
python3 AUTOMATIONS/youtube_factory.py --test
```

---

## 10. Troubleshooting

### "MPS backend not available"
```bash
# Ensure PyTorch is installed with MPS support
python3 -c "import torch; print(torch.backends.mps.is_available())"
# Should print True
# If False, reinstall PyTorch: pip install torch torchvision
```

### ComfyUI crashes on video gen
```bash
# Reduce resolution: use 480x848 instead of 720x1280
# Use GGUF Q4 quantization instead of Q8
# Set: export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
```

### Wan2.1 noise/artifacts
```bash
# Pin PyTorch to 2.4.1 (2.5+ has noise issues on Mac)
pip install torch==2.4.1 torchvision==0.19.1
```

### TTS sounds robotic
```bash
# Use Qwen3-TTS Pro model (1.7B) instead of Lite (0.6B)
# Provide a voice reference clip for voice cloning
# Ensure clean audio: no background noise, 5-10s clip
```
