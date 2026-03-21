#!/usr/bin/env python3
"""Generate executable template scripts from all DAG configs.

Reads AUTOMATIONS/auto_ops/dag_plans/*.json and creates a working Python
script for each one. No claude -p needed — pure template generation.

Usage:
    python3 AUTOMATIONS/generate_scripts_from_dags.py --run
    python3 AUTOMATIONS/generate_scripts_from_dags.py --dry-run
    python3 AUTOMATIONS/generate_scripts_from_dags.py --status
"""
from __future__ import annotations
import argparse
import json
import os
import py_compile
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
DAG_DIR = AUTOMATIONS / "auto_ops" / "dag_plans"
LOG_FILE = AUTOMATIONS / "logs" / "generate_scripts.log"

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
{description}

Auto-generated from DAG: {dag_name}
Venture: {venture} | Phases: {phase_count}
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PROJECT, safe_path, capture_skill_from_result

AUTOMATIONS = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS / "logs" / "{log_name}.log"

STEPS = {steps_json}


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{{ts}}] [{tag}] [{{level}}] {{msg}}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\\n")


def run(dry_run: bool = False) -> None:
    log(f"Starting ({{len(STEPS)}} steps)")
    for i, step in enumerate(STEPS, 1):
        log(f"Step {{i}}/{{len(STEPS)}}: {{step}}")
        if dry_run:
            continue
        try:
            r = subprocess.run(
                ["claude", "-p", "--model", "sonnet",
                 f"Execute this step for PRINTMAXX. Be concise. Step: {{step}}"],
                capture_output=True, text=True, timeout=120, cwd=str(PROJECT),
            )
            log(f"  {{'OK' if r.returncode == 0 else 'FAIL'}}: {{r.stdout[:80]}}")
        except subprocess.TimeoutExpired:
            log(f"  TIMEOUT on step {{i}}", "WARN")
        except Exception as e:
            log(f"  ERROR: {{e}}", "ERROR")
    capture_skill_from_result(task="{description_short}", result=f"Ran {{len(STEPS)}} steps", success=True)
    log("Complete")


def status() -> None:
    print(f"Script: {script_name}")
    print(f"Venture: {venture}")
    print(f"Steps: {{len(STEPS)}}")
    if LOG_FILE.exists():
        lines = LOG_FILE.read_text().strip().splitlines()
        print(f"Log: {{len(lines)}} entries")
        if lines:
            print(f"Last: {{lines[-1][:80]}}")


def main() -> None:
    parser = argparse.ArgumentParser(description="{description_short}")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.status:
        status()
    elif args.run or args.dry_run:
        run(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
'''


def generate_all(dry_run: bool = False) -> dict:
    created = compiled = skipped = errors = 0

    for dag_file in sorted(DAG_DIR.glob("dag_*.json")):
        try:
            config = json.loads(dag_file.read_text())
            name = config.get("name", dag_file.stem)
            venture = config.get("venture", "UNKNOWN")
            method = config.get("method", "")[:200]
            phases = config.get("phases", [])

            # Build script name
            slug = name[:35].lower().replace(" ", "_").replace("-", "_")
            slug = "".join(c for c in slug if c.isalnum() or c == "_").strip("_")
            if not slug:
                skipped += 1
                continue

            script_name = f"int_{slug}.py"
            script_path = AUTOMATIONS / script_name

            if script_path.exists():
                skipped += 1
                continue

            # Collect steps from all phases
            steps = []
            for phase in phases:
                for step in phase.get("steps", []):
                    if isinstance(step, str) and step.strip():
                        steps.append(step.strip())

            if not steps:
                skipped += 1
                continue

            if dry_run:
                print(f"  Would create: {script_name} ({len(steps)} steps, {venture})")
                created += 1
                continue

            # Generate script from template
            tag = slug[:20].upper()
            code = SCRIPT_TEMPLATE.format(
                description=method.replace('"', "'"),
                dag_name=dag_file.name,
                venture=venture,
                phase_count=len(phases),
                log_name=slug[:30],
                steps_json=json.dumps(steps[:12], indent=4),
                tag=tag,
                script_name=script_name,
                description_short=method[:80].replace('"', "'"),
            )

            script_path.write_text(code)
            os.chmod(str(script_path), 0o755)

            # Verify compilation
            try:
                py_compile.compile(str(script_path), doraise=True)
                compiled += 1
            except py_compile.PyCompileError:
                errors += 1
                script_path.unlink()
                continue

            created += 1

        except Exception as e:
            errors += 1

    return {"created": created, "compiled": compiled, "skipped": skipped, "errors": errors}


def show_status():
    existing = len(list(AUTOMATIONS.glob("int_*.py")))
    dags = len(list(DAG_DIR.glob("dag_*.json")))
    print(f"DAG configs: {dags}")
    print(f"Scripts generated: {existing}")
    print(f"Missing: {dags - existing}")


def main():
    parser = argparse.ArgumentParser(description="Generate scripts from DAG configs")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.run or args.dry_run:
        result = generate_all(dry_run=args.dry_run)
        print(f"\nCreated: {result['created']}")
        print(f"Compiled: {result['compiled']}")
        print(f"Skipped: {result['skipped']}")
        print(f"Errors: {result['errors']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
