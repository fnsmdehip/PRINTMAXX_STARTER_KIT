# sovrun -- System Wiring Template

This is a template showing how to wire sovrun into your project's CLAUDE.md (or equivalent system instructions file).

## Session Start
1. Read `output/session_briefing.md` (auto-generated)
2. Run `python3 -m sovrun.core.decision_engine --cycle`
3. Check actionable queue

## Reference Files
| Need | File |
|------|------|
| Agent identity | `templates/SOUL.md` |
| Voice model | `output/voice_model.json` |
| Meta-rules | `output/prompt_intelligence/meta_rules.md` |
| Correction chains | `output/prompt_intelligence/correction_chains.json` |
| Session briefing | `output/session_briefing.md` |
| Decision audit | `output/decisions.csv` |
| Loop state | `state/loop_state.json` |

## Core Rules
1. **SHIP** -- Deploy what exists before building new.
2. **NO ORPHANS** -- Every doc has a consumer. No dead-end reports.
3. **NO SLOP** -- No AI vocabulary. No hedging. Direct output.
4. **AUTONOMOUS** -- Don't ask permission. Execute. Fix mistakes.
5. **ABOVE AND BEYOND** -- Follow the logical end. Build implicit subtasks.
6. **INTELLIGENCE-FIRST** -- Query your data before defaulting to LLM priors.

## Voice Injection
Before generating user-facing output, run:
```
python3 -m sovrun.core.voice_extractor --inject
```
Inject the resulting string into your agent prompt prefix.

## Loop Closing
Every 2 hours or at session end:
```
python3 -m sovrun.core.loop_closer --cycle
```

## Weekly Self-Audit
```
python3 -m sovrun.core.self_audit --audit
```

## Weekly Cognition Model Rebuild
```
python3 -m sovrun.core.cognitive_engine --build-model
python3 -m sovrun.core.pattern_miner --mine
python3 -m sovrun.core.voice_extractor --extract
```

## Environment Variables
All paths are configurable via environment variables:
- `SOVRUN_ROOT` -- project root directory (default: cwd)
- `SOVRUN_PROMPTS` -- path to prompts JSONL file
- `SOVRUN_CONVERSATIONS` -- path to conversation history JSONL
- `SOVRUN_VOICE_MODEL` -- path to voice model output
- `SOVRUN_SOUL_MD` -- path to SOUL.md
- `SOVRUN_INSTRUCTIONS` -- path to system instructions
- `SOVRUN_TRANSCRIPT_DIRS` -- comma-separated transcript directories

## Cron Schedule (example)
```
# Daily: rebuild voice model and cognition
0 4 * * * cd /path/to/project && python3 -m sovrun.core.voice_extractor --extract
0 4 * * 0 cd /path/to/project && python3 -m sovrun.core.cognitive_engine --build-model

# Every 2 hours: close loops
0 */2 * * * cd /path/to/project && python3 -m sovrun.core.loop_closer --cycle

# Weekly: self audit
0 5 * * 0 cd /path/to/project && python3 -m sovrun.core.self_audit --audit

# Session start: briefing
# (run manually or via session start hook)
```
