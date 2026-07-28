#!/usr/bin/env python3
"""Shared runtime for BookForge Studio Claude Code plugin hooks.

Two roots matter here and must not be confused:

- PROJECT_ROOT: the author's own workspace (where they keep `projects/`,
  `capability-library/`, and any project-local `.claude/` overrides). This is
  `$CLAUDE_PROJECT_DIR` when Claude Code sets it, otherwise the current
  working directory.
- PLUGIN_ROOT: where this plugin is installed (where the bundled
  `genre-packs/` definitions live). This is `$CLAUDE_PLUGIN_ROOT`, with a
  local-checkout fallback so the script also works when run directly from a
  clone of this repo during development.
"""

from __future__ import annotations

import json
import os
import re
import select
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def _project_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env).resolve() if env else Path.cwd().resolve()


def _plugin_root() -> Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return Path(env).resolve()
    # Local-checkout fallback: scripts/bookforge_hook.py -> plugin root
    return Path(__file__).resolve().parents[1]


PROJECT_ROOT = _project_root()
PLUGIN_ROOT = _plugin_root()


def load_yaml(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return default
    return yaml.safe_load(text) or default


def parse_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def read_stdin_json() -> dict[str, Any]:
    if sys.stdin.isatty():
        return {}
    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if not ready:
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_stdin": raw}


def project_id_from_env_or_file() -> str | None:
    env = os.environ.get("BOOKFORGE_PROJECT") or os.environ.get("CURRENT_PROJECT")
    if env:
        return env.strip()
    current = load_yaml(PROJECT_ROOT / "projects" / "_current_project.yaml", {})
    if isinstance(current, dict):
        value = current.get("project_id") or current.get("current_project")
        if value:
            return str(value)
    return None


def project_path(project_id: str | None) -> Path | None:
    if not project_id:
        return None
    path = PROJECT_ROOT / "projects" / project_id
    return path if path.exists() else None


def active_project() -> tuple[str | None, Path | None, dict[str, Any]]:
    pid = project_id_from_env_or_file()
    ppath = project_path(pid)
    meta = parse_frontmatter(ppath / "PROJECT.md") if ppath else {}
    return pid, ppath, meta


def active_pack(project_dir: Path | None, project_meta: dict[str, Any]) -> dict[str, Any]:
    pack_file = project_dir / "genre-context" / "active-pack.yaml" if project_dir else None
    pack = load_yaml(pack_file, {}) if pack_file else {}
    if not isinstance(pack, dict):
        pack = {}
    genre = pack.get("primary_genre") or pack.get("genre") or project_meta.get("genre")
    if genre:
        pack["primary_genre"] = genre
    return pack


def event(project_dir: Path | None, hook: str, status: str, message: str, extra: dict[str, Any] | None = None) -> None:
    if not project_dir:
        return
    history = project_dir / ".history"
    history.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hook": hook,
        "status": status,
        "message": message,
    }
    if extra:
        payload.update(extra)
    with (history / "events.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ok(message: str, project_dir: Path | None = None, hook: str = "hook") -> int:
    print(f"OK: {message}")
    event(project_dir, hook, "ok", message)
    return 0


def block(message: str, project_dir: Path | None = None, hook: str = "hook") -> int:
    print(f"BLOCK: {message}", file=sys.stderr)
    event(project_dir, hook, "block", message)
    return 1


def review(message: str, project_dir: Path | None = None, hook: str = "hook") -> int:
    print(f"REVIEW: {message}", file=sys.stderr)
    event(project_dir, hook, "needs_review", message)
    return 2


def registry() -> dict[str, Any]:
    return load_yaml(PLUGIN_ROOT / "genre-packs" / "_registry.yaml", {}) or {}


def pack_dir(genre: str | None) -> Path | None:
    if not genre:
        return None
    packs = registry().get("packs", {})
    item = packs.get(genre, {})
    rel = item.get("path") or f"genre-packs/{genre}/"
    return PLUGIN_ROOT / rel


def listed_agents(pack: Path) -> list[str]:
    meta = parse_frontmatter(pack / "PACK.md")
    return list(meta.get("specialist_agents") or [])


def check_pack_complete(genre: str) -> tuple[bool, list[str]]:
    pdir = pack_dir(genre)
    if not pdir or not pdir.exists():
        return False, [f"Pack directory missing for {genre}"]
    required = [
        "PACK.md",
        "agents",
        "skills",
        "memory-schema.yaml",
        "structure-paradigm.yaml",
        "reader-profiles.yaml",
        "quality-metrics.yaml",
        "collaboration-mode.yaml",
        "consistency-rules.yaml",
    ]
    missing = [item for item in required if not (pdir / item).exists()]
    for agent in listed_agents(pdir):
        if not (pdir / "agents" / f"{agent}.md").exists():
            missing.append(f"agents/{agent}.md")
    rules = load_yaml(pdir / "consistency-rules.yaml", {}) or {}
    levels = [rule.get("level") for rule in (rules.get("rules") or {}).values() if isinstance(rule, dict)]
    if "critical" not in levels:
        missing.append("critical consistency rule")
    return not missing, missing


def hook_session_start(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pid:
        return ok("BookForge session started without active project")
    if not pdir:
        return review(f"Active project '{pid}' is configured but missing")
    genre = active_pack(pdir, meta).get("primary_genre")
    return ok(f"BookForge session started for {pid} ({genre or 'genre-unset'})", pdir, "session-start")


def hook_project_context_loader(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pid:
        return ok("No active project configured; project context loader idle")
    if not pdir:
        return review(f"Configured project '{pid}' does not exist")
    required = ["PROJECT.md", "constitution", "genre-context"]
    missing = [name for name in required if not (pdir / name).exists()]
    if missing:
        return review(f"Project {pid} is missing: {', '.join(missing)}", pdir, "project-context-loader")
    return ok(f"Loaded project context for {pid}", pdir, "project-context-loader")


def hook_genre_pack_loader(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; genre pack loader idle")
    pack = active_pack(pdir, meta)
    genre = pack.get("primary_genre")
    if not genre or str(genre).startswith("<"):
        return review("Active project has no concrete genre", pdir, "genre-pack-loader")
    complete, missing = check_pack_complete(str(genre))
    if not complete:
        return block(f"Genre pack {genre} incomplete: {', '.join(missing)}", pdir, "genre-pack-loader")
    memory = pdir / "genre-context" / "genre-memory"
    memory.mkdir(parents=True, exist_ok=True)
    return ok(f"Loaded genre pack {genre}", pdir, "genre-pack-loader")


def hook_project_isolation_guard(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; isolation guard idle")
    path = payload.get("tool_input", {}).get("file_path") or payload.get("file_path") or payload.get("path")
    if not path:
        return ok("No target path supplied; isolation guard idle", pdir, "project-isolation-guard")
    target = Path(path).resolve() if str(path).startswith("/") else (PROJECT_ROOT / path).resolve()
    # Only PROJECT_ROOT-side workspace areas are writable through this guard.
    # PLUGIN_ROOT (this plugin's own bundled agents/skills/genre-packs) is
    # shared, versioned reference material and is intentionally excluded.
    allowed = [
        pdir.resolve(),
        (PROJECT_ROOT / ".claude").resolve(),
        (PROJECT_ROOT / "capability-library").resolve(),
        (PROJECT_ROOT / "docs").resolve(),
    ]
    if any(target == base or base in target.parents for base in allowed):
        return ok(f"Write target allowed: {target}", pdir, "project-isolation-guard")
    return review(f"Write target outside BookForge work areas: {target}", pdir, "project-isolation-guard")


def hook_human_checkpoint_gate(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; human checkpoint gate idle")
    stage = meta.get("current_stage")
    mode = meta.get("collaboration_mode")
    tool_input = payload.get("tool_input", {}) if isinstance(payload.get("tool_input"), dict) else {}
    target = str(tool_input.get("file_path") or payload.get("file_path") or "")
    sensitive = any(part in target for part in ["constitution/brief.yaml", "genre-context/active-pack.yaml", "historiography", "knowledge-dag", "world-bible"])
    approved = os.environ.get("BOOKFORGE_HUMAN_APPROVED") == "1"
    if sensitive and not approved:
        return review(f"Human approval required for {target or stage or mode}", pdir, "human-checkpoint-gate")
    return ok("No human checkpoint required", pdir, "human-checkpoint-gate")


def hook_consistency_engine_check(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; consistency engine idle")
    findings = payload.get("consistency_findings") or payload.get("findings") or []
    if isinstance(findings, list):
        if any(isinstance(item, dict) and item.get("level") == "critical" for item in findings):
            return block("Critical consistency finding supplied by hook payload", pdir, "consistency-engine-check")
        if any(isinstance(item, dict) and item.get("level") == "high" for item in findings):
            return review("High-severity consistency finding supplied by hook payload", pdir, "consistency-engine-check")
    genre = active_pack(pdir, meta).get("primary_genre")
    if not genre or str(genre).startswith("<"):
        return ok("No concrete genre; consistency engine idle", pdir, "consistency-engine-check")
    rules_path = pack_dir(str(genre)) / "consistency-rules.yaml"
    rules = load_yaml(rules_path, {}) or {}
    critical = [rid for rid, rule in (rules.get("rules") or {}).items() if isinstance(rule, dict) and rule.get("level") == "critical"]
    if not critical:
        return block(f"No critical consistency rules for {genre}", pdir, "consistency-engine-check")
    return ok(f"Consistency rules available for {genre}: {', '.join(critical)}", pdir, "consistency-engine-check")


def hook_pipeline_stage_gate(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; pipeline gate idle")
    stage = meta.get("current_stage", "ideation")
    required_by_stage = {
        "ideation": ["constitution/brief.yaml", "genre-context/active-pack.yaml"],
        "outline": ["outline/outline.yaml"],
        "extended": ["extended-outline"],
        "drafting": ["drafts"],
        "review": ["review"],
        "typeset": ["typeset"],
    }
    missing = [rel for rel in required_by_stage.get(stage, []) if not (pdir / rel).exists()]
    if missing:
        return review(f"Stage {stage} missing: {', '.join(missing)}", pdir, "pipeline-stage-gate")
    return ok(f"Stage {stage} gate passed", pdir, "pipeline-stage-gate")


def hook_auto_version_snapshot(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; snapshot idle")
    snap = pdir / ".history" / "snapshots"
    snap.mkdir(parents=True, exist_ok=True)
    event(pdir, "auto-version-snapshot", "ok", "Snapshot point recorded")
    return ok("Snapshot point recorded", pdir, "auto-version-snapshot")


def hook_style_anchor_check(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; style anchor check idle")
    anchors = pdir / "registry" / "style_anchors"
    if not anchors.exists():
        return review("No style anchors directory found", pdir, "style-anchor-check")
    return ok("Style anchor directory present", pdir, "style-anchor-check")


def hook_memory_write_guard(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; memory write guard idle")
    return hook_project_isolation_guard(payload)


def hook_capability_harvest_trigger(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; capability harvest idle")
    genre = active_pack(pdir, meta).get("primary_genre") or "unknown"
    # Capability harvest writes into the author's own workspace, not the
    # plugin install — each workspace grows its own library across projects.
    target = PROJECT_ROOT / "capability-library" / "by-genre" / str(genre)
    target.mkdir(parents=True, exist_ok=True)
    return ok(f"Capability harvest target ready: {target.relative_to(PROJECT_ROOT)}", pdir, "capability-harvest-trigger")


def hook_concept_registry_update(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; concept registry update idle")
    registry_path = pdir / "registry" / "concepts.yaml"
    if not registry_path.exists():
        return review("Concept registry missing", pdir, "concept-registry-update")
    return ok("Concept registry present", pdir, "concept-registry-update")


def hook_pre_compact_preserve(payload: dict[str, Any]) -> int:
    pid, pdir, meta = active_project()
    if not pdir:
        return ok("No active project; pre-compact preserve idle")
    state = pdir / ".history" / "last_context.json"
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps({"project_id": pid, "stage": meta.get("current_stage")}, ensure_ascii=False, indent=2), encoding="utf-8")
    return ok("Saved compact context", pdir, "pre-compact-preserve")


def hook_consistency_final_check(payload: dict[str, Any]) -> int:
    return hook_consistency_engine_check(payload)


def hook_consistency_violation_alert(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; violation alert idle")
    return ok("No consistency violation payload received", pdir, "consistency-violation-alert")


def hook_human_review_required_alert(payload: dict[str, Any]) -> int:
    pid, pdir, _meta = active_project()
    if not pdir:
        return ok("No active project; human review alert idle")
    return review("Human review required", pdir, "human-review-required-alert")


def hook_pre_bash_validation(payload: dict[str, Any]) -> int:
    command = payload.get("tool_input", {}).get("command") if isinstance(payload.get("tool_input"), dict) else None
    dangerous = ["rm -rf /", "git reset --hard", "git checkout --"]
    if command and any(item in command for item in dangerous):
        return block(f"Blocked dangerous command: {command}", None, "pre-bash-validation")
    return ok("Bash command accepted")


HOOKS = {
    "session-start": hook_session_start,
    "project-context-loader": hook_project_context_loader,
    "genre-pack-loader": hook_genre_pack_loader,
    "project-isolation-guard": hook_project_isolation_guard,
    "genre-agent-affinity-check": lambda payload: ok("Agent affinity check deferred to rule validation"),
    "memory-write-guard": hook_memory_write_guard,
    "human-checkpoint-gate": hook_human_checkpoint_gate,
    "pre-bash-validation": hook_pre_bash_validation,
    "consistency-engine-check": hook_consistency_engine_check,
    "style-anchor-check": hook_style_anchor_check,
    "auto-version-snapshot": hook_auto_version_snapshot,
    "capability-harvest-trigger": hook_capability_harvest_trigger,
    "concept-registry-update": hook_concept_registry_update,
    "pre-compact-preserve": hook_pre_compact_preserve,
    "pipeline-stage-gate": hook_pipeline_stage_gate,
    "consistency-final-check": hook_consistency_final_check,
    "consistency-violation-alert": hook_consistency_violation_alert,
    "human-review-required-alert": hook_human_review_required_alert,
}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: bookforge_hook.py <hook-name>", file=sys.stderr)
        return 1
    hook = sys.argv[1].removesuffix(".sh")
    payload = read_stdin_json()
    handler = HOOKS.get(hook)
    if not handler:
        return block(f"Unknown hook: {hook}")
    try:
        return int(handler(payload))
    except Exception as exc:
        print(f"HOOK ERROR: {hook}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
