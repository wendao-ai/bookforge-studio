---
description: "Typeset output standards"
globs:
  - "projects/*/typeset/**"
---

# Typeset Output Rules

## Mandatory Standards

- Typeset output must include metadata: title, author, genre, version, export date, and source chapters.
- DOCX and EPUB exports use Pandoc when available.
- PDF export must detect Typst or LaTeX before attempting generation.
- Missing export engines must produce a clear report instead of a silent failure.
- Final exports must be generated from approved V3 or later chapter drafts.

## Anti-Patterns

- Manual copy/paste export without source trace.
- Marking PDF complete when the engine is missing.
- Exporting mixed chapter versions.
- Losing citations, footnotes, exercises, or genre-specific front matter.
