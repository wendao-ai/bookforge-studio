---
description: "Review report standards"
globs:
  - "projects/*/review/**"
---

# Review Report Rules

## Mandatory Standards

- Reader reports must name reader profile, chapter/artifact reviewed, quality dimensions, findings, severity, and suggested fixes.
- `controversy_map.yaml` must summarize disagreements between simulated readers.
- Review output must distinguish taste feedback from consistency or factual problems.
- Fix cascade plans must assign each issue to revise, defer, or reject.
- High and critical issues must be reviewed before typeset.
- Every review skill run (`multi-dim-feedback` / `consensus-analysis` / `fix-cascade` / `/spawn-reader-panel`) must end with a four-state overall status and classify any exceptions into the three handling categories (see Skill Output Status below).

## Skill Output Status

Review skills end every run with a **four-state overall status** and classify exceptions into **three handling categories**. This lets the author see at a glance whether the step succeeded and whether their input is needed, and lets downstream skills route by status. The operations skills `/project-doctor` and `/query-project-state` adopt the same taxonomy.

### Four-state overall status

| Status | Meaning | Trigger |
|---|---|---|
| `completed` | Done; exit gate satisfied; safe to proceed | No unresolved critical/high; artifacts complete |
| `partial` | Mostly done, but open items remain (deferred medium/low, optional fixes, pending `override_rationale`) | medium/low carried forward, or high has a fix plan not yet executed |
| `needs_user` | A creative crux or critical block awaits the author | critical unresolved, key decision unconfirmed, genre/pack mismatch |
| `failed` | A critical upstream gap prevents reliable completion | upstream artifact missing, engine missing, stage undecidable |

### Three exception categories

Each exception is classified by handling path (maps to `shared-tooling/editorial-collaboration/error-catalog.json` `severity_mapping`):

| Category | Meaning | Maps to severity |
|---|---|---|
| `auto_handled` | Handled and recorded (warn); does not interrupt | medium / low |
| `needs_confirmation` | Needs author confirmation (fix plan, `override_rationale`, direction choice) | high (+ medium/low carrying an `override_rationale`) |
| `must_handle` | Must be fixed; blocks the next step | critical |

### Wiring into report artifacts

- The overall status + exception categories appear at the top of every report under `review/` (reader reports, `controversy_map.yaml`, fix cascade plan).
- Author-facing wording is downgraded through `shared-tooling/editorial-collaboration/author-glossary.json` (e.g. completed→"完成", needs_user→"需要你定夺", must_handle→"必须先修").
- A `must_handle` exception must never be silently downgraded to `auto_handled`; a `needs_user` status must never decide for the author.

## Anti-Patterns

- Treating all reader comments as equally valid.
- Mixing author preference, genre law, and grammar polish without labels.
- Skipping controversy synthesis when readers disagree.
- Marking review complete while unresolved critical issues remain.
- Marking a `must_handle` (critical) exception as `auto_handled`, or silently downgrading `needs_user` to `completed`.
