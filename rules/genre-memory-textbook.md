---
description: "Textbook genre memory standards"
globs:
  - "projects/*/genre-context/genre-memory/knowledge-dag/**"
---

# Textbook Genre Memory Rules

## Mandatory Standards

- Knowledge nodes must include concept id, definition, prerequisites, learning objective, Bloom level, and assessment link.
- Prerequisite edges must distinguish hard prerequisites from helpful background.
- Exercises must map to concepts and expected cognitive level.
- Expert review is required for final knowledge claims, examples, and answer keys.
- Circular dependencies are critical violations.

## Anti-Patterns

- Introducing concepts before prerequisites.
- Creating exercises that test unstated knowledge.
- Using examples that add hidden assumptions.
- Treating curriculum order as a prose preference rather than a graph constraint.
