# Style Corpus Rules

## Mandatory Standards

- `corpus-index.yaml` 每本书必须含字段：`book_id`、`title`、`author`、`publisher`、`year`、`price`、`sales_tier`、`rating`、`positioning`、`angle`、`representativeness`、`source_tier`（L1/L2/L3）、`compliance`（合法来源声明）、`provenance`（URL / 文件路径 / 抓取时间）。
- 对标书数量 ≥5，至少含 1 本近 2 年新书 + 1 本经典；全是新书缺经典、或全是经典缺新书，均不合规。
- `<book-id>.deconstruction.md` 必须覆盖维度：`title_pattern`、`chapter_title_structure`、`opening_pattern`、`sentence_length_distribution`、`terminology_density`、`voice_and_person`、`case_usage`、`data_presentation`、`chapter_closing`、`typesetting_features`。每个维度必须引用具体段落 / 引文 / 样本数据。
- `<book-id>.anti-patterns.md` 每条反面教材必须含四字段：`pattern`（失败模式）、`evidence`（具体证据，引文或页码）、`why_bad`（为什么不好）、`avoid_how`（本书如何避开）。缺 `avoid_how` 视为不合规。
- `style-anchor.yaml` 必须含可机读字段：`sentence_length`（min/p50/max，单位：字）、`terminology_density`（术语占比区间）、`voice`（人称 / 语气 / 时态）、`chapter_title_paradigm`（范式 + ≥3 示例）、`opening_template`、`typesetting_spec`、`forbidden_drift`（清单）、`exemplar_passages`（≥3 段，每段带出处）。
- 所有数据源必须可追溯：L1 记 URL，L2 记 URL + 抓取时间，L3 记文件路径 + 合法来源声明。
- 抓取前必须做红线自检：付费墙 / DRM / 盗版站 / L3 合法来源缺失。触发即停，不静默跳过。
- 作者必须确认 `corpus-index.yaml` + `style-anchor.yaml` + 差异化空间后，才能进入宪法文件。确认事件入 `dialogue_log.jsonl`。
- 品类共性结论必须基于 ≥3 本对标书的交叉证据，不得用单本书（n=1）的结论冒充品类共性。

## Anti-Patterns

- 解构维度写成"文笔流畅""深入浅出"等空泛评语，无具体引文或样本数据。
- 反面教材只说"不好"却不给"本书如何避开"。
- `style-anchor.yaml` 只用自然语言描述，无可机读字段（草稿期 `anchor-style` 无法消费）。
- 对标书全是经典无近 2 年新书（风格会过时），或全是新书无经典（缺失品类根基）。
- L3 全书解析却无合法来源声明（版权风险，出版社 B 端不可交付）。
- 红线触发却静默跳过继续抓取。
- `corpus-index.yaml` 与 editorial-acquisition 竞品矩阵重复调研、不共享。
- 把单本对标书的风格当成品类共性沉淀（n=1 沉淀）。
- 解构只看"写了什么"不看"怎么排版"（排版是专业感的核心组成，不可遗漏）。
