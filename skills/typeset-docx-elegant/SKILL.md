---
name: "typeset-docx-elegant"
description: "把定稿全书 markdown 排版成「思源宋体+Georgia」风格的出版社投稿级 Word 文档 — 当书稿 V3+ 已通过 review、需发出版社编辑审阅或交付投稿时使用。不负责基础快速导出（由 export-docx 负责）、EPUB/PDF（由 export-epub/typeset-pdf 负责）、内容创作与审校（由 drafting/review 负责）。"
category: "typeset"
agents:
  - lead-typeset
inputs:
  - "drafts/chapters/*/v3_polished.md 或 v4_expanded.md（全书定稿成稿）"
  - "constitution/brief.yaml（书名/作者/副标题，进 front matter）"
  - "style-corpus/style-anchor.yaml（voice 已固化，确认无未决项）"
outputs:
  - "projects/<project-id>/typeset/<书名>_V<版本>_精排版.docx（投稿级 Word）"
  - "projects/<project-id>/typeset/reference.docx（可复用排版模板）"
required_reviews:
  - internal: ["lead-review"]
  - client: required
duration_estimate: "15-30 分钟"
---

# typeset-docx-elegant — 中文书稿精排版

## Overview

把 V3+ 全书 markdown 一键排版成「思源宋体 + Georgia」风格的出版社投稿级 Word。区别于 `export-docx`（基础快速导出），本 Skill 输出**精排**：专业中文字体、标题层级、段首缩进、页码、每章分页——直接可发编辑审阅 / 投稿。由 `lead-typeset` 主导（S6 排版阶段）。

## 排版规范（核心参数 · 思源宋体 + Georgia）

| 元素 | 中文字体 | 西文字体 | 字号 | 行距 | 对齐 | 其他 |
|---|---|---|---|---|---|---|
| 正文 Normal | 思源宋体 | Georgia | 10pt | 1.5 倍 | 两端对齐 | 段首缩进 2 字符 |
| 章 heading 1 | 思源宋体 | Georgia | 22pt | 1.0 倍 | 左 | 粗体 · 每章新页 |
| 节 heading 2 | 思源宋体 | Georgia | 15pt | 1.2 倍 | 左 | 粗体 |
| 小节 heading 3 | 思源宋体 | Georgia | 12pt | 1.2 倍 | 左 | 粗体 |
| 书名 Title | 思源宋体 | Georgia | 30pt | — | 居中 | 粗体 |
| 页边距 | — | — | — | — | — | 上下 3.5cm / 左右 3.0cm |
| 页码 | — | — | — | — | 居中 footer | PAGE 域 |
| 代码 Verbatim | — | Consolas | 11pt | — | — | — |

> 字体可替换（如出版社指定宋体/黑体）—— 改 reference 模板的 eastAsia/ascii 即可，其余流程不变。

## 能力要求

### 必须能做的

1. **剥元块整合全书**：去掉各章 header/footer 写作过程元信息（V4 改写说明 / review gate / 一致性检查），只留正文，按 ch01–ch13 + 后记顺序合并
2. **生成思源宋体+Georgia reference 模板**：正文 / 标题 / 书名各级字体字号行距 + 页边距 + 页码
3. **Pandoc `--reference-doc` 精排**：应用模板生成 docx（带目录）
4. **后处理双保险**：段落级首行缩进（firstLineChars=200）+ 每章分页符
5. **officecli + grep 验证**：字体 / 缩进 / 页码 / 分页 + 铁律闻道正文 = 0

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|---|---|
| 基础快速导出（默认 Pandoc，无精排） | `export-docx` |
| EPUB / PDF 排版 | `export-epub` / `typeset-pdf` |
| 内容创作、审校、补字 | `draft-v*` / `multi-dim-feedback` / `fix-cascade` |
| 风格 voice 规范制定 | `anchor-style` / `benchmark-corpus-research` |

## 必备上下文

产出前加载 / 确认：

- 全书定稿（V3+ 各章成稿，review 通过）
- `constitution/brief.yaml`（书名 / 作者 / 副标题 → front matter）
- 排版规范（本 SKILL「排版规范」表）
- 执行资产（`assets/`）：`build_book.py` / `reference_gen.py` / `post_process.py`

## Steps

### Step 1: 前置检查

- 确认 review 通过（`multi-dim-feedback` / `fix-cascade` 无未决 critical）
- 确认 V3+ 成稿（typeset-output rule：**只从 V3+ 导出**）
- 确认 Pandoc + python-docx 可用（缺则报告，不静默）

### Step 2: 整合全书 markdown（`assets/build_book.py`）

- 各章取最新版（v4 优先，否则 v3）
- 剥 header（到首个 `## `）+ footer（`V[0-9] 改写说明` / 一致性检查元块）
- 去掉 `## 章首引子` 小标题（保留引子正文）
- 每章前插分页符（raw openxml `<w:br w:type="page"/>`）
- 加 YAML 扉页（书名 / 副标题 / 作者 / 版本 / 日期）+ 出版交稿说明（内容简介 / 本版更新）
- 输出 `全书_V<版本>.md`

### Step 3: 生成 reference 模板（`assets/reference_gen.py`）

- 基于 Pandoc 默认 reference（`pandoc --print-default-data-file reference.docx > base.docx`，含全部样式）
- 设 Normal / Body Text / First Paragraph：思源宋体 + Georgia，10pt，1.5 倍，段首缩进 2 字符（firstLine=480 + firstLineChars=200）
- 设 Heading 1/2/3：思源宋体 + Georgia，22/15/12pt，粗体
- 设 Title：30pt 居中
- 页面 A4，页边距上下 3.5cm / 左右 3.0cm
- 页脚居中页码（PAGE 域）

### Step 4: Pandoc 生成 docx

```bash
pandoc 全书_V<版本>.md -o <书名>_V<版本>_精排版.docx \
  --toc --toc-depth=2 --metadata lang=zh-CN \
  --metadata toc-title="目录" --reference-doc=reference.docx
```

### Step 5: 后处理（`assets/post_process.py`）

- 给所有 Body Text / First Paragraph 段落加**段落级** firstLineChars=200（officecli 查段落级，样式层不够，需双保险）

### Step 6: 验证（officecli + grep）

- `view stats`：字体 = 思源宋体 + Georgia
- `view issues`：Format Issues（首行缩进缺失）应清零
- grep `styles.xml`：firstLineChars=200、eastAsia=思源宋体
- grep `document.xml`：分页符数、页码域
- **铁律**：grep 闻道正文 = 0

### Step 7: 交付确认

- `lead-typeset` 产出 → `production-director` 上报 → **client（作者）required** 审阅
- 文件命名：`<书名>_V<版本>_精排版.docx`

## 运营规则

- **只从 V3+ 导出**（typeset-output rule）
- **思源宋体 + Georgia 为默认**（出版社指定字体时改 reference 模板参数）
- **段落级 + 样式层双保险缩进**（officecli 查段落级，单样式层不够）
- **剥元块**：交付版不含写作过程元信息（V4 改写说明 / review gate）
- **缺引擎报告不静默**（typeset-output rule）
- **排版规范跨 genre 通用**：字体 / 字号 / 页边距对所有非虚构书稿一致；genre 差异化（结构 / voice / 案例）在内容层，由上游 drafting / review 保证——本 Skill 不按 genre 改排版字体

### 反模式（严禁）

- 从 V3 以下版本导出
- 用 Pandoc 默认字体（必须用思源宋体 + Georgia reference 模板）
- 缩进只设样式层（officecli 会报 missing，必须段落级双保险）
- 交付版含写作元块（review gate / 一致性检查）
- 静默跳过缺 Pandoc / python-docx

## Quality Gates

| 检查项 | 不通过的处理 |
|---|---|
| review 是否通过（无未决 critical） | 回 review，不排版 |
| Pandoc + python-docx 是否可用 | 报告缺引擎，不静默继续 |
| 字体是否 = 思源宋体 + Georgia（grep styles.xml） | 重生成 reference 模板 |
| 段落缩进 firstLineChars=200 是否设上（officecli issues 无 missing） | 跑 post_process.py |
| 铁律闻道正文 = 0（grep document.xml） | 回草稿修，不交付 |
| 元数据完整（title / author / version / date / source） | 补 front matter |
| 分页符数 = 章数 + 后记 | 重跑 build_book.py |
| client（作者）最终审阅通过（交付前） | 按反馈修订内容/排版后重排，再送审 |
| SKILL.md ≤ 500 行 | 拆 references/ |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|---|---|
| `draft-v3-polish` | 上游：提供 V3+ 成稿 |
| `multi-dim-feedback` / `fix-cascade` | 上游：review 通过门 |
| `export-docx` | 并列：基础导出（快速） vs 本 Skill 精排（投稿级） |
| `export-epub` / `typeset-pdf` | 并列：其他格式 |
| `anchor-style` | 上游参考：voice 规范（确保内容定稿） |

## 文件输出

默认位置：

- 精排 docx：`projects/<pid>/typeset/<书名>_V<版本>_精排版.docx`
- reference 模板：`projects/<pid>/typeset/reference.docx`（可复用）
- 整合 md：`projects/<pid>/typeset/全书_V<版本>.md`（中间产物）
- 执行脚本：`.claude/skills/typeset-docx-elegant/assets/{build_book,reference_gen,post_process}.py`
