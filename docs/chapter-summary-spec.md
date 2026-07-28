# Chapter Summary Spec — 每章写后摘要（长程记忆层）

> 长程记忆层。每章草稿完成后生成压缩摘要，作为百万字连载的长程记忆。
> 对标 webnovel-writer `summaries/`——Bookie 用**非冲击方式**实现：摘要是正文派生的压缩，registry 仍是真源，**不造第二事实源**（区别于 webnovel 的 story-system 提交链）。

## 为什么需要

百万字连载靠不了记忆。写到第 200 章时，作者/AI 需要知道：
- 第 47 章某个配角当前状态？
- 第 12 章埋的伏笔回收了吗？预期哪章回收？
- 主角和某角色在第 150 章是什么关系？

`registry/` 登记的是"规划时的承诺"，不是"写到第 N 章的实际状态"。每章摘要补这层——**写后事实压缩**。这是 Bookie 此前的长程记忆缺口（2026-07-12 复盘 adoption-plan 盲点后补）。

## 产物位置

`drafts/chapters/<ch_id>/summary.md`

## 摘要内容（六字段，缺一不可）

1. **chapter_meta**：章号 / 标题 / 版本（V1/V2/V3）/ 字数 / stage（hook/development/...）
2. **what_happened**：本章实际发生了什么（3-5 句，事实层，不评价）
3. **character_state_changes**：角色状态变化（谁变强/变弱/关系变迁/受伤/死亡/资源增减）——每个变化引用角色 id
4. **foreshadowing_actions**：本章 **埋设** 的伏笔（id）/ **回收** 的伏笔（id）/ **推进** 的伏笔（id）
5. **promise_actions**：本章 **兑现** 的读者承诺（id）/ **新增** 承诺
6. **key_numbers**：关键数字（资金量级 / 等级 / 时间线节点）——用于跨章一致性检查

## 生成时机

- V1 草稿完成后生成（draft-v1 之后，必填）
- V3 定稿后最终更新（重大改动时）
- 不强制每版都更（V1 生成，V3 终更）

## 与 registry 的关系（核心：不造第二事实源）

| 层 | 位置 | 角色 | 性质 |
|---|---|---|---|
| 真源 | `registry/`（concepts/promises/foreshadowing） | 规划时的承诺 + 登记状态 | append-friendly，可审计 |
| 派生 | `drafts/chapters/<ch>/summary.md` | 写后的状态压缩（快照链） | 从正文派生，可重建 |

**registry 仍是真源**，summary 是"写到哪了"的快照链。summary 可从正文 + registry 重建，不是独立事实源。

**开放环回写**：summary 的 `foreshadowing_actions` / `promise_actions` 回写到 registry 对应条目的 `last_checked_chapter` + `current_status`（open/near_due/overdue/closed）——这让 registry 的开放环状态始终反映"写到第 N 章的实际进度"。

## Quality Gates

- 六字段齐全，无空字段
- `character_state_changes` 必须可追溯到正文场景（标注大致位置）
- `foreshadowing_actions` / `promise_actions` 的 id 必须在 registry 存在（不得发明新 id）
- `key_numbers` 必须与正文一致（跨章一致性检查的数据源）
- 摘要是事实压缩，不含评价（"写得好不好"归 review-chapter）

## 与 query-project-state 的对接（长程查询能力）

`/query-project-state` 查"角色 X 当前状态" / "伏笔 Y 开放环" 时：
1. 读 `registry/concepts.yaml`（角色基础设定，真源）
2. 聚合最近 N 章 `summary.md` 的 `character_state_changes`（状态变迁链）
3. 输出"角色 X 截至第 N 章的状态"

这让 Bookie 有 webnovel `query-entity-state --at-chapter N` 的能力，但用"registry + 摘要链"实现，不造 story-system 提交链。

## 与 review-chapter 的对接（跨章连贯）

`/review-chapter` 的 continuity 维度检查时：
1. 读前 1-2 章 `summary.md`（章首接续锚点是否对得上）
2. 读 registry/foreshadowing 的 `current_status`（开放环是否逾期未回收）
3. 检查本章 `key_numbers` 与前章一致（资金量级/等级不突变）

这让 Bookie 有 webnovel serial-continuity-checker 的能力。

## 适用范围

- **连载品类（网文/系列书）必填**：百万字长程记忆刚需
- **单本书可选**：短篇/单本不需要（outline + registry 足够）
- 由 active-pack 的 collaboration-mode（serial-review）或 brief 的 serial 标记触发
