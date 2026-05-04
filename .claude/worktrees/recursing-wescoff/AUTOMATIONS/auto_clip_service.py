#!/usr/bin/env python3
"""
Auto Clip Service - Streamer clipping automation for client work.

Downloads VODs from Twitch/YouTube, detects highlights via audio peaks
and chat density, extracts clips, crops vertical for TikTok/Shorts/Reels,
adds captions via Whisper, and tracks client work in LEDGER.

Usage:
    python3 auto_clip_service.py --url "https://twitch.tv/videos/xxx" --clips 5
    python3 auto_clip_service.py --url "https://youtube.com/watch?v=xxx" --duration 30 --vertical --captions
    python3 auto_clip_service.py --batch urls.txt --clips 10 --vertical --captions
    python3 auto_clip_service.py --status
    python3 auto_clip_service.py --demo --url "https://youtube.com/watch?v=xxx"

Requires: yt-dlp, ffmpeg, whisper (all pre-installed)
"""

import os
import sys
import json
import csv
import time
import struct
import wave
import math
import argparse
import subprocess
import hashlib
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import defaultdict

# Project root for guardrails
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OUTPUT_BASE = PROJECT_ROOT / "OUTPUT" / "clips"

# Optional imports
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


class AudioPeakDetector:
    """Detect audio peaks (loud/hype moments) using ffmpeg and raw PCM analysis."""

    def __init__(self, threshold_db: float = -10.0, min_gap_seconds: float = 30.0):
        self.threshold_db = threshold_db
        self.min_gap_seconds = min_gap_seconds

    def extract_audio_pcm(self, video_path: Path, sample_rate: int = 8000) -> Optional[Path]:
        """Extract audio as raw 16-bit mono PCM using ffmpeg."""
        pcm_path = video_path.parent / f"{video_path.stem}_audio.raw"
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_path),
                '-vn',
                '-acodec', 'pcm_s16le',
                '-ar', str(sample_rate),
                '-ac', '1',
                '-f', 's16le',
                str(pcm_path)
            ]
            subprocess.run(cmd, capture_output=True, check=True, timeout=300)
            return pcm_path if pcm_path.exists() else None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"[ERROR] Audio extraction failed: {e}")
            return None

    def analyze_peaks(
        self,
        pcm_path: Path,
        sample_rate: int = 8000,
        window_seconds: float = 2.0,
        max_peaks: int = 50
    ) -> List[Dict]:
        """Analyze PCM audio for volume peaks. Returns list of {time_seconds, rms_db, rms_raw}."""
        file_size = pcm_path.stat().st_size
        num_samples = file_size // 2  # 16-bit = 2 bytes per sample
        total_seconds = num_samples / sample_rate
        window_samples = int(window_seconds * sample_rate)

        print(f"[INFO] Analyzing {total_seconds:.0f}s of audio ({num_samples} samples)...")

        rms_values = []

        with open(pcm_path, 'rb') as f:
            offset = 0
            while offset + window_samples * 2 <= file_size:
                raw = f.read(window_samples * 2)
                if len(raw) < window_samples * 2:
                    break

                # Parse 16-bit signed little-endian samples
                samples = struct.unpack(f'<{window_samples}h', raw)

                # Calculate RMS
                sum_sq = sum(s * s for s in samples)
                rms = math.sqrt(sum_sq / window_samples) if window_samples > 0 else 0

                # Convert to dB (relative to max 16-bit value)
                if rms > 0:
                    rms_db = 20 * math.log10(rms / 32768.0)
                else:
                    rms_db = -96.0

                time_sec = offset / (2 * sample_rate)
                rms_values.append({
                    'time_seconds': time_sec,
                    'rms_db': rms_db,
                    'rms_raw': rms
                })

                offset += window_samples * 2

        if not rms_values:
            return []

        # Sort by loudness descending
        rms_values.sort(key=lambda x: x['rms_db'], reverse=True)

        # Pick top peaks with minimum gap between them
        selected = []
        for candidate in rms_values:
            if candidate['rms_db'] < self.threshold_db:
                break
            too_close = False
            for existing in selected:
                if abs(candidate['time_seconds'] - existing['time_seconds']) < self.min_gap_seconds:
                    too_close = True
                    break
            if not too_close:
                selected.append(candidate)
            if len(selected) >= max_peaks:
                break

        # Sort by time for chronological output
        selected.sort(key=lambda x: x['time_seconds'])
        return selected

    def detect_highlights(
        self,
        video_path: Path,
        max_highlights: int = 20
    ) -> List[Dict]:
        """Full pipeline: extract audio, find peaks, return highlight timestamps."""
        pcm_path = self.extract_audio_pcm(video_path)
        if not pcm_path:
            return []

        try:
            peaks = self.analyze_peaks(pcm_path, max_peaks=max_highlights)
            return peaks
        finally:
            # Cleanup temp audio
            if pcm_path.exists():
                pcm_path.unlink()


class ChatDensityAnalyzer:
    """Analyze Twitch chat replay density from downloaded chat logs."""

    @staticmethod
    def download_chat(url: str, output_path: Path) -> Optional[Path]:
        """Download Twitch chat replay using yt-dlp's chat subtitle feature."""
        try:
            cmd = [
                'yt-dlp',
                '--write-subs',
                '--sub-langs', 'live_chat',
                '--skip-download',
                '--output', str(output_path / '%(id)s.%(ext)s'),
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            # Look for downloaded chat file
            for f in output_path.iterdir():
                if 'live_chat' in f.name or f.suffix == '.json':
                    return f
            return None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    @staticmethod
    def parse_chat_density(
        chat_path: Path,
        bucket_seconds: float = 10.0
    ) -> List[Dict]:
        """Parse chat JSON and compute message density per time bucket."""
        if not chat_path or not chat_path.exists():
            return []

        try:
            with open(chat_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return []

        # Try to parse as JSON lines (yt-dlp format)
        messages = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                # yt-dlp chat format has replayChatItemAction -> videoOffsetTimeMsec
                offset_ms = None
                if 'replayChatItemAction' in obj:
                    action = obj['replayChatItemAction']
                    offset_ms = int(action.get('videoOffsetTimeMsec', 0))
                elif 'videoOffsetTimeMsec' in obj:
                    offset_ms = int(obj['videoOffsetTimeMsec'])
                elif 'content_offset_seconds' in obj:
                    offset_ms = int(float(obj['content_offset_seconds']) * 1000)

                if offset_ms is not None:
                    messages.append(offset_ms / 1000.0)
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                continue

        if not messages:
            return []

        messages.sort()
        max_time = messages[-1]
        num_buckets = int(max_time / bucket_seconds) + 1

        buckets = defaultdict(int)
        for t in messages:
            bucket_idx = int(t / bucket_seconds)
            buckets[bucket_idx] += 1

        # Convert to list with times
        density = []
        for i in range(num_buckets):
            density.append({
                'time_seconds': i * bucket_seconds,
                'message_count': buckets.get(i, 0)
            })

        return density

    @staticmethod
    def get_peak_chat_moments(
        density: List[Dict],
        top_n: int = 20,
        min_gap_seconds: float = 30.0
    ) -> List[Dict]:
        """Get top N chat density peaks with minimum gap between them."""
        if not density:
            return []

        sorted_density = sorted(density, key=lambda x: x['message_count'], reverse=True)

        selected = []
        for candidate in sorted_density:
            if candidate['message_count'] == 0:
                break
            too_close = False
            for existing in selected:
                if abs(candidate['time_seconds'] - existing['time_seconds']) < min_gap_seconds:
                    too_close = True
                    break
            if not too_close:
                selected.append(candidate)
            if len(selected) >= top_n:
                break

        selected.sort(key=lambda x: x['time_seconds'])
        return selected


class ClipExtractor:
    """Extract and process video clips using ffmpeg."""

    @staticmethod
    def get_video_duration(video_path: Path) -> float:
        """Get video duration in seconds using ffprobe."""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
            return float(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError, subprocess.TimeoutExpired):
            return 0.0

    @staticmethod
    def get_video_dimensions(video_path: Path) -> Tuple[int, int]:
        """Get video width and height."""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
            parts = result.stdout.strip().split(',')
            return int(parts[0]), int(parts[1])
        except (subprocess.CalledProcessError, ValueError, IndexError, subprocess.TimeoutExpired):
            return 1920, 1080  # Default assumption

    @staticmethod
    def extract_clip(
        video_path: Path,
        output_path: Path,
        start_seconds: float,
        duration_seconds: float,
        vertical: bool = False,
        quality_crf: int = 23
    ) -> Optional[Path]:
        """Extract a clip from video. Optionally crop to vertical 9:16."""
        safe_path(output_path)

        vf_filters = []
        if vertical:
            # Center crop to 9:16 aspect ratio
            vf_filters.append("crop=ih*9/16:ih:(iw-ih*9/16)/2:0")

        vf_arg = ','.join(vf_filters) if vf_filters else None

        cmd = [
            'ffmpeg', '-y',
            '-ss', str(start_seconds),
            '-i', str(video_path),
            '-t', str(duration_seconds),
        ]

        if vf_arg:
            cmd.extend(['-vf', vf_arg])

        cmd.extend([
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', str(quality_crf),
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            str(output_path)
        ])

        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=300)
            if output_path.exists() and output_path.stat().st_size > 0:
                return output_path
            return None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"[ERROR] Clip extraction failed: {e}")
            return None

    @staticmethod
    def burn_captions(
        clip_path: Path,
        srt_path: Path,
        output_path: Path,
        font_size: int = 22,
        margin_v: int = 40
    ) -> Optional[Path]:
        """Burn SRT captions into video clip."""
        safe_path(output_path)

        # Escape special chars in path for ffmpeg subtitle filter
        srt_str = str(srt_path).replace("'", "\\'").replace(":", "\\:")

        style = (
            f"FontSize={font_size},"
            f"PrimaryColour=&H00FFFFFF,"
            f"OutlineColour=&H00000000,"
            f"BackColour=&H80000000,"
            f"BorderStyle=4,"
            f"Outline=1,"
            f"Shadow=0,"
            f"MarginV={margin_v},"
            f"Alignment=2"
        )

        cmd = [
            'ffmpeg', '-y',
            '-i', str(clip_path),
            '-vf', f"subtitles='{srt_str}':force_style='{style}'",
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=300)
            if output_path.exists() and output_path.stat().st_size > 0:
                return output_path
            return None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"[WARN] Caption burn failed (delivering without captions): {e}")
            return None


class CaptionGenerator:
    """Generate SRT captions using Whisper."""

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        """Lazy-load whisper model."""
        if self._model is None:
            if not WHISPER_AVAILABLE:
                print("[WARN] Whisper not installed. pip install openai-whisper")
                return None
            print(f"[INFO] Loading whisper model '{self.model_name}'...")
            self._model = whisper.load_model(self.model_name)
        return self._model

    def transcribe_clip(self, clip_path: Path) -> Optional[Dict]:
        """Transcribe a clip and return whisper result dict."""
        model = self._load_model()
        if model is None:
            return None

        try:
            result = model.transcribe(
                str(clip_path),
                word_timestamps=True,
                language='en'
            )
            return result
        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}")
            return None

    def generate_srt(self, transcript: Dict, output_path: Path) -> Optional[Path]:
        """Generate SRT file from whisper transcript."""
        safe_path(output_path)

        segments = transcript.get('segments', [])
        if not segments:
            return None

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                start = seg['start']
                end = seg['end']
                text = seg['text'].strip()
                if not text:
                    continue
                f.write(f"{i}\n")
                f.write(f"{_srt_timestamp(start)} --> {_srt_timestamp(end)}\n")
                f.write(f"{text}\n\n")

        return output_path if output_path.exists() else None


def _srt_timestamp(seconds: float) -> str:
    """Format timestamp for SRT (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def _format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


class ClipServiceTracker:
    """Track client clip work in LEDGER/CLIP_SERVICE_TRACKER.csv."""

    HEADERS = [
        'job_id', 'client_name', 'source_url', 'platform',
        'clip_number', 'clip_path', 'start_time', 'end_time',
        'duration_seconds', 'detection_method', 'detection_score',
        'vertical', 'captioned', 'status', 'created_at', 'notes'
    ]

    def __init__(self):
        self.csv_path = safe_path(LEDGER_DIR / "CLIP_SERVICE_TRACKER.csv")
        self._init_csv()

    def _init_csv(self):
        """Create CSV with headers if it doesn't exist."""
        if not self.csv_path.exists():
            LEDGER_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADERS)

    def add_entry(self, entry: Dict):
        """Append a clip entry to the tracker."""
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                entry.get('job_id', ''),
                entry.get('client_name', 'default'),
                entry.get('source_url', ''),
                entry.get('platform', ''),
                entry.get('clip_number', 0),
                entry.get('clip_path', ''),
                entry.get('start_time', ''),
                entry.get('end_time', ''),
                entry.get('duration_seconds', 0),
                entry.get('detection_method', ''),
                entry.get('detection_score', 0),
                entry.get('vertical', False),
                entry.get('captioned', False),
                entry.get('status', 'CREATED'),
                entry.get('created_at', datetime.now().isoformat()),
                entry.get('notes', '')
            ])

    def get_status(self) -> str:
        """Return summary of all tracked jobs."""
        if not self.csv_path.exists():
            return "No clip service tracker found."

        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            return "Tracker exists but no entries yet."

        total = len(rows)
        by_status = defaultdict(int)
        by_client = defaultdict(int)
        by_platform = defaultdict(int)

        for r in rows:
            by_status[r.get('status', 'UNKNOWN')] += 1
            by_client[r.get('client_name', 'unknown')] += 1
            by_platform[r.get('platform', 'unknown')] += 1

        lines = [
            f"=== CLIP SERVICE STATUS ===",
            f"Total clips: {total}",
            f"",
            f"By Status:"
        ]
        for status, count in sorted(by_status.items()):
            lines.append(f"  {status}: {count}")

        lines.append(f"\nBy Client:")
        for client, count in sorted(by_client.items()):
            lines.append(f"  {client}: {count}")

        lines.append(f"\nBy Platform:")
        for platform, count in sorted(by_platform.items()):
            lines.append(f"  {platform}: {count}")

        return "\n".join(lines)


class AutoClipService:
    """Main orchestrator for the clip service."""

    def __init__(
        self,
        output_dir: Optional[str] = None,
        client_name: str = "default",
        clip_duration: int = 30,
        num_clips: int = 5,
        vertical: bool = False,
        captions: bool = False,
        audio_threshold_db: float = -10.0,
        whisper_model: str = "base"
    ):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_BASE
        safe_path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.downloads_dir = self.output_dir / "downloads"
        self.clips_dir = self.output_dir / "clips"
        self.temp_dir = self.output_dir / "temp"

        for d in [self.downloads_dir, self.clips_dir, self.temp_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self.client_name = client_name
        self.clip_duration = clip_duration
        self.num_clips = num_clips
        self.vertical = vertical
        self.captions = captions

        self.peak_detector = AudioPeakDetector(
            threshold_db=audio_threshold_db,
            min_gap_seconds=max(clip_duration * 1.5, 30.0)
        )
        self.chat_analyzer = ChatDensityAnalyzer()
        self.clip_extractor = ClipExtractor()
        self.caption_gen = CaptionGenerator(model_name=whisper_model)
        self.tracker = ClipServiceTracker()

    def _url_to_id(self, url: str) -> str:
        """Generate a short deterministic ID from URL."""
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def _detect_platform(self, url: str) -> str:
        """Detect platform from URL."""
        url_lower = url.lower()
        if 'twitch.tv' in url_lower:
            return 'twitch'
        elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'kick.com' in url_lower:
            return 'kick'
        else:
            return 'unknown'

    def download_vod(self, url: str) -> Optional[Path]:
        """Download VOD using yt-dlp."""
        video_id = self._url_to_id(url)

        # Check for existing download
        for ext in ['mp4', 'webm', 'mkv', 'mov']:
            existing = self.downloads_dir / f"{video_id}.{ext}"
            if existing.exists() and existing.stat().st_size > 0:
                print(f"[INFO] Using cached download: {existing.name}")
                return existing

        print(f"[INFO] Downloading VOD: {url}")
        output_template = str(self.downloads_dir / f"{video_id}.%(ext)s")

        try:
            cmd = [
                'yt-dlp',
                '--format', 'best[ext=mp4]/best',
                '--output', output_template,
                '--no-playlist',
                '--socket-timeout', '30',
                url
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)

            for ext in ['mp4', 'webm', 'mkv', 'mov']:
                path = self.downloads_dir / f"{video_id}.{ext}"
                if path.exists():
                    print(f"[OK] Downloaded: {path.name} ({path.stat().st_size / (1024*1024):.1f} MB)")
                    return path

            print("[ERROR] Download succeeded but file not found")
            return None

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Download failed: {e.stderr[:200] if e.stderr else 'unknown error'}")
            return None
        except subprocess.TimeoutExpired:
            print("[ERROR] Download timed out (10 min limit)")
            return None
        except FileNotFoundError:
            print("[ERROR] yt-dlp not found. Install: pip install yt-dlp")
            return None

    def find_highlight_moments(
        self,
        video_path: Path,
        url: str,
        max_moments: int = 20
    ) -> List[Dict]:
        """Find highlight moments using audio peaks + chat density."""
        platform = self._detect_platform(url)
        video_duration = self.clip_extractor.get_video_duration(video_path)

        if video_duration <= 0:
            print("[WARN] Could not determine video duration")
            return self._generate_evenly_spaced(video_duration or 3600, max_moments)

        print(f"[INFO] Video duration: {_format_time(video_duration)}")

        # Method 1: Audio peak detection
        print("[INFO] Detecting audio peaks...")
        audio_peaks = self.peak_detector.detect_highlights(video_path, max_highlights=max_moments * 2)
        print(f"[INFO] Found {len(audio_peaks)} audio peaks")

        # Method 2: Chat density (Twitch only)
        chat_peaks = []
        if platform == 'twitch':
            print("[INFO] Analyzing chat density...")
            chat_path = self.chat_analyzer.download_chat(url, self.temp_dir)
            if chat_path:
                density = self.chat_analyzer.parse_chat_density(chat_path)
                chat_peaks = self.chat_analyzer.get_peak_chat_moments(
                    density, top_n=max_moments * 2
                )
                print(f"[INFO] Found {len(chat_peaks)} chat density peaks")
                # Cleanup
                try:
                    chat_path.unlink()
                except OSError:
                    pass
            else:
                print("[INFO] No chat replay available")

        # Merge and score moments
        moments = self._merge_highlight_sources(
            audio_peaks, chat_peaks, video_duration, max_moments
        )

        if not moments:
            print("[WARN] No highlights detected, using evenly spaced clips")
            moments = self._generate_evenly_spaced(video_duration, max_moments)

        return moments

    def _merge_highlight_sources(
        self,
        audio_peaks: List[Dict],
        chat_peaks: List[Dict],
        video_duration: float,
        max_moments: int
    ) -> List[Dict]:
        """Merge audio and chat peaks into scored highlight moments."""
        # Create time buckets (30s windows)
        bucket_size = 30.0
        num_buckets = int(video_duration / bucket_size) + 1
        scores = defaultdict(lambda: {'audio': 0.0, 'chat': 0.0, 'method': []})

        # Score from audio peaks
        for peak in audio_peaks:
            bucket = int(peak['time_seconds'] / bucket_size)
            if 0 <= bucket < num_buckets:
                # Normalize dB to 0-1 score (higher dB = louder = better)
                normalized = min(1.0, max(0.0, (peak['rms_db'] + 30) / 30.0))
                if normalized > scores[bucket]['audio']:
                    scores[bucket]['audio'] = normalized
                    if 'audio_peak' not in scores[bucket]['method']:
                        scores[bucket]['method'].append('audio_peak')

        # Score from chat density
        if chat_peaks:
            max_chat = max(p['message_count'] for p in chat_peaks) if chat_peaks else 1
            for peak in chat_peaks:
                bucket = int(peak['time_seconds'] / bucket_size)
                if 0 <= bucket < num_buckets:
                    normalized = peak['message_count'] / max(max_chat, 1)
                    if normalized > scores[bucket]['chat']:
                        scores[bucket]['chat'] = normalized
                        if 'chat_density' not in scores[bucket]['method']:
                            scores[bucket]['method'].append('chat_density')

        # Compute combined score (audio weighted 60%, chat 40%)
        ranked = []
        for bucket, data in scores.items():
            combined = data['audio'] * 0.6 + data['chat'] * 0.4
            if combined > 0:
                ranked.append({
                    'time_seconds': bucket * bucket_size,
                    'score': combined,
                    'method': '+'.join(data['method']) if data['method'] else 'combined',
                    'audio_score': data['audio'],
                    'chat_score': data['chat']
                })

        # Sort by score descending
        ranked.sort(key=lambda x: x['score'], reverse=True)

        # Select top moments with minimum gap
        min_gap = max(self.clip_duration * 1.5, 45.0)
        selected = []
        for candidate in ranked:
            too_close = False
            for existing in selected:
                if abs(candidate['time_seconds'] - existing['time_seconds']) < min_gap:
                    too_close = True
                    break
            if not too_close:
                # Ensure clip fits within video
                if candidate['time_seconds'] + self.clip_duration <= video_duration:
                    selected.append(candidate)
            if len(selected) >= max_moments:
                break

        # Sort chronologically
        selected.sort(key=lambda x: x['time_seconds'])
        return selected

    def _generate_evenly_spaced(self, duration: float, count: int) -> List[Dict]:
        """Fallback: generate evenly spaced clip positions."""
        if duration <= 0:
            duration = 3600

        interval = duration / (count + 1)
        moments = []
        for i in range(count):
            start = interval * (i + 1)
            if start + self.clip_duration <= duration:
                moments.append({
                    'time_seconds': start,
                    'score': 0.5,
                    'method': 'evenly_spaced',
                    'audio_score': 0.0,
                    'chat_score': 0.0
                })
        return moments

    def process_url(self, url: str) -> List[Path]:
        """Full pipeline for one URL. Returns list of created clip paths."""
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        print(f"Settings: {self.num_clips} clips, {self.clip_duration}s each, "
              f"vertical={self.vertical}, captions={self.captions}")
        print(f"{'='*60}\n")

        platform = self._detect_platform(url)
        video_id = self._url_to_id(url)
        job_id = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Step 1: Download
        video_path = self.download_vod(url)
        if not video_path:
            print("[FAIL] Could not download VOD")
            return []

        # Step 2: Find highlights
        moments = self.find_highlight_moments(video_path, url, max_moments=self.num_clips)
        print(f"\n[INFO] Selected {len(moments)} highlight moments:")
        for i, m in enumerate(moments, 1):
            print(f"  {i}. {_format_time(m['time_seconds'])} "
                  f"(score: {m['score']:.2f}, method: {m['method']})")

        # Step 3: Extract clips
        created_clips = []
        job_clips_dir = self.clips_dir / job_id
        job_clips_dir.mkdir(parents=True, exist_ok=True)
        safe_path(job_clips_dir)

        for i, moment in enumerate(moments[:self.num_clips], 1):
            print(f"\n[INFO] Creating clip {i}/{min(self.num_clips, len(moments))}...")

            start = moment['time_seconds']
            # Offset start slightly before the peak for context
            adjusted_start = max(0, start - 3)
            duration = self.clip_duration

            suffix = "_vertical" if self.vertical else ""
            clip_filename = f"clip_{i:02d}_{_format_time(adjusted_start).replace(':', '-')}{suffix}.mp4"
            clip_path = job_clips_dir / clip_filename

            # Extract clip
            result = self.clip_extractor.extract_clip(
                video_path=video_path,
                output_path=clip_path,
                start_seconds=adjusted_start,
                duration_seconds=duration,
                vertical=self.vertical
            )

            if not result:
                print(f"[WARN] Failed to extract clip {i}")
                continue

            # Step 4: Add captions if requested
            captioned = False
            if self.captions:
                print(f"[INFO] Generating captions for clip {i}...")
                transcript = self.caption_gen.transcribe_clip(clip_path)
                if transcript:
                    srt_path = job_clips_dir / f"clip_{i:02d}.srt"
                    srt_result = self.caption_gen.generate_srt(transcript, srt_path)
                    if srt_result:
                        captioned_path = job_clips_dir / f"clip_{i:02d}_captioned.mp4"
                        burn_result = self.clip_extractor.burn_captions(
                            clip_path, srt_path, captioned_path
                        )
                        if burn_result:
                            # Replace original with captioned version
                            clip_path.unlink()
                            burn_result.rename(clip_path)
                            captioned = True
                            print(f"[OK] Captions added to clip {i}")
                        else:
                            print(f"[WARN] Caption burn failed for clip {i}, keeping without captions")

            size_mb = clip_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Clip {i}: {clip_path.name} ({size_mb:.1f} MB)")
            created_clips.append(clip_path)

            # Track in ledger
            self.tracker.add_entry({
                'job_id': job_id,
                'client_name': self.client_name,
                'source_url': url,
                'platform': platform,
                'clip_number': i,
                'clip_path': str(clip_path),
                'start_time': _format_time(adjusted_start),
                'end_time': _format_time(adjusted_start + duration),
                'duration_seconds': duration,
                'detection_method': moment.get('method', 'unknown'),
                'detection_score': round(moment.get('score', 0), 3),
                'vertical': self.vertical,
                'captioned': captioned,
                'status': 'CREATED',
                'notes': f"audio={moment.get('audio_score', 0):.2f} chat={moment.get('chat_score', 0):.2f}"
            })

        print(f"\n[DONE] Created {len(created_clips)}/{self.num_clips} clips")
        print(f"[DONE] Output: {job_clips_dir}")
        return created_clips

    def process_batch(self, urls: List[str]) -> Dict[str, List[Path]]:
        """Process multiple URLs. Returns {url: [clip_paths]}."""
        results = {}
        total = len(urls)

        print(f"\n{'#'*60}")
        print(f"BATCH MODE: {total} VODs to process")
        print(f"{'#'*60}")

        for idx, url in enumerate(urls, 1):
            print(f"\n[BATCH {idx}/{total}]")
            try:
                clips = self.process_url(url)
                results[url] = clips
            except KeyboardInterrupt:
                print("\n[INTERRUPTED] Stopping batch processing")
                break
            except Exception as e:
                print(f"[ERROR] Failed to process {url}: {e}")
                results[url] = []
                continue

        # Summary
        total_clips = sum(len(c) for c in results.values())
        successful = sum(1 for c in results.values() if c)

        print(f"\n{'#'*60}")
        print(f"BATCH COMPLETE")
        print(f"  VODs processed: {successful}/{total}")
        print(f"  Total clips created: {total_clips}")
        print(f"  Output: {self.clips_dir}")
        print(f"{'#'*60}\n")

        return results

    def demo_mode(self, url: str):
        """Show what would happen without processing."""
        platform = self._detect_platform(url)
        video_id = self._url_to_id(url)

        print(f"\n{'='*60}")
        print(f"DEMO MODE")
        print(f"{'='*60}\n")

        print(f"URL: {url}")
        print(f"Platform: {platform}")
        print(f"Video ID: {video_id}")
        print(f"")
        print(f"Settings:")
        print(f"  Clips to extract: {self.num_clips}")
        print(f"  Clip duration: {self.clip_duration}s")
        print(f"  Vertical crop (9:16): {self.vertical}")
        print(f"  Auto-captions: {self.captions}")
        print(f"  Client: {self.client_name}")
        print(f"")
        print(f"Output directory: {self.clips_dir}")
        print(f"Tracker CSV: {self.tracker.csv_path}")
        print(f"")
        print(f"Pipeline steps:")
        print(f"  1. Download VOD via yt-dlp")
        print(f"  2. Extract audio, detect volume peaks (loud moments = hype)")
        if platform == 'twitch':
            print(f"  3. Download chat replay, compute message density per 10s window")
            print(f"  4. Merge audio peaks (60%) + chat density (40%) into combined score")
        else:
            print(f"  3. (Chat density: N/A for {platform})")
            print(f"  4. Rank moments by audio peak score")
        print(f"  5. Extract top {self.num_clips} clips at {self.clip_duration}s each")
        if self.vertical:
            print(f"  6. Crop to 9:16 vertical (center crop)")
        if self.captions:
            print(f"  7. Transcribe clips with Whisper, burn SRT captions")
        print(f"  8. Track in LEDGER/CLIP_SERVICE_TRACKER.csv")
        print(f"")
        print(f"Dependencies:")
        print(f"  yt-dlp:  {_check_cmd('yt-dlp')}")
        print(f"  ffmpeg:  {_check_cmd('ffmpeg')}")
        print(f"  ffprobe: {_check_cmd('ffprobe')}")
        print(f"  whisper: {'installed' if WHISPER_AVAILABLE else 'NOT installed'}")
        print(f"  numpy:   {'installed' if NUMPY_AVAILABLE else 'NOT installed (optional)'}")


def _check_cmd(cmd: str) -> str:
    """Check if command is available."""
    try:
        result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=10)
        # Get first line of version output
        version = result.stdout.strip().split('\n')[0][:60] if result.stdout else 'installed'
        return version
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return 'NOT installed'


def parse_batch_file(file_path: str) -> List[str]:
    """Read URLs from a batch file (one URL per line)."""
    path = Path(file_path)
    if not path.exists():
        print(f"[ERROR] Batch file not found: {file_path}")
        sys.exit(1)

    urls = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)

    if not urls:
        print(f"[ERROR] No URLs found in {file_path}")
        sys.exit(1)

    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Auto Clip Service - Extract highlight clips from streamer VODs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single VOD, 5 clips at 30s each
  python3 auto_clip_service.py --url "https://twitch.tv/videos/123456" --clips 5

  # Vertical + captions for TikTok
  python3 auto_clip_service.py --url "https://youtube.com/watch?v=xxx" --vertical --captions

  # Batch mode from file
  python3 auto_clip_service.py --batch urls.txt --clips 10 --duration 60 --vertical --captions

  # Check status
  python3 auto_clip_service.py --status

  # Demo mode (show what would happen)
  python3 auto_clip_service.py --demo --url "https://youtube.com/watch?v=xxx"
"""
    )

    parser.add_argument('--url', help='Single VOD URL to process')
    parser.add_argument('--batch', metavar='FILE', help='File with URLs (one per line)')
    parser.add_argument('--clips', type=int, default=5, help='Number of clips to extract (default: 5)')
    parser.add_argument('--duration', type=int, default=30, choices=[15, 30, 60],
                        help='Clip duration in seconds: 15, 30, or 60 (default: 30)')
    parser.add_argument('--vertical', action='store_true',
                        help='Crop to 9:16 vertical for TikTok/Shorts/Reels')
    parser.add_argument('--captions', action='store_true',
                        help='Auto-generate captions via Whisper')
    parser.add_argument('--client', default='default', help='Client name for tracking')
    parser.add_argument('--output', help='Output directory (default: OUTPUT/clips/)')
    parser.add_argument('--audio-threshold', type=float, default=-10.0,
                        help='Audio peak threshold in dB (default: -10.0, lower = more sensitive)')
    parser.add_argument('--whisper-model', default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size (default: base)')
    parser.add_argument('--status', action='store_true', help='Show clip service status')
    parser.add_argument('--demo', action='store_true', help='Demo mode - show plan without executing')

    args = parser.parse_args()

    # Status mode
    if args.status:
        tracker = ClipServiceTracker()
        print(tracker.get_status())
        return

    # Validate inputs
    if not args.url and not args.batch and not args.demo:
        parser.error("Must provide --url, --batch, --status, or --demo")

    if args.demo and not args.url:
        parser.error("--demo requires --url")

    # Build service
    service = AutoClipService(
        output_dir=args.output,
        client_name=args.client,
        clip_duration=args.duration,
        num_clips=args.clips,
        vertical=args.vertical,
        captions=args.captions,
        audio_threshold_db=args.audio_threshold,
        whisper_model=args.whisper_model
    )

    # Demo mode
    if args.demo:
        service.demo_mode(args.url)
        return

    # Batch mode
    if args.batch:
        urls = parse_batch_file(args.batch)
        if args.url:
            urls.insert(0, args.url)
        service.process_batch(urls)
        return

    # Single URL mode
    if args.url:
        clips = service.process_url(args.url)
        if clips:
            print(f"\n[RESULT] {len(clips)} clips ready:")
            for c in clips:
                print(f"  {c}")
        else:
            print("\n[RESULT] No clips created")
            sys.exit(1)


if __name__ == '__main__':
    main()
