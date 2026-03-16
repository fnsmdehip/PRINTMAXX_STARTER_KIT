# EAS Subcontractor Protection Strategy — March 2026

## Legal Stack (in order of enforceability)

1. **Non-Solicitation** (MOST enforceable) — 12-24 months, prohibits soliciting EAS clients. Liquidated damages: $50K-100K per violation.
2. **NDA** — Perpetual for trade secrets, 3-5 years for general confidential info. Covers: playbooks, pricing, client lists, prompt libraries.
3. **IP Assignment** — Belt-and-suspenders: work-for-hire designation AND separate assignment clause.
4. **Non-Circumvention** — Prevents bypassing EAS to deal directly with introduced parties.
5. **Non-Compete** (ONLY in enforceable states) — 6-12 months, narrow scope. NEVER in California, Minnesota, North Dakota, Oklahoma, Montana.

## Hire In These Jurisdictions (Easiest Enforcement)

| Jurisdiction | Why |
|---|---|
| **Florida** | Courts required to "blue pencil" overbroad clauses. Strongest enforcement state. |
| **Texas** | Marsh USA (2011) expanded enforceability. Strong trade secret protection. |
| **Georgia** | 2011 constitutional amendment. Courts can modify restrictions. |
| **Ohio, Pennsylvania** | Generally enforceable with reasonable restrictions. |

**AVOID:** California (banned), Minnesota (banned), India (constitutional right to livelihood), Ontario Canada (banned), EU (requires 50-100% compensation during restriction period).

## Compartmentalization (Most Powerful Non-Legal Protection)

1. **Modular delivery** — Sub A does data pipeline, Sub B does AI config, Sub C does dashboard. Nobody sees the full system.
2. **Abstraction** — Subs use our platform through interfaces, never see underlying code/prompts.
3. **Client isolation** — ALL client comms through EAS project manager. Sub never gets direct client contact info.
4. **Rotation** — Don't assign same sub to same client long-term.
5. **Knowledge segmentation** — "Client-facing" playbooks (shareable) vs "internal-only" strategy (never leaves EAS).

## Technical Moat (Stronger Than Legal)

1. **API keys on EAS accounts** — Sub accesses through our proxy. Revoked instantly on termination.
2. **Workflows on our infrastructure** — Sub logs into OUR n8n/platform. Loses access when terminated.
3. **Code in EAS repos** — Branch access only, never admin. Audit every clone/download.
4. **Watermarking** — Unique identifiers in docs/templates per sub. Leak traceable to source.

## Financial Retention

1. **Quarterly loyalty bonus** ($2,500-5,000) with 100% clawback if sub leaves within 6 months or violates terms
2. **Deferred compensation** — Hold 10-20% in pool, vests at 12 months
3. **Tiered rate increases** — Auto-increase at 6/12/18 months. Leaving means starting over.

## Enforcement Cost Reality

- Cease & desist letter: $1,500-5,000 (stops ~40% of violations)
- TRO / preliminary injunction: $10,000-30,000 (the critical step)
- Full litigation: $50,000-180,000+
- Most cases settle after TRO is granted

## Real Case Precedents

- **McKinsey v. Former Partner**: IP theft to Accenture. Clear IP ownership agreements were key.
- **Alpine v. Jacokes (2025)**: Ex-employee stole clients + data. Forum selection clause gave favorable jurisdiction. Motion to dismiss DENIED.
- **CSC v. Tata**: Source code theft. **$210M jury verdict.** Willful conduct = punitive damages.

## Referral Program

| Referral Type | Commission |
|---|---|
| Warm intro | 10% of first project |
| Qualified opportunity | 15% of first project |
| Retainer client | 5-10% recurring for 12 months |
| Two-sided: referred client gets | 10% off first project |

## First 10 Case Studies Plan

1. **Cases 1-3**: 50-70% discount + testimonial agreement built into contract
2. **Cases 4-7**: 20-30% discount + testimonial
3. **Cases 8-10**: Full price + testimonial (standard contract clause)

**FTC rule:** If discount is tied to testimonial, must disclose. Better approach: offer discount as "introductory rate," ask for testimonial separately after delivery.

## Testimonial Process

1. Ask immediately after measurable result (not after project ends)
2. Provide 3 specific questions, not "write a testimonial"
3. Offer to draft it for them
4. Immediately follow with referral ask
5. Build testimonial release into standard onboarding contract (opt-out, not opt-in)
