---
name: "query-project-state"
description: "按查询意图最小化加载并只读呈现项目状态 — 触发场景：作者想快速查某个角色当前状态/弧光、某条伏笔的回收进度、核心概念体系、写作进度或当前阶段、某章版本链（V0-V3）、主题研究内容、或类型记忆（世界观/关系/知识图）时。不负责质量评判（爽点/节奏/文笔归 multi-dim-feedback/reader-panel）、不负责写前上下文组装（归 inject-context）、不修改任何文件、不替一致性引擎裁判、不跨项目。"
category: "operations"
agents:
  - Memory Curator
  - Research Agent
  - Production Director
inputs:
  - "projects/<project-id>/PROJECT.md + genre-context/active-pack.yaml（确认活动项目）"
  - "registry/*.yaml（按意图裁剪：concepts / promises / foreshadowing）"
  - "constitution/concept_tree.json（概念体系查询）"
  - "outline/outline.yaml + extended-outline/（进度 / 节奏 / 依赖查询）"
  - "drafts/chapters/<ch_id>/（版本链 V0-V3 查询）"
  - "drafts/chapters/<ch_id>/summary.md（长程查询：character_state_at_N 时聚合最近 N 章摘要，见 chapter-summary-spec）"
  - "research/（主题知识查询，region-read source-note）"
  - "genre-context/genre-memory/（类型记忆查询：世界观 / 关系 / 知识图）"
  - ".history/events.jsonl + review/（一致性遗留查询）"
  - ".claude/docs/context-management.md（4 层真源优先级 + region-read 协议）"
outputs:
  - "按意图裁剪的状态视图（默认直接呈现，不落盘）"
  - "可选：projects/<project-id>/review/query-snapshot.md（作者明确要求留档时）"
required_reviews:
  - internal: never
  - client: never
duration_estimate: "3-10 分钟"
---

# /query-project-state

## Overview

`/query-project-state` 是 BookForge Studios 的**意图感知只读状态查询** skill。作者给出一个查询意图（查角色 / 伏笔 / 概念 / 进度 / 版本链 / 研究 / 类型记忆 / 一致性遗留），它把意图映射到**最小真源集**，按 Region-Read Protocol 窄读，按意图组织呈现，每条数据标注来自哪份真源。

它是**查询入口**，不是评判器也不是写前组装器：不做质量评判、不组装起草上下文、不修改任何文件、不替一致性引擎裁判、默认不落盘。定位对标"出版项目的按需问诊台"——和 `/project-doctor`（飞行体检）成对：doctor 在作者不知查啥时给全景体检，query 在作者有明确意图时给窄而深的状态切片。

## 能力要求

### 必须能做的

1. **意图解析**：把作者的查询归入标准意图类别（见 Step 1 的意图表），模糊时与作者澄清而非猜测。
2. **意图→最窄真源映射**：每个意图映射到最小真源集，遵循真源优先级链（`registry/` 真源 > `drafts/` 派生 > 派生产物），一次查询不同时加载两个以上 reference。
3. **Region-Read 窄读**：先 Grep `^#{1,3} ` 标题锚点定位，再 Read offset/limit 取段，不全文 cat（继承 `.claude/docs/context-management.md` 的 Region-Read Protocol）。
4. **来源标注**：每条呈现的数据标注来源真源；当 registry 真源与 drafts 派生冲突时，呈现真源并标注差异，不抹平。
5. **按意图呈现**：按查询意图组织呈现，只呈现状态，文案经 author-glossary 降级工程术语。
6. **遗留引导（不评判）**：若查到未解决 critical/high 或缺登记，提示引导下游 skill，但不评判、不执行。

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| 质量评判（爽点 / 节奏 / 文笔 / 论点力度） | `multi-dim-feedback` / `spawn-reader-panel` |
| 写前上下文组装（为起草服务） | `inject-context` |
| 阶段判定 + 健康体检 + 自愈导航（全景） | `project-doctor` |
| critical 阻断裁判 | consistency-engine（hook + `consistency-rules.yaml`） |
| 修改任何项目文件 | query 纯只读；落盘仅限作者要求的 `review/query-snapshot.md` |
| 概念 / 模式登记写入 | `extract-concepts` / `harvest-writing-pattern` |

## 必备上下文

按 Region-Read Protocol 加载——先 Grep 标题锚点定位，再 Read offset/limit 取段：

- `projects/<project-id>/PROJECT.md` + `genre-context/active-pack.yaml`（确认活动项目与当前类型包）
- `.claude/docs/context-management.md`（4 层真源优先级链 + Region-Read Protocol，本 skill 的执行依据）
- `shared-tooling/editorial-collaboration/author-glossary.json`（呈现术语降级映射）
- 按查询意图裁剪加载的真源（见 Step 2 映射表）

## Steps

### Step 1: 确认活动项目 + 解析查询意图

- 读 `PROJECT.md` 与 `active-pack.yaml`。
  - 若无活动项目 → 标 `needs_user`（`project.not_configured`，文案取自 error-catalog），停下。
  - 若类型不一致 → 标 `needs_user`（`genre.pack_mismatch`），停下请作者确认。
- 解析作者查询意图，归入标准类别（模糊时与作者澄清，不猜测）：

| 意图 | 典型问法 |
|------|---------|
| `character` | "X 角色现在状态？弧光进展？" |
| `foreshadowing` | "这条伏笔回收了吗？还差多远？" |
| `concept` | "核心概念体系是什么？" |
| `pacing` | "节奏 / 三线平衡怎样？" |
| `progress` | "整体进度？现在第几阶段？" |
| `version-chain` | "第 N 章版本链？" |
| `research` | "主题调研有哪些证据？" |
| `genre-memory` | "世界观 / 关系 / 知识图？" |
| `consistency-residue` | "还有哪些未解决的一致性问题？" |

### Step 2: 意图→最窄真源映射

- 每个意图映射到最小真源集（真源优先级：`registry/` > `drafts/` > 派生）：

| 意图 | 最窄真源集 |
|------|-----------|
| `character` | `registry/concepts.yaml`（角色项）+ `genre-memory`（关系 / 情绪状态，按类型包） |
| `foreshadowing` | `registry/foreshadowing.yaml`（埋设 / 目标回收 / 紧急度） |
| `concept` | `registry/concepts.yaml` + `constitution/concept_tree.json` |
| `pacing` | `outline/outline.yaml`（word_budget / strand 配比）+ 已写章统计 |
| `progress` | `PROJECT.md` + 各阶段关键产物存在性（S1-S6） |
| `version-chain` | `drafts/chapters/<ch_id>/`（v0~v3 独立快照，遵循 chapter-draft 规则） |
| `research` | `research/`（按 source-note 的 url_or_citation / confidence，region-read） |
| `genre-memory` | `genre-context/genre-memory/`（按活动类型包的 schema） |
| `consistency-residue` | `.history/events.jsonl`（最近未解决事件）+ `review/` |
| `character_state_at_N`（长程查询） | `registry/concepts.yaml`（基础设定）+ 最近 N 章 `summary.md` 的 `character_state_changes`（状态变迁链）——对标 webnovel `query-entity-state --at-chapter N` |
| `open_loops`（长程查询） | `registry/foreshadowing.yaml` + `promises.yaml` 的 `current_status`（open/near_due/overdue/closed）——对标 webnovel `memory-contract get-open-loops` |

- 走 Region-Read：Grep `^#{1,3} ` 定位锚点 → Read offset/limit 取段，**不全文 cat**。

### Step 3: 最窄读取 + 来源标注

- 仅读 Step 2 映射的最小真源集；一次查询**不同时加载两个以上 reference**（最小化）。
- 每条数据标注来源真源（`registry/concepts.yaml` vs `drafts/` vs `genre-memory/`）。
- 真源优先级：冲突时以 `registry/` 真源为准并标注与 drafts 的差异，不抹平、不静默择一。

### Step 4: 按意图呈现（不评判）

- 按查询意图组织呈现，**只呈现状态，不做质量评判**（爽点 / 节奏 / 文笔归 `multi-dim-feedback` / `spawn-reader-panel`）。
- 文案经 author-glossary 降级工程术语（registry→"设定档案"、v3→"定稿"等）。
- 默认直接呈现，**不落盘**；作者明确要求留档时才写 `review/query-snapshot.md`，并标注查询意图 + 来源 + 时间。

### Step 5: 发现遗留时引导下游（不评判）

- 若查到未解决 critical/high 或缺登记 → 提示引导（可复制命令），但不评判、不执行：
  - 高 / 严重问题未修 → `/fix-cascade`
  - 读者争议未综合 → `/consensus-analysis`
  - 缺概念登记 → `/extract-concepts`
  - 缺可复用写作模式 → `/harvest-writing-pattern`

## 运营规则

- **纯只读**：不修改任何项目文件；落盘仅限作者明确要求的 `review/query-snapshot.md`。
- **最小化加载**：一次查询读取的文件数 ≤ 意图所需最小集；不同时加载两个以上 reference。
- **真源优先级**：`registry/` 真源 > `drafts/` 派生 > 派生产物；冲突时呈现真源并标注差异，不抹平。
- **来源标注**：呈现前每条数据必须标注来自哪份真源。
- **不评判**：只呈现状态；质量评判归 reader-panel / multi-dim-feedback。
- **不替 inject-context**：写前上下文组装归 inject-context；本 skill 只负责按需查询呈现。
- **不替裁判**：consistency 残留只汇总呈现，阻断判定归 consistency-engine。
- **不跨项目**：只查 `BOOKFORGE_PROJECT` 指定的活动项目（一个 session 一本书）。
- **Region-Read**：先 Grep 锚点定位 → Read offset/limit 取段，不全文 cat 长参考文件。

### 反模式（严禁）

- 不裁剪意图就全文加载 `registry/` 或 `research/`（违反最小化）。
- 呈现状态时夹带质量评判（爽点弱 / 节奏差 / 论点不力）。
- 混淆真源与派生：拿 `drafts/` 当 `registry/` 真源呈现，或在冲突时静默择一。
- 替 `inject-context` 组装写前上下文包。
- 默认就落盘（除非作者明确要求留档）。
- 跳过 Region-Read Protocol，全文 cat 长文件。
- 呈现直接甩工程术语而不经 author-glossary 降级。
- 跨项目查询或读取非活动项目产物。

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| 读取文件数 ≤ 意图所需最小集（不同时 ≥2 reference） | 收窄读取范围，回 Step 2 重映射 |
| 呈现前每条数据是否标注来源真源 | 补来源标注 |
| 是否纯只读（默认不落盘；仅 query-snapshot 可选且需作者要求） | 移除写操作 |
| 是否夹带质量评判（爽点 / 节奏 / 文笔语句） | 移除评判语句 |
| 是否走 Region-Read（Grep 锚点 → Read 段）而非全文 cat | 改用 region-read |
| 意图→真源映射是否走真源优先级链（registry > drafts > 派生） | 回 Step 2 重映射 |
| 真源冲突是否呈现并标注差异（而非抹平） | 补差异标注 |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `/inject-context` | query 按需查状态供作者参考；inject-context 为写前组装服务，两者不互替 |
| `/project-doctor` | doctor 在作者不知查啥时给全景体检 + 落盘报告；query 在作者有明确意图时给窄查（默认不落盘）。两者都是 operations 只读，互不重叠 |
| `/multi-dim-feedback` / `/spawn-reader-panel` | 它们做质量评判；query 只呈现状态不评判 |
| `/extract-concepts` / `/harvest-writing-pattern` | query 发现缺登记时引导它们补登记（下游） |
| `/fix-cascade` / `/consensus-analysis` | query 发现未解决遗留时引导它们（下游） |
| consistency-engine（hook + `consistency-rules.yaml`） | query 只汇总呈现一致性残留，不替代裁判 |

## 文件输出

- 默认：直接呈现，**不落盘**。
- 可选（作者明确要求留档时）：`projects/<project-id>/review/query-snapshot.md`，含查询意图 + 来源标注 + 呈现内容 + 时间。
