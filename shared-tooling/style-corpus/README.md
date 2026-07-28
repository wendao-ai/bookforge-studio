# Style Corpus（对标书风格语料库）

> 两层结构：项目专属（单本书调研）+ 全局共享（跨项目复用）

## 为什么需要

Bookie 写出来的书要达到品类专业水平，必须先向品类内最好的书学风格。style-corpus 是这个"学习"的产物落地处——把"风格"从主观感受变成可追溯、可机读、可复用的工程产物。

由 [`/benchmark-corpus-research`](../../.claude/skills/benchmark-corpus-research/SKILL.md) 产出，schema 标准见 [rules/style-corpus.md](../../.claude/rules/style-corpus.md)。

## 两层结构

### 项目专属：`projects/<project-id>/style-corpus/`

本书的对标调研，由 `/benchmark-corpus-research` 在 ideation 阶段产出：

```
projects/<project-id>/style-corpus/
├── corpus-index.yaml              # 对标书清单（≥5 本）
├── <book-id>.deconstruction.md    # 逐本正面风格解构
├── <book-id>.anti-patterns.md     # 逐本反面教材
├── style-anchor.yaml              # 综合可机读风格锚（喂给宪法 + 草稿）
└── synthesis.md                   # 品类共性 + 差异化空间
```

### 全局共享：`shared-tooling/style-corpus/<genre>/<book-id>/`

跨项目复用的品类语料，由 `/harvest-writing-pattern` 从项目沉淀而来。一本书被 ≥2 个项目引用后，晋升到全局层，避免每个项目重复调研同一本经典。

## 与 capability-library 的分工

| 位置 | 存什么 | 形态 |
|---|---|---|
| `capability-library/by-genre/<genre>/style-anchoring-patterns/` | 抽象的、可复用的风格模式（如"经管书的案例-框架-数据三段式"） | 模式 |
| `shared-tooling/style-corpus/<genre>/<book-id>/` | 具体的对标书解构原文（带引文、数据源、句长样本） | 语料 |

抽象模式 + 具体操料，两者互补。模式指导"怎么写"，语料证明"为什么这么写"。

## 数据源与合规

数据源分 L1（公开元数据）/ L2（公开试读内容）/ L3（合法全书）三层，红线与抓取边界详见 [`/benchmark-corpus-research` SKILL.md](../../.claude/skills/benchmark-corpus-research/SKILL.md) 的"数据源分层"小节。L3 必须有合法来源声明，出版社 B 端交付时此为硬性合规要求。
