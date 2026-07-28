---
name: curate-evidence
description: curate evidence. Use this skill when nonfiction-general-stage work needs this operation. Applies only within the nonfiction-general Genre Pack.
category: nonfiction-general
---

# /curate-evidence

## Purpose

Curate evidence for `nonfiction-general` projects.

## Inputs

- Active project id and `PROJECT.md`.
- `genre-context/active-pack.yaml`.
- `nonfiction-general` Pack files under `genre-packs/nonfiction-general/`.
- Current stage artifact and relevant genre memory.

## Outputs

- Updated project artifact or genre memory entry.
- A short decision summary for `.history/events.jsonl`.
- Any human-review requirement or consistency concern.

## Steps

1. Confirm the active project uses `nonfiction-general` as primary or secondary genre.
2. Load the relevant Pack schema, quality metrics, and consistency rules.
3. Inspect the current artifact and upstream project memory.
4. Produce the requested genre-specific artifact or review.
5. Record confidence, assumptions, and unresolved questions.
6. Run or request the applicable consistency check.

## Quality Gates

- Output follows `nonfiction-general` memory and template conventions.
- Critical genre rules are not bypassed.
- Human approval is requested for Pack-specific creative cruxes.
- The next stage can continue from durable files, not chat-only context.

## Error Handling

- If the active genre is different, stop and route to `/switch-genre`.
- If upstream memory is missing, create a gap report instead of inventing state.
- If the requested action conflicts with approved decisions, ask for confirmation.
- If confidence is speculative, label it and request review.
