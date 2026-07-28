---
name: "fix-cascade"
description: "修复级联——S5 Review 第四步（收口）。把 controversy_map 的 finding 按 severity×feedback_type 分流到 revise/defer/reject，critical 触发 backtrack，factual 类走软隔离（强制 auto_fix=false + needs_expert_review，专家升级前绝不自动改原文）。产出 fix-cascade-plan.yaml，factual_pending_expert 队列非空则 S5 不允许 clean exit。把'意见→修复'闭环，且防住'读者投票把对的改错'。不负责跑反馈/仲裁（上游）。"
category: "review"
---

# /fix-cascade

## Purpose

consensus-analysis 产出 controversy_map 后，每条 finding 必须有明确去向——否则意见悬空、初稿无法进入排版。本 skill 是 review 流水线的收口（详见 [reader-simulation-spec.md §10](../../docs/reader-simulation-spec.md)）。

核心职责：

1. **分流**：按 severity（critical/high/medium/low）× feedback_type（factual/genre_law/craft|clarity/taste）映射到 action——revise / defer / reject / needs_review / backtrack。taste 类默认 reject/defer，不消耗修订预算。

2. **backtrack**：critical 的 genre_law/craft 问题不只在当前章节改，而是回溯到最早引入矛盾的 artifact（draft → chapter plan → outline → constitution），由 Director 层定 revise 范围（[consistency-engine-spec.md](../../docs/consistency-engine-spec.md) backtrack protocol）。

3. **准确度软隔离（关键护栏）**：factual 类 finding 强制 `auto_fix: false` + `needs_expert_review: true` + `expert_status: pending`，进独立分组 `factual_pending_expert`。**专家升级为 observed 前，任何情况都不自动改原文**——即使多数 reader 一致指出同一"事实错误"。一致性 ≠ 正确性。这是防止"读者投票把对的改错"的核心机制（[reader-simulation-spec.md §8](../../docs/reader-simulation-spec.md)）。

## 触发时机

S5 Review 收口，consensus-analysis 之后。fix-cascade-plan 落定后，S5 才能进入 S6 Typeset。

前置：`review/controversy_map.yaml` 已产出。

## Inputs

- `review/controversy_map.yaml`（待分流的聚合 finding）
- [consistency-engine-spec.md](../../docs/consistency-engine-spec.md)（severity 定义 + backtrack protocol）
- [three-tier-confidence.md](../../docs/three-tier-confidence.md)（expert 升级 observed 的判据）
- active Genre Pack 的 consistency-rules（判断 critical）
- 专家审核结果（若已有；否则 factual 进 pending 队列）

## Outputs

写入 `projects/<project-id>/review/fix-cascade-plan.yaml`：

- `items[]`：每条修复项含 id / topic / source_readers / severity / feedback_type / action / target_artifact / auto_fix / needs_expert_review / expert_status / owner
- `factual_pending_expert[]`：factual 类待专家确认（软隔离队列）
- `deferred[]` / `rejected[]`：显式记录，不丢失

schema 见 [reader-simulation-spec.md §10.3](../../docs/reader-simulation-spec.md)。

## Steps

1. 读 `controversy_map.yaml`，对每个 finding 按 severity×feedback_type 查分流表（[spec §10.1](../../docs/reader-simulation-spec.md)）定 action。
2. **factual 软隔离**：所有 feedback_type=factual 的项，强制写 `auto_fix: false` + `needs_expert_review: true` + `expert_status: pending`，归入 `factual_pending_expert` 分组。**跳过此步 = 放弃软隔离护栏，禁止。**
3. **critical backtrack**：severity=critical 的 genre_law/craft 项，识别最早引入矛盾的 artifact（沿 draft → chapter plan → outline → constitution 回溯），标 backtrack 范围，提请 Director 层（Editorial Director / Production Director）+ 人审。
4. **taste 清理**：feedback_type=taste 的项默认 reject 或 defer，归入对应分组，不进 revise。
5. **owner 分配**：每条 revise 项分配 owner（Lead Drafting / Genre Strategy Director / 人类专家）。
6. 写 `fix-cascade-plan.yaml`，含 factual_pending_expert / deferred / rejected 完整分组。
7. **exit gate 检查**：若 `factual_pending_expert` 非空，S5 标记 `exit_blocked: factual_pending`——要么 expert 处理，要么作者显式 defer 并在 events.jsonl 记理由。
8. 记录到 `.history/events.jsonl`：revise/defer/reject/pending 计数、是否 exit_blocked。

## Quality Gates

- 每条 finding 必须有明确 action（revise/defer/reject/needs_review/backtrack），不得悬空（[review-report 规则](../../rules/review-report.md)）
- factual 类必须 `auto_fix: false` + `needs_expert_review: true`——**违反则该计划无效**，必须回退重分流
- critical 必须触发 backtrack 或人审，不得降级为 medium 静默放行（[consistency-engine-spec.md](../../docs/consistency-engine-spec.md)）
- taste 类不得进入 revise（不消耗修订预算于个人偏好）
- `factual_pending_expert` 非空时必须标 `exit_blocked`，不得 clean exit
- high/critical revise 项必须经人审后才执行（[human-collaboration-modes.md](../../docs/human-collaboration-modes.md)）
- expert 已确认"读者指错但实际正确"的项须 reject 但保留记录（供 `harvest-writing-pattern` 沉淀）

## Error Handling

- 若 controversy_map.yaml 缺失：报错指向 `/consensus-analysis`
- 若 expert 长期缺席（factual_pending 积压）：标 `exit_blocked`，提示作者安排 expert 或显式 defer，不自动修
- 若 critical backtrack 涉及 constitution 改动：强制人审 + 记录 decision event（[human-collaboration-modes.md](../../docs/human-collaboration-modes.md)），不自动改宪法
- 若 revise 项的 target_artifact 不存在：标注 `target_missing`，不编造路径
- 若同一 topic 同时有 factual 与 genre_law 判断：分别进各自队列，不合并

## 关联

- 上游：`consensus-analysis` → **fix-cascade**
- 下游：**fix-cascade** → revise 执行（回到 `draft-v*` 对应版本）/ `typeset-pdf`·`export-docx`（exit gate 通过后）
- 规范：[reader-simulation-spec.md §8、§10](../../docs/reader-simulation-spec.md)、[docs/consistency-engine-spec.md](../../docs/consistency-engine-spec.md)、[docs/three-tier-confidence.md](../../docs/three-tier-confidence.md)、[docs/human-collaboration-modes.md](../../docs/human-collaboration-modes.md)、[rules/review-report.md](../../rules/review-report.md)
- Agent：Lead Review（分流）+ Director 层（Editorial Director / Production Director，定 backtrack 范围）；factual 升级由人类专家完成（expert-reviewed 模式，见 [human-collaboration-modes.md](../../docs/human-collaboration-modes.md)）
- 沉淀：项目结束后由 `harvest-writing-pattern` 把有效的 fix 模式沉淀到 `capability-library/`
- 否定边界：只分流修复计划，不执行 prose 改写（→ draft-v*）、不跑反馈/仲裁（上游）
