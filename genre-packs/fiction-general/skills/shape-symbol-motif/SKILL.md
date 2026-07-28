---
name: "shape-symbol-motif"
description: "fiction-general 象征母题塑造。设计核心象征物/母题，追踪其在全文的意义演变（开头建立→转折动摇→结尾换意义），承载主题与首尾呼应。消费 theme_consistency 指标。"
category: "fiction-general"
---

# /shape-symbol-motif

## Purpose

设计核心象征/母题并追踪其意义演变，让抽象主题落到具体可感的物件/意象上，同时承载首尾呼应。

## Inputs

- `constitution/brief.yaml`（核心主题）。
- `/develop-character-arc` 的弧光节点（象征意义随弧光转变）。
- `/track-promise-payoff` 的首尾呼应需求。
- `quality-metrics.yaml`（theme_consistency）。
- 当前草稿。

## Outputs

- 象征母题档案：核心象征物/意象 + 常规意义 + 各阶段意义演变（开头→转折→结尾换意义）。
- 母题出现追踪表（章节 × 意义）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 从主题提取 1-2 个核心象征物/意象/反复短语（具体可感，非抽象概念）。
3. 设计意义演变：开头建立常规意义 → 转折期意义动摇 → 结尾换意义（呼应开篇但意义已随人物弧光改变）。
4. 母题出现须自然（不生硬植入），每次出现承载当前阶段的意义。
5. 不过度解释象征——让读者体会，不点破（对接 `/gate-anti-ai-prose` 的去说教）。
6. 与 `/track-promise-payoff` 的首尾呼应对接：象征物结尾换意义 = 一种呼应兑现。
7. 记录决策。

## Quality Gates

- 核心象征 1-2 个，具体可感（非抽象概念）。
- 意义演变轨迹清晰（开头→转折→结尾换意义）。
- 象征不生硬植入，不过度解释。
- 结尾换意义呼应开篇。

## Error Handling

- 若象征过多（>2）：建议精简，避免象征泛滥。
- 若象征被直接点破解释：标说教风险，调 `/revise-by-failure-mode`。
- 若象征意义未演变（结尾仍是开头意义）：标 theme_consistency 风险，设计意义转变。

## 关联

- 指标：theme_consistency
- 协同：`/check-theme-consistency`（主题承载）、`/track-promise-payoff`（首尾呼应）、`/develop-character-arc`（意义随弧光变）
- 素材：源 short-sci-fi-novel-writer plot-design（结尾回应开头/物件换意义）
