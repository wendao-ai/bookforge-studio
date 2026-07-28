---
description: "Chapter draft version standards"
globs:
  - "projects/*/drafts/chapters/**"
---

# Chapter Draft Rules

## Mandatory Standards

- Drafts evolve through `v0_skeleton.md`, `v1_rough.md`, `v2_refined.md`, and `v3_polished.md`.
- V0 records structure only; V1 expands content; V2 resolves logic and genre consistency; V3 polishes voice and reader experience.
- Each version must identify the source chapter plan and active style anchor.
- Critical consistency checks must pass before V3 is considered ready for review.
- Major changes after V3 must create a new revision note or snapshot.
- 版本升级必须创建新文件（`cp` 旧版本 + Edit 新版本），禁止在旧版本文件上直接 Edit + `mv`——每个版本（V0/V1/V2/V3）必须保留独立快照，保证版本链可追溯。

## Anti-Patterns

- Overwriting polished drafts without preserving review context.
- Jumping directly to V3 for long chapters.
- Fixing consistency by silently changing genre memory.
- Letting style drift between chapters without updating style anchors.
- 在旧版本文件上直接 Edit + `mv`（破坏上一版本快照，版本链断裂）。必须 `cp` 新文件后再 Edit。
