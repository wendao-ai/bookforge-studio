# Consistency Engine Spec

The consistency engine enforces the active genre's definition of "coherent." It is a guardrail system, not a replacement for editorial judgment.

## Inputs

- Active project manifest: `projects/<project-id>/PROJECT.md`
- Active pack: `projects/<project-id>/genre-context/active-pack.yaml`
- Genre rules: `genre-packs/<genre>/consistency-rules.yaml`
- Project memory: `constitution/`, `registry/`, and `genre-context/genre-memory/`
- Changed artifact path from hook payload when available.

## Severity Levels

| Level | Meaning | Default action |
| --- | --- | --- |
| critical | Breaks the creative law of the genre | Block and request backtrack or approval |
| high | Likely damages reader trust or learning flow | Mark for review and require fix plan |
| medium | Local quality issue | Warn and record |
| low | Style or polish concern | Record only |

## Genre-Specific Definitions

- `scifi`: world laws, tech capability, timeline, nomenclature, and revelation curve.
- `textbook`: knowledge prerequisites, DAG integrity, cognitive load, exercises, and terminology.
- `romance`: emotional causality, relationship state, tension curve, character integrity, and beat coverage.
- `history`: source credibility, timeline, historiography, citation format, and disputed evidence handling.
- `fiction-general`: plot causality, character arc, theme continuity, pacing, and promises.
- `nonfiction-general`: thesis consistency, argument chain, evidence alignment, concept order, and counterargument handling.

## Check Output

Each check should emit:

- `rule_id`
- `level`
- `artifact`
- `status`: `pass`, `warn`, `block`, or `needs_review`
- `message`
- optional `suggested_fix`

## Fact-Layer vs Experience-Layer Checks

Consistency checks divide into two layers with different enforcement semantics. This prevents the engine from refereeing facts and judging taste at the same severity, which would inflate severity and dilute the meaning of `critical`.

- **Fact-layer checks (blockable)** verify objectively decidable state — timeline, world-law, knowledge prerequisites, causal or argument logic, terminology, registered promises and foreshadowing. A violation is a correctness defect. These map to `critical`/`high` severity and use `block`/`needs_review` status. The engine enforces these hard.
- **Experience-layer checks (advisory)** judge reader experience — pacing, emotional rhythm, hook strength, voice, delight. A violation is a taste/quality signal, not a correctness defect. These typically map to `medium`/`low` severity and use `warn` status. They inform the author and the reader panel but do not block on their own.

Guidance for genre packs: when authoring `consistency-rules.yaml`, place objectively verifiable constraints at `critical`/`high` (fact layer) and reserve `medium`/`low` for experience-layer guidance. A `critical` finding should always mean "a verifiable creative law was broken" — never "it did not feel right."

## Blocking Rules

Critical findings return exit code `1`. Human review gates return exit code `2`. All checks append events to `.history/events.jsonl` when an active project is available.

## Backtrack Protocol

When a critical issue appears after a stage exit, identify the earliest artifact that introduced the contradiction. The Director layer chooses one of:

- revise current artifact only,
- regenerate chapter plan,
- revise outline,
- revise constitution or active genre decision.
