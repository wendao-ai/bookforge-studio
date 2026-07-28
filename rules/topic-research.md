# Topic Research Rules

## Mandatory Standards

- `research/` 调研充分性必须按主题复杂度达标（light：检索 ≥30/全文精读 ≥3/来源 ≥3 类；medium：≥80/≥5/≥3；heavy：≥150/≥8/≥4），由 `scripts/research_coverage_check.py` 校验；不达标标 `knowledge_coverage: insufficient`。
- 每个核心论断必须有第一性原理拆解（学科+机制+指标，D2 起步），禁止现象层结论（"市场大""体验差"）进入宪法核心论点。
- 每个数字、案例、论断必须有 `source-note` 可追溯：含 `url_or_citation`、`publication_date`、`freshness_status`、`confidence`（对接 three-tier-confidence 的 observed/inferred/speculated）。
- 关键数字（用于核心论点的）须 ≥ 2 个独立来源（三角验证）；史观/史料主张、专业知识主张须 `observed` 或经专家审。
- 不同来源矛盾必须保留 `conflict_status`（none/partially_conflicting/conflicting），不得选择性引用或抹平争议。
- 调研充分性不足时必须诚实降级：标 `knowledge_coverage: insufficient` 并拒绝回填高置信核心论点，宁可慢不可假。
- 调研产物必须边检索边落盘到 `research/`；上下文只常驻 `research-log.md` + 当前步骤，source-note 细节按需 Read（对接 context-management）。
- KnowledgeBundle 回填 `concept_tree.json` / `brief.yaml` / `registry/concepts.yaml` 前，调研方向与核心论点须作者确认，确认事件入 `dialogue_log.jsonl`。
- 检索必须走"原理翻译四层"（P0 原理名→P1 机制→P2 指标→P3 场景），每个原理 ≥6 条中英文 query 带 `derived_from`，禁止只用主题词或作者原话检索。

## Anti-Patterns

- 用搜索摘要替代一手资料全文（摘要 ≠ 调研；典型表现：只读搜索结果 snippet 就下结论）。
- 未读作者提供的锚点一手资料就下判断（漏掉真实细节，论点悬空）。
- 未检索就声称"几乎没有先例"（"无先例"必须用检索证据定义）。
- 跨域借鉴不做四项检验（尺度/环境/成本/成熟度）就写"可借鉴"。
- 用 YAML / 置信度 / 评分矩阵包装浅调研（框架不能替代知识，典型表现：source-note 字段齐全但 finding 空泛）。
- 调研产物堆在对话上下文不落盘（超出长度 + 丢失细节，违反 context-management）。
- 把 quality_score < 0.50 的资料当论据，或把 confidence: speculated 的迁移假设写成确定事实。
- 调研充分性不足却强行回填高置信核心论点到宪法（典型表现：3 篇摘要就敢定 thesis）。
- 抹平史观争议 / 学派分歧 / 研究冲突，只呈现单方观点。
