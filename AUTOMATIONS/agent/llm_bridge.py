#!/usr/bin/env python3
"""
PRINTMAXX LLM Bridge — Auto-conversation between Claude Code & OpenAI
======================================================================
Reads from the shared chat bus, detects messages addressed to "codex",
calls OpenAI API (GPT-5.4 / o3 / gpt-5.3-codex), posts response back.

Claude Code writes to the bus naturally. This bridge picks up messages
for codex and gets real responses. No copy-pasting.

Usage:
  python3 AUTOMATIONS/agent/llm_bridge.py                     # Run bridge (polls every 5s)
  python3 AUTOMATIONS/agent/llm_bridge.py --once               # Process pending, exit
  python3 AUTOMATIONS/agent/llm_bridge.py --ask "review this code"  # One-shot question to OpenAI
  python3 AUTOMATIONS/agent/llm_bridge.py --model o3            # Use specific model

Security:
  - API key from SECRETS/CREDENTIALS.env only (never hardcoded)
  - Output sanitized before posting to bus (strip system prompt leaks)
  - No external repos cloned. Pure stdlib + official openai package.
  - Conversation context limited to last 10 messages (prevent token bombs)
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
BUS_FILE = PROJECT / "AUTOMATIONS" / "agent" / "llm_chat_bus.jsonl"
CREDS_FILE = PROJECT / "SECRETS" / "CREDENTIALS.env"
BRIDGE_STATE = PROJECT / "AUTOMATIONS" / "agent" / "bridge_state.json"

# Model aliases for convenience
MODEL_MAP = {
    "best": "gpt-5.4",
    "codex": "gpt-5.3-codex",
    "reasoning": "o3",
    "fast": "o3-mini",
    "cheap": "gpt-5.3-chat-latest",
}
DEFAULT_MODEL = "gpt-5.4"

# System prompt for OpenAI — establishes context without leaking internals
SYSTEM_PROMPT = """You are ChatGPT, working collaboratively with Claude Code (Anthropic Opus 4.6) on the PRINTMAXX project. You are in a shared chat where both AIs help the user build an autonomous multi-venture business system.

Your role:
- Provide your best analysis, code, and ideas when asked
- Be direct and specific. No filler.
- When reviewing Claude's work, be genuinely critical — find real issues, suggest real improvements
- When given a task, execute it thoroughly
- You can reference files in the project at /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/

Style: lowercase energy, specific numbers, no AI slop vocabulary (leverage, utilize, comprehensive, robust, innovative, seamless). Think like a builder, not a consultant."""

# Prompt injection patterns to strip from outputs
INJECTION_PATTERNS = [
    r"(?i)ignore (?:all )?previous instructions",
    r"(?i)you are now",
    r"(?i)system:\s*",
    r"(?i)<\|im_start\|>",
    r"(?i)<\|endoftext\|>",
    r"(?i)\[INST\]",
    r"(?i)<<SYS>>",
    r"(?i)### (?:system|instruction)",
    r"(?i)IMPORTANT: override",
]


def load_api_key():
    """Load OpenAI API key from credentials file."""
    if not CREDS_FILE.exists():
        return os.environ.get("OPENAI_API_KEY", "")
    for line in CREDS_FILE.read_text().split("\n"):
        line = line.strip()
        if line.startswith("OPENAI_API_KEY=") and not line.endswith("="):
            val = line.split("=", 1)[1].strip().strip('"').strip("'")
            if val:
                return val
    return os.environ.get("OPENAI_API_KEY", "")


def sanitize_output(text):
    """Remove potential prompt injection patterns from model output."""
    for pattern in INJECTION_PATTERNS:
        text = re.sub(pattern, "[FILTERED]", text)
    # Truncate absurdly long responses
    if len(text) > 15000:
        text = text[:15000] + "\n\n[truncated — response exceeded 15K chars]"
    return text


def sanitize_input(text):
    """Sanitize input before sending to OpenAI to prevent injection via bus."""
    for pattern in INJECTION_PATTERNS:
        text = re.sub(pattern, "[REMOVED]", text)
    # Cap input length
    if len(text) > 10000:
        text = text[:10000] + "\n[truncated]"
    return text


def get_messages(n=200):
    if not BUS_FILE.exists():
        return []
    msgs = []
    for line in BUS_FILE.read_text().strip().split("\n")[-n:]:
        try:
            msgs.append(json.loads(line))
        except Exception:
            pass
    return msgs


def post_message(sender, body, recipient="all"):
    msg = {"ts": datetime.now().isoformat(), "from": sender, "to": recipient, "body": body}
    with open(BUS_FILE, "a") as f:
        f.write(json.dumps(msg) + "\n")
    return msg


def get_last_processed_ts():
    if BRIDGE_STATE.exists():
        try:
            return json.loads(BRIDGE_STATE.read_text()).get("last_ts", "")
        except Exception:
            pass
    return ""


def save_last_processed_ts(ts):
    BRIDGE_STATE.write_text(json.dumps({"last_ts": ts, "updated": datetime.now().isoformat()}))


def build_conversation_context(messages, max_msgs=10):
    """Build OpenAI conversation from recent bus messages."""
    conv = [{"role": "system", "content": SYSTEM_PROMPT}]
    recent = messages[-max_msgs:]
    for m in recent:
        sender = m.get("from", "user")
        body = sanitize_input(m.get("body", ""))
        if sender == "codex":
            conv.append({"role": "assistant", "content": body})
        else:
            label = {"claude": "Claude Code", "user": "User", "local": "Local LLM"}.get(sender, sender)
            conv.append({"role": "user", "content": f"[{label}]: {body}"})
    return conv


def call_openai(messages, model=DEFAULT_MODEL, api_key=""):
    """Call OpenAI API. Returns (success, response_text)."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
        )
        text = response.choices[0].message.content
        return True, sanitize_output(text)
    except ImportError:
        return _call_openai_raw(messages, model, api_key)
    except Exception as e:
        return False, f"OpenAI API error: {e}"


def _call_openai_raw(messages, model, api_key):
    """Fallback: call OpenAI with urllib if openai package fails."""
    import urllib.request
    import urllib.error
    url = "https://api.openai.com/v1/chat/completions"
    data = json.dumps({"model": model, "messages": messages, "max_tokens": 4096, "temperature": 0.7}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
            text = result["choices"][0]["message"]["content"]
            return True, sanitize_output(text)
    except Exception as e:
        return False, f"Raw API error: {e}"


def process_pending(model=DEFAULT_MODEL, api_key=""):
    """Find messages addressed to codex that haven't been answered yet."""
    messages = get_messages()
    last_ts = get_last_processed_ts()

    # Find messages to codex that came after our last processed timestamp
    pending = []
    for m in messages:
        if m["ts"] > last_ts and m.get("to") in ("codex", "all") and m.get("from") != "codex":
            pending.append(m)

    if not pending:
        return 0

    # Build conversation context from ALL recent messages (not just pending)
    conv = build_conversation_context(messages, max_msgs=10)

    # Call OpenAI
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing {len(pending)} message(s) -> {model}")
    ok, response = call_openai(conv, model=model, api_key=api_key)

    if ok:
        post_message("codex", response, "all")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Codex responded ({len(response)} chars)")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {response}")
        post_message("codex", f"[Bridge error: {response}]", "all")

    # Update state to latest message timestamp
    save_last_processed_ts(messages[-1]["ts"])
    return len(pending)


def daemon_loop(model=DEFAULT_MODEL, api_key="", interval=5):
    """Poll the bus every N seconds for new messages to codex."""
    print(f"LLM Bridge running — model={model}, polling every {interval}s")
    print(f"Watching: {BUS_FILE}")
    print("Send messages to 'codex' in the chat and they'll be auto-answered.")
    print("Ctrl+C to stop\n")

    while True:
        try:
            process_pending(model=model, api_key=api_key)
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in loop: {e}")
        time.sleep(interval)


def one_shot(question, model=DEFAULT_MODEL, api_key=""):
    """Ask OpenAI a single question, post to bus."""
    post_message("claude", question, "codex")
    messages = get_messages()
    conv = build_conversation_context(messages, max_msgs=5)
    ok, response = call_openai(conv, model=model, api_key=api_key)
    if ok:
        post_message("codex", response, "all")
        print(response)
    else:
        print(f"ERROR: {response}")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX LLM Bridge")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Model to use. Aliases: {', '.join(MODEL_MAP.keys())}")
    parser.add_argument("--once", action="store_true", help="Process pending and exit")
    parser.add_argument("--ask", type=str, help="One-shot question to OpenAI")
    parser.add_argument("--interval", type=int, default=5, help="Poll interval in seconds")
    args = parser.parse_args()

    # Resolve model alias
    model = MODEL_MAP.get(args.model, args.model)

    # Load API key
    api_key = load_api_key()
    if not api_key:
        print("ERROR: No OpenAI API key found.")
        print(f"Set it in {CREDS_FILE} as OPENAI_API_KEY=sk-...")
        print("Or export OPENAI_API_KEY=sk-... in your shell")
        sys.exit(1)

    print(f"API key loaded ({api_key[:8]}...{api_key[-4:]})")
    print(f"Model: {model}")

    if args.ask:
        one_shot(args.ask, model=model, api_key=api_key)
    elif args.once:
        n = process_pending(model=model, api_key=api_key)
        print(f"Processed {n} message(s)")
    else:
        daemon_loop(model=model, api_key=api_key, interval=args.interval)


if __name__ == "__main__":
    main()
