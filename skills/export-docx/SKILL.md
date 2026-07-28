---
name: "export-docx"
description: "把 V3+ 章节草稿（markdown）导出为 DOCX（送编辑/审阅/投稿用）。用 pandoc 生成，保留标题/表格/加粗/列表结构。Bookie 导出能力第一环。"
category: "typeset"
---

# /export-docx

## Purpose

把 V3+ 章节草稿（markdown）导出为 DOCX，用于送编辑 / 审阅 / 投稿。

打通"作者侧 markdown 创作"与"出版社侧 Word 工作流"——责编习惯在 Word 里用修订/批注，DOCX 是送编辑的标准形态。这是 Bookie "导出可用"能力的第一环（DOCX → EPUB → PDF 中的 DOCX），也是 Bookie 接入出版社生产链的接口。

## Inputs

- 章节草稿：`drafts/chapters/<ch>/v3_polished.md` 或更新版本（typeset-output rule：**只从 V3+ 导出**）
- frontmatter：YAML 元数据（导出时进 docx 文档属性，不显示在正文）
- 可选：reference-doc 模板（`.docx` 样式模板，用于品牌化排版；Phase 3 样式优化时引入）

## Outputs

- `typeset/<chapter-id>-<version>-sample.docx`（送编辑用 DOCX）

## Steps

1. **前置检查**：
   - 确认源版本 ≥ V3（v3_polished 或更新）；低于 V3 报错（typeset-output 强制）
   - 确认 pandoc 可用（`which pandoc`）；缺失则产出清晰报告（不静默失败）
2. **准备输出目录**：`mkdir -p typeset/`
3. **导出**（pandoc）：

   ```bash
   pandoc drafts/chapters/<ch>/<version>.md \
     -o typeset/<chapter-id>-<version>-sample.docx
   ```

   可选（品牌化排版）：`--reference-doc=<template.docx>`

4. **验证**：
   - 文件生成（`ls typeset/`）
   - 反向校验内容完整：`pandoc typeset/<out>.docx -t plain | head -50`
5. **记录**：导出事件追加到 `dialogue_log.jsonl`

## Quality Gates

- 只从 V3+ 导出（typeset-output 强制）；低于 V3 必须报错，不降级
- pandoc 缺失时产出清晰报告（含安装指引），**不静默失败**（typeset-output 强制）
- 导出后必须验证：文件存在 + 反向校验内容完整（不丢表格/标题）
- frontmatter 元数据进文档属性，不污染正文
- 表格 / 加粗 / 列表 / 引用块结构必须保留（pandoc 默认支持，但要校验）

## Error Handling

- **pandoc 未装**：报错 + 安装指引（macOS: `brew install pandoc`；Ubuntu: `apt install pandoc`）；不 fallback 到手动复制粘贴
- **源版本 < V3**：报错 + 指向 V3 修订流程
- **frontmatter 非标准字段**：pandoc 默认忽略，不报错（chapter_id / version 等进不了 docx metadata，但无害）
- **表格/图片异常**：pandoc 警告时记录到日志，继续导出（送编辑用，可人工修）
- **路径含空格/中文**：用双引号包裹路径

## 实战参数（ai-tob-endgame ch03 首次跑通，2026-07-02）

- pandoc 版本：3.9.0.2（macOS homebrew）
- 命令：`pandoc v3_polished.md -o ch03-v3-sample.docx`
- 结果：47 KB docx，标题 / 表格（横向对比表 / 分层表 / 诊断模板）/ 加粗 / 列表 / 引用块全部保留；frontmatter 进文档属性（正文干净）
- 用时：< 1 秒

## 关联

- 规则：[typeset-output.md](.claude/rules/typeset-output.md)（DOCX 用 pandoc + 只从 V3+ 导出 + 引擎缺失不静默）
- 配套 skill：`export-epub`（同样 pandoc，可复用本 skill 模式）/ `typeset-pdf`（Typst/LaTeX，Phase 3）
- 下一步优化（Phase 3）：reference-doc 模板（人邮经管书风格：封面 / 页眉页脚 / 正文字体 / 标题样式），让 docx 从"可读"升级到"接近出版形态"
