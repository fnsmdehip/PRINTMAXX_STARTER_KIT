#!/usr/bin/env python3
"""Set PRINTMAXX node role (control|worker)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ROLE_JSON = BASE_DIR / "OPS" / "NODE_ROLE.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    parser = argparse.ArgumentParser(description="Set PRINTMAXX node role")
    parser.add_argument("role", choices=["control", "worker"], help="Node role to set")
    args = parser.parse_args()

    ROLE_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "role": args.role,
        "updated_at": now_iso(),
        "notes": "Set via scripts/set_node_role.py",
    }
    with open(ROLE_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(f"role_set={args.role} path={ROLE_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
