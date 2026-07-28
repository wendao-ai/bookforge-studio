---
description: "Outline artifact standards"
globs:
  - "projects/*/outline/**"
---

# Outline Rules

## Mandatory Standards

- `outline.yaml` must include the selected structure, chapter list, reader promise per section, genre paradigm alignment, dependencies, and open risks.
- Candidate outlines belong in `outline/candidates/` and must record why they were accepted or rejected.
- The selected outline must reference the active genre's `structure-paradigm.yaml`.
- Promises, foreshadowing, concepts, or argument commitments must be added to `registry/`.
- Outline approval is required before extended outline work.
- `outline.yaml` 必须含每章 `word_budget` 分配，总和须匹配 `brief.target_length`，偏差 >20% 触发结构风险标注。

## Anti-Patterns

- A flat chapter list with no reader effect or dependency information.
- Selecting an outline without comparing alternatives when the direction is ambiguous.
- Ignoring genre-specific structure rules.
- Moving to drafting while outline risks remain unresolved.
- 单章字数超均值 2 倍而无说明（结构失衡、主线被稀释的典型信号）。
