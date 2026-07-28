# Genre Packs

每种书籍类型的完整创作范式包。

## 已注册 Pack

| Pack | 类型 | 核心引擎 | 状态 |
|------|------|---------|------|
| `scifi` | 科幻小说 | 世界设定圣经 + 科学一致性引擎 | stable |
| `textbook` | 教材 | 知识点 DAG + 强人审 | stable |
| `romance` | 言情小说 | 情感节拍器 + 关系状态机 | stable |
| `history` | 历史书籍 | 史料库 + 史观一致性 + 时间线 | stable |
| `fiction-general` | 通用虚构 | 通用故事弧线 + 人物弧光 | stable |
| `nonfiction-general` | 通用非虚构 | 多种子范式 | stable |
| `biography` | 人物传记/回忆录 | 人物本质溯源 + 事实核查 + 叙事弧光 | stable |

## 标准 Pack 结构（9 组件）

每个 Pack 必须包含：

1. `PACK.md` — 元数据与类型识别触发条件
2. `agents/` — 类型专属 Agent
3. `skills/` — 类型专属 Skill
4. `memory-schema.yaml` — Memory 结构扩展
5. `structure-paradigm.yaml` — 结构范式
6. `reader-profiles.yaml` — 模拟读者画像群
7. `quality-metrics.yaml` — 质量度量定义
8. `collaboration-mode.yaml` — 人机协作模式
9. `consistency-rules.yaml` — 一致性规则

另可选：`templates/`（排版与文档模板）、`knowledge/`（类型知识库）
