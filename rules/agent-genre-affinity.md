---
description: "Agent genre affinity and frontmatter standards"
globs:
  - ".claude/agents/**"
  - "genre-packs/*/agents/**"
---

# Agent Genre Affinity

## Mandatory Standards

- Every agent file must include YAML frontmatter.
- Shared agents use `genre: "shared"`.
- Genre-specific agents use the owning Pack id, for example `genre: "scifi"`.
- Agents must declare `name`, `role`, `model`, `genre`, `domain`, and `reports_to`.
- Agents that write memory must declare `memory_access.write`.
- Any decision requiring human approval must appear under `authority.requires_approval`.

## Anti-Patterns

- A scifi agent writing textbook knowledge DAG files.
- Omitting `genre` and relying on filename inference.
- Granting autonomous authority for worldview, historiography, expert-accuracy, or final thesis decisions.
- Reporting to an agent that does not exist.
