---
description: "Project registry standards"
globs:
  - "projects/*/registry/**"
---

# Registry Rules

## Mandatory Standards

- `concepts.yaml` tracks names, definitions, first appearance, aliases, and status.
- `promises.yaml` tracks reader promises, origin, payoff plan, and fulfillment status.
- `foreshadowing.yaml` tracks setup, target payoff, chapter references, and risk.
- Style anchors must include exemplar passages, voice constraints, and forbidden drift.
- Registry updates must be append-friendly and auditable.

## 开放环状态机（长程记忆层）

`foreshadowing.yaml` 和 `promises.yaml` 的每个条目除现有字段外，**连载品类（webnovel/系列）建议**加状态机字段，追踪"写到第 N 章的实际进度"（对标 webnovel memory-contract open-loops，但用 append-friendly 方式，不造第二事实源）：

- `expected_payoff_chapter`：预期回收/兑现的章节（规划时填）
- `current_status`：当前状态（`open` / `near_due` / `overdue` / `closed`）——由 chapter summary 的 actions 回写
- `last_checked_chapter`：最后一次被 summary 检查/推进的章（用于 urgency 计算）

状态判定：
- `open`：未到预期回收章
- `near_due`：接近 expected_payoff_chapter（urgency > 0.8）
- `overdue`：超过 expected_payoff_chapter 未回收（触发 `foreshadowing_overdue` 规则）
- `closed`：已回收/兑现（summary 标记）

这是 registry 的 append-friendly 增强（现有条目不带也合规，但连载品类建议补全）。状态机字段由 `/review-chapter`（continuity 维度）和 chapter summary spec（`.claude/docs/chapter-summary-spec.md`）联动维护。

## Anti-Patterns

- Introducing terms or promises only inside chapter prose.
- Renaming concepts without aliases.
- Leaving promises without payoff owners.
- Using registry files as freeform notes instead of structured state.
