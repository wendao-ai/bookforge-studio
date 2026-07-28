# 深度调研教义（Deep Research Doctrine）

> **信条**：破解一个有价值的问题，必须储备 100 倍的知识。搜索 ≠ 调研；摘要 ≠ 全文；框架 ≠ 知识。
> 不充分调研的产出，比不产出更危险——它会用专业框架包装浅薄判断，让整本书建立在虚假地基上。
> 本文件是 deep-topic-research SKILL 原则 2 的操作手册，定义 Step 2-5 的强制流程与门槛。

---

## 1. 100 倍知识储备法则

> 就像博士生为在人类前沿做一个微小突破，储备 20-40 年知识。写一本有立论深度的书，本质上是在某个主题的认知边界上做系统性整理——用 5 分钟搜索替代充分调研，是傲慢，不是高效。

| 目标层级 | 最低知识储备 | 典型投入 |
|---------|------------|---------|
| 单个论点/知识点 | ≥ 100 倍 | 数十篇资料精读 |
| 本书核心论点 | ≥ 300 倍 | 跨学科 + 跨案例 + 全前沿 |
| 争议性核心论断 | ≥ 1000 倍 | 接近博士级储备 |

---

## 2. 量化门槛（按主题复杂度分级）

本 skill 面向**单本书**，门槛按主题复杂度分级（区别于大全的统一高门槛）。门槛是地板，不是天花板。

### 调研充分性门槛表

| 复杂度 | 适用主题 | 检索操作数（query 执行次数） | 一手资料全文精读 | 案例检索 | 来源类型覆盖 |
|--------|---------|---------------------------|----------------|---------|------------|
| **轻（light）** | 单一概念 / 单一技术 / 单点现象 | ≥ 30 | ≥ 3 篇 | ≥ 5 条 | ≥ 3 类 |
| **中（medium）** | 中等复杂主题 / 单一行业 / 多概念体系 | ≥ 80 | ≥ 5 篇 | ≥ 8 条/方向 | ≥ 3 类 |
| **重（heavy）** | 跨学科 / 复杂系统 / 产业级 / 强争议 | ≥ 150 | ≥ 8 篇 | ≥ 12 条/方向 | ≥ 4 类 |

### 复杂度判定指引

- 默认按"重"准备，除非作者明确主题窄、争议小（才降到中/轻）
- 涉及核心论点真伪、史料史观、专业准确性、投资决策的，**强制按"重"**
- 由 `scripts/research_coverage_check.py --complexity` 自动校验是否达标

### 禁止项（任何复杂度都不许）

| 知识类型 | 禁止 |
|---------|------|
| 一手资料全文精读 | ❌ 只读搜索摘要就下结论 |
| 案例检索 | ❌ 凭印象举例 |
| 跨域成熟方案候选 | ❌ 凭空说"可借鉴"（须四项检验） |
| 作者锚点一手资料（如有） | ❌ 不读就下判断 |

---

## 3. 深度调研五步法（强制流程，不可跳过）

对应 SKILL 的 Step 2-6。每一步都必须留下可审计痕迹。

```
Step 2: KnowledgeRequest    先写结构化请求
  说明"要解决什么原理问题、为什么需要外部知识、知识将注入本书哪个论断/章节"
  → 落盘 research/knowledge-requests/

Step 3: QueryPlan           原理→中英文 query 翻译
  每个 primary_principle 至少生成 6 条 query（含同义词/上下位/中英双语）
  每条带 derived_from 追溯
  → 落盘 research/query-plans/

Step 4: 多源检索            学术 + 跨域 + 趋势 + 实时 + 锚点资料
  每条 query 立即记入 research-log.md 检索账本
  每源/每方向落盘 sources/

Step 5: 全文深读            关键论文/报告 WebFetch 全文（非摘要）
  锚点项目一手资料必读
  每篇落盘一个 source-note

Step 6: 评分归档            质量分(6子项) + 新鲜度 + 迁移四项检验
  审计回写 research-log
  诚实的边界判断
  → 汇总落盘 bundles/，回填宪法
```

---

## 4. 分阶段落盘（上下文治理，关键！）

> 深度调研涉及大量资料。**禁止把所有调研产物堆在对话上下文里**——会超出长度并丢失细节。每步产出立即落盘到 `research/`；上下文只保留"当前步骤 + research-log 索引"。
> 这条对接 BookForge 的 `.claude/docs/context-management.md`：项目文件胜过对话记忆。

### 调研工作台目录结构（每个项目首次调研时建）

```
projects/<project-id>/research/
├── research-log.md          # ★ 唯一常驻上下文的调研文件（检索账本+进度+指针）
├── knowledge-requests/      # Step 2：每个 KnowledgeRequest 一个 .md
├── query-plans/             # Step 3：每个 QueryPlan 一个 .md
├── sources/                 # Step 4-5：检索结果 + 全文深读笔记
│   ├── academic/            #   论文/报告深读笔记（每篇一个 source-note）
│   ├── cases/               #   案例检索结果
│   ├── cross-domain/        #   跨域迁移候选
│   ├── anchor-assets/       #   作者提供的一手资料
│   └── realtime/            #   实时网络检索
└── bundles/                 # Step 6：KnowledgeBundle 汇总（喂给宪法）
```

### 落盘红线

1. **边检索边落盘**：每完成一条 query / 一篇深读，立即追加 research-log + 写 source-note，绝不"等最后汇总"
2. **上下文只留 research-log + 当前步**：source-note / query-plan 细节一律按需 Read，不常驻
3. **产物引用路径，不内联内容**：回填宪法的论据引用 source-note 路径，不把全文复制进 brief
4. **可重建可追溯**：任何结论都能从 research-log → source-note → 原始资料逐层追溯
5. **冲突必须保留**：不同来源矛盾时标注 conflict_status，不得选择性引用

---

## 5. source-note 模板（每条知识一个）

详见 `templates/source-note.md.tmpl`。核心字段：

```yaml
---
item_id: "ki-{date}-{topic}-{seq}"
source: "academic | report | cross-domain | realtime | anchor-asset"
title: "资料标题"
finding: "可注入本书论断的具体发现（非泛泛背景）"
url_or_citation: "DOI/URL/报告编号/内部路径"
publication_date: "YYYY-MM"
retrieved_at: "YYYY-MM-DD"
freshness: "YYYY-Qn"
freshness_status: "fresh | aging | stale | expired"

principle_mapping:
  primary_principle: "对应的第一性原理"
  mechanisms: ["机制词"]
  measurable_variables: ["指标"]

scores:
  quality_score: 0.0-1.0      # 六子项加权（见 knowledge-sources-protocol.md）
  relevance_score: 0.0-1.0
  final_score: 0.0-1.0
  confidence: "observed | inferred | speculated"   # 对接 three-tier-confidence

injection_use: "它会如何影响本书的哪个论断/章节"
limitations:
  - "适用边界 1"
  - "适用边界 2"
---
```

---

## 6. 红线（绝对禁止项）

- ❌ **用搜索摘要替代一手资料全文**（摘要 ≠ 调研）
- ❌ **未读作者提供的锚点一手资料就下判断**（会漏掉真实细节）
- ❌ **未检索就声称"几乎没有先例"**（"无先例"必须用检索证据定义）
- ❌ **跨域借鉴不做四项检验**（尺度/环境/成本/成熟度）
- ❌ **把"搜索到的东西"等同于"充分调研"**
- ❌ **用专业框架（YAML/置信度/矩阵）包装浅调研**（框架不能替代知识）
- ❌ **跳过五步法的任何一步**
- ❌ **调研产物堆在上下文不落盘**（会爆 + 丢细节）

---

## 7. 守门与降级

- **前置守门**：`scripts/research_coverage_check.py` 在回填宪法前校验 research-log 检索操作数 + 全文精读数 + 来源覆盖度
- **诚实降级**：若知识不足，标 `knowledge_coverage: insufficient` 并拒绝产出高置信结论、拒绝回填高置信核心论点
- **类型加重**：history（史料）/ textbook（专业准确性）/ 涉投资决策的论断，门槛只升不降

---

## 8. 一句话总结

> **用博士储备的尺度做调研，用工程师的严谨守门槛，用科学家的诚实承认边界。**
> 宁可慢，不可假。

---

## 9. 与其他 references 的关系

- 本教义是知识获取的**信条层与强制层**（Step 2-5 + 门槛 + 红线）
- `knowledge-sources-protocol.md` 是**机制层**（怎么检索/评分/新鲜度）
- `first-principles-method.md` 定义调研结果如何用于主题/论点拆解（Step 1）
