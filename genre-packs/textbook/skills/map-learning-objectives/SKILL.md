---
name: map-learning-objectives
description: map chapters to learning objectives. Use this skill when textbook-stage work needs this operation. Applies only within the textbook Genre Pack.
category: textbook
---

# /map-learning-objectives

## Purpose

Map chapters to learning objectives for `textbook` projects.

## Inputs

- Active project id and `PROJECT.md`.
- `genre-context/active-pack.yaml`.
- `textbook` Pack files under `genre-packs/textbook/`.
- Current stage artifact and relevant genre memory.

## Outputs

- Updated project artifact or genre memory entry.
- A short decision summary for `.history/events.jsonl`.
- Any human-review requirement or consistency concern.

## Steps

1. Confirm the active project uses `textbook` as primary or secondary genre.
2. Load the relevant Pack schema, quality metrics, and consistency rules.
3. Inspect the current artifact and upstream project memory.
4. Produce the requested genre-specific artifact or review.
5. Record confidence, assumptions, and unresolved questions.
6. Run or request the applicable consistency check.

## Quality Gates

- Output follows `textbook` memory and template conventions.
- Critical genre rules are not bypassed.
- Human approval is requested for Pack-specific creative cruxes.
- The next stage can continue from durable files, not chat-only context.

## Error Handling

- If the active genre is different, stop and route to `/switch-genre`.
- If upstream memory is missing, create a gap report instead of inventing state.
- If the requested action conflicts with approved decisions, ask for confirmation.
- If confidence is speculative, label it and request review.
