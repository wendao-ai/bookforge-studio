---
genre_id: webnovel
genre_name: 网文连载
genre_family: fiction
maturity: stable
detection_signals:
  explicit_keywords:
  - 网文
  - 连载
  - 爽文
  - 追更
  - 追读
  - 起点
  - 番茄
  - 晋江
  - 每日更新
  - 金手指
  - 升级流
  - 打脸
  intent_patterns:
  - 追读力优先（留存生死线）
  - 爽点节奏峰谷
  - 黄金三章留存
  - 长篇连载（百万字级）
  - 订阅/月票/推荐驱动
  composes_with: [urban, scifi, romance, history, mystery]
sub_genres:
- 都市网文
- 玄幻网文
- 科幻网文
- 言情网文
- 悬疑网文
core_challenges:
- 追读力（留存生死线）
- 爽点节奏峰谷
- 水字控制（按字数付费易注水）
- 长线伏笔一致性（百万字易烂尾）
- 断更/烂尾风险
specialist_agents:
- webnovel-genre-lead
- reading-power-auditor
- coolpoint-designer
- pacing-controller
- serial-continuity-checker
memory_extensions:
- golden-finger
- escalation-track
- face-slap-ledger
- coolpoint-ledger
- foreshadowing-urgency
- reader-promise
collaboration_mode: serial-review
quality_focus:
- reading_power
- coolpoint_density
- micro_payoff_density
- strand_balance
- pacing
- water_content
composable_with:
- fiction-general
- scifi
- romance
- history
---

# 网文连载创作范式

## Core Engine

追读力经济学 + 黄金三章 + 卷划分爽点节拍，由**网文专属能力层**承载：

- 追读力：Hook（5类钩子）/ Cool-point（9类爽点套路）/ Micro-payoff（8类微兑现）/ Strand Weave（三线编织）/ 伏笔紧急度
- 节奏：黄金三章留存 / 爽点峰谷 / 卷末高潮
- 连载：每章独立可读 + 连续追读不懵 / 水字控制 / 长线伏笔不烂尾

## Creative Law

网文的核心契约是**追读**——每一章都必须给读者一个继续往下翻的理由。这要求：

1. **章末必有钩子**（Hook）——过渡章也必须有弱钩子，无钩子章 = 掉读者。
2. **每 2-3 章必有爽点兑现**（Cool-point）——连续 3 章无爽点 = 追读力红线。
3. **每章必有微兑现**（Micro-payoff）——即使过渡章，至少给读者 1 个小收获。
4. **三线编织不断档**（Strand）——Quest/Fire/Constellation 任一断档超红线 = 读者疲劳/流失。
5. **伏笔按紧急度回收**——core 伏笔逾期必回收，否则烂尾。

这五条是网文的"硬约束"，不是建议。

## 为什么独立成 pack（A/B 实测验证）

> 2026-07-11 A/B 实验（重生2008：大空头，Bookie vs webnovel-writer）实测：用 fiction-general（出版级通用虚构）写网文，产出在追读力/爽感/节奏/作者体验 4 维系统性弱于网文原生工具。根因：fiction-general 做了"出版级通用化"，剔除了纯网文套路（装逼打脸/迪化误解/扮猪吃虎）；而网文的爽点密度、黄金三章留存、卷划分节拍是独立创作范式。
>
> 本 pack 把 adoption-plan 阶段三剔除的 A2 纯网文套路 + 完整追读力经济学还回来，作为网文专精 pack。fiction-general 保留给"出版级通用虚构"（不追求网文爽感的文学向小说）。

本 pack 可与题材 pack 组合（都市网文 = webnovel + urban 元素；玄幻网文 = webnovel + 玄幻设定）。detection 时，若作者明确"网文/连载/爽文/追更"信号，优先用本 pack 驱动写作范式，题材元素从 composable_with 补。

## Required Human Decisions

- **金手指类型与代价边界**（网文的魂）——决定全书爽点机制，必人审。
- **主角灰度底线**——决定能写多狠、读者面。
- **全书卷划分与爽点里程碑**——init 阶段就要规划（网文百万字，无规划必烂尾）。
- **第一桶金/第一次大爽点的量级**——网文爽感校准（A/B 实测：Bookie 93 万偏保守，webnovel 387 万/27 倍更网文）。
- **感情线配置**（无女主/单女主/多女主）——影响读者面与 Fire strand 密度。

## Quality Focus

- `reading_power`（追读力综合）
- `coolpoint_density`（爽点密度）
- `micro_payoff_density`（微兑现密度）
- `strand_balance`（三线编织）
- `pacing`（峰谷节奏）
- `water_content`（水字控制）

## Specialist Agents

- `webnovel-genre-lead`: 统筹网文创作范式
- `reading-power-auditor`: 审计每章追读力（Hook/Cool-point/Micro-payoff/Strand 是否达标）
- `coolpoint-designer`: 设计爽点套路与峰谷节奏
- `pacing-controller`: 控制黄金三章/卷划分/爽点节拍
- `serial-continuity-checker`: 检查连载连贯（每章独立可读 + 长线伏笔不烂尾）
