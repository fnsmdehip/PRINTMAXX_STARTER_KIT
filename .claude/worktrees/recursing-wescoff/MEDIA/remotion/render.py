#!/usr/bin/env python3
"""Remotion render wrapper for PRINTMAXX agents.

Usage:
    python3 render.py --comp SocialHook --props '{"hookText":"...", "highlightWord":"...", "subtitle":"..."}'
    python3 render.py --comp QuoteCard --props '{"quote":"...", "attribution":"..."}'
    python3 render.py --comp StatsDashboard --props '{"title":"...", "subtitle":"...", "stats":[...]}'
    python3 render.py --all  # render all compositions with default props
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REMOTION_DIR = Path(__file__).parent
OUT_DIR = REMOTION_DIR / "out"
ENTRY = "src/index.ts"

COMPOSITIONS = ["SocialHook", "StatsDashboard", "QuoteCard", "PipelinePressure", "BeforeAfter", "BigNumber", "TrendStack"]


def render(comp_id: str, props: dict | None = None, output: str | None = None) -> bool:
    OUT_DIR.mkdir(exist_ok=True)

    if output is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = str(OUT_DIR / f"{comp_id}_{ts}.mp4")

    cmd = ["npx", "remotion", "render", ENTRY, comp_id, output]

    if props:
        cmd.extend(["--props", json.dumps(props)])

    print(f"Rendering {comp_id} → {output}")
    result = subprocess.run(cmd, cwd=str(REMOTION_DIR), capture_output=True, text=True, timeout=120)

    if result.returncode == 0:
        size = Path(output).stat().st_size if Path(output).exists() else 0
        print(f"  OK — {size / 1024:.0f}KB")
        return True
    else:
        print(f"  FAILED: {result.stderr[-500:]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Remotion render wrapper")
    parser.add_argument("--comp", type=str, help=f"Composition ID: {', '.join(COMPOSITIONS)}")
    parser.add_argument("--props", type=str, help="JSON props string")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--all", action="store_true", help="Render all compositions with defaults")
    args = parser.parse_args()

    if args.all:
        for comp in COMPOSITIONS:
            render(comp)
    elif args.comp:
        if args.comp not in COMPOSITIONS:
            print(f"Unknown composition: {args.comp}")
            print(f"Available: {', '.join(COMPOSITIONS)}")
            sys.exit(1)
        props = json.loads(args.props) if args.props else None
        render(args.comp, props, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
