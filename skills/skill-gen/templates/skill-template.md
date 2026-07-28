# Skill 标准模板

> 这是 BookForge Studios Skill 的标准骨架。生成新 Skill 时，基于 Phase 2（定位）和 Phase 3（关联）的结果填入具体内容。

---

## frontmatter 模板

```yaml
---
name: "<skill-name>"
description: "<一句话核心价值> — <触发场景说明>。不负责 <否定边界>（由 <现有Skill> 负责）。"
category: "<category>"
agents:
  - <agent-role-1>
  - <agent-role-2>
inputs:
  - <输入文件或数据 1>
  - <输入文件或数据 2>
outputs:
  - <输出文件 1>
  - <输出文件 2>
required_reviews:
  - internal: ["<reviewer-agent-1>"]
  - client: <required | optional | never>
duration_estimate: "<时间预估>"
---
```

## body 骨架

```markdown
# <Skill 标题>

## Overview

<一段话说明这个 Skill 的核心价值和在 BookForge Studios 系统中的位置。>

## 能力要求

### 必须能做的

1. **<能力名称 1>**
   - 具体能力描述
   - 包含量化标准（如有）

### 明确不做的（由其他 Skill 负责）

| 不负责 | 由谁负责 |
|--------|---------|
| <边界 1> | `<现有Skill>` |

## 必备上下文

在产出任何内容之前，加载：

- `<必加载文件 1>`（说明用途）
- 如需详细方法论，仅加载所需参考文档：
  - `references/<参考文件>.md`：用于 <子命令/场景>

## Steps

### Step 1: <步骤名称>

- 输入：<从哪里获取数据>
- 动作：<具体做什么>
- 输出：<产出了什么>

### Step 2: <步骤名称>

- 输入：<从哪里获取数据>
- 动作：<具体做什么>
- 输出：<产出了什么>

## 运营规则

- **<规则 1>**：<具体规则描述>
- **与其他 Skill 的边界**：<明确说明>

### 反模式（严禁）

- <反模式 1>
- <反模式 2>

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| <检查项 1> | <不通过时的动作> |
| <检查项 2> | <不通过时的动作> |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `<上游Skill>` | <上游Skill> 输出 <文件>，作为本 Skill 的输入 |
| `<下游Skill>` | 本 Skill 输出 <文件>，作为 <下游Skill> 的输入 |

## 文件输出

除非用户另有指定，使用以下默认位置：

- <输出文件 1>：`<默认路径>`
```

---

## 模板使用说明

### frontmatter 字段填写规则

| 字段 | 必填 | 填写指南 |
|------|------|---------|
| name | 是 | kebab-case 标识符 |
| description | 是 | 核心价值 + 触发场景 + 否定边界。触发场景要写得"宽"一些，避免漏触发 |
| category | 是 | 从现有分类中选择：drafting, extended-outline, genre-detection, ideation, outline, review, sedimentation, typeset |
| agents | 是 | 从 .claude/agents/ 中选择，遵循系统既有层级 |
| inputs | 是 | 列出需要读取的文件 |
| outputs | 是 | 列出会产出的文件路径 |
| required_reviews | 是 | 内审至少 1 人，client 标明 required/optional/never |
| duration_estimate | 是 | 估算完成时间 |

### body 章节填写规则

| 章节 | 必填 | 填写指南 |
|------|------|---------|
| Overview | 是 | 一段话说清核心价值 + 在系统中的位置 |
| 能力要求 | 视情况 | 列出"必须能做的"和"明确不做的" |
| 必备上下文 | 视情况 | 需要加载系统核心资源的 Skill 必须有此章节 |
| Steps | 是 | 按步骤描述执行流程 |
| 运营规则 | 是 | 包含强制规则 + 反模式声明 |
| Quality Gates | 是 | 至少 3 条可量化的检查项 |
| 与其他 Skill 的协作 | 是 | 列出上游/下游/并行 Skill |
| 文件输出 | 视情况 | 如输出路径不显而易见，需包含此章节 |
