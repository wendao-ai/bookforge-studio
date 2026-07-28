# Reader Simulation Spec

## 1. 定位

读者模拟系统是 S5 Review 阶段的执行系统（见 [pipeline-stage-spec.md](pipeline-stage-spec.md)）。它在 V3 初稿完成后、人工审校前运行，把出版业的"试读反馈"环节前置并结构化：生成目标读者画像、收集多维反馈、仲裁共识、分流修复。

它**不替代**专家审校。读者对事实/准确性的判断走软隔离（见 §6），必须经 expert 升级为 `observed` 级才能进入可执行修复。这与 [reader-profiles 规则](../rules/reader-profiles.md)"读者画像不能当事实权威用"一致。

## 2. 设计目标

1. **覆盖多样性**：从画像空间采样，保证怀疑型/敌意型读者一定在场，避免 LLM 生成同质化好评。
2. **维度类型化**：反馈维度随 Genre Pack 变化，查类型专属硬伤（非虚构查论证链、教材查前置依赖、科幻查世界观一致性）。
3. **准确度隔离**：读者可指出"这里可疑"，但不能靠人头投票把错误"坐实"或把对的"改错"。
4. **仲裁可解释**：共识不靠数人头，靠既定优先级裁定（见 [coordination-rules.md](coordination-rules.md)）。
5. **闭环到修复**：每条反馈有去向（revise/defer/reject），不悬空。

## 3. 与现有 spec 的关系

- [pipeline-stage-spec.md](pipeline-stage-spec.md)：S5 输入/输出/exit gate。
- [consistency-engine-spec.md](consistency-engine-spec.md)：severity 定义、check 输出 schema、backtrack protocol。
- [three-tier-confidence.md](three-tier-confidence.md)：confidence 标签（`observed`/`inferred`/`speculated`）。
- [coordination-rules.md](coordination-rules.md)：冲突仲裁优先级。
- [human-collaboration-modes.md](human-collaboration-modes.md)：reader simulation 非阻断，但 `expert-reviewed` 类型的事实需 expert。
- [rules/reader-profiles.md](../rules/reader-profiles.md)：至少三类画像 + 必含怀疑型；读者不能当事实权威。
- [rules/review-report.md](../rules/review-report.md)：区分 taste/genre_law/factual；`controversy_map.yaml`；fix 分流到 revise/defer/reject。

## 4. 流水线总览

四个 review skill 是一条流水线，不是并列工具。上游产物是下游输入。

```
V3 drafts + pack reader-profiles + brief.target_readers + consistency reports
      │
      ▼
[spawn-reader-panel]   定义画像空间 → 锚点+加权采样 → review/reader_pool.yaml
      │
      ▼
[multi-dim-feedback]   每个 reader instance 跑五维反馈 → review/reader_reports/<id>.md
      │
      ▼
[consensus-analysis]   跨 reader 聚合 → review/controversy_map.yaml
      │
      ▼
[fix-cascade]          severity×type 分流 → review/fix-cascade-plan.yaml（含 backtrack）
```

## 5. Profile Space（画像空间）

不是固定个体清单，是可组合的维度空间。每个 reader instance = 维度取值的一个组合。

### 5.1 维度

| 维度 | 字段 | 取值 | 决定 |
|---|---|---|---|
| 角色 | `role` | 专业同行/通识入门/怀疑型/实践应用/媒体评论人/学生/监管者 | 看重什么、挑什么刺 |
| 知识水平 | `knowledge_level` | 专家/进阶/入门/小白 | 术语密度容忍度 |
| 阅读目的 | `reading_goal` | 求知/实操/证伪/消遣/引用研究 | 评价标尺 |
| 立场 | `stance` | 认同/中立/怀疑/敌意 | 是否给好评（保证挑刺者在场） |
| 阅读场景 | `context` | 深度研读/通勤碎片/课堂/决策参考 | 篇幅与结构偏好 |
| 敏感点 | `sensitivity_profile` | 继承 pack sensitivities + brief 特化 | rejection triggers |

### 5.2 来源（双源）

- **pack 锚定**：`role` 与 `sensitivity_profile` 从 active Genre Pack 的 [reader-profiles.yaml](../../genre-packs/nonfiction-general/reader-profiles.yaml) 继承，每类原型至少采样 1 个 instance（保证类型合规 + 怀疑型在场）。
- **brief 特化**：`knowledge_level` / `reading_goal` / `stance` / `context` 的分布权重来自 `constitution/brief.yaml` 的 `target_readers`。目标读者占多数，边缘 stance（怀疑/敌意）占少数做压力测试。

## 6. Sampling（采样）

### 6.1 策略

1. **确定性锚点**：pack 每类原型各取 ≥1 instance（`role` 固定，其余维度按原型语义填充，`is_anchor: true`）。锚点保证下限不塌——怀疑型、专业型一定在场。
2. **加权填充**：剩余 instance 按 `brief.target_readers` 分布加权采样，显式覆盖边缘 stance（怀疑/敌意）。
3. **去重**：维度组合 hash 去重，避免同质化。

### 6.2 默认规模

`N = 20-30`（默认）。其中 pack 原型锚点占 4-6，加权采样填充 15-25。可在 `PROJECT.md` 或 review 配置覆盖。大规模采样须**分批汇总**（每批 ≤10 reader，逐批进 consensus，避免单次 context 爆炸）。

### 6.3 reader_pool.yaml schema

```yaml
project_id: <id>
genre: <genre_id>
sampled_at: <iso>
default_n: 24
distribution_basis: constitution/brief.yaml#target_readers
instances:
  - id: R01
    archetype: 专业同行读者          # 来自 pack 原型
    role: 专业同行
    knowledge_level: 专家
    reading_goal: 证伪
    stance: 怀疑
    context: 深度研读
    sensitivity_profile: [逻辑漏洞, 选择性引用]
    weight: 1.2                      # 采样权重
    is_anchor: true
  - id: R02
    archetype: 实践应用读者
    role: 实践应用
    knowledge_level: 进阶
    reading_goal: 实操
    stance: 认同
    context: 决策参考
    sensitivity_profile: [案例虚, 缺落地路径]
    weight: 1.0
    is_anchor: false
```

## 7. Multi-dim Feedback（多维反馈）

### 7.1 五维 + 类型专属子项

| 维度 | 含义 | 类型专属子项来源 |
|---|---|---|
| `reader_promise` | 读者承诺兑现 | `brief.core_promise` × pack |
| `genre_law` | 类型铁律 | pack `consistency-rules.yaml` |
| `craft` | 技艺（结构/节奏/语言） | pack `quality-metrics.yaml` |
| `clarity` | 清晰度（逻辑/术语/可懂度） | 类型定义（见 consistency-engine-spec） |
| `risk` | 风险（事实/利益相关/敏感内容） | 类型定义 |

子项随类型变化：非虚构查论证链/证据强度；教材查前置依赖/布鲁姆层级；科幻查世界观一致性/技术代价；历史查史料可信度/史观。

### 7.2 每条反馈字段

```yaml
reader_id: R01
dimension: clarity
sub_item: argument_chain            # 类型专属子项
severity: high                      # critical/high/medium/low
feedback_type: genre_law            # taste/genre_law/factual/craft
confidence: inferred                # observed/inferred/speculated；读者来源封顶 inferred
verdict: negative                   # positive/negative（夸奖与批评都收）
evidence:                           # 必填，违反则 reject（review-report 规则）
  chapter: ch03
  location: "§2 第3段"
  quote: "..."
comment: "论证从 A 跳到 C，缺 B 的前提"
suggested_fix: "在 §2 前补 B 的定义"
```

- `verdict: positive` 同样收集（命中 `delight_triggers`），用于回答"哪些角度打动读者"。
- `evidence` 必填——空泛评语（"文笔流畅""深入浅出"）违反 [review-report 规则](../rules/review-report.md)，一律 reject。

### 7.3 reader_reports/<reader_id>.md schema

每份报告包含：reader instance 摘要 → 五维评分（每维 1-5 + 评语）→ 逐条 findings（上述字段）→ 整体 verdict。

## 8. Accuracy Isolation（准确度软隔离）

> **设计意图**：本系统采用软隔离——factual 类反馈与普通 fix 共用 fix-cascade 队列，但靠强制标记 + 禁止自动修防住"读者投票改错"。这是用户在硬隔离/软隔离之间选择的路径；护栏一旦缺失，多 reader 一致指出某"事实错误"时可能被误当普通 fix 自动改掉（把对的改错）。因此下列标记与护栏为强制项，不可省略。

读者对**事实/准确性**的判断（`feedback_type: factual`，或 `dimension: risk` 中事实性子项）走软隔离。

### 8.1 强制标记

所有读者来源的 factual 类反馈，写入 fix-cascade-plan.yaml 时强制带：

- `source: reader`
- `confidence`：封顶 `inferred`（读者来源不得 `observed`）
- `auto_fix: false`
- `needs_expert_review: true`
- `expert_status: pending`

### 8.2 护栏（防"投票改错"）

- fix-cascade 处理时，`auto_fix: false` 命中的条目**绝不**修改原文，只能进入 `needs_review` 待 expert 确认。
- 即使多数 reader 一致指出同一"事实错误"，仍不自动修——**一致性不等于正确性**。
- 在 fix-cascade-plan.yaml 单独分组 `factual_pending_expert`，便于专家批量处理。

### 8.3 升级路径

expert 审核后：

- 确认为错 → 给 `observed` 级判断 → 升级为可执行 fix（`auto_fix` 可置 `true`）。
- 确认为对 → `reject` 该读者反馈，但保留"读者曾质疑此事实"的记录（供后续敏感处理与 capability 沉淀）。
- 存疑 → 标 `open_question`，人审。

### 8.4 Exit gate

`factual_pending_expert` 队列非空时，S5 不允许 clean exit：要么 expert 处理完，要么作者显式 defer 并在 `.history/events.jsonl` 记录放弃理由。防止"读者指了错、专家没看、错就留下了"。

## 9. Consensus Analysis（共识仲裁）

### 9.1 controversy_map.yaml 三档

```yaml
findings_aggregated:
  - topic: "ch03 论证跳步"
    dimension: clarity
    severity_votes: { high: 3, medium: 5, low: 1 }   # 投票聚合 severity
    consensus: consensus                              # consensus / split / outlier
    readers: [R01, R03, R07, R11, R15]
    conflicting_readers: []                           # split 时列对立双方
    arbitration_priority: genre_law                   # 命中的仲裁优先级层
    action: revise
```

### 9.2 双轨仲裁

- **severity**：数人头投票聚合（多少 reader 提到、严重度分布）。
- **action 仲裁**：不靠数人头，靠 [coordination-rules.md](coordination-rules.md) 优先级裁定：
  1. author-confirmed constitution
  2. active genre critical rules
  3. stage exit criteria
  4. reader promise
  5. local style

  即：taste 类吐槽（第 5 层）与 genre_law（第 2 层）冲突时，genre_law 赢，不数人头。

### 9.3 分档判定

- `consensus`：≥70% reader 同向 → 直接进 fix-cascade（按 severity）。
- `split`：立场对立 → 进 controversy_map，标 `needs_author_arbitration`，人审。
- `outlier`：个别 → 记录，默认 defer，除非命中 genre critical。

## 10. Fix Cascade（修复分流）

### 10.1 severity × type → action

| severity | type=factual | type=genre_law | type=craft/clarity | type=taste |
|---|---|---|---|---|
| critical | expert + backtrack | backtrack（阻断） | revise | defer |
| high | factual-pending-expert | revise + 人审 | revise | defer |
| medium | factual-pending-expert | revise | revise / 记录 | reject |
| low | factual-pending-expert | 记录 | 记录 | reject |

- `taste` 类反馈默认 reject 或 defer，不消耗修订预算。
- `factual` 类恒进 `factual_pending_expert`（软隔离），expert 升级前不自动修。
- critical 的 `genre_law`/`craft` 触发 backtrack（见 consistency-engine-spec backtrack protocol）。

### 10.2 backtrack

critical 出现时，识别最早引入矛盾的 artifact（draft → chapter plan → outline → constitution），由 Director 层选 revise 范围。

### 10.3 fix-cascade-plan.yaml schema

```yaml
project_id: <id>
generated_at: <iso>
items:
  - id: F01
    topic: "ch03 论证跳步"
    source_readers: [R01, R03, R07]
    severity: high
    feedback_type: genre_law
    action: revise
    target_artifact: drafts/chapters/ch03/v3_polished.md
    auto_fix: true
    needs_expert_review: false
    owner: lead-drafting
  - id: F07
    topic: "ch05 数据可能过时"
    source_readers: [R11, R15]
    severity: high
    feedback_type: factual
    action: needs_review
    auto_fix: false                 # 软隔离护栏：强制 false
    needs_expert_review: true
    expert_status: pending
    owner: expert-reviewer
factual_pending_expert: [F07]
deferred: []
rejected: []
```

## 11. 人审介入点

reader simulation 本身非阻断（见 [human-collaboration-modes.md](human-collaboration-modes.md)）。但以下暂停：

- controversy_map 出现 `split` + high/critical → `needs_author_arbitration`。
- `factual_pending_expert` 队列非空 → 等 expert（textbook/history 类强制 `expert-reviewed`）。
- 读者共识与 constitution 冲突 → constitution 赢，记录，但提示作者复核。
- 任何 backtrack（critical）→ 人审。

## 12. 产出文件清单

```
review/
  reader_pool.yaml              # 采样的 reader instances
  reader_reports/
    R01.md ... R24.md            # 每份多维反馈
  controversy_map.yaml           # 共识/分歧/孤立 + 仲裁
  fix-cascade-plan.yaml          # 分流计划（含 factual_pending_expert 分组）
  review_summary.md              # 给作者/Director 的摘要
```

## 13. 四个 skill 的实现契约

> 以下契约供四个空壳 skill 正文 fill 时遵循。当前 [spawn-reader-panel](../skills/spawn-reader-panel/SKILL.md)、[multi-dim-feedback](../skills/multi-dim-feedback/SKILL.md)、[consensus-analysis](../skills/consensus-analysis/SKILL.md)、[fix-cascade](../skills/fix-cascade/SKILL.md) 的 SKILL.md 仍是模板骨架，需按本契约填实。

### spawn-reader-panel
- **输入**：`PROJECT.md`、`active-pack.yaml`、pack `reader-profiles.yaml`、`brief.yaml#target_readers`
- **输出**：`review/reader_pool.yaml`
- **步骤**：加载 pack 原型 → 读 brief 分布 → 锚点采样 → 加权填充 → 去重 → 写 pool

### multi-dim-feedback
- **输入**：`reader_pool.yaml`、V3 drafts、pack `consistency-rules.yaml` + `quality-metrics.yaml`
- **输出**：`review/reader_reports/<id>.md`
- **步骤**：每个 instance → 按其维度组合定评价标尺 → 五维反馈（带 evidence/confidence/type）→ 同时收 positive 与 negative

### consensus-analysis
- **输入**：`review/reader_reports/`、coordination-rules 优先级
- **输出**：`review/controversy_map.yaml`
- **步骤**：跨 reader 聚合 topic → severity 投票 → 分档（consensus/split/outlier）→ 优先级仲裁 action

### fix-cascade
- **输入**：`controversy_map.yaml`、consistency-engine severity、three-tier confidence
- **输出**：`review/fix-cascade-plan.yaml`（含 `factual_pending_expert` 分组）
- **步骤**：severity×type → action 映射 → factual 软隔离强制标记 → critical 触发 backtrack → 写计划
