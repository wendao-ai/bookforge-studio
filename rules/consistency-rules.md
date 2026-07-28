---
description: "Consistency rule schema"
globs:
  - "genre-packs/*/consistency-rules.yaml"
---

# Consistency Rules Schema

## Mandatory Standards

- Root key must be `rules`.
- Each rule must have stable id, `level`, `description`, `check`, and `action`.
- `level` must be one of `critical`, `high`, `medium`, or `low`.
- At least one rule per Pack must be `critical`.
- Critical rule actions must block or require backtrack.
- Rules should map to the active genre's core creative risk.

## Recommended Fields (optional, non-blocking)

The following optional fields do **not** affect the Mandatory Standards above — existing rules without them remain compliant. They improve how consistency findings are communicated to authors and how a future `/project-doctor` renders them.

- `impact`: one line on what happens if this rule is violated ("what breaks if unfixed"). Helps authors understand why the rule exists.
- `repair`: one line of executable remediation — either the fix direction or the skill to trigger (e.g., `/fix-cascade`).
- `override_rationale` (medium / low rules only): when an author has a higher-priority reason to violate this rule, the reason is recorded here. Suggested values: `logic_integrity` (logic/fairness first), `character_credibility` (character believability first), `world_rule_constraint` (setting constraint), `transitional_setup` (setup/transition), `arc_timing` (long-arc pacing), `genre_convention` (genre convention), `editorial_intent` (author intent — strictest quota). **critical rules are never overridable** and must still block or backtrack.
- `enforce_in_prose` (string, optional): one line describing how this rule must be **fulfilled in the prose itself**, not merely registered in memory/registry. Absent or empty = registry-only constraint (state tracked, no on-page check); non-empty = `/review-chapter` must verify the prose actually delivers it. Use for constraints whose value lies in reader-facing payoff — e.g., a golden-finger cost that must visibly cost the protagonist on-page (not just `memory-schema.golden-finger.cost` filled), a promise that must pay off in-scene (not just `registry/promises.yaml` status), a thesis that must be argued in-chapter (not just asserted in `brief.yaml`). **This field closes the A/B-observed gap** (rebirth-capital, 2026-07-11): registry-tracking a constraint ≠ delivering it to the reader; `enforce_in_prose` makes the review skill check delivery, not just registration.

A medium/low violation carried forward under an `override_rationale` must still be recorded in the review report (never silently passed).

## Anti-Patterns

- Vague checks such as "make it good".
- All rules set to medium to avoid blocking.
- Rules that cannot name the artifact or memory they inspect.
- Actions that warn about critical errors but allow silent continuation.
- Allowing a rule to be overridden without requiring the override reason to be recorded.
