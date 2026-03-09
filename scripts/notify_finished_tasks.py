#!/usr/bin/env python3
"""Notify when background evaluation tasks finish.

Scans for running python processes whose cmdline matches known eval scripts.
Keeps a small state file to remember which PIDs were running.
When a previously-known PID disappears, send a Telegram notification via OpenClaw message tool.

Env:
- OPENCLAW_BIN: path to openclaw CLI (default: ~/.npm-global/bin/openclaw)
- OPENCLAW_NOTIFY_TO: optional target for message (e.g. telegram:8284141351); if unset, send to main direct session.

State file: ~/.openclaw/workspace/.background_tasks_state.json
Format: {"pids": {"<pid>": {"cmd": "...", "started": <ts>}}}
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Set

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / ".background_tasks_state.json"

OPENCLAW_BIN = os.getenv("OPENCLAW_BIN", str(Path.home() / ".npm-global/bin/openclaw"))

# Patterns to recognize eval tasks (adjust as needed)
EVAL_PATTERNS = [
    "eval_himalaya_multi_pairs_strict.py",
    "eval_himalaya_multi_readonly.py",
    "eval_himalaya_pairs_readonly.py",
    "eval_real_email_pairs_readonly.py",
]


def _load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {"pids": {}}
    return {"pids": {}}


def _save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def _get_running_pids() -> Set[int]:
    pids: Set[int] = set()
    try:
        out = subprocess.check_output(["ps", "aux"], text=True, errors="ignore")
    except Exception:
        return pids
    for line in out.splitlines():
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        pid_str, cmd = parts[1], parts[10]
        for pat in EVAL_PATTERNS:
            if pat in cmd:
                try:
                    pids.add(int(pid_str))
                except Exception:
                    continue
                break
    return pids


def _find_main_session_key() -> str:
    """Return the most recent direct session key for agent 'main'."""
    try:
        import subprocess, json
        out = subprocess.check_output(
            ["openclaw", "sessions", "list", "--kinds", "direct", "--limit", "10", "--json"],
            stderr=subprocess.DEVNULL,
            timeout=30,
            text=True,
        )
        data = json.loads(out)
        for s in data.get("sessions", []):
            if s.get("agentId") == "main":
                return s["key"]
    except Exception:
        pass
    return ""


def _notify_done(pid: int, info: Dict[str, Any]) -> None:
    """Send a Telegram notification that the task finished."""
    cmd_short = info.get("cmd", "")[:80]
    started = info.get("started", 0)
    age_min = int((time.time() - started) / 60) if started else 0
    text = (
        f"✅ Background task finished:\n"
        f"PID: {pid}\n"
        f"Command: {cmd_short}\n"
        f"Duration: ~{age_min} min"
    )

    notify_to = os.getenv("OPENCLAW_NOTIFY_TO", "").strip()  # e.g. telegram:8284141351 or channel name

    if notify_to:
        # Send directly via message send
        try:
            subprocess.run(
                [OPENCLAW_BIN, "message", "send", "--target", notify_to, "--message", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            return
        except Exception:
            pass

    # Fallback: send to main direct session
    session_key = _find_main_session_key()
    if session_key:
        try:
            subprocess.run(
                [OPENCLAW_BIN, "sessions", "send", "--sessionKey", session_key, "--message", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            return
        except Exception:
            pass

    # Fallback: print to stdout (cron log)
    print(text)


def main() -> int:
    state = _load_state()
    known_pids = set(int(pid) for pid in state.get("pids", {}) if str(pid).isdigit())
    current_pids = _get_running_pids()

    # PIDs that disappeared
    finished = known_pids - current_pids
    for pid in finished:
        info = state["pids"].get(str(pid), {})
        _notify_done(pid, info)

    # Update state: keep only currently running
    new_pids = {}
    for pid in current_pids:
        info = state["pids"].get(str(pid), {})
        # Ensure we have start time; if missing, set now.
        if not info:
            info = {"cmd": "(unknown)", "started": int(time.time())}
        new_pids[str(pid)] = info
    state["pids"] = new_pids
    _save_state(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
