# Auto-Quality Pipeline

Runs by default, no human trigger needed.

## BEFORE building
- `superpowers:brainstorming` — MANDATORY before creative work
- `superpowers:writing-plans` — For multi-step tasks
- `feature-dev:feature-dev` — For new features

## WHILE writing code
- `superpowers:systematic-debugging` — For ANY bug/failure. Diagnose before fixing.
- `superpowers:dispatching-parallel-agents` — 2+ independent tasks = parallel agents

## AFTER writing code (50+ lines)
- `/simplify` — 3 parallel review agents
- `pr-review-toolkit:silent-failure-hunter` — After error handling code
- Verify new scripts compile: `python3 -c "import py_compile; py_compile.compile('FILE')"`

## BEFORE claiming done
- `superpowers:verification-before-completion` — MANDATORY

## External dependencies
- Rule 13 security scan (6-point audit) on any pip/npm install, git clone

## Commits
- `coderabbit:code-review` on staged changes
- Secret detection, credential check
- `pr-review-toolkit:comment-analyzer` for docstring changes

## PRs
- `pr-review-toolkit:review-pr` + `pr-review-toolkit:pr-test-analyzer`

## Session end
- `/simplify` on code changes
- `superpowers:verification-before-completion` final check

## Periodic
- `claude-code-setup:claude-automation-recommender` — recommend new automations
- `hookify:hookify` — create hooks for repeated mistakes
- `claude-md-management:claude-md-improver` — audit CLAUDE.md

## Token conservation
If approaching limits: skip /simplify, skip brainstorming, defer reviews.
