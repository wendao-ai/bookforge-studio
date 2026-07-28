---
name: "check-biography-consistency"
description: "传记一致性检查。守 5 条 consistency-rules（2 critical + 2 high + 1 medium），产出违规清单与修复建议，critical 阻断。"
category: "biography"
---

# /check-biography-consistency

## Purpose

对传记项目运行 5 条 consistency-rules 检查，守 fact-narrative-separation + subject-ethics-boundary 两条 critical，产出违规清单。critical 阻断进度，high 出具修复计划。

## Inputs

- 本 Pack `consistency-rules.yaml`。
- fact-narrative-map / source-conflict-log / outline word_budget / design-life-arc / dialogue_log。
- 共享 `/fix-cascade`（critical backtrack）。

## Outputs

- 违规清单（rule_id × severity × 位置 × 修复建议）。
- critical 违规阻断标记（exit_blocked）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载 `consistency-rules.yaml`。
2. 逐条检查：
   - fact-narrative-separation（critical）：fact-narrative-map 覆盖率 + narrative_type 非空
   - subject-ethics-boundary（critical）：requires_approval 项均有 decision event
   - immutable-trait-fidelity（high）：design-life-arc 越界项有标注
   - source-conflict-preservation（high）：source-conflict-log 无 silently-adopted
   - life-stage-weighting（medium）：outline word_budget turning > 童年晚年
3. critical 违规 → 阻断（exit_blocked），走 `/fix-cascade` backtrack。
4. high 违规 → 出具书面修复计划。
5. medium 违规 → 记录在案，可继续。
6. 记录决策。

## Quality Gates

- 5 条规则全检查。
- critical 违规必阻断，不得静默放行。
- high 违规有书面修复计划。
- 违规清单可追溯到 rule_id + 位置。

## Error Handling

- 若 fact-narrative-map 缺失：报错指向 `/separate-fact-narrative`。
- 若 critical 涉及 constitution 改动：强制人审 + decision event。
- 若检查依赖的产物缺失：标 target_missing，不编造。

## 关联

- 规则：`consistency-rules.yaml`
- 下游：`/fix-cascade`（backtrack）、`/typeset-pdf`·`/export-docx`（exit gate）
