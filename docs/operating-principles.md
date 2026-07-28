# BookForge Studio 运营原则（供你项目 CLAUDE.md 引用）

这份文档是原 BookForge Studios 模板仓库 `CLAUDE.md` 的运营原则部分，抽取出来供插件用户参考。**插件本身不会替你写入这些内容**——Claude Code 插件不提供"自动往消费者项目里塞 CLAUDE.md"的机制，请把下面对你适用的部分手动复制/改写进你自己工作区根目录的 `CLAUDE.md`。

## 建议写入你项目 CLAUDE.md 的内容

```markdown
本项目使用 bookforge-studio 插件进行 AI 原生图书生产，请把它当作一座出版工作室来对待。

## 运营原则

- 一个 session 只做一本书的项目。
- 活动项目位于 `projects/<project-id>/` 之下。
- 类型在构思阶段确定，并驱动下游的 agents、skills、memory、review gates 与质量度量。
- Genre Pack 是一整套创作范式包，不是风格预设。
- 关键创作决策必须经人工确认：世界观、史观、人物命运、核心论点、读者承诺，以及任何类型专属的硬性门。
- 所有持久化决策必须写入项目文件，不能只保留在对话里。
- 主题核心论点须有 `research/` 调研论据支撑，不得凭空判断。
- 每个完成的项目都应把可复用的经验沉淀到工作区根目录的 `capability-library/`
  （首次使用请从插件的 `capability-library-template/` 复制一份到你的工作区根目录，
  重命名为 `capability-library/`）。

## 项目隔离

- 一个 session 中不得混入第二个图书项目。
- 写入前必须确认活动项目。
- 类型 memory 只能写入活动项目的 `genre-context/genre-memory/`。

## Genre Pack 加载

活动类型从 `projects/<project-id>/PROJECT.md` 与
`projects/<project-id>/genre-context/active-pack.yaml` 读取。若两者不一致，
停下来请作者确认以哪一份为准，确认前不得继续。

## 审校纪律

- 关键（critical）一致性违规阻断进度。
- 高（high）严重度问题必须出具书面修复计划。
- 中（medium）等问题可继续推进，但必须记录在案。
- 需要人工审校的 hook 应返回 review-needed 状态，而非静默放行。
```

## 协作协议（按顺序推进，除非明确要求检查/修复既有项目）

1. 意图采集（Idea intake）
2. 苏格拉底式深挖（Socratic deep dive）
3. 类型识别与作者确认（Genre detection and author confirmation）
4. 深度主题调研（Deep topic research）——与第 5 步可并行
5. 对标书调研与风格学习（Benchmark corpus research）——与第 4 步可并行
6. 宪法文件（Constitution file）——消费 `research/` 与 `style-corpus/`
7. 大纲候选（Outline candidates）
8. 选定大纲（Selected outline）
9. 扩展章节计划（Extended chapter plan）
10. 草稿 V0 至 V3
11. 读者模拟与修复级联（Reader simulation and fix cascade）
12. 排版导出（Typeset export）
13. 能力沉淀（Capability harvest）

## 必读参考

插件内以下文档定义了各阶段的详细协议，建议在对应阶段按需 Read（路径相对插件安装目录，Claude Code 会以 `${CLAUDE_PLUGIN_ROOT}` 解析）：

- `docs/coordination-rules.md`
- `docs/genre-pack-protocol.md`
- `docs/genre-detection-guide.md`
- `docs/consistency-engine-spec.md`
- `docs/human-collaboration-modes.md`
- `docs/pipeline-stage-spec.md`
- `docs/three-tier-confidence.md`
- `docs/context-management.md`
- `docs/writing-brief-spec.md`
- `docs/chapter-summary-spec.md`
- `docs/reader-simulation-spec.md`

以及 `rules/` 目录下按产物类型划分的强制标准（`constitution.md`、`outline.md`、`chapter-draft.md`、`consistency-rules.md`、`registry.md`、`review-report.md`、`capability-asset.md`、`typeset-output.md`、`style-corpus.md`、`topic-research.md`、`genre-pack.md`、`agent-genre-affinity.md`、`extended-outline.md`、`reader-profiles.md`、`reader-facing-prose.md`，以及各类型专属的 `genre-memory-*.md`）。
