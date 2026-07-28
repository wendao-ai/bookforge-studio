---
name: "review-chapter"
description: "章节通用一致性审查（五维：设定/时间线/连贯/角色/逻辑）+ anti-AI 文笔终检 — 触发场景：章节草稿完成后、V2/V3 修订前、卷末批量审查、或作者怀疑一致性/AI 腔问题时。所有 genre 适用。不负责追读力审计（网文 pack 的 /audit-reading-power 负责 Hook/Cool-point/Micro-payoff/Strand）、不负责修复执行（归 /fix-cascade）、不替人审、不替 consistency-engine 的 critical 阻断裁判。"
category: "review"
agents:
  - Lead Review
inputs:
  - "drafts/chapters/<ch_id>/v*_*.md（待审章节）"
  - "registry/*.yaml（concepts/promises/foreshadowing 真源）"
  - "constitution/concept_tree.json（概念体系）"
  - "active-pack 的 consistency-rules.yaml + quality-metrics.yaml（genre-specific 审查参照）"
  - "前序章节摘要（.history/events.jsonl 或前章 v*_*.md，region-read）"
  - "shared-tooling/editorial-collaboration/author-glossary.json（报告术语降级）"
outputs:
  - "projects/<project-id>/review/chapter-review/<ch_id>.md（五维报告 + anti-AI 终检 + 总状态）"
required_reviews:
  - internal: never
  - client: never
duration_estimate: "5-15 分钟"
---

# /review-chapter

## Overview

`/review-chapter` 是 BookForge Studios 的**章节级通用一致性审查 + anti-AI 终检** skill。它对标 webnovel-writer 的 reviewer 五维（setting/timeline/continuity/character/logic）+ anti-AI 八癖终检，补齐 Bookie 此前无自带章节审查 skill 的缺口（2026-07-11 A/B 实测发现）。

它对一章草稿做五维一致性扫描 + AI 腔终检，输出可追溯的审查报告（每条违规带 severity/impact/repair），不修复、不替裁判、不替人审。所有 genre 通用；网文 pack 另有 `/audit-reading-power` 负责追读力四维（两者互补：本 skill 查"对不对/像不像 AI"，那个查"够不够爽/留不留得住"）。

## 能力要求

### 必须能做的

1. **五维一致性审查**（对标 webnovel-review reviewer）：
   - `setting`：设定一致性（与 registry/concept_tree/genre-memory 是否冲突）
   - `timeline`：时间线（事件时序、人物同时出现在两地、时间跨度矛盾）
   - `continuity`：叙事连贯（章首接续、跨章伏笔状态、依赖读者记忆的关键设定）
   - `character`：角色一致性（人设/动机/弧光是否突变，对照 concept_tree 与 genre-memory）
   - `logic`：逻辑（因果链、金手指边界、机械降神）
2. **anti-AI 八癖终检**：段末感悟闭环 / 副词滥用 / 角色同一反应 / 辩论赛式对话 / 情绪贴标签 / 信息均匀分布 / 安全着陆 / 展示后解释。
3. **违规分级**：按 active-pack 的 consistency-rules severity（critical/high/medium/low）+ 事实层/感性层分层（adoption-plan A8）。
4. **四态总状态**（adoption-plan A15）：completed/partial/needs_user/failed + blocking_count。
5. **修复导航**：每条违规带 impact/repair（取自 consistency-rules 的 repair 字段或 error-catalog），导航到 `/fix-cascade`。

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| 追读力审计（Hook/Cool-point/Micro-payoff/Strand） | `/audit-reading-power`（网文 pack 专属） |
| 修复执行 | `/fix-cascade` |
| critical 阻断裁判 | consistency-engine（hook + consistency-rules） |
| 关键创作决策（世界观/人设/论点） | 人审 |
| 读者反馈/质量评判 | `/multi-dim-feedback` / `/spawn-reader-panel` |

## 必备上下文

按 Region-Read Protocol 加载（Grep `^#{1,3} ` 锚点 → Read offset/limit，不全文 cat）：

- active-pack 的 `consistency-rules.yaml` + `quality-metrics.yaml`（审查参照，region-read 对应段）
- `registry/*.yaml` + `constitution/concept_tree.json`（真源）
- 前序章节摘要（.history/events.jsonl 最近事件，或前章末段）
- `shared-tooling/editorial-collaboration/author-glossary.json`（报告术语降级）

## Steps

### Step 1: 加载参照与真源
- 确认活动项目与 active-pack。
- region-read active-pack 的 consistency-rules（取该 pack 的规则集）+ concept_tree/registry（真源）。
- 读前序章节摘要（连贯审查需要）。

### Step 2: 五维一致性审查
逐维扫描，每维给 pass/warn/block + 证据（引用正文 + 冲突真源）：

| 维度 | 检查 | 典型违规 |
|---|---|---|
| setting | 与 registry/concept_tree/genre-memory 冲突 | 角色设定前后矛盾、世界法则冲突 |
| timeline | 事件时序、人物位置、时间跨度 | 时间回跳未标注、人物同时在两地 |
| continuity | 章首接续、跨章伏笔状态（读前章 summary + registry 开放环 current_status）、依赖记忆、key_numbers 一致 | 章首无锚点、伏笔状态丢失、量级突变 |
| character | 人设/动机/弧光突变 | OOC、无动机行为、弧光跳变 |
| logic | 因果链、金手指边界、机械降神 | 凭空开挂解局、因果断裂 |

**enforce_in_prose 兑现检查**（A/B 实测催生的关键步）：扫描 active-pack consistency-rules 中所有带 `enforce_in_prose` 字段的规则，逐条核验**正文是否实际兑现**（而非仅 registry/memory 登记）。典型检查：金手指代价是否在某章让主角在场景里真实付代价（不是 memory-schema 填了 cost 字段就过）；伏笔回收是否有正文兑现的回收场景（不是 registry 标 closed 就过）；承诺是否有 in-scene payoff。登记 ≠ 兑现——这是本 skill 与 consistency-engine 的分工：后者查状态登记，本 skill 查读者侧兑现。

**长程记忆联动（跨章连贯，连载品类）**：连载品类（webnovel/系列）审查时，continuity 维度额外检查（对标 webnovel serial-continuity-checker）：
- 读前 1-2 章 `drafts/chapters/<ch>/summary.md`（见 chapter-summary-spec），核验章首接续锚点对得上前章结尾
- 读 `registry/foreshadowing.yaml` 的 `current_status`，标出 `near_due`/`overdue` 的开放环（催回收，对接 foreshadowing_overdue 规则）
- 核验本章 `summary.key_numbers` 与前章一致（资金量级/等级不突变）
- 本章审查通过后，回写 registry 开放环的 `last_checked_chapter` + `current_status`

这让本 skill 承担 webnovel serial-continuity-checker 的跨章连贯职能，用"registry 开放环 + 章节摘要链"实现，不造 story-system 提交链。

### Step 3: anti-AI 八癖终检
逐癖扫描正文：

| AI 癖好 | 检查 |
|---|---|
| ① 段末感悟闭环 | "他终于明白…""这一刻他懂了"式总结 |
| ② 副词滥用 | 缓缓/淡淡/微微/静静地 高频 |
| ③ 角色同一反应 | 瞳孔微缩/心中一凛/倒吸凉气 滥用 |
| ④ 辩论赛式对话 | 对话像发言而非试探/打断/省略 |
| ⑤ 情绪贴标签 | "他感到愤怒"而非生理反应 |
| ⑥ 信息均匀分布 | 每段等长、无疏密节奏 |
| ⑦ 安全着陆 | 章末解决一切、无悬念 |
| ⑧ 展示后解释 | 先现象后立刻解释，不留悬念 |

### Step 4: 违规分级与聚合
- 每条违规映射到 active-pack consistency-rules 的 severity（critical/high/medium/low）。
- 事实层（setting/timeline/character OOC/逻辑）→ 可阻断；感性层（文笔/anti-AI 多数）→ 建议。
- 消费 override_rationale（adoption-plan A9）：medium/low 违规若作者已记录理由，标"带理由继续"，但仍记档。

### Step 5: 输出四态报告
- 写 `review/chapter-review/<ch_id>.md`：五维表 + anti-AI 终检表 + 违规清单（severity/impact/repair/证据）+ 总状态 + blocking_count + 修复导航。
- 总状态规则：`completed`（0 blocking）/ `partial`（有 medium/low）/ `needs_user`（有 high 待裁决或关键决策）/ `failed`（有 critical）。
- 报告文案经 author-glossary 降级。

## 运营规则

- **纯只读**：不改章节草稿，只写自身的 `review/chapter-review/<ch_id>.md`。
- **消费而非重造**：每条违规必须可追溯到某条 consistency-rule 或 anti-AI 癖好，不发明新标准。
- **不替裁判**：标"待处理"是建议；critical 的阻断判定归 consistency-engine。
- **不替人审**：发现关键决策冲突（人设/世界观）时引导人审，不代决。
- **region-read**：长参照文件不全文 cat。
- **与 audit-reading-power 互补不重叠**：本 skill 查一致性 + AI 腔（所有 genre）；那个查追读力（网文）。

### 反模式（严禁）

- 自动修复发现的违规（审查只报告，修复归 `/fix-cascade`）。
- 把追读力检查混进本 skill（追读力归 `/audit-reading-power`）。
- 凭主观"感觉不好"开违规（每条必须有规则/癖好依据 + 正文证据）。
- 跳过 anti-AI 终检（它是 A/B 实测的关键缺口修复点）。
- 报告甩工程术语而不经 author-glossary 降级。

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| 每条违规是否可追溯到 consistency-rule 或 anti-AI 白好 + 正文证据 | 删除无依据违规 |
| 五维是否全部覆盖（setting/timeline/continuity/character/logic） | 补缺维 |
| anti-AI 八癖是否全部扫描 | 补缺癖 |
| 是否纯只读（除报告外无章节修改） | 移除写操作 |
| 是否含四态总状态 + blocking_count | 补总状态 |
| critical/high 违规是否标注事实层/感性层 | 补分层 |
| 带 `enforce_in_prose` 的规则是否逐条核验正文兑现（非仅登记） | 回 Step 2 补兑现检查 |
| 报告术语是否经 author-glossary 降级 | 替换工程术语 |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `/audit-reading-power`（网文 pack） | 互补：本 skill 查一致性+AI腔（全 genre），那个查追读力（网文） |
| `/fix-cascade` | 本 skill 发现 high/critical 时，导航到 fix-cascade 修复 |
| `/multi-dim-feedback` / `/spawn-reader-panel` | 它们做读者质量评判；本 skill 做客观一致性审查 |
| consistency-engine（hook + consistency-rules） | 本 skill 消费 rules 做审查，不替代 critical 阻断裁判 |
| `/project-doctor` | doctor 汇总一致性遗留时，消费本 skill 的 chapter-review 报告 |

## 文件输出

- 章节审查报告：`projects/<project-id>/review/chapter-review/<ch_id>.md`
