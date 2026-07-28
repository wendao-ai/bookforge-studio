# Capability Library（能力库模板）

跨项目写作模式沉淀，按类型分区。每本书的写作模式沉淀进这里，让后续同类型项目站在前面项目的肩膀上。

## 使用方式

这是一个**空骨架模板**，不是插件运行时依赖的目录。首次在你自己的工作区（`$CLAUDE_PROJECT_DIR`，即你存放 `projects/` 的地方）里启用 BookForge Studio 时，把整个 `capability-library-template/` 复制为工作区根目录下的 `capability-library/`：

```bash
cp -R <plugin>/capability-library-template ./capability-library
```

之后 `capability-harvest-trigger` hook 与 `/capability-audit` skill 都会读写这个位于你工作区根目录的 `capability-library/`，而不是插件安装目录里的模板——插件本身不携带任何真实项目沉淀的资产。

## 分区

- `by-genre/<genre>/` — 按类型分区（`biography`/`fiction-general`/`history`/`nonfiction-general`/`romance`/`scifi`/`textbook`/`webnovel`，与内置 Genre Pack 一一对应）
- `cross-genre/` — 跨类型通用模式
- `author-preferences/` — 用户偏好学习（区分稳定偏好与一次性项目决定，参见 `rules/capability-asset.md`）

## 规范

写入前请遵守插件 `rules/capability-asset.md` 的强制标准：记录来源项目、类型、解决的问题、可复用模式、成功证据与局限性；不要把整章正文倒进这里。
