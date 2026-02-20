#!/usr/bin/env python3
"""
Sprint Timer — Productivity enforcement tool with alarms and reminders.

Usage:
    python3 sprint_timer.py <sprint_file.json>
    python3 sprint_timer.py --example          # print example sprint JSON

Features:
    - Countdown timer with task tracking
    - macOS notifications at configurable intervals
    - Alarm sound when deadline hits with incomplete tasks
    - Stale-task warnings if nothing completed in X minutes
    - Reusable: just swap the JSON sprint file
    - Terminal UI with color coding

Controls (while running):
    1-9     Mark task # as done
    s       Show status
    q       Quit early
"""

import json
import sys
import os
import time
import threading
import subprocess
import select
import signal
import termios
import tty
from datetime import datetime, timedelta
from pathlib import Path

# ── Colors ──────────────────────────────────────────────────────────────────

R = "\033[91m"   # red
G = "\033[92m"   # green
Y = "\033[93m"   # yellow
B = "\033[94m"   # blue
C = "\033[96m"   # cyan
W = "\033[97m"   # white
DIM = "\033[2m"  # dim
BOLD = "\033[1m" # bold
RST = "\033[0m"  # reset


# ── macOS Integration ───────────────────────────────────────────────────────

def notify(title: str, message: str, sound: str = "Ping"):
    """Send macOS notification."""
    script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
    subprocess.Popen(["osascript", "-e", script],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def alarm_sound(repeat: int = 3):
    """Play alarm sound using macOS system sounds."""
    for _ in range(repeat):
        # Try multiple sound paths
        for sound in [
            "/System/Library/Sounds/Sosumi.aiff",
            "/System/Library/Sounds/Funk.aiff",
            "/System/Library/Sounds/Glass.aiff",
            "/System/Library/Sounds/Ping.aiff",
        ]:
            if os.path.exists(sound):
                subprocess.Popen(["afplay", sound],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
        time.sleep(1.5)


def say(text: str):
    """Text-to-speech on macOS."""
    subprocess.Popen(["say", "-v", "Samantha", text],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ── Sprint Data ─────────────────────────────────────────────────────────────

class Sprint:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            data = json.load(f)

        self.name = data["sprint_name"]
        self.total_minutes = data["total_minutes"]
        self.reminder_interval = data.get("reminder_interval_minutes", 15)
        self.stale_warning_minutes = data.get("stale_warning_minutes", 20)
        self.tasks = []
        for i, t in enumerate(data["tasks"]):
            self.tasks.append({
                "id": i + 1,
                "name": t["name"],
                "platform": t.get("platform", ""),
                "time_estimate": t.get("time_estimate", ""),
                "instructions": t.get("instructions", []),
                "done": False,
                "done_at": None,
            })

        self.start_time = None
        self.end_time = None
        self.last_completion_time = None

    @property
    def completed(self):
        return [t for t in self.tasks if t["done"]]

    @property
    def remaining(self):
        return [t for t in self.tasks if not t["done"]]

    @property
    def all_done(self):
        return len(self.remaining) == 0

    def elapsed_seconds(self):
        if not self.start_time:
            return 0
        return (datetime.now() - self.start_time).total_seconds()

    def remaining_seconds(self):
        return max(0, self.total_minutes * 60 - self.elapsed_seconds())

    def mark_done(self, task_id: int) -> str:
        for t in self.tasks:
            if t["id"] == task_id:
                if t["done"]:
                    return f"Task {task_id} already done."
                t["done"] = True
                t["done_at"] = datetime.now().isoformat()
                self.last_completion_time = datetime.now()
                return f"Task {task_id} completed: {t['name']}"
        return f"No task #{task_id}"


# ── Display ─────────────────────────────────────────────────────────────────

def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m:02d}m {s:02d}s"


def clear_screen():
    print("\033[2J\033[H", end="", flush=True)


def draw_progress_bar(done: int, total: int, width: int = 40) -> str:
    filled = int(width * done / total) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * done / total) if total > 0 else 0
    return f"[{bar}] {pct}%"


def render(sprint: Sprint):
    clear_screen()
    remaining = sprint.remaining_seconds()
    elapsed = sprint.elapsed_seconds()

    if remaining < 600:
        time_color = R
    elif remaining < 1800:
        time_color = Y
    else:
        time_color = G

    pbar = draw_progress_bar(len(sprint.completed), len(sprint.tasks))

    # Compact header
    print(f"  {BOLD}{C}SPRINT:{RST} {sprint.name}  {time_color}{BOLD}{format_time(remaining)}{RST}  {DIM}{format_time(elapsed)} elapsed{RST}")
    print(f"  {pbar}  {len(sprint.completed)}/{len(sprint.tasks)} done\n")

    # Compact task list — one line each, minimal
    for t in sprint.tasks:
        if t["done"]:
            print(f"  {G}✓ {t['id']}{RST} {DIM}{t['name']}{RST}")
        elif sprint.remaining and t["id"] == sprint.remaining[0]["id"]:
            # Current task — highlighted
            print(f"  {Y}▸ {t['id']}{RST} {BOLD}{W}{t['name']}{RST} {Y}~{t['time_estimate']}{RST}")
        else:
            print(f"  {DIM}○ {t['id']} {t['name']}{RST}")

    # INSTRUCTIONS — always visible, prominent
    if sprint.remaining:
        nxt = sprint.remaining[0]
        print(f"\n  {BOLD}{C}{'─' * 50}{RST}")
        print(f"  {BOLD}{Y}NOW:{RST} {BOLD}{nxt['name']}{RST} ({nxt['platform']})")
        if nxt["instructions"]:
            for i, step in enumerate(nxt["instructions"], 1):
                print(f"  {W}{i}. {step}{RST}")
        print(f"  {BOLD}{C}{'─' * 50}{RST}")

    print(f"\n  {DIM}[1-9] done  [s] refresh  [q] quit{RST}")


# ── Reminder / Alarm Thread ─────────────────────────────────────────────────

def reminder_loop(sprint: Sprint, stop_event: threading.Event):
    """Background thread: sends reminders and alarms."""
    last_reminder = datetime.now()
    deadline_alarmed = False

    while not stop_event.is_set():
        time.sleep(5)
        now = datetime.now()

        if sprint.all_done:
            break

        # Periodic reminder
        if (now - last_reminder).total_seconds() >= sprint.reminder_interval * 60:
            done = len(sprint.completed)
            total = len(sprint.tasks)
            left = format_time(sprint.remaining_seconds())
            notify("Sprint Reminder",
                   f"{done}/{total} tasks done. {left} remaining. Keep going!",
                   "Ping")
            last_reminder = now

        # Stale warning: nothing completed in X minutes
        if sprint.last_completion_time:
            stale = (now - sprint.last_completion_time).total_seconds()
        else:
            stale = sprint.elapsed_seconds()

        if stale >= sprint.stale_warning_minutes * 60 and not sprint.all_done:
            notify("STALE WARNING",
                   f"No tasks completed in {sprint.stale_warning_minutes}min! Move faster!",
                   "Sosumi")
            say(f"Warning. No tasks completed in {sprint.stale_warning_minutes} minutes.")
            # Reset so it fires again after another interval
            sprint.last_completion_time = now

        # Deadline alarm
        if sprint.remaining_seconds() <= 0 and not deadline_alarmed and not sprint.all_done:
            deadline_alarmed = True
            notify("TIME'S UP",
                   f"Sprint deadline hit! {len(sprint.remaining)} tasks still incomplete!",
                   "Sosumi")
            say("Time is up! Sprint deadline reached. You have incomplete tasks.")
            alarm_sound(5)

        # 10-minute warning
        if 595 < sprint.remaining_seconds() < 605 and not sprint.all_done:
            notify("10 MINUTES LEFT",
                   f"{len(sprint.remaining)} tasks remaining. Push through!",
                   "Funk")
            say("Ten minutes remaining.")


# ── Main Loop ───────────────────────────────────────────────────────────────

def get_char_nonblocking(timeout: float = 0.5) -> str | None:
    """Read a single character from stdin without blocking."""
    if select.select([sys.stdin], [], [], timeout)[0]:
        return sys.stdin.read(1)
    return None


def run_sprint(config_path: str):
    sprint = Sprint(config_path)

    print(f"\n{BOLD}{C}Sprint: {sprint.name}{RST}")
    print(f"Duration: {sprint.total_minutes} minutes")
    print(f"Tasks: {len(sprint.tasks)}")
    print(f"\nReminders every {sprint.reminder_interval}min")
    print(f"Stale warning if nothing done in {sprint.stale_warning_minutes}min")
    print(f"\n{Y}Press ENTER to start the sprint...{RST}")
    input()

    sprint.start_time = datetime.now()
    sprint.end_time = sprint.start_time + timedelta(minutes=sprint.total_minutes)
    sprint.last_completion_time = datetime.now()

    notify("Sprint Started!",
           f"{sprint.name} — {sprint.total_minutes} min — {len(sprint.tasks)} tasks",
           "Glass")

    stop_event = threading.Event()
    reminder_thread = threading.Thread(target=reminder_loop, args=(sprint, stop_event), daemon=True)
    reminder_thread.start()

    # Set terminal to raw mode for single-char input
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())
        render(sprint)

        while True:
            ch = get_char_nonblocking(1.0)

            if ch:
                if ch == 'q':
                    break
                elif ch == 's':
                    render(sprint)
                elif ch.isdigit() and int(ch) > 0:
                    task_num = int(ch)
                    msg = sprint.mark_done(task_num)
                    if "completed" in msg:
                        notify("Task Done!", msg, "Glass")
                    render(sprint)
                    # Print feedback below the render
                    print(f"  {G}{msg}{RST}")
                continue

            # Re-render every second for countdown
            render(sprint)

            if sprint.all_done:
                elapsed = format_time(sprint.elapsed_seconds())
                print(f"\n  {G}{BOLD}ALL TASKS COMPLETE in {elapsed}!{RST}")
                notify("SPRINT COMPLETE!",
                       f"All {len(sprint.tasks)} tasks done in {elapsed}!",
                       "Glass")
                say(f"Sprint complete! All tasks finished in {elapsed}.")
                alarm_sound(1)
                break

            if sprint.remaining_seconds() <= 0 and not sprint.all_done:
                # Keep running past deadline so user can still mark tasks
                pass

    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        stop_event.set()

    # Save results
    results = {
        "sprint_name": sprint.name,
        "started_at": sprint.start_time.isoformat() if sprint.start_time else None,
        "ended_at": datetime.now().isoformat(),
        "elapsed_seconds": int(sprint.elapsed_seconds()),
        "total_tasks": len(sprint.tasks),
        "completed_tasks": len(sprint.completed),
        "tasks": [{
            "id": t["id"],
            "name": t["name"],
            "platform": t["platform"],
            "done": t["done"],
            "done_at": t["done_at"],
        } for t in sprint.tasks],
    }

    results_dir = Path(config_path).parent / "sprint_results"
    results_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = results_dir / f"sprint_{ts}.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n  {DIM}Results saved: {results_path}{RST}")

    # Print summary
    print(f"""
{BOLD}{'=' * 58}{RST}
  Sprint: {sprint.name}
  Time:   {format_time(sprint.elapsed_seconds())} / {sprint.total_minutes}min
  Done:   {len(sprint.completed)}/{len(sprint.tasks)} tasks
{'=' * 58}""")

    for t in sprint.tasks:
        mark = f"{G}✓{RST}" if t["done"] else f"{R}✗{RST}"
        print(f"  {mark} {t['name']}")

    incomplete = sprint.remaining
    if incomplete:
        print(f"\n  {R}{BOLD}INCOMPLETE ({len(incomplete)}):{RST}")
        for t in incomplete:
            print(f"    → {t['name']} ({t['platform']})")

    print()


def print_example():
    example = {
        "sprint_name": "Example Sprint",
        "total_minutes": 120,
        "reminder_interval_minutes": 15,
        "stale_warning_minutes": 20,
        "tasks": [
            {
                "name": "Do the thing",
                "platform": "Gumroad",
                "time_estimate": "15min",
                "instructions": [
                    "Step 1: go here",
                    "Step 2: paste this",
                ]
            }
        ]
    }
    print(json.dumps(example, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <sprint_file.json>")
        print(f"       python3 {sys.argv[0]} --example")
        sys.exit(1)

    if sys.argv[1] == "--example":
        print_example()
    else:
        run_sprint(sys.argv[1])
