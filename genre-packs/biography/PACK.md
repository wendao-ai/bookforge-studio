---
genre_id: biography
genre_name: 人物传记/回忆录
genre_family: nonfiction
maturity: stable
detection_signals:
  explicit_keywords:
  - 人物传记
  - 传记
  - 回忆录
  - biography
  - memoir
  - 人物生平
  intent_patterns: &id001
  - 传主真实生平
  - 事实与叙事分离
  - 多源交叉验证
  - 传主伦理边界
  - 人生阶段叙事权重
  sub_genres:
  - 他传（biography）
  - 自传/回忆录（memoir）
core_challenges: *id001
specialist_agents:
- biography-genre-lead
- biographer
- fact-checker
- subject-curator
- life-arc-designer
- biography-reader-simulator
memory_extensions:
- subject-archive
- life-timeline
- fact-narrative-map
- source-conflict-log
collaboration_mode: subject-ethics-gated
quality_focus:
- factual_accuracy
- narrative_arc
- source_traceability
- subject_ethics
- life_stage_weighting
composable_with:
- history
- fiction-general
---

# 人物传记/回忆录创作范式

## Core Engine

人物本质溯源 + 事实核查 + 叙事弧光

传记是 nonfiction，但核心是"人的故事"。它消费跨 genre 共享的人物能力（`/trace-character-foundation`、`/design-character-arc`、`/name-character`），但所有人物结论受**事实约束**——不能为戏剧性改变真实人物的"不可变区"特质。

传记专属增量（fiction-general 没有）：
1. **事实-叙事分离**：真实经历（fact，带 source + confidence）vs 叙事重构（narrative_reconstruction，显式标注）。critical。
2. **传主伦理边界**：授权状态/隐私/在世人物法律风险/敏感事件。critical 人审。
3. **多源记忆交叉验证**：访谈/档案/第三方回忆矛盾必须保留（对接 history 的 conflict_status），不得抹平。
4. **人生阶段-叙事权重映射**：童年/成长/成就/转折/晚年不平均分配，转折期权重最高。

## Shared Capabilities（消费的跨 genre 能力）

| 能力 | 共享 skill | 传记语境调整 |
|---|---|---|
| 人物本质溯源 | /trace-character-foundation | 溯源须基于真实资料，非虚构推导；产出标 confidence |
| 人物弧光八要素 | /design-character-arc | 弧光受事实约束，不可改真实人物不可变区特质；改了须标 narrative_reconstruction |
| 角色命名 | /name-character | 真实人名不改名，退化为"记录+解释烙印" |
| 剧情引擎 | /select-plot-engines | 引擎用于"如何组织真实事件"而非虚构情节 |
| 反 AI 腔门 | /gate-anti-ai-prose | 适用 |
| 修订进化循环 | /revise-by-failure-mode | 适用 |

## Creative Law

本 Pack 规定传记项目的结构、记忆、质量度量和人审边界。与 history pack 组合时，history 管史料核查与史观，本 pack 管传主人物弧光与伦理；与 fiction-general 组合时，fiction-general 管叙事技法，本 pack 管事实约束。

## Required Human Decisions

- 确认传主授权状态（在世/已故/家属授权/公共人物）。
- 确认事实-叙事分离边界（哪些事件可叙事重构、哪些必须严格据实）。
- 确认敏感事件/隐私边界处理方式。
- 确认多源矛盾的处理（保留争议 vs 采信一方并标注）。

## Quality Focus

- `factual_accuracy`
- `narrative_arc`
- `source_traceability`
- `subject_ethics`
- `life_stage_weighting`

## Specialist Agents

- `biography-genre-lead`: 协调传记方法与人审门
- `biographer`: 撰写传记正文，平衡事实与叙事
- `fact-checker`: 事实核查，守事实-叙事分离
- `subject-curator`: 策展传主资料（访谈/档案/第三方回忆）
- `life-arc-designer`: 设计人生弧光（受事实约束）
- `biography-reader-simulator`: 模拟传记读者（求知/共情/专业审视）
