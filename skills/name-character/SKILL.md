---
name: "name-character"
description: "角色命名。基于时代/地域/阶层/姓氏/命运暗示/音韵六维度为角色命名，生成候选清单并跨作品去重。消费 cross-genre/001-character-naming-six-dimensions，去重写入 registry/concepts.yaml。"
category: "drafting"
---

# /name-character

## Purpose

为角色精心命名，使名字承载时代/地域/阶层信息、隐性命运暗示、且跨作品不重复。命名发生在人物本质溯源（`/trace-character-foundation`）之后、人物弧光（`/design-character-arc`）之前。

跨 genre 通用：fiction-general / romance / scifi / biography 共享（传记真实人名时退化为"记录+解释烙印"）。方法论见 [capability-library/cross-genre/001-character-naming-six-dimensions.md](../../../capability-library/cross-genre/001-character-naming-six-dimensions.md)。

## Inputs

- `/trace-character-foundation` 产出的人物溯源（时代/地域/阶层/家庭背景）。
- `registry/concepts.yaml`（已登记角色名，用于去重）。
- 跨项目已用名字（`capability-library` 沉淀的命名记录，若有）。
- 方法论资产 [001-character-naming-six-dimensions.md](../../../capability-library/cross-genre/001-character-naming-six-dimensions.md)。

## Outputs

- 每个主要角色的候选名字清单（5-10 个，附六维评估）+ 最终选定名 + 命名理由。
- 同步登记到 `registry/concepts.yaml`（name / aliases / 命名理由）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 加载活动项目、人物溯源档案、`registry/concepts.yaml`。
2. 对每个待命名角色，按 [001-character-naming-six-dimensions.md](../../../capability-library/cross-genre/001-character-naming-six-dimensions.md) 工作流前四步：定时代地域 → 定阶层 → 定父母取名逻辑 → 生成 5-10 候选。
3. 每个候选附六维评估（时代合理性/阶层匹配/声调搭配/简称自然度/隐含信息）。
4. **去重检查**：候选与 `registry/concepts.yaml` 及跨项目记录比对，命中硬约束（同名同姓）则淘汰，回到第 3 步。
5. 命运暗示最多 1-2 个角色有，其余名字须"正常"。
6. 选定最终名，记录命名理由（时代/阶层/父母逻辑/暗示）。
7. 写入 `registry/concepts.yaml`；记录决策。

## Quality Gates

- 每个主要角色有命名理由（六维至少覆盖时代+阶层+父母逻辑三项）。
- 跨作品零硬约束冲突（无同名同姓）。
- 网文风复姓+古风名禁用（除非讽刺并标注）。
- 命运暗示不超过 2 个角色，且不干扰正常阅读。
- 名字在全文读起来顺口（音韵自检）。

## Error Handling

- 若无人物溯源：报错指向 `/trace-character-foundation`——无时代/地域/阶层信息的命名会失真。
- 若是传记/真实人物：不改名，改为记录真名 + 用六维解释其时代阶层烙印，标注 `real_name: true`。
- 若候选全部与已有重名：扩大地域/阶层搜索，或提请作者放宽约束并记 decision。
- 若非中文语境：提示本资产六维表针对中文取名，需另建外文命名维度。

## 关联

- 方法论：[001-character-naming-six-dimensions.md](../../../capability-library/cross-genre/001-character-naming-six-dimensions.md)
- 上游：`/trace-character-foundation`（提供时代/地域/阶层）
- 去重：`registry/concepts.yaml`（[rules/registry.md](../../rules/registry.md)）
