#!/bin/sh
# Agents run this first: sh "$DEV_INSTINCTS_HOME/tools/sync-check.sh" <agent-name>
# Silent and exit 0 when the setup is in sync; otherwise one line saying what to fix.
name=$1
home=${DEV_INSTINCTS_HOME:-}
[ -n "$home" ] || { echo "DEV_INSTINCTS_HOME is not set. Run agent/sync-agents.ps1."; exit 1; }
command -v cygpath >/dev/null 2>&1 && home=$(cygpath -u "$home")
[ -f "$home/DEV-INSTINCTS.md" ] || { echo "DEV_INSTINCTS_HOME ($home) is not a Dev Instincts repo."; exit 1; }
repo="$home/agent/$name.md"
inst="$HOME/.claude/agents/$name.md"
[ -f "$repo" ] || { echo "No agent/$name.md in Dev Instincts."; exit 1; }
[ -f "$inst" ] || { echo "$name isn't installed in ~/.claude/agents/. Run agent/sync-agents.ps1."; exit 1; }
if ! cmp -s "$repo" "$inst"; then
    # A calibration run installs the blind copy on purpose.
    if [ "$name" = senior-coder ] && grep -q 'Calibration copy (blind)' "$inst"; then exit 0; fi
    echo "$name in ~/.claude/agents/ differs from Dev Instincts agent/$name.md. Run agent/sync-agents.ps1, then restart Claude Code."
    exit 1
fi
