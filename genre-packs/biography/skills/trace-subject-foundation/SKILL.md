---
name: "trace-subject-foundation"
description: "传记传主本质溯源。调用 /trace-character-foundation 为传主建立溯源，但所有结论基于真实资料（subject-archive）并标 confidence；产出受事实约束的可变/不可变边界。消费共享能力 + 传记事实核查。"
category: "biography"
---

# /trace-subject-foundation

## Purpose

为传主建立本质溯源，但与虚构不同——所有溯源结论必须基于 subject-archive 真实资料，标 confidence（observed/inferred/speculated）。产出受事实约束的可变/不可变边界，供 `/design-life-arc` 使用。

## Inputs

- `subject-archive`（subject-curator 产出）。
- `constitution/brief.yaml`（传主核心论点、读者承诺）。
- 共享 skill `/trace-character-foundation`。
- 本 Pack `memory-schema.yaml`、`consistency-rules.yaml`。

## Outputs

- 传主溯源档案（成长环境/关键经历/优缺点同源/可变不可变），每条标 confidence + fact_basis。
- 真实人名记录（交 `/name-character` 退化处理）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 biography。
2. 从 subject-archive 提取传主真实资料（访谈/档案/第三方回忆）。
3. 调 `/trace-character-foundation` 框架，但每个溯源结论必须挂 fact_basis（subject-archive item_id）+ confidence。
4. confidence=speculated 的结论不得作为传主核心论点的高置信依据（对接 [rules/topic-research.md](../../../../.claude/rules/topic-research.md)）。
5. 多源矛盾保留（写 source-conflict-log），不抹平。
6. 标注可变/不可变边界——真实人物的不可变区特质由资料支撑，不可为弧光改变。
7. 真实人名交 `/name-character` 记录真名 + 解释时代阶层烙印（不改名）。
8. 运行 fact-narrative-separation critical 检查；记录决策。

## Quality Gates

- 每条溯源结论有 fact_basis + confidence。
- 多源矛盾保留（conflict_status 非 none 的进 source-conflict-log）。
- speculated 结论不进核心论点高置信。
- 真实人名未改名。

## Error Handling

- 若 subject-archive 为空：报错指向 subject-curator / `/active-research`，不凭空编传主生平。
- 若资料矛盾无法判定：保留为 conflicting，标 open，不强行采信。
- 若溯源需虚构填补空白：标 narrative_reconstruction 并人审。

## 关联

- 共享：`/trace-character-foundation`
- 下游：`/design-life-arc`
- 规则：fact-narrative-separation（critical）
