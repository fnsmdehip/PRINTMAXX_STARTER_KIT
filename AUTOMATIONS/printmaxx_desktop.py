#!/usr/bin/env python3
"""
PRINTMAXX Command Center v2 — Full Master Ops Integration
Zero-dependency desktop app (tkinter + openpyxl for XLSX).
Integrates: Daily Goals, 180 Ops, 18 Priority Items, 55 Ventures,
38 Alpha Theses, 26 Synergy Stacks, Video/LeadGen/Hosting/Browser stacks,
Product Launch Tracker, Alarms, Hourly Reminders with Goal Progress.

Usage:
  python3 AUTOMATIONS/printmaxx_desktop.py
  python3 AUTOMATIONS/printmaxx_desktop.py --minimized
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import time
import csv
import re
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# ── paths ───────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"

# ── colors (dark PRINTMAXX theme) ──────────────────────────────────────────
BG = "#0d1117"
BG2 = "#161b22"
BG3 = "#21262d"
FG = "#c9d1d9"
FG2 = "#8b949e"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
RED = "#f85149"
YELLOW = "#d29922"
PURPLE = "#bc8cff"
ORANGE = "#f0883e"
WHITE = "#ffffff"
CYAN = "#39d2c0"

# ── motivational quotes ────────────────────────────────────────────────────
MOTIVATION = [
    "the version of you that wins everything just woke up. prove it.",
    "stop overthinking. just ship it. the market will tell you if it's good.",
    "every minute planning instead of shipping = $0. every minute shipping = compounding.",
    "you have 200+ scripts built and $0 revenue. open accounts. list products. NOW.",
    "someone with half your tools is making 10x your revenue right now. because they shipped.",
    "the game rewards aggression not caution. go all in. leave nothing on the table.",
    "your future self is watching you through your memories. make that version proud.",
    "cold emailed 200 dentists. 14% reply rate. $2.5k closed before lunch. just send the emails.",
    "12,948 hot leads sitting in a CSV. 0 emails sent. fix that TODAY.",
    "278 alpha entries pending review. each one could be $1K/mo. process them.",
    "the bar is lower than you think. most people are zombified. just try.",
    "0/48 accounts created. that's the only thing blocking all revenue. fix it.",
    "don't build another system. deploy the ones you have.",
    "figure-it-the-fuck-out attitude. that's the whole strategy.",
    "accept the money. list the products. send the emails. ship the apps.",
    "every piece of research that doesn't become content is wasted alpha.",
    "one piece of content, 6x distribution. stop overthinking this.",
    "6 apps deployed. 0 in app stores. 0 on product directories. fix that.",
    "you are not competing with other solopreneurs. you're competing with your own inaction.",
    "build, print, compound. that's the entire playbook.",
    "revenue solves all problems. ship something that makes money TODAY.",
    "deploy first, build second. every time. no exceptions.",
    "if you're not embarrassed by the first version, you launched too late.",
    "48 accounts needed. 0 created. that's not a technical problem. open the signup page.",
    "your overnight system ran 72 scripts while you slept. now ship what it found.",
    "failure is content. 'I spent 6 hours on X and here's what I learned' > 'shipped X, it's great'",
    "documentation without execution is cope. execution without documentation is fine.",
    "an imperfect product that's live beats a perfect product that's not.",
    "treat every research task like a hedge fund analyst. stress test claims.",
    "use every piece of the hunt. native american principle. nothing gets wasted.",
]

# ── hourly tasks ────────────────────────────────────────────────────────────
HOURLY_TASKS = {
    7: "MORNING: Check HEARTBEAT. Run daily_agent_runner --status. Review overnight logs.",
    8: "Check alpha staging (278 pending). Process top 10. Generate 3 tweets from findings.",
    9: "OUTREACH HOUR: Open Reddit. Post freelance responses. Check freelance pipeline.",
    10: "PRODUCT HOUR: Submit 1 product to 5 launch directories. Update tracker.",
    11: "CONTENT HOUR: Review content QA queue. Approve/reject 10 pieces. Schedule posts.",
    12: "MIDDAY CHECK: Run system_health_monitor --quick. Check leads pipeline.",
    13: "BUILD HOUR: Work on highest priority unblocked task from tracker.",
    14: "BUILD HOUR: Continue on priority task. Ship something by 3 PM.",
    15: "DEPLOY HOUR: Deploy anything deployable. Run tests. Push live.",
    16: "OUTREACH HOUR 2: Send cold emails from HOT_BATCH. Follow up on responses.",
    17: "CONTENT SQUEEZE: Generate 3 tweets + 1 thread from today's work.",
    18: "EVENING: Run rebalancer. Update HEARTBEAT. Log today's learnings.",
    19: "EVENING: Review all task statuses. Update tracker. Plan tomorrow.",
    20: "WRAP UP: Run memory_manager --full. Check overnight system is armed.",
    21: "OVERNIGHT PREP: perpetual_ship_engine.sh armed. Cron verified.",
}


# ── notifications ───────────────────────────────────────────────────────────
def macos_notify(title: str, message: str, sound: str = "Glass"):
    script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
    try:
        subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def macos_alert(title: str, message: str):
    script = f'display alert "{title}" message "{message}" as informational'
    try:
        subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


# ── data loading ────────────────────────────────────────────────────────────

def load_heartbeat() -> dict:
    hb_path = OPS / "HEARTBEAT.md"
    data = {"timestamp": "unknown", "lines": [], "raw": {}}
    if not hb_path.exists():
        return data
    text = hb_path.read_text()
    for line in text.strip().splitlines():
        line = line.strip()
        if line.startswith("# HEARTBEAT"):
            m = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", line)
            if m:
                data["timestamp"] = m.group(1)
        elif line and not line.startswith("#"):
            data["lines"].append(line)
            # parse key metrics
            if "hot" in line.lower():
                m = re.search(r"([\d,]+)\s*hot", line)
                if m:
                    data["raw"]["hot_leads"] = m.group(1)
            if "revenue" in line.lower():
                m = re.search(r"\$([\d,.]+)", line)
                if m:
                    data["raw"]["revenue"] = m.group(1)
            if "alpha" in line.lower() and "pending" in line.lower():
                m = re.search(r"(\d+)\s*pending", line)
                if m:
                    data["raw"]["alpha_pending"] = m.group(1)
            if "account" in line.lower():
                m = re.search(r"(\d+/\d+)", line)
                if m:
                    data["raw"]["accounts"] = m.group(1)
            if "app" in line.lower() and "live" in line.lower():
                m = re.search(r"(\d+/\d+)\s*live", line)
                if m:
                    data["raw"]["apps_live"] = m.group(1)
            if "script" in line.lower():
                m = re.search(r"(\d+)\s*automation", line)
                if m:
                    data["raw"]["scripts"] = m.group(1)
    return data


def load_daily_goals() -> list:
    """Parse daily goals from OPS/DAILY_GOALS_*.md (today's date)."""
    today = datetime.now().strftime("%Y_%m_%d")
    goal_path = OPS / f"DAILY_GOALS_{today.replace('_', '_')}.md"
    # also try with dashes
    if not goal_path.exists():
        goal_path = OPS / f"DAILY_GOALS_{datetime.now().strftime('%Y-%m-%d')}.md"
    if not goal_path.exists():
        # scan for any daily goals file for today
        for f in OPS.glob("DAILY_GOALS_*"):
            if today in f.name or datetime.now().strftime("%Y-%m-%d") in f.name:
                goal_path = f
                break
    if not goal_path.exists():
        return []

    goals = []
    text = goal_path.read_text()
    current_goal = None
    for line in text.splitlines():
        if line.startswith("### ") and re.match(r"### \d+\.", line):
            if current_goal:
                goals.append(current_goal)
            title = re.sub(r"### \d+\.\s*", "", line).strip()
            current_goal = {"title": title, "tasks": [], "done_count": 0}
        elif current_goal and line.strip().startswith("- ["):
            checked = "[x]" in line.lower() or "[X]" in line
            task_text = re.sub(r"- \[.\]\s*", "", line.strip())
            current_goal["tasks"].append({"text": task_text, "done": checked})
            if checked:
                current_goal["done_count"] += 1
    if current_goal:
        goals.append(current_goal)
    return goals


def load_tasks() -> list:
    path = OPS / "PERSISTENT_TASK_TRACKER.md"
    tasks = []
    if not path.exists():
        return tasks
    text = path.read_text()
    current_task = None
    for line in text.splitlines():
        if line.startswith("### T"):
            if current_task:
                tasks.append(current_task)
            m = re.match(r"### (T\d+):\s*(.*)", line)
            if m:
                current_task = {"id": m.group(1), "title": m.group(2), "status": "UNKNOWN", "priority": "", "details": []}
        elif current_task and line.startswith("- **Status:**"):
            m = re.search(r"Status:\*\*\s*(.*)", line)
            if m:
                st = m.group(1).strip()
                if "DONE" in st:
                    current_task["status"] = "DONE"
                elif "IN_PROGRESS" in st:
                    current_task["status"] = "IN_PROGRESS"
                elif "BLOCKED" in st:
                    current_task["status"] = "BLOCKED"
                else:
                    current_task["status"] = "PENDING"
        elif current_task and line.startswith("- **Priority:**"):
            m = re.search(r"Priority:\*\*\s*(.*)", line)
            if m:
                current_task["priority"] = m.group(1).strip()
        elif current_task and line.startswith("- "):
            current_task["details"].append(line.strip("- ").strip())
    if current_task:
        tasks.append(current_task)
    return tasks


def load_launch_tracker() -> list:
    path = LEDGER / "LAUNCH_DIRECTORY_TRACKER.csv"
    entries = []
    if not path.exists():
        return entries
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def load_master_ops() -> dict:
    """Load Master Ops Enhanced XLSX using openpyxl."""
    data = {
        "auto_status": [],
        "priority_exec": [],
        "ventures": [],
        "synergy": [],
        "alpha_thesis": [],
        "video_stack": [],
        "lead_gen": [],
        "hosting": [],
        "browser_proxy": [],
        "existing_infra": [],
        "filename": None,
    }
    try:
        import openpyxl
    except ImportError:
        return data

    # find latest enhanced xlsx
    xlsx_files = sorted(BASE.glob("PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx"), reverse=True)
    if not xlsx_files:
        xlsx_files = sorted(BASE.glob("PRINTMAXX_MASTER_OPS*.xlsx"), reverse=True)
    if not xlsx_files:
        return data

    xlsx_path = xlsx_files[0]
    data["filename"] = xlsx_path.name

    try:
        wb = openpyxl.load_workbook(str(xlsx_path), read_only=True, data_only=True)
    except Exception:
        return data

    def sheet_to_dicts(name):
        if name not in wb.sheetnames:
            return []
        ws = wb[name]
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) < 2:
            return []
        headers = [str(h or "").strip() for h in rows[0]]
        result = []
        for row in rows[1:]:
            if all(c is None for c in row):
                continue
            d = {}
            for i, h in enumerate(headers):
                if h and i < len(row):
                    d[h] = row[i]
            result.append(d)
        return result

    # map sheet names (try exact then fuzzy match)
    sheet_map = {
        "auto_status": ["AUTO_STATUS_LIVE"],
        "priority_exec": ["PRIORITY_AUTOMATION_EXEC"],
        "ventures": ["VENTURE_AUTOMATION_MAP"],
        "synergy": ["SYNERGY_STACKS"],
        "alpha_thesis": ["ALPHA_THESIS_INDEX"],
        "video_stack": ["VIDEO & MEDIA STACK", "VIDEO_MEDIA_STACK"],
        "lead_gen": ["LEAD GEN STACK", "LEAD_GEN_STACK"],
        "hosting": ["HOSTING & DEPLOY", "HOSTING_DEPLOY"],
        "browser_proxy": ["BROWSER & PROXY STACK", "BROWSER_PROXY_STACK"],
        "existing_infra": ["EXISTING INFRA", "EXISTING_INFRA"],
    }

    for key, candidates in sheet_map.items():
        for name in candidates:
            if name in wb.sheetnames:
                data[key] = sheet_to_dicts(name)
                break
        # fuzzy match
        if not data[key]:
            for sn in wb.sheetnames:
                for cand in candidates:
                    if cand.lower().replace(" ", "").replace("_", "") in sn.lower().replace(" ", "").replace("_", ""):
                        data[key] = sheet_to_dicts(sn)
                        break
                if data[key]:
                    break

    wb.close()
    return data


# ── alarm manager ───────────────────────────────────────────────────────────

class AlarmManager:
    def __init__(self):
        self.alarms = []
        self._lock = threading.Lock()

    def add_alarm(self, alarm_time: datetime, message: str):
        with self._lock:
            self.alarms.append({"time": alarm_time, "message": message, "fired": False})

    def remove_alarm(self, index: int):
        with self._lock:
            if 0 <= index < len(self.alarms):
                self.alarms.pop(index)

    def check_alarms(self):
        fired = []
        now = datetime.now()
        with self._lock:
            for alarm in self.alarms:
                if not alarm["fired"] and now >= alarm["time"]:
                    alarm["fired"] = True
                    fired.append(alarm["message"])
        return fired

    def get_pending(self) -> list:
        with self._lock:
            return [a for a in self.alarms if not a["fired"]]


# ── reminder engine ─────────────────────────────────────────────────────────

class ReminderEngine(threading.Thread):
    def __init__(self, alarm_mgr: AlarmManager):
        super().__init__(daemon=True)
        self.alarm_mgr = alarm_mgr
        self.running = True
        self._last_hour_notified = -1
        self._last_motivation_idx = 0

    def run(self):
        while self.running:
            now = datetime.now()
            hour = now.hour
            minute = now.minute

            # hourly task + daily goal progress
            if hour != self._last_hour_notified and hour in HOURLY_TASKS:
                self._last_hour_notified = hour
                task_msg = HOURLY_TASKS[hour]
                macos_notify("PRINTMAXX hourly", task_msg, "Purr")

                # daily goals progress reminder
                goals = load_daily_goals()
                if goals:
                    total = sum(len(g["tasks"]) for g in goals)
                    done = sum(g["done_count"] for g in goals)
                    remaining = [g["title"] for g in goals if g["done_count"] < len(g["tasks"])]
                    if remaining:
                        goal_msg = f"GOALS: {done}/{total} done. Still need: {', '.join(remaining[:3])}"
                        macos_notify("PRINTMAXX GOALS", goal_msg, "Tink")

            # motivation every 30 min at :30
            if minute == 30:
                quote = MOTIVATION[self._last_motivation_idx % len(MOTIVATION)]
                self._last_motivation_idx += 1
                macos_notify("PRINTMAXX", quote, "Tink")

            # custom alarms
            fired = self.alarm_mgr.check_alarms()
            for msg in fired:
                macos_alert("PRINTMAXX ALARM", msg)
                subprocess.Popen(["afplay", "/System/Library/Sounds/Funk.aiff"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            next_min = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
            sleep_secs = max(1, (next_min - datetime.now()).total_seconds())
            time.sleep(sleep_secs)

    def stop(self):
        self.running = False


# ── helper: scrolled text widget ────────────────────────────────────────────

def make_text(parent, height=10, **kw):
    t = scrolledtext.ScrolledText(
        parent, bg=BG2, fg=FG, font=("Menlo", 11), relief="flat",
        wrap="word", insertbackground=FG, state="disabled", height=height, **kw
    )
    return t


def write_text(widget, content_fn):
    """Helper to update a disabled text widget."""
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    content_fn(widget)
    widget.configure(state="disabled")


# ── main GUI ────────────────────────────────────────────────────────────────

class PrintmaxxApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PRINTMAXX Command Center v2")
        self.root.geometry("1200x900")
        self.root.configure(bg=BG)
        self.root.minsize(1000, 700)

        self.alarm_mgr = AlarmManager()
        self.reminder_engine = ReminderEngine(self.alarm_mgr)
        self.reminder_engine.start()

        # cached data
        self.master_ops = {}
        self.daily_goals = []
        self.goal_vars = {}  # track checkbox state

        # style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=BG, foreground=FG, font=("Menlo", 11))
        style.configure("TNotebook", background=BG)
        style.configure("TNotebook.Tab", background=BG2, foreground=FG, padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", BG3)], foreground=[("selected", ACCENT)])
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG)
        style.configure("TButton", background=BG3, foreground=FG)

        # header
        header = tk.Frame(root, bg=BG, height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(header, text="PRINTMAXX", font=("Menlo", 24, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        self.clock_label = tk.Label(header, text="", font=("Menlo", 14), fg=FG2, bg=BG)
        self.clock_label.pack(side="right")
        self.status_label = tk.Label(header, text="", font=("Menlo", 11), fg=GREEN, bg=BG)
        self.status_label.pack(side="right", padx=20)

        # notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # build all tabs
        self.build_dashboard_tab()
        self.build_goals_tab()
        self.build_operations_tab()
        self.build_priority_tab()
        self.build_intelligence_tab()
        self.build_tools_infra_tab()
        self.build_tasks_tab()
        self.build_launch_tab()
        self.build_alarms_tab()
        self.build_quick_launch_tab()

        # load data + start refresh
        self.load_all_data()
        self.refresh_all()
        self.update_clock()

    def load_all_data(self):
        """Load heavy data (XLSX) once, refresh lighter data periodically."""
        self.status_label.configure(text="Loading Master Ops...", fg=YELLOW)
        self.root.update()
        self.master_ops = load_master_ops()
        self.daily_goals = load_daily_goals()
        fname = self.master_ops.get("filename", "not found")
        ops_count = len(self.master_ops.get("auto_status", []))
        self.status_label.configure(text=f"Loaded {ops_count} ops from {fname}", fg=GREEN)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 1: DASHBOARD
    # ══════════════════════════════════════════════════════════════════════

    def build_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Dashboard ")

        # heartbeat section
        hb_frame = tk.Frame(frame, bg=BG2, highlightbackground=BG3, highlightthickness=1)
        hb_frame.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(hb_frame, text="SYSTEM HEARTBEAT", font=("Menlo", 13, "bold"), fg=ACCENT, bg=BG2).pack(anchor="w", padx=10, pady=(8, 2))
        self.heartbeat_text = make_text(hb_frame, height=8)
        self.heartbeat_text.pack(fill="x", padx=10, pady=(2, 8))

        # quick stats row
        stats_frame = tk.Frame(frame, bg=BG)
        stats_frame.pack(fill="x", padx=10, pady=5)
        self.stat_labels = {}
        stat_items = [
            ("Revenue", "$0", RED),
            ("Accounts", "0/48", RED),
            ("Hot Leads", "12,948", GREEN),
            ("Alpha", "278", YELLOW),
            ("Apps", "6/6", GREEN),
            ("Scripts", "222", ACCENT),
            ("Ops", "0", PURPLE),
            ("Ventures", "0", CYAN),
        ]
        for label, default, color in stat_items:
            sf = tk.Frame(stats_frame, bg=BG2, highlightbackground=BG3, highlightthickness=1)
            sf.pack(side="left", fill="both", expand=True, padx=2)
            tk.Label(sf, text=label, font=("Menlo", 9), fg=FG2, bg=BG2).pack(pady=(4, 0))
            lbl = tk.Label(sf, text=default, font=("Menlo", 14, "bold"), fg=color, bg=BG2)
            lbl.pack(pady=(0, 4))
            self.stat_labels[label] = lbl

        # daily goals summary + motivation side by side
        bottom = tk.Frame(frame, bg=BG)
        bottom.pack(fill="both", expand=True, padx=10, pady=5)

        # goals summary (left)
        goal_sum = tk.Frame(bottom, bg=BG2, highlightbackground=GREEN, highlightthickness=1)
        goal_sum.pack(side="left", fill="both", expand=True, padx=(0, 3))
        tk.Label(goal_sum, text="TODAY'S GOALS", font=("Menlo", 11, "bold"), fg=GREEN, bg=BG2).pack(anchor="w", padx=10, pady=(8, 2))
        self.goals_summary_text = make_text(goal_sum, height=8)
        self.goals_summary_text.pack(fill="both", expand=True, padx=10, pady=(2, 8))
        self.goals_summary_text.tag_configure("done", foreground=GREEN)
        self.goals_summary_text.tag_configure("pending", foreground=RED)
        self.goals_summary_text.tag_configure("header", font=("Menlo", 11, "bold"))

        # motivation + current task (right)
        right_col = tk.Frame(bottom, bg=BG)
        right_col.pack(side="left", fill="both", expand=True, padx=(3, 0))

        mot_frame = tk.Frame(right_col, bg=BG2, highlightbackground=PURPLE, highlightthickness=1)
        mot_frame.pack(fill="x", pady=(0, 3))
        tk.Label(mot_frame, text="MOTIVATION", font=("Menlo", 11, "bold"), fg=PURPLE, bg=BG2).pack(anchor="w", padx=10, pady=(8, 2))
        self.motivation_label = tk.Label(mot_frame, text="", font=("Menlo", 11, "italic"), fg=WHITE, bg=BG2, wraplength=500, justify="left")
        self.motivation_label.pack(fill="x", padx=10, pady=(2, 8))

        hour_frame = tk.Frame(right_col, bg=BG2, highlightbackground=ORANGE, highlightthickness=1)
        hour_frame.pack(fill="both", expand=True, pady=(3, 0))
        tk.Label(hour_frame, text="CURRENT FOCUS", font=("Menlo", 11, "bold"), fg=ORANGE, bg=BG2).pack(anchor="w", padx=10, pady=(8, 2))
        self.hour_task_label = tk.Label(hour_frame, text="", font=("Menlo", 11), fg=WHITE, bg=BG2, wraplength=500, justify="left")
        self.hour_task_label.pack(fill="x", padx=10, pady=(2, 8))

    # ══════════════════════════════════════════════════════════════════════
    # TAB 2: DAILY GOALS (with checkboxes)
    # ══════════════════════════════════════════════════════════════════════

    def build_goals_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Daily Goals ")

        header = tk.Frame(frame, bg=BG2, highlightbackground=GREEN, highlightthickness=1)
        header.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header, text="TODAY'S GOALS — CHECK OFF AS COMPLETED", font=("Menlo", 13, "bold"), fg=GREEN, bg=BG2).pack(anchor="w", padx=10, pady=8)
        self.goals_progress_label = tk.Label(header, text="", font=("Menlo", 12), fg=YELLOW, bg=BG2)
        self.goals_progress_label.pack(anchor="w", padx=10, pady=(0, 8))

        # scrollable goals
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.goals_inner = tk.Frame(canvas, bg=BG)
        self.goals_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.goals_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

    def refresh_goals_tab(self):
        # clear previous
        for w in self.goals_inner.winfo_children():
            w.destroy()
        self.goal_vars.clear()

        goals = self.daily_goals
        if not goals:
            tk.Label(self.goals_inner, text="  No daily goals found for today.", font=("Menlo", 12), fg=FG2, bg=BG).pack(anchor="w", padx=10, pady=10)
            self.goals_progress_label.configure(text="No goals loaded")
            return

        total_tasks = sum(len(g["tasks"]) for g in goals)
        total_done = sum(g["done_count"] for g in goals)

        for i, goal in enumerate(goals):
            gf = tk.Frame(self.goals_inner, bg=BG2, highlightbackground=BG3, highlightthickness=1)
            gf.pack(fill="x", padx=5, pady=3)

            done = goal["done_count"]
            total = len(goal["tasks"])
            pct = int(done / total * 100) if total > 0 else 0
            color = GREEN if pct == 100 else (YELLOW if pct > 0 else RED)

            tk.Label(gf, text=f"  {i + 1}. {goal['title']}  [{done}/{total}]", font=("Menlo", 12, "bold"), fg=color, bg=BG2).pack(anchor="w", padx=10, pady=(8, 4))

            for j, task in enumerate(goal["tasks"]):
                key = f"g{i}_t{j}"
                var = tk.BooleanVar(value=task["done"])
                self.goal_vars[key] = var
                cb = tk.Checkbutton(
                    gf, text=task["text"], variable=var,
                    font=("Menlo", 11), fg=FG if not task["done"] else GREEN,
                    bg=BG2, selectcolor=BG3, activebackground=BG2, activeforeground=ACCENT,
                    anchor="w",
                )
                cb.pack(anchor="w", padx=30, pady=1)

            # progress bar
            bar_frame = tk.Frame(gf, bg=BG3, height=6)
            bar_frame.pack(fill="x", padx=10, pady=(4, 8))
            if pct > 0:
                fill = tk.Frame(bar_frame, bg=color, height=6, width=max(1, int(pct * 4)))
                fill.place(x=0, y=0, relheight=1)

        self.goals_progress_label.configure(text=f"Overall: {total_done}/{total_tasks} tasks done ({int(total_done / total_tasks * 100) if total_tasks else 0}%)")

    # ══════════════════════════════════════════════════════════════════════
    # TAB 3: OPERATIONS (180 ops from AUTO_STATUS_LIVE)
    # ══════════════════════════════════════════════════════════════════════

    def build_operations_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Operations ")

        # filter bar
        filter_frame = tk.Frame(frame, bg=BG)
        filter_frame.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(filter_frame, text="Filter:", font=("Menlo", 11), fg=FG, bg=BG).pack(side="left")
        self.ops_filter = tk.StringVar(value="ALL")
        for label, val in [("All", "ALL"), ("Ready", "READY"), ("Blocked", "BLOCKED"), ("High Score", "HIGH")]:
            rb = tk.Radiobutton(
                filter_frame, text=label, variable=self.ops_filter, value=val,
                bg=BG, fg=FG, selectcolor=BG2, activebackground=BG, activeforeground=ACCENT,
                font=("Menlo", 10), command=self.refresh_operations,
            )
            rb.pack(side="left", padx=5)

        self.ops_count_label = tk.Label(filter_frame, text="", font=("Menlo", 10), fg=FG2, bg=BG)
        self.ops_count_label.pack(side="right")

        self.ops_text = make_text(frame, height=30)
        self.ops_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.ops_text.tag_configure("high", foreground=GREEN, font=("Menlo", 11, "bold"))
        self.ops_text.tag_configure("medium", foreground=YELLOW)
        self.ops_text.tag_configure("low", foreground=FG2)
        self.ops_text.tag_configure("blocked", foreground=RED)
        self.ops_text.tag_configure("header", font=("Menlo", 12, "bold"), foreground=ACCENT)
        self.ops_text.tag_configure("score", foreground=PURPLE)

    def refresh_operations(self):
        ops = self.master_ops.get("auto_status", [])
        filt = self.ops_filter.get()

        def content(w):
            if not ops:
                w.insert("end", "  No operations data loaded. Check PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx\n")
                return

            w.insert("end", f"  AUTO_STATUS_LIVE — {len(ops)} Operations\n\n", "header")
            w.insert("end", f"  {'OP_ID':<12} {'OP_NAME':<35} {'LANE':<12} {'READY':<10} {'SCORE':<8} {'BLOCKER'}\n", "header")
            w.insert("end", "  " + "-" * 100 + "\n")

            shown = 0
            for op in ops:
                op_id = str(op.get("OP_ID", ""))
                name = str(op.get("OP_NAME", ""))[:34]
                lane = str(op.get("LANE", ""))[:11]
                readiness = str(op.get("READINESS", ""))[:9]
                score = op.get("AUTOMATION_SCORE_100", 0)
                try:
                    score_num = float(score) if score else 0
                except (ValueError, TypeError):
                    score_num = 0
                blocker = str(op.get("BLOCKER_KEY", "") or "")

                # filter
                if filt == "READY" and "ready" not in readiness.lower() and score_num < 50:
                    continue
                elif filt == "BLOCKED" and not blocker:
                    continue
                elif filt == "HIGH" and score_num < 70:
                    continue

                # color by score
                if score_num >= 70:
                    tag = "high"
                elif score_num >= 40:
                    tag = "medium"
                elif blocker:
                    tag = "blocked"
                else:
                    tag = "low"

                w.insert("end", f"  {op_id:<12} {name:<35} {lane:<12} {readiness:<10} ", tag)
                w.insert("end", f"{score_num:<8.0f}", "score")
                w.insert("end", f" {blocker}\n", "blocked" if blocker else tag)
                shown += 1

            self.ops_count_label.configure(text=f"Showing {shown}/{len(ops)}")

        write_text(self.ops_text, content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 4: PRIORITY LAUNCH (18 ranked items)
    # ══════════════════════════════════════════════════════════════════════

    def build_priority_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Priority ")

        self.priority_text = make_text(frame, height=30)
        self.priority_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.priority_text.tag_configure("rank1", foreground=RED, font=("Menlo", 12, "bold"))
        self.priority_text.tag_configure("rank2", foreground=ORANGE, font=("Menlo", 11, "bold"))
        self.priority_text.tag_configure("rank3", foreground=YELLOW)
        self.priority_text.tag_configure("header", foreground=ACCENT, font=("Menlo", 13, "bold"))
        self.priority_text.tag_configure("detail", foreground=FG2)

    def refresh_priority(self):
        items = self.master_ops.get("priority_exec", [])

        def content(w):
            w.insert("end", "  PRIORITY AUTOMATION EXEC — Ranked Launch Priorities\n\n", "header")
            if not items:
                w.insert("end", "  No priority data loaded.\n")
                return

            for i, item in enumerate(items):
                # try to get rank/priority
                rank = item.get("RANK", item.get("PRIORITY_RANK", i + 1))
                try:
                    rank_num = float(rank) if rank else i + 1
                except (ValueError, TypeError):
                    rank_num = i + 1

                tag = "rank1" if rank_num <= 3 else ("rank2" if rank_num <= 8 else "rank3")
                name = str(item.get("OP_NAME", item.get("NAME", "")))
                category = str(item.get("CATEGORY", ""))
                status = str(item.get("STATUS", item.get("LANE", "")))

                w.insert("end", f"  #{rank_num:<5.1f} ", tag)
                w.insert("end", f"{name}\n", tag)
                w.insert("end", f"         Category: {category}  |  Status: {status}\n", "detail")

                # show any additional fields
                for key in ["BLOCKER_KEY", "NEXT_ACTION", "NEXT_AUTOMATION_ACTION", "READINESS", "AUTOMATION_SCORE_100"]:
                    val = item.get(key)
                    if val:
                        w.insert("end", f"         {key}: {val}\n", "detail")
                w.insert("end", "\n")

        write_text(self.priority_text, content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 5: INTELLIGENCE (Alpha Theses, Synergy, Ventures)
    # ══════════════════════════════════════════════════════════════════════

    def build_intelligence_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Intelligence ")

        # sub-notebook for 3 sections
        sub_nb = ttk.Notebook(frame)
        sub_nb.pack(fill="both", expand=True, padx=5, pady=5)

        # Alpha Theses
        at_frame = ttk.Frame(sub_nb)
        sub_nb.add(at_frame, text=" Alpha Theses (38) ")
        self.alpha_thesis_text = make_text(at_frame, height=25)
        self.alpha_thesis_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.alpha_thesis_text.tag_configure("header", foreground=ACCENT, font=("Menlo", 12, "bold"))
        self.alpha_thesis_text.tag_configure("opportunity", foreground=GREEN)
        self.alpha_thesis_text.tag_configure("blocked", foreground=RED)
        self.alpha_thesis_text.tag_configure("detail", foreground=FG2)

        # Synergy Stacks
        sy_frame = ttk.Frame(sub_nb)
        sub_nb.add(sy_frame, text=" Synergy Stacks (26) ")
        self.synergy_text = make_text(sy_frame, height=25)
        self.synergy_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.synergy_text.tag_configure("header", foreground=ACCENT, font=("Menlo", 12, "bold"))
        self.synergy_text.tag_configure("high_synergy", foreground=GREEN, font=("Menlo", 11, "bold"))
        self.synergy_text.tag_configure("detail", foreground=FG2)

        # Ventures
        ve_frame = ttk.Frame(sub_nb)
        sub_nb.add(ve_frame, text=" Ventures (55) ")
        self.ventures_text = make_text(ve_frame, height=25)
        self.ventures_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.ventures_text.tag_configure("header", foreground=ACCENT, font=("Menlo", 12, "bold"))
        self.ventures_text.tag_configure("ready", foreground=GREEN)
        self.ventures_text.tag_configure("blocked", foreground=RED)
        self.ventures_text.tag_configure("detail", foreground=FG2)

    def refresh_intelligence(self):
        # Alpha theses
        theses = self.master_ops.get("alpha_thesis", [])

        def at_content(w):
            w.insert("end", f"  ALPHA THESIS INDEX — {len(theses)} Theses\n\n", "header")
            for t in theses:
                alpha_id = str(t.get("ALPHA_ID", ""))
                opp = str(t.get("OPPORTUNITY", ""))
                lane = str(t.get("LANE", ""))
                blocker = str(t.get("BLOCKER_KEY", "") or "")
                edge = str(t.get("EDGE_DURATION", "") or "")
                tag = "blocked" if blocker else "opportunity"
                w.insert("end", f"  {alpha_id:<12} ", tag)
                w.insert("end", f"{opp}\n", tag)
                if lane or edge:
                    w.insert("end", f"              Lane: {lane}  Edge: {edge}\n", "detail")
                if blocker:
                    w.insert("end", f"              BLOCKER: {blocker}\n", "blocked")
                w.insert("end", "\n")

        write_text(self.alpha_thesis_text, at_content)

        # Synergy stacks
        synergy = self.master_ops.get("synergy", [])

        def sy_content(w):
            w.insert("end", f"  SYNERGY STACKS — {len(synergy)} Packages\n\n", "header")
            for s in synergy:
                pkg_id = str(s.get("PACKAGE_ID", ""))
                name = str(s.get("NAME", ""))
                score = s.get("SYNERGY_SCORE", 0)
                methods = str(s.get("METHODS_COMBINED", "") or "")
                mult = s.get("REVENUE_MULTIPLIER", "")
                try:
                    score_num = float(score) if score else 0
                except (ValueError, TypeError):
                    score_num = 0
                tag = "high_synergy" if score_num >= 80 else "detail"
                w.insert("end", f"  {pkg_id:<12} {name}  [Score: {score_num:.0f}]", tag)
                if mult:
                    w.insert("end", f"  [Multiplier: {mult}x]", tag)
                w.insert("end", "\n")
                if methods:
                    w.insert("end", f"              Methods: {methods[:80]}\n", "detail")
                w.insert("end", "\n")

        write_text(self.synergy_text, sy_content)

        # Ventures
        ventures = self.master_ops.get("ventures", [])

        def ve_content(w):
            w.insert("end", f"  VENTURE AUTOMATION MAP — {len(ventures)} Ventures\n\n", "header")
            for v in ventures:
                vid = str(v.get("VENTURE_ID", ""))
                name = str(v.get("VENTURE_NAME", ""))
                lane = str(v.get("LANE", ""))
                readiness = str(v.get("READINESS", ""))
                score = v.get("AUTOMATION_SCORE_100", 0)
                blocker = str(v.get("BLOCKER_KEY", "") or "")
                try:
                    score_num = float(score) if score else 0
                except (ValueError, TypeError):
                    score_num = 0
                tag = "blocked" if blocker else ("ready" if score_num >= 60 else "detail")
                w.insert("end", f"  {vid:<12} {name[:30]:<32} {lane:<12} Score: {score_num:<6.0f}", tag)
                if blocker:
                    w.insert("end", f" BLOCKER: {blocker}", "blocked")
                w.insert("end", "\n")

        write_text(self.ventures_text, ve_content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 6: TOOLS & INFRA
    # ══════════════════════════════════════════════════════════════════════

    def build_tools_infra_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Tools/Infra ")

        sub_nb = ttk.Notebook(frame)
        sub_nb.pack(fill="both", expand=True, padx=5, pady=5)

        stacks = [
            ("Video/Media", "video_stack", 28),
            ("Lead Gen", "lead_gen", 33),
            ("Hosting", "hosting", 14),
            ("Browser/Proxy", "browser_proxy", 60),
            ("Existing Infra", "existing_infra", 60),
        ]
        self.stack_texts = {}
        for label, key, count in stacks:
            sf = ttk.Frame(sub_nb)
            sub_nb.add(sf, text=f" {label} ({count}) ")
            t = make_text(sf, height=25)
            t.pack(fill="both", expand=True, padx=5, pady=5)
            t.tag_configure("header", foreground=ACCENT, font=("Menlo", 12, "bold"))
            t.tag_configure("item", foreground=FG)
            self.stack_texts[key] = t

    def refresh_tools_infra(self):
        for key, text_widget in self.stack_texts.items():
            items = self.master_ops.get(key, [])

            def make_content(w, items=items, key=key):
                w.insert("end", f"  {key.upper().replace('_', ' ')} — {len(items)} items\n\n", "header")
                if not items:
                    w.insert("end", "  No data loaded for this stack.\n")
                    return
                # show all columns for each item
                headers = list(items[0].keys()) if items else []
                for item in items:
                    first_val = str(item.get(headers[0], "")) if headers else ""
                    w.insert("end", f"  {first_val}\n", "item")
                    for h in headers[1:]:
                        val = item.get(h)
                        if val:
                            w.insert("end", f"    {h}: {val}\n")

            write_text(text_widget, make_content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 7: TASKS
    # ══════════════════════════════════════════════════════════════════════

    def build_tasks_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Tasks ")

        filter_frame = tk.Frame(frame, bg=BG)
        filter_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.task_filter = tk.StringVar(value="ALL")
        for label, val in [("All", "ALL"), ("Pending", "PENDING"), ("Active", "IN_PROGRESS"), ("Blocked", "BLOCKED"), ("Done", "DONE")]:
            rb = tk.Radiobutton(
                filter_frame, text=label, variable=self.task_filter, value=val,
                bg=BG, fg=FG, selectcolor=BG2, activebackground=BG, activeforeground=ACCENT,
                font=("Menlo", 10), command=self.refresh_tasks,
            )
            rb.pack(side="left", padx=5)

        self.task_text = make_text(frame, height=25)
        self.task_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.task_text.tag_configure("done", foreground=GREEN)
        self.task_text.tag_configure("in_progress", foreground=ACCENT)
        self.task_text.tag_configure("blocked", foreground=RED)
        self.task_text.tag_configure("pending", foreground=YELLOW)
        self.task_text.tag_configure("title", font=("Menlo", 12, "bold"))
        self.task_text.tag_configure("detail", foreground=FG2)

    def refresh_tasks(self):
        tasks = load_tasks()
        filt = self.task_filter.get()

        def content(w):
            counts = {"DONE": 0, "IN_PROGRESS": 0, "BLOCKED": 0, "PENDING": 0, "UNKNOWN": 0}
            for t in tasks:
                counts[t["status"]] = counts.get(t["status"], 0) + 1
            w.insert("end", f"  Total: {len(tasks)}  |  Done: {counts['DONE']}  |  Active: {counts['IN_PROGRESS']}  |  Blocked: {counts['BLOCKED']}  |  Pending: {counts['PENDING']}\n\n")

            for t in tasks:
                if filt != "ALL" and t["status"] != filt:
                    continue
                status_tag = t["status"].lower()
                icon = {"DONE": "[+]", "IN_PROGRESS": "[>]", "BLOCKED": "[X]", "PENDING": "[ ]"}.get(t["status"], "[?]")
                w.insert("end", f"  {icon} ", status_tag)
                w.insert("end", f"{t['id']}: {t['title']}\n", "title")
                if t["priority"]:
                    w.insert("end", f"      Priority: {t['priority']}\n", "detail")
                for d in t["details"][:3]:
                    w.insert("end", f"      {d}\n", "detail")
                w.insert("end", "\n")

        write_text(self.task_text, content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 8: PRODUCT LAUNCH
    # ══════════════════════════════════════════════════════════════════════

    def build_launch_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Launch ")

        summary_frame = tk.Frame(frame, bg=BG2, highlightbackground=BG3, highlightthickness=1)
        summary_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.launch_summary_label = tk.Label(summary_frame, text="Loading...", font=("Menlo", 12), fg=FG, bg=BG2, justify="left")
        self.launch_summary_label.pack(anchor="w", padx=10, pady=8)

        sel_frame = tk.Frame(frame, bg=BG)
        sel_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(sel_frame, text="Product:", font=("Menlo", 11), fg=FG, bg=BG).pack(side="left", padx=(0, 5))
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(sel_frame, textvariable=self.product_var, state="readonly", width=30)
        self.product_combo.pack(side="left", padx=5)
        self.product_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_launch_list())

        tk.Button(sel_frame, text="Open HIGHEST Tabs", font=("Menlo", 10), bg=PURPLE, fg=WHITE, relief="flat", command=self.open_highest_priority_tabs).pack(side="right", padx=5)
        tk.Button(sel_frame, text="Run Automator", font=("Menlo", 10), bg=GREEN, fg=BG, relief="flat", command=self.run_launch_automator).pack(side="right", padx=5)

        self.launch_text = make_text(frame, height=20)
        self.launch_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.launch_text.tag_configure("highest", foreground=RED, font=("Menlo", 11, "bold"))
        self.launch_text.tag_configure("high", foreground=ORANGE)
        self.launch_text.tag_configure("medium", foreground=YELLOW)
        self.launch_text.tag_configure("low", foreground=FG2)
        self.launch_text.tag_configure("submitted", foreground=GREEN)
        self.launch_text.tag_configure("url", foreground=ACCENT)

    def refresh_launch(self):
        entries = load_launch_tracker()
        if not entries:
            return
        products = sorted(set(e.get("product_id", "") for e in entries))
        self.product_combo["values"] = products
        if not self.product_var.get() and products:
            self.product_var.set(products[0])

        counts = {}
        for e in entries:
            s = e.get("status", "UNKNOWN")
            counts[s] = counts.get(s, 0) + 1
        total = len(entries)
        pending = counts.get("PENDING", 0)
        submitted = counts.get("SUBMITTED", 0)
        approved = counts.get("APPROVED", 0)
        self.launch_summary_label.configure(text=f"Total: {total} across {len(products)} products  |  Pending: {pending}  |  Submitted: {submitted}  |  Approved: {approved}")
        self.refresh_launch_list()

    def refresh_launch_list(self):
        entries = load_launch_tracker()
        product = self.product_var.get()

        def content(w):
            filtered = [e for e in entries if e.get("product_id") == product]
            for priority in ["HIGHEST", "HIGH", "MEDIUM", "LOW"]:
                group = [e for e in filtered if e.get("priority") == priority]
                if not group:
                    continue
                tag = priority.lower()
                w.insert("end", f"\n  [{priority}] ({len(group)} directories)\n", tag)
                for e in group:
                    status = e.get("status", "PENDING")
                    name = e.get("directory_name", "")
                    url = e.get("directory_url", "")
                    icon = "[+]" if status != "PENDING" else "[ ]"
                    stag = "submitted" if status != "PENDING" else tag
                    w.insert("end", f"    {icon} {name}", stag)
                    w.insert("end", f"  {url}\n", "url")

        write_text(self.launch_text, content)

    def open_highest_priority_tabs(self):
        product = self.product_var.get()
        entries = load_launch_tracker()
        count = 0
        for e in entries:
            if e.get("product_id") == product and e.get("priority") == "HIGHEST" and e.get("status") == "PENDING":
                url = e.get("directory_url", "")
                if url:
                    subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    count += 1
                    time.sleep(0.3)
        self.status_label.configure(text=f"Opened {count} tabs for {product}", fg=GREEN)

    def run_launch_automator(self):
        script = AUTO / "product_launch_automator.py"
        if script.exists():
            self.run_tool(f"python3 {script} --launch --product {self.product_var.get()}", "Launch Automator")

    # ══════════════════════════════════════════════════════════════════════
    # TAB 9: ALARMS
    # ══════════════════════════════════════════════════════════════════════

    def build_alarms_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Alarms ")

        add_frame = tk.Frame(frame, bg=BG2, highlightbackground=BG3, highlightthickness=1)
        add_frame.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(add_frame, text="SET ALARM", font=("Menlo", 13, "bold"), fg=ACCENT, bg=BG2).pack(anchor="w", padx=10, pady=(8, 5))

        input_frame = tk.Frame(add_frame, bg=BG2)
        input_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(input_frame, text="Time (HH:MM):", font=("Menlo", 11), fg=FG, bg=BG2).pack(side="left")
        self.alarm_time_entry = tk.Entry(input_frame, width=8, bg=BG3, fg=FG, font=("Menlo", 12), insertbackground=FG, relief="flat")
        self.alarm_time_entry.pack(side="left", padx=5)
        tk.Label(input_frame, text="Message:", font=("Menlo", 11), fg=FG, bg=BG2).pack(side="left", padx=(10, 0))
        self.alarm_msg_entry = tk.Entry(input_frame, width=40, bg=BG3, fg=FG, font=("Menlo", 12), insertbackground=FG, relief="flat")
        self.alarm_msg_entry.pack(side="left", padx=5)
        tk.Button(input_frame, text="Set", font=("Menlo", 10), bg=GREEN, fg=BG, relief="flat", command=self.add_alarm).pack(side="left", padx=10)

        quick_frame = tk.Frame(add_frame, bg=BG2)
        quick_frame.pack(fill="x", padx=10, pady=(5, 10))
        for minutes, label in [(15, "15min"), (30, "30min"), (60, "1hr"), (120, "2hr")]:
            tk.Button(quick_frame, text=label, font=("Menlo", 10), bg=BG3, fg=ACCENT, relief="flat", command=lambda m=minutes: self.add_quick_alarm(m)).pack(side="left", padx=3)

        self.alarms_text = make_text(frame, height=10)
        self.alarms_text.pack(fill="x", padx=10, pady=5)

        # hourly schedule
        tk.Label(frame, text="DAILY SCHEDULE", font=("Menlo", 11, "bold"), fg=FG2, bg=BG).pack(anchor="w", padx=10, pady=(5, 2))
        sched_text = make_text(frame, height=8)
        sched_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        sched_text.configure(state="normal")
        for hour in sorted(HOURLY_TASKS.keys()):
            sched_text.insert("end", f"  {hour:02d}:00  {HOURLY_TASKS[hour]}\n")
        sched_text.configure(state="disabled")

    def add_alarm(self):
        time_str = self.alarm_time_entry.get().strip()
        msg = self.alarm_msg_entry.get().strip()
        if not time_str or not msg:
            return
        try:
            h, m = map(int, time_str.split(":"))
            now = datetime.now()
            alarm_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if alarm_dt <= now:
                alarm_dt += timedelta(days=1)
            self.alarm_mgr.add_alarm(alarm_dt, msg)
            self.alarm_time_entry.delete(0, "end")
            self.alarm_msg_entry.delete(0, "end")
            self.refresh_alarms()
            self.status_label.configure(text=f"Alarm set for {alarm_dt.strftime('%H:%M')}", fg=GREEN)
        except Exception:
            self.status_label.configure(text="Invalid time format. Use HH:MM", fg=RED)

    def add_quick_alarm(self, minutes: int):
        alarm_dt = datetime.now() + timedelta(minutes=minutes)
        self.alarm_mgr.add_alarm(alarm_dt, f"{minutes} minute reminder")
        self.refresh_alarms()
        macos_notify("PRINTMAXX", f"Alarm set for {minutes} minutes", "Pop")
        self.status_label.configure(text=f"Alarm: {alarm_dt.strftime('%H:%M')} ({minutes}min)", fg=GREEN)

    def refresh_alarms(self):
        pending = self.alarm_mgr.get_pending()

        def content(w):
            if not pending:
                w.insert("end", "  No active alarms.\n")
            else:
                for i, a in enumerate(pending):
                    dt = a["time"].strftime("%H:%M")
                    delta = a["time"] - datetime.now()
                    mins = max(0, int(delta.total_seconds() / 60))
                    w.insert("end", f"  [{i + 1}] {dt} ({mins}min) - {a['message']}\n")

        write_text(self.alarms_text, content)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 10: QUICK LAUNCH
    # ══════════════════════════════════════════════════════════════════════

    def build_quick_launch_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Quick Launch ")

        groups = [
            ("System", [
                ("Health Check", f"python3 {AUTO}/system_health_monitor.py --quick"),
                ("Heartbeat", f"python3 {AUTO}/memory_manager.py --heartbeat"),
                ("Memory Full", f"python3 {AUTO}/memory_manager.py --full"),
                ("Venture Scores", f"python3 {AUTO}/venture_performance_tracker.py --recommend"),
            ]),
            ("Dashboard", [
                ("Web Dashboard", f"python3 {AUTO}/ops_web_dashboard.py"),
                ("Quant Terminal", f"python3 {AUTO}/printmaxx_quant_terminal.py --summary"),
                ("Pipeline", f"python3 {AUTO}/closed_loop_pipeline.py --status"),
                ("Rebalancer", f"python3 {AUTO}/auto_rebalancer.py --check"),
            ]),
            ("Research", [
                ("Twitter Scraper", f"python3 {AUTO}/twitter_alpha_scraper.py --all"),
                ("Reddit Scraper", f"python3 {AUTO}/background_reddit_scraper.py --scrape"),
                ("Alpha Processor", f"python3 {AUTO}/alpha_auto_processor.py --process-new"),
                ("Memory Search", f"python3 {AUTO}/semantic_memory_search.py --stats"),
            ]),
            ("Content", [
                ("Content Trends", f"python3 {AUTO}/content_trend_pipeline.py --status"),
                ("Compliance", f"python3 {AUTO}/compliance_scanner.py --audit-all"),
                ("Freelance Pipe", f"python3 {AUTO}/freelance_pipeline.py --daily"),
                ("Cold Email", f"python3 {AUTO}/generate_cold_emails.py --dry-run"),
            ]),
            ("Launch", [
                ("Launch Status", f"python3 {AUTO}/product_launch_automator.py --status"),
                ("SaaS Scanner", f"python3 {AUTO}/saas_product_scanner.py --scan"),
                ("App Clones", f"python3 {AUTO}/app_clone_pipeline.py --status"),
                ("Trend Scanner", f"python3 {AUTO}/trend_aggregator.py --scan"),
            ]),
        ]

        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for group_name, tools in groups:
            gf = tk.Frame(scroll_frame, bg=BG2, highlightbackground=BG3, highlightthickness=1)
            gf.pack(fill="x", padx=10, pady=3)
            tk.Label(gf, text=group_name.upper(), font=("Menlo", 11, "bold"), fg=ACCENT, bg=BG2).pack(anchor="w", padx=10, pady=(6, 3))
            btn_frame = tk.Frame(gf, bg=BG2)
            btn_frame.pack(fill="x", padx=10, pady=(0, 6))
            for tool_name, cmd in tools:
                btn = tk.Button(
                    btn_frame, text=tool_name, font=("Menlo", 10),
                    bg=BG3, fg=FG, relief="flat", width=18,
                    command=lambda c=cmd, n=tool_name: self.run_tool(c, n),
                )
                btn.pack(side="left", padx=3)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ══════════════════════════════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════════════════════════════

    def run_tool(self, cmd: str, name: str):
        apple_script = f'''
        tell application "Terminal"
            activate
            do script "cd \\"{BASE}\\" && {cmd}"
        end tell
        '''
        try:
            subprocess.Popen(["osascript", "-e", apple_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.status_label.configure(text=f"Launched: {name}", fg=GREEN)
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", fg=RED)

    # ══════════════════════════════════════════════════════════════════════
    # REFRESH
    # ══════════════════════════════════════════════════════════════════════

    def update_clock(self):
        now = datetime.now()
        self.clock_label.configure(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def refresh_all(self):
        try:
            self.refresh_dashboard()
            self.refresh_goals_tab()
            self.refresh_operations()
            self.refresh_priority()
            self.refresh_intelligence()
            self.refresh_tools_infra()
            self.refresh_tasks()
            self.refresh_launch()
            self.refresh_alarms()
        except Exception:
            pass
        self.root.after(60000, self.refresh_all)

    def refresh_dashboard(self):
        hb = load_heartbeat()

        # heartbeat text
        def hb_content(w):
            w.insert("end", f"  Last update: {hb['timestamp']}\n\n")
            for line in hb["lines"]:
                w.insert("end", f"  {line}\n")

        write_text(self.heartbeat_text, hb_content)

        # stats from heartbeat
        raw = hb.get("raw", {})
        if "hot_leads" in raw:
            self.stat_labels["Hot Leads"].configure(text=raw["hot_leads"])
        if "revenue" in raw:
            val = raw["revenue"]
            color = GREEN if val != "0" else RED
            self.stat_labels["Revenue"].configure(text=f"${val}", fg=color)
        if "alpha_pending" in raw:
            self.stat_labels["Alpha"].configure(text=raw["alpha_pending"])
        if "accounts" in raw:
            self.stat_labels["Accounts"].configure(text=raw["accounts"])
        if "apps_live" in raw:
            self.stat_labels["Apps"].configure(text=raw["apps_live"])
        if "scripts" in raw:
            self.stat_labels["Scripts"].configure(text=raw["scripts"])

        # ops + ventures count from master ops
        ops_count = len(self.master_ops.get("auto_status", []))
        vent_count = len(self.master_ops.get("ventures", []))
        self.stat_labels["Ops"].configure(text=str(ops_count))
        self.stat_labels["Ventures"].configure(text=str(vent_count))

        # motivation
        idx = int(time.time() / 120) % len(MOTIVATION)
        self.motivation_label.configure(text=f'"{MOTIVATION[idx]}"')

        # current hour task
        hour = datetime.now().hour
        if hour in HOURLY_TASKS:
            self.hour_task_label.configure(text=HOURLY_TASKS[hour])
        else:
            self.hour_task_label.configure(text="No scheduled task this hour. Build something.")

        # goals summary on dashboard
        self.daily_goals = load_daily_goals()
        goals = self.daily_goals

        def goals_content(w):
            if not goals:
                w.insert("end", "  No daily goals loaded for today.\n")
                return
            total = sum(len(g["tasks"]) for g in goals)
            done = sum(g["done_count"] for g in goals)
            pct = int(done / total * 100) if total > 0 else 0
            w.insert("end", f"  Progress: {done}/{total} ({pct}%)\n\n", "header")
            for g in goals:
                d = g["done_count"]
                t = len(g["tasks"])
                tag = "done" if d == t else "pending"
                icon = "[+]" if d == t else f"[{d}/{t}]"
                w.insert("end", f"  {icon} {g['title']}\n", tag)

        write_text(self.goals_summary_text, goals_content)


# ── main ────────────────────────────────────────────────────────────────────

def main():
    minimized = "--minimized" in sys.argv

    if minimized:
        print("PRINTMAXX reminders running in background. Ctrl+C to stop.")
        macos_notify("PRINTMAXX", "Background reminders active. Goal tracking enabled.", "Pop")
        alarm_mgr = AlarmManager()
        engine = ReminderEngine(alarm_mgr)
        engine.start()
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            engine.stop()
            print("\nPRINTMAXX reminders stopped.")
        return

    root = tk.Tk()
    try:
        root.iconphoto(False, tk.PhotoImage(data=""))
    except Exception:
        pass

    app = PrintmaxxApp(root)

    # startup notification with goal count
    goals = load_daily_goals()
    total = sum(len(g["tasks"]) for g in goals)
    done = sum(g["done_count"] for g in goals)
    macos_notify("PRINTMAXX", f"Command Center v2 active. Goals: {done}/{total} done. Ship something.", "Pop")

    def on_close():
        app.reminder_engine.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
