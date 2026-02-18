#!/usr/bin/env python3
"""Render approved longform/video scripts into voice assets.

Primary path:
- Local Qwen3-TTS renderer (`scripts/qwen3_tts_longform.sh`).

Fallback path:
- ElevenLabs API only when local render fails.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent.parent
QA_DIR = ROOT / "OPS" / "CONTENT_QA_QUEUE"
QUEUE_CSV = ROOT / "OPS" / "VOICEOVER_APPROVED_QUEUE.csv"
QWEN_WRAPPER = ROOT / "scripts" / "qwen3_tts_longform.sh"
OUTPUT_DIR = ROOT / "output" / "qwen_tts" / "approved"
LEDGER_CSV = ROOT / "LEDGER" / "VOICE_RENDER_RUNS.csv"
STATE_PATH = ROOT / "AUTOMATIONS" / "voice_pipeline_state.json"
LOCK_PATH = ROOT / "AUTOMATIONS" / ".voice_pipeline.lock"

VIDEO_HINTS = (
    "youtube",
    "video",
    "shorts",
    "reels",
    "tiktok",
    "faceless",
    "voiceover",
    "narration",
)


@dataclass
class Job:
    source_kind: str
    status: str
    source_file: str
    qa_file: str = ""
    platform: str = ""
    content_type: str = ""
    title: str = ""
    speaker: str = ""
    language: str = ""


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def slugify(text: str, limit: int = 96) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", (text or "").strip().lower()).strip("-")
    return (value or "voice-script")[:limit]


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def ensure_within_root(path_value: str) -> Optional[Path]:
    if not path_value:
        return None
    p = Path(path_value.strip())
    resolved = p if p.is_absolute() else (ROOT / p)
    try:
        safe = resolved.resolve()
    except Exception:
        return None
    if str(safe).startswith(str(ROOT.resolve())):
        return safe
    return None


def read_frontmatter(md_text: str) -> Dict[str, str]:
    m = re.match(r"(?s)\A---\n(.*?)\n---\n", md_text)
    if not m:
        return {}
    data: Dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip().lower()] = value.strip()
    return data


def looks_like_video_content(*, platform: str, content_type: str, source_file: str) -> bool:
    hay = " ".join([platform or "", content_type or "", source_file or ""]).lower()
    return any(h in hay for h in VIDEO_HINTS)


def discover_qa_jobs() -> List[Job]:
    jobs: List[Job] = []
    if not QA_DIR.exists():
        return jobs
    for qa_path in sorted(QA_DIR.glob("QA_*.md")):
        text = qa_path.read_text(encoding="utf-8", errors="replace")
        fm = read_frontmatter(text)
        status = (fm.get("status") or "").strip().upper()
        source_file = (fm.get("source_file") or "").strip()
        if not source_file:
            continue
        job = Job(
            source_kind="qa",
            status=status,
            source_file=source_file,
            qa_file=str(qa_path.relative_to(ROOT)),
            platform=(fm.get("platform") or "").strip(),
            content_type=(fm.get("content_type") or "").strip(),
            title=qa_path.stem,
        )
        jobs.append(job)
    return jobs


def ensure_queue_csv_exists() -> None:
    if QUEUE_CSV.exists():
        return
    QUEUE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["status", "source_file", "title", "speaker", "language", "notes"])
        writer.writerow(["PENDING_REVIEW", "CONTENT/YOUTUBE_SCRIPTS_30.md", "youtube batch", "aiden", "English", "set APPROVED when ready"])


def discover_queue_jobs() -> List[Job]:
    jobs: List[Job] = []
    ensure_queue_csv_exists()
    with QUEUE_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_file = (row.get("source_file") or "").strip()
            if not source_file:
                continue
            jobs.append(
                Job(
                    source_kind="queue",
                    status=(row.get("status") or "").strip().upper(),
                    source_file=source_file,
                    title=(row.get("title") or "").strip(),
                    speaker=(row.get("speaker") or "").strip(),
                    language=(row.get("language") or "").strip(),
                )
            )
    return jobs


def extract_quoted_narration(text: str) -> str:
    matches = re.findall(r'"([^"\n][^"]{24,})"', text, flags=re.MULTILINE)
    cleaned = [normalize_spaces(m) for m in matches if len(normalize_spaces(m)) >= 20]
    return "\n\n".join(cleaned)


def markdown_to_plain(text: str) -> str:
    body = re.sub(r"(?s)\A---\n.*?\n---\n", "", text)
    body = re.sub(r"(?s)```.*?```", "", body)
    lines: List[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("*(") or (line.startswith("(") and line.endswith(")")):
            continue
        if line.startswith(("-", "*", "|")):
            continue
        if line.startswith("**") and line.endswith("**"):
            continue
        if re.match(r"^\[[0-9:.\-]+\]", line):
            continue
        lines.append(line)
    return "\n\n".join(lines)


def extract_script_blocks(source_text: str, source_hint: str, max_chars: int) -> List[Tuple[str, str, str]]:
    blocks: List[Tuple[str, str, str]] = []
    pattern = re.compile(
        r"(?ms)^###\s+VIDEO\s+(\d+):\s*(.+?)\n(.*?)(?=^###\s+VIDEO\s+\d+:|\Z)"
    )
    for m in pattern.finditer(source_text):
        idx = m.group(1).strip()
        title = normalize_spaces(m.group(2))
        block_text = m.group(3)
        narration = extract_quoted_narration(block_text)
        if not narration:
            narration = markdown_to_plain(block_text)
        narration = narration[:max_chars].strip()
        if narration:
            blocks.append((f"video{idx}", title or f"video-{idx}", narration))

    if blocks:
        return blocks

    narration = extract_quoted_narration(source_text)
    if not narration:
        narration = markdown_to_plain(source_text)
    narration = narration[:max_chars].strip()
    if narration:
        blocks.append(("full", source_hint, narration))
    return blocks


def load_state() -> Dict[str, object]:
    if not STATE_PATH.exists():
        return {"completed": {}}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"completed": {}}
    if not isinstance(data, dict):
        return {"completed": {}}
    if "completed" not in data or not isinstance(data["completed"], dict):
        data["completed"] = {}
    return data


def save_state(state: Dict[str, object]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ensure_ledger() -> None:
    if LEDGER_CSV.exists():
        return
    LEDGER_CSV.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "generated_at",
                "status",
                "backend",
                "source_kind",
                "qa_file",
                "source_file",
                "block_id",
                "title",
                "out_wav",
                "srt_path",
                "manifest_path",
                "error",
            ]
        )


def append_ledger_row(
    *,
    status: str,
    backend: str,
    source_kind: str,
    qa_file: str,
    source_file: str,
    block_id: str,
    title: str,
    out_wav: str,
    srt_path: str,
    manifest_path: str,
    error: str,
) -> None:
    ensure_ledger()
    with LEDGER_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                now_iso(),
                status,
                backend,
                source_kind,
                qa_file,
                source_file,
                block_id,
                title,
                out_wav,
                srt_path,
                manifest_path,
                error,
            ]
        )


def probe_duration_seconds(audio_path: Path) -> float:
    ffprobe = shutil_which("ffprobe")
    if not ffprobe:
        return 0.0
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return 0.0
    try:
        return float((proc.stdout or "0").strip())
    except ValueError:
        return 0.0


def shutil_which(binary: str) -> str:
    return subprocess.run(
        ["bash", "-lc", f"command -v {binary} || true"],
        capture_output=True,
        text=True,
    ).stdout.strip()


def write_estimated_srt(text: str, srt_path: Path, total_duration_sec: float) -> int:
    sentences = [normalize_spaces(s) for s in re.split(r"(?<=[.!?])\s+", text) if normalize_spaces(s)]
    if not sentences:
        srt_path.write_text("", encoding="utf-8")
        return 0
    weights = [max(1, len(s)) for s in sentences]
    total_weight = sum(weights)
    cursor = 0.0
    rows: List[str] = []
    for idx, sentence in enumerate(sentences, start=1):
        dur = (weights[idx - 1] / max(1, total_weight)) * max(1.0, total_duration_sec)
        start = cursor
        end = min(max(total_duration_sec, start + 0.5), start + dur)
        cursor = end
        rows.append(str(idx))
        rows.append(f"{format_srt_ts(start)} --> {format_srt_ts(end)}")
        rows.extend(wrap_caption(sentence, 56))
        rows.append("")
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    srt_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(sentences)


def format_srt_ts(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000.0)))
    h = ms // 3_600_000
    rem = ms % 3_600_000
    m = rem // 60_000
    rem = rem % 60_000
    s = rem // 1000
    mm = rem % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{mm:03d}"


def wrap_caption(text: str, max_chars: int) -> List[str]:
    words = normalize_spaces(text).split()
    if not words:
        return [""]
    lines: List[str] = []
    cur: List[str] = []
    cur_len = 0
    for word in words:
        n = len(word) if not cur else cur_len + 1 + len(word)
        if cur and n > max_chars:
            lines.append(" ".join(cur))
            cur = [word]
            cur_len = len(word)
        else:
            cur.append(word)
            cur_len = n
    if cur:
        lines.append(" ".join(cur))
    return lines


def run_qwen_render(
    *,
    script_path: Path,
    out_wav: Path,
    manifest_path: Path,
    segments_dir: Path,
    speaker: str,
    language: str,
    chunk_chars: int,
    max_new_tokens: int,
    join_silence_ms: int,
) -> Tuple[bool, str]:
    cmd = [
        "bash",
        str(QWEN_WRAPPER),
        "--text-file",
        str(script_path),
        "--speaker",
        speaker,
        "--language",
        language,
        "--out",
        str(out_wav),
        "--manifest",
        str(manifest_path),
        "--segments-dir",
        str(segments_dir),
        "--chunk-chars",
        str(chunk_chars),
        "--max-new-tokens",
        str(max_new_tokens),
        "--join-silence-ms",
        str(join_silence_ms),
        "--attn-implementation",
        "eager",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return True, ""
    return False, (proc.stderr or proc.stdout or "qwen_failed").strip()[:700]


def run_ffmpeg_convert_mp3_to_wav(mp3_path: Path, wav_path: Path, normalize: bool) -> Tuple[bool, str]:
    ffmpeg = shutil_which("ffmpeg")
    if not ffmpeg:
        return False, "ffmpeg_not_found"
    cmd = [ffmpeg, "-y", "-i", str(mp3_path)]
    if normalize:
        cmd.extend(
            [
                "-af",
                "loudnorm=I=-16:LRA=11:TP=-1.5:linear=true:print_format=summary",
            ]
        )
    cmd.extend(["-ar", "24000", "-ac", "1", str(wav_path)])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return True, ""
    return False, (proc.stderr or proc.stdout or "ffmpeg_convert_failed").strip()[:700]


def run_elevenlabs_fallback(
    *,
    text: str,
    out_wav: Path,
    srt_path: Path,
    manifest_path: Path,
    voice_id: str,
    model_id: str,
    timeout_sec: int,
) -> Tuple[bool, str]:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        return False, "missing_ELEVENLABS_API_KEY"
    if not voice_id:
        return False, "missing_elevenlabs_voice_id"

    out_wav.parent.mkdir(parents=True, exist_ok=True)
    mp3_path = out_wav.with_suffix(".elevenlabs.mp3")

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    req = urllib.request.Request(
        url=url,
        method="POST",
        data=data,
        headers={
            "xi-api-key": api_key,
            "accept": "audio/mpeg",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=max(30, timeout_sec)) as resp:
            audio_bytes = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return False, f"elevenlabs_http_{e.code}: {body[:350]}"
    except Exception as e:
        return False, f"elevenlabs_request_failed: {e}"

    mp3_path.write_bytes(audio_bytes)
    ok, err = run_ffmpeg_convert_mp3_to_wav(mp3_path, out_wav, True)
    if not ok:
        return False, err

    duration = probe_duration_seconds(out_wav)
    srt_count = write_estimated_srt(text, srt_path, duration)
    manifest = {
        "generated_at": now_iso(),
        "backend": "elevenlabs_fallback",
        "output_wav": str(out_wav),
        "srt_path": str(srt_path),
        "srt_entries": srt_count,
        "duration_sec": round(duration, 4),
        "voice_id": voice_id,
        "model_id": model_id,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True, ""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Render approved scripts to local TTS assets")
    ap.add_argument("--max-jobs", type=int, default=4, help="Max approved files to process per run")
    ap.add_argument("--max-blocks-per-source", type=int, default=2, help="Max script blocks per source file")
    ap.add_argument("--chunk-chars", type=int, default=650)
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--join-silence-ms", type=int, default=350)
    ap.add_argument("--speaker", default="aiden")
    ap.add_argument("--language", default="English")
    ap.add_argument("--max-script-chars", type=int, default=30000)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-queue-source", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--allow-qa-source", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--elevenlabs-fallback", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--elevenlabs-voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID", "").strip())
    ap.add_argument("--elevenlabs-model-id", default=os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2").strip())
    ap.add_argument("--elevenlabs-timeout-sec", type=int, default=180)
    ap.add_argument("--source-file", default="", help="Optional manual source markdown/txt path")
    ap.add_argument("--source-title", default="", help="Optional manual title override for --source-file")
    return ap.parse_args()


def acquire_lock() -> bool:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(LOCK_PATH), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    os.write(fd, f"{os.getpid()}\n".encode("utf-8"))
    os.close(fd)
    return True


def release_lock() -> None:
    LOCK_PATH.unlink(missing_ok=True)


def active_jobs(args: argparse.Namespace) -> List[Job]:
    jobs: List[Job] = []
    if args.source_file:
        jobs.append(
            Job(
                source_kind="manual",
                status="APPROVED",
                source_file=args.source_file,
                title=(args.source_title or Path(args.source_file).stem),
                platform="manual",
                content_type="video_script",
            )
        )
    if args.allow_qa_source:
        jobs.extend(discover_qa_jobs())
    if args.allow_queue_source:
        jobs.extend(discover_queue_jobs())
    filtered: List[Job] = []
    for job in jobs:
        if job.status != "APPROVED":
            continue
        if not looks_like_video_content(
            platform=job.platform,
            content_type=job.content_type,
            source_file=job.source_file,
        ) and job.source_kind == "qa":
            continue
        filtered.append(job)
    return filtered


def process(args: argparse.Namespace) -> int:
    if not acquire_lock():
        print("approved_script_voice_runner: lock already held, skipping")
        return 0

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        state = load_state()
        completed = state.get("completed", {})
        if not isinstance(completed, dict):
            completed = {}
            state["completed"] = completed

        jobs = active_jobs(args)
        print(f"approved_script_voice_runner: approved_jobs={len(jobs)}")
        if args.dry_run:
            for j in jobs[: max(1, args.max_jobs)]:
                print(f"- {j.source_kind}: {j.source_file} (status={j.status})")
            return 0

        processed_sources = 0
        for job in jobs:
            if processed_sources >= max(1, int(args.max_jobs)):
                break
            source_path = ensure_within_root(job.source_file)
            if not source_path or not source_path.exists():
                append_ledger_row(
                    status="SKIP",
                    backend="none",
                    source_kind=job.source_kind,
                    qa_file=job.qa_file,
                    source_file=job.source_file,
                    block_id="",
                    title=job.title,
                    out_wav="",
                    srt_path="",
                    manifest_path="",
                    error="source_missing_or_outside_root",
                )
                continue

            source_text = source_path.read_text(encoding="utf-8", errors="replace")
            source_hint = job.title or source_path.stem
            blocks = extract_script_blocks(
                source_text,
                source_hint=source_hint,
                max_chars=max(500, int(args.max_script_chars)),
            )
            if not blocks:
                append_ledger_row(
                    status="SKIP",
                    backend="none",
                    source_kind=job.source_kind,
                    qa_file=job.qa_file,
                    source_file=job.source_file,
                    block_id="",
                    title=source_hint,
                    out_wav="",
                    srt_path="",
                    manifest_path="",
                    error="no_narration_text_extracted",
                )
                continue

            for block_idx, (block_id, title, narration) in enumerate(blocks, start=1):
                if block_idx > max(1, int(args.max_blocks_per_source)):
                    break

                key_seed = "|".join(
                    [
                        job.source_kind,
                        job.qa_file,
                        job.source_file,
                        block_id,
                        sha1_text(narration),
                    ]
                )
                render_key = sha1_text(key_seed)
                if render_key in completed:
                    continue

                day_dir = OUTPUT_DIR / datetime.now().strftime("%Y-%m-%d")
                day_dir.mkdir(parents=True, exist_ok=True)
                slug = slugify(f"{source_path.stem}-{block_id}-{title}")
                script_txt = day_dir / f"{slug}.txt"
                out_wav = day_dir / f"{slug}.wav"
                manifest_path = day_dir / f"{slug}.json"
                srt_path = day_dir / f"{slug}.srt"
                segments_dir = day_dir / f"{slug}_segments"

                script_txt.write_text(narration + "\n", encoding="utf-8")

                speaker = job.speaker or args.speaker
                language = job.language or args.language

                ok, err = run_qwen_render(
                    script_path=script_txt,
                    out_wav=out_wav,
                    manifest_path=manifest_path,
                    segments_dir=segments_dir,
                    speaker=speaker,
                    language=language,
                    chunk_chars=int(args.chunk_chars),
                    max_new_tokens=int(args.max_new_tokens),
                    join_silence_ms=int(args.join_silence_ms),
                )
                backend = "qwen_local"
                if not ok and args.elevenlabs_fallback:
                    fb_ok, fb_err = run_elevenlabs_fallback(
                        text=narration,
                        out_wav=out_wav,
                        srt_path=srt_path,
                        manifest_path=manifest_path,
                        voice_id=(args.elevenlabs_voice_id or "").strip(),
                        model_id=(args.elevenlabs_model_id or "").strip(),
                        timeout_sec=int(args.elevenlabs_timeout_sec),
                    )
                    if fb_ok:
                        ok = True
                        err = ""
                        backend = "elevenlabs_fallback"
                    else:
                        err = f"{err} | fallback={fb_err}".strip(" |")

                status = "OK" if ok else "ERROR"
                append_ledger_row(
                    status=status,
                    backend=backend,
                    source_kind=job.source_kind,
                    qa_file=job.qa_file,
                    source_file=job.source_file,
                    block_id=block_id,
                    title=title,
                    out_wav=str(out_wav),
                    srt_path=str(srt_path),
                    manifest_path=str(manifest_path),
                    error=err,
                )

                if ok:
                    completed[render_key] = {
                        "created_at": now_iso(),
                        "backend": backend,
                        "qa_file": job.qa_file,
                        "source_file": job.source_file,
                        "block_id": block_id,
                        "title": title,
                        "out_wav": str(out_wav),
                    }
                    print(f"approved_script_voice_runner: OK [{backend}] {out_wav}")
                else:
                    print(f"approved_script_voice_runner: ERROR {job.source_file}#{block_id} -> {err}")

            processed_sources += 1

        save_state(state)
        return 0
    finally:
        release_lock()


def main() -> int:
    args = parse_args()
    return process(args)


if __name__ == "__main__":
    raise SystemExit(main())
