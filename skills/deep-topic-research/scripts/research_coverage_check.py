#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research_coverage_check.py — deep-topic-research 调研充分性校验

扫描 projects/<project-id>/research/ 目录，按主题复杂度（light/medium/heavy）
判定调研是否达到门槛，产出报告。不达标标 knowledge_coverage: insufficient。

仅校验"调研充分性"维度（检索操作数 / 一手全文精读 / 来源类型覆盖），
不涉及正文结构（那是 draft-v* 与 genre pack 的职责）。

纯 Python 3 标准库，无第三方依赖。

用法:
    python3 research_coverage_check.py --out projects/<id>/research --complexity heavy
    python3 research_coverage_check.py --out projects/<id>/research --complexity medium --json
    python3 research_coverage_check.py --out projects/<id>/research --strict   # 不达标 exit 1
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# 复杂度门槛表（对应 references/deep-research-doctrine.md §2）
# (min_queries, min_fulltext, min_source_types)
THRESHOLDS = {
    "light": {"queries": 30, "fulltext": 3, "source_types": 3},
    "medium": {"queries": 80, "fulltext": 5, "source_types": 3},
    "heavy": {"queries": 150, "fulltext": 8, "source_types": 4},
}

# 合法的来源类型（对应 research/sources/ 子目录）
SOURCE_TYPES = {"academic", "cases", "cross-domain", "anchor-assets", "realtime"}


def count_executed_queries(log_path: Path) -> int:
    """
    统计 research-log.md「检索账本」表格中实际执行的 query 数。
    计数规则：表格内每条以 | 开头、含日期模式（YYYY-MM-DD）的数据行算一条。
    表头与分隔行（---）不计。
    """
    if not log_path.is_file():
        return 0
    text = log_path.read_text(encoding="utf-8", errors="replace")

    # 定位「检索账本」段落到下一个二级标题之前
    section = re.search(
        r"##\s*检索账本(.*?)(?:\n##\s|\Z)", text, re.DOTALL
    )
    body = section.group(1) if section else text

    count = 0
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # 跳过分隔行 |---|---|
        if re.match(r"^\|[\s:\-\|]+\|$", stripped):
            continue
        # 跳过表头行（含「query」「检索」字样且无日期）
        if re.search(r"\d{4}-\d{2}-\d{2}", stripped):
            count += 1
    return count


def count_source_notes(sources_dir: Path):
    """
    统计 sources/ 下的 source-note 数量与来源类型覆盖。
    返回 (total_notes, covered_types_set)。
    每个子目录代表一类源；子目录内有 .md 文件才算该类被覆盖。
    """
    total = 0
    covered = set()
    if not sources_dir.is_dir():
        return total, covered

    for child in sources_dir.iterdir():
        if not child.is_dir():
            continue
        # 目录名映射到标准来源类型
        dirname = child.name.lower()
        type_key = dirname.replace("_", "-")
        md_files = list(child.glob("*.md"))
        if md_files:
            total += len(md_files)
            covered.add(type_key if type_key in SOURCE_TYPES else dirname)
    return total, covered


def evaluate(research_dir: Path, complexity: str) -> dict:
    """评估调研充分性，返回结果 dict。"""
    threshold = THRESHOLDS[complexity]
    log_path = research_dir / "research-log.md"
    sources_dir = research_dir / "sources"

    queries = count_executed_queries(log_path)
    fulltext, covered_types = count_source_notes(sources_dir)

    checks = {
        "queries": {
            "actual": queries,
            "threshold": threshold["queries"],
            "pass": queries >= threshold["queries"],
        },
        "fulltext": {
            "actual": fulltext,
            "threshold": threshold["fulltext"],
            "pass": fulltext >= threshold["fulltext"],
        },
        "source_types": {
            "actual": len(covered_types),
            "covered": sorted(covered_types),
            "threshold": threshold["source_types"],
            "pass": len(covered_types) >= threshold["source_types"],
        },
    }

    all_pass = all(c["pass"] for c in checks.values())
    coverage = "sufficient" if all_pass else "insufficient"

    return {
        "research_dir": str(research_dir),
        "complexity": complexity,
        "threshold": threshold,
        "checks": checks,
        "knowledge_coverage": coverage,
        "pass": all_pass,
    }


def render_text(result: dict) -> str:
    """渲染人类可读报告。"""
    lines = []
    lines.append("=" * 60)
    lines.append("调研充分性校验报告（deep-topic-research）")
    lines.append("=" * 60)
    lines.append(f"调研目录 : {result['research_dir']}")
    lines.append(f"复杂度   : {result['complexity']}")
    lines.append("")
    lines.append("检查项                          实际/门槛   结果")
    lines.append("-" * 60)

    q = result["checks"]["queries"]
    f = result["checks"]["fulltext"]
    s = result["checks"]["source_types"]

    lines.append(
        f"检索操作数                      {q['actual']:>4}/{q['threshold']:<4} "
        f"{'✅' if q['pass'] else '❌'}"
    )
    lines.append(
        f"一手全文精读                    {f['actual']:>4}/{f['threshold']:<4} "
        f"{'✅' if f['pass'] else '❌'}"
    )
    lines.append(
        f"来源类型覆盖                    {s['actual']:>4}/{s['threshold']:<4} "
        f"{'✅' if s['pass'] else '❌'}"
    )
    lines.append(f"  已覆盖源类型: {', '.join(s['covered']) or '(无)'}")
    lines.append("-" * 60)

    cov = result["knowledge_coverage"]
    flag = "✅ sufficient" if cov == "sufficient" else "❌ insufficient"
    lines.append(f"knowledge_coverage : {flag}")

    if cov == "insufficient":
        lines.append("")
        lines.append("⚠️  调研不充分。按 deep-research-doctrine 原则 4（诚实降级）：")
        lines.append("    - 禁止把本主题回填为高置信核心论点")
        lines.append("    - 补调研，或在 brief 标注 partial 并降级结论置信度")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="deep-topic-research 调研充分性校验"
    )
    parser.add_argument(
        "--out",
        required=True,
        help="research/ 目录路径（含 research-log.md 与 sources/）",
    )
    parser.add_argument(
        "--complexity",
        choices=list(THRESHOLDS.keys()),
        default="heavy",
        help="主题复杂度，决定门槛（默认 heavy：跨学科/产业级/强争议）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON（便于其他工具消费）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="不达标时以非零状态码退出（用于 gate 拦截）",
    )
    args = parser.parse_args()

    research_dir = Path(args.out).resolve()
    if not research_dir.is_dir():
        msg = (
            f"❌ 调研目录不存在: {research_dir}\n"
            f"   请先按 deep-topic-research SKILL 创建 research/ 工作台。"
        )
        if args.json:
            print(json.dumps(
                {"error": "research_dir_missing", "path": str(research_dir)},
                ensure_ascii=False, indent=2,
            ))
        else:
            print(msg)
        sys.exit(2)

    result = evaluate(research_dir, args.complexity)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))

    if args.strict and not result["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
