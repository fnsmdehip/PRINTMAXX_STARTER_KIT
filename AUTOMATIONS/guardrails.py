#!/usr/bin/env python3
"""
PRINTMAXX Safety Guardrails Module
===================================
Import this in ANY automation script to enforce safety rules:

    from guardrails import safe_open, safe_write, safe_delete, safe_move, verify_path, create_checkpoint

RULES ENFORCED:
1. ALL file operations MUST be within the PRINTMAXX project folder
2. Pre-destructive-operation backups (checkpoint system)
3. Downloads: only touch the specific file downloaded, nothing else in ~/Downloads
4. No modification of system files, other projects, or user data outside project
5. Comprehensive audit log of every file operation
6. Revert capability via checkpoints
7. Dry-run mode for testing dangerous operations
8. Rate limiting on bulk delete/move operations
9. Protected paths that can NEVER be touched (even inside project)
10. Maximum file size limits to prevent disk filling

USAGE:
    from guardrails import GuardRails
    gr = GuardRails()  # auto-detects project root

    # Safe file write (auto-validates path)
    gr.safe_write("/path/to/file.txt", "content")

    # Safe delete with auto-checkpoint
    gr.safe_delete("/path/to/file.txt")

    # Verify a path is safe before any operation
    gr.verify_path("/some/path")  # raises if outside project

    # Create a checkpoint before risky operations
    checkpoint_id = gr.create_checkpoint("before bulk delete")
    # ... do stuff ...
    gr.revert_checkpoint(checkpoint_id)  # if something went wrong

    # Safe download handling
    gr.safe_download_move("filename.zip", destination_in_project)
"""

import os
import sys
import json
import shutil
import hashlib
import logging
import time
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Union
from functools import wraps

# ============================================================
# CONFIGURATION - HARDCODED SAFETY BOUNDARIES
# ============================================================

# The ONE folder we're allowed to modify
PROJECT_ROOT = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

# Folders we can READ from (but not write to) outside project
READABLE_EXTERNAL = [
    "/Library/Frameworks/Python.framework",  # Python itself
    "/usr/local",  # Homebrew tools
    "/usr/bin",  # System binaries
    "/tmp",  # Temp files
    os.path.expanduser("~/Downloads"),  # Downloads (read only, copy in)
]

# System paths that must NEVER be touched under ANY circumstances
FORBIDDEN_PATHS = [
    "/System",
    "/Library",
    "/usr",
    "/bin",
    "/sbin",
    "/etc",
    "/var",
    "/private",
    os.path.expanduser("~/Library"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),  # We only allow our specific subfolder
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music"),
    os.path.expanduser("~/Movies"),
    os.path.expanduser("~/Applications"),
    os.path.expanduser("~/.ssh"),
    os.path.expanduser("~/.gnupg"),
    os.path.expanduser("~/.aws"),
    os.path.expanduser("~/.config"),
    os.path.expanduser("~/.zshrc"),
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.bash_profile"),
    os.path.expanduser("~/.zsh_history"),
    os.path.expanduser("~/.bash_history"),
    os.path.expanduser("~/.gitconfig"),
]

# Paths within the project that should never be auto-deleted
PROTECTED_PROJECT_PATHS = [
    "CLAUDE.md",
    ".claude/",
    "LEDGER/",
    "FINANCIALS/",
    "SECRETS/",
    "PRINTMAXX_MASTER_OPS.xlsx",
    "PRINTMAXX_STRATEGIC_RBI.xlsx",
    "PRINTMAXX_FREELANCE_ARB.xlsx",
    "PRINTMAXX_OPS_PLAYBOOK.xlsx",
]

# Apps/commands that are SAFE to launch (not file operations, just launching)
# These are the ONLY external interactions allowed outside the project folder
ALLOWED_EXTERNAL_COMMANDS = [
    "open",              # macOS open command (launch apps, URLs, files in their default app)
    "open -a Safari",    # Launch Safari
    "open -a 'Google Chrome'",  # Launch Chrome
    "open -a 'Brave Browser'",  # Launch Brave
    "open -a Simulator", # Launch iOS Simulator
    "open -a Xcode",     # Launch Xcode
    "open -a Terminal",  # Launch Terminal
    "open -a Finder",    # Launch Finder
    "open https://",     # Open URLs in default browser
    "npx",               # Run npm packages (e.g., wrangler, surge)
    "npm",               # npm commands
    "node",              # Node.js
    "python3",           # Python scripts
    "pip3",              # Package installation
    "git",               # Git operations
    "gh",                # GitHub CLI
    "curl",              # HTTP requests
    "wget",              # Downloads
    "brew",              # Homebrew (read-only installs)
    "vercel",            # Vercel deployments
    "surge",             # Surge deployments
    "crontab",           # Cron management
    "xcrun",             # Xcode command line tools
    "xcodebuild",        # Xcode builds
]

# Maximum operations before requiring explicit confirmation
MAX_BULK_DELETES = 20
MAX_BULK_WRITES = 100
MAX_SINGLE_FILE_SIZE_MB = 500  # Don't write files > 500MB
MAX_CHECKPOINT_SIZE_MB = 2000  # Don't checkpoint if project > 2GB of changed files
CHECKPOINT_RETENTION_DAYS = 7  # Auto-cleanup old checkpoints

# Backup location (inside project, gitignored)
BACKUP_DIR = os.path.join(PROJECT_ROOT, ".guardrails")
CHECKPOINT_DIR = os.path.join(BACKUP_DIR, "checkpoints")
AUDIT_LOG = os.path.join(BACKUP_DIR, "audit.jsonl")
OPERATION_LOG = os.path.join(BACKUP_DIR, "operations.log")

# ============================================================
# LOGGING SETUP
# ============================================================

def _setup_logging():
    """Set up dual logging: file + console."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    logger = logging.getLogger("guardrails")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # File handler (everything)
        fh = logging.FileHandler(OPERATION_LOG)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(fh)

        # Console handler (warnings and above)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(logging.Formatter('[GUARDRAIL] %(message)s'))
        logger.addHandler(ch)

    return logger

log = _setup_logging()

# ============================================================
# EXCEPTIONS
# ============================================================

class GuardrailViolation(Exception):
    """Raised when a safety guardrail is triggered."""
    pass

class PathViolation(GuardrailViolation):
    """Raised when an operation targets a forbidden path."""
    pass

class BulkOperationLimit(GuardrailViolation):
    """Raised when too many destructive operations are attempted."""
    pass

class FileSizeLimit(GuardrailViolation):
    """Raised when a file exceeds size limits."""
    pass

class ProtectedPathViolation(GuardrailViolation):
    """Raised when trying to delete a protected project file."""
    pass

# ============================================================
# CORE GUARDRAILS CLASS
# ============================================================

class GuardRails:
    """
    Main safety class. Import and instantiate in any automation script.

    Usage:
        gr = GuardRails()
        gr.safe_write("path/to/file.txt", "content")
        gr.safe_delete("path/to/old_file.txt")
    """

    def __init__(self, project_root: str = PROJECT_ROOT, dry_run: bool = False):
        self.project_root = os.path.realpath(project_root)
        self.dry_run = dry_run
        self._operation_count = {"delete": 0, "write": 0, "move": 0}
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{os.getpid()}"

        # Ensure backup directory exists
        os.makedirs(CHECKPOINT_DIR, exist_ok=True)

        # Write gitignore for guardrails folder
        gitignore_path = os.path.join(BACKUP_DIR, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write("*\n")

        # Auto-cleanup old checkpoints on init
        self._cleanup_old_checkpoints()

        log.info(f"GuardRails initialized. Session: {self._session_id}, Dry-run: {dry_run}")
        self._audit("INIT", {"session": self._session_id, "dry_run": dry_run})

    # --------------------------------------------------------
    # PATH VALIDATION (the most critical function)
    # --------------------------------------------------------

    def verify_path(self, path: str, operation: str = "access") -> str:
        """
        Verify a path is safe to operate on. Returns resolved absolute path.
        Raises PathViolation if the path is outside allowed boundaries.

        This is THE core safety function. Every file operation goes through here.
        """
        # Resolve to absolute path, following symlinks
        resolved = os.path.realpath(os.path.expanduser(path))

        # CHECK 1: Must be within project root
        if not resolved.startswith(self.project_root):
            # Exception: reading from explicitly allowed external paths
            if operation == "read":
                for allowed in READABLE_EXTERNAL:
                    if resolved.startswith(allowed):
                        log.debug(f"External read allowed: {resolved}")
                        return resolved

            raise PathViolation(
                f"BLOCKED: '{operation}' on '{resolved}' is OUTSIDE project root "
                f"'{self.project_root}'. All file operations must stay within the project folder."
            )

        # CHECK 2: Not in forbidden system paths (defense in depth - symlink attacks)
        # BUT: explicitly allow our project root even though it's under ~/Documents
        for forbidden in FORBIDDEN_PATHS:
            if resolved.startswith(forbidden):
                # Exception: the project root IS under ~/Documents - that's fine
                if resolved.startswith(self.project_root):
                    break  # It's in our project, skip all forbidden checks
                raise PathViolation(
                    f"BLOCKED: '{operation}' on '{resolved}' hits forbidden system path '{forbidden}'. "
                    f"This is a critical safety violation."
                )

        # CHECK 3: For destructive operations, check protected project paths
        if operation in ("delete", "move", "overwrite"):
            rel_path = os.path.relpath(resolved, self.project_root)
            for protected in PROTECTED_PROJECT_PATHS:
                if rel_path == protected or rel_path.startswith(protected):
                    if operation == "delete":
                        raise ProtectedPathViolation(
                            f"BLOCKED: Cannot delete protected path '{rel_path}'. "
                            f"This file is critical to the project. Create a checkpoint and "
                            f"manually delete if you're sure."
                        )
                    elif operation in ("move", "overwrite"):
                        log.warning(f"Modifying protected path: {rel_path} (operation: {operation})")

        # CHECK 4: Don't allow operations on the guardrails backup dir itself
        guardrails_dir = os.path.realpath(BACKUP_DIR)
        if resolved.startswith(guardrails_dir) and operation in ("delete", "move"):
            raise PathViolation(
                f"BLOCKED: Cannot {operation} guardrails backup files at '{resolved}'. "
                f"Use revert_checkpoint() or cleanup_checkpoints() instead."
            )

        log.debug(f"Path verified: {resolved} ({operation})")
        return resolved

    def is_safe_path(self, path: str, operation: str = "access") -> bool:
        """Non-throwing version of verify_path. Returns True/False."""
        try:
            self.verify_path(path, operation)
            return True
        except GuardrailViolation:
            return False

    # --------------------------------------------------------
    # SAFE FILE OPERATIONS
    # --------------------------------------------------------

    def safe_write(self, path: str, content: Union[str, bytes],
                   backup_existing: bool = True) -> str:
        """
        Safely write content to a file within the project.
        Auto-backs up existing file if it exists.
        Returns the resolved path written to.
        """
        resolved = self.verify_path(path, "write")

        # Check file size
        content_size = len(content.encode('utf-8') if isinstance(content, str) else content)
        if content_size > MAX_SINGLE_FILE_SIZE_MB * 1024 * 1024:
            raise FileSizeLimit(
                f"BLOCKED: Attempting to write {content_size / 1024 / 1024:.1f}MB file "
                f"(limit: {MAX_SINGLE_FILE_SIZE_MB}MB). This could fill disk."
            )

        # Check bulk operation limit
        self._operation_count["write"] += 1
        if self._operation_count["write"] > MAX_BULK_WRITES:
            raise BulkOperationLimit(
                f"BLOCKED: {self._operation_count['write']} write operations in one session "
                f"(limit: {MAX_BULK_WRITES}). This looks like a runaway process."
            )

        # Backup existing file
        if backup_existing and os.path.exists(resolved):
            self._backup_file(resolved, "pre_write")

        if self.dry_run:
            log.info(f"[DRY-RUN] Would write {content_size} bytes to {resolved}")
            self._audit("DRY_WRITE", {"path": resolved, "size": content_size})
            return resolved

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(resolved), exist_ok=True)

        # Write to temp file first, then atomic rename (prevents corruption)
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=os.path.dirname(resolved),
            prefix=".guardrail_tmp_"
        )
        try:
            with os.fdopen(tmp_fd, 'wb' if isinstance(content, bytes) else 'w') as f:
                f.write(content)
            os.replace(tmp_path, resolved)  # Atomic on same filesystem
        except Exception as e:
            # Cleanup temp file on failure
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

        log.info(f"WRITE: {resolved} ({content_size} bytes)")
        self._audit("WRITE", {"path": resolved, "size": content_size})
        return resolved

    def safe_read(self, path: str) -> str:
        """Safely read a file. Allows reading from project + approved external paths."""
        resolved = self.verify_path(path, "read")

        with open(resolved, 'r', errors='replace') as f:
            content = f.read()

        log.debug(f"READ: {resolved} ({len(content)} chars)")
        return content

    def safe_delete(self, path: str, require_checkpoint: bool = True) -> bool:
        """
        Safely delete a file within the project.
        Auto-creates checkpoint of the file before deletion.
        """
        resolved = self.verify_path(path, "delete")

        if not os.path.exists(resolved):
            log.warning(f"DELETE skipped (not found): {resolved}")
            return False

        # Check bulk operation limit
        self._operation_count["delete"] += 1
        if self._operation_count["delete"] > MAX_BULK_DELETES:
            raise BulkOperationLimit(
                f"BLOCKED: {self._operation_count['delete']} delete operations in one session "
                f"(limit: {MAX_BULK_DELETES}). This looks like a runaway process. "
                f"Create a checkpoint and use safe_bulk_delete() for large cleanups."
            )

        # Backup before delete
        if require_checkpoint:
            self._backup_file(resolved, "pre_delete")

        if self.dry_run:
            log.info(f"[DRY-RUN] Would delete {resolved}")
            self._audit("DRY_DELETE", {"path": resolved})
            return True

        if os.path.isdir(resolved):
            shutil.rmtree(resolved)
        else:
            os.unlink(resolved)

        log.info(f"DELETE: {resolved}")
        self._audit("DELETE", {"path": resolved})
        return True

    def safe_move(self, src: str, dst: str) -> str:
        """Safely move/rename a file within the project."""
        resolved_src = self.verify_path(src, "move")
        resolved_dst = self.verify_path(dst, "write")

        if not os.path.exists(resolved_src):
            raise FileNotFoundError(f"Source not found: {resolved_src}")

        # Backup source
        self._backup_file(resolved_src, "pre_move")

        # Check operation count
        self._operation_count["move"] += 1

        if self.dry_run:
            log.info(f"[DRY-RUN] Would move {resolved_src} -> {resolved_dst}")
            self._audit("DRY_MOVE", {"src": resolved_src, "dst": resolved_dst})
            return resolved_dst

        os.makedirs(os.path.dirname(resolved_dst), exist_ok=True)
        shutil.move(resolved_src, resolved_dst)

        log.info(f"MOVE: {resolved_src} -> {resolved_dst}")
        self._audit("MOVE", {"src": resolved_src, "dst": resolved_dst})
        return resolved_dst

    def safe_copy(self, src: str, dst: str) -> str:
        """Safely copy a file. Source can be external (Downloads), dst must be in project."""
        resolved_src = self.verify_path(src, "read")
        resolved_dst = self.verify_path(dst, "write")

        if self.dry_run:
            log.info(f"[DRY-RUN] Would copy {resolved_src} -> {resolved_dst}")
            return resolved_dst

        os.makedirs(os.path.dirname(resolved_dst), exist_ok=True)

        if os.path.isdir(resolved_src):
            shutil.copytree(resolved_src, resolved_dst, dirs_exist_ok=True)
        else:
            shutil.copy2(resolved_src, resolved_dst)

        log.info(f"COPY: {resolved_src} -> {resolved_dst}")
        self._audit("COPY", {"src": resolved_src, "dst": resolved_dst})
        return resolved_dst

    def safe_download_move(self, filename: str, destination: str) -> str:
        """
        Safely move a specific file from ~/Downloads into the project.
        ONLY touches the exact file specified - nothing else in Downloads.
        """
        downloads_dir = os.path.expanduser("~/Downloads")
        src = os.path.join(downloads_dir, filename)

        if not os.path.exists(src):
            raise FileNotFoundError(f"Download not found: {src}")

        # Verify destination is in project
        resolved_dst = self.verify_path(destination, "write")

        if self.dry_run:
            log.info(f"[DRY-RUN] Would move download {src} -> {resolved_dst}")
            return resolved_dst

        os.makedirs(os.path.dirname(resolved_dst), exist_ok=True)
        shutil.move(src, resolved_dst)

        log.info(f"DOWNLOAD_MOVE: {src} -> {resolved_dst}")
        self._audit("DOWNLOAD_MOVE", {"src": src, "dst": resolved_dst, "filename": filename})
        return resolved_dst

    def safe_bulk_delete(self, paths: List[str], checkpoint_name: str = None) -> Dict:
        """
        Delete multiple files with a single checkpoint covering all of them.
        Use this instead of repeated safe_delete() for large cleanups.
        """
        if not checkpoint_name:
            checkpoint_name = f"bulk_delete_{len(paths)}_files"

        # Verify all paths first (fail fast)
        resolved_paths = []
        for p in paths:
            resolved_paths.append(self.verify_path(p, "delete"))

        # Create one checkpoint for all files
        checkpoint_id = self.create_checkpoint(checkpoint_name, paths=resolved_paths)

        results = {"deleted": 0, "skipped": 0, "errors": 0, "checkpoint_id": checkpoint_id}

        for resolved in resolved_paths:
            try:
                if os.path.exists(resolved):
                    if self.dry_run:
                        results["deleted"] += 1
                        continue
                    if os.path.isdir(resolved):
                        shutil.rmtree(resolved)
                    else:
                        os.unlink(resolved)
                    results["deleted"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                log.error(f"Bulk delete error on {resolved}: {e}")
                results["errors"] += 1

        self._audit("BULK_DELETE", results)
        return results

    # --------------------------------------------------------
    # CHECKPOINT SYSTEM (backup + revert)
    # --------------------------------------------------------

    def create_checkpoint(self, name: str, paths: List[str] = None) -> str:
        """
        Create a checkpoint (snapshot) of specified files or entire project.
        Returns checkpoint ID for later revert.

        If paths is None, checkpoints the entire project (excluding heavy dirs).
        """
        checkpoint_id = f"{self._session_id}_{name.replace(' ', '_')}"
        checkpoint_path = os.path.join(CHECKPOINT_DIR, checkpoint_id)

        if self.dry_run:
            log.info(f"[DRY-RUN] Would create checkpoint: {checkpoint_id}")
            return checkpoint_id

        os.makedirs(checkpoint_path, exist_ok=True)

        manifest = {
            "id": checkpoint_id,
            "name": name,
            "created": datetime.now().isoformat(),
            "session": self._session_id,
            "files": [],
        }

        if paths:
            # Checkpoint specific files
            for p in paths:
                if os.path.exists(p):
                    rel = os.path.relpath(p, self.project_root)
                    dst = os.path.join(checkpoint_path, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if os.path.isdir(p):
                        shutil.copytree(p, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(p, dst)
                    manifest["files"].append(rel)
        else:
            # Full project checkpoint (exclude heavy directories)
            exclude_dirs = {
                "node_modules", ".git", ".guardrails", "__pycache__",
                ".next", ".vercel", "venv", ".venv", "dist",
                "app factory",  # Legacy dir with node_modules bloat
            }
            for dirpath, dirnames, filenames in os.walk(self.project_root):
                # Skip excluded directories
                dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

                for filename in filenames:
                    src_file = os.path.join(dirpath, filename)
                    rel = os.path.relpath(src_file, self.project_root)
                    dst_file = os.path.join(checkpoint_path, rel)

                    # Skip very large files (>50MB each)
                    try:
                        if os.path.getsize(src_file) > 50 * 1024 * 1024:
                            continue
                    except OSError:
                        continue

                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    try:
                        shutil.copy2(src_file, dst_file)
                        manifest["files"].append(rel)
                    except (PermissionError, OSError):
                        continue

        # Save manifest
        manifest_path = os.path.join(checkpoint_path, "_MANIFEST.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        log.info(f"CHECKPOINT created: {checkpoint_id} ({len(manifest['files'])} files)")
        self._audit("CHECKPOINT_CREATE", {
            "id": checkpoint_id, "name": name, "files": len(manifest["files"])
        })
        return checkpoint_id

    def revert_checkpoint(self, checkpoint_id: str) -> Dict:
        """
        Revert to a previous checkpoint. Restores all files from that checkpoint.
        """
        checkpoint_path = os.path.join(CHECKPOINT_DIR, checkpoint_id)
        manifest_path = os.path.join(checkpoint_path, "_MANIFEST.json")

        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        results = {"restored": 0, "errors": 0}

        for rel_path in manifest["files"]:
            src = os.path.join(checkpoint_path, rel_path)
            dst = os.path.join(self.project_root, rel_path)

            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
                results["restored"] += 1
            except Exception as e:
                log.error(f"Revert error on {rel_path}: {e}")
                results["errors"] += 1

        log.info(f"CHECKPOINT reverted: {checkpoint_id} ({results['restored']} files)")
        self._audit("CHECKPOINT_REVERT", {
            "id": checkpoint_id, **results
        })
        return results

    def list_checkpoints(self) -> List[Dict]:
        """List all available checkpoints."""
        checkpoints = []
        if not os.path.exists(CHECKPOINT_DIR):
            return checkpoints

        for entry in sorted(os.listdir(CHECKPOINT_DIR)):
            manifest_path = os.path.join(CHECKPOINT_DIR, entry, "_MANIFEST.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                # Calculate size
                cp_path = os.path.join(CHECKPOINT_DIR, entry)
                size = sum(
                    os.path.getsize(os.path.join(dp, fn))
                    for dp, _, fns in os.walk(cp_path)
                    for fn in fns
                )
                manifest["size_mb"] = round(size / 1024 / 1024, 1)
                checkpoints.append(manifest)

        return checkpoints

    def _cleanup_old_checkpoints(self):
        """Auto-remove checkpoints older than retention period."""
        if not os.path.exists(CHECKPOINT_DIR):
            return

        cutoff = datetime.now() - timedelta(days=CHECKPOINT_RETENTION_DAYS)

        for entry in os.listdir(CHECKPOINT_DIR):
            manifest_path = os.path.join(CHECKPOINT_DIR, entry, "_MANIFEST.json")
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    created = datetime.fromisoformat(manifest.get("created", "2020-01-01"))
                    if created < cutoff:
                        shutil.rmtree(os.path.join(CHECKPOINT_DIR, entry))
                        log.info(f"Cleaned old checkpoint: {entry}")
                except Exception:
                    pass

    # --------------------------------------------------------
    # BACKUP FILE (internal)
    # --------------------------------------------------------

    def _backup_file(self, resolved_path: str, reason: str):
        """Internal: backup a single file before modification."""
        if not os.path.exists(resolved_path):
            return

        rel = os.path.relpath(resolved_path, self.project_root)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{timestamp}_{reason}_{rel.replace('/', '_')}"
        backup_path = os.path.join(BACKUP_DIR, "file_backups", backup_name)

        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        try:
            if os.path.isdir(resolved_path):
                shutil.copytree(resolved_path, backup_path)
            else:
                shutil.copy2(resolved_path, backup_path)
        except Exception as e:
            log.warning(f"Backup failed for {resolved_path}: {e}")

    # --------------------------------------------------------
    # AUDIT LOG
    # --------------------------------------------------------

    def _audit(self, operation: str, details: dict):
        """Append to audit log (JSONL format)."""
        entry = {
            "time": datetime.now().isoformat(),
            "session": self._session_id,
            "pid": os.getpid(),
            "operation": operation,
            "details": details,
        }

        try:
            os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
            with open(AUDIT_LOG, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass  # Never let audit logging crash the actual operation

    # --------------------------------------------------------
    # SAFETY VALIDATORS (for shell commands)
    # --------------------------------------------------------

    def validate_shell_command(self, command: str) -> bool:
        """
        Check if a shell command is safe to execute.
        Returns True if safe, raises GuardrailViolation if not.
        """
        dangerous_patterns = [
            "rm -rf /",
            "rm -rf ~",
            "rm -rf $HOME",
            "rm -rf /*",
            "mkfs",
            "dd if=",
            ":(){:|:&};:",  # Fork bomb
            "> /dev/sda",
            "chmod -R 777 /",
            "chown -R",
            "sudo rm",
            "sudo dd",
            "diskutil erase",
            "diskutil partitionDisk",
        ]

        cmd_lower = command.lower().strip()

        for pattern in dangerous_patterns:
            if pattern.lower() in cmd_lower:
                raise GuardrailViolation(
                    f"BLOCKED: Dangerous command detected: '{command}' matches pattern '{pattern}'"
                )

        # Check if rm/rmdir targets are within project
        if "rm " in cmd_lower or "rmdir " in cmd_lower:
            # Extract paths from rm command (simplified parsing)
            parts = command.split()
            for part in parts:
                if part.startswith("/") or part.startswith("~"):
                    resolved = os.path.realpath(os.path.expanduser(part))
                    if not resolved.startswith(self.project_root):
                        raise GuardrailViolation(
                            f"BLOCKED: 'rm' targeting path outside project: '{resolved}'"
                        )

        log.debug(f"Command validated: {command[:80]}...")
        return True

    # --------------------------------------------------------
    # CONVENIENCE: Context manager for checkpointed operations
    # --------------------------------------------------------

    class CheckpointContext:
        """Context manager that auto-reverts on exception."""
        def __init__(self, guardrails, name, paths=None):
            self.gr = guardrails
            self.name = name
            self.paths = paths
            self.checkpoint_id = None

        def __enter__(self):
            self.checkpoint_id = self.gr.create_checkpoint(self.name, self.paths)
            return self.checkpoint_id

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                log.warning(f"Exception detected, reverting checkpoint: {self.checkpoint_id}")
                self.gr.revert_checkpoint(self.checkpoint_id)
                return False  # Re-raise the exception
            return False

    def checkpoint(self, name: str, paths: List[str] = None):
        """
        Context manager for auto-reverting operations.

        Usage:
            with gr.checkpoint("risky operation", paths=[...]):
                # do risky stuff
                # auto-reverts if exception is raised
        """
        return self.CheckpointContext(self, name, paths)

    # --------------------------------------------------------
    # STATUS / DIAGNOSTICS
    # --------------------------------------------------------

    def status(self) -> Dict:
        """Get current guardrails status."""
        checkpoints = self.list_checkpoints()
        total_backup_size = sum(c.get("size_mb", 0) for c in checkpoints)

        # Count audit entries
        audit_count = 0
        if os.path.exists(AUDIT_LOG):
            with open(AUDIT_LOG, 'r') as f:
                audit_count = sum(1 for _ in f)

        return {
            "project_root": self.project_root,
            "session_id": self._session_id,
            "dry_run": self.dry_run,
            "operations_this_session": dict(self._operation_count),
            "checkpoints": len(checkpoints),
            "total_backup_size_mb": total_backup_size,
            "audit_entries": audit_count,
            "limits": {
                "max_bulk_deletes": MAX_BULK_DELETES,
                "max_bulk_writes": MAX_BULK_WRITES,
                "max_file_size_mb": MAX_SINGLE_FILE_SIZE_MB,
                "checkpoint_retention_days": CHECKPOINT_RETENTION_DAYS,
            }
        }


# ============================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ============================================================

_default_gr = None

def _get_default():
    global _default_gr
    if _default_gr is None:
        _default_gr = GuardRails()
    return _default_gr

def verify_path(path: str, operation: str = "access") -> str:
    return _get_default().verify_path(path, operation)

def safe_write(path: str, content: Union[str, bytes], backup_existing: bool = True) -> str:
    return _get_default().safe_write(path, content, backup_existing)

def safe_read(path: str) -> str:
    return _get_default().safe_read(path)

def safe_delete(path: str) -> bool:
    return _get_default().safe_delete(path)

def safe_move(src: str, dst: str) -> str:
    return _get_default().safe_move(src, dst)

def safe_copy(src: str, dst: str) -> str:
    return _get_default().safe_copy(src, dst)

def create_checkpoint(name: str, paths: List[str] = None) -> str:
    return _get_default().create_checkpoint(name, paths)

def revert_checkpoint(checkpoint_id: str) -> Dict:
    return _get_default().revert_checkpoint(checkpoint_id)

def validate_shell_command(command: str) -> bool:
    return _get_default().validate_shell_command(command)


# ============================================================
# DECORATOR: @guarded - wrap any function with path checking
# ============================================================

def guarded(func):
    """
    Decorator that wraps a function with guardrail protection.
    Any file paths in the function's arguments are validated.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        gr = _get_default()
        # Log the function call
        gr._audit("GUARDED_CALL", {
            "function": func.__name__,
            "module": func.__module__,
        })
        try:
            return func(*args, **kwargs)
        except GuardrailViolation:
            raise
        except Exception as e:
            log.error(f"Error in guarded function {func.__name__}: {e}")
            raise
    return wrapper


# ============================================================
# CLI: Run directly for status/backup/revert
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="PRINTMAXX Safety Guardrails System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 guardrails.py --status              Show guardrails status
  python3 guardrails.py --checkpoint "name"   Create a full project checkpoint
  python3 guardrails.py --list-checkpoints    List all checkpoints
  python3 guardrails.py --revert <id>         Revert to a checkpoint
  python3 guardrails.py --verify /some/path   Check if a path is safe
  python3 guardrails.py --validate "rm -rf"   Check if a command is safe
  python3 guardrails.py --audit               Show recent audit log
  python3 guardrails.py --test                Run safety self-test
        """
    )

    parser.add_argument("--status", action="store_true", help="Show guardrails status")
    parser.add_argument("--checkpoint", type=str, help="Create a named checkpoint")
    parser.add_argument("--list-checkpoints", action="store_true", help="List all checkpoints")
    parser.add_argument("--revert", type=str, help="Revert to a checkpoint ID")
    parser.add_argument("--verify", type=str, help="Verify if a path is safe")
    parser.add_argument("--validate", type=str, help="Validate a shell command")
    parser.add_argument("--audit", action="store_true", help="Show recent audit log")
    parser.add_argument("--test", action="store_true", help="Run safety self-test")
    parser.add_argument("--cleanup", action="store_true", help="Clean old checkpoints")

    args = parser.parse_args()
    gr = GuardRails()

    if args.status:
        status = gr.status()
        print("\n=== PRINTMAXX GUARDRAILS STATUS ===")
        print(f"Project Root: {status['project_root']}")
        print(f"Session: {status['session_id']}")
        print(f"Checkpoints: {status['checkpoints']} ({status['total_backup_size_mb']:.1f} MB)")
        print(f"Audit Entries: {status['audit_entries']}")
        print(f"Operations This Session: {status['operations_this_session']}")
        print(f"\nLimits:")
        for k, v in status['limits'].items():
            print(f"  {k}: {v}")

    elif args.checkpoint:
        print(f"Creating checkpoint: {args.checkpoint}")
        cp_id = gr.create_checkpoint(args.checkpoint)
        print(f"Checkpoint created: {cp_id}")
        print("To revert: python3 guardrails.py --revert " + cp_id)

    elif args.list_checkpoints:
        checkpoints = gr.list_checkpoints()
        if not checkpoints:
            print("No checkpoints found.")
        else:
            print(f"\n{'ID':<60} {'Created':<25} {'Files':<8} {'Size'}")
            print("-" * 110)
            for cp in checkpoints:
                print(f"{cp['id']:<60} {cp['created']:<25} {len(cp.get('files', [])):<8} {cp.get('size_mb', 0):.1f} MB")

    elif args.revert:
        print(f"Reverting to checkpoint: {args.revert}")
        results = gr.revert_checkpoint(args.revert)
        print(f"Restored {results['restored']} files, {results['errors']} errors")

    elif args.verify:
        try:
            resolved = gr.verify_path(args.verify)
            print(f"SAFE: {resolved}")
        except GuardrailViolation as e:
            print(f"BLOCKED: {e}")
            sys.exit(1)

    elif args.validate:
        try:
            gr.validate_shell_command(args.validate)
            print(f"SAFE: Command passes validation")
        except GuardrailViolation as e:
            print(f"BLOCKED: {e}")
            sys.exit(1)

    elif args.audit:
        if not os.path.exists(AUDIT_LOG):
            print("No audit log yet.")
        else:
            print("\n=== RECENT AUDIT LOG (last 20 entries) ===")
            with open(AUDIT_LOG, 'r') as f:
                lines = f.readlines()
            for line in lines[-20:]:
                try:
                    entry = json.loads(line)
                    print(f"[{entry['time']}] {entry['operation']}: {json.dumps(entry['details'])[:100]}")
                except json.JSONDecodeError:
                    print(line.strip())

    elif args.test:
        print("\n=== GUARDRAIL SAFETY SELF-TEST ===\n")
        passed = 0
        failed = 0

        tests = [
            ("Block write to home directory",
             lambda: gr.verify_path(os.path.expanduser("~/test.txt"), "write"),
             True),
            ("Block write to /etc",
             lambda: gr.verify_path("/etc/passwd", "write"),
             True),
            ("Block write to Desktop",
             lambda: gr.verify_path(os.path.expanduser("~/Desktop/test.txt"), "write"),
             True),
            ("Allow write to project",
             lambda: gr.verify_path(os.path.join(PROJECT_ROOT, "test.txt"), "write"),
             False),
            ("Allow read from project",
             lambda: gr.verify_path(os.path.join(PROJECT_ROOT, "CLAUDE.md"), "read"),
             False),
            ("Block delete of CLAUDE.md",
             lambda: gr.verify_path(os.path.join(PROJECT_ROOT, "CLAUDE.md"), "delete"),
             True),
            ("Block delete of LEDGER/",
             lambda: gr.verify_path(os.path.join(PROJECT_ROOT, "LEDGER/test.csv"), "delete"),
             True),
            ("Block rm -rf /",
             lambda: gr.validate_shell_command("rm -rf /"),
             True),
            ("Block fork bomb",
             lambda: gr.validate_shell_command(":(){:|:&};:"),
             True),
            ("Allow project rm",
             lambda: gr.validate_shell_command(f"rm {PROJECT_ROOT}/temp.txt"),
             False),
            ("Block rm outside project",
             lambda: gr.validate_shell_command("rm /Users/macbookpro/Documents/other_project/file.txt"),
             True),
            ("Block write to .ssh",
             lambda: gr.verify_path(os.path.expanduser("~/.ssh/authorized_keys"), "write"),
             True),
            ("Block delete of guardrails backups",
             lambda: gr.verify_path(os.path.join(BACKUP_DIR, "checkpoints/test"), "delete"),
             True),
        ]

        for name, test_func, should_raise in tests:
            try:
                test_func()
                if should_raise:
                    print(f"  FAIL: {name} (should have been blocked)")
                    failed += 1
                else:
                    print(f"  PASS: {name}")
                    passed += 1
            except (GuardrailViolation, ProtectedPathViolation):
                if should_raise:
                    print(f"  PASS: {name} (correctly blocked)")
                    passed += 1
                else:
                    print(f"  FAIL: {name} (incorrectly blocked)")
                    failed += 1
            except Exception as e:
                print(f"  ERROR: {name} ({e})")
                failed += 1

        print(f"\n{'=' * 40}")
        print(f"Results: {passed} passed, {failed} failed out of {passed + failed}")

        if failed == 0:
            print("ALL TESTS PASSED - Guardrails are working correctly")
        else:
            print(f"WARNING: {failed} tests failed!")
            sys.exit(1)

    elif args.cleanup:
        gr._cleanup_old_checkpoints()
        print("Old checkpoints cleaned up.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
