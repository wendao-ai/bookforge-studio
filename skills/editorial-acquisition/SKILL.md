---
name: "editorial-acquisition"
description: "选题论证/编辑评审——模拟出版社编辑视角，对作者方案做五维检查 + 竞品矩阵 + 市场空白 + 体量/定价/风险，产出选题论证报告。把'编辑用 AI 做 V2'这件事产品化为 Bookie 的内建能力。"
category: "ideation"
---

# /editorial-acquisition

## Purpose

在 ideation 阶段引入"编辑视角的对手盘"，模拟出版社编辑对作者方案做选题论证。

避免作者方案与出版社期望脱节（体量失控 / 读者模糊 / 案例单一 / 理论过重 / 结构发散——这正是 ai-tob-endgame 项目人邮编辑 V2 反馈暴露的五大问题）。把"选题论证"从出版社一侧的人工环节，**前置为作者可自助触发的 AI 评审**。

这是 Bookie 面向出版社的核心产品化卖点——出版社买 Bookie，相当于买一个"AI 责编"。

## 触发时机

ideation 阶段，`finalize-constitution` 之后、`synthesize-outline` 之前。也可在 outline 完成后、送编辑前再跑一次。

## Inputs

- `constitution/brief.yaml`（作者方案：title / 读者 / promise / scope / target_length / genre / uniqueness）
- `outline/outline.yaml`（若已有大纲；可选）
- 资料底座信息（若基于已有资料库写书；可选）
- 品类基准库（体量/定价的品类甜区；见 `editorial-acquisition/category-benchmarks.yaml`，待建）
- 竞品数据库（可选；若无可联网检索或请作者补充）

## Outputs

- `review/editorial-acquisition-report.md`（选题论证报告），含：
  - **五维检查**（体量 / 读者聚焦 / 案例多元 / 视角鲜明 / 结构主线）逐维给具体证据 + pass/fail
  - **竞品矩阵**（同类书 × 定位 / 体量 / 视角 / 销量，至少 5 本）
  - **市场空白识别**（基于竞品矩阵找视角/赛道空白）
  - **体量/定价建议**（对标品类基准给区间，不拍脑袋）
  - **销售预测**（分渠道加总：行业人脉 / 科技媒体 / 社区 / 峰会 / 电商）
  - **风险标注**（体量压缩 🔴 / 案例脱敏 🟡 / 读者窄 🟢 等，区分高/中/低）
  - **立项可行性评分**（市场空白 / 内容基础 / 作者专业度 / 读者需求，各 ⭐1-5）
  - **决策建议**（接受 / 调整后接受 / 重做方向）

## Steps

1. 加载 brief/outline + 品类基准库（若无基准库，提示作者补建或指定品类）
2. **五维检查**：逐维对照（体量超品类 1.5×？读者通吃>2 类？案例集中于自有品牌？视角撞名撞位？结构平铺无主线？）—— 每维给具体证据，不空泛
3. **竞品扫描**：列同类书（≥5 本），标注每本的定位/体量/视角/销量
4. **市场空白识别**：基于竞品矩阵，找"市面都在讲 X，没人讲 Y"的视角空白
5. **体量/定价建议**：基于品类基准给区间（如经管书 16-25 万字 / ¥69-89）
6. **销售预测**：分渠道加总，给区间
7. **风险标注 + 可行性评分**：逐项标高/中/低；四维各打 ⭐1-5
8. **输出报告 + 决策建议**：明确"接受 / 调整后接受 / 重做方向"
9. 若建议"调整/重做"，记录到 `dialogue_log.jsonl` 并请作者确认

## Quality Gates

- 五维检查必须逐维给**具体证据**（引用 brief/outline 的具体字段），不空泛
- 竞品矩阵至少列 5 本同类书，每本带可查证的公开信息
- 体量/定价建议必须对标品类基准，**不拍脑袋**
- 风险标注必须区分高/中/低，且给应对
- 报告必须给明确的"接受/调整/重做"建议，不模糊
- 若方案与品类基准严重冲突，必须停下来请作者确认（不自动改方案）

## Error Handling

- 若无品类基准库：明确标注"建议补建 category-benchmarks.yaml"，不给盲估
- 若竞品数据不足：标注"需联网检索"或"需作者补充"，不编造
- 若作者方案与出版社期望（如品类甜区）冲突：停下来请作者确认以哪边为准，不自动改
- 若触发本 skill 但 brief 未完成：报错并指向 `finalize-constitution`

## 关联

- 资产来源：`capability-library/cross-genre/editorial-acquisition-patterns/001-renyou-v2-feedback.md`（选题论证五维检查的首次沉淀）
- 衔接：`finalize-constitution` → **editorial-acquisition** → `synthesize-outline`
- 产品化价值：本 skill 是 Bookie 面向出版社的核心卖点（"AI 责编"）
