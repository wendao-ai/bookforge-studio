---
name: "spawn-reader-panel"
description: "读者面板生成——S5 Review 第一步。从 Genre Pack 的 reader-profiles 原型 + brief.target_readers 双源定义画像空间，用锚点+加权采样产出 20-30 个 reader instances（保证怀疑型/敌意型一定在场、去同质化），喂给 multi-dim-feedback。把'多视角读者反馈'从拍脑袋的 persona 变成可追溯的采样工程。不负责跑反馈（→ multi-dim-feedback）、不负责仲裁（→ consensus-analysis）。"
category: "review"
---

# /spawn-reader-panel

## Purpose

V3 初稿出来后、人工审校前，先把"谁来读这本书"这个问题工程化。

传统 beta reader 的痛点：人数少（5-15）、难覆盖边缘视角、全靠编辑人脉。而 LLM 直接"生成 100 个读者画像"会撞上三个工程问题——多样性坍缩（生成的画像高度同质）、噪声爆炸（100 份反馈无法决策）、成本失控。

本 skill 的解法是**画像空间 + 锚点加权采样**（详见 [reader-simulation-spec.md §5-6](../../docs/reader-simulation-spec.md)）：

- 定义可组合的维度空间（role / knowledge_level / reading_goal / stance / context / sensitivity_profile），而非固定个体清单。
- **双源**：role 与 sensitivity_profile 从 Genre Pack 原型锚定（保证类型合规 + 怀疑型在场），其余维度按 brief.target_readers 分布加权采样（贴合本书目标人群）。
- **锚点**：pack 每类原型至少各取 1 个 instance，设下限；**加权填充**覆盖边缘 stance 做压力测试；**hash 去重**防同质化。

产物 `reader_pool.yaml` 是整条 review 流水线的入口，被 multi-dim-feedback 逐个消费。

## 触发时机

S5 Review 阶段，V3 初稿就绪后。是 review 流水线的第一步，后续接 multi-dim-feedback。

前置：active Genre Pack 已加载、brief.yaml 的 target_readers 已定义。

## Inputs

- `projects/<project-id>/PROJECT.md` + `genre-context/active-pack.yaml`
- active Genre Pack 的 `reader-profiles.yaml`（画像原型来源）
- `constitution/brief.yaml` 的 `target_readers`（采样分布权重来源）
- V3 初稿清单（确定 review 范围；从 `drafts/chapters/*/v3_polished.md`）
- 作者指定的采样规模 N（默认 20-30）或边缘 stance 加重要求

## Outputs

写入 `projects/<project-id>/review/reader_pool.yaml`：

- `instances[]`：每个 reader instance 含 id / archetype / role / knowledge_level / reading_goal / stance / context / sensitivity_profile / weight / is_anchor
- `default_n`、`distribution_basis`、`sampled_at`、`genre`、可选 `batched`

完整 schema 见 [reader-simulation-spec.md §6.3](../../docs/reader-simulation-spec.md)。

## Steps

1. 加载 active Genre Pack 的 `reader-profiles.yaml`，提取所有画像原型（role + sensitivity_profile + 对应 expectations/sensitivities/delight/rejection）。
2. 读 `brief.yaml#target_readers`，解析目标读者的知识水平/阅读目的/场景分布，作为加权采样的权重依据。
3. **锚点采样**：pack 每类原型各生成 ≥1 instance（role 固定，knowledge_level/reading_goal/stance/context 按原型语义填充），标记 `is_anchor: true`。**必须含至少一个 stance=怀疑/敌意的锚点**（满足 [reader-profiles 规则](../../rules/reader-profiles.md)"必含挑剔型读者"）。
4. **加权填充**：剩余 `N - 锚点数` 个 instance，按 brief 分布加权采样，显式覆盖边缘 stance（怀疑/敌意），保证压力测试视角在场。
5. **去重**：对维度组合做 hash 去重，剔除高度同质的 instance；若去重后不足 N，回到步骤 4 补采。
6. 写 `review/reader_pool.yaml`，记录 distribution_basis 与 sampled_at。
7. 输出摘要：N 值、锚点数、stance 分布、是否覆盖怀疑/敌意型。记录到 `.history/events.jsonl`。

## Quality Gates

- 锚点覆盖 pack 每类原型，且**至少一个 stance=怀疑/敌意**——否则违反 [reader-profiles 规则](../../rules/reader-profiles.md)，重采
- stance 分布不能全为"认同"（全好评面板无压力测试价值）——认同型占比 ≤60%
- 去重后无高度同质 instance（维度组合 hash 无重复）
- `distribution_basis` 必须指向 `brief.yaml#target_readers`，不得凭空生成分布
- N 值落在配置区间（默认 20-30）；偏离须记录理由
- pack 原型字段（role/sensitivity_profile）必须忠实继承，不得自创 role

## Error Handling

- 若 brief.yaml 无 target_readers：停下，提示作者补 brief（不凭空假设读者分布）
- 若 active-pack 未加载 / reader-profiles 缺失：报错指向 `/detect-genre` 或 `/switch-genre`
- 若 pack 原型 <3 类（违反 reader-profiles 规则）：停下提示补 pack，不凑数
- 若作者要求 N 极大（如 100）：接受但强制分批（每批 ≤10 instance 出 review），并在 pool 标 `batched: true`
- 若无 V3 初稿：报错，本 skill 是 review 阶段技能，不适用于未完成初稿

## 关联

- 上游：`draft-v3-polish`（产出 V3 初稿）→ **spawn-reader-panel**
- 下游：**spawn-reader-panel** → `multi-dim-feedback`（逐个消费 instances）
- 规范：[reader-simulation-spec.md §5-6](../../docs/reader-simulation-spec.md)、[rules/reader-profiles.md](../../rules/reader-profiles.md)
- 类型数据：`genre-packs/<genre>/reader-profiles.yaml`
- Agent：Lead Review（review/ 的 owner，见 [coordination-rules.md](../../docs/coordination-rules.md)）
- 否定边界：只生成画像，不跑反馈（→ multi-dim-feedback）、不仲裁（→ consensus-analysis）
