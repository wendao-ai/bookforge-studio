---
name: active-research
description: 实时研究支持，补充领域知识——触发场景：构思 阶段需要执行该操作时使用。
category: ideation
---

# /active-research

## Purpose

Gather targeted research context without letting research replace author decisions.

## Inputs

- Active project id from `BOOKFORGE_PROJECT` or project context.
- `projects/<project-id>/PROJECT.md`.
- Current stage artifacts relevant to `ideation`.
- Active Genre Pack metadata and rules when genre-specific behavior applies.
- Author instructions from the current session.

## Outputs

- Primary output: `constitution/` artifacts and project decisions.
- A short decision or action summary suitable for `.history/events.jsonl`.
- Any unresolved questions, risks, or human-review requirements.

## Steps

1. Load the active project and confirm the current stage.
2. Load the constitution, registry, active Genre Pack, and relevant prior artifacts.
3. Identify the exact artifact this skill is responsible for changing or producing.
4. Apply the workflow for `ideation` without changing unrelated project state.
5. Record decisions, confidence levels, and follow-up actions in the appropriate project file.
6. Run or request the relevant consistency, style, or stage gate checks.
7. Report what changed, what remains open, and the next recommended skill.

## Quality Gates

- The output is written to the expected project path.
- The result references the active Genre Pack when genre affects the work.
- Human approval is requested before creative cruxes or high-risk decisions.
- Critical consistency issues are not ignored.
- The skill leaves enough durable context for the next session to continue.

## Error Handling

- If no active project is configured, stop and ask for or create a project id.
- If required upstream artifacts are missing, name the missing files and do not fabricate them.
- If genre confidence is low, route to `/detect-genre` or `/switch-genre`.
- If toolchain support is missing, create a clear report instead of claiming success.
- If author intent conflicts with project memory, ask for confirmation and record the decision.
