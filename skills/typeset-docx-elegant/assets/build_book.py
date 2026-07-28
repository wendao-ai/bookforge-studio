#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""整合全书 markdown（出版社编辑审阅版）。

剥离各章 v3/v4 稿的 header/footer 写作过程元块，只留正文；用
`constitution/brief.yaml` 生成 front matter；每章标题优先取章节文件自身的
一级标题（`# ...`），否则回退为章节目录名。

用法:
    python build_book.py <project_dir> [version_prefix]

    project_dir      书稿项目目录（如 <workspace>/projects/<project-id>）。
                      省略时从 $CLAUDE_PROJECT_DIR/projects/$BOOKFORGE_PROJECT 推导。
    version_prefix    只取以该前缀开头的稿件文件名（如 "v4"）；省略时每章自动
                      取字典序最大的 v*_*.md（即最新版本）。
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - 环境缺 PyYAML 时给出清晰报错而非崩溃
    yaml = None


def resolve_project_dir() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    pid = os.environ.get("BOOKFORGE_PROJECT")
    if not pid:
        raise SystemExit(
            "用法: build_book.py <project_dir>，或设置 BOOKFORGE_PROJECT 环境变量"
        )
    return os.path.join(root, "projects", pid)


PROJECT_DIR = resolve_project_dir()
VERSION_PREFIX = sys.argv[2] if len(sys.argv) > 2 else None

FOOTER_RE = re.compile(r'^(> )?\*\*V[0-9].*(改写说明|一致性检查)')
# Pandoc DOCX 分页符（raw openxml 块，每章前插入，实现"每章新起一页"）
PAGE_BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'


def load_brief() -> dict:
    path = os.path.join(PROJECT_DIR, "constitution", "brief.yaml")
    if not yaml or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def latest_draft(chapter_dir: str) -> str | None:
    candidates = sorted(glob.glob(os.path.join(chapter_dir, "v*_*.md")))
    if VERSION_PREFIX:
        prefixed = [c for c in candidates if os.path.basename(c).startswith(VERSION_PREFIX)]
        if prefixed:
            return prefixed[-1]
    return candidates[-1] if candidates else None


def discover_chapters() -> list[tuple[str, str]]:
    chapters_root = os.path.join(PROJECT_DIR, "drafts", "chapters")
    if not os.path.isdir(chapters_root):
        return []
    items = []
    for ch in sorted(os.listdir(chapters_root)):
        ch_dir = os.path.join(chapters_root, ch)
        draft = latest_draft(ch_dir) if os.path.isdir(ch_dir) else None
        if draft:
            items.append((ch, draft))
    return items


def extract_title_and_body(path: str) -> tuple[str | None, str]:
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    title = next((l[2:].strip() for l in lines if l.startswith("# ") and not l.startswith("## ")), None)
    start = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
    if start is None:
        return title, ""
    foot = len(lines)
    for i in range(start, len(lines)):
        if FOOTER_RE.match(lines[i].strip()):
            foot = i
            break
    body = "\n".join(lines[start:foot]).rstrip()
    body = re.sub(r"\n+---\s*$", "", body)  # 去末尾孤立分隔线
    body = "\n".join(l for l in body.split("\n") if not l.startswith("## 章首引子"))  # 去章首引子小标题（保留引子正文）
    body = re.sub(r"\n{3,}", "\n\n", body)  # 压多余空行
    return title, body


def main() -> None:
    brief = load_brief()
    title = brief.get("title", "未命名书稿")
    subtitle = brief.get("subtitle", "")
    author = brief.get("author", "")
    version_label = VERSION_PREFIX or "定稿"
    out = os.path.join(PROJECT_DIR, "typeset", f"全书_{version_label}.md")

    parts = [
        f'''---
title: "{title}"
subtitle: "{subtitle}"
author: "{author}"
date: "{version_label} 交稿版"
---

'''
    ]

    chapters = discover_chapters()
    if not chapters:
        raise SystemExit(f"未在 {os.path.join(PROJECT_DIR, 'drafts', 'chapters')} 找到任何章节稿件")

    for ch, path in chapters:
        heading, body = extract_title_and_body(path)
        if not body:
            continue
        parts.append(f"{PAGE_BREAK}# {heading or ch}\n\n{body}\n")

    afterword_dir = os.path.join(PROJECT_DIR, "drafts", "afterword")
    afterword_draft = latest_draft(afterword_dir) if os.path.isdir(afterword_dir) else None
    if afterword_draft:
        heading, body = extract_title_and_body(afterword_draft)
        if body:
            parts.append(f"{PAGE_BREAK}# {heading or '后记'}\n\n{body}\n")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    content = open(out, encoding="utf-8").read()
    print(f"✓ 全书 markdown 已生成: {out}")
    print(f"  字符数: {len(content)}")
    print(f"  一级标题(#)数: {content.count(chr(10) + '# ')}")


if __name__ == "__main__":
    main()
