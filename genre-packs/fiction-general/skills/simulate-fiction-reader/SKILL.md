---
name: "simulate-fiction-reader"
description: "fiction-general 读者模拟。按 reader-profiles 模拟至少3类读者反应，按质量14项+禁止15项评判，产出读者报告与争议图，对接 multi-dim-feedback/consensus-analysis/fix-cascade。"
category: "fiction-general"
---

# /simulate-fiction-reader

## Purpose

按读者画像模拟读者反应，产出结构化读者报告，区分 taste 与 consistency 问题，为修订提供依据。

## Inputs

- `reader-profiles.yaml`（本 Pack 画像；若无则用通用虚构三类）。
- `quality-metrics.yaml`（全维度）。
- 当前草稿 + 上游档案（弧光/引擎/主题）。
- 共享 `/multi-dim-feedback`、`/consensus-analysis`、`/fix-cascade`。

## Outputs

- 读者报告：每类画像 × 章节/产物 × 质量维度 × findings × severity × feedback_type × 建议修复。
- `controversy_map.yaml`（读者分歧汇总）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 按读者画像模拟至少 3 类读者（含 1 类审视型）。
3. 评判维度（去科幻化质量 14 项）：核心处境清晰/处境推动人物命运/人物有血有肉/情节持续推进/开头有钩子/中段有升级/高潮有选择代价/结尾有余韵/背景感/语言情绪氛围/无前后矛盾/无模仿具体作者/有原创性/有完成度。
4. 区分 feedback_type：taste（个人偏好，默认 reject/defer）/ consistency（规则问题，进 revise）/ factual（事实问题，软隔离）。
5. 产出读者报告 + controversy_map（汇总分歧）。
6. 对接 `/multi-dim-feedback`、`/consensus-analysis`；factual 走 `/fix-cascade` 软隔离。
7. 记录决策。

## Quality Gates

- 至少 3 类读者画像（含 1 类审视型）。
- 每条 finding 有 severity + feedback_type + 建议修复。
- taste 与 consistency/factual 分开标注。
- 读者分歧有 controversy_map 汇总。

## Error Handling

- 若读者对事实判断不一致：factual 走软隔离，不自动改正文。
- 若全是正面反馈（无审视型批评）：提示增加审视型画像，避免过拟合赞美。
- 若 taste 与 consistency 混淆：重新标注 feedback_type。

## 关联

- 画像：`reader-profiles.yaml` / 指标：`quality-metrics.yaml` 全维度
- 下游：`/multi-dim-feedback`、`/consensus-analysis`、`/fix-cascade`
- 素材：源 short-sci-fi-novel-writer continuity-and-quality（质量 14 项 + 禁止 15 项，去科幻化）
