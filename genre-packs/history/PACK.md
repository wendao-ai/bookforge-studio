---
genre_id: history
genre_name: 历史书籍
genre_family: nonfiction
maturity: stable
detection_signals:
  explicit_keywords:
  - 历史书籍
  - history
  intent_patterns: &id001
  - 史料可信度
  - 史观一致
  - 叙事与论证平衡
  - 时间线管理
  sub_genres: []
core_challenges: *id001
specialist_agents:
- history-genre-lead
- source-research-specialist
- source-credibility-assessor
- historiography-advisor
- timeline-manager
- narrative-argument-balancer
- citation-manager
- history-reader-simulator
memory_extensions:
- source-archive
- timeline
- historiography-statement
- citation-map
collaboration_mode: author-decides-historiography
quality_focus:
- source_reliability
- historiography_consistency
- narrative_readability
- argument_rigor
- timeline_accuracy
composable_with:
- scifi
- textbook
- romance
---

# 历史书籍创作范式

## Core Engine

史料库 + 史观一致性 + 时间线

## Creative Law

本 Pack 规定 `历史书籍` 项目的结构、记忆、质量度量和人审边界。共享六阶段流水线仍然适用，但每个阶段都必须读取本 Pack 的结构范式、读者画像和一致性规则。

## Required Human Decisions

- 确认该类型是否为 primary genre。
- 确认核心读者承诺。
- 确认 `author-decides-historiography` 模式下列出的关键创作决策。

## Quality Focus

- `source_reliability`
- `historiography_consistency`
- `narrative_readability`
- `argument_rigor`
- `timeline_accuracy`

## Specialist Agents

- `history-genre-lead`: coordinates historical method and review gates
- `source-research-specialist`: collects and summarizes sources
- `source-credibility-assessor`: labels source credibility and bias
- `historiography-advisor`: maintains viewpoint and interpretive frame
- `timeline-manager`: keeps chronology coherent
- `narrative-argument-balancer`: balances story and evidence
- `citation-manager`: maintains citation format and traceability
- `history-reader-simulator`: simulates expert, enthusiast, lay, and skeptical readers
