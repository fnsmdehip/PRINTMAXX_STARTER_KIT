#!/usr/bin/env python3
"""Build a full-content, chunked context dump for the entire repository.

Outputs raw content chunks (not summaries) so downstream audits can load
context in manageable windows.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_DIR = BASE_DIR / "AUDIT"
SKIP_DIRS = {".git", ".idea", ".vscode", "__pycache__", ".pytest_cache"}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_binary(sample: bytes) -> bool:
    if not sample:
        return False
    if b"\x00" in sample:
        return True
    # If many non-printable bytes exist, treat as binary.
    nonprint = sum(1 for b in sample if b < 9 or (13 < b < 32))
    return (nonprint / max(1, len(sample))) > 0.30


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def collect_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        filtered: List[str] = []
        for d in dirnames:
            if d in SKIP_DIRS:
                continue
            child = dpath / d
            # Prevent recursive re-ingestion of prior raw context dumps.
            if child.parent == AUDIT_DIR and d.startswith("FULL_CONTEXT_"):
                continue
            filtered.append(d)
        dirnames[:] = filtered
        for name in filenames:
            files.append(dpath / name)
    files.sort()
    return files


def split_text_chunks(text: str, chunk_chars: int) -> List[Tuple[int, int, str]]:
    out: List[Tuple[int, int, str]] = []
    n = len(text)
    i = 0
    while i < n:
        j = min(n, i + chunk_chars)
        out.append((i, j, text[i:j]))
        i = j
    if not out:
        out.append((0, 0, ""))
    return out


def process_file(path: Path, chunk_chars: int, preview_bytes: int) -> Dict[str, Any]:
    try:
        st = path.stat()
    except Exception as exc:
        return {
            "ok": False,
            "path": str(path),
            "error": str(exc),
            "chunks": [],
        }

    try:
        rel = path.relative_to(BASE_DIR).as_posix()
    except Exception:
        rel = str(path)

    mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    try:
        data = path.read_bytes()
    except Exception as exc:
        return {
            "ok": False,
            "path": rel,
            "size_bytes": int(st.st_size),
            "mtime_iso": mtime,
            "error": str(exc),
            "chunks": [],
        }

    digest = sha256_bytes(data)
    sample = data[:4096]
    binary = is_binary(sample)

    if binary:
        preview = data[:preview_bytes].hex()
        return {
            "ok": True,
            "path": rel,
            "kind": "binary",
            "size_bytes": int(st.st_size),
            "mtime_iso": mtime,
            "sha256": digest,
            "chunks": [
                {
                    "chunk_index": 0,
                    "char_start": 0,
                    "char_end": 0,
                    "content": "",
                    "binary_hex_preview": preview,
                }
            ],
            "error": "",
        }

    text = data.decode("utf-8", errors="replace")
    split = split_text_chunks(text, max(256, chunk_chars))
    chunks = []
    for idx, (start, end, content) in enumerate(split):
        chunks.append(
            {
                "chunk_index": idx,
                "char_start": start,
                "char_end": end,
                "content": content,
                "binary_hex_preview": "",
            }
        )

    return {
        "ok": True,
        "path": rel,
        "kind": "text",
        "size_bytes": int(st.st_size),
        "mtime_iso": mtime,
        "sha256": digest,
        "chunks": chunks,
        "error": "",
    }


class ChunkWriter:
    def __init__(self, chunk_dir: Path, max_records_per_shard: int, compress: bool) -> None:
        self.chunk_dir = chunk_dir
        self.max_records = max(200, max_records_per_shard)
        self.compress = bool(compress)
        self.chunk_dir.mkdir(parents=True, exist_ok=True)
        self.shard_idx = 0
        self.rec_in_shard = 0
        self.handle = None
        self.shard_paths: List[str] = []

    def _open_new(self) -> None:
        if self.handle is not None:
            self.handle.close()
        suffix = ".jsonl.gz" if self.compress else ".jsonl"
        path = self.chunk_dir / f"context_shard_{self.shard_idx:05d}{suffix}"
        if self.compress:
            self.handle = gzip.open(path, "wt", encoding="utf-8")
        else:
            self.handle = open(path, "w", encoding="utf-8")
        self.shard_paths.append(path.as_posix())
        self.rec_in_shard = 0
        self.shard_idx += 1

    def write_record(self, record: Dict[str, Any]) -> None:
        if self.handle is None or self.rec_in_shard >= self.max_records:
            self._open_new()
        self.handle.write(json.dumps(record, ensure_ascii=True) + "\n")
        self.rec_in_shard += 1

    def close(self) -> None:
        if self.handle is not None:
            self.handle.close()
            self.handle = None


def write_manifest_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "path",
                "kind",
                "size_bytes",
                "mtime_iso",
                "sha256",
                "chunk_count",
                "chunk_records_written",
                "is_duplicate",
                "primary_path",
                "error",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "path": row.get("path", ""),
                    "kind": row.get("kind", ""),
                    "size_bytes": row.get("size_bytes", 0),
                    "mtime_iso": row.get("mtime_iso", ""),
                    "sha256": row.get("sha256", ""),
                    "chunk_count": row.get("chunk_count", 0),
                    "chunk_records_written": row.get("chunk_records_written", 0),
                    "is_duplicate": row.get("is_duplicate", False),
                    "primary_path": row.get("primary_path", ""),
                    "error": row.get("error", ""),
                }
            )


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Create full-content chunk context dump")
    ap.add_argument("--write", action="store_true", help="Generate dump")
    ap.add_argument("--tag", default="", help="Output tag (default: YYYY_MM_DD)")
    ap.add_argument("--chunk-chars", type=int, default=5000, help="Text chunk size")
    ap.add_argument("--workers", type=int, default=8, help="Parallel file workers")
    ap.add_argument("--max-records-per-shard", type=int, default=2000, help="JSONL records per shard")
    ap.add_argument("--binary-preview-bytes", type=int, default=256, help="Hex preview bytes for binary files")
    ap.add_argument(
        "--compress-shards",
        action="store_true",
        default=True,
        help="Write chunk shards as .jsonl.gz (default: enabled)",
    )
    ap.add_argument("--no-compress-shards", dest="compress_shards", action="store_false", help="Write plain .jsonl shards")
    ap.add_argument(
        "--dedupe-content",
        action="store_true",
        default=True,
        help="Write full chunks once per sha256 and reference duplicates (default: enabled)",
    )
    ap.add_argument("--no-dedupe-content", dest="dedupe_content", action="store_false", help="Write duplicate file chunks fully")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.write:
        print("full_context_swarm_dump: pass --write")
        return 2

    tag = args.tag.strip() or datetime.now().strftime("%Y_%m_%d")
    out_dir = AUDIT_DIR / f"FULL_CONTEXT_{tag}"
    chunks_dir = out_dir / "chunks"
    manifest_csv = out_dir / "file_manifest.csv"
    summary_json = out_dir / "summary.json"

    files = collect_files(BASE_DIR)
    writer = ChunkWriter(chunks_dir, args.max_records_per_shard, compress=bool(args.compress_shards))

    manifests: List[Dict[str, Any]] = []
    text_files = 0
    binary_files = 0
    error_files = 0
    total_chunks = 0
    total_bytes = 0
    dedupe_hits = 0
    dedupe_bytes = 0
    seen_sha_primary: Dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {
            ex.submit(process_file, path, args.chunk_chars, args.binary_preview_bytes): path
            for path in files
        }
        for fut in as_completed(futures):
            result = fut.result()
            if not bool(result.get("ok", False)):
                manifests.append(
                    {
                        "path": result.get("path", ""),
                        "kind": "error",
                        "size_bytes": int(result.get("size_bytes", 0)),
                        "mtime_iso": result.get("mtime_iso", ""),
                        "sha256": "",
                        "chunk_count": 0,
                        "chunk_records_written": 0,
                        "is_duplicate": False,
                        "primary_path": "",
                        "error": result.get("error", ""),
                    }
                )
                error_files += 1
                continue

            path = str(result.get("path", ""))
            kind = str(result.get("kind", "text"))
            size_bytes = int(result.get("size_bytes", 0))
            mtime_iso = str(result.get("mtime_iso", ""))
            digest = str(result.get("sha256", ""))
            chunks = result.get("chunks", [])
            if not isinstance(chunks, list):
                chunks = []

            chunk_count = len(chunks)
            primary_path = seen_sha_primary.get(digest, "") if digest else ""
            is_duplicate = bool(args.dedupe_content and digest and primary_path and primary_path != path)

            if digest and not primary_path:
                seen_sha_primary[digest] = path
                primary_path = path

            chunk_records_written = 0
            if is_duplicate:
                dedupe_hits += 1
                dedupe_bytes += size_bytes
                writer.write_record(
                    {
                        "path": path,
                        "kind": kind,
                        "sha256": digest,
                        "is_duplicate": True,
                        "primary_path": primary_path,
                        "ref_only": True,
                        "chunk_index": 0,
                        "char_start": 0,
                        "char_end": 0,
                        "content": "",
                        "binary_hex_preview": "",
                    }
                )
                chunk_records_written = 1
            else:
                for chunk in chunks:
                    writer.write_record(
                        {
                            "path": path,
                            "kind": kind,
                            "sha256": digest,
                            "is_duplicate": False,
                            "primary_path": primary_path,
                            "ref_only": False,
                            "chunk_index": int(chunk.get("chunk_index", 0)),
                            "char_start": int(chunk.get("char_start", 0)),
                            "char_end": int(chunk.get("char_end", 0)),
                            "content": str(chunk.get("content", "")),
                            "binary_hex_preview": str(chunk.get("binary_hex_preview", "")),
                        }
                    )
                chunk_records_written = len(chunks)

            manifests.append(
                {
                    "path": path,
                    "kind": kind,
                    "size_bytes": size_bytes,
                    "mtime_iso": mtime_iso,
                    "sha256": digest,
                    "chunk_count": chunk_count,
                    "chunk_records_written": chunk_records_written,
                    "is_duplicate": is_duplicate,
                    "primary_path": primary_path,
                    "error": "",
                }
            )
            total_chunks += chunk_count
            total_bytes += size_bytes
            if kind == "text":
                text_files += 1
            else:
                binary_files += 1

    writer.close()
    manifests.sort(key=lambda r: str(r.get("path", "")))
    write_manifest_csv(manifest_csv, manifests)

    summary = {
        "generated_at": now_iso(),
        "tag": tag,
        "base_dir": str(BASE_DIR),
        "output_dir": str(out_dir),
        "files_total": len(files),
        "text_files": text_files,
        "binary_files": binary_files,
        "error_files": error_files,
        "total_chunks": total_chunks,
        "total_bytes": total_bytes,
        "dedupe_enabled": bool(args.dedupe_content),
        "dedupe_hits": dedupe_hits,
        "dedupe_bytes": dedupe_bytes,
        "compress_shards": bool(args.compress_shards),
        "shard_count": writer.shard_idx,
        "shard_paths": writer.shard_paths,
        "chunk_chars": int(args.chunk_chars),
        "workers": int(args.workers),
        "max_records_per_shard": int(args.max_records_per_shard),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("full_context_swarm_dump: wrote")
    print(f"- {summary_json}")
    print(f"- {manifest_csv}")
    print(f"- {chunks_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
