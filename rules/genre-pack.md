---
description: "Genre Pack 9 组件完整性"
globs:
  - "genre-packs/*/**"
---

# Genre Pack 9 组件完整性

## Mandatory Standards

- 每个 Pack 必须包含 `PACK.md`、`agents/`、`skills/`、`memory-schema.yaml`、`structure-paradigm.yaml`、`reader-profiles.yaml`、`quality-metrics.yaml`、`collaboration-mode.yaml`、`consistency-rules.yaml`。
- `PACK.md` frontmatter 必须声明 `genre_id`、`genre_family`、`detection_signals`、`core_challenges`、`specialist_agents`、`memory_extensions`、`collaboration_mode`、`quality_focus`。
- `specialist_agents` 中列出的每个 agent 必须在本 Pack 的 `agents/` 中存在。
- `consistency-rules.yaml` 至少包含一条 `critical` 规则，且每条规则必须有 `description`、`check`、`action`。
- `reader-profiles.yaml` 至少定义三类读者画像。
- `collaboration-mode.yaml` 必须列出需要人审的关键决策。

## Anti-Patterns

- 只改 prompt 文案却不定义 memory、质量度量与一致性规则。
- Pack 的 `genre_id` 与目录名不一致。
- 专属 Agent 写入其他 Pack 的 memory schema。
- 教材、历史等高风险类型标记为 fully automated。
