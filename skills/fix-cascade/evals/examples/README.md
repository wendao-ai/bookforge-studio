# Golden Samples

此目录存放 /fix-cascade 的 golden sample（历史最佳输出），作为回归基准。

## 用途

- **回归对照**：skill 调整后，重新跑相同输入，对比输出是否偏离 golden
- **未来 Tier 3 LLM-as-Judge**：用 golden sample 作为评分参照（clarity/completeness/actionability）

## 如何积累

1. 首次跑 /fix-cascade 产生满意输出后，将输出文件复制到此目录
2. 文件命名：`sample-<场景描述>.md`（如 `sample-典型客户简报场景.md`）
3. 在文件头部注明：输入摘要 + 为什么这是 golden（满足哪些质量标准）

## 当前状态

- [ ] 尚无 golden sample（首次使用后请补充）
