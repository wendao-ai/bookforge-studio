---
name: "multi-dim-feedback"
description: "多维读者反馈——S5 Review 第二步。逐个 reader instance 从自身定位出发，对 V3 初稿跑五维反馈（reader_promise/genre_law/craft/clarity/risk，维度随类型化），同时收批评与夸奖，每条带 evidence/confidence/feedback_type。把'有趣/准确/错别字/逻辑'这类泛化评价落到类型专属、可仲裁的结构化证据。不负责采样（→ spawn-reader-panel）、不负责聚合（→ consensus-analysis）。读者对事实的判断封顶 confidence=inferred（软隔离前置，详见 fix-cascade）。"
category: "review"
---

# /multi-dim-feedback

## Purpose

spawn-reader-panel 产出 reader_pool 后，让每个 reader instance 真正"读"V3 初稿并给反馈。

这一步解决两个问题：

1. **维度泛化**：用户直觉里的"有趣/准确/错别字/逻辑"是跨类型通用的模糊词。本 skill 把它落到五维框架，且**每维挂类型专属子项**——非虚构查论证链/证据强度，教材查前置依赖/布鲁姆层级，科幻查世界观一致性/技术代价。一套通用维度跑所有书会漏类型硬伤。
2. **只有批评没有结构**：传统 review 容易只剩"哪里不好"。本 skill 同时收 `verdict: positive`（命中 delight_triggers 的打动点），回答"哪些角度能打动目标读者"。

每条反馈强制带 `evidence`（具体段落/引文）、`confidence`（observed/inferred/speculated）、`feedback_type`（taste/genre_law/factual/craft）。空泛评语（"文笔流畅"）违反 [review-report 规则](../../rules/review-report.md)，一律 reject。

**准确度边界**：读者对事实/准确性的判断，confidence 封顶 `inferred`，并标 `feedback_type: factual`——这是软隔离的前置标记，fix-cascade 据此禁止自动修改原文（详见 [reader-simulation-spec.md §8](../../docs/reader-simulation-spec.md)）。读者可以指出"这里可疑"，但不能坐实对错。

完整机制见 [reader-simulation-spec.md §7](../../docs/reader-simulation-spec.md)。

## 触发时机

S5 Review，spawn-reader-panel 之后、consensus-analysis 之前。

前置：`review/reader_pool.yaml` 已生成、V3 初稿就绪。

## Inputs

- `review/reader_pool.yaml`（reader instances）
- V3 初稿：`drafts/chapters/<ch_id>/v3_polished.md`
- active Genre Pack 的 `consistency-rules.yaml`（genre_law 维度的子项来源）+ `quality-metrics.yaml`（craft 维度子项来源）
- `constitution/brief.yaml` 的 core_promise（reader_promise 维度锚点）
- `registry/`（promises/concepts，用于核对承诺兑现）

## Outputs

写入 `projects/<project-id>/review/reader_reports/<reader_id>.md`，每份含：

- reader instance 摘要（role/stance/knowledge_level...）
- 五维评分（每维 1-5 + 评语）
- 逐条 findings，每条字段：dimension / sub_item / severity / feedback_type / confidence / verdict / evidence / comment / suggested_fix
- 整体 verdict + 该 reader 最打动点 + 最拒斥点

finding 字段 schema 见 [reader-simulation-spec.md §7.2](../../docs/reader-simulation-spec.md)。

## Steps

1. 读 `reader_pool.yaml`，对每个 instance：按其维度组合（role×stance×knowledge_level×reading_goal）确定评价标尺——怀疑型专家读者的标尺 ≠ 认同型入门读者。
2. 加载 pack `consistency-rules.yaml` + `quality-metrics.yaml`，确定本类型的五维子项（如非虚构 clarity 查 argument_chain/concept_order）。
3. **逐 instance 跑五维反馈**：对 reader_promise / genre_law / craft / clarity / risk 逐维，结合该 reader 的 sensitivity_profile 找问题与亮点。
4. **同时收 positive 与 negative**：positive = 命中 delight_triggers 的打动点；negative = 命中 rejection_triggers 的拒斥点。两者都要 evidence。
5. **强制打标**：每条 finding 必填 evidence（章节+定位+引文）；事实/准确性相关 finding 强制 `feedback_type: factual` + `confidence: inferred`（封顶）。
6. **reject 空泛评语**：无 evidence、无具体段落的反馈（"写得很好""逻辑混乱"无定位）一律剔除，不进报告。
7. 写 `review/reader_reports/<reader_id>.md`。若 reader_pool 标 `batched: true`，分批产出（每批 ≤10）。
8. 汇总各 report 的 finding 计数，记录到 `.history/events.jsonl`。

## Quality Gates

- 每条 finding 必须有 evidence（章节 + 定位 + 引文），空泛评语一律 reject（[review-report 规则](../../rules/review-report.md)）
- 五维子项必须随类型化（引用 pack consistency-rules/quality-metrics），不得用一套通用维度跑所有类型
- 每个 report 必须同时含 positive 与 negative verdict（只有批评或只有夸奖都失衡）
- factual 类 finding 的 confidence 必须 ≤ inferred，不得 observed（软隔离前置）
- severity 必须落在 critical/high/medium/low 四级（对齐 [consistency-engine-spec.md](../../docs/consistency-engine-spec.md)）
- 怀疑型/敌意型 reader 的报告必须有实质 negative finding（否则该 reader 形同虚设）

## Error Handling

- 若 reader_pool.yaml 缺失：报错指向 `/spawn-reader-panel`
- 若 V3 初稿缺失某章：标注该章 `coverage: missing`，不编造反馈
- 若 pack 无 consistency-rules/quality-metrics：降级为通用五维，并在 report 标注 `type_specific_coverage: partial`
- 若某 reader instance 维度组合无法生成有效 finding：保留该 reader 但标 `yield: low`，不硬凑
- 若 factual finding 数量异常多（占比 >40%）：标注"事实密度高，建议优先排 expert"，提示 fix-cascade 关注 factual_pending_expert 队列

## 关联

- 上游：`spawn-reader-panel` → **multi-dim-feedback**
- 下游：**multi-dim-feedback** → `consensus-analysis`（聚合所有 reports）
- 规范：[reader-simulation-spec.md §7](../../docs/reader-simulation-spec.md)、[rules/review-report.md](../../rules/review-report.md)
- 类型数据：`genre-packs/<genre>/consistency-rules.yaml`、`quality-metrics.yaml`、`reader-profiles.yaml`
- Agent：Lead Review 统筹（review/ owner）；reader 模拟由其调度的 specialist 执行——reader simulator 是职能角色，非独立 agent 文件（归属见 [coordination-rules.md](../../docs/coordination-rules.md)）
- 否定边界：只跑单 reader 反馈，不采样（→ spawn-reader-panel）、不跨 reader 聚合（→ consensus-analysis）、不改原文（→ fix-cascade）
