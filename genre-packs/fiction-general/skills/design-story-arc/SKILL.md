---
name: "design-story-arc"
description: "fiction-general 故事弧线设计。调用 /select-plot-engines 选 2-3 引擎组合，对齐人物弧光转折/代价节点，按 structure-paradigm 落到章节结构。消费共享能力层。"
category: "fiction-general"
---

# /design-story-arc

## Purpose

fiction-general 专属故事弧线设计编排器。调用跨 genre 共享的 `/select-plot-engines` 选引擎组合，对齐 `/develop-character-arc` 的人物弧光节点，按本 Pack `structure-paradigm.yaml` 落到章节结构。

## Inputs

- `constitution/brief.yaml`（读者承诺）。
- `/develop-character-arc` 产出的人物弧光。
- 共享 skill `/select-plot-engines`。
- 本 Pack `templates/story-arc.yaml`、`structure-paradigm.yaml`、`consistency-rules.yaml`。

## Outputs

- `projects/<id>/genre-context/genre-memory/story-arc/` 下故事弧线档案（符合 story-arc.yaml 字段）。
- 引擎组合 + 升级阶梯 + 与弧光节点对齐表。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 调 `/select-plot-engines`：从读者承诺出发选 2-3 引擎组合，展开结构要素与升级阶梯。
3. 对齐 `/develop-character-arc` 的弧光：转折选择落在哪个引擎节点，代价在高潮如何兑现。
4. 按本 Pack `structure-paradigm.yaml` 的结构（hook/development/complication/deepening/payoff）落到章节。
5. 按 `templates/story-arc.yaml` 字段组装档案。
6. 运行 `consistency-rules.yaml` 的 plot_causality_gap / pacing_sag 检查。
7. 记录决策与未决风险。

## Quality Gates

- 引擎组合 2-3 个，主引擎与读者承诺一致。
- 弧光转折/代价有引擎节点承载。
- 章节结构符合 structure-paradigm。
- 无 plot_causality_gap / pacing_sag 违规。

## Error Handling

- 若无读者承诺：报错指向 `/finalize-constitution`。
- 若引擎与已批准大纲矛盾：标 conflict 提请确认。
- 若选 4+ 引擎：提示精简。

## 关联

- 编排：`/select-plot-engines`
- 模板：`templates/story-arc.yaml`、`structure-paradigm.yaml`
- 资产：[001-plot-engine-library](../../../../capability-library/cross-genre/001-plot-engine-library.md)
