---
name: skill-gen
description: "BookForge Studios Skill 生成器 — 通过对话式引导在 BookForge Studios 系统中创建新 Skill，自动建立与现有 Skill/Agent/Rule/Hook 的关联，确保符合系统原则。触发场景：用户要创建新 Skill、新增能力、把某个工作流固化为 Skill、扩展现有 Skill 体系。不负责 Skill 的测试驱动开发（由 skill-creator 负责），不负责创建 Agent/Rule/Hook（需手动创建）。"
category: "system"
agents: []
inputs:
  - .claude/skills/ 下所有 Skill 的 SKILL.md（系统扫描）
  - .claude/agents/ 下所有 Agent 定义
  - .claude/rules/ 下所有 Rule
outputs:
  - .claude/skills/<new-skill-name>/SKILL.md
  - .claude/skills/<new-skill-name>/references/（可选）
  - .claude/skills/<new-skill-name>/templates/（可选）
required_reviews:
  - internal: []
  - client: never
duration_estimate: "15-30 分钟"
---

# Skill Generator — BookForge Studios Skill 生成器

## Overview

在 BookForge Studios 系统中创建新 Skill 时使用。通过六阶段对话式引导，帮助用户定义新 Skill 的定位、建立与现有系统的关联、生成符合 BookForge Studios 标准的完整 SKILL.md，并通过原则检查验证质量。

**核心价值**：确保新 Skill 不是孤立存在的，而是与现有的 32 个 Skill、12 个 Agent、17 个 Rule、18 个 Hook 形成有机整体。

**系统定位**：**BookForge Studios** 是一套面向「AI 原生书籍创作」的 Claude Code Agent 模板项目，把 AI Agent 组织成一个能为**不同类型书籍**提供专属创作范式的"虚拟出版集团"，覆盖从用户模糊想法到专业排版成品的全流程。

**与 skill-creator 的区别**：skill-gen 负责系统级设计（定位、关联、原则遵从）；skill-creator（官方插件）负责后续的测试驱动优化（eval、description 优化）。建议先用 skill-gen 创建，再用 skill-creator 优化。

## 必备上下文

在执行任何阶段之前，加载：

- `references/skill-patterns.md`：五种 Skill 设计模式，用于 Phase 2 推荐模式
- `references/principle-checklist.md`：七维度原则检查清单（4 通用 + 3 BookForge Studios 特化），用于 Phase 5 验证
- `templates/skill-template.md`：标准 Skill 骨架，用于 Phase 4 生成

系统扫描时需读取：
- `.claude/skills/*/SKILL.md`：提取 name/description/category/inputs/outputs/agents
- `.claude/agents/*.md`：提取 role/layer/domain/consults
- `.claude/rules/*.md`：提取 globs 和约束摘要

## 工作流

### Phase 1: ANALYZE — 系统扫描

**目标**：建立当前系统全景，为后续阶段的定位和关联提供数据基础。

**执行步骤**：

1. 扫描 `.claude/skills/` 下所有 SKILL.md，提取 frontmatter 关键字段
2. 扫描 `.claude/agents/` 下所有 Agent 定义，提取角色层级和协作关系
3. 扫描 `.claude/rules/` 下所有 Rule，提取 glob 模式和约束摘要

**输出格式**（向用户展示）：

```markdown
## 系统全景

### 现有 Skill 分布（按 category）

| category | 数量 | Skill 列表 |
|----------|------|-----------|

### Agent 层级概览

| 层级 | Agent |
|------|-------|
| 未分层 层 | Editorial Director, Genre Detector, Genre Strategy Director, Lead Drafting, Lead Extended Outline, Lead Ideation, Lead Outline, Lead Review, Lead Typeset, Memory Curator, Production Director, Research Agent |

### 当前数据流概览

[简要说明现有 Skill 间的主要数据流向]
```

**展示全景后，暂停等待用户确认再进入 Phase 2。**

---

### Phase 2: POSITION — 定位对话

**目标**：通过与用户对话，明确新 Skill 的核心价值和职责边界。

**执行步骤**：

1. **询问核心目标**：新 Skill 要解决什么问题？一句话描述。
2. **确定 category**：展示现有分类供选择：drafting, extended-outline, genre-detection, ideation, outline, review, sedimentation, typeset。或新建分类（需说明理由）。
3. **选择设计模式**：基于用户的回答，从 `skill-patterns.md` 推荐最合适的模式，说明理由。
4. **标记重叠**：基于 Phase 1 的扫描数据，列出可能与新 Skill 职责重叠的现有 Skill。
5. **定义边界**：看到重叠的 Skill 后，让用户明确新 Skill 的否定边界——不负责什么。
6. **生成定位声明**（核心价值 + 设计模式 + category + 否定边界）

**展示定位声明后，暂停等待用户确认或修改。可多轮调整。**

---

### Phase 3: RELATE — 关联建立

**目标**：自动推荐新 Skill 与现有系统的关联关系，经用户确认后确定。

**执行步骤**：

1. **推荐 Agent**：基于 category 和领域关键词，对照 `.claude/agents/` 匹配 role/domain，遵循系统既有 Agent 层级。
2. **推荐 Rule**：基于预期输出文件路径，匹配 Rule 的 glob 模式。
3. **推荐数据流**：基于现有 Skill 的 inputs/outputs 字段交叉匹配，推荐上游和下游 Skill。
4. **推荐 Hook**：基于操作类型（文件写入、Bash 执行等），列出会自动触发的 Hook。

**展示关联推荐后，暂停等待用户确认或调整。**

---

### Phase 4: GENERATE — 生成文档

**目标**：基于 Phase 2-3 的结果，生成完整的 SKILL.md。

基于 `templates/skill-template.md` 骨架，依次生成：frontmatter、Overview、能力要求（含否定边界）、必备上下文、Steps、运营规则、Quality Gates、协作表、文件输出。

**展示完整文档后，暂停等待用户审阅。可多轮迭代。**

---

### Phase 5: VALIDATE — 验证检查

**目标**：基于 `principle-checklist.md` 逐项检查新生成的 Skill。

1. **确定 Skill 类型**：根据 category 判断适用的检查项范围（参考 principle-checklist.md 末尾的快速判定矩阵）
2. **逐项检查**：按七大维度执行（4 通用维度 + 3 BookForge Studios 特化维度）
3. **生成验证报告**（通过率 X/Y）

**如有不通过项，与用户讨论修改方案。修改后重新验证，直到全部通过。**

---

### Phase 6: INTEGRATE — 系统集成

**目标**：将验证通过的 Skill 写入系统。

1. 确认目录名称（kebab-case）
2. 写入 `.claude/skills/<new-skill-name>/SKILL.md`
3. 如有 references/templates 需求，创建对应子目录
4. 输出集成确认 + 系统位置摘要 + 下一步建议

## 运营规则

- **每个 Phase 都需要用户确认后才能进入下一个。** 不允许跳过或一口气跑完。
- **否定边界是强制的。** 每个新 Skill 必须声明"不负责什么"。
- **系统扫描必须实时执行。** 不依赖缓存，每次调用都重新扫描。
- **Agent 引用必须有效。** agents 字段中的每个角色名都必须在 `.claude/agents/` 中存在。
- **不创建 Agent/Rule/Hook。** 本 Skill 只创建 Skill 文件。
- **原则检查不可跳过。** Phase 5 的验证是强制门控。
- **保持简洁。** 生成的 SKILL.md 控制在 500 行以内。超长则拆到 references/。

### 反模式（严禁）

- 生成与现有 Skill 职责完全重叠的新 Skill（应扩展现有 Skill 而非新建）
- 跳过 Phase 2 的定位对话直接生成
- 生成的 Skill 不声明否定边界
- agents 字段中引用不存在的 Agent
- 跳过验证直接写入系统
- 在 description 中省略触发场景

## Quality Gates

| 检查项 | 不通过的处理 |
|--------|------------|
| Phase 2 是否产出明确的定位声明（含否定边界） | 回到 Phase 2 重新定位 |
| Phase 3 推荐的 Agent 是否都在 .claude/agents/ 中存在 | 提示用户创建或替换 |
| Phase 4 frontmatter 是否包含所有必需字段 | 补充缺失字段 |
| Phase 5 原则检查是否全部通过 | 修改后重新验证 |
| 生成的 SKILL.md 是否在 500 行以内 | 将详细内容拆到 references/ |

## 与其他 Skill 的协作

| 协作 Skill | 协作方式 |
|-----------|---------|
| `skill-creator`（官方插件） | skill-gen 完成系统级设计后，交由 skill-creator 做测试驱动优化 |
