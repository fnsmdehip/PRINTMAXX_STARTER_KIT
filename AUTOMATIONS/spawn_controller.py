#!/usr/bin/env python3
"""Intelligent spawn controller for claude -p calls.

Usage in any script that calls claude -p:

    from spawn_controller import SpawnController
    sc = SpawnController("auto_approve")

    # Check if we should even run
    if not sc.should_run():
        print("Skipped — no new data or daily budget exhausted")
        sys.exit(0)

    # Get how many items to process
    max_items = sc.get_batch_size(total_pending=len(pending_items))
    items_to_process = pending_items[:max_items]

    # Before each claude -p call
    if not sc.can_call():
        print("Daily budget exhausted")
        break

    # After each call
    sc.record_call()

    # Get the right model
    model = sc.model  # returns "sonnet", "haiku", or "opus"
"""

import json
import os
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "agent" / "spawn_config.json"


class SpawnController:
    def __init__(self, script_name: str):
        self.script_name = script_name
        self.config = self._load_config()
        self.script_config = self.config.get("scripts", {}).get(script_name, {})
        self.global_config = self.config.get("global", {})
        self._reset_daily_counter()

    def _load_config(self) -> dict:
        if CONFIG_PATH.exists():
            try:
                return json.loads(CONFIG_PATH.read_text())
            except Exception:
                pass
        return {"global": {"max_daily_calls": 200, "calls_today": 0, "last_reset": "", "budget_mode": "standard"}, "scripts": {}}

    def _reset_daily_counter(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.global_config.get("last_reset") != today:
            self.global_config["calls_today"] = 0
            self.global_config["last_reset"] = today
            self._save()

    def _save(self):
        try:
            self.config["global"] = self.global_config
            CONFIG_PATH.write_text(json.dumps(self.config, indent=2))
        except Exception:
            pass

    @property
    def model(self) -> str:
        return self.script_config.get("model", "sonnet")

    @property
    def budget_mode(self) -> str:
        return self.global_config.get("budget_mode", "standard")

    def should_run(self) -> bool:
        """Check if this script should run at all."""
        # Check if disabled in current budget mode
        mode = self.budget_mode
        modes = self.config.get("budget_modes", {})
        if mode in modes:
            disabled = modes[mode].get("disabled_scripts", [])
            if self.script_name in disabled:
                return False

        # Check daily budget
        max_daily = self.global_config.get("max_daily_calls", 200)
        if mode in modes:
            max_daily = modes[mode].get("max_daily_calls", max_daily)
        if self.global_config.get("calls_today", 0) >= max_daily:
            return False

        return True

    def get_batch_size(self, total_pending: int) -> int:
        """Calculate how many items to process based on config and data volume."""
        if not self.script_config:
            return min(total_pending, 10)

        mode = self.script_config.get("spawn_mode", "fixed")
        max_calls = self.script_config.get("max_calls", 10)
        min_calls = self.script_config.get("min_calls", 1)
        batch_size = self.script_config.get("batch_size", 1)
        skip_below = self.script_config.get("skip_if_below", 0)

        if total_pending < skip_below:
            return 0

        if mode == "fixed":
            return min(max_calls, total_pending)

        # Variable mode: scale calls by data volume
        calls_needed = max(min_calls, (total_pending + batch_size - 1) // batch_size)
        calls_allowed = min(calls_needed, max_calls)

        # Also check remaining daily budget
        remaining_daily = self.global_config.get("max_daily_calls", 200) - self.global_config.get("calls_today", 0)
        calls_allowed = min(calls_allowed, remaining_daily)

        return max(0, calls_allowed * batch_size)

    def can_call(self) -> bool:
        """Check if we can make another claude -p call."""
        max_daily = self.global_config.get("max_daily_calls", 200)
        mode = self.budget_mode
        modes = self.config.get("budget_modes", {})
        if mode in modes:
            max_daily = modes[mode].get("max_daily_calls", max_daily)
        return self.global_config.get("calls_today", 0) < max_daily

    def record_call(self):
        """Record that a claude -p call was made."""
        self.global_config["calls_today"] = self.global_config.get("calls_today", 0) + 1
        self._save()

    def get_model_for_task(self, task_type: str) -> str:
        """Get the recommended model for a specific task type."""
        routing = self.config.get("model_routing", {})
        return routing.get(task_type, self.model)

    def status(self) -> dict:
        """Return current spawn status for this script."""
        return {
            "script": self.script_name,
            "model": self.model,
            "budget_mode": self.budget_mode,
            "calls_today": self.global_config.get("calls_today", 0),
            "max_daily": self.global_config.get("max_daily_calls", 200),
            "spawn_mode": self.script_config.get("spawn_mode", "unknown"),
            "max_calls": self.script_config.get("max_calls", "?"),
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sc = SpawnController(sys.argv[1])
        print(json.dumps(sc.status(), indent=2))
    else:
        print("Usage: python3 spawn_controller.py <script_name>")
        print("\nGlobal status:")
        sc = SpawnController("_global")
        print(f"  Budget mode: {sc.budget_mode}")
        print(f"  Calls today: {sc.global_config.get('calls_today', 0)}")
        print(f"  Max daily: {sc.global_config.get('max_daily_calls', 200)}")
        print(f"  Scripts configured: {list(sc.config.get('scripts', {}).keys())}")
