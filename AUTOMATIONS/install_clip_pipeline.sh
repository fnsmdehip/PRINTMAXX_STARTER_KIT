#!/bin/bash
# Installation script for Automated Clip Pipeline
# Run: ./install_clip_pipeline.sh

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "  Automated Clip Pipeline - Installation"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install status
install_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

echo "Checking dependencies..."
echo ""

# Check Python
if command_exists python3; then
    echo -e "${GREEN}✓${NC} Python 3 installed"
    python3 --version
else
    echo -e "${RED}✗${NC} Python 3 not found"
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# Check pip
if command_exists pip3; then
    echo -e "${GREEN}✓${NC} pip3 installed"
else
    echo -e "${RED}✗${NC} pip3 not found"
    echo "   Install with: python3 -m ensurepip"
    exit 1
fi

echo ""

# Check yt-dlp
if command_exists yt-dlp; then
    echo -e "${GREEN}✓${NC} yt-dlp installed"
    yt-dlp --version | head -n 1
else
    echo -e "${YELLOW}→${NC} Installing yt-dlp..."
    pip3 install yt-dlp
    install_status "yt-dlp installed"
fi

echo ""

# Check ffmpeg
if command_exists ffmpeg; then
    echo -e "${GREEN}✓${NC} ffmpeg installed"
    ffmpeg -version | head -n 1
else
    echo -e "${YELLOW}!${NC} ffmpeg not installed"
    echo ""
    echo "   Install ffmpeg:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   → macOS: brew install ffmpeg"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "   → Ubuntu/Debian: sudo apt-get install ffmpeg"
        echo "   → CentOS/RHEL: sudo yum install ffmpeg"
    fi
    echo ""
    read -p "   Install now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if command_exists brew; then
                brew install ffmpeg
                install_status "ffmpeg installed"
            else
                echo -e "${RED}✗${NC} Homebrew not found. Install from: https://brew.sh"
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
            install_status "ffmpeg installed"
        fi
    else
        echo -e "${YELLOW}!${NC} Skipping ffmpeg (pipeline will not work without it)"
    fi
fi

echo ""

# Check Whisper
if python3 -c "import whisper" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} OpenAI Whisper installed"
else
    echo -e "${YELLOW}→${NC} Installing OpenAI Whisper..."
    pip3 install openai-whisper
    install_status "OpenAI Whisper installed"
fi

echo ""

# Check Anthropic
if python3 -c "import anthropic" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Anthropic SDK installed"
else
    echo -e "${YELLOW}→${NC} Installing Anthropic SDK..."
    pip3 install anthropic
    install_status "Anthropic SDK installed"
fi

echo ""

# Check API key
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} ANTHROPIC_API_KEY environment variable set"
else
    echo -e "${YELLOW}!${NC} ANTHROPIC_API_KEY not set"
    echo ""
    echo "   Get your API key from: https://console.anthropic.com/"
    echo ""
    read -p "   Enter API key (or press Enter to skip): " api_key
    if [ -n "$api_key" ]; then
        echo ""
        echo "   Add to your shell profile:"
        echo "   → ~/.zshrc (macOS default)"
        echo "   → ~/.bashrc (Linux default)"
        echo ""
        echo "   export ANTHROPIC_API_KEY=\"$api_key\""
        echo ""

        # Detect shell
        if [ -n "$ZSH_VERSION" ]; then
            profile="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            profile="$HOME/.bashrc"
        else
            profile="$HOME/.profile"
        fi

        read -p "   Add to $profile now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "" >> "$profile"
            echo "# Anthropic API key for clip pipeline" >> "$profile"
            echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> "$profile"
            echo -e "${GREEN}✓${NC} Added to $profile (restart shell or run: source $profile)"
        fi
    else
        echo "   → You can also pass API key with: --api-key flag"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Installation Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""

# Run test
echo "Running demo test..."
echo ""
python3 auto_clip_pipeline.py --demo

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Next Steps"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "1. Test with a real video:"
echo "   python3 auto_clip_pipeline.py --url \"https://youtube.com/watch?v=xxx\""
echo ""
echo "2. Batch process:"
echo "   python3 auto_clip_pipeline.py --urls-file example_urls.txt"
echo ""
echo "3. Generate posting schedule:"
echo "   python3 clip_post_scheduler.py --input clips/clips_metadata.csv"
echo ""
echo "4. Read docs:"
echo "   • CLIP_PIPELINE_QUICKSTART.md"
echo "   • AUTO_CLIP_PIPELINE_README.md"
echo ""
echo "════════════════════════════════════════════════════════════"
