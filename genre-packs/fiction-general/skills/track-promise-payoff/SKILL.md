---
name: "track-promise-payoff"
description: "fiction-general 承诺-兑现追踪。建 promise-ledger（每个读者承诺的 origin/payoff_plan/fulfillment），逐章追踪兑现，守 promise_unpaid 规则。"
category: "fiction-general"
---

# /track-promise-payoff

## Purpose

确保每个读者承诺（情节钩子/伏笔/悬念/情感期待）有兑现或有意留白。建 promise-ledger 逐章追踪，防承诺悬空。

## Inputs

- `constitution/brief.yaml`（读者承诺）。
- `/design-story-arc` 的引擎钩子与升级。
- `/map-scene-causality` 的伏笔/物件追踪。
- `consistency-rules.yaml`（promise_unpaid high）、`structure-paradigm.yaml`（reader_promise track）。
- 当前草稿。

## Outputs

- `promise-ledger.yaml`：每条承诺含 id/origin（首次出现章节）/payoff_plan（计划兑现方式与章节）/fulfillment_status（unpaid/paid/deferred/rejected）。
- promise_unpaid 检查记录（high 违规出具修复计划）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 从 brief 读者承诺 + 大纲钩子 + 草稿伏笔，建 promise-ledger。
3. 每条承诺标 origin（首次出现）/payoff_plan（计划兑现方式与章节）/fulfillment_status。
4. 逐章更新 fulfillment_status：兑现→paid，有意留白→deferred（须说明理由），放弃→rejected（须人审）。
5. 检查 promise_unpaid：核心承诺未兑现且无 deferred 理由 = high 违规，出具修复计划。
6. 首尾呼应：开篇钩子/物件在结尾换意义（对接 `/shape-symbol-motif`）。
7. 记录决策。

## Quality Gates

- 每个承诺有 origin + payoff_plan + fulfillment_status。
- 核心承诺 100% 兑现或有意 deferred（标注理由）。
- 无悬空承诺（promise_unpaid）。
- 首尾呼应（开篇钩子结尾回响）。

## Error Handling

- 若核心承诺未兑现：标 promise_unpaid（high），出具修复计划，补兑现或显式 defer。
- 若兑现与 payoff_plan 不符：标 conflict，确认改兑现还是改计划。
- 若 rejected 承诺：须人审（放弃读者承诺是创作决策）。

## 关联

- 规则：promise_unpaid（high）/ track：reader_promise
- 协同：`/map-scene-causality`（伏笔/物件）、`/shape-symbol-motif`（首尾呼应）
- 素材：源 short-sci-fi-novel-writer continuity-and-quality（伏笔回收/首尾呼应）
