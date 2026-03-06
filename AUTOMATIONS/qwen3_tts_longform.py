#!/usr/bin/env python3
"""Render longform narration with Qwen3-TTS local model.

Designed for faceless YouTube workflows:
- Splits long scripts into manageable chunks.
- Renders each chunk with Qwen3-TTS CustomVoice.
- Exports both merged narration and per-chunk segment WAVs.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence

try:
    import numpy as np
except ImportError:
    np = None
    print("WARNING: numpy not installed. Run: pip3 install numpy")

try:
    import soundfile as sf
except ImportError:
    sf = None
    print("WARNING: soundfile not installed. Run: pip3 install soundfile")

try:
    import torch
except ImportError:
    torch = None
    print("WARNING: torch not installed. Run: pip3 install torch")

try:
    from qwen_tts import Qwen3TTSModel
except ImportError:
    Qwen3TTSModel = None
    print("WARNING: qwen_tts not installed. This requires the Qwen3-TTS model package.")


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
DEFAULT_LOCAL_MODEL_DIR = BASE_DIR / "models" / "Qwen3-TTS-12Hz-1.7B-CustomVoice"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def format_srt_ts(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000.0)))
    hours = total_ms // 3_600_000
    remain = total_ms % 3_600_000
    minutes = remain // 60_000
    remain = remain % 60_000
    secs = remain // 1000
    millis = remain % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def wrap_caption(text: str, max_chars: int) -> List[str]:
    words = normalize_text(text).split(" ")
    if not words or max_chars < 12:
        return [normalize_text(text)]
    lines: List[str] = []
    cur: List[str] = []
    cur_len = 0
    for w in words:
        w_len = len(w)
        next_len = w_len if not cur else cur_len + 1 + w_len
        if cur and next_len > max_chars:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = w_len
        else:
            cur.append(w)
            cur_len = next_len
    if cur:
        lines.append(" ".join(cur))
    return lines


def write_srt(
    *,
    srt_path: Path,
    segment_meta: List[Dict[str, object]],
    join_silence_ms: int,
    caption_max_chars: int,
) -> int:
    gap_sec = max(0, int(join_silence_ms)) / 1000.0
    cursor = 0.0
    rows: List[str] = []
    idx = 1
    for seg in segment_meta:
        duration = float(seg.get("duration_sec", 0.0) or 0.0)
        text = normalize_text(str(seg.get("text", "")))
        if duration <= 0.0 or not text:
            cursor += max(0.0, duration) + gap_sec
            continue

        start = cursor
        end = start + duration
        lines = wrap_caption(text, caption_max_chars)

        rows.append(str(idx))
        rows.append(f"{format_srt_ts(start)} --> {format_srt_ts(end)}")
        rows.extend(lines)
        rows.append("")

        idx += 1
        cursor = end + gap_sec

    if not rows:
        srt_path.write_text("", encoding="utf-8")
        return 0

    srt_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return idx - 1


def normalize_audio_ffmpeg(
    *,
    in_wav: Path,
    out_wav: Path,
    sample_rate: int,
    target_lufs: float,
    target_lra: float,
    target_true_peak: float,
) -> str:
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        return "ffmpeg_not_found"

    loudnorm = (
        f"loudnorm=I={target_lufs}:LRA={target_lra}:TP={target_true_peak}:"
        "linear=true:print_format=summary"
    )
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(in_wav),
        "-af",
        loudnorm,
        "-ar",
        str(int(sample_rate)),
        "-ac",
        "1",
        str(out_wav),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return ""
    return (proc.stderr or proc.stdout or "ffmpeg_failed").strip()[:500]


def split_into_chunks(text: str, max_chars: int) -> List[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    chunks: List[str] = []
    current = ""
    for sentence in sentences:
        if not sentence:
            continue
        candidate = sentence if not current else f"{current} {sentence}"
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(sentence) <= max_chars:
            current = sentence
            continue
        # Hard-wrap very long sentences.
        start = 0
        while start < len(sentence):
            part = sentence[start : start + max_chars].strip()
            if part:
                chunks.append(part)
            start += max_chars
        current = ""
    if current:
        chunks.append(current)
    return chunks


def resolve_dtype(name: str) -> torch.dtype:
    n = (name or "").strip().lower()
    if n in {"float32", "fp32"}:
        return torch.float32
    if n in {"float16", "fp16"}:
        return torch.float16
    if n in {"bfloat16", "bf16"}:
        return torch.bfloat16
    raise ValueError(f"Unsupported dtype: {name}")


def resolve_speaker(requested: str, supported: Sequence[str]) -> str:
    if not supported:
        return requested
    lower_map = {s.lower(): s for s in supported}
    candidate = (requested or "").strip().lower()
    if candidate in lower_map:
        return lower_map[candidate]
    supported_sorted = ", ".join(sorted(supported))
    raise ValueError(
        f"Unsupported speaker '{requested}'. Supported speakers: {supported_sorted}"
    )


def build_manifest(
    *,
    args: argparse.Namespace,
    chosen_speaker: str,
    sample_rate: int,
    out_wav: Path,
    segment_paths: List[str],
    segment_meta: List[Dict[str, object]],
    total_duration_sec: float,
    srt_path: str,
    srt_entries: int,
    loudness_normalized: bool,
    normalization_error: str,
) -> Dict[str, object]:
    return {
        "generated_at": now_iso(),
        "model": args.model,
        "model_source": str(args.model_source),
        "language": args.language,
        "speaker": chosen_speaker,
        "device_map": args.device_map,
        "dtype": args.dtype,
        "chunk_chars": args.chunk_chars,
        "join_silence_ms": args.join_silence_ms,
        "sampling_rate": sample_rate,
        "segment_count": len(segment_meta),
        "total_duration_sec": round(total_duration_sec, 4),
        "output_wav": str(out_wav),
        "srt_path": srt_path,
        "srt_entries": int(srt_entries),
        "loudness_normalized": bool(loudness_normalized),
        "normalization_error": normalization_error,
        "segments": segment_paths,
        "segment_meta": segment_meta,
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Longform local narration using Qwen3-TTS CustomVoice")
    ap.add_argument("--text", default="", help="Inline narration text")
    ap.add_argument("--text-file", default="", help="Path to narration text file")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model id or local path")
    ap.add_argument(
        "--prefer-local-model",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Prefer local snapshot under models/Qwen3-TTS-12Hz-1.7B-CustomVoice when available",
    )
    ap.add_argument("--speaker", default="aiden", help="Speaker id (case-insensitive)")
    ap.add_argument("--language", default="English", help="Language (or Auto)")
    ap.add_argument("--instruct", default="Speak naturally and clearly.", help="Optional style instruction")
    ap.add_argument("--device-map", default="cpu", help="device_map passed to from_pretrained (cpu/auto)")
    ap.add_argument(
        "--attn-implementation",
        default="eager",
        choices=["eager", "sdpa"],
        help="Attention backend passed to from_pretrained (eager avoids flash-attn warnings on Apple Silicon)",
    )
    ap.add_argument("--dtype", default="float32", choices=["float32", "fp32", "float16", "fp16", "bfloat16", "bf16"])
    ap.add_argument("--chunk-chars", type=int, default=650, help="Max chars per TTS chunk")
    ap.add_argument("--max-new-tokens", type=int, default=1024, help="Generation cap per chunk")
    ap.add_argument("--join-silence-ms", type=int, default=350, help="Silence inserted between chunks")
    ap.add_argument("--out", default=str(BASE_DIR / "output" / "qwen_tts" / "longform.wav"), help="Merged output wav path")
    ap.add_argument(
        "--segments-dir",
        default=str(BASE_DIR / "output" / "qwen_tts" / "segments"),
        help="Directory for per-chunk wavs",
    )
    ap.add_argument("--manifest", default="", help="Optional manifest path (default: <out>.json)")
    ap.add_argument("--no-segments", action="store_true", help="Disable per-chunk wav exports")
    ap.add_argument(
        "--normalize-loudness",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Normalize final wav via ffmpeg loudnorm",
    )
    ap.add_argument("--target-lufs", type=float, default=-16.0, help="Integrated loudness target for ffmpeg loudnorm")
    ap.add_argument("--target-lra", type=float, default=11.0, help="Loudness range target for ffmpeg loudnorm")
    ap.add_argument("--target-true-peak", type=float, default=-1.5, help="True peak target for ffmpeg loudnorm")
    ap.add_argument(
        "--no-srt",
        action="store_true",
        help="Disable subtitle export",
    )
    ap.add_argument(
        "--subs-srt",
        default="",
        help="Optional subtitle path (default: <out>.srt)",
    )
    ap.add_argument(
        "--caption-max-chars",
        type=int,
        default=56,
        help="Max chars per subtitle line",
    )
    return ap.parse_args()


def load_text(args: argparse.Namespace) -> str:
    inline = normalize_text(args.text)
    file_text = ""
    if args.text_file:
        file_path = Path(args.text_file).expanduser().resolve()
        file_text = normalize_text(file_path.read_text(encoding="utf-8", errors="replace"))
    source = inline or file_text
    if not source:
        raise ValueError("Provide --text or --text-file.")
    return source


def resolve_model_source(model: str, prefer_local: bool) -> str:
    if prefer_local and str(model).strip() == DEFAULT_MODEL and DEFAULT_LOCAL_MODEL_DIR.exists():
        return str(DEFAULT_LOCAL_MODEL_DIR)
    return model


def main() -> int:
    args = parse_args()
    text = load_text(args)
    chunks = split_into_chunks(text, max(120, int(args.chunk_chars)))
    if not chunks:
        raise ValueError("No text chunks generated.")

    out_wav = Path(args.out).expanduser().resolve()
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    segments_dir = Path(args.segments_dir).expanduser().resolve()
    if not args.no_segments:
        segments_dir.mkdir(parents=True, exist_ok=True)

    model_source = resolve_model_source(args.model, bool(args.prefer_local_model))
    args.model_source = model_source

    tts = Qwen3TTSModel.from_pretrained(
        model_source,
        device_map=args.device_map,
        dtype=resolve_dtype(args.dtype),
        attn_implementation=args.attn_implementation,
    )

    supported_speakers = tts.get_supported_speakers() or []
    speaker = resolve_speaker(args.speaker, supported_speakers)

    rendered: List[np.ndarray] = []
    segment_paths: List[str] = []
    segment_meta: List[Dict[str, object]] = []
    sample_rate = 0

    for idx, chunk in enumerate(chunks, start=1):
        wavs, sr = tts.generate_custom_voice(
            text=chunk,
            language=args.language,
            speaker=speaker,
            instruct=args.instruct or None,
            max_new_tokens=int(args.max_new_tokens),
        )
        wav = np.asarray(wavs[0], dtype=np.float32).reshape(-1)
        if sample_rate == 0:
            sample_rate = int(sr)
        elif int(sr) != sample_rate:
            raise RuntimeError(f"Sample-rate mismatch: got {sr}, expected {sample_rate}")

        rendered.append(wav)
        duration = float(len(wav) / max(1, sample_rate))
        segment_row = {
            "chunk_index": idx,
            "chars": len(chunk),
            "duration_sec": round(duration, 4),
            "text": chunk,
        }

        if not args.no_segments:
            seg_path = segments_dir / f"segment_{idx:03d}.wav"
            sf.write(str(seg_path), wav, sample_rate)
            segment_paths.append(str(seg_path))
            segment_row["path"] = str(seg_path)
        segment_meta.append(segment_row)

    silence = np.zeros(int(sample_rate * max(0, args.join_silence_ms) / 1000.0), dtype=np.float32)
    merged_parts: List[np.ndarray] = []
    for i, wav in enumerate(rendered):
        merged_parts.append(wav)
        if i < len(rendered) - 1 and len(silence) > 0:
            merged_parts.append(silence)
    merged = np.concatenate(merged_parts) if merged_parts else np.zeros(0, dtype=np.float32)

    raw_out_wav = out_wav.with_suffix(".raw.wav") if args.normalize_loudness else out_wav
    sf.write(str(raw_out_wav), merged, sample_rate)

    normalized = False
    normalization_error = ""
    if args.normalize_loudness:
        normalization_error = normalize_audio_ffmpeg(
            in_wav=raw_out_wav,
            out_wav=out_wav,
            sample_rate=sample_rate,
            target_lufs=float(args.target_lufs),
            target_lra=float(args.target_lra),
            target_true_peak=float(args.target_true_peak),
        )
        if not normalization_error:
            normalized = True
            raw_out_wav.unlink(missing_ok=True)
        else:
            raw_out_wav.replace(out_wav)

    final_info = sf.info(str(out_wav))
    total_duration_sec = float(final_info.frames / max(1, final_info.samplerate))
    sample_rate = int(final_info.samplerate)

    srt_entries = 0
    srt_path = ""
    if not args.no_srt:
        srt_file = Path(args.subs_srt).expanduser().resolve() if args.subs_srt else out_wav.with_suffix(".srt")
        srt_file.parent.mkdir(parents=True, exist_ok=True)
        srt_entries = write_srt(
            srt_path=srt_file,
            segment_meta=segment_meta,
            join_silence_ms=int(args.join_silence_ms),
            caption_max_chars=max(16, int(args.caption_max_chars)),
        )
        srt_path = str(srt_file)

    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else out_wav.with_suffix(".json")
    manifest = build_manifest(
        args=args,
        chosen_speaker=speaker,
        sample_rate=sample_rate,
        out_wav=out_wav,
        segment_paths=segment_paths,
        segment_meta=segment_meta,
        total_duration_sec=total_duration_sec,
        srt_path=srt_path,
        srt_entries=srt_entries,
        loudness_normalized=normalized,
        normalization_error=normalization_error,
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("qwen3_tts_longform: wrote")
    print(f"- wav: {out_wav}")
    print(f"- manifest: {manifest_path}")
    if not args.no_segments:
        print(f"- segments_dir: {segments_dir}")
    if srt_path:
        print(f"- srt: {srt_path}")
        print(f"- srt_entries: {srt_entries}")
    print(f"- loudness_normalized: {normalized}")
    if normalization_error:
        print(f"- normalization_error: {normalization_error}")
    print(f"- chunks: {len(chunks)}")
    print(f"- duration_sec: {total_duration_sec:.2f}")
    print(f"- speaker: {speaker}")
    print(f"- sample_rate: {sample_rate}")
    return 0


if __name__ == "__main__":
    _missing = []
    if np is None: _missing.append("numpy")
    if sf is None: _missing.append("soundfile")
    if torch is None: _missing.append("torch")
    if Qwen3TTSModel is None: _missing.append("qwen_tts")
    if _missing:
        print(f"\nERROR: Missing required packages: {', '.join(_missing)}")
        print(f"Install with: pip3 install {' '.join(m for m in _missing if m != 'qwen_tts')}")
        if "qwen_tts" in _missing:
            print("For qwen_tts: see https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice")
        raise SystemExit(1)
    raise SystemExit(main())
