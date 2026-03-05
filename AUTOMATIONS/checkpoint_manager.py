#!/usr/bin/env python3
"""
PRINTMAXX Checkpoint Manager
==============================
Human-in-the-loop approval system for autonomous operations.

Only 4 things need human approval:
  1. PURCHASE  — spending money (>$50)
  2. PUBLISH   — going live on a platform (first time)
  3. ACCOUNT   — creating accounts (needs credentials)
  4. STRATEGY  — kill/pivot decisions

Everything else runs autonomously.

Usage:
  python3 checkpoint_manager.py --status          # Show all pending
  python3 checkpoint_manager.py --create TYPE DESC # Create checkpoint
  python3 checkpoint_manager.py --approve FILE     # Approve a checkpoint
  python3 checkpoint_manager.py --reject FILE      # Reject a checkpoint
  python3 checkpoint_manager.py --summary          # Generate human-readable summary
  python3 checkpoint_manager.py --clean            # Archive old resolved items
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OPS = BASE / "OPS"
CKPT = OPS / "checkpoints"
PENDING = CKPT / "pending"
APPROVED = CKPT / "approved"
REJECTED = CKPT / "rejected"
DONE = CKPT / "done"
HISTORY = CKPT / "history.jsonl"

for d in [PENDING, APPROVED, REJECTED, DONE]:
    d.mkdir(parents=True, exist_ok=True)

VALID_TYPES = ["PURCHASE", "PUBLISH", "ACCOUNT", "STRATEGY", "KILL"]


def create_checkpoint(cp_type, description, details="", recommended_action=""):
    """Create a new checkpoint for human review."""
    cp_type = cp_type.upper()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = description.lower().replace(" ", "_")[:40]
    filename = f"{cp_type}_{slug}_{ts}.md"
    path = PENDING / filename

    content = f"""# Checkpoint: {cp_type}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Type:** {cp_type}
**Description:** {description}

## Details
{details if details else 'No additional details.'}

## Recommended Action
{recommended_action if recommended_action else 'Review and decide.'}

---
**To approve:** `python3 AUTOMATIONS/checkpoint_manager.py --approve {filename}`
**To reject:** `python3 AUTOMATIONS/checkpoint_manager.py --reject {filename}`
**Or:** Move this file to `OPS/checkpoints/approved/` or `OPS/checkpoints/rejected/`
"""
    path.write_text(content, encoding="utf-8")
    log_event("CREATED", filename, cp_type, description)
    print(f"[CHECKPOINT] Created: {path}")
    return path


def approve_checkpoint(filename):
    """Approve a pending checkpoint."""
    src = PENDING / filename
    if not src.exists():
        print(f"[CHECKPOINT] Not found: {src}")
        return False

    dst = APPROVED / filename
    shutil.move(str(src), str(dst))
    log_event("APPROVED", filename)
    print(f"[CHECKPOINT] Approved: {filename}")
    return True


def reject_checkpoint(filename, reason=""):
    """Reject a pending checkpoint."""
    src = PENDING / filename
    if not src.exists():
        print(f"[CHECKPOINT] Not found: {src}")
        return False

    # Append rejection reason
    if reason:
        content = src.read_text() + f"\n\n## Rejection Reason\n{reason}\n"
        src.write_text(content)

    dst = REJECTED / filename
    shutil.move(str(src), str(dst))
    log_event("REJECTED", filename, reason=reason)
    print(f"[CHECKPOINT] Rejected: {filename}")
    return True


def log_event(action, filename, cp_type="", description="", reason=""):
    """Append to history log."""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "action": action,
        "file": filename,
        "type": cp_type,
        "description": description,
        "reason": reason,
    }
    try:
        with open(HISTORY, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def show_status():
    """Show all pending checkpoints."""
    pending = sorted(PENDING.glob("*.md"))
    approved = sorted(APPROVED.glob("*.md"))
    rejected = sorted(REJECTED.glob("*.md"))

    print("=" * 60)
    print(f"CHECKPOINT STATUS — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    if pending:
        print(f"\nPENDING ({len(pending)}):")
        for p in pending:
            # Extract type from filename
            parts = p.stem.split("_")
            cp_type = parts[0] if parts else "?"
            print(f"  [{cp_type}] {p.name}")
    else:
        print("\nNo pending checkpoints. All clear.")

    if approved:
        print(f"\nAPPROVED (unprocessed: {len(approved)}):")
        for a in approved[:5]:
            print(f"  {a.name}")
        if len(approved) > 5:
            print(f"  ... and {len(approved) - 5} more")

    if rejected:
        print(f"\nREJECTED (recent: {len(rejected)}):")
        for r in rejected[:3]:
            print(f"  {r.name}")

    print()
    return pending


def generate_summary():
    """Generate human-readable summary of all pending items."""
    pending = sorted(PENDING.glob("*.md"))
    if not pending:
        print("No pending checkpoints.")
        return

    lines = [
        f"# Checkpoint Summary — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**{len(pending)} items need your review.**",
        "",
    ]

    for i, p in enumerate(pending, 1):
        content = p.read_text(encoding="utf-8", errors="replace")
        # Extract first few lines for summary
        preview = "\n".join(content.split("\n")[:6])
        lines.append(f"## {i}. {p.name}")
        lines.append(preview)
        lines.append(f"\nApprove: `python3 AUTOMATIONS/checkpoint_manager.py --approve {p.name}`")
        lines.append("")

    summary = "\n".join(lines)
    out = CKPT / "DAILY_CHECKPOINT_SUMMARY.md"
    out.write_text(summary, encoding="utf-8")
    print(f"[CHECKPOINT] Summary written: {out}")
    print(summary)


def clean_old():
    """Move processed approved items to done."""
    moved = 0
    for f in APPROVED.glob("*.md"):
        shutil.move(str(f), str(DONE / f.name))
        moved += 1
    for f in REJECTED.glob("*.md"):
        shutil.move(str(f), str(DONE / f.name))
        moved += 1
    print(f"[CHECKPOINT] Archived {moved} resolved items to done/")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PRINTMAXX Checkpoint Manager")
    p.add_argument("--status", action="store_true")
    p.add_argument("--create", nargs=2, metavar=("TYPE", "DESC"))
    p.add_argument("--approve", metavar="FILE")
    p.add_argument("--reject", metavar="FILE")
    p.add_argument("--summary", action="store_true")
    p.add_argument("--clean", action="store_true")
    args = p.parse_args()

    if args.create:
        create_checkpoint(args.create[0], args.create[1])
    elif args.approve:
        approve_checkpoint(args.approve)
    elif args.reject:
        reject_checkpoint(args.reject)
    elif args.summary:
        generate_summary()
    elif args.clean:
        clean_old()
    else:
        show_status()
