#!/bin/bash
# AUTO-INSTALL ComfyUI — run with: bash ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/AI_ART_VENTURE/install_now.sh
set -e
echo "=== Installing ComfyUI ==="
cd ~/Documents
[ -d ComfyUI ] || git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip3 install torch torchvision torchaudio --break-system-packages 2>/dev/null || pip3 install torch torchvision torchaudio
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
cd custom_nodes && [ -d ComfyUI-Manager ] || git clone https://github.com/ltdrdata/ComfyUI-Manager.git && cd ..
echo "=== Generating test image via Pollinations ==="
mkdir -p ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/AI_ART_VENTURE/test_output
curl -sL --max-time 60 -o ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/AI_ART_VENTURE/test_output/test_character.png "https://image.pollinations.ai/prompt/anime+digital+art+character+portrait+elegant+fantasy+woman+detailed?width=1024&height=1024&nologo=true&seed=42"
echo "=== Test image saved ==="
echo "=== Launching ComfyUI on port 8188 ==="
python3 main.py --force-fp16
