#!/usr/bin/env python3
"""
PRINTMAXX LLM Backend System — Multi-Provider Agent Runner

Pluggable LLM backends for the autonomous supervisor.
Primary: Codex CLI (OAuth, free with ChatGPT Pro)
Fallback 1: Kimi 2.5 API (Moonshot AI)
Fallback 2: MiniMax API

Each backend implements the same interface:
    generate(prompt, timeout_min) -> (return_code, output_text, duration_minutes)

The supervisor calls these to execute autonomous agent tasks.
"""

import subprocess
import json
import time
import os
import logging
from pathlib import Path
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

log = logging.getLogger("llm_backends")

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# BASE BACKEND
# ============================================================

class LLMBackend:
    """Base class for LLM backends."""

    name = "base"

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        """
        Send prompt to LLM and get response.
        Returns: (return_code, output_text, duration_minutes)
            return_code: 0 = success, -1 = timeout, -2 = not found, -3 = error
        """
        raise NotImplementedError

    def is_available(self) -> bool:
        """Check if this backend is configured and reachable."""
        raise NotImplementedError

    def get_model_info(self) -> dict:
        """Return info about the model being used."""
        return {"name": self.name, "model": "unknown"}


# ============================================================
# CODEX CLI BACKEND (PRIMARY)
# Uses OpenAI Codex CLI with OAuth authentication.
# Free with ChatGPT Pro subscription.
# ============================================================

class CodexBackend(LLMBackend):
    """
    OpenAI Codex CLI backend.
    Spawns `codex` process with full-auto mode.
    Uses OAuth (free with ChatGPT Pro plan).
    """

    name = "codex"

    def __init__(self, model: str = "gpt-5.3-codex", approval_mode: str = "full-auto"):
        self.model = model
        self.approval_mode = approval_mode
        self._codex_cmd = self._find_codex()

    def _find_codex(self) -> str:
        """Find the codex CLI binary."""
        # Check common locations
        for cmd in ["codex", "npx codex", "npx @openai/codex"]:
            try:
                result = subprocess.run(
                    cmd.split()[0] if " " not in cmd else ["which", cmd.split()[0]],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    return cmd
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        return "codex"  # Default, will fail gracefully

    def is_available(self) -> bool:
        """Check if codex CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                [self._codex_cmd.split()[0], "--help"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        """Spawn a codex session with the given prompt."""
        timeout_sec = timeout_min * 60
        start = time.time()

        # Build command
        cmd = self._codex_cmd.split()
        cmd.extend([
            "--approval-mode", self.approval_mode,
            "--model", self.model,
            "--quiet",
            prompt,
        ])

        log.info(f"[codex] Spawning session (model={self.model}, timeout={timeout_min}min)")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=str(PROJECT_ROOT),
                env={
                    **os.environ,
                    "CODEX_ENTRYPOINT": "autonomous_supervisor",
                },
            )
            duration = (time.time() - start) / 60
            output = result.stdout or ""
            if result.returncode != 0 and result.stderr:
                output += f"\n\nSTDERR:\n{result.stderr}"
            return result.returncode, output, duration

        except subprocess.TimeoutExpired:
            duration = timeout_min
            log.warning(f"[codex] Session timed out after {timeout_min}min")
            return -1, f"TIMEOUT after {timeout_min} minutes", duration

        except FileNotFoundError:
            log.error("[codex] 'codex' command not found. Install: npm i -g @openai/codex")
            return -2, "codex command not found", 0

        except Exception as e:
            duration = (time.time() - start) / 60
            log.error(f"[codex] Session error: {e}")
            return -3, str(e), duration

    def get_model_info(self) -> dict:
        return {"name": "codex", "model": self.model, "auth": "oauth"}


# ============================================================
# CLAUDE CLI BACKEND (ALTERNATIVE PRIMARY)
# Uses Claude Code CLI with --print mode.
# Works if claude is authenticated via `claude login`.
# ============================================================

class ClaudeBackend(LLMBackend):
    """
    Claude Code CLI backend.
    Spawns `claude --print` with dangerously-skip-permissions.
    Uses OAuth from `claude login` (works with Max plan).
    """

    name = "claude"

    def __init__(self, model: str = "sonnet"):
        self.model = model

    def is_available(self) -> bool:
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        timeout_sec = timeout_min * 60
        start = time.time()

        cmd = [
            "claude",
            "--dangerously-skip-permissions",
            "--print",
            "-p", prompt,
        ]

        log.info(f"[claude] Spawning session (timeout={timeout_min}min)")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=str(PROJECT_ROOT),
                env={**os.environ, "CLAUDE_CODE_ENTRYPOINT": "autonomous_supervisor"},
            )
            duration = (time.time() - start) / 60
            output = result.stdout or ""
            if result.returncode != 0 and result.stderr:
                output += f"\n\nSTDERR:\n{result.stderr}"
            return result.returncode, output, duration

        except subprocess.TimeoutExpired:
            return -1, f"TIMEOUT after {timeout_min} minutes", timeout_min

        except FileNotFoundError:
            log.error("[claude] 'claude' command not found")
            return -2, "claude command not found", 0

        except Exception as e:
            duration = (time.time() - start) / 60
            log.error(f"[claude] Session error: {e}")
            return -3, str(e), duration

    def get_model_info(self) -> dict:
        return {"name": "claude", "model": self.model, "auth": "oauth"}


# ============================================================
# KIMI 2.5 API BACKEND (FALLBACK 1)
# Moonshot AI's Kimi 2.5 — OpenAI-compatible API.
# Cheap/free tier available.
# ============================================================

class KimiBackend(LLMBackend):
    """
    Kimi 2.5 (Moonshot AI) API backend.
    Uses OpenAI-compatible chat completions endpoint.
    """

    name = "kimi"

    def __init__(self, api_key: str = "", model: str = "kimi-k2-0711-chat",
                 base_url: str = "https://api.moonshot.cn/v1"):
        self.api_key = api_key or os.environ.get("KIMI_API_KEY", "")
        self.model = model
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _call_api(self, messages: list, timeout_sec: int = 300) -> str:
        """Call Kimi chat completions API."""
        url = f"{self.base_url}/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 16384,
        }).encode("utf-8")

        req = Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")

        try:
            with urlopen(req, timeout=timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Kimi API error {e.code}: {body}")

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        if not self.api_key:
            return -2, "KIMI_API_KEY not set", 0

        start = time.time()
        timeout_sec = timeout_min * 60

        messages = [
            {"role": "system", "content": (
                "You are an autonomous worker agent for the PRINTMAXX project. "
                "Execute the task described below. Be specific, write real code, "
                "provide exact file paths and contents. Do NOT be vague."
            )},
            {"role": "user", "content": prompt},
        ]

        log.info(f"[kimi] Calling API (model={self.model}, timeout={timeout_min}min)")

        try:
            output = self._call_api(messages, timeout_sec=timeout_sec)
            duration = (time.time() - start) / 60
            return 0, output, duration

        except Exception as e:
            duration = (time.time() - start) / 60
            log.error(f"[kimi] API error: {e}")
            return -3, str(e), duration

    def get_model_info(self) -> dict:
        return {"name": "kimi", "model": self.model, "auth": "api_key"}


# ============================================================
# MINIMAX API BACKEND (FALLBACK 2)
# MiniMax AI — OpenAI-compatible API.
# ============================================================

class MiniMaxBackend(LLMBackend):
    """
    MiniMax API backend.
    Uses OpenAI-compatible chat completions endpoint.
    """

    name = "minimax"

    def __init__(self, api_key: str = "", model: str = "MiniMax-Text-01",
                 base_url: str = "https://api.minimax.chat/v1"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.model = model
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _call_api(self, messages: list, timeout_sec: int = 300) -> str:
        """Call MiniMax chat completions API."""
        url = f"{self.base_url}/text/chatcompletion_v2"
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 16384,
        }).encode("utf-8")

        req = Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")

        try:
            with urlopen(req, timeout=timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # MiniMax response format
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                elif "reply" in data:
                    return data["reply"]
                else:
                    return json.dumps(data)
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"MiniMax API error {e.code}: {body}")

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        if not self.api_key:
            return -2, "MINIMAX_API_KEY not set", 0

        start = time.time()
        timeout_sec = timeout_min * 60

        messages = [
            {"role": "system", "content": (
                "You are an autonomous worker agent for the PRINTMAXX project. "
                "Execute the task described below. Be specific, write real code, "
                "provide exact file paths and contents. Do NOT be vague."
            )},
            {"role": "user", "content": prompt},
        ]

        log.info(f"[minimax] Calling API (model={self.model}, timeout={timeout_min}min)")

        try:
            output = self._call_api(messages, timeout_sec=timeout_sec)
            duration = (time.time() - start) / 60
            return 0, output, duration

        except Exception as e:
            duration = (time.time() - start) / 60
            log.error(f"[minimax] API error: {e}")
            return -3, str(e), duration

    def get_model_info(self) -> dict:
        return {"name": "minimax", "model": self.model, "auth": "api_key"}


# ============================================================
# MULTI-BACKEND ROUTER
# Tries primary backend first, falls back to secondaries.
# ============================================================

class MultiBackendRouter:
    """
    Routes LLM calls through multiple backends with automatic fallback.

    Priority order (configurable — NO Claude in autonomous chain):
    1. Codex CLI (OAuth, free with ChatGPT Pro) — best available model
    2. Kimi 2.5 API (cheap, high quality)
    3. MiniMax API (cheap, fast)
    """

    def __init__(self, config: dict = None):
        self.backends = []
        self.config = config or {}
        self._setup_backends()

    def _setup_backends(self):
        """Initialize backends based on config and availability."""
        backend_order = self.config.get("backend_order", [
            "codex", "kimi", "minimax"
        ])

        backend_map = {
            "codex": lambda: CodexBackend(
                model=self.config.get("codex_model", "gpt-5.3-codex"),
                approval_mode=self.config.get("codex_approval_mode", "full-auto"),
            ),
            "claude": lambda: ClaudeBackend(
                model=self.config.get("claude_model", "sonnet"),
            ),
            "kimi": lambda: KimiBackend(
                api_key=self.config.get("kimi_api_key", ""),
                model=self.config.get("kimi_model", "kimi-k2-0711-chat"),
            ),
            "minimax": lambda: MiniMaxBackend(
                api_key=self.config.get("minimax_api_key", ""),
                model=self.config.get("minimax_model", "MiniMax-Text-01"),
            ),
        }

        for name in backend_order:
            if name in backend_map:
                try:
                    backend = backend_map[name]()
                    self.backends.append(backend)
                    log.info(f"Backend registered: {name} (available={backend.is_available()})")
                except Exception as e:
                    log.warning(f"Failed to init backend {name}: {e}")

        if not self.backends:
            log.error("No LLM backends available!")

    def generate(self, prompt: str, timeout_min: int = 30) -> tuple:
        """
        Try each backend in priority order.
        Returns (return_code, output, duration) from first successful backend.
        Also returns which backend was used via output prefix.
        """
        errors = []

        for backend in self.backends:
            if not backend.is_available():
                log.debug(f"Skipping {backend.name} (not available)")
                continue

            log.info(f"Trying backend: {backend.name}")
            code, output, duration = backend.generate(prompt, timeout_min)

            if code == 0:
                # Success
                log.info(f"Backend {backend.name} succeeded in {duration:.1f}min")
                return code, f"[{backend.name}] {output}", duration

            elif code == -1:
                # Timeout — don't retry on different backend
                log.warning(f"Backend {backend.name} timed out")
                return code, f"[{backend.name}] {output}", duration

            elif code == -2:
                # Backend not found — try next
                log.info(f"Backend {backend.name} not installed, trying next")
                errors.append(f"{backend.name}: not found")
                continue

            else:
                # Other error — try next backend
                log.warning(f"Backend {backend.name} failed (code={code}), trying next")
                errors.append(f"{backend.name}: {output[:200]}")
                continue

        # All backends failed
        error_summary = " | ".join(errors) if errors else "No backends available"
        log.error(f"All backends failed: {error_summary}")
        return -3, f"ALL_BACKENDS_FAILED: {error_summary}", 0

    def get_available_backends(self) -> list:
        """Return list of available backend names."""
        return [b.name for b in self.backends if b.is_available()]

    def get_status(self) -> dict:
        """Return status of all backends."""
        return {
            b.name: {
                "available": b.is_available(),
                "info": b.get_model_info(),
            }
            for b in self.backends
        }


# ============================================================
# TOOL-USE AGENT LOOP
# For API-based backends that don't have built-in tool use.
# Wraps the LLM in a read-plan-act loop.
# ============================================================

class ToolUseAgent:
    """
    Wraps an API-based LLM backend with a tool-use loop.
    The LLM can request file reads, writes, and command execution.

    Used when the backend is an API (Kimi, MiniMax) rather than
    a CLI with built-in tool use (Codex, Claude).
    """

    TOOL_SYSTEM_PROMPT = """You are an autonomous worker agent. You can use these tools:

## Available Tools

To use a tool, output a JSON block like this:
```tool
{"tool": "read_file", "path": "OPS/HEARTBEAT.md"}
```

Available tools:
1. read_file(path) - Read a file. Path relative to project root.
2. write_file(path, content) - Write content to a file.
3. list_files(directory) - List files in a directory.
4. run_python(script_path, args) - Run a Python script. Args is a string.
5. done(summary) - Signal that you're done. Include a summary of what you did.

## Rules
- All file paths are relative to the PRINTMAXX project root
- You CANNOT write outside the project folder
- You CANNOT run git push, rm -rf, or destructive commands
- You CANNOT modify CLAUDE.md, SECRETS/, or .env files
- Complete the task, then call done() with a summary

## Your Task
"""

    def __init__(self, backend: LLMBackend, max_iterations: int = 20):
        self.backend = backend
        self.max_iterations = max_iterations

    def _parse_tool_calls(self, response: str) -> list:
        """Extract tool calls from LLM response."""
        import re
        calls = []
        # Match ```tool ... ``` blocks
        pattern = r'```tool\s*\n(.*?)\n```'
        matches = re.findall(pattern, response, re.DOTALL)
        for match in matches:
            try:
                call = json.loads(match.strip())
                if isinstance(call, dict) and "tool" in call:
                    calls.append(call)
            except json.JSONDecodeError:
                continue
        return calls

    def _execute_tool(self, call: dict) -> str:
        """Execute a single tool call with guardrails."""
        tool = call.get("tool", "")

        if tool == "read_file":
            path = PROJECT_ROOT / call.get("path", "")
            if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
                return "ERROR: Path outside project root"
            if not path.exists():
                return f"ERROR: File not found: {call.get('path')}"
            try:
                content = path.read_text()
                if len(content) > 50000:
                    content = content[:50000] + "\n\n[TRUNCATED — file too large]"
                return content
            except Exception as e:
                return f"ERROR: {e}"

        elif tool == "write_file":
            path = PROJECT_ROOT / call.get("path", "")
            if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
                return "ERROR: Path outside project root"
            # Check protected files
            protected = ["CLAUDE.md", "SECRETS/", ".env", ".claude/rules/"]
            for p in protected:
                if p in str(call.get("path", "")):
                    return f"ERROR: Cannot modify protected file: {p}"
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(call.get("content", ""))
                return f"OK: Written to {call.get('path')}"
            except Exception as e:
                return f"ERROR: {e}"

        elif tool == "list_files":
            directory = call.get("directory", call.get("path", "."))
            path = PROJECT_ROOT / directory
            if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
                return "ERROR: Path outside project root"
            if not path.exists():
                return f"ERROR: Directory not found: {directory}"
            try:
                entries = sorted(path.iterdir())[:100]  # Limit
                return "\n".join(
                    f"{'[DIR] ' if e.is_dir() else ''}{e.name}"
                    for e in entries
                )
            except Exception as e:
                return f"ERROR: {e}"

        elif tool == "run_python":
            script = call.get("script_path", call.get("path", ""))
            args = call.get("args", "")
            script_path = PROJECT_ROOT / script
            if not str(script_path.resolve()).startswith(str(PROJECT_ROOT)):
                return "ERROR: Script path outside project root"
            if not script_path.exists():
                return f"ERROR: Script not found: {script}"
            try:
                cmd = ["python3", str(script_path)]
                if args:
                    cmd.extend(args.split())
                result = subprocess.run(
                    cmd, capture_output=True, text=True,
                    timeout=300, cwd=str(PROJECT_ROOT)
                )
                output = result.stdout[:10000]
                if result.stderr:
                    output += f"\nSTDERR:\n{result.stderr[:5000]}"
                return output
            except subprocess.TimeoutExpired:
                return "ERROR: Script timed out after 300s"
            except Exception as e:
                return f"ERROR: {e}"

        elif tool == "done":
            return "DONE"

        else:
            return f"ERROR: Unknown tool: {tool}"

    def run(self, task_prompt: str, timeout_min: int = 30) -> tuple:
        """
        Run the tool-use agent loop.
        Returns (return_code, output_text, duration_minutes).
        """
        start = time.time()
        full_prompt = self.TOOL_SYSTEM_PROMPT + task_prompt
        conversation = full_prompt
        all_outputs = []

        for iteration in range(self.max_iterations):
            elapsed = (time.time() - start) / 60
            if elapsed >= timeout_min:
                all_outputs.append(f"\n[TIMEOUT after {timeout_min} min]")
                return -1, "\n".join(all_outputs), timeout_min

            # Call LLM
            code, response, _ = self.backend.generate(conversation, timeout_min=5)
            if code != 0:
                all_outputs.append(f"\n[LLM ERROR: {response}]")
                return code, "\n".join(all_outputs), elapsed

            # Remove backend prefix if present
            if response.startswith("["):
                bracket_end = response.find("] ")
                if bracket_end > 0:
                    response = response[bracket_end + 2:]

            all_outputs.append(f"\n--- Iteration {iteration + 1} ---\n{response[:2000]}")

            # Parse tool calls
            tool_calls = self._parse_tool_calls(response)

            if not tool_calls:
                # No tool calls — LLM is done (or confused)
                all_outputs.append("\n[No tool calls — agent finished]")
                duration = (time.time() - start) / 60
                return 0, "\n".join(all_outputs), duration

            # Execute tools
            tool_results = []
            for call in tool_calls:
                result = self._execute_tool(call)
                if result == "DONE":
                    summary = call.get("summary", "Task completed")
                    all_outputs.append(f"\n[DONE] {summary}")
                    duration = (time.time() - start) / 60
                    return 0, "\n".join(all_outputs), duration
                tool_results.append(f"Tool: {call.get('tool')} -> {result[:2000]}")

            # Build next prompt with tool results
            conversation = (
                full_prompt +
                "\n\n## Previous Actions\n" +
                "\n".join(all_outputs[-3:]) +  # Last 3 iterations for context
                "\n\n## Tool Results\n" +
                "\n\n".join(tool_results) +
                "\n\nContinue executing the task. Use tools or call done() when finished."
            )

        # Max iterations reached
        all_outputs.append(f"\n[MAX ITERATIONS ({self.max_iterations}) reached]")
        duration = (time.time() - start) / 60
        return 0, "\n".join(all_outputs), duration


# ============================================================
# FACTORY FUNCTION
# ============================================================

def create_router(config: dict = None) -> MultiBackendRouter:
    """Create a multi-backend router from config."""
    return MultiBackendRouter(config or {})


def create_agent(backend: LLMBackend, max_iterations: int = 20) -> ToolUseAgent:
    """Create a tool-use agent wrapping an API backend."""
    return ToolUseAgent(backend, max_iterations)


# ============================================================
# CLI — Quick test
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Backend System")
    parser.add_argument("--status", action="store_true", help="Show backend status")
    parser.add_argument("--test", type=str, help="Test a specific backend (codex|claude|kimi|minimax)")
    parser.add_argument("--prompt", type=str, default="Say hello and confirm you're working.", help="Test prompt")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    router = create_router()

    if args.status:
        print("\n" + "=" * 50)
        print("  LLM BACKEND STATUS")
        print("=" * 50)
        status = router.get_status()
        for name, info in status.items():
            avail = "READY" if info["available"] else "NOT AVAILABLE"
            print(f"\n  {name}: {avail}")
            for k, v in info["info"].items():
                print(f"    {k}: {v}")
        available = router.get_available_backends()
        print(f"\n  Active chain: {' -> '.join(available) if available else 'NONE'}")
        print("=" * 50 + "\n")

    elif args.test:
        backend_map = {
            "codex": CodexBackend,
            "claude": ClaudeBackend,
            "kimi": KimiBackend,
            "minimax": MiniMaxBackend,
        }
        if args.test not in backend_map:
            print(f"Unknown backend: {args.test}")
            print(f"Available: {', '.join(backend_map.keys())}")
        else:
            backend = backend_map[args.test]()
            print(f"\nTesting {args.test} backend...")
            print(f"Available: {backend.is_available()}")
            if backend.is_available():
                code, output, dur = backend.generate(args.prompt, timeout_min=2)
                print(f"Return code: {code}")
                print(f"Duration: {dur:.1f} min")
                print(f"Output:\n{output[:500]}")
            else:
                print("Backend not available. Check installation/credentials.")
    else:
        parser.print_help()
