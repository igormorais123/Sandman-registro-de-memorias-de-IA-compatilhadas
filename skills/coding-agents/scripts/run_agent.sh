#!/bin/bash
# =============================================================================
# run_agent.sh — Wrapper pra rodar coding agents nos projetos do Igor
# =============================================================================
# Uso:
#   run_agent.sh claude "tarefa" [projeto]
#   run_agent.sh codex "tarefa" [projeto]
#   run_agent.sh opencode "tarefa" [projeto]
#   run_agent.sh status                        → listar agents rodando
# =============================================================================

PROJECTS_MAP=(
    "pesquisa:/mnt/c/Agentes"
    "academy:/mnt/c/Users/IgorPC/opencode-academy"
    "clawd:/root/clawd"
    "sandman:/root/clawd/sandman"
)

resolve_project() {
    local proj="${1:-pesquisa}"
    for mapping in "${PROJECTS_MAP[@]}"; do
        local key="${mapping%%:*}"
        local path="${mapping#*:}"
        if [[ "$proj" == "$key" ]]; then
            echo "$path"
            return
        fi
    done
    # Se não achou no map, usar como path direto
    echo "$proj"
}

AGENT="${1:-}"
TASK="${2:-}"
PROJECT="${3:-pesquisa}"
WORKDIR=$(resolve_project "$PROJECT")

case "$AGENT" in
    claude)
        echo "🧠 Claude Code → $WORKDIR"
        echo "📝 Tarefa: $TASK"
        cd "$WORKDIR" && claude -p "$TASK"
        ;;
    codex)
        echo "🤖 Codex CLI → $WORKDIR"
        echo "📝 Tarefa: $TASK"
        cd "$WORKDIR" && codex exec "$TASK"
        ;;
    opencode)
        echo "💻 OpenCode → $WORKDIR"
        echo "📝 Tarefa: $TASK"
        cd "$WORKDIR" && opencode run "$TASK"
        ;;
    status)
        echo "=== Agents rodando ==="
        ps aux | grep -E "claude|codex|opencode" | grep -v grep | grep -v "openclaw"
        ;;
    *)
        echo "Uso: run_agent.sh <claude|codex|opencode|status> \"tarefa\" [projeto]"
        echo ""
        echo "Projetos: pesquisa, academy, clawd, sandman (ou path direto)"
        exit 1
        ;;
esac
