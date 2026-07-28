# Context Management

Long-form book creation cannot rely on chat memory alone. Durable state belongs in project files.

## Context Layers

| Layer | Location | Purpose |
| --- | --- | --- |
| Working context | Current Claude session | Immediate task and local reasoning |
| Project memory | `projects/<project-id>/` | Constitution, outline, registry, drafts, review, typeset |
| Genre memory | `projects/<project-id>/genre-context/genre-memory/` | World bible, knowledge DAG, relationship state, source archive |
| Long-term memory | `capability-library/` | Reusable patterns and author preferences |

## Before Drafting

Load:

- `PROJECT.md`
- `constitution/brief.yaml`
- active pack metadata
- current outline or chapter plan
- relevant registry files
- relevant genre memory.

## Before Review

Load:

- V3 chapter drafts,
- reader profiles,
- quality metrics,
- unresolved consistency findings,
- style anchors.

## Before Compacting

Persist:

- current project id,
- active stage,
- active chapter,
- unresolved decisions,
- pending human approvals,
- changed files.

## Region-Read Protocol

Long reference files (rules, docs, genre-pack knowledge, research notes, style corpus) must be read by segment, not swallowed whole. This protects the context budget and makes the Context Layers above load on demand rather than all at once.

The protocol, applied whenever a skill loads a reference file longer than ~200 lines during Before Drafting / Before Review / Before Compacting:

1. **Locate first.** Run a `Grep` for heading anchors (typically `^#{1,3} `) to find the line numbers of the target section.
2. **Read by segment.** Use `Read` with `offset` and `limit` to pull only the target section, not the whole file.
3. **Never swallow whole.** Do not `cat` an entire long file, and do not `Read` a long reference without a `limit`. Full-file reads are reserved for short files or when the whole file is genuinely the unit of work.
4. **Cite the source segment.** When a loaded segment informs a decision, reference it by file path and heading, so the next session can re-locate it.

This is a universal discipline inherited by every skill; it does not need to be repeated in each skill's Steps.

## Anti-Drift Rule

If chat and project files disagree, project files win unless the author explicitly says the chat decision supersedes them. Record the superseding decision immediately.
