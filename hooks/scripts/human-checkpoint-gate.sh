#!/bin/bash
set -euo pipefail
exec python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bookforge_hook.py" "human-checkpoint-gate" "$@"
