---
name: "consensus-analysis"
description: "读者共识分析——S5 Review 第三步。跨所有 reader_reports 聚合 finding，分共识/分歧/孤立三档，severity 用投票聚合、action 用 coordination-rules 优先级裁定（不数人头）。产出 controversy_map.yaml，区分 taste/genre_law/factual，对立反馈标 needs_author_arbitration。把'几十条意见怎么决策'变成可解释的仲裁。不负责跑反馈（→ multi-dim-feedback）、不负责分流修复（→ fix-cascade）。"
category: "review"
---

# /consensus-analysis

## Purpose

multi-dim-feedback 产出 N 份 reader_reports 后，面临"意见爆炸"：N 个读者、每人若干 finding，如何决策？

本 skill 解决两个核心问题（详见 [reader-simulation-spec.md §9](../../docs/reader-simulation-spec.md)）：

1. **数人头 vs 讲道理**：纯数人头会让 taste 类吐槽（人多）压过 genre_law（人少）。本 skill 用**双轨**：severity 靠投票聚合（多少 reader 提到、严重度分布），但 action 靠 [coordination-rules.md](../../docs/coordination-rules.md) 的既定优先级裁定——constitution > genre critical > stage gate > reader promise > local style。taste（第5层）与 genre_law（第2层）冲突时，genre_law 赢，不数人头。

2. **分歧不可掩盖**：读者立场对立时（如认同型说好、怀疑型说烂），不能取平均。本 skill 分三档——consensus（≥70% 同向，直接进 fix-cascade）/ split（立场对立，标 needs_author_arbitration 人审）/ outlier（个别，默认 defer）。对立被显式记录进 `controversy_map.yaml`，满足 [review-report 规则](../../rules/review-report.md)"分歧必须汇总、不能掩盖"。

## 触发时机

S5 Review，multi-dim-feedback 之后、fix-cascade 之前。

前置：`review/reader_reports/` 已产出。

## Inputs

- `review/reader_reports/*.md`（全部 reader 反馈）
- `review/reader_pool.yaml`（reader 立场分布，用于判断 split）
- [coordination-rules.md](../../docs/coordination-rules.md) 优先级（action 仲裁依据）
- active Genre Pack 的 consistency-rules（判断 genre critical）

## Outputs

写入 `projects/<project-id>/review/controversy_map.yaml`：

- `findings_aggregated[]`：每个 topic 聚合条目，含 topic / dimension / severity_votes / consensus(consensus|split|outlier) / readers / conflicting_readers / arbitration_priority / action

schema 见 [reader-simulation-spec.md §9.1](../../docs/reader-simulation-spec.md)。

## Steps

1. 读全部 `reader_reports/`，按 topic（章节+问题点）聚合 finding。
2. **severity 投票**：对每个 topic，统计各 reader 的 severity 投票分布（如 `{high:3, medium:5, low:1}`），取加权 severity。
3. **分档**：
   - consensus：≥70% reader 同向（都批或都夸）→ 直接定 action
   - split：立场对立（认同型与怀疑型/敌意型相反）→ 标 `needs_author_arbitration`
   - outlier：个别 reader 提及 → 默认 defer，除非命中 genre critical
4. **action 优先级仲裁**：按 [coordination-rules.md](../../docs/coordination-rules.md) 优先级裁定 action——若 finding 命中 constitution/genre critical，优先级压过 reader 多数意见。
5. **区分 feedback_type**：taste 类归入 defer/reject 候选；genre_law/factual/craft 进入 fix-cascade 不同队列。factual 类标记留给 fix-cascade 软隔离。
6. 写 `controversy_map.yaml`。split + high/critical 的条目额外高亮，提示人审。
7. 记录到 `.history/events.jsonl`：共识数、分歧数、孤立数、需人审数。

## Quality Gates

- 每个聚合 topic 必须有 severity_votes 与 consensus 分档，不得只取多数意见掩盖分歧（[review-report 规则](../../rules/review-report.md)）
- split 档必须列出 conflicting_readers 双方，不得取平均或丢弃一方
- action 必须由优先级仲裁产出，不得纯数人头（[coordination-rules.md](../../docs/coordination-rules.md)）
- taste / genre_law / factual 必须分流标注，不得混为一谈（[review-report 规则](../../rules/review-report.md)）
- 命中 genre critical 的 finding 即使是 outlier 也须升级处理，不得 defer
- 若全部 finding 都是 consensus（无分歧）：自检 reader_pool 是否 stance 多样（全认同型会让 split 永不出现，是采样失败信号）

## Error Handling

- 若 reader_reports 缺失：报错指向 `/multi-dim-feedback`
- 若 reader_reports 只有 1-2 份：标注"样本不足，共识统计无意义"，建议回到 `/spawn-reader-panel` 增采
- 若某 topic 严重度投票完全分裂（critical vs low 各半）：强制标 split + needs_author_arbitration，不自动定 action
- 若 taste 类 finding 占比 >50%：标注"反馈偏 taste，结构性问题覆盖不足"，提示关注 genre_law/clarity 维度

## 关联

- 上游：`multi-dim-feedback` → **consensus-analysis**
- 下游：**consensus-analysis** → `fix-cascade`（按 action 分流修复）
- 规范：[reader-simulation-spec.md §9](../../docs/reader-simulation-spec.md)、[rules/review-report.md](../../rules/review-report.md)、[docs/coordination-rules.md](../../docs/coordination-rules.md)
- Agent：Lead Review（仲裁负责人）
- 人审：split + high/critical → needs_author_arbitration
- 否定边界：只聚合仲裁，不跑反馈（→ multi-dim-feedback）、不分流修复（→ fix-cascade）
