---
name: "trace-character-foundation"
description: "人物与群体本质溯源。在宪法/扩展大纲阶段，为主要人物与群体建立存在根基→历史→衍生三层溯源 + 优缺点同源 + 可变/不可变边界 + 社会立场分析，作为人物弧光的地基。消费 cross-genre/001-character-foundation-tracing。"
category: "drafting"
---

# /trace-character-foundation

## Purpose

为活动项目的主要人物与群体建立**本质溯源**，回答"这个人物/群体为什么是这个样子"。产出是人物弧光（`/design-character-arc`）和正文草稿的地基——没有溯源，人物会前后不一致、被剧情推着走、性格无根源。

本 skill 是跨 genre 通用能力：fiction-general / romance / scifi / biography 共享。方法论见 [capability-library/cross-genre/001-character-foundation-tracing.md](../../../capability-library/cross-genre/001-character-foundation-tracing.md)。

## Inputs

- 活动项目 id 与 `projects/<id>/PROJECT.md`、`genre-context/active-pack.yaml`。
- `constitution/brief.yaml`（核心人物矛盾、读者承诺）。
- `registry/concepts.yaml`（已登记人物/概念）。
- 活动 Genre Pack 的 `memory-schema.yaml` 与 `consistency-rules.yaml`（人物相关规则）。
- 方法论资产 [001-character-foundation-tracing.md](../../../capability-library/cross-genre/001-character-foundation-tracing.md)。

## Outputs

- `projects/<id>/genre-context/character-foundations/`（或 pack 指定路径）下每个主要人物的溯源档案：
  - 群体三层（根基/历史/衍生 + 优缺点同源）
  - 人物五项（成长环境/关键经历/根基烙印/优缺点同源/可变不可变）
  - 群体位置 + 社会立场分析
- 7 项自洽校验记录。
- 关键人物同步登记到 `registry/concepts.yaml`（含 aliases）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载活动项目与 active pack，确认 stage 允许人物地基工作（constitution 之后、或 extended-outline）。
2. 从 `brief.yaml` 与已批准大纲识别主要人物与关键群体。
3. 按 [001-character-foundation-tracing.md](../../../capability-library/cross-genre/001-character-foundation-tracing.md) 模块 A 完成群体三层溯源；模块 B 完成每个主要人物五项溯源；模块 C/D 完成群体位置与社会立场。
4. **具体化要求**：每条溯源禁写空泛词（"出身普通""面临压力"），必须落到具体物件/动作/数字/场景（资产里有改写示范）。
5. 运行 7 项自洽校验；不通过的项标注并修正（修正人物或修正群体设定）。
6. 标注可变/不可变边界——这直接约束后续 `/design-character-arc` 的变化落点。
7. 人物姓名交由 `/name-character` 处理（本 skill 不负责命名，只负责本质）。
8. 将溯源写入项目文件并同步 `registry/concepts.yaml`；记录决策与未决问题。

## Quality Gates

- 每个主要人物必须有成长环境 + 关键经历 + 优缺点同源 + 可变/不可变四项（模块 B 最小集）。
- 优缺点必须同源（共同根源非空）；不满足则打回重设。
- 弧光计划的变化若落在不可变区，本 skill 必须在交接时标注 risk。
- 溯源是地基文档，不是正文——禁止把溯源内容当设定说明书写入草稿。
- 关键创作决策（人物核心创伤、立场选择）须人审并记 `dialogue_log.jsonl`。

## Error Handling

- 若 active pack 是 textbook 等非叙事类型：提示本 skill 主要服务虚构/传记/叙事非虚构，确认是否继续。
- 若 `brief.yaml` 缺核心人物矛盾：报错指向 `/finalize-constitution`，不凭空编人物。
- 若人物与已批准大纲矛盾：标 conflict，提请作者确认改人物还是改大纲（不改大纲则记 backtrack）。
- 若溯源与现有草稿已写人物反应矛盾：要么修溯源（说明人物在成长）、要么修草稿，二选一并记 reason。

## 关联

- 方法论：[001-character-foundation-tracing.md](../../../capability-library/cross-genre/001-character-foundation-tracing.md)
- 下游：`/design-character-arc`（消费本 skill 的可变/不可变边界）
- 命名：`/name-character`（消费本 skill 的人物时代/地域/阶层）
- 规则：[rules/registry.md](../../rules/registry.md)、活动 pack 的 consistency-rules
