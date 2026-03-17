"""dogwalk core — meta-cognition framework for AI agents.

stop dog walking your AI through every decision.
6.9 corrections per task → 1.

Modules:
    voice_extractor    - analyze prompt history, distill communication style
    cognitive_engine   - build cognition model from correction chains + task history
    pattern_miner      - extract meta-rules from user prompt patterns
    user_sim_refiner   - simulate user critique for autonomous improvement
    loop_closer        - close open loops: decide, act, log, learn
    self_audit         - competitive cognition audit (meta-improvement)
    decision_engine    - closed-loop autonomous decision agent
    resilience         - retry, file locking, circuit breaker, sanitization
    conversation_logger - extract and search conversation transcripts
    session_briefing   - generate session start briefings from system state
"""

__version__ = "0.1.0"
