#!/usr/bin/env python3
"""
Seed Skills -- Pre-populate procedural memory with starter skill documents.
===========================================================================

Seeds the skills database with 5 foundational skill categories that agents
can recall immediately without learning from scratch:

  1. proposal_writing         -- freelance proposal template
  2. cold_email_personalization -- personalization patterns that get replies
  3. content_hook_patterns    -- hooks that drive engagement
  4. app_listing_copy         -- ASO description patterns
  5. client_objection_handling -- responses to common objections

Usage:
  python3 AUTOMATIONS/seed_skills.py          # Seed all skills
  python3 AUTOMATIONS/seed_skills.py --check  # Check what's already seeded
  python3 AUTOMATIONS/seed_skills.py --force  # Re-seed even if exists
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure sibling modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Sovrun modules
_SOVRUN_PATH = str(Path(__file__).resolve().parent.parent / "OPEN_SOURCE" / "agent-soul")
if _SOVRUN_PATH not in sys.path:
    sys.path.insert(0, _SOVRUN_PATH)

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
SKILLS_DB_PATH = PROJECT / "AUTOMATIONS" / "agent" / "sovrun" / "skills.db"

try:
    from core.procedural_memory import ProceduralMemory
    _AVAILABLE = True
except ImportError:
    ProceduralMemory = None  # type: ignore[assignment, misc]
    _AVAILABLE = False


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [SEED] [{level}] {msg}")


# === Skill Definitions ===

SEED_SKILLS = [
    {
        "task": "Write a winning freelance proposal for a client project",
        "title": "Freelance Proposal Writing",
        "problem": (
            "Writing proposals that win freelance contracts on Upwork, Fiverr, "
            "and cold outreach. Most proposals get ignored because they talk about "
            "the freelancer instead of the client's problem."
        ),
        "steps": [
            "1. Open with the client's specific pain point, not your credentials. "
            "Reference something specific from their job post or website.",
            "2. Show you understand the problem better than they do. Restate it "
            "in sharper terms. 'You need X because Y is costing you Z.'",
            "3. Propose a concrete solution in 2-3 sentences. Name the deliverables "
            "and timeline. 'I will build X by [date]. You will get [specific outcome].'",
            "4. Include one micro-proof: a link to similar work, a metric from a past "
            "project, or a 30-second screen recording showing relevant skills.",
            "5. End with a specific next step, not 'let me know.' Try: 'I can start "
            "Monday. Want me to send a quick scope doc by tomorrow?'",
            "6. Keep total length under 150 words. Respect their time. If the proposal "
            "needs scrolling, it is too long.",
        ],
        "tags": ["freelance", "proposal", "outreach", "upwork", "client_acquisition"],
        "confidence": 0.85,
    },
    {
        "task": "Personalize a cold email to get a reply from a business owner",
        "title": "Cold Email Personalization",
        "problem": (
            "Cold emails that get replies vs ones that get deleted. Generic templates "
            "get 1-2% reply rates. Personalized emails using the 6-question framework "
            "and specific triggers get 15-30%."
        ),
        "steps": [
            "1. Find a trigger event: recent hire, product launch, funding, bad review, "
            "website change, social post. Use this as your opening line.",
            "2. Apply the 6-question framework in under 100 words: What you do, Who for, "
            "How, Problem solved, Proof, ROI.",
            "3. Personalization layer: mention their company name, a specific page on "
            "their site, a recent post, or a competitor they are losing to.",
            "4. One clear CTA: 'Worth a 10-min call this week?' not 'Let me know if "
            "you are interested in learning more about our solutions.'",
            "5. Subject line: reference their company or trigger event. "
            "'[CompanyName] + [specific observation]' format. Never 'Quick question.'",
            "6. Follow up 3x: Day 3 (value-add), Day 7 (case study), Day 14 (breakup). "
            "Each follow-up adds new information, never just 'bumping this up.'",
            "7. Send between 8-10 AM in their timezone, Tuesday through Thursday.",
        ],
        "tags": ["cold_email", "outreach", "personalization", "lead_gen", "b2b", "sales"],
        "confidence": 0.90,
    },
    {
        "task": "Write a content hook that drives engagement on social media",
        "title": "Content Hook Patterns",
        "problem": (
            "Creating hooks that stop the scroll and drive engagement. Most content "
            "fails because the first line is boring. Hooks are 80% of the engagement "
            "equation across Twitter, TikTok, YouTube, and email."
        ),
        "steps": [
            "1. Consequence-first hook: lead with what happened, not the explanation. "
            "'I lost $10K in 30 days. Here is exactly what went wrong.' not "
            "'Here are some mistakes to avoid.'",
            "2. Specific number hook: exact numbers beat vague claims. "
            "'I cold emailed 2,847 people. 412 replied.' not 'I sent a lot of emails.'",
            "3. Contrarian hook: challenge conventional wisdom. "
            "'SEO is dead for solopreneurs. Here is what actually works.' "
            "Must have substance to back it up.",
            "4. Pattern interrupt: start with something unexpected. "
            "'My competitor called me to say thanks.' Then explain why.",
            "5. Before/after hook: show transformation with proof. "
            "'6 months ago I had 200 followers. Today I closed $50K from Twitter alone. "
            "Here is the exact system.'",
            "6. Gatekeeping hook: position as insider knowledge. "
            "'Most people do not know this exists. It is borderline illegal how much "
            "intel this gives you.'",
            "7. Self-reply thread structure: hook tweet + 5-7 value tweets + final CTA. "
            "Each tweet in the thread must stand alone as valuable.",
        ],
        "tags": ["content", "hooks", "engagement", "twitter", "social_media", "copywriting"],
        "confidence": 0.88,
    },
    {
        "task": "Write an app store listing that drives downloads (ASO)",
        "title": "App Listing Copy (ASO)",
        "problem": (
            "App Store Optimization for indie apps. Most listings fail because they "
            "describe features instead of outcomes. The description must sell within "
            "the first 3 lines (above the fold) and use keywords naturally."
        ),
        "steps": [
            "1. Title: [App Name] - [Primary Benefit]. Under 30 chars. Include the #1 "
            "keyword. 'FocusFlow - Deep Work Timer' not 'FocusFlow App.'",
            "2. Subtitle (iOS) / Short Description (Android): One sentence, primary "
            "benefit + secondary keyword. 'Block distractions. Get 3x more done.'",
            "3. First 3 lines (above fold): Answer 'why should I download this right now?' "
            "Lead with the pain point, then the solution, then social proof.",
            "4. Feature bullets: 5-7 bullets. Each starts with a benefit, not a feature. "
            "'Save 2 hours daily with smart task batching' not 'Has task batching feature.'",
            "5. Keywords field (iOS): fill all 100 chars. No spaces after commas. "
            "No duplicates from title. Use competitor names if allowed. Research with "
            "AppTweak, Sensor Tower, or AppFollow.",
            "6. Screenshots: first 2 screenshots are 70% of the decision. Show the "
            "primary action + outcome with large text overlay. Not UI tours.",
            "7. Localization: translate title + subtitle + keywords for top 5 markets "
            "(EN, ES, PT, DE, JA). Even basic translation 2-3x visibility.",
        ],
        "tags": ["aso", "app_store", "listing", "copy", "mobile", "seo", "downloads"],
        "confidence": 0.82,
    },
    {
        "task": "Handle common client objections in a sales conversation",
        "title": "Client Objection Handling",
        "problem": (
            "Converting leads who push back on price, timing, or trust. Most "
            "freelancers and agencies lose deals not because of capability but "
            "because they fold on objections or get defensive."
        ),
        "steps": [
            "1. 'Too expensive': Reframe from cost to ROI. 'What is the cost of NOT "
            "solving this? You told me [pain point] is costing you $X/month. This "
            "pays for itself in [timeframe].' Never discount immediately.",
            "2. 'Need to think about it': Diagnose the real objection. 'Totally get it. "
            "Usually when someone says that, it is about [price/timing/trust]. "
            "Which one is it for you?' Then address the real concern.",
            "3. 'We have someone already': 'Great, that means you already see the value. "
            "Most of my best clients came from switching. What would make you consider "
            "an alternative?' Find the gap in current service.",
            "4. 'Can you do it cheaper?': 'I can adjust the scope. What matters most: "
            "[deliverable A] or [deliverable B]? I will build a package around your "
            "priority.' Reduce scope, not price.",
            "5. 'Not the right time': 'When would be the right time? Let me send you "
            "something useful in the meantime.' Drop a case study or free audit. "
            "Follow up on their stated timeline.",
            "6. 'Send me a proposal': This is not buying intent. 'Before I put together "
            "something detailed, can we do a 15-min call so I scope it right? "
            "I do not want to waste your time with a generic doc.'",
            "7. Universal technique: Agree, Isolate, Resolve. 'I hear you (agree). "
            "If we solved [objection], would you move forward (isolate)? "
            "Here is how we handle that (resolve).'",
        ],
        "tags": ["sales", "objections", "closing", "client", "freelance", "negotiation"],
        "confidence": 0.87,
    },
]


def seed_all(force: bool = False) -> int:
    """Seed all skills into procedural memory. Returns count seeded."""
    if not _AVAILABLE:
        log("ProceduralMemory not available. Install sovrun from OPEN_SOURCE/agent-soul/", "ERROR")
        return 0

    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    SKILLS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    mem = ProceduralMemory(db_path=SKILLS_DB_PATH)

    seeded = 0
    skipped = 0

    for skill_def in SEED_SKILLS:
        title = skill_def["title"]

        # Check if already exists (unless force)
        if not force:
            existing = mem.recall(title, top_k=1)
            if existing and existing[0].get("title") == title:
                log(f"  SKIP: {title} (already exists)")
                skipped += 1
                continue

        # Build the result text from steps
        steps_text = "\n".join(skill_def["steps"])
        result_text = f"Problem: {skill_def['problem']}\n\nSolution:\n{steps_text}"

        doc = mem.capture(
            task=skill_def["task"],
            result=result_text,
            success=True,
            source_session="seed_skills",
            confidence=skill_def["confidence"],
        )

        if doc:
            log(f"  SEEDED: {title} (id={doc.skill_id})")
            seeded += 1
        else:
            log(f"  FAIL: {title}", "WARN")

    mem.close()
    log(f"Seeding complete: {seeded} seeded, {skipped} skipped")
    return seeded


def check_existing() -> None:
    """Check what skills are already in the database."""
    if not _AVAILABLE:
        log("ProceduralMemory not available.", "ERROR")
        return

    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    if not SKILLS_DB_PATH.exists():
        print("No skills database found. Run seed_skills.py first.")
        return

    mem = ProceduralMemory(db_path=SKILLS_DB_PATH)

    print("\n=== Procedural Memory Status ===\n")

    for skill_def in SEED_SKILLS:
        title = skill_def["title"]
        results = mem.recall(title, top_k=1)
        if results and results[0].get("title") == title:
            r = results[0]
            print(f"  [SEEDED] {title}")
            print(f"           id={r['skill_id']} conf={r['confidence']:.2f} "
                  f"used={r['success_count']}x last={r['last_used'][:10]}")
        else:
            print(f"  [MISSING] {title}")

    # Overall stats
    try:
        stats = mem.stats()
        print(f"\nTotal skills in DB: {stats.get('total_skills', '?')}")
    except Exception:
        pass

    mem.close()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed procedural memory with starter skill documents"
    )
    parser.add_argument("--check", action="store_true",
                        help="Check what is already seeded")
    parser.add_argument("--force", action="store_true",
                        help="Re-seed even if skills already exist")
    args = parser.parse_args()

    if args.check:
        check_existing()
    else:
        count = seed_all(force=args.force)
        if count > 0:
            print(f"\nSeeded {count} skill(s). Query with:")
            print(f"  python3 AUTOMATIONS/agent_swarm.py --skills 'proposal writing'")
            print(f"  python3 AUTOMATIONS/agent_swarm.py --skills 'cold email'")
            print(f"  python3 AUTOMATIONS/agent_swarm.py --skills 'content hooks'")


if __name__ == "__main__":
    main()
