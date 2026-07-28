---
name: audit-reading-power
description: 网文章节追读力四维审计（Hook/Cool-point/Micro-payoff/Strand）——触发场景：网文章节草稿完成后、卷末批量审查、或作者怀疑某段追读力不足时。输出追读力报告 + 红线违规清单。仅活动项目为 webnovel pack 时启用。
category: review
agents:
  - reading-power-auditor
inputs:
  - "drafts/chapters/<ch_id>/v*_*.md（待审章节）"
  - "registry/foreshadowing.yaml（伏笔紧急度）"
  - "genre-context/genre-memory/coolpoint-ledger（历史爽点峰谷）"
  - "genre-packs/webnovel/quality-metrics.yaml（阈值参照）"
outputs:
  - "review/reading-power/<ch_id>.md（追读力报告）"
---

# /audit-reading-power

## Overview

逐章审计网文追读力四维——Hook（章末钩子）/ Cool-point（爽点密度与峰谷）/ Micro-payoff（每章微兑现）/ Strand（三线断档），对照 `webnovel/quality-metrics.yaml` 阈值，输出追读力报告 + 红线违规。这是 webnovel pack 的核心审查 skill，补齐 Bookie 此前无网文追读力审计的缺口（A/B 实测发现）。

## Steps

### 1. 加载阈值与历史
- 读 `quality-metrics.yaml` 的 hook_quality / coolpoint_pattern / micro_payoff_density / strand_balance 阈值。
- 读 `coolpoint-ledger` 近 5 章，判断峰谷节奏。
- 读 `foreshadowing.yaml` 的 urgency。

### 2. Hook 审计（critical 维度）
- 检查章末是否有未解决问题/悬念/危机/反转驱动翻页。
- 无钩子 → 标 `no_hook_chapter`（critical）。
- 黄金三章（前 3 章）钩子强度要求加倍。

### 3. Cool-point 审计
- 本章是否有爽点兑现（9 类之一）。
- 结合 coolpoint-ledger 近 2 章，判断是否触发 `no_coolpoint_streak`（连续 3 章无爽点 = high）。
- 峰谷：是否双高断层或长谷。

### 4. Micro-payoff 审计
- 本章微兑现数（8 类）是否 ≥ per_chapter_min（网文 2）。
- 过渡章是否 ≥ transition_chapter_min（1）。

### 5. Strand 审计
- 本章推进了哪条线（quest/fire/constellation）。
- 结合历史，判断是否触发 `strand_gap`（fire_gap_max 8 / constellation_gap_max 10 / quest_consecutive_max 5）。

### 6. 输出报告
- 写 `review/reading-power/<ch_id>.md`：四维评分 + 红线违规清单（含 impact/repair）+ 总状态（completed/partial/needs_user/failed）。
- 红线违规文案取自 `consistency-rules.yaml`。

## Quality Gates
- 每条红线违规必须可追溯到 quality-metrics 阈值或 consistency-rules。
- 无钩子章（critical）必须阻断，不得静默放行。
- 报告必须给出总状态 + blocking_count。
