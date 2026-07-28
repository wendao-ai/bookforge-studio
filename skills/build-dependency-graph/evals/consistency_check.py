#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""七维度一致性校验（通用版，由 studio-architect build_eval_set.py 生成）。

Tier 2.5 一致性 gate：校验 skill 的 SKILL.md 在系统内的一致性。
参考 deep-mastery-researcher/scripts/consistency_check.py 的七维 gate 范式，
裁剪为单 skill 检查、纯 Python 标准库、支持 --strict 做 gate。

七维度：
  1. frontmatter 有效性   name/description/category 字段存在且非空
  2. 章节完整性           Overview/Steps/Quality Gates 等必需章节存在
  3. 交叉引用可达性       [text](path) 链接的 path 文件存在
  4. 术语引用（弱）       如有 --glossary，检查 SKILL.md 是否引用术语表
  5. 否定边界声明         description 或 body 含否定边界关键词
  6. Agent 引用有效性     agents 字段的每个角色在 --agents-dir 有对应 .md
  7. Quality Gates 可量化 Quality Gates 表格行含量化词

用法：
  python3 evals/consistency_check.py
  python3 evals/consistency_check.py --strict
  python3 evals/consistency_check.py --glossary ../terms.md --agents-dir ../../agents

退出码：0=通过（或仅警告），1=有错误（或 --strict 下有警告）
"""
import argparse
import re
import sys
from pathlib import Path

# skill 根目录 = 本脚本的上两级（evals/consistency_check.py → skill 根）
SKILL_ROOT = Path(__file__).resolve().parent.parent

# 必需章节（## 或 ### 标题）
REQUIRED_SECTIONS = ["Overview", "Steps", "Quality Gates"]

# 否定边界关键词
NEGATIVE_BOUNDARY_KEYWORDS = [
    "不负责", "不创建", "不做", "不属于", "不处理", "不在本",
    "not responsible", "does not", "doesn't create",
]

# Quality Gates 量化词（含数字 / "至少" / "必须" / ≥ / > 等）
QUANTITATIVE_PATTERN = re.compile(
    r"(\d+|至少|必须|≥|<=?|>=?|不少于|不超过|全部|所有)"
)

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def log(level, msg):
    prefix = {"ERROR": "X", "WARN": "!", "OK": "OK", "INFO": "-"}.get(level, "  ")
    print(f"[{prefix}] {msg}")
    return level


def load_skill_md():
    skill_md = SKILL_ROOT / "SKILL.md"
    if not skill_md.exists():
        return None, ""
    return skill_md, skill_md.read_text(encoding="utf-8")


def parse_frontmatter(content):
    m = FRONTMATTER_PATTERN.match(content)
    if not m:
        return None
    fm_text = m.group(1)
    fm = {}
    # 简单解析：key: value 或 key: \n  - item
    for line in fm_text.splitlines():
        m2 = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m2:
            key, val = m2.group(1), m2.group(2).strip()
            if val:
                fm[key] = val
    # agents 字段（YAML list，去掉行内 # 注释）
    agents_match = re.findall(r"^agents:\s*\n((?:\s*-\s*.+\n?)+)", fm_text, re.MULTILINE)
    if agents_match:
        agents = []
        for raw in re.findall(r"-\s*(.+)$", agents_match[0], re.MULTILINE):
            agent = raw.split("#")[0].strip().strip('"').strip("'")
            if agent:
                agents.append(agent)
        fm["agents"] = agents
    return fm


# === 七维检查 ===

def check_frontmatter(content):
    """维度 1：frontmatter 有效性"""
    errors, warns = [], []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append("缺少 YAML frontmatter（--- ... ---）")
        return errors, warns
    for field in ["name", "description"]:
        if not fm.get(field):
            errors.append(f"frontmatter 缺少 {field} 字段或为空")
    if not fm.get("category"):
        warns.append("frontmatter 缺少 category 字段（建议补充以便系统分类）")
    return errors, warns


def check_sections(content):
    """维度 2：章节完整性"""
    errors, warns = [], []
    for sec in REQUIRED_SECTIONS:
        pat = rf"^#{{2,3}}\s*{re.escape(sec)}"
        if not re.search(pat, content, re.MULTILINE):
            errors.append(f"缺少必需章节：## {sec}")
    return errors, warns


def check_links(content):
    """维度 3：交叉引用可达性"""
    errors, warns = [], []
    broken = []
    for m in LINK_PATTERN.finditer(content):
        link = m.group(2).strip()
        if link.startswith(("http", "#", "mailto:")) or link.startswith("{"):
            continue
        target = (SKILL_ROOT / link).resolve()
        if not target.exists():
            broken.append((m.group(1)[:30], link))
    if broken:
        for text, link in broken[:5]:
            errors.append(f"断链：[{text}]({link})")
    return errors, warns


def check_glossary_ref(content, glossary_path):
    """维度 4：术语引用（弱）—— 检查 SKILL.md 是否引用了 glossary 文件"""
    errors, warns = [], []
    if not glossary_path:
        return errors, warns  # 未提供 glossary 则跳过（INFO，不算问题）
    gname = Path(glossary_path).name
    # 检查 SKILL.md 是否提及 glossary 文件名或路径片段
    candidates = [gname, str(Path(glossary_path).stem)]
    if not any(c in content for c in candidates):
        warns.append(f"SKILL.md 未引用系统术语表（{gname}）—— 建议在必备上下文中引用")
    return errors, warns


def check_negative_boundary(content):
    """维度 5：否定边界声明"""
    errors, warns = [], []
    # 检查 description（frontmatter 内）和 body
    fm = parse_frontmatter(content)
    desc = (fm or {}).get("description", "")
    body = content
    has_boundary_in_desc = any(k in desc for k in NEGATIVE_BOUNDARY_KEYWORDS)
    has_boundary_in_body = any(k in body for k in NEGATIVE_BOUNDARY_KEYWORDS)
    if not has_boundary_in_desc and not has_boundary_in_body:
        warns.append("未检测到否定边界声明（建议在 description 或运营规则中声明'不负责什么'）")
    return errors, warns


def check_agent_refs(content, agents_dir):
    """维度 6：Agent 引用有效性"""
    errors, warns = [], []
    if not agents_dir:
        return errors, warns  # 未提供 agents-dir 则跳过
    fm = parse_frontmatter(content)
    agents = (fm or {}).get("agents", [])
    if not agents:
        return errors, warns  # 无 agents 字段则跳过
    agents_path = Path(agents_dir)
    for agent in agents:
        agent = agent.strip().strip('"').strip("'")
        if not agent:
            continue
        # 查找 <agents_dir>/<agent>.md
        agent_file = agents_path / f"{agent}.md"
        if not agent_file.exists():
            errors.append(f"agents 字段引用的 Agent 不存在：{agent}（{agent_file}）")
    return errors, warns


def check_quality_gates_quant(content):
    """维度 7：Quality Gates 可量化"""
    errors, warns = [], []
    # 提取 Quality Gates 章节
    m = re.search(r"^##\s*Quality Gates\s*$\n(.*?)(?=^##\s|\Z)", content, re.MULTILINE | re.DOTALL)
    if not m:
        return errors, warns  # 章节缺失由维度 2 处理
    section = m.group(1)
    # 统计表格行（| ... |）
    rows = [r for r in section.splitlines() if r.strip().startswith("|") and not re.match(r"^\|[|\s-]+\|?$", r.strip())]
    if not rows:
        warns.append("Quality Gates 章节无表格内容（建议用表格列出可量化检查项）")
        return errors, warns
    # 至少一半的行应含量化词
    quant_rows = [r for r in rows if QUANTITATIVE_PATTERN.search(r)]
    if len(quant_rows) < max(1, len(rows) // 2):
        warns.append(
            f"Quality Gates 仅 {len(quant_rows)}/{len(rows)} 行含量化标准（建议用'至少 X 条''必须包含 Y'等可判断标准）"
        )
    return errors, warns


def main():
    p = argparse.ArgumentParser(description="skill 七维度一致性校验（通用版）")
    p.add_argument("--strict", action="store_true", help="警告也视为失败")
    p.add_argument("--glossary", help="系统术语表文件路径（可选）")
    p.add_argument("--agents-dir", help="Agent 目录路径（可选，校验 agents 字段引用）")
    args = p.parse_args()

    skill_md, content = load_skill_md()
    print(f"\n=== 一致性校验（七维）===")
    print(f"Skill 根：{SKILL_ROOT}\n")

    if skill_md is None:
        log("ERROR", "SKILL.md 不存在")
        sys.exit(1)

    all_errors, all_warns = [], []
    checks = [
        ("维度1 frontmatter", check_frontmatter(content)),
        ("维度2 章节完整性", check_sections(content)),
        ("维度3 交叉引用", check_links(content)),
        ("维度4 术语引用", check_glossary_ref(content, args.glossary)),
        ("维度5 否定边界", check_negative_boundary(content)),
        ("维度6 Agent引用", check_agent_refs(content, args.agents_dir)),
        ("维度7 QualityGates量化", check_quality_gates_quant(content)),
    ]
    for name, (e, w) in checks:
        if e:
            print(f"\n{name}:")
            for msg in e:
                log("ERROR", msg)
        all_errors.extend(e)
        all_warns.extend(w)

    if all_warns:
        print(f"\n[警告]")
        for w in all_warns:
            log("WARN", w)

    if not all_errors and not all_warns:
        print("\n[OK] 七维度全部通过")

    print(f"\n汇总：{len(all_errors)} 错误，{len(all_warns)} 警告")
    if all_errors:
        sys.exit(1)
    if args.strict and all_warns:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
