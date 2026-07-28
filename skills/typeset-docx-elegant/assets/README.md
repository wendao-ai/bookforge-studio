# typeset-docx-elegant · assets

三个执行脚本（参考实现，源自 ai-tob-endgame 项目实战），配合 SKILL.md 的 Steps 使用：

| 脚本 | 对应 Step | 作用 |
|---|---|---|
| `build_book.py` | Step 2 | 整合全书 markdown（剥 header/footer 元块 + YAML 扉页 + 出版交稿说明 + 去章首引子标题 + 每章分页符） |
| `reference_gen.py` | Step 3 | 生成「思源宋体+Georgia」reference 模板（基于 `pandoc --print-default-data-file reference.docx` 的 base，含全部样式） |
| `post_process.py` | Step 5 | 后处理：给所有 Body Text/First Paragraph 段落加段落级 firstLineChars=200（officecli 查段落级，样式层不够，需双保险） |

## 复用到其他项目时的泛化要点

这三个脚本当前硬编码了 ai-tob-endgame 的路径与书名。复用到新项目时改三处：

1. **`build_book.py`**：`BASE`（项目根）→ 新项目根；`OUT` 书名 → 新书名；`ORDER` 章节列表（若章序/标题不同）
2. **`reference_gen.py`**：`OUT`（reference.docx 路径）→ 新项目 `typeset/reference.docx`；`BASE`（base.docx）同目录
3. **`post_process.py`**：`DOCX`（目标 docx）→ 新项目 docx 路径（建议改为 `sys.argv[1]` 参数化）

## 排版参数调整

字体 / 字号 / 行距 / 页边距 / 页码 全部在 `reference_gen.py` 顶部（`set_font` 调用），按 SKILL.md「排版规范」表修改即可（如出版社指定宋体，改 `ea='思源宋体'` → `ea='宋体'`）。
