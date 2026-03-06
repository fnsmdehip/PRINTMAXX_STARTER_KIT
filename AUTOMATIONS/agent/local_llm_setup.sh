#!/bin/bash
# PRINTMAXX Local LLM Setup — LM Studio (primary) + Ollama (fallback)
# Hardware: M1 Max 64GB — can run 70B models at Q4
#
# LM Studio is preferred because it has a GUI for monitoring.
# Both expose an OpenAI-compatible API that the ops manager connects to.

echo "=== PRINTMAXX Local LLM Setup ==="
echo ""
echo "Your hardware: M1 Max 64GB — excellent for large models"
echo ""

# LM Studio setup
echo "=== LM STUDIO (Primary — has GUI) ==="
echo ""
echo "1. Download LM Studio from: https://lmstudio.ai"
echo "   (or open it if already installed)"
echo ""
echo "2. In LM Studio, search for and download ONE of these models:"
echo ""
echo "   BEST QUALITY (uses ~40GB RAM):"
echo "   - dolphin-3.0-llama-3.1-70b (Q4_K_M) — best overall uncensored"
echo ""
echo "   GREAT QUALITY + CREATIVE (uses ~20GB RAM):"
echo "   - eva-qwen2.5-32b (Q4_K_M) — excellent for creative/roleplay"
echo "   - nous-hermes-3-llama-3.1-70b (Q4_K_M) — strong creative writing"
echo ""
echo "   FAST + GOOD (uses ~5GB RAM):"
echo "   - dolphin-2.9.4-llama3.1-8b (Q8_0) — fast, good quality"
echo "   - hermes-3-llama-3.2-8b — quick generations"
echo ""
echo "3. Load the model in LM Studio"
echo ""
echo "4. Start the local server:"
echo "   - Click the 'Local Server' tab (left sidebar)"
echo "   - Click 'Start Server'"
echo "   - Default port: 1234"
echo "   - API endpoint: http://localhost:1234/v1/chat/completions"
echo ""
echo "5. Test it:"
echo '   curl http://localhost:1234/v1/chat/completions \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'"'"
echo ""
echo "=== INTEGRATION ==="
echo ""
echo "The PRINTMAXX ops manager (printmaxx_ops_manager.py) auto-detects:"
echo "  - LM Studio on port 1234 (checked first)"
echo "  - Ollama on port 11434 (fallback)"
echo ""
echo "Once LM Studio is running with a model loaded and server started,"
echo "the adult_content venture will automatically use it for content generation."
echo ""
echo "Claude handles business intel. Local LLM handles persona content."
echo "=== Done ==="
