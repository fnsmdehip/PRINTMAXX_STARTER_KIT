#!/bin/bash
# ComfyUI Setup Script for PRINTMAXX AI Art Venture
# Run this on the Mac directly: bash MONEY_METHODS/AI_ART_VENTURE/setup_comfyui.sh

set -e

echo "=== PRINTMAXX ComfyUI Setup ==="
echo "Requires: Python 3.10+, 64GB RAM, Apple Silicon recommended"
echo ""

# Check if ComfyUI already exists
if [ -d "$HOME/Documents/ComfyUI" ]; then
    echo "[OK] ComfyUI already cloned at ~/Documents/ComfyUI"
    COMFY_DIR="$HOME/Documents/ComfyUI"
elif [ -d "$HOME/ComfyUI" ]; then
    echo "[OK] ComfyUI found at ~/ComfyUI"
    COMFY_DIR="$HOME/ComfyUI"
else
    echo "[INSTALL] Cloning ComfyUI..."
    cd "$HOME/Documents"
    git clone https://github.com/comfyanonymous/ComfyUI.git
    COMFY_DIR="$HOME/Documents/ComfyUI"
    echo "[OK] ComfyUI cloned"
fi

cd "$COMFY_DIR"

# Install Python dependencies
echo ""
echo "[INSTALL] Installing PyTorch with MPS (Apple Silicon) support..."
pip3 install torch torchvision torchaudio --break-system-packages 2>/dev/null || pip3 install torch torchvision torchaudio

echo "[INSTALL] Installing ComfyUI requirements..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

# Install ComfyUI Manager
echo ""
echo "[INSTALL] Installing ComfyUI Manager..."
cd custom_nodes
if [ ! -d "ComfyUI-Manager" ]; then
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
    echo "[OK] ComfyUI Manager installed"
else
    echo "[OK] ComfyUI Manager already installed"
fi
cd ..

# Check for models
echo ""
echo "=== Model Check ==="
MODELS_DIR="$COMFY_DIR/models/checkpoints"
if ls "$MODELS_DIR"/*.safetensors 1>/dev/null 2>&1; then
    echo "[OK] Found models:"
    ls -lh "$MODELS_DIR"/*.safetensors
else
    echo "[NEEDED] No models found in $MODELS_DIR"
    echo ""
    echo "Download one of these (place in $MODELS_DIR):"
    echo "  1. PonyDiffusionV6XL (BEST for anime/art characters):"
    echo "     https://civitai.com/models/257749/pony-diffusion-v6-xl"
    echo ""
    echo "  2. AnimagineXL 3.1 (high quality anime):"
    echo "     https://civitai.com/models/260267/animagine-xl-31"
    echo ""
    echo "  3. Juggernaut XL (photorealistic):"
    echo "     https://civitai.com/models/133005/juggernaut-xl"
    echo ""
    echo "Or use ComfyUI Manager to download from the UI after launch."
fi

# Generate test image via Pollinations (quick validation)
echo ""
echo "=== Quick Test (Pollinations API) ==="
TEST_DIR="$(dirname "$0")/test_output"
mkdir -p "$TEST_DIR" 2>/dev/null || TEST_DIR="/tmp/ai_art_test"
mkdir -p "$TEST_DIR"

echo "Generating test character via Pollinations..."
curl -sL --max-time 60 -o "$TEST_DIR/test_character.png" \
    "https://image.pollinations.ai/prompt/anime+digital+art+character+portrait+elegant+fantasy+woman+detailed?width=1024&height=1024&nologo=true&seed=42"

if [ -f "$TEST_DIR/test_character.png" ] && [ -s "$TEST_DIR/test_character.png" ]; then
    echo "[OK] Test image saved to: $TEST_DIR/test_character.png"
    echo "     Size: $(du -h "$TEST_DIR/test_character.png" | cut -f1)"
    open "$TEST_DIR/test_character.png" 2>/dev/null || echo "     Open manually to view"
else
    echo "[SKIP] Pollinations timed out. Will test with ComfyUI directly."
fi

# Launch ComfyUI
echo ""
echo "=== Ready to Launch ==="
echo "Run: cd $COMFY_DIR && python3 main.py --force-fp16"
echo "Then open: http://127.0.0.1:8188"
echo ""
echo "With 64GB RAM you can:"
echo "  - Run SDXL at full quality"
echo "  - Batch generate 4-8 images simultaneously"
echo "  - Run AnimateDiff for video generation"
echo "  - Train LoRAs for consistent characters"
echo ""
read -p "Launch ComfyUI now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$COMFY_DIR"
    python3 main.py --force-fp16
fi
