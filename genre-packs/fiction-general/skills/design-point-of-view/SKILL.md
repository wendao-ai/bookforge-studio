---
name: "design-point-of-view"
description: "fiction-general 视角设计。选定 POV 策略（第一人称/第三限知/全知/多视角），维护视角一致性，与人物弧光对齐。消费 voice 指标。"
category: "fiction-general"
---

# /design-point-of-view

## Purpose

选定并维护 POV（视点）策略，确保视角一致、信息释放受控、承载弧光的人物优先作为主视角。

## Inputs

- `constitution/brief.yaml`（读者代入对象、读者承诺）。
- `/develop-character-arc` 的人物弧光（谁承载主弧光）。
- `/select-plot-engines` 的信息释放需求（真相分层等引擎需控信息）。
- `quality-metrics.yaml`（voice）。
- 当前草稿。

## Outputs

- POV 策略：视角类型 + 主视角人物 + 转换规则（若多视角）+ 信息释放边界。
- 视角一致性检查记录。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 选 POV 策略：
   - 第一人称：强代入、限知、适合单人物弧光。
   - 第三人称限知（单人物）：控信息、代入较强、最常用。
   - 第三人称全知：宏大叙事、多线、代入弱。
   - 多视角轮替：群像、多弧光、须明确转换标记。
3. 承载主弧光的人物优先作为主视角（对接 `/develop-character-arc`）。
4. 定信息释放边界：限知视角不泄露人物未知信息；真相分层类引擎（`/select-plot-engines` 引擎 J）须靠视角控制信息。
5. 维护视角一致性：不随意切换；转换有明确标记（章节/分隔线）；同一场景内不跳视角。
6. 检查草稿视角违规（限知视角泄露、无标记转换）。
7. 记录决策。

## Quality Gates

- POV 策略明确，主视角承载主弧光。
- 限知视角不泄露人物未知信息。
- 视角转换有标记，同场景不跳视角。
- 信息释放与引擎需求一致。

## Error Handling

- 若限知视角泄露未知信息：标违规，改视角或改信息释放时机。
- 若视角频繁无标记切换：标 voice 风险，建议固定视角或加转换标记。
- 若主视角与主弧光人物不一致：标 conflict，确认改视角还是改弧光归属。

## 关联

- 指标：voice
- 协同：`/develop-character-arc`（主视角=主弧光人物）、`/select-plot-engines`（信息释放）、`/style-enhancement`（voice 落地）
- Agent：voice-continuity-editor
