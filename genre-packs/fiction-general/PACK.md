---
genre_id: fiction-general
genre_name: 通用虚构
genre_family: fiction
maturity: stable
detection_signals:
  explicit_keywords:
  - 通用虚构
  - fiction-general
  - 小说
  intent_patterns: &id001
  - 因果链稳固
  - 人物弧光
  - 主题统一
  - 节奏控制
  sub_genres: []
core_challenges: *id001
specialist_agents:
- fiction-general-genre-lead
- story-arc-designer
- character-development-specialist
- narrative-pacing-manager
- theme-consistency-checker
- fiction-reader-simulator
- scene-causality-checker
- voice-continuity-editor
memory_extensions:
- story-arc
- character-arc
- theme-map
- promise-ledger
collaboration_mode: editorial-review
quality_focus:
- plot_causality
- character_depth
- theme_consistency
- pacing
- voice
composable_with:
- scifi
- textbook
- romance
- biography
---

# 通用虚构创作范式

## Core Engine

故事弧线 + 人物弧光 + 主题一致性，由**跨 genre 共享能力层**承载：

- 人物：`/trace-character-foundation`（本质溯源）→ `/name-character`（命名）→ `/design-character-arc`（八要素弧光）
- 情节：`/select-plot-engines`（12 引擎组合）
- 质量门：`/gate-anti-ai-prose`（反 AI 腔硬门）、`/revise-by-failure-mode`（失败模式分类修订）

方法论资产见 `capability-library/cross-genre/001-*.md`。本 Pack 的 skill/agent 是这些共享能力的 fiction-general 专属编排，不重复定义方法论。

## Creative Law

本 Pack 规定 `通用虚构` 项目的结构、记忆、质量度量和人审边界。共享六阶段流水线仍然适用，但每个阶段都必须读取本 Pack 的结构范式、读者画像和一致性规则，并消费上表共享能力。

## Shared Capabilities（消费的跨 genre 能力）

| 能力 | 共享 skill | 方法论资产 | 本 Pack 消费点 |
|---|---|---|---|
| 人物本质溯源 | /trace-character-foundation | 001-character-foundation-tracing | develop-character-arc 编排第一步 |
| 人物弧光八要素 | /design-character-arc | 001-character-arc-eight-elements | develop-character-arc 编排第三步 |
| 角色命名六维 | /name-character | 001-character-naming-six-dimensions | develop-character-arc 编排第二步 |
| 剧情引擎库 | /select-plot-engines | 001-plot-engine-library | design-story-arc 编排 |
| 反 AI 腔门 | /gate-anti-ai-prose | 001-anti-ai-prose-gate | draft-v3 后硬门 |
| 修订进化循环 | /revise-by-failure-mode | 001-revision-evolution-loop | review 阶段 |

## Required Human Decisions

- 确认该类型是否为 primary genre。
- 确认核心读者承诺。
- 确认 `editorial-review` 模式下列出的关键创作决策（人物核心创伤、立场选择、弧光类型）。

## Quality Focus

- `plot_causality`
- `character_depth`
- `theme_consistency`
- `pacing`
- `voice`

## Specialist Agents

- `fiction-general-genre-lead`: coordinates general fiction craft
- `story-arc-designer`: 调用 `/select-plot-engines` 设计故事结构
- `character-development-specialist`: 编排 `/trace-character-foundation` → `/name-character` → `/design-character-arc` 发展人物
- `narrative-pacing-manager`: manages pacing and rhythm
- `theme-consistency-checker`: checks thematic continuity
- `fiction-reader-simulator`: simulates fiction readers
- `scene-causality-checker`: checks scene-to-scene causality
- `voice-continuity-editor`: checks narrative voice continuity

## Reference Loading Map

每个 skill 只读本表所列最小 reference 集（配合 `.claude/docs/context-management.md` 的 Region-Read Protocol：Grep `^#{1,3} ` 锚点定位 → Read offset/limit 取段，不全文 cat）。`consistency-rules.yaml` / `quality-metrics.yaml` 只取该 skill 守的规则或指标对应段。

| Skill | Pack 内 reference（region-read 取段） | 项目真源 | 上游 skill 产出 |
|---|---|---|---|
| `/design-story-arc` | `structure-paradigm.yaml`、`templates/story-arc.yaml`、`consistency-rules.yaml`（结构相关段） | `constitution/brief.yaml`（读者承诺） | `/develop-character-arc`、共享 `/select-plot-engines` |
| `/develop-character-arc` | `templates/character-arc.yaml`、`consistency-rules.yaml`（人物相关段）、`quality-metrics.yaml`（`character_depth`） | `constitution/brief.yaml`、`registry/concepts.yaml` | 共享 `/trace-character-foundation`→`/name-character`→`/design-character-arc` |
| `/design-point-of-view` | `quality-metrics.yaml`（`voice`） | `constitution/brief.yaml`（代入对象） | `/develop-character-arc`、共享 `/select-plot-engines` |
| `/manage-narrative-pacing` | `structure-paradigm.yaml`、`consistency-rules.yaml`（节奏段：strand 断档 / hook 强度）、`quality-metrics.yaml`（`pacing` + `strand_balance`） | 当前草稿 | `/design-story-arc`、`/develop-character-arc` |
| `/map-scene-causality` | `consistency-rules.yaml`（`plot_causality_gap`）、`quality-metrics.yaml`（`plot_causality`） | 当前草稿 | `/design-story-arc`、`/develop-character-arc` |
| `/track-promise-payoff` | `consistency-rules.yaml`（`promise_broken`）、`structure-paradigm.yaml`（reader_promise track） | `constitution/brief.yaml`、`registry/promises.yaml`、`registry/foreshadowing.yaml` | `/design-story-arc`、`/map-scene-causality` |
| `/check-theme-consistency` | `consistency-rules.yaml`（主题相关段）、`quality-metrics.yaml`（`theme_consistency`） | `constitution/brief.yaml`（核心主题）、当前草稿 | `/design-story-arc`、`/develop-character-arc` |
| `/shape-symbol-motif` | `quality-metrics.yaml`（`theme_consistency`） | `constitution/brief.yaml`、当前草稿 | `/develop-character-arc`、`/track-promise-payoff` |
| `/style-enhancement` | `quality-metrics.yaml`（`voice`） | `style-corpus/style-anchor.yaml` | 共享 `/gate-anti-ai-prose` |
| `/simulate-fiction-reader` | `reader-profiles.yaml`（画像段）、`quality-metrics.yaml`（按各画像 `review_focus` 取段） | 当前草稿 + 上游档案 | 共享 `/multi-dim-feedback`、`/consensus-analysis`、`/fix-cascade` |

加载纪律：

- **最窄路由**：表中"Pack 内 reference"只取该 skill 守的规则/指标对应段（如 `/map-scene-causality` 只读 `plot_causality_gap` 一条，不读全 `consistency-rules.yaml`）。
- **真源优先**：项目真源冲突时按 `.claude/docs/writing-brief-spec.md` 的数据权重链取（constitution > registry > genre-memory > outline > drafts > research）。
- **上游按需**：上游 skill 产出按 region-read 取其交付物摘要段，不重载全文。
- **此表为先行模板**：romance / scifi pack 可按同构补各自 loading-map。
