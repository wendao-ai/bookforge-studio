---
name: "design-character-arc"
description: "人物弧光设计。为主要人物设计八要素弧光（初始状态/外部目标/内部缺口/错误信念/关键冲突/转折选择/代价/结尾状态），选正向/负向/平坦模板，确保转变落在溯源的可变区。消费 cross-genre/001-character-arc-eight-elements。"
category: "drafting"
---

# /design-character-arc

## Purpose

为主要人物设计结构化人物弧光，避免转变突兀、人物被剧情推着走、靠顿悟完成转变。本 skill 消费 `/trace-character-foundation` 产出的可变/不可变边界，确保弧光的"改变"落在可变区。

跨 genre 通用：fiction-general / romance / scifi / biography 共享。方法论见 [capability-library/cross-genre/001-character-arc-eight-elements.md](../../../capability-library/cross-genre/001-character-arc-eight-elements.md)。

## Inputs

- `/trace-character-foundation` 产出的人物溯源档案（含可变/不可变边界）。
- `constitution/brief.yaml`（读者承诺、核心矛盾）。
- 已选大纲与剧情引擎（`/select-plot-engines` 产出，若有）。
- 活动 Genre Pack 的 `templates/character-arc.yaml`（若存在）。
- 方法论资产 [001-character-arc-eight-elements.md](../../../capability-library/cross-genre/001-character-arc-eight-elements.md)。

## Outputs

- `projects/<id>/genre-context/character-arcs/<character>.yaml`：八要素结构化弧光。
- 弧光类型（正向/负向/平坦）+ 转变落点（须在可变区）+ 转折铺垫清单（≥2 处）。
- 与剧情引擎的衔接点（转折/代价落在哪个引擎节点）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载活动项目、人物溯源档案、active pack。
2. 对每个主要人物，按 [001-character-arc-eight-elements.md](../../../capability-library/cross-genre/001-character-arc-eight-elements.md) 填八要素。
3. 选择弧光模板（正向/负向/平坦）；群像作品至少一个主要人物有完整弧光。
4. **校验可变/不可变边界**：弧光计划的所有"改变"必须落在溯源的可变区。若落在不可变区 → 要么改弧光（改变落点），要么标记为"人物失真风险"提请作者确认。
5. 为转折选择设计 ≥2 处前置铺垫（细节/对话/行为）。
6. 确认代价是真实、不可逆的失去（非象征性）。
7. 标注人物与核心处境的纠缠点（处境如何放大缺口/制造两难/提供契机）。
8. 与 `/select-plot-engines` 的引擎节点对齐：转折选择落在哪个引擎的升级阶梯，代价在高潮如何兑现。
9. 写入项目文件，记录决策与未决问题。

## Quality Gates

- 每个主要人物弧光含完整八要素（短篇可压缩为四要素最小集）。
- 转变落点 100% 在可变区；落在不可变区的必须标注 risk 并人审。
- 转折选择有 ≥2 处前置铺垫。
- 代价是真实不可逆失去。
- 弧光不靠口号/顿悟完成。
- 结尾状态与初始状态形成可辨识对比。

## Error Handling

- 若无 `/trace-character-foundation` 产出：报错指向该 skill，不凭空设计弧光（无地基的弧光会失真）。
- 若弧光需改变不可变区特质：标 `immutable_violation` risk，提请作者——要么改弧光落点，要么（传记类）承认这是叙事重构而非事实并标注。
- 若弧光与已批准大纲的情节转折矛盾：标 conflict，提请改弧光或改大纲。
- 若多个主要人物弧光同质（都正向顿悟）：提示增加多样性（至少一个负向或平坦）。

## 关联

- 方法论：[001-character-arc-eight-elements.md](../../../capability-library/cross-genre/001-character-arc-eight-elements.md)
- 上游：`/trace-character-foundation`（提供可变/不可变边界）
- 情节：`/select-plot-engines`（弧光转折/代价落在引擎节点）
- 修订：`/revise-by-failure-mode`（弧光断裂失败模式 → 模式 4）
