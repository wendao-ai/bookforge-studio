---
description: "Constitution artifact standards"
globs:
  - "projects/*/constitution/**"
---

# Constitution Rules

## Mandatory Standards

- `brief.yaml` must define title, author intent, target readers, core promise, scope, non-goals, style direction, target length, genre decision, and uniqueness anchor.
- `dialogue_log.jsonl` must be append-only and keep one JSON object per dialogue event.
- `concept_tree.json` must distinguish core concepts, supporting concepts, unresolved questions, and author decisions.
- Human approval of the constitution must be recorded before outline work starts.
- Any change to genre, promise, thesis, ending, worldview, or historiography must create a decision event.
- `brief.yaml` 的 `target_length` 必须标注品类基准（如经管书 16-25 万字、技术教程 25-40 万字、小说 8-20 万字）；超基准 1.5× 须在 `open_questions` 标 high 风险并说明理由（多卷/分册须显式声明）。
- `brief.yaml` 的 `style_direction` 必须引用 `projects/<project-id>/style-corpus/style-anchor.yaml`；无对标书调研出处的凭空填写不予接受（由 `/benchmark-corpus-research` 产出，参见 [style-corpus.md](style-corpus.md)）。

## Anti-Patterns

- Starting outline work from chat memory only.
- Treating vague audience labels as sufficient.
- Burying major author decisions inside prose without structured fields.
- Editing dialogue history retroactively instead of appending corrections.
- 体量超过品类基准 2 倍而无多卷/分册声明（典型表现：把资料库当单本书交付，远超市场可接受体量）。
- 在 `style_direction` 凭空填写风格描述而无对标书调研支撑（典型表现：宪法里的风格只是形容词堆砌，草稿期 anchor-style 无可消费的 voice constraints）。
