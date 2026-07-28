# 知识源协议（Knowledge Sources Protocol）

> 定义"知识从哪来、怎么翻译成 query、怎么评质量、怎么管新鲜度"。是深度调研教义的机制层，对应 SKILL 的 Step 3-6。
> 本文件同时定义与 BookForge `.claude/docs/three-tier-confidence.md` 的对接。

---

## 1. 五类知识源

| 源 | 用途 | 质量特征 | 默认新鲜度阈值 |
|----|------|---------|--------------|
| **① academic / authoritative** | 全球最新研究 / 权威报告 / 经典著作 / 教材 | 权威，但有滞后 | 18 个月 |
| **② cross-domain-transfer** ★ | 把别的领域/学科的成熟原理迁移过来阐释本主题 | 启发性强，需验证 | 无固定过期，按主题复审 |
| **③ trends-standards** | 行业趋势 / 标准 / 路线图 / 白皮书 / 共识 | 方向性 | 12 个月 |
| **④ realtime-search** | 实时网络检索（新闻/发布会/博客/官方公告） | 最新，但质量参差 | 7-30 天 |
| **⑤ anchor-corpus** ★ | 作者提供的一手资料（调研报告/内部数据/访谈/已购正版书） | 最贴合本书论点，但单点 | 项目期内有效 |

**检索优先级**：①⑤ > ③ > ② > ④（一手 + 锚点优先，实时搜索最后补缺）。

**类型特化侧重**（读 active-pack 后调整源优先级，不改方法论）：
- history：①史料/档案 + ⑤作者史料 > ③史学界共识；重视史观争议
- textbook：①经典教材/教研文献 > ③课程标准；重视知识 DAG 与专家审
- scifi：①前沿论文 > ②跨域外推；明确区分 plausible extrapolation 与 speculation
- nonfiction：①权威报告 + ⑤行业一手数据 > ③趋势；重视案例与三角验证

---

## 2. 原理翻译四层（把第一性原理翻译成 query）

知识检索**不直接用主题词**，先把第一性原理拆成四层，再为不同源生成 query。

| 层 | 作用 | 示例（主题=读者工作记忆限制） |
|----|------|------------------|
| P0 原理名 | 保留第一性锚点 | 工作记忆容量限制 / working memory capacity limit |
| P1 机制词 | 捕捉具体作用机制 | 组块化、认知负荷、信息衰减、注意力切换 |
| P2 指标词 | 绑定可验证变量 | 7±2、保持时长、错误率、迁移率 |
| P3 场景词 | 控制迁移方向 | 教材编排、在线课程、技能训练、知识图谱 |

**禁止**：只用主题词或书名检索（如只搜"怎么写好教材"）。每个原理至少生成 6 条 query，含中英双语 + 同义词 + 上下位概念。

---

## 3. Query 生成算法

```
输入：primary_principle + mechanism_terms + measurable_variables + target_domains + source_domains_to_probe

Step 1：规范化术语
  生成中英文同义词、缩写、上位/下位概念

Step 2：按源拆分意图
  academic     = 原理词 + 机制词 + 指标词 + recent/review/survey
  cross-domain = 原理词 + 来源领域 + mature technique + transfer target
  trends       = 目标领域 + 路线图/标准/白皮书/共识 + 年份
  realtime     = 原理词 + breakthrough/latest/official/报告 + 年份

Step 3：组合 query（每源 3-8 条，含 zh/en 两组）

Step 4：添加排除词
  去掉营销软文、泛泛科普、无来源转载

Step 5：记录 provenance
  每条 query 必须能回溯到哪个原理/机制/指标（derived_from）
```

### QueryPlan 输出格式（详见 templates/query-plan.md.tmpl）

```yaml
query_plan_id: "qp-{date}-{topic}-{seq}"
principle: "工作记忆容量限制"
queries:
  - source: "academic"
    language: "en"
    query: "\"working memory capacity\" \"cognitive load\" review"
    derived_from: ["primary_principle", "measurable_variables.cognitive load"]
    intent: "寻找前沿研究"
  - source: "cross-domain-transfer"
    language: "zh"
    query: "\"组块化\" \"技能训练\" \"教材编排\" 迁移"
    derived_from: ["source_domains_to_probe.技能训练", "target_domains.教材编排"]
    intent: "寻找成熟方法迁移"
```

### Query 质量门

- 每个 primary_principle 至少 6 条 query：academic ≥ 2、cross-domain ≥ 2、realtime ≥ 1、trends ≥ 1
- 每个 query 含 ≥ 1 个原理词 + ≥ 1 个机制/指标词
- 高价值主题必须含中英文双语 query
- 禁止只用作者原话或主题名检索
- 所有 query 保留 derived_from，否则结果不得进入审计日志

---

## 4. 六子项质量评分

每条知识按六子项评分（0-1），再按检索目的加权。

| 子项 | 记号 | 含义 |
|------|------|------|
| 来源可信度 | C | 期刊/官方/标准 > 预印本 > 企业白皮书 > 媒体 > 未知 |
| 证据强度 | E | 可复现实验/标准条文 > 定量数据 > 案例 > 专家观点 > 纯结论 |
| 相关性 | R | 命中原理 + 机制 + 指标 + 场景的层数 |
| 新鲜度 | F | 在该源阈值内（见 §5） |
| 可迁移性 | T | 跨域知识能否迁移到本主题（尺度/环境/成本/成熟度） |
| 可行动性 | A | 能否转化为本书论断/案例/数字 |

**默认权重**（按检索目的）：

| purpose | C | E | R | F | T | A |
|---------|---|---|---|---|---|---|
| frontier_inspiration（前沿启发） | 0.15 | 0.15 | 0.25 | 0.15 | 0.15 | 0.15 |
| case_collection（案例收集） | 0.20 | 0.25 | 0.30 | 0.10 | 0.05 | 0.10 |
| transfer_scouting（跨域迁移） | 0.10 | 0.15 | 0.20 | 0.10 | 0.30 | 0.15 |
| trend_validation（趋势验证） | 0.20 | 0.20 | 0.20 | 0.20 | 0.05 | 0.15 |

```
final_score = C*wC + E*wE + R*wR + F*wF + T*wT + A*wA
```

### 质量等级与动作

| final_score | 等级 | 动作 |
|-------------|------|------|
| ≥ 0.80 | A | 可作为关键论据回填宪法 |
| 0.65-0.79 | B | 可用，但 source-note 须写明 limitations |
| 0.50-0.64 | C | 仅作背景参考，不单独支撑论断 |
| < 0.50 | D | 不进入论据库 |

**硬规则**：
- quality_score < 0.50 不得作为论据
- relevance_score < 0.70 不得作为核心论断的主要依据
- source_credibility < 0.40 默认丢弃
- confidence: speculated 的迁移假设不得写成确定事实

---

## 5. 与 BookForge 三层置信度对接（关键）

本 skill 的 source-note 评分与 BookForge `.claude/docs/three-tier-confidence.md` 的三级标签对齐，**每条知识必须标 confidence**：

| 本 skill 判定 | three-tier-confidence 标签 | 含义 | 能否支撑核心论点 |
|---|---|---|---|
| 一手资料直接陈述 / 有原始出处 / 作者决策 | `observed` | 直接陈述、已引用、存在于项目记忆 | 可作核心论断主依据 |
| 证据强相关推论 / 多源一致但非原文 | `inferred` | 证据强相关暗示 | 可用，标注推论依据 |
| 推测 / 单点来源 / 跨域迁移假设 | `speculated` | 合理但未被充分支撑 | **不得**作核心论断（critical 决策不得停留在 speculated） |

对接规则：
- 回填宪法 `concept_tree.json` / `brief.yaml` 的核心论点，主依据须 ≥ `inferred`，理想 `observed`
- `speculated` 知识只进 source-note 与 background，不进核心论断；若核心论断只有 speculated 支撑，触发诚实降级
- history 的史料主张、textbook 的知识主张：须 `observed` 或经专家审，与 three-tier-confidence 的领域要求一致

---

## 6. 新鲜度阈值

新鲜度按知识源 × 用途 × 领域变化速度配置。

### 默认阈值

| 源 | 默认阈值 | 过期动作 |
|----|---------|---------|
| academic | 18 个月 | 刷新或标 stale |
| cross-domain-transfer | 无固定（按主题复审，年度） | 复审迁移假设 |
| trends-standards | 12 个月 | 刷新 |
| realtime-search | 7-30 天 | 刷新 |
| anchor-corpus | 项目期内 | 项目结束即归档 |

### 按领域变化速度覆盖

| 速度 | 典型领域 | academic | realtime | trends |
|------|---------|----------|----------|--------|
| fast | AI模型 / 半导体 / 电池材料 / 通信标准 | 12 月 | 7 天 | 6 月 |
| normal | 机械结构 / 传统工艺 / 工业控制 | 18 月 | 14 天 | 12 月 |
| slow | 基础物理原理 / 经典方法 / 成熟工艺 | 36 月 | 30 天 | 24 月 |

### freshness_status 判定

```
age_days = retrieved_at - publication_date
threshold = resolved threshold (source × purpose × domain_velocity)

fresh   : age ≤ threshold × 0.75      → score 1.0，直接用
aging   : age ≤ threshold              → score 0.7，可用 + 补 1 条更新来源
stale   : age ≤ threshold × 1.5        → score 0.4，不得作唯一依据
expired : age > threshold × 1.5        → score 0.1，不得注入新论断（经典原理例外，须标注理由）
```

---

## 7. KnowledgeBundle 返回格式（喂给宪法）

一次 KnowledgeRequest 返回一个 bundle。详见 `templates/knowledge-bundle.md.tmpl`。

```yaml
bundle_id: "kbundle-{date}-{topic}-{seq}"
coverage:
  requested_sources: [academic, cross-domain, trends, realtime]
  fulfilled_sources: [academic, cross-domain, realtime]
  missing_sources:
    - source: "trends-standards"
      reason: "未找到与主题直接相关的现行标准"
  knowledge_coverage: "sufficient | partial | insufficient"

top_items: ["ki-001", "ki-002", "ki-003"]

injection_summary:
  principle: "工作记忆容量限制"
  strongest_findings:
    - "组块化可将一次性可处理概念数提升 3-5 倍（observed，2 篇 meta 分析）"
    - "认知负荷理论在教材编排中已有成熟应用（observed）"
  transfer_hypotheses:
    - "将技能训练的间隔重复机制迁移到本书的章节复习设计（speculated，待四项检验）"
  decision_impact:
    - "concept_tree 应增加'认知负荷'节点作为全书编排原理"
    - "核心论点可主张：本书按工作记忆原理重组知识结构，区别于现有书的内容堆砌"
  risks:
    - "迁移假设需在草稿期用案例验证"
    - "部分前沿研究 sample size 偏小，须标注"
```

`knowledge_coverage: insufficient` 时，禁止把该方向写成高置信结论、禁止回填核心论点。

---

## 8. 去重与冲突标注

同一发现来自多来源时合并，不重复注入：

```yaml
dedup_key: "principle:{p}|mechanism:{m}|finding_hash:{hash}"
supporting_sources:
  - source: "academic"
    citation: "..."
  - source: "realtime"
    url: "..."
conflict_status: "none | partially_conflicting | conflicting"
conflict_note: "不同来源对指标/成熟度/适用场景的冲突说明"
```

冲突**必须保留**，不得选择性引用。史观/学派争议（history）、不同研究结论冲突（textbook/scifi）尤其要如实呈现对立观点。

---

## 9. 与其他 references 的关系

- 本协议是机制层（怎么检索/评分/新鲜度/置信度对接）
- `deep-research-doctrine.md` 是信条层（为什么必须这个深度 + 门槛 + 红线）
- 二者共同支撑 `first-principles-method.md` 的 P2 原理拆解
