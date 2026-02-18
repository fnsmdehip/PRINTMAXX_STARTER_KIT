#!/bin/bash
# PRINTMAXX QUANT TERMINAL LAUNCHER
# =================================
# Institutional-grade solopreneurship dashboard
# Inspired by Jane Street, Two Sigma, RenTech, Bloomberg

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# Check for required packages
python3 -c "import textual, rich" 2>/dev/null || {
    echo "Installing required packages..."
    pip3 install textual rich
}

# Launch options
case "${1:-full}" in
    summary|--summary|-s)
        python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary
        ;;
    export|--export|-e)
        python3 AUTOMATIONS/printmaxx_quant_terminal.py --export
        ;;
    full|--full|-f|*)
        echo "═══════════════════════════════════════════════════════════════"
        echo "           PRINTMAXX QUANT TERMINAL"
        echo "   Institutional-Grade Solopreneurship Dashboard"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        echo "Launching Bloomberg-style TUI..."
        echo "Press 'q' to quit, 'r' to refresh, 'e' to export report"
        echo ""
        python3 AUTOMATIONS/printmaxx_quant_terminal.py
        ;;
esac
