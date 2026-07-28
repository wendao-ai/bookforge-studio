# Genre Detection Guide

Genre detection converts the author's intent into an active creative paradigm.

## Sources

- Author's explicit words.
- Dialogue log.
- `_detection-rules.yaml`.
- Existing constitution draft.
- Similar prior projects in `capability-library/`.

## Output Shape

```yaml
primary_genre: scifi
sub_genre: hard-scifi
secondary_genre: null
confidence: observed
signals:
  explicit_keywords: []
  intent_patterns: []
requires_author_confirmation: true
```

## Confidence

- `observed`: author explicitly names the genre or accepts a proposed genre.
- `inferred`: several strong signals point to one genre.
- `speculated`: weak signals; ask a clarifying question before loading a pack.

## Detection Rules

Use `genre-packs/_detection-rules.yaml` first. If multiple packs match, choose the pack that controls the main reader promise as `primary_genre` and record the other as `secondary_genre`.

## Clarifying Questions

Ask when:

- confidence is `speculated`,
- two genres imply different structure,
- a mixed genre changes critical consistency rules,
- the user's stated genre conflicts with the actual creative promise.

## Genre Switch

Use `/switch-genre` only when a later artifact proves the initial genre wrong or the author deliberately changes direction. A switch requires a regeneration impact list.
