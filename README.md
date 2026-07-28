# BookForge Studio（Claude Code 插件）

BookForge Studio 是一个面向 AI 原生图书生产的 Claude Code 插件。它把 agents、skills、hooks、rules、文档模板以及 8 个类型专属 Genre Pack 打包成一套可安装、可复用的出版工作流，源自作者本地的 BookForge Studios 模板项目整理而成。

本系统专为长篇写作项目设计——在这类项目里，类型会改变作品的创作法则：科幻小说需要世界圣经与科学一致性校验；教材需要知识 DAG 与专家审定门；言情小说需要情感节拍与关系状态；历史著作需要史料可信度与史观纪律。

## 核心工作流

每一本书都遵循同一条六阶段流水线：

1. **构思（Ideation）**：厘清意图、读者、核心论点/故事种子、约束条件与类型。
2. **大纲（Outline）**：生成并选择具备类型意识的结构。
3. **扩展大纲（Extended Outline）**：规划章节级依赖、读者承诺、揭示点与证据。
4. **草稿（Drafting）**：产出 V0 骨架、V1 粗稿、V2 精炼、V3 润色四个版本。
5. **审校（Review）**：模拟目标读者、综合反馈、规划修复。
6. **排版（Typeset）**：在本地工具链支持的前提下导出 DOCX/EPUB/PDF。

## 已支持的 Genre Pack

| 类型 | Pack id | 核心 memory | 主要质量门 |
| --- | --- | --- | --- |
| 科幻小说 | `scifi` | 世界圣经、科技树、时间线、势力图 | 世界/科学一致性 |
| 教材 | `textbook` | 知识 DAG、学习目标、习题 | 前置依赖完整性 |
| 言情 | `romance` | 关系状态机、情感节拍表 | 情感逻辑 |
| 历史 | `history` | 史料库、时间线、史观声明 | 史料与观点一致性 |
| 通用小说 | `fiction-general` | 故事弧、人物、主题、承诺 | 叙事连贯性 |
| 通用非虚构 | `nonfiction-general` | 论点、论证链、证据图 | 逻辑与证据 |
| 人物传记/回忆录 | `biography` | 传主资料库、人生时间线、事实-叙事映射 | 事实-叙事分离 + 传主伦理 |
| 网络小说 | `webnovel` | 开放环状态机、量级校准 | 长程记忆一致性 |

## 安装

**本地开发/试用**（在插件目录旁运行）：

```bash
claude --plugin-dir /path/to/bookforge-studio-plugin
```

**从 GitHub 安装**（推荐，本仓库已自带 `.claude-plugin/marketplace.json`，自托管为一个单插件 marketplace）：

```bash
/plugin marketplace add wendao-ai/bookforge-studio
/plugin install bookforge-studio@bookforge-studio
```

## 工作区自举（无需手动步骤）

插件只携带**可复用的工具与范式**，不携带你的具体图书项目和跨项目积累的经验——这些属于你自己的工作区（`$CLAUDE_PROJECT_DIR`）。你**不需要**手动创建或复制任何目录，插件会在你实际用到时自动搭好：

- **`capability-library/`**：`SessionStart` hook 在检测到工作区还没有这个目录时，自动从插件的 `capability-library-template/` 复制一份过去（每个工作区只做一次，已存在则跳过）。
- **`projects/<project-id>/`**：第一次跑 `/start-book-project` 时，由该 skill 从插件的 `projects-template/_template/` 复制出对应的新项目骨架——不需要你自己 `mkdir`/`cp`。`projects-template/` 里的 6 个 `sample-*` 只是给你（和 Claude）参考的示例，不会被自动复制。
- **`CLAUDE.md` 运营原则**：`/start-book-project` 首次运行时会检查你工作区根目录的 `CLAUDE.md` 是否已包含 BookForge 的协作协议；如果没有，会询问你是否要把 [`docs/operating-principles.md`](docs/operating-principles.md) 里的内容追加进去——这一步需要你确认，插件不会静默改写你自己的 `CLAUDE.md`。

插件的 hooks 通过 `$CLAUDE_PROJECT_DIR`（你的工作区，前面这些自举产物都写在这里）与 `$CLAUDE_PLUGIN_ROOT`（本插件安装位置，只读参考资料）区分"你的书"和"插件自带的范式资产"，`project-isolation-guard` 不允许把插件安装目录当写入目标。

## 快速开始

1. 在 Claude Code 中打开你的工作区目录（不是插件安装目录）——插件已安装即可，无需预建任何文件。
2. 从 `/start-book-project` 开始：告诉 Claude 你的书的想法，第一次运行会自动创建 `projects/<project-id>/` 并引导你确认要不要往 `CLAUDE.md` 追加运营原则。
3. 从构思进入大纲前，必须先确认类型。
4. （可选）在 ideation 阶段做写书前调研三支柱：`/deep-topic-research` 建可追溯知识库、`/benchmark-corpus-research` 学习对标书风格、`/editorial-acquisition` 做选题论证。
5. 按顺序使用各阶段 skill；当活动类型有要求时，不得跳过人工审校门。
6. V3 定稿后用 `/export-docx` 基础导出；需投稿级精排用 `/typeset-docx-elegant`。

## 插件内容导航

| 路径 | 用途 |
| --- | --- |
| `.claude-plugin/plugin.json` | 插件清单 |
| `agents/` | 共享 director、stage lead 与 specialist agent 定义（12 个） |
| `skills/` | 跨所有图书类型复用的共享工作流命令（45 个，含选题论证、导出、精排、"人和事驱动写作"叙事 skill 等） |
| `genre-packs/` | 8 个类型专属 Pack，各自带 `PACK.md`、`agents/`、`skills/`、`memory-schema.yaml`、`structure-paradigm.yaml`、`reader-profiles.yaml`、`quality-metrics.yaml`、`collaboration-mode.yaml`、`consistency-rules.yaml` |
| `hooks/hooks.json` + `hooks/scripts/` | Claude Code hook 入口：会话/项目上下文加载、写入护栏、一致性检查、版本快照 |
| `scripts/bookforge_hook.py` | 所有 hook 共用的 Python 运行时 |
| `docs/` | Studio 的运行协议文档，含 `operating-principles.md`（供你复制进项目 CLAUDE.md） |
| `rules/` | 各类产物（constitution/outline/chapter-draft/registry/review/typeset/genre-memory-* 等）的强制标准与反模式 |
| `shared-tooling/` | 责编协作协议、风格语料调研说明 |
| `capability-library-template/` | 能力库空骨架模板（不含真实项目沉淀内容）；`SessionStart` hook 首次运行时自动复制到你工作区的 `capability-library/`，无需手动操作 |
| `projects-template/` | `_template`（新项目骨架，`/start-book-project` 首次运行时自动复制到 `projects/<project-id>/`）+ 6 个 `sample-*` 类型示例项目（仅供参考，不会被自动复制） |

### 关于未接线的 hook 脚本

`hooks/scripts/` 下有 18 个脚本、`scripts/bookforge_hook.py` 里也都注册了对应 handler，但 `hooks/hooks.json` 目前只接线了 14 个事件触发点。以下 4 个脚本逻辑齐全但**未被任何事件自动调用**，属于预留能力，如需启用请自行在 `hooks/hooks.json` 里补事件绑定：

- `pre-compact-preserve.sh`（对应 `PreCompact` 事件，保存压缩前上下文）
- `concept-registry-update.sh`
- `consistency-violation-alert.sh`
- `human-review-required-alert.sh`

## License

见 [`LICENSE`](LICENSE)（MIT）。
