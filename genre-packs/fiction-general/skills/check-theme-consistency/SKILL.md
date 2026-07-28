---
name: "check-theme-consistency"
description: "fiction-general 主题一致性检查。从 brief 提取核心主题，逐章检查主题深化轨迹，防漂移与说教。守 theme_drift 规则，消费 theme_consistency 指标。"
category: "fiction-general"
---

# /check-theme-consistency

## Purpose

确保主题在全文逐渐深化而非中途消失/漂移/说教。从 brief 核心论点提取主题，逐章检查主题轨迹。

## Inputs

- `constitution/brief.yaml`（核心主题/论点）。
- `/design-story-arc`、`/develop-character-arc`（主题如何通过弧光承载）。
- `consistency-rules.yaml`（theme_drift）、`quality-metrics.yaml`（theme_consistency）。
- 当前草稿。

## Outputs

- 主题深化轨迹：每章主题呈现方式（显性陈述/行为承载/代价显现/结尾回响）。
- theme_drift 检查记录（漂移/说教/突然拔高）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 从 brief 提取核心主题/论点，明确"主题通过人物代价与结局显现，而非台词陈述"。
3. 逐章标注主题呈现方式，检查深化轨迹：主题应逐渐深化，不在中途消失或转向。
4. 检查 theme_drift 三种表现：主题中途消失/转向无铺垫/被角色直接说教（说教腔）。
5. 检查结尾是否"突然拔高主题"（禁止）——主题应在结尾通过人物选择回响，而非总结陈词。
6. 主题与人物弧光对齐：弧光的转折/代价是否承载主题（对接 `/design-character-arc`）。
7. 记录决策。

## Quality Gates

- 主题深化轨迹逐章可追溯。
- 无 theme_drift（消失/转向/说教）。
- 结尾无突然拔高主题。
- 主题通过人物代价显现，非台词陈述。

## Error Handling

- 若主题中途消失：标 theme_drift，建议在相关章节注入主题承载场景。
- 若角色说教：调 `/revise-by-failure-mode` 的"说教腔"模式（模式 9）。
- 若主题与 brief 核心论点不符：标 conflict，提请确认改主题还是改 brief。

## 关联

- 规则：theme_drift（medium）/ 指标：theme_consistency
- 协同：`/develop-character-arc`（弧光承载主题）、`/revise-by-failure-mode`（说教腔）
- 素材：源 short-sci-fi-novel-writer continuity-and-quality（主题深化/禁止拔高）
