#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""后处理：给所有正文段落（Body Text/First Paragraph）加段落级首行缩进(2字符)。
双保险——样式层已设，段落层也设，确保 Word 与 officecli 都识别。

用法:
    python post_process.py <docx_path>

    docx_path  要后处理的精排 docx 文件路径。省略时取
                <project_dir>/typeset/ 下最新修改的 .docx（project_dir 由
                $CLAUDE_PROJECT_DIR/projects/$BOOKFORGE_PROJECT 推导）。
    结果原地覆盖写回 docx_path（你自己的工作区文件），不写入插件目录。
"""
import glob
import os
import sys

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def resolve_docx_path() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    pid = os.environ.get("BOOKFORGE_PROJECT")
    if not pid:
        raise SystemExit(
            "用法: post_process.py <docx_path>，或设置 BOOKFORGE_PROJECT 环境变量"
        )
    typeset_dir = os.path.join(root, "projects", pid, "typeset")
    candidates = sorted(glob.glob(os.path.join(typeset_dir, "*.docx")), key=os.path.getmtime)
    if not candidates:
        raise SystemExit(f"未在 {typeset_dir} 找到任何 .docx，请显式传入路径")
    return candidates[-1]


DOCX = resolve_docx_path()

doc = Document(DOCX)
n = 0
for p in doc.paragraphs:
    sn = p.style.name if p.style else ''
    if sn in ('Body Text', 'First Paragraph'):
        pPr = p._p.get_or_add_pPr()
        ind = pPr.find(qn('w:ind'))
        if ind is None:
            ind = OxmlElement('w:ind')
            pPr.append(ind)
        ind.set(qn('w:firstLineChars'), '200')  # 2 字符
        ind.set(qn('w:firstLine'), '480')  # 24pt（twips）
        n += 1
doc.save(DOCX)
print(f"✓ 给 {n} 个正文段落加段落级首行缩进（2 字符），文件: {DOCX}")
