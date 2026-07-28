# Coordination Rules

BookForge agents operate as an editorial studio.

## Agent Layers

- Directors own strategy, stage transitions, and final quality.
- Stage leads own the six pipeline stages.
- Genre leads own genre-specific creative law.
- Specialists perform bounded tasks and report findings.

## Decision Flow

1. Stage lead frames the current objective.
2. Genre lead names active genre constraints.
3. Specialists produce candidate artifacts or checks.
4. Director resolves conflicts.
5. Human author approves creative cruxes.
6. Memory curator records durable decisions.

## Conflict Resolution

When agents disagree, prioritize:

1. Author-confirmed constitution.
2. Active genre critical rules.
3. Stage exit criteria.
4. Reader promise.
5. Local style preference.

## Artifact Ownership

- `constitution/`: Editorial Director and Lead Ideation.
- `outline/`: Lead Outline plus active Genre Lead.
- `extended-outline/`: Lead Extended Outline.
- `drafts/`: Lead Drafting plus relevant specialists.
- `review/`: Lead Review and reader simulators.
- `typeset/`: Lead Typeset.
- `genre-context/`: active Genre Lead and Memory Curator.
- `capability-library/`: Memory Curator.

## Reporting

All non-trivial agent output should name:

- input files used,
- decision made,
- confidence,
- files written,
- next recommended step.
