---
name: "design-life-arc"
description: "传记人生弧光设计。调用 /design-character-arc 设计八要素弧光，按 structure-paradigm 人生阶段映射，守 immutable-trait-fidelity（不改真实人物不可变区）。消费共享能力 + 传记事实约束。"
category: "biography"
---

# /design-life-arc

## Purpose

为传主设计人生弧光，受事实约束。调 `/design-character-arc` 八要素，按人生阶段（childhood/growth/achievement/turning/later-life）映射，转折对齐 turning 阶段；不可改真实人物不可变区特质。

## Inputs

- `/trace-subject-foundation` 产出（受事实约束的可变/不可变边界）。
- subject-archive + life-timeline。
- 共享 skill `/design-character-arc`、`/select-plot-engines`。
- 本 Pack `structure-paradigm.yaml`、`consistency-rules.yaml`。

## Outputs

- 传主人生弧光档案（八要素 + 人生阶段映射 + 转折对齐 turning）。
- immutable-trait-fidelity 校验记录（越界项标 narrative_reconstruction）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 biography。
2. 调 `/design-character-arc` 填八要素，但初始状态/转折选择/代价须有 fact_basis。
3. 按 `structure-paradigm.yaml` 人生阶段映射弧光节点；转折选择对齐 turning 阶段。
4. **immutable-trait-fidelity 校验**：弧光改变不得落在真实人物不可变区特质。若叙事需要改变，标 narrative_reconstruction + reconstruction_reason，人审。
5. 代价须事实支撑（fact-narrative-map 标 fact），真实不可逆。
6. 可调 `/select-plot-engines` 组织真实事件（引擎用于组织非虚构情节，不改事实）。
7. 记录决策；传主核心论点/人生定论人审。

## Quality Gates

- 八要素齐全，转折对齐 turning 阶段。
- 无未标注的不可变区改变（越界项全标 narrative_reconstruction + 人审）。
- 代价有 fact_basis。
- 传主定论人审。

## Error Handling

- 若无 `/trace-subject-foundation` 产出：报错指向该 skill。
- 若弧光需改不可变区：标 immutable_violation risk，人审确认是叙事重构还是放弃该弧光。
- 若事实不足以支撑转折：标 insufficient_basis，提请补资料或调整弧光。

## 关联

- 共享：`/design-character-arc`、`/select-plot-engines`
- 上游：`/trace-subject-foundation`
- 规则：immutable-trait-fidelity（high）
