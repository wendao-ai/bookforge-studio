# Writing Brief Spec

写作任务书（Writing Brief）是 `/inject-context` 为单章起草注入的结构化上下文包，被 `draft-v0-skeleton` → `draft-v1-rough` → `draft-v2-refine` → `draft-v3-polish` 逐版消费。它把散落在 `constitution/` / `registry/` / `genre-memory/` / `outline/` / `style-corpus/` / `research/` 的状态收敛成一份 drafting agent 可直接执行的五段式简报，避免起草时反复翻找或凭记忆写作。

本 spec 是 drafting 阶段的通用输出契约（所有 genre 共享底座）。题材差异（scifi 的世界法则、romance 的关系状态、textbook 的前置知识等）由活动 genre pack 的 memory schema 与 quality-metrics 注入到对应段。

## 五段式结构

每份写作任务书含五段，缺一不可：

### 1. 开篇委托（Commission）

- 本章位置（章号 / 卷 / arc 位置）与核心任务（一句话）。
- 字数预算（来自 `outline/outline.yaml` 的 `word_budget`）。
- 所属 strand 或题材等价定位（fiction: Quest/Fire/Constellation；非虚构:论点推进 / 案例 / 反方处理）。
- 版本子目标（V0 骨架 / V1 初稿 / V2 修订 / V3 润色 分别要做到什么）。

### 2. 故事（Story）

- 场景因果链：本章发生什么、场景间如何衔接（消费 `extended-outline/` 章节计划 beats）。
- 与上一章的接续点 + 给下一章的钩子承诺。
- 关键事件 / 揭示 / 转折（按题材：scifi 的 revelation、romance 的 beat、textbook 的 concept 引入）。

### 3. 人物（Characters）

- 出场人物当前状态（消费 `registry/concepts.yaml` 角色项 + `genre-context/genre-memory/` 关系/情绪/能力状态）。
- 本章弧光推进约束（消费 `character-arc.yaml` / 故事弧线）。
- 行为动机边界：不得违背已建立的人设、伤口、关系状态（对接各 pack 的 genre-memory 状态机）。

### 4. 怎么写（Craft）

- 风格锚点（消费 `style-corpus/style-anchor.yaml`：voice / sentence_length / terminology_density / chapter_title_paradigm）。
- 视角、人称、时态。
- 禁漂清单（`forbidden_drift`）。
- 追读力要求（按题材 pack 的 `quality-metrics.yaml`：钩子类型与强度、微兑现每章下限、strand 配比）；非虚构题材对应"论证密度 / 案例配比 / 概念引入节奏"。

### 5. 收在哪（Landing）

- 章末落点：兑现了什么承诺（`registry/promises.yaml`）、埋了什么伏笔（`registry/foreshadowing.yaml` + 紧急度）。
- 章末钩子强度要求（按章节类型：strong/medium/weak）。
- 本章产生的 registry 待更新项（新概念 / 新承诺 / 新伏笔 / 状态变迁）——交回 registry，不留在正文记忆。

## 数据权重链

当多源信息冲突时，写作任务书按以下优先级取真源（高 → 低）：

1. `constitution/`（宪法：核心承诺、论点、读者契约、边界）——最高，不可被下源覆盖。
2. `registry/`（已登记的概念 / 承诺 / 伏笔 / 命名）。
3. `genre-context/genre-memory/`（类型记忆：世界法则 / 关系状态 / 知识图）。
4. `outline/` + `extended-outline/`（结构承诺与章节计划）。
5. `drafts/` 前序章节（已发生事实，仅作衔接参考，不作设定真源）。
6. `research/`（调研论据，支持非虚构论点 / 历史史料 / 教材知识，不作叙事真源）。

冲突不抹平：在"故事"或"人物"段标注冲突与所取真源，交回作者裁决（人审），记录进 `dialogue_log.jsonl`。

## 术语不外泄

写作任务书内部使用 Bookie 工程术语（registry / strand / coolpoint / micro-payoff / foreshadowing urgency 等）供 drafting agent 消费，但：

- **正文禁用词**：最终章节正文（`v3_polished.md`）不得出现这些工程术语，也不得把系统结构（如"本章属于 Quest strand 占比 60%"）写成元叙事。
- **作者可见文案降级**：任务书面向作者的摘要段（交接说明）须经 `shared-tooling/editorial-collaboration/author-glossary.json` 降级（registry→"设定档案"、v3→"定稿"、fix-cascade→"修订级联"）。
- **权重链不外泄**：不在正文解释"为何取 registry 而非 drafts"，只呈现结果。

## 与阶段对齐

| 阶段 | 角色 |
|---|---|
| `/inject-context`（S4 入口） | 产出五段式写作任务书，落 `drafts/chapters/<ch_id>/writing-brief.md` |
| `draft-v0` → `draft-v3` | 逐版消费任务书；版本升级不得违背"开篇委托"的字数与子目标 |
| registry 回写 | "收在哪"段的待更新项交回 registry（append-friendly） |
| `/fix-cascade`（S5） | 发现任务书与草稿冲突时，回溯修订任务书或上游 outline/constitution |

## Quality Gates（`/inject-context` 产出时自检）

- 五段齐全，无占位空段。
- 每段数据标注来源真源（对齐数据权重链）。
- 冲突已标注并交回作者，未静默择一。
- 正文禁用词清单附在任务书末尾供 `draft-v3` 自检。
- 字数预算与 `outline.yaml` 的 `word_budget` 一致，偏差 >20% 标结构风险。
