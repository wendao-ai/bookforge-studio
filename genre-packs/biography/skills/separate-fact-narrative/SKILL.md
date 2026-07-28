---
name: "separate-fact-narrative"
description: "传记事实-叙事分离。为每段正文建立 fact-narrative-map（fact_basis + narrative_type + confidence），守 fact-narrative-separation critical 规则。传记区别于虚构的核心护栏。"
category: "biography"
---

# /separate-fact-narrative

## Purpose

为传记正文建立事实-叙事分离映射，守 critical 规则：每段叙事可追溯到 subject-archive fact_basis；叙事重构显式标注。这是传记区别于虚构的核心护栏。

## Inputs

- `drafts/`（正文）。
- `subject-archive`。
- 本 Pack `memory-schema.yaml`、`consistency-rules.yaml`。

## Outputs

- `fact-narrative-map.yaml`（每段 passage_ref → fact_basis + narrative_type + confidence + reconstruction_reason）。
- 未标 fact_basis 的段落清单（critical 违规，阻断 V3）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 biography。
2. 遍历正文每段，挂 fact_basis（subject-archive item_id）。
3. 标 narrative_type：fact（严格据实）/ narrative_reconstruction（叙事重构）。
4. narrative_reconstruction 项必须填 reconstruction_reason（为何重构 + 依据）。
5. 未挂 fact_basis 的段落 → critical 违规，阻断进入 V3。
6. factual 软隔离：事实性 finding 不自动改正文，交 fact-checker + 专家（对接 `/fix-cascade`）。
7. 记录决策。

## Quality Gates

- 每段正文有 fact-narrative-map 条目。
- narrative_type 字段非空。
- narrative_reconstruction 项有 reconstruction_reason。
- 无未挂 fact_basis 的叙事段落（critical）。

## Error Handling

- 若段落无 fact_basis：标 critical 违规，阻断，提示补资料或改写。
- 若 narrative_reconstruction 缺理由：标违规，要求补 reconstruction_reason。
- 若 fact_basis 指向的 subject-archive 条目不存在：标 target_missing，不编造。

## 关联

- 规则：fact-narrative-separation（critical）
- 协同：fact-checker、`/fix-cascade`（factual 软隔离）
