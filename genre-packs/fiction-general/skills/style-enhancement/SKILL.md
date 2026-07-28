---
name: "style-enhancement"
description: "fiction-general 风格增强。正向风格追求（情绪化/氛围感/画面感/真实质地/流畅性），消费 style-anchor 对标书风格，与 /gate-anti-ai-prose 互补（反AI门管硬禁令，本skill管正向追求）。消费 voice 指标。"
category: "fiction-general"
---

# /style-enhancement

## Purpose

提升正文正向风格质量——让文字有温度、场景有质感、画面可感、日常有说服力、推进流畅。与 `/gate-anti-ai-prose` 互补：反 AI 门管硬禁令（句式/词汇），本 skill 管正向风格追求。

## Inputs

- `style-corpus/style-anchor.yaml`（对标书解构产出的可机读风格锚：句长/术语密度/voice/开篇模板/排版）。
- `/gate-anti-ai-prose` 的扫描结果（已通过的硬门基线）。
- `quality-metrics.yaml`（voice）。
- 当前草稿。

## Outputs

- 风格增强建议：按维度的改写建议（情绪化/氛围感/画面感/真实质地/流畅性）。
- style-anchor 对齐报告（句长/术语密度/voice 偏差）。
- `.history/events.jsonl` 决策摘要。

## Steps

1. 确认 active pack 为 fiction-general。
2. 正向风格追求（去科幻化）：
   - 情绪化：文字有温度，情绪通过细节行为传递非修辞宣泄。
   - 氛围感：场景有气味、光线、质感。
   - 画面感：读者能在脑中看到画面。
   - 真实生活质地：日常细节有说服力，非抽象。
   - 流畅性：被推着读，想知道人物怎么了。
3. 避免反风格：空洞抒情/过度形容词堆砌/过度解释/过度哲学化/角色说教/伪文学腔/纯概念堆砌/模仿具体作者句式。
4. 消费 `style-anchor.yaml`：对齐句长 p50/p90、术语密度、voice（人称/语气/时态）、开篇模板、排版规范。
5. 与 `/gate-anti-ai-prose` 互补：反 AI 门已过基线后，本 skill 在其上做正向提升，不重复硬禁令检查。
6. 借鉴规则：借鉴对标书"功能"不复制"内容"（提取抽象优点，不模仿具体作者）；改变五维度（设定/关系/赌注/规则/结尾）中至少三个。
7. 记录决策。

## Quality Gates

- 正向风格五维度有提升（非仅过反 AI 门基线）。
- 对齐 style-anchor 的可机读字段（句长/术语密度/voice）。
- 无反风格（空洞抒情/过度形容词/伪文学腔等）。
- 不模仿具体作者句式。

## Error Handling

- 若无 style-anchor：报错指向 `/benchmark-corpus-research`（风格锚须由对标书解构产出，不凭空写）。
- 若风格与反 AI 门冲突：以反 AI 门硬禁令为准，本 skill 让步。
- 若对标书风格借鉴过度（可识别模仿）：标违规，按五维度改变规则重写。

## 关联

- 指标：voice / 协同：`/gate-anti-ai-prose`（硬门互补）、`/anchor-style`（style-anchor 落地）
- 上游：`/benchmark-corpus-research`（产出 style-anchor）
- 素材：源 short-sci-fi-novel-writer style-and-research（正向追求 + 借鉴功能不复制内容 + 五维度改变规则，去科幻化去银河奖特化）
