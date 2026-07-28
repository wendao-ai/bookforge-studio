---
name: "revise-by-failure-mode"
description: "失败模式分类修订。收到批评后先分类失败模式（钩子弱/AI腔/弧光断裂等11类），针对该模式重写整个相关段落而非打补丁，再判断经验是否可迁移沉淀（防过拟合）。消费 cross-genre/001-revision-evolution-loop。与 /fix-cascade 互补。"
category: "review"
---

# /revise-by-failure-mode

## Purpose

收到对草稿的批评后，按"先分类失败模式→针对性重写→防过拟合沉淀"三步处理，避免打补丁（治标不治本）和过拟合（单次反馈污染全局）。本 skill 是创作者面对反馈时的修订方法，与 `/fix-cascade`（review 流水线意见分流）互补。

跨 genre 通用。方法论见 [capability-library/cross-genre/001-revision-evolution-loop.md](../../../capability-library/cross-genre/001-revision-evolution-loop.md)。

## Inputs

- 待修订草稿（`projects/<id>/drafts/` 下某版本）。
- 批评/反馈内容（来自读者模拟、作者、或 `multi-dim-feedback`）。
- 相关上游档案（人物溯源/弧光/引擎，用于针对性重写）。
- 方法论资产 [001-revision-evolution-loop.md](../../../capability-library/cross-genre/001-revision-evolution-loop.md)。

## Outputs

- 失败模式分类记录（归类到 11 类之一或多类）。
- 针对性重写后的草稿片段（遵循章节版本规则：`cp` 新版本文件后 Edit，保留版本链）。
- 经验可迁移性判断（task-local 修复 / 观察区候选 / 稳定规则候选）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载草稿与反馈，按 [001-revision-evolution-loop.md](../../../capability-library/cross-genre/001-revision-evolution-loop.md) 第一步把批评归类到失败模式（11 类）。
2. 若多重失败：按严重程度排序（设定不自洽 > AI 腔 > 弧光 > 其他），一次只针对一种主导失败模式重写，避免改到失控。
3. **针对性重写**（第二步）：按该失败模式的重写流程重写整个相关段落或结构，非打补丁：
   - 钩子弱 → 删背景开头，前三段植入异常/失去/危机
   - AI 腔 → 调 `/gate-anti-ai-prose` 扫描改写
   - 弧光断裂 → 重走 `/design-character-arc`，强化初始状态+转折铺垫
   - 人物扁平 → 给可见欲望+私人伤口，调 `/trace-character-foundation` 补强
   - 冲突不升级 → 检查 `/select-plot-engines` 升级阶梯，设计 ≥3 次升级
   - 其余模式见资产
4. **版本规则**：重写须 `cp` 旧版本为新版本文件后 Edit，禁在旧版本直接 Edit+mv（[rules/chapter-draft.md](../../rules/chapter-draft.md)）。
5. **判断可迁移性**（第三步）：单次偶发→task-local 不记录；重复/高信号/可迁移→记录到观察区候选；满足"重复或高信号+可迁移+不冲突"→提为稳定规则候选，对接 `/harvest-writing-pattern`。
6. 记录决策与未决问题。

## Quality Gates

- 每条批评已归类到具体失败模式（非"整体不好"）。
- 重写的是相关段落/结构，不是只改用户指出的句子。
- 版本链完整（新版本文件独立快照）。
- 单次反馈未被提升为全局规则（防过拟合）。
- 稳定规则候选记录了来源作品与反馈内容（可追溯）。

## Error Handling

- 若反馈无法归类到 11 类：标注为新失败模式候选，记录到观察区，不强行归类。
- 若重写涉及 critical 一致性违规：先走 `/fix-cascade` 的 backtrack，不在本 skill 内静默改。
- 若重写需改 constitution/大纲：强制人审 + 记 decision event，不自动改宪法。
- 若与 `/fix-cascade` 同时触发：fix-cascade 管意见分流，本 skill 管重写执行；先分流定 action=revise，再用本 skill 重写。

## 关联

- 方法论：[001-revision-evolution-loop.md](../../../capability-library/cross-genre/001-revision-evolution-loop.md)
- 互补：`/fix-cascade`（意见分流）、`/harvest-writing-pattern`（沉淀）
- 依赖：`/gate-anti-ai-prose`、`/design-character-arc`、`/trace-character-foundation`、`/select-plot-engines`
- 规则：[rules/chapter-draft.md](../../rules/chapter-draft.md)（版本链）
