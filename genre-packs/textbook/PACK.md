---
genre_id: textbook
genre_name: 教材
genre_family: nonfiction
maturity: stable
detection_signals:
  explicit_keywords:
  - 教材
  - textbook
  intent_patterns: &id001
  - 知识路径拓扑正确
  - 认知负荷管理
  - 习题与知识点对齐
  - 专家审定
  sub_genres: []
core_challenges: *id001
specialist_agents:
- textbook-genre-lead
- knowledge-graph-architect
- concept-prerequisite-checker
- cognitive-load-manager
- pedagogy-designer
- exercise-designer
- example-curator
- student-simulator
memory_extensions:
- knowledge-dag
- learning-objectives
- exercise-bank
- assessment-map
collaboration_mode: expert-reviewed
quality_focus:
- prerequisite_integrity
- cognitive_load
- exercise_alignment
- clarity
- expert_accuracy
composable_with:
- scifi
- romance
- history
---

# 教材创作范式

## Core Engine

知识点 DAG + 强人审

## Creative Law

本 Pack 规定 `教材` 项目的结构、记忆、质量度量和人审边界。共享六阶段流水线仍然适用，但每个阶段都必须读取本 Pack 的结构范式、读者画像和一致性规则。

## Required Human Decisions

- 确认该类型是否为 primary genre。
- 确认核心读者承诺。
- 确认 `expert-reviewed` 模式下列出的关键创作决策。

## Quality Focus

- `prerequisite_integrity`
- `cognitive_load`
- `exercise_alignment`
- `clarity`
- `expert_accuracy`

## Specialist Agents

- `textbook-genre-lead`: coordinates textbook pedagogy and expert gates
- `knowledge-graph-architect`: builds the knowledge DAG
- `concept-prerequisite-checker`: detects prerequisite jumps
- `cognitive-load-manager`: balances new concepts per section
- `pedagogy-designer`: designs teaching strategy and learning path
- `exercise-designer`: creates aligned exercises and answers
- `example-curator`: curates examples for transfer and clarity
- `student-simulator`: simulates strong, average, struggling, and self-study learners
