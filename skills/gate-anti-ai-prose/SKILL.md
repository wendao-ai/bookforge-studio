---
name: "gate-anti-ai-prose"
description: "反AI腔硬质量门。对草稿做句式/词汇/节奏/情感扫描，命中禁令则改写，朗读测试去演讲腔。draft-v3 之后、typeset 之前的硬门。消费 cross-genre/001-anti-ai-prose-gate。"
category: "review"
---

# /gate-anti-ai-prose

## Purpose

对正文草稿执行反 AI 腔硬质量门扫描与改写，消除否定平行结构、排比、过渡词泛滥、修辞堆砌、空泛情绪词、每段升华等 AI 写作模式。这是 draft-v3-polish 之后、typeset 之前的**硬门**，不通过不放行。

跨 genre 通用（叙事散文标准；诗歌/学术论述类由 pack 覆盖调整）。方法论见 [capability-library/cross-genre/001-anti-ai-prose-gate.md](../../../capability-library/cross-genre/001-anti-ai-prose-gate.md)。

## Inputs

- 待检查草稿（`projects/<id>/drafts/` 下 v2/v3 版本）。
- 活动 Genre Pack 的 `quality-metrics.yaml`（若有 prose 相关覆盖）。
- 方法论资产 [001-anti-ai-prose-gate.md](../../../capability-library/cross-genre/001-anti-ai-prose-gate.md)。

## Outputs

- 扫描报告：命中的句式禁令 / 词汇禁令 / 节奏问题 / 情感问题清单（含位置）。
- 改写后的草稿片段（遵循版本规则：`cp` 新版本后 Edit）。
- 通过/未通过判定。未通过则标 `exit_blocked: anti-ai-gate`。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载草稿与 active pack 的 quality-metrics（确认有无文体覆盖）。
2. **句式扫描**：全文搜索 [001-anti-ai-prose-gate.md](../../../capability-library/cross-genre/001-anti-ai-prose-gate.md) 句式禁令清单（否定平行/排比/列举/收束/升华），命中则改写。
3. **词汇扫描**：搜索词汇禁令清单，命中则替换或删除；过渡词/比喻连接词计数（全文 ≤2 / ≤3）。
4. **节奏抽样**：随机抽 3-5 段，检查长短句混用、连续长句、形容词节制、具体名词替代抽象形容词。
5. **朗读测试**：默读全文，凡是"像演讲稿/朗诵"的段落重写。
6. **自检对照**：每段删修饰词后内容是否为零、句式是否对称到像诗、连续相同语法结构。
7. 改写遵循版本规则（`cp` 新版本文件后 Edit，[rules/chapter-draft.md](../../rules/chapter-draft.md)）。
8. 全部通过才放行；未通过标 `exit_blocked` 并列出剩余项。

## Quality Gates

- 零句式禁令命中（否定平行/排比/列举/收束/每段升华）。
- 过渡词全文 ≤2 次、比喻连接词 ≤3 次。
- 无连续 3 句以上超 20 字长句。
- 无空泛情绪词与宏大空洞修辞。
- 朗读测试无演讲腔段落。
- 改写版本链完整。

## 非虚构产业书 AI 腔特化清单（v4 重构补 · dlg-037）

> 通用清单（句式/词汇禁令）针对科幻/叙事散文（"时代的洪流""命运的残酷"）。**非虚构产业书 AI 腔形态不同**——glm-5.2 等模型在产业书里偏好：戏剧化比喻、强化副词、戏剧化动词、过度对仗。本节是产业书特化禁令。

### 戏剧化比喻（清）
- "递了（一把更快的）刀""换刀""血洗""碾压""屠杀"——资源/竞争的暴力戏剧化具象 → 改平实动词（"提供工具""挤压""胜过"）

### 强化副词（清）
- "更狠""死死的""彻底""完全""根本（不）"——口语化过度强化 → 删或改准确

### 戏剧化动词（清）
- "重写（了一遍）""颠覆""重构""重塑""改写"——把普通变化说成根本变革 → 改"改变/调整/更新/转变"

### 过度对仗疑问（清）
- "是X，还是Y""不是X，而是Y"——工整对仗疑问，产业书 AI 腔标志 → 改直白陈述

### 强调副词（限频）
- "本质上""根本上""底层逻辑"——AI 偏好强调，过度堆砌 → 全文 ≤2 次

### 改写示范（ai-tob-endgame 实证）
- 错："是给你换了一把更快的刀，还是把你的生意逻辑整个重写了一遍？"
- 对："是给你更好的工具，还是改变了这门生意的根本逻辑？"
- 错："把这三个问题做更狠的版本"
- 对："把这三个问题再追问一层"
- 错："三个原子约束把传统 toB 服务商卡得死死的"
- 对："三个原子约束把传统服务商卡住"

### 边界（保留）
- "服务商你"对话感（产业书调性，非 AI 腔）——保留
- "原子约束""价值捕获鸿沟"等术语（本书概念）——保留
- 2026 最新数据（refresh 产物）——完整保留

## Error Handling

- 若 active pack 是诗歌/韵文体：提示句式禁令针对叙事散文，按 pack 覆盖调整或跳过本门。
- 若是学术论述类：过渡词限制可放宽（仍有正当用途），但空泛修辞与每段升华仍禁；按 nonfiction pack 调整阈值。
- 若命中数量过大（整篇 AI 腔严重）：不建议逐句改，标 `exit_blocked` 并建议走 `/revise-by-failure-mode` 的"AI 腔"模式整体重写。
- 本门不管事实正确性——事实问题交 `/fix-cascade` 的 factual 软隔离。

## 关联

- 方法论：[001-anti-ai-prose-gate.md](../../../capability-library/cross-genre/001-anti-ai-prose-gate.md)
- 协同：`/revise-by-failure-mode`（AI 腔失败模式调本门）、`/fix-cascade`（事实软隔离互补）
- 时机：draft-v3-polish 后、`/typeset-pdf`·`/export-docx` 前
- 规则：[rules/chapter-draft.md](../../rules/chapter-draft.md)（版本链）
