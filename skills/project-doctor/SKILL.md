---
name: "project-doctor"
description: "活动项目阶段感知体检与自愈导航 — 触发场景：作者想确认项目当前是否健康、能否进入下一阶段、卡在哪里该跑哪个 skill、或长时间未触碰该项目想快速恢复上下文时。不负责内容质量评判（由 multi-dim-feedback/reader-panel 负责）、不负责修复执行（由 fix-cascade 负责）、不替代一致性引擎的 critical 阻断裁判、不替人审。"
category: "operations"
agents:
  - Production Director
  - Memory Curator
  - Lead Review
inputs:
  - "projects/<project-id>/PROJECT.md"
  - "projects/<project-id>/genre-context/active-pack.yaml"
  - ".claude/docs/pipeline-stage-spec.md"
  - ".claude/docs/consistency-engine-spec.md"
  - "shared-tooling/editorial-collaboration/error-catalog.json"
  - "shared-tooling/editorial-collaboration/author-glossary.json"
  - "活动项目各阶段产物（constitution/ outline/ extended-outline/ drafts/ registry/ review/ typeset/）"
  - "active-pack 的 consistency-rules.yaml 与 quality-metrics.yaml（genre-specific 体检参照）"
outputs:
  - "projects/<project-id>/review/doctor-report.md"
required_reviews:
  - internal: ["Lead Review"]
  - client: never
duration_estimate: "10-20 分钟"
---

# /project-doctor

## Overview

`/project-doctor` 是 BookForge Studios 的**只读项目健康体检与自愈导航** skill。它解析活动项目当前处于六阶段流水线（S1 构思 → S2 大纲 → S3 扩展大纲 → S4 起草 → S5 审校 → S6 排版）的哪一步，按该阶段的 exit gate 检查应有产物是否齐全、一致、可进入下一阶段，输出一份带 `impact`（不修会怎样）+ `repair`（怎么修）的体检报告，并导航到下一步该跑的 skill。

它是**入口诊断器**，不是裁判也不是修复工：不做内容质量评判、不修改任何项目文件、不替代一致性引擎的 critical 阻断、不替人审。定位对标"出版项目的飞行体检"，让作者一眼看到"现在健康吗、卡在哪、下一步干什么"。

## 能力要求

### 必须能做的

1. **阶段判定**：基于 `pipeline-stage-spec.md` 的 S1-S6 exit gate，判定活动项目当前阶段（含子阶段，如 S4 drafting 的 V0/V1/V2/V3）。
2. **阶段产物体检**：按当前阶段的 exit gate 检查应有产物是否存在、是否合规（引用对应 rule 的 Mandatory Standards）、是否满足进入下一阶段的条件。**只检查当前阶段应有的**，不超前检查下一阶段（阶段感知，避免噪音）。
3. **一致性遗留汇总**：消费 `.history/events.jsonl` 与 `review/` 产物，汇总未解决的 critical/high 问题，每项带 `impact` + `repair`，并区分事实层（blockable）与感性层（advisory）问题。
4. **自愈导航**：基于阶段判定 + 体检结果，给出可执行的下一步 skill 推荐（缺宪法 → `/finalize-constitution`；缺大纲 → `/synthesize-outline`；有 high 未修 → `/fix-cascade`；V3 就绪 → `/typeset-pdf` 等）。
5. **四态总状态**：报告以 `completed` / `partial` / `needs_user` / `failed` 四态收尾，附 `blocking_count`，文案经 author-glossary 降级。

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| 内容质量评判（爽点/节奏/文笔/论点力度） | `multi-dim-feedback` / `spawn-reader-panel` |
| 修复执行（修订/搁置/驳回） | `fix-cascade` |
| critical 阻断裁判 | consistency-engine（hook + `consistency-rules.yaml`） |
| 关键创作决策（世界观/史观/核心论点/读者承诺/结局） | 人审（作者拍板，记录进 `dialogue_log.jsonl`） |
| 跨项目能力库审计 | `capability-audit` |
| 修改任何项目文件 | doctor 纯只读，只写自己的报告 `review/doctor-report.md` |

## 必备上下文

按 Region-Read Protocol（`.claude/docs/context-management.md`）加载——先 Grep 标题锚点定位，再 Read offset/limit 取段，不全文 cat：

- `projects/<project-id>/PROJECT.md` + `genre-context/active-pack.yaml`（确认活动项目与当前类型包）
- `.claude/docs/pipeline-stage-spec.md`（S1-S6 的 inputs/outputs/exit gate，阶段判定唯一依据）
- `.claude/docs/consistency-engine-spec.md`（severity 四级 + 事实层/感性层分层）
- `shared-tooling/editorial-collaboration/error-catalog.json`（错误场景 → 友好文案 + impact/next_action）
- `shared-tooling/editorial-collaboration/author-glossary.json`（报告术语降级映射）
- genre-specific 体检标准（按需，region-read）：active-pack 的 `consistency-rules.yaml` + `quality-metrics.yaml`

## Steps

### Step 1: 确认活动项目与类型包

- 读 `PROJECT.md` 与 `active-pack.yaml`。
- 若类型不一致 → 标 `needs_user`（`genre.pack_mismatch`，文案取自 error-catalog），停下请作者确认以哪份为准，确认前不继续。
- 若无活动项目 → 标 `needs_user`（`project.not_configured`）。

### Step 2: 阶段判定

- 按 `pipeline-stage-spec.md` 的 exit gate 顺序，逐阶段检查关键产物存在性，判定当前阶段：
  - **S1 构思**：`constitution/`（brief.yaml + concept_tree.json + dialogue_log.jsonl）+ 人审批准记录
  - **S2 大纲**：`outline/outline.yaml` + `registry/promises.yaml`
  - **S3 扩展大纲**：`extended-outline/` 章节计划（含 purpose/inputs/outputs/dependencies/review gates）
  - **S4 起草**：`drafts/chapters/<ch_id>/v0~v3`（判定到具体版本子阶段）
  - **S5 审校**：`review/reader_reports/` + `controversy_map.yaml` + fix-cascade plan
  - **S6 排版**：`typeset/` 产物

### Step 3: 当前阶段产物体检

- 对当前阶段的 exit gate 逐项检查（引用对应 rule 的 Mandatory Standards，如 `constitution.md` / `outline.md` / `chapter-draft.md` / `registry.md`）。
- 每个体检项输出：`id` / `status`(ok/warn/block) / `severity` / `impact` / `repair` / `artifact`。
- **只检查当前阶段应有的**；不把刚 init 的项目按已写多章检查。

### Step 4: 一致性遗留汇总

- 读 `.history/events.jsonl` 最近事件 + `review/` 产物。
- 汇总未解决的 critical/high，每项带 `impact` + `repair`（文案取自 error-catalog），并按事实层（可阻断）vs 感性层（建议）分类呈现。

### Step 5: 自愈导航

- 基于阶段判定 + 体检 + 遗留，给出下一步 skill 推荐（可复制命令）：
  - S1 缺人审批准 → 引导人审，记录进 `dialogue_log.jsonl`
  - S2 缺大纲 → `/synthesize-outline`
  - S3 章节计划缺依赖 → `/build-dependency-graph`
  - S4 V3 就绪且无 high → `/spawn-reader-panel` 或直接 `/typeset-pdf`
  - 有 high/critical 未修 → `/fix-cascade`

### Step 6: 生成四态报告

- 写 `review/doctor-report.md`，含：阶段判定 / 体检项表（带 impact/repair）/ 遗留汇总 / 下一步导航 / 四态总状态 + `blocking_count`。
- 总状态规则：
  - `completed`：当前阶段 exit gate 全过，可进入下一步
  - `partial`：可推进但有 warn（中等问题/可选修复）
  - `needs_user`：有 critical/blocking 或关键决策待裁决
  - `failed`：关键阶段产物缺失，无法可靠判定
- 报告文案用 author-glossary 把工程术语降级为作者语言。

## 运营规则

- **纯只读**：不修改任何项目文件，只写自身的 `review/doctor-report.md`。
- **阶段感知**：只检查当前阶段应有的产物，不超前检查下一阶段，不制造噪音。
- **不替裁判**：doctor 标"需处理"是建议；critical 的阻断判定归 consistency-engine（hook + rules）。
- **不替人审**：发现关键决策未确认时引导人审，不代决。
- **不跨项目**：只体检 `BOOKFORGE_PROJECT` 指定的活动项目（一个 session 一本书）。
- **消费而非重造**：每个体检项必须可追溯到某条 rule 或 pipeline-stage 的 exit gate，不发明新标准。
- **术语降级**：面向作者的报告统一经 author-glossary 翻译工程术语。

### 反模式（严禁）

- 自动修复发现的问题（doctor 只诊断，修复归 `/fix-cascade`）。
- 直接修改 `constitution/` / `outline/` / `registry/` / `drafts/` 等项目文件。
- 超前检查下一阶段产物，把刚 init 的项目按已写多章检查。
- 把 doctor 的"需处理"当成 consistency-engine 的 blocking（越权裁判）。
- 凭空发明体检标准（每项必须可追溯到 rule 或 exit gate）。
- 跳过 Region-Read Protocol，全文 cat 长参考文件。
- 报告直接甩出工程术语而不经 author-glossary 降级。

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| 每个体检项是否可追溯到某条 rule 或 pipeline-stage exit gate | 删除无溯源的体检项 |
| 报告是否含四态总状态 + `blocking_count` | 补充总状态聚合 |
| 是否纯只读（除 `review/doctor-report.md` 外无任何项目文件修改） | 移除写操作 |
| 每个非 ok 体检项是否含 `impact` + `repair` | 补充（可取自 error-catalog） |
| 阶段判定是否基于 `pipeline-stage-spec` exit gate 而非主观猜测 | 回 Step 2 重新判定 |
| 报告术语是否经 author-glossary 降级 | 替换工程术语 |
| 是否只检查当前阶段产物（不超前） | 移除超前体检项 |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| 所有产出 skill（finalize-constitution / synthesize-outline / expand-chapter-plan / draft-v0~v3 / multi-dim-feedback / typeset-*） | 其产物是 doctor 的体检对象（上游） |
| `/fix-cascade` | doctor 发现 high/critical 未修时，导航到 fix-cascade（下游） |
| `/multi-dim-feedback` / `/spawn-reader-panel` | 它们产出的 `review/` 报告被 doctor 汇总消费 |
| consistency-engine（hook + `consistency-rules.yaml`） | doctor 消费其裁判结果，不替代裁判 |
| `/capability-audit` | 互不重叠：doctor 查单项目状态，capability-audit 查跨项目能力库 |

## 文件输出

除非用户另有指定，使用以下默认位置：

- 体检报告：`projects/<project-id>/review/doctor-report.md`
