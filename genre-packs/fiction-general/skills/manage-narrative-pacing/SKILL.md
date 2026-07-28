---
name: "manage-narrative-pacing"
description: "fiction-general 叙事节奏管理。按 structure-paradigm 五阶段分配节奏权重，中段用六功能防 sag，高潮承载人物选择×处境的转折与代价。守 pacing_sag 规则，消费 pacing 指标。"
category: "fiction-general"
---

# /manage-narrative-pacing

## Purpose

管理叙事节奏，确保故事持续推进不原地踏步。按 hook/development/complication/deepening/payoff 五阶段分配节奏权重，中段用"六功能"防止 sag（推进力下降），高潮承载转折选择与代价。

## Inputs

- `/design-story-arc` 的引擎组合与升级阶梯。
- `/develop-character-arc` 的人物弧光节点。
- `structure-paradigm.yaml`、`consistency-rules.yaml`（pacing_sag）、`quality-metrics.yaml`（pacing）。
- 当前草稿（若已有）。

## Outputs

- 节奏图：五阶段 × 节奏权重 × 关键节点（钩子/升级×N/高潮/余韵）。
- 中段六功能分配表（每段至少完成一种功能）。
- pacing_sag 检查记录。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 按 `structure-paradigm.yaml` 五阶段定节奏权重：hook 紧凑、development 升级、complication 加压、deepening 最重（高潮）、payoff 收束留余韵。
3. 中段（development/complication）每段至少完成一种功能：推进情节/加深人物/暴露世界/增强冲突/制造悬念/重新理解。连续多段只解释设定而无功能 = pacing_sag。
4. 高潮须是人物选择 × 核心处境的共同作用（对接 `/design-character-arc` 转折选择 + `/select-plot-engines` 升级阶梯顶点），代价在开头不可接受、现在不得不承受。
5. 结尾完成至少一种效果（情感回响/观念反转/命运余韵/人物完成或拒绝改变/回应开头），不突然拔高主题。
6. 检查 pacing_sag：标记推进力下降的段落，重排或注入功能。
7. 记录决策。

## Quality Gates

- 五阶段节奏权重明确，deepening 最重。
- 中段无连续"只解释设定不推进"的段落。
- 高潮 = 人物选择 × 处境，代价真实。
- 结尾有余韵，不拔高主题。

## Error Handling

- 若无 `/design-story-arc`：报错指向该 skill。
- 若中段 sag 严重：建议调 `/revise-by-failure-mode` 的"冲突不升级"模式（模式 10）。
- 若高潮与弧光转折脱节：标 conflict，对齐 `/design-character-arc`。

## 关联

- 规则：pacing_sag（medium）/ 指标：pacing
- 上游：`/design-story-arc`、`/develop-character-arc`
- 素材：源 short-sci-fi-novel-writer plot-design（中段六功能/高潮/结尾六效果）
