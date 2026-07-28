#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/select-outline-candidate 结构验证器（由 studio-architect build_eval_set.py 生成）。

Tier 1 结构 gate：检查 skill 包的完整性。
  1. SKILL.md 存在且 frontmatter 有效（name/description）
  2. description 含核心触发词
  3. body 含必需章节
  4. examples 目录存在（有 golden sample 更佳）

用法：
  python3 evals/validate_skill.py
  python3 evals/validate_skill.py --strict   # 警告也视为失败

退出码：0=通过，1=有错误（或 --strict 下有警告）
"""
import sys
import re
from pathlib import Path

# skill 根目录 = 本脚本的上两级（evals/validate_skill.py → skill 根）
SKILL_ROOT = Path(__file__).resolve().parent.parent

# 触发词（build_eval_set.py 从 description 提取或用 skill name 填充）
TRIGGER_WORDS = ["/select-outline-candidate", "选择大纲候选"]

# 必需章节
REQUIRED_SECTIONS = ["Overview", "Steps", "Quality Gates"]


def log(level, msg):
    prefix = {"ERROR": "X", "WARN": "!", "OK": "OK", "INFO": "-"}.get(level, "  ")
    print(f"[{prefix}] {msg}")
    return level


def validate_frontmatter():
    errors, warns = [], []
    skill_md = SKILL_ROOT / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md 不存在")
        return errors, warns
    content = skill_md.read_text(encoding="utf-8")

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        errors.append("SKILL.md 缺少 YAML frontmatter（--- ... ---）")
        return errors, warns
    fm = m.group(1)

    if not re.search(r"^name:\s*\S+", fm, re.MULTILINE):
        errors.append("frontmatter 缺少 name 字段")
    if not re.search(r"^description:\s*", fm, re.MULTILINE):
        errors.append("frontmatter 缺少 description 字段")
    else:
        desc_match = re.search(r"^description:\s*(.+?)(?=\n[a-zA-Z_]+:|\Z)", fm, re.MULTILINE | re.DOTALL)
        desc = desc_match.group(1) if desc_match else ""
        if TRIGGER_WORDS:
            if not any(t in desc for t in TRIGGER_WORDS):
                warns.append(f"description 未检测到核心触发词：{TRIGGER_WORDS}")
    return errors, warns


def validate_sections():
    errors, warns = [], []
    skill_md = SKILL_ROOT / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md 不存在")
        return errors, warns
    content = skill_md.read_text(encoding="utf-8")
    for sec in REQUIRED_SECTIONS:
        # 匹配 ## 或 ### 标题
        pat = rf"^#{{2,3}}\s*{re.escape(sec)}"
        if not re.search(pat, content, re.MULTILINE):
            errors.append(f"缺少必需章节：{sec}")
    return errors, warns


def validate_examples():
    # examples 可能在 skill 根目录或 evals/examples/（build_eval_set 生成位置）
    errors, warns = [], []
    candidates = [SKILL_ROOT / "examples", SKILL_ROOT / "evals" / "examples"]
    ex_dir = next((d for d in candidates if d.is_dir()), None)
    if ex_dir is None:
        # examples 缺失只是 INFO（golden sample 是手动积累的，首次生成时缺失正常）
        return errors, warns
    samples = [f for f in ex_dir.glob("*.md") if f.name != "README.md"]
    if not samples:
        # 无 golden sample 只是 INFO，不阻塞 strict
        return errors, warns
    return errors, warns


def main():
    strict = "--strict" in sys.argv
    all_errors, all_warns = [], []

    for fn in [validate_frontmatter, validate_sections, validate_examples]:
        e, w = fn()
        all_errors.extend(e)
        all_warns.extend(w)

    print(f"\n=== /select-outline-candidate 结构验证 ===")
    print(f"根目录：{SKILL_ROOT}\n")

    for e in all_errors:
        log("ERROR", e)
    for w in all_warns:
        log("WARN", w)

    if not all_errors and not all_warns:
        log("OK", "全部检查通过")

    print()
    if all_errors:
        log("ERROR", f"共 {len(all_errors)} 个错误")
        sys.exit(1)
    if strict and all_warns:
        log("WARN", f"--strict 模式：{len(all_warns)} 个警告视为失败")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
