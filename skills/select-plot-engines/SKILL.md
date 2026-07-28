---
name: "select-plot-engines"
description: "剧情引擎选择。从12个去科幻化剧情引擎中选2-3个组合，展开结构要素与升级阶梯，对齐人物弧光的转折/代价节点，落地到大纲。消费 cross-genre/001-plot-engine-library。"
category: "outline"
---

# /select-plot-engines

## Purpose

为活动项目选定剧情引擎组合并展开为具体情节结构，避免情节单薄或混乱、原地打转不升级、高潮与人物选择脱节。引擎是情节骨架，承载 `/design-character-arc` 的转折与代价。

跨 genre 通用：fiction-general / romance / scifi / biography 共享（传记时引擎用于组织真实事件而非虚构情节）。方法论见 [capability-library/cross-genre/001-plot-engine-library.md](../../../capability-library/cross-genre/001-plot-engine-library.md)。

## Inputs

- `constitution/brief.yaml`（读者承诺、核心矛盾）。
- `/design-character-arc` 产出的人物弧光（转折选择/代价节点）。
- 已选大纲结构（若有）。
- 活动 Genre Pack 的 `structure-paradigm.yaml`。
- 方法论资产 [001-plot-engine-library.md](../../../capability-library/cross-genre/001-plot-engine-library.md)。

## Outputs

- `projects/<id>/outline/plot-engines.yaml`：选定 2-3 引擎 + 主辅关系 + 每引擎结构要素/升级阶梯。
- 引擎节点与人物弧光转折/代价的对齐表。
- 与读者承诺的一致性校验（避免主引擎与承诺矛盾）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载活动项目、brief、人物弧光、active pack 的 structure-paradigm。
2. 从 brief 读者承诺出发，按 [001-plot-engine-library.md](../../../capability-library/cross-genre/001-plot-engine-library.md) 引擎总表选 4-6 个候选引擎。
3. 确定主辅关系（2-3 个组合），参照组合规则表，避开避免组合（E+E / 三以上并列 / 主引擎与承诺矛盾）。
4. 展开每引擎的结构要素与升级阶梯，落地到具体情节节点。
5. **对齐人物弧光**：转折选择落在哪个引擎的升级阶梯，代价在高潮如何兑现（与 `/design-character-arc` 交叉校验）。
6. 校验立场冲突（[[001-character-foundation-tracing]] 模块 D）是否被引擎承载——立场碰撞制造冲突，动摇制造转折。
7. 写入 `outline/plot-engines.yaml`，记录决策与未决风险。

## Quality Gates

- 引擎组合 2-3 个，有明确主辅关系。
- 主引擎与 brief 读者承诺一致（不矛盾）。
- 每个引擎的结构要素与升级阶梯已展开为具体节点（非空泛）。
- 弧光转折/代价有引擎节点承载。
- 借鉴灵感时改变设定/关系/赌注/规则/结尾中至少三个（避免情节链照搬）。

## Error Handling

- 若无读者承诺：报错指向 `/finalize-constitution`，不凭空选引擎。
- 若是传记：提示引擎用于组织真实事件，不能为套引擎改写事实；与事实冲突时以事实为准并标 `narrative_reconstruction`。
- 若引擎组合与已批准大纲结构矛盾：标 conflict，提请改引擎或改大纲。
- 若选了 4+ 引擎：提示精简到 2-3 个（结构混乱风险）。

## 关联

- 方法论：[001-plot-engine-library.md](../../../capability-library/cross-genre/001-plot-engine-library.md)
- 上游：`/finalize-constitution`（读者承诺）、`/design-character-arc`（转折/代价节点）
- 下游：`/synthesize-outline`、`/expand-chapter-plan`（引擎落地到章节）
- 修订：`/revise-by-failure-mode`（冲突不升级失败模式 → 模式 10）
