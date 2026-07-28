# Genre Pack Protocol

Genre Packs encode the creative laws for each book type. They are loaded after ideation and remain active until an explicit genre switch is approved.

## Required Components

Each `genre-packs/<genre>/` directory must contain:

1. `PACK.md` with metadata, detection signals, challenges, agents, memory extensions, collaboration mode, and quality focus.
2. `agents/` with the genre lead and specialists.
3. `skills/` with genre-specific workflows.
4. `memory-schema.yaml` describing project memory extensions.
5. `structure-paradigm.yaml` describing the book structure model.
6. `reader-profiles.yaml` with at least three target reader profiles.
7. `quality-metrics.yaml` with measurable review dimensions.
8. `collaboration-mode.yaml` defining human approval requirements.
9. `consistency-rules.yaml` with at least one critical rule.

Optional but recommended:

- `templates/` for genre-specific artifacts.
- `knowledge/` for tropes, methods, references, and examples.

## Loading Flow

1. `genre-detector` proposes `primary_genre`, optional `secondary_genre`, `sub_genre`, and confidence.
2. The author confirms the genre decision.
3. `genre-pack-loader.sh` checks the registry and pack completeness.
4. The active project records the pack in `genre-context/active-pack.yaml`.
5. Required genre memory directories are initialized.
6. Stage skills consult the active pack before creating downstream artifacts.

## Mixed Genres

Mixed genres use one primary pack and one optional secondary pack. The primary pack owns structure and critical consistency. The secondary pack can add memory, reader profiles, and quality metrics. If the packs conflict, the Director layer resolves the priority and records the decision in `genre-context/genre-decisions/`.

## Switching Genres

Genre switching is allowed only during ideation or outline unless the author approves a backtrack. A switch must record:

- Original genre and new genre.
- Reason for switch.
- Artifacts requiring regeneration.
- Human approval.

## Pack Completion Criteria

A pack is usable when all required components exist, required YAML parses cleanly, all listed specialist agents have files, and every critical consistency rule has an action.
