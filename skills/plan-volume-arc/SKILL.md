---
name: "plan-volume-arc"
description: "连载品类全书卷规划 — 触发场景：网文/系列书在 outline 选定后、扩展章节计划前，需要规划全书卷划分（卷数/卷名/章节范围/核心冲突/卷末高潮/跨卷钩子）+ 爽点里程碑 + 长线伏笔。单本书不用。不负责单章计划（归 /expand-chapter-plan）、不替 /synthesize-outline（消费它）、不写正文、关键决策（卷划分/结局/core 伏笔回收）人审。补 A/B 实测暴露的缺口：webnovel-writer init 就规划 5 卷 500 章，Bookie 流程重只做单段。"
category: "outline"
agents:
  - Lead Outline
inputs:
  - "constitution/brief.yaml + concept_tree.json（核心承诺/论点/边界）"
  - "outline/outline.yaml（已选定大纲）"
  - "active-pack 的 structure-paradigm.yaml（连载卷结构范式，如 webnovel 的 volume_structure）"
  - "active-pack 的 quality-metrics.yaml（爽点里程碑/卷末高潮阈值）"
  - "registry/promises.yaml + foreshadowing.yaml（长线承诺与伏笔）"
outputs:
  - "projects/<project-id>/outline/volume-arc.yaml（全书卷划分 + 爽点里程碑 + 长线伏笔规划）"
required_reviews:
  - internal: ["Lead Outline"]
  - client: never
duration_estimate: "20-40 分钟"
---

# /plan-volume-arc

## Overview

`/plan-volume-arc` 是 BookForge Studios 的**连载品类全书卷规划** skill。在 outline 选定后、扩展章节计划前，规划全书卷划分（卷数/卷名/章节范围/核心冲突/卷末高潮/跨卷钩子）+ 爽点里程碑 + 长线伏笔与承诺的跨卷节奏。

它补 A/B 实测暴露的缺口（rebirth-capital，2026-07-11）：webnovel-writer 的 `/webnovel-init` 阶段就规划了 5 卷 500 章 + 卷划分 + 爽点里程碑；Bookie 流程重，10 章就消耗大量前置精力，**没做全书卷规划**。对连载网文/系列书，init/outline 阶段的全书卷规划是刚需（百万字不烂尾的根基），本 skill 补上。

**仅连载品类启用**（active-pack 为 webnovel，或 brief 标注 serial/multi-volume）。单本书不用——`outline.yaml` 足够。

## 能力要求

### 必须能做的

1. **全书卷划分**：卷数 / 卷名 / 章节范围 / 核心冲突 / 中段反转 / 危机链 / 卷末高潮 / 跨卷钩子（消费 active-pack `structure-paradigm.yaml` 的 `volume_structure` required_fields）。
2. **爽点里程碑**：全书 N 个量级递增的大爽点（网文：第一桶金 / 第一次大收网 / 中段反杀 / 终局清算）；每个里程碑标所在卷 / 章范围 / 量级 / 消费的承诺。
3. **长线伏笔与承诺规划**：core 伏笔的跨卷埋设-回收节奏（哪卷埋、哪卷回收）+ reader-promise 的兑现节奏；标注 `enforce_in_prose`（哪些兑现必须在正文落地）。
4. **跨卷一致性检查**：升级线连续（不跳级不回退）/ 人物弧光跨卷承接 / Strand 配比跨卷平衡（Fire/Constellation 不得跨卷断档）/ core 伏笔回收不逾期。
5. **人审 gate**：卷划分 / 结局走向 / core 伏笔回收节点 必人审。

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| 单章计划 / 单卷章纲拆分 | `/expand-chapter-plan` |
| 大纲结构（单本书结构） | `/synthesize-outline`（本 skill 消费它） |
| 写正文 | `draft-v0` ~ `draft-v3` |
| 章节一致性审查 | `/review-chapter` |

## 必备上下文

按 Region-Read Protocol 加载：

- `outline/outline.yaml`（已选定大纲——本 skill 的上游）
- `constitution/brief.yaml` + `concept_tree.json`（核心承诺/论点/边界）
- active-pack 的 `structure-paradigm.yaml`（`volume_structure` 字段——卷结构范式）
- active-pack 的 `quality-metrics.yaml`（卷级阈值：爽点里程碑量级 / 卷末高潮）
- `registry/promises.yaml` + `foreshadowing.yaml`（长线承诺与伏笔）

## Steps

### Step 1: 确认连载品类 + 加载
- 确认 active-pack 是连载品类（webnovel 或 brief 标注 serial/multi-volume）。**单本书 → 提示不需要本 skill，退出**（不强制给单本书套卷结构）。
- 加载 outline.yaml + brief/concept_tree + active-pack 的 volume_structure 范式 + quality-metrics 卷级阈值。

### Step 2: 全书卷划分
- 基于大纲 + 题材，规划全书卷：
  - 卷数（网文 3-5 卷起步；系列书 2-3 卷；A/B 阶段可只规划已写卷 + 后续卷骨架）
  - 每卷字段（消费 active-pack `volume_structure.required_fields`）：volume_summary / core_conflict / mid_reversal（必填，无则写理由）/ crisis_chain（≥3 递增）/ volume_climax / cross_volume_hook（必须落到本卷最后一章章末）/ strand_plan / foreshadowing_plan / milestone_payoffs

### Step 3: 爽点里程碑
- 全书 N 个量级递增的大爽点。每个标：所在卷 / 章范围 / 量级（strong/medium）/ 消费的 reader-promise。
- 峰谷节奏：里程碑间允许低谷（但低谷卷也要有微兑现），不得长谷（连续卷无里程碑）。

### Step 4: 长线伏笔与承诺规划
- core 伏笔（如 F1 仇敌 / F2 金手指边界）的跨卷埋设-回收节奏：哪卷埋、哪卷回收、urgency 跨卷追踪。
- reader-promise 的兑现节奏：哪些承诺在哪卷 payoff。
- **标注 `enforce_in_prose`**（对接改造 2）：哪些兑现必须在正文落地（如"金手指代价必在 X 卷正文付"），交 `/review-chapter` 检查。

### Step 5: 跨卷一致性检查
- 升级线连续：主角能力/资源/地位跨卷承接，不跳级不回退（除非有剧情解释）。
- 人物弧光跨卷承接：wound/欲望驱动的行为变化跨卷延续。
- Strand 配比跨卷平衡：Fire/Constellation 不得跨卷断档（对接 webnovel strand_balance red_lines）。
- core 伏笔回收不逾期：跨卷 urgency 追踪。

### Step 6: 输出 + 人审 gate
- 写 `outline/volume-arc.yaml`：全书卷划分 + 爽点里程碑 + 长线伏笔规划 + 跨卷一致性检查结果。
- 人审 gate：卷划分 / 结局走向 / core 伏笔回收节点 必人审，记录进 `dialogue_log.jsonl`。
- 总状态（A15 四态：completed/partial/needs_user/failed）+ blocking_count。

## 运营规则

- **仅连载品类**：单本书不用（outline.yaml 足够）；强制给单本书套卷结构是过度工程。
- **消费而非重造**：消费 outline + active-pack structure-paradigm，不重做大纲。
- **战略层**：本 skill 做全书卷战略；单卷章纲拆分归 `/expand-chapter-plan`（战术层）。
- **关键决策人审**：卷划分 / 结局 / core 伏笔回收 不得自动定。
- **Region-Read**：长参照不全文 cat。

### 反模式（严禁）

- 给单本书强套卷结构（过度工程）。
- 重做大纲（消费 outline，不覆盖）。
- 自动定结局走向/core 伏笔回收（人审）。
- 卷规划与 outline 冲突（应回溯修 outline 或裁决）。
- 跳过跨卷一致性检查（连载烂尾的主因）。

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| 是否连载品类（单本书应退出） | 提示退出，不强制套卷 |
| 每卷是否含 volume_structure 全部 required_fields | 补缺字段 |
| 爽点里程碑是否量级递增 + 峰谷交替 | 调整里程碑排布 |
| core 伏笔是否标跨卷埋设-回收卷 | 补伏笔规划 |
| 升级线是否跨卷连续（不跳级） | 回 Step 5 修正 |
| 卷划分/结局/core 伏笔回收是否人审 | 阻断待人审 |
| enforce_in_prose 兑现是否标注（交 review-chapter） | 补标注 |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `/synthesize-outline` | 上游：消费其 outline.yaml |
| `/expand-chapter-plan` | 下游：消费 volume-arc.yaml 做单卷章纲拆分 |
| `/review-chapter` | 消费 volume-arc 的 enforce_in_prose 标注做正文兑现检查 |
| `/project-doctor` | doctor 体检连载项目时消费 volume-arc 判定卷进度 |

## 文件输出

- 全书卷规划：`projects/<project-id>/outline/volume-arc.yaml`
