# Human Collaboration Modes

Human approval intensity is configured per genre. Hooks and skills use this document plus `collaboration-mode.yaml` to decide when to pause.

## Mode Catalog

| Mode | Meaning | Examples |
| --- | --- | --- |
| `author-decides-worldview` | Author confirms core world laws and irreversible setting decisions | Science fiction |
| `expert-reviewed` | Domain expert must confirm accuracy-critical artifacts | Textbooks |
| `author-decides-emotional-contract` | Author confirms couple, ending, heat/sweet/bitter balance | Romance |
| `author-decides-historiography` | Author confirms viewpoint, source policy, and disputed interpretation | History |
| `editorial-review` | Author/editor confirms structure and theme before drafting | General fiction |
| `thesis-review` | Author confirms thesis, evidence standard, and argument frame | General nonfiction |

## Approval Events

Human approval is required for:

- genre confirmation,
- constitution finalization,
- primary structure selection,
- critical genre memory changes,
- stage transitions after critical or high-severity issues,
- final delivery.

## Recording Approval

Approvals should be recorded in the active project under either:

- `genre-context/genre-decisions/`, for genre-specific decisions.
- `.history/events.jsonl`, for stage and hook events.
- The relevant artifact frontmatter, when a document has a stable approval field.

## Non-Blocking Collaboration

Routine drafting, local polish, reader simulation, and format conversion can proceed without approval unless the active pack says otherwise.

## Failure Behavior

If a required approval is missing, hooks return exit code `2` and write a message naming the missing approval. They do not invent approval on the author's behalf.
