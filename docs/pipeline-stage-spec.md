# Pipeline Stage Spec

BookForge uses a six-stage pipeline. Each stage has explicit inputs, outputs, and exit gates.

## S1 Ideation

Inputs: author idea, constraints, target audience, preferred language, intended length.

Outputs:

- `constitution/dialogue_log.jsonl`
- `constitution/brief.yaml`
- `constitution/concept_tree.json`
- `genre-context/active-pack.yaml`

Exit gates:

- Genre is confirmed.
- Brief contains audience, promise, thesis/story seed, non-goals, and uniqueness anchor.
- Human approval is recorded.

## S2 Outline

Inputs: constitution files, active pack, structure paradigm, reader profiles.

Outputs:

- `outline/candidates/`
- `outline/outline.yaml`
- `registry/promises.yaml`

Exit gates:

- At least two outline candidates were considered unless the author requests a single-track outline.
- Selected outline is compatible with the active genre paradigm.
- Promises, foreshadowing, or argument commitments are registered.

## S3 Extended Outline

Inputs: selected outline, genre memory, dependency rules.

Outputs:

- `extended-outline/`
- chapter plans with inputs, outputs, dependencies, and review gates.

Exit gates:

- Each chapter has purpose, reader effect, key concepts/events, and dependencies.
- Genre-specific memory updates are identified.
- Stage lead confirms no critical structural issue remains.

## S4 Drafting

Inputs: extended outline, project memory, style anchors, active pack.

Outputs:

- `drafts/chapters/<ch_id>/v0_skeleton.md`
- `drafts/chapters/<ch_id>/v1_rough.md`
- `drafts/chapters/<ch_id>/v2_refined.md`
- `drafts/chapters/<ch_id>/v3_polished.md`

Exit gates:

- V3 draft satisfies style anchor and chapter plan.
- Consistency checks have no critical violations.
- Any high-severity issues are captured in review notes.

Writing brief format (produced by `/inject-context`, consumed by `draft-v0` through `draft-v3`): see `.claude/docs/writing-brief-spec.md` — five sections (Commission / Story / Characters / Craft / Landing), data-source precedence chain, and system-term containment rules.

Chapter summary (long-range memory, produced after `draft-v1`, final-updated at `draft-v3`): see `.claude/docs/chapter-summary-spec.md` — six fields (chapter_meta / what_happened / character_state_changes / foreshadowing_actions / promise_actions / key_numbers). Required for serial genres (webnovel/series); single-book optional. Feeds `/review-chapter` continuity checks and `/query-project-state` long-range queries;回写 registry 开放环状态机.

## S5 Review

Inputs: V3 drafts, reader profiles, quality metrics, consistency reports.

Outputs:

- `review/reader_reports/`
- `review/controversy_map.yaml`
- fix cascade plan.

Exit gates:

- Target readers have reported on genre-specific quality dimensions.
- Conflicting feedback is summarized.
- Fixes are assigned or explicitly deferred.

## S6 Typeset

Inputs: approved chapters, typeset config, export target.

Outputs:

- `typeset/final.docx`
- `typeset/final.epub`
- `typeset/final.pdf` when a PDF engine is available.

Exit gates:

- Export artifacts exist or toolchain gaps are reported.
- Metadata and front/back matter are present.
- Final consistency check is clean enough for delivery.
