---
name: "benchmark-corpus-research"
description: "对标书调研与风格学习——在宪法前抓取并解构品类内 ≥5 本代表书的风格（书名/标题/行文/用词/排版），识别反面教材，产出可机读 style-anchor 喂给宪法与草稿。把'写得像专业品类书'从玄学变成可追溯的工程流程。"
category: "ideation"
---

# /benchmark-corpus-research

## Purpose

在类型识别后、宪法文件前，引入"对标书学习"环节。

Bookie 写出来的书要达到专业水平，不能凭空设定 `style_direction`。必须先调研品类内已有的代表书，解构它们的风格是如何形成"专业感"的，同时识别它们的失败模式，作为本书的 do-not 清单。

这一步把"风格"从主观感受变成可追溯、可机读、可复用的工程产物：

- **正面解构**：书名范式 / 章节标题结构 / 开篇范式 / 句长分布 / 术语密度 / 案例用法 / 数据呈现 / 章节收束 / 排版特征
- **反面教材**：注水 / 重复 / 术语堆砌 / 案例陈旧 / 逻辑跳跃 / 标题党 / 排版灾难

产物 `style-anchor.yaml` 反向喂给宪法的 `style_direction` / `uniqueness_anchor` / `target_length`，并贯穿后续 `anchor-style`、草稿、`editorial-acquisition`。

与 [editorial-acquisition](../editorial-acquisition/SKILL.md) 互补：editorial-acquisition 管"选题能不能立项/能不能卖"（编辑视角），本 skill 管"风格怎么写得专业"（作者视角）。两者共用 `corpus-index.yaml`，调研一次、两处用。

## 触发时机

ideation 阶段，`detect-genre` 之后、`finalize-constitution` 之前。

前置：类型已识别、苏格拉底深挖已产出主题/赛道/读者轮廓。

## 数据源分层（全自动抓取的合规边界）

为满足"全自动抓取"且可向出版社 B 端交付（出版社自有正版库），数据源分三层 + 一条红线：

| 层级 | 内容 | 抓取方式 | 用途 |
|---|---|---|---|
| **L1 公开元数据** | 书名 / 作者 / 出版社 / 年份 / 定价 / 销量级 / 评分 / 分类 / **完整目录** | 联网自动抓（出版社官网、豆瓣、当当、京东、Goodreads、Amazon） | corpus-index / 竞品矩阵 / 标题结构分析 |
| **L2 公开试读内容** | 出版社试读章 / 作者公众号连载 / 媒体转载章节 / Google Books 预览 / 豆瓣读书笔记摘录 / 书评引用段落 | 联网自动抓 | 开篇范式 / 行文片段 / 用词样本 |
| **L3 合法全书** | 作者本地已购正版的 PDF / EPUB / 纸质书 OCR / 出版社授权样书 | 自动解析全文 | 完整风格解构（句长分布、术语密度、章节收束、排版） |

**红线（禁止）**：

- 不绕过付费墙、不破解 DRM
- 不从盗版站抓全书正文
- L3 必须有合法来源声明（购书凭证 / 出版社授权 / 公有领域 / 合理使用标注），否则拒绝解析

**"全自动"的含义**：作者给出主题后，skill 自动完成"对标书发现（L1）→ 公开内容抓取（L2）→ 本地文件解析（L3，若提供）→ 解构 → 反面识别 → 风格锚综合"，全程无需作者手动摘抄。红线由 skill 在抓取前自检，触发即停并报告，不静默跳过。

## Inputs

- 类型（`detect-genre` 产出）+ 主题/赛道（苏格拉底深挖产出）
- 作者已有的对标书清单（可选；若无，skill 自动发现）
- 作者提供的本地电子书文件路径（可选，L3）
- `editorial-acquisition/category-benchmarks.yaml`（品类基准，若有；可与 editorial-acquisition 共享调研）
- 作者偏好的对标书数量与侧重（默认 ≥5 本，至少含 1 本近 2 年新书 + 1 本经典）

## Outputs

写入 `projects/<project-id>/style-corpus/`：

- `corpus-index.yaml` —— 对标书清单（≥5 本），每本带 book_id / 书名 / 作者 / 出版社 / 年份 / 定价 / 销量级 / 评分 / 定位 / 视角 / 品类代表度 / 数据源层级 / 合规标记 / provenance
- `<book-id>.deconstruction.md` —— 逐本风格解构（必含字段见 [rules/style-corpus.md](../../rules/style-corpus.md)）
- `<book-id>.anti-patterns.md` —— 逐本反面教材（必含字段见 [rules/style-corpus.md](../../rules/style-corpus.md)）
- `style-anchor.yaml` —— 综合提炼的可机读风格锚（schema 见 [rules/style-corpus.md](../../rules/style-corpus.md)）
- `synthesis.md` —— 综合分析：品类风格共性 + 反面教训汇总 + 本书的差异化风格空间（喂给宪法的 `uniqueness_anchor` 与 editorial-acquisition 的市场空白识别）

## Steps

1. **对标书发现**：基于类型 + 主题，自动检索品类代表书（销量 / 口碑 / 近 2 年新书 / 经典），产出候选清单（≥10 本）供作者圈选或自动取 Top N。来源 L1。
2. **元数据抓取**：对选定的 ≥5 本，自动抓 L1 公开元数据，填 `corpus-index.yaml`。
3. **内容抓取**：自动抓 L2 公开试读内容；若作者提供 L3 本地文件，解析全文。抓取前做红线自检（付费墙 / DRM / 盗版站 / 合法来源）。
4. **逐本风格解构**：对每本对标书，按解构维度（书名范式 / 章节标题结构 / 开篇范式 / 句长分布 / 术语密度 / 人称与语气 / 案例用法 / 数据呈现 / 章节收束 / 排版特征）逐项分析，**每项必须引用具体段落或样本数据**，写 `<book-id>.deconstruction.md`。
5. **反面教材识别**：逐本标注失败模式（注水 / 重复 / 术语堆砌 / 案例陈旧 / 逻辑跳跃 / 标题党 / 排版灾难），每条给"为什么不好 + 本书如何避开"两条，写 `<book-id>.anti-patterns.md`。
6. **风格锚综合**：跨书提炼共性 → `style-anchor.yaml`（可机读：句长分布区间、术语密度、人称、章节标题范式、开篇模板、排版规范、forbidden_drift 清单、exemplar_passages）。
7. **差异化空间识别**：基于共性 + 反面，输出 `synthesis.md` 的"本书风格差异化空间"，喂给宪法的 `uniqueness_anchor`。
8. **合规与可追溯**：所有解构保留数据源引用（URL / 页码 / 文件路径 / 抓取时间），写入 `corpus-index.yaml` 的 provenance 字段。
9. **请作者确认**：对标书清单、style-anchor、差异化空间需作者确认后才能进入宪法文件。确认事件记录到 `dialogue_log.jsonl`。

## Quality Gates

- 对标书 ≥5 本，其中至少 1 本近 2 年新书 + 1 本经典；不足则停下请作者补充
- 每本解构的每个维度**必须引用具体段落 / 引文 / 样本数据**，不接受"文笔流畅""深入浅出"这类空泛评语
- 反面教材每条必须给"为什么不好 + 本书如何避开"两条，缺一不可
- `style-anchor.yaml` 必须含可机读字段（句长分布、术语密度、人称、章节标题范式），不只靠自然语言描述——否则草稿期 `anchor-style` 无法消费
- 所有数据源必须可追溯：L1 记 URL，L2 记 URL + 抓取时间，L3 记文件路径 + 合法来源声明
- 红线触发（付费墙 / DRM / 盗版站 / 无合法来源的 L3）必须停下报告，不静默跳过
- `synthesis.md` 的差异化空间必须基于共性 + 反面推导，不能凭空主张独特性

## Error Handling

- 若对标书不足 5 本（小众品类）：标注"品类语料稀疏"，请作者补充或放宽品类边界，不编造
- 若 L2 公开内容不足以解构（如对标书无试读）：降级为"仅元数据 + 目录结构分析"，并在 deconstruction 标注 `coverage: partial`
- 若 L3 文件无合法来源声明：拒绝解析，提示作者补声明或改用 L1/L2
- 若红线触发：停下，报告触发的源与规则，不抓取
- 若触发本 skill 但类型未识别：报错并指向 `/detect-genre`
- 若与 editorial-acquisition 调研重叠：复用 `corpus-index.yaml`，不重复抓取（调研一次，两处用）

## 关联

- 衔接：`detect-genre` → **benchmark-corpus-research** → `finalize-constitution`（`style_direction` 引用 style-anchor）→ `editorial-acquisition`（复用 corpus-index 做竞品矩阵）
- 反向喂给：宪法 `brief.yaml` 的 `style_direction` / `uniqueness_anchor` / `target_length`（参见 [rules/constitution.md](../../rules/constitution.md)）
- 草稿期引用：`anchor-style` 与 `draft-v*` 引用 `style-anchor.yaml` 作为 voice constraints 来源
- 沉淀：项目结束后由 `harvest-writing-pattern` 把验证有效的解构沉淀到 `shared-tooling/style-corpus/<genre>/` 与 `capability-library/by-genre/<genre>/style-anchoring-patterns/`
- 规则：[rules/style-corpus.md](../../rules/style-corpus.md) 定义语料库 schema 与解构标准
- 产品化价值：与 editorial-acquisition（选题论证）互补——一个管"市场能不能卖"，一个管"风格怎么写得专业"。两者合一，覆盖出版社 B 端"前段选题 + 风格品控"的核心价值主张
