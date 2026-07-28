---
name: "map-scene-causality"
description: "fiction-general 场景因果映射。为每个场景标注因果链（前置→本场景→后果），守 plot_causality_gap critical 规则，追踪时间线/动机延续/伏笔/物件。"
category: "fiction-general"
---

# /map-scene-causality

## Purpose

为每个场景建立因果链，确保关键转折有因果支撑（critical），无时间悖论、动机断裂、伏笔悬空、物件失踪。

## Inputs

- `/design-story-arc` 的场景结构。
- `/develop-character-arc` 的人物动机。
- `consistency-rules.yaml`（plot_causality_gap critical）、`quality-metrics.yaml`（plot_causality）。
- 当前草稿。

## Outputs

- 场景因果图：每场景的 causes（前置场景/事件）→ action → effects（后续场景/状态变化）。
- 连贯性追踪表：时间线/人物动机延续/伏笔回收/物件去向/关系变化。
- plot_causality_gap 检查记录（critical 违规阻断）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 为每个场景标注因果链：前置 cause → 本场景 action → 后续 effect。
3. 关键转折（complication/deepening）必须有因果支撑——无前置铺垫的转折 = plot_causality_gap critical 违规。
4. 追踪连贯性 6 项：时间线合理/动机延续/伏笔回收/物件去向/关系变化可追踪/首尾呼应。
5. 发现矛盾在输出前修正，不留给读者。
6. critical 违规（关键转折无因果）阻断，走 `/fix-cascade` backtrack。
7. 记录决策。

## Quality Gates

- 每场景有因果链标注。
- 关键转折 100% 有前置因果支撑（critical）。
- 连贯性 6 项无悬空（伏笔回收/物件去向/动机延续）。
- 无时间悖论。

## Error Handling

- 若关键转折无因果：标 critical，阻断，回溯补铺垫或调整转折。
- 若伏笔悬空：标 promise_unpaid（high），纳入 `/track-promise-payoff`。
- 若与已有草稿矛盾：标 conflict，修草稿或修因果链并记 reason。

## 关联

- 规则：plot_causality_gap（critical）/ 指标：plot_causality
- 协同：`/track-promise-payoff`（伏笔/承诺）、`/fix-cascade`（critical backtrack）
- 素材：源 short-sci-fi-novel-writer continuity-and-quality（连贯性 10 项）
