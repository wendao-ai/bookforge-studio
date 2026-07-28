---
name: start-book-project
description: 启动新书项目，从模糊想法到加载 Genre Pack；首次运行时自动在工作区搭好 projects/<project-id>/ 目录脚手架——触发场景：构思阶段需要执行该操作时使用，通常是一个工作区里第一个被调用的 skill。
category: ideation
---

# /start-book-project

## Purpose

Bootstrap a durable project workspace directory (from this plugin's bundled
template — the author's workspace does not need to pre-exist any of this)
and guide the author through initial idea capture. This is normally the
first skill run in a fresh workspace, so it owns creating the scaffolding
other skills assume exists.

## Inputs

- Active project id from `BOOKFORGE_PROJECT` env var, `projects/_current_project.yaml`,
  or a fresh id the author supplies (kebab-case; ask if none of the above resolve one).
- `projects/<project-id>/PROJECT.md` (created by this skill if the project is new).
- Current stage artifacts relevant to `ideation`.
- Active Genre Pack metadata and rules when genre-specific behavior applies.
- Author instructions from the current session.

## Outputs

- Primary output: `constitution/` artifacts and project decisions.
- A short decision or action summary suitable for `.history/events.jsonl`.
- Any unresolved questions, risks, or human-review requirements.

## Steps

1. **Resolve the project id.** Check `BOOKFORGE_PROJECT` env var, then
   `projects/_current_project.yaml`. If neither resolves one, this is a new
   project — ask the author for a short kebab-case id (e.g. `my-scifi-novel`).
2. **Bootstrap the project directory if it doesn't exist yet.** Copy
   `${CLAUDE_PLUGIN_ROOT}/projects-template/_template/` to
   `projects/<project-id>/` in the author's workspace (`$CLAUDE_PROJECT_DIR`,
   normally the current working directory). Do not hand-author the skeleton
   files — this plugin ships them; copy, don't recreate. Do not touch the
   `sample-*` directories in `projects-template/` — those are reference
   material for you to consult, never copy targets.
3. Write/update `projects/_current_project.yaml` with `project_id: <id>` so
   downstream hooks (`project-context-loader`, `genre-pack-loader`, etc.)
   pick up the active project automatically.
4. **Check workspace CLAUDE.md.** If `CLAUDE.md` at the workspace root is
   missing the BookForge operating principles (no mention of "Genre Pack" /
   "genre-context/active-pack.yaml"), tell the author and offer to append
   the block from `${CLAUDE_PLUGIN_ROOT}/docs/operating-principles.md`.
   Append only after the author confirms — this file is theirs, don't
   overwrite existing content silently.
   (`capability-library/` at the workspace root does not need manual setup:
   the `session-start` hook already bootstraps it from the plugin's
   `capability-library-template/` the first time a session starts in a
   workspace that doesn't have one yet.)
5. Load the constitution, registry, active Genre Pack, and relevant prior
   artifacts.
6. Identify the exact artifact this skill is responsible for changing or
   producing.
7. Apply the workflow for `ideation` without changing unrelated project
   state.
8. Record decisions, confidence levels, and follow-up actions in the
   appropriate project file.
9. Run or request the relevant consistency, style, or stage gate checks.
10. Report what changed, what remains open, and the next recommended skill.

## Quality Gates

- `projects/<project-id>/` exists and was copied from the plugin template,
  not hand-authored from scratch.
- The output is written to the expected project path.
- The result references the active Genre Pack when genre affects the work.
- Human approval is requested before creative cruxes or high-risk decisions,
  and before appending to the author's own `CLAUDE.md`.
- Critical consistency issues are not ignored.
- The skill leaves enough durable context for the next session to continue.

## Error Handling

- If no active project is configured and the author gives no id, stop and
  ask — do not silently invent one.
- If `${CLAUDE_PLUGIN_ROOT}/projects-template/_template/` is missing (e.g.
  a corrupted install), report that clearly instead of fabricating a
  skeleton by hand.
- If required upstream artifacts are missing, name the missing files and do
  not fabricate them.
- If genre confidence is low, route to `/detect-genre` or `/switch-genre`.
- If toolchain support is missing, create a clear report instead of
  claiming success.
- If author intent conflicts with project memory, ask for confirmation and
  record the decision.
