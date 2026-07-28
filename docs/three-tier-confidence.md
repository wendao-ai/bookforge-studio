# Three-Tier Confidence

BookForge uses confidence labels whenever evidence, genre detection, worldbuilding, or interpretation may be uncertain.

## Labels

| Label | Meaning | Use |
| --- | --- | --- |
| `observed` | Directly stated, cited, or present in project memory | Author decisions, source facts, explicit genre names |
| `inferred` | Strongly implied by available evidence | Genre detection, character motivation, likely reader expectation |
| `speculated` | Plausible but not yet supported | Technology extrapolation, historical interpretation, future plot consequence |

## Requirements

- Critical decisions should not stay `speculated`.
- Historical source claims must include source confidence separately from interpretation confidence.
- Science-fiction technology may be speculative, but its role in the world bible must be explicit.
- Textbook knowledge claims should be `observed` or expert-approved before final delivery.

## Recording Format

```yaml
claim: "The core technology requires energy scarcity to remain a plot constraint."
confidence: inferred
basis:
  - "constitution/brief.yaml"
  - "genre-context/genre-memory/world-bible/tech-tree.yaml"
needs_review: true
```
