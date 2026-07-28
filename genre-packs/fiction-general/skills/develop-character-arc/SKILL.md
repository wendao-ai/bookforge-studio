---
name: "develop-character-arc"
description: "fiction-general 人物发展编排。依次调用 /trace-character-foundation（本质溯源）→ /name-character（命名）→ /design-character-arc（八要素弧光），产出符合 character-arc.yaml 模板的人物档案。消费共享能力层。"
category: "fiction-general"
---

# /develop-character-arc

## Purpose

fiction-general 专属人物发展编排器。把跨 genre 共享的三步人物能力串成 fiction-general 项目的工作流：先溯源（为什么是这个样子）→ 再命名（名字承载时代阶层）→ 再设计弧光（转变落在可变区）。

本 skill 不重复定义方法论，只做 fiction-general 语境下的编排与模板对齐。方法论见对应共享 skill 与 cross-genre 资产。

## Inputs

- 活动项目 id、`genre-context/active-pack.yaml`（确认 fiction-general）。
- `constitution/brief.yaml`（核心人物矛盾、读者承诺）。
- `registry/concepts.yaml`。
- 共享 skill 产出：`/trace-character-foundation`、`/name-character`、`/design-character-arc`。
- 本 Pack `templates/character-arc.yaml`、`consistency-rules.yaml`、`quality-metrics.yaml`。

## Outputs

- `projects/<id>/genre-context/genre-memory/character-arc/` 下每个主要人物的完整档案（符合 character-arc.yaml 字段）。
- 同步 `registry/concepts.yaml`。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general（primary 或 secondary）；否则路由 `/switch-genre`。
2. **溯源**：调 `/trace-character-foundation`，产出群体三层 + 人物五项 + 社会立场 + 可变/不可变边界。
3. **命名**：调 `/name-character`，基于溯源的时代/地域/阶层生成候选并去重，写入 `registry/concepts.yaml`。
4. **弧光**：调 `/design-character-arc`，设计八要素弧光，校验转变落在可变区。
5. 按 `templates/character-arc.yaml` 字段组装档案，落盘到 genre-memory。
6. 运行本 Pack `consistency-rules.yaml` 的人物相关检查（character_motivation_gap 等）。
7. 记录决策、confidence、未决问题；人审项（核心创伤、立场选择）记 `dialogue_log.jsonl`。

## Quality Gates

- 每个主要人物有溯源 + 命名理由 + 八要素弧光三件套。
- 优缺点同源、转变落可变区、转折有 ≥2 处铺垫。
- 档案符合 character-arc.yaml 字段约定。
- 关键创作决策人审。

## Error Handling

- 若 active genre 非 fiction-general：路由 `/switch-genre`。
- 若上游 brief 缺核心人物矛盾：报错指向 `/finalize-constitution`。
- 若弧光落在不可变区：标 risk 并人审（见 /design-character-arc Error Handling）。

## 关联

- 编排：`/trace-character-foundation` → `/name-character` → `/design-character-arc`
- 模板：`templates/character-arc.yaml`
- 资产：[001-character-foundation-tracing](../../../../capability-library/cross-genre/001-character-foundation-tracing.md)、[001-character-arc-eight-elements](../../../../capability-library/cross-genre/001-character-arc-eight-elements.md)、[001-character-naming-six-dimensions](../../../../capability-library/cross-genre/001-character-naming-six-dimensions.md)
