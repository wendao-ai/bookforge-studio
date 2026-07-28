# 责编协作协议（Editorial Collaboration Protocol）

> 阶段：Phase 2 系统轨设计稿 | 制定日期：2026-07-02
> 状态：设计稿，待 ch04+ 写作期 + 人邮责编真实往返中验证
> 目标：让出版社责编的修改可被 Bookie 追踪、合并、回溯——不重造编辑器，复用 git。

## 1. 为什么需要这个协议

作者 V3 定稿 → 送编辑 → 责编批注/修改 → 作者接收 → 合并 → V4 → ... → 终稿。

当前 Bookie 的版本管理（V0-V3）是**作者单侧**的。责编的修改（在 docx / 纸质稿 / Word 批注里）进不了 Bookie 的版本链——作者手工合并，容易丢修改、难追溯、无法回放"编辑为什么这么改"。

出版社的核心价值之一就是"编辑协作"。Bookie 若不能接入责编协作，就只能停在"作者工具"，进不了出版社的生产链。

本协议把"责编-作者往返修改"产品化为 Bookie 的可追踪协作层。

## 2. 设计原则

- **不重造编辑器**：复用 git 的 diff / branch / merge，不建独立协作服务
- **接入现有编辑工具**：责编习惯用 Word / WPS / 批注 PDF，不强制改工具
- **协议层而非应用层**：定义"修改如何表达、追踪、合并"的规范，具体前端可选
- **append-only**：修订记录只增不改，可审计

## 3. 协议核心：三态修订模型

每次责编修改表达为三态：

- **base**：修改前的文本（对应 Bookie 的某版本，如 V3 的某节）
- **proposed**：责编建议的文本（带批注理由）
- **decision**：作者的决定（accept / reject / counter-propose）

修订记录格式（JSON Line，append-only，存 `review/editorial-revisions.jsonl`）：

```json
{
  "rev_id": "r001",
  "chapter": "ch03",
  "section": "3.2",
  "locator": "第 4 段第 2 句",
  "base_version": "v3_polished",
  "editor": "人邮责编A",
  "timestamp": "2026-07-15",
  "base_text": "...",
  "proposed_text": "...",
  "comment": "建议把'杀死'改为'拖垮'，更中性",
  "severity": "taste",
  "decision": "pending",
  "decided_at": null,
  "decided_by": null,
  "decision_reason": null
}
```

`severity` 分四档：`critical`（一致性/事实错误）/ `high`（逻辑/结构）/ `medium`（表达）/ `taste`（个人偏好）。critical/high 必须处理，taste 可批量 defer。

## 4. 协作流程（5 步）

1. **导出**：作者从 Bookie V3 导出 docx（带章节/段落标记），送责编
2. **批注**：责编在 docx 用 Word 修订/批注，返回
3. **导入**：Bookie 解析 docx 的修订/批注，转为 rev 记录（三态），写入 `editorial-revisions.jsonl`
4. **决策**：作者逐条 accept / reject / counter，decision 入库
5. **合并**：Bookie 按决策合并 accept 的修订，产出 V4（cp V3 + Edit，遵守 chapter-draft 版本规则）+ 修订日志

## 5. 与 Bookie 版本管理的衔接

- 责编一轮修改 = 一个新版本（V4 / V5...），遵守 [chapter-draft.md](.claude/rules/chapter-draft.md) 的 `cp + Edit` 规则
- 修订日志 = `dialogue_log.jsonl` 的子集（关键决策事件）+ `review/editorial-revisions.jsonl`（逐条记录）
- 责编修改若触及 critical 一致性（如 `vendor_exclusion_violation`），hook 自动检查并阻断合并

## 6. 实现路线（分阶段）

- **阶段 1（Phase 2，当前）**：协议规范（本文件）+ docx 修订解析原型（pandoc / python-docx）+ 简单合并。目标：人邮责编第一轮往返跑通
- **阶段 2（Phase 3 前段）**：批注可视化 + 冲突处理 + 多责编协同（大型项目有多个责编）
- **阶段 3（远期）**：独立协作服务（若出版社要 SaaS 形态）

## 7. 产品化价值（Bookie 的二号卖点）

| 卖点 | 对应环节 | 形态 |
|---|---|---|
| **选题论证**（[editorial-acquisition](.claude/skills/editorial-acquisition/SKILL.md) skill）| 前段·选题 | 把"编辑用 AI 做 V2"产品化（AI 责编）|
| **责编协作**（本协议）| 中段·写作+review | 把"责编-作者往返修改"产品化（可追溯协作层）|

两者合一，Bookie 就是一个覆盖"前段选题 + 中段协作"的出版社 AI 系统——这是面向出版社 B 端的核心价值主张。

## 8. 待决策（Phase 2 末确认）

| 待决策 | 选项 | 何时定 |
|---|---|---|
| 协作技术形态 | git-based 协议层 / 独立协作服务 / Word 插件 | Phase 2 末，看人邮责编工具习惯 |
| docx 解析方案 | pandoc / python-docx / 自研 | 阶段 1 原型时选 |
| 多责编协同 | 是否支持 + 冲突仲裁机制 | 阶段 2 |
| 与三审三校衔接 | 责编修改如何流入三审三校流程 | Phase 3 后段 |

## 9. 验证计划

ch03 样章送人邮责编后，第一轮真实往返即用于验证本协议：

- 责编返回的批注/修改，手动按三态录入 `editorial-revisions.jsonl`
- 跑一遍 5 步流程，找痛点（导入解析、决策 UI、合并冲突）
- 痛点反哺协议修订 + 阶段 1 实现

这一步同时推进书轨（ch03 责编往返）和系统轨（协议验证），是双轨策略的再一次落地。
