---
name: "deep-topic-research"
description: "深度主题调研——写书前用第一性原理 + 深度调研教义为主题建知识库，产出可追溯论据喂给宪法的 concept_tree / 核心论点。当作者要'调研下这个主题 / 把这个赛道摸透 / 为这本书打知识地基 / 这个论断站不站得住 / 有没有先例 / 这个原理是什么'时用本 skill。不负责正文生成（draft-v*）、风格学习（benchmark-corpus-research）、选题商业论证（editorial-acquisition）。"
category: "ideation"
agents:
  - lead-ideation
  - research-agent
inputs:
  - "projects/<project-id>/PROJECT.md"
  - "主题/赛道（socratic-dialogue 产出）"
  - "类型（detect-genre 产出）+ genre-context/active-pack.yaml"
  - "constitution/dialogue_log.jsonl（苏格拉底深挖记录）"
  - "作者提供的锚点一手资料（可选：调研报告/访谈/内部数据/已购正版书）"
outputs:
  - "projects/<project-id>/research/ 主题知识库（research-log + knowledge-requests + query-plans + sources + bundles）"
  - "回填 constitution/concept_tree.json（概念节点）"
  - "回填 constitution/brief.yaml（核心论点 / uniqueness_anchor 论据）"
  - "回填 registry/concepts.yaml（术语）"
required_reviews:
  - internal: ["lead-ideation"]
  - client: required
duration_estimate: "按主题复杂度 4h（轻）–3d（重）"
---

# Deep Topic Research

## Overview

写书前，为主题建一座**可追溯的知识地基**。

BookForge 的宪法（`brief.yaml` 的核心论点 / `uniqueness_anchor`、`concept_tree.json`）一旦建立在浅调研或凭空判断上，后续整本书都会被"专业框架包装的浅薄结论"拖累——这是比不写更危险的失败模式。本 skill 在苏格拉底深挖 + 类型识别之后、宪法文件之前，用三套方法论把主题拆深、查透、沉淀成可审计的论据库：

- **第一性原理**：追问本质/原理/终局，禁止现象层结论（"市场大" ≠ "值得写/值得投"）
- **深度调研教义**：100 倍知识储备，一手资料全文精读，搜索 ≠ 调研
- **知识源协议**：五类知识源 + 原理翻译四层 + 六子项评分 + 新鲜度阈值

与 [benchmark-corpus-research](../benchmark-corpus-research/SKILL.md) 互补：它调"已有书的风格怎么写"（形式），本 skill 调"这个主题到底是什么、原理是什么、有没有料"（内容）。两者都在 ideation 阶段，可并行，共同为宪法供料。

> 本 skill 平移自全局 `~/.claude/skills/deep-mastery-researcher`，但**只保留调研能力**——大全正文生成（5 编金字塔 / 10 要素 / 并行渲染）交还给 BookForge 的 `draft-v0~v3` + genre pack 的 `structure-paradigm`。

---

## ⛔ 不可违反原则（Non-Negotiable Principles）

### 原则 1：第一性原理优先

任何调研判断前，先做问题降维 + 原理拆解，禁止现象层结论。详见 `references/first-principles-method.md`。

### 原则 2：深度调研不可跳过

搜索 ≠ 调研；摘要 ≠ 全文；框架 ≠ 知识。关键论断必须有一手资料全文支撑。详见 `references/deep-research-doctrine.md`。

### 原则 3：来源可追溯 + 冲突保留

每个数字/论断必须有 `source-note` 可回溯；不同来源矛盾时标 `conflict_status`，**不得选择性引用**。

### 原则 4：诚实降级

调研不充分时，标 `knowledge_coverage: insufficient` 并拒绝产出高置信结论。宁可慢，不可假。

---

## 能力要求

### 必须能做的

1. **第一性原理降维**：把主题拆到原子约束 + 原理表述（学科+机制+指标），产出调研方向树。
2. **结构化调研请求**：为每个原理方向写 KnowledgeRequest（说明要解决什么原理问题、知识注入哪个论断）。
3. **原理翻译成 query**：每个原理 ≥ 6 条中英文 query（含同义词/上下位），带 `derived_from` 追溯。
4. **多源检索 + 全文深读**：五类知识源检索，关键论文/报告 WebFetch **全文**（非摘要），每篇落 source-note。
5. **六子项评分归档**：来源可信度/证据强度/相关性/新鲜度/可迁移性/可行动性加权评分，质量分 < 0.50 不进正文论据。
6. **喂给宪法**：把 KnowledgeBundle 的 strongest_findings / transfer_hypotheses / decision_impact 回填 `concept_tree.json` / `brief.yaml` / `registry/concepts.yaml`。

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| 正文生成 / 章节写作 / 分编结构 | `draft-v0-skeleton` / `draft-v1-rough` / `draft-v2-refine` / `draft-v3-polish` |
| 对标书的风格解构（句长/术语密度/排版） | `benchmark-corpus-research` |
| 选题商业论证 / 市场能否立项 / 竞品矩阵 | `editorial-acquisition` |
| 大纲设计 / 章节结构 | `synthesize-outline` / `expand-chapter-plan` |
| 宪法文件本身的撰写（本 skill 只供料） | `finalize-constitution` |

---

## 必备上下文

在产出任何内容之前，加载：

- `projects/<project-id>/PROJECT.md`（活动项目确认）
- `projects/<project-id>/genre-context/active-pack.yaml`（类型，影响调研侧重——如 history 需史料源、textbook 需教研源、scifi 需前沿论文）
- `.claude/docs/three-tier-confidence.md`（observed/inferred/speculated 三级标签，六子项评分须对接）
- `.claude/docs/context-management.md`（调研产物落盘规范）

仅加载所需参考文档：
- `references/first-principles-method.md`：**任何时候做调研判断前**（原则 1 操作手册）
- `references/deep-research-doctrine.md`：Step 1-5 调研执行（五步法 + 量化门槛 + 落盘红线）
- `references/knowledge-sources-protocol.md`：Step 3-5 检索评分（五类源 + 原理翻译四层 + 六子项评分 + 新鲜度）

---

## Steps

### Step 1：第一性原理降维（加载 first-principles-method.md）

- 输入：主题/赛道（socratic-dialogue 产出）+ 类型
- 动作：跑五段流程——问题降维（拆到原子约束）→ 普遍性评估 → 原理拆解（学科+机制+指标，D2 起步）→ 问题重构（≥2 候选）→ 上溯回流。产出"调研方向树"：每个方向对应一个核心原理 + 若干可验证指标。
- 输出：`research/knowledge-requests/` 下的方向索引（每个方向一个 KnowledgeRequest，见 Step 2）
- **gate**：每个方向有原理表述三段式（禁现象词），作者确认调研方向树后进入 Step 2

### Step 2：KnowledgeRequest（写结构化请求）

- 输入：Step 1 的调研方向树
- 动作：每个原理方向写一个 KnowledgeRequest，说明"要解决什么原理问题、为什么需要外部知识、知识将注入本书的哪个论断/章节"
- 输出：`research/knowledge-requests/<direction>.md`

### Step 3：QueryPlan（原理翻译四层 → 中英文 query）

- 输入：每个 KnowledgeRequest 的 primary_principle
- 动作：原理翻译四层（P0 原理名 → P1 机制词 → P2 指标词 → P3 场景词），为五类源各生成 3-8 条 query（含中英双语），每条带 `derived_from`
- 输出：`research/query-plans/<direction>.md`
- **质量门**：每个原理 ≥ 6 条 query（academic ≥2、cross-domain ≥2、realtime ≥1、trends ≥1），含 ≥1 原理词 + ≥1 机制/指标词

### Step 4：多源检索（五类知识源）

- 输入：QueryPlan
- 动作：按优先级 ①⑤>③>②>④ 检索（academic + cross-domain + trends + realtime + anchor）。**每条 query 立即记入 research-log**，不"等最后汇总"
- 输出：`research/research-log.md`（检索账本，唯一常驻上下文）+ `research/sources/<type>/` 检索结果
- 详见 `references/knowledge-sources-protocol.md` §1-3

### Step 5：全文深读（一手资料全文，非摘要）

- 输入：Step 4 检索结果中 quality 候选高的资料
- 动作：关键论文/报告/锚点一手资料 WebFetch **全文**，每篇落一个 source-note（YAML frontmatter：finding / url_or_citation / freshness / principle_mapping / scores / injection_use / limitations）
- 输出：`research/sources/<type>/<item_id>.md`
- **gate（由 scripts/research_coverage_check.py 校验）**：检索操作数 + 全文精读数 + 来源覆盖达复杂度门槛（见 Quality Gates），不达标标 `knowledge_coverage: insufficient`，禁止进入 Step 6 的高置信产出

### Step 6：评分归档 + 喂宪法

- 输入：所有 source-note
- 动作：
  1. 六子项评分 + 迁移四项检验（尺度/环境/成本/成熟度），quality_score < 0.50 不进论据，relevance_score < 0.70 不作核心论断主依据
  2. 每个 KnowledgeRequest 汇总成一个 KnowledgeBundle（strongest_findings / transfer_hypotheses / decision_impact / risks / knowledge_coverage）
  3. 抽取概念节点回填 `constitution/concept_tree.json`；核心论据回填 `brief.yaml` 的核心论点 / uniqueness_anchor；术语回填 `registry/concepts.yaml`
- 输出：`research/bundles/<direction>.yaml` + 宪法三文件回填
- **gate**：作者确认 KnowledgeBundle 与回填的核心论点后，才能进入 `finalize-constitution`

---

## 运营规则

- **调研方向由作者确认**：Step 1 的调研方向树、Step 6 的 KnowledgeBundle 回填的核心论点，必须作者拍板（人类驱动协作）。AI 提供调研结果与候选论据，不替作者下核心论点。
- **类型无关底座 + 类型特化侧重**：本 skill 是共享调研底座；但调研侧重受 active-pack 影响——history 重史料源与史观争议，textbook 重教研源与知识 DAG，scifi 重前沿论文与外推边界，nonfiction 重产业数据与案例。读 active-pack 后调整源优先级，但不改方法论。
- **边检索边落盘**：每完成一条 query / 一篇深读，立即追加 research-log + 写 source-note。**上下文只留 research-log + 当前步**，source-note 细节按需 Read（对接 context-management.md）。
- **引用路径不内联**：回填宪法的论据引用 source-note 路径，不把全文复制进 brief。
- **与其他 Skill 的边界**：本 skill 只到 KnowledgeBundle + 宪法回填为止；大纲与正文由下游 skill 消费 research/ 作为论据库。

### 反模式（严禁）

- ❌ 用搜索摘要替代一手资料全文（摘要 ≠ 调研）
- ❌ 未读作者提供的锚点一手资料就下判断
- ❌ 未检索就声称"几乎没有先例"（"无先例"必须用检索证据定义）
- ❌ 跨域借鉴不做四项检验（尺度/环境/成本/成熟度）就写"可借鉴"
- ❌ 用 YAML / 置信度 / 矩阵包装浅调研（框架不能替代知识）
- ❌ 调研产物堆在对话上下文不落盘（会爆 + 丢细节）
- ❌ 只用主题词检索（如只搜"手机壳散热"），不做原理翻译四层
- ❌ 用现象词（"体验差""效率低"）当调研结论
- ❌ 调研充分性不足却强行回填高置信核心论点

---

## Quality Gates

| 检查项 | 量化标准 | 不通过的处理 |
|--------|---------|------------|
| 调研充分性（按复杂度分级） | 轻：检索 ≥30 / 全文精读 ≥3 / 来源覆盖 ≥3 类；中：≥80 / ≥5 / ≥3 类；重：≥150 / ≥8 / ≥4 类 | 标 `knowledge_coverage: insufficient`，禁止回填高置信核心论点，补调研或诚实降级 |
| 第一性原理深度 | 每个核心论断有原理拆解（学科+机制+指标，D2 起步），无现象词结论 | 重做 Step 1 降维，拒绝现象层结论进宪法 |
| 来源可追溯 | 每个数字/论断有 source-note（含 url_or_citation + freshness_status） | 报告无源断言，补 source-note 或删除论断 |
| 质量分门槛 | quality_score ≥0.50 才进论据；relevance_score ≥0.70 才作核心论断主依据 | 丢弃或降级为背景参考 |
| 冲突保留 | 不同来源矛盾标 conflict_status，不得选择性引用 | 报告冲突被掩盖，恢复冲突标注 |
| 新鲜度 | 数据标年份，超阈值（academic 18 月 / trends 12 月 / realtime 7-30 天，快变领域收紧）告警 | 刷新来源或标 stale 并补更新来源 |
| 人类确认 | 调研方向树 + KnowledgeBundle 回填的核心论点经作者确认 | 停下请作者确认，记录到 dialogue_log.jsonl |

---

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `socratic-dialogue`（上游） | 输出主题/赛道/读者轮廓，作为本 Skill 的调研起点 |
| `detect-genre`（上游） | 输出类型 + active-pack，决定调研侧重（史料/教研/论文/产业数据） |
| `benchmark-corpus-research`（并行） | 并行调研——它调书的风格（style-corpus/），本 Skill 调主题知识（research/），互不依赖，都为宪法供料 |
| `editorial-acquisition`（并行） | 并行——它做选题商业论证，本 Skill 做主题知识建库；可共享一手资料但产物不同 |
| `finalize-constitution`（下游） | 消费 research/bundles/ 回填 concept_tree.json / brief.yaml 核心论点 |
| `synthesize-outline` / `expand-chapter-plan`（下游） | 引用 research/sources/ 作为章节论据库 |
| `draft-v0~v3`（下游） | 草稿期引用 source-note 路径作为可追溯论据，不内联全文 |

---

## 文件输出

除非用户另有指定，主题知识库写入 `projects/<project-id>/research/`（与 `style-corpus/` / `constitution/` 并列）：

```
projects/<project-id>/research/
├── research-log.md          # ★ 唯一常驻上下文的调研文件（检索账本 + 进度 + source-note 指针）
├── knowledge-requests/      # Step 2：每个原理方向一个 .md
├── query-plans/             # Step 3：每个方向一个 QueryPlan
├── sources/                 # Step 4-5：检索结果 + 全文深读笔记
│   ├── academic/            #   论文/报告深读笔记（每篇一个 source-note）
│   ├── cases/               #   案例检索结果
│   ├── cross-domain/        #   跨域迁移候选
│   ├── anchor-assets/       #   作者提供的一手资料
│   └── realtime/            #   实时网络检索（新闻/发布会/博客）
└── bundles/                 # Step 6：KnowledgeBundle 汇总（喂给宪法）
```

调研充分性校验脚本：`python3 .claude/skills/deep-topic-research/scripts/research_coverage_check.py --out projects/<project-id>/research --complexity <light|medium|heavy>`

模板见 `.claude/skills/deep-topic-research/templates/`。
