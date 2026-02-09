#!/bin/bash
# =============================================================================
# codelab.sh — Gerenciador de coding agents via tmux
# =============================================================================
# O NEXO (Clawdbot) e o Igor podem ver/controlar as mesmas sessões.
#
# Uso:
#   codelab start <agent> <projeto> "tarefa"   → Inicia agent em tmux
#   codelab list                                → Lista sessões ativas
#   codelab watch <nome>                        → Captura output da sessão
#   codelab send <nome> "texto"                 → Envia texto pra sessão
#   codelab sendkeys <nome> "keys"              → Envia teclas especiais
#   codelab kill <nome>                         → Mata sessão
#   codelab killall                             → Mata todas as sessões
#   codelab attach <nome>                       → Attach (uso humano)
#   codelab log <nome>                          → Salva log completo
# =============================================================================

TMUX_PREFIX="codelab"
LOG_DIR="/root/clawd/memory/codelab-logs"
mkdir -p "$LOG_DIR"

# Projetos
declare -A PROJECTS=(
    [pesquisa]="/mnt/c/Agentes"
    [academy]="/mnt/c/Users/IgorPC/opencode-academy"
    [clawd]="/root/clawd"
    [sandman]="/root/clawd/sandman"
)

# Agentes
declare -A AGENTS=(
    [claude]="claude -p"
    [claude-i]="claude"
    [codex]="codex exec"
    [opencode]="opencode run"
)

session_name() {
    local agent="$1"
    local project="$2"
    echo "${TMUX_PREFIX}-${agent}-${project}"
}

cmd_start() {
    local agent="${1:-claude}"
    local project="${2:-pesquisa}"
    local task="$3"
    local workdir="${PROJECTS[$project]:-$project}"
    local agent_cmd="${AGENTS[$agent]}"
    local name=$(session_name "$agent" "$project")

    if [ -z "$agent_cmd" ]; then
        echo "❌ Agent desconhecido: $agent"
        echo "   Disponíveis: claude, claude-i, codex, opencode"
        return 1
    fi

    if [ -z "$task" ] && [ "$agent" != "claude-i" ]; then
        echo "❌ Falta a tarefa. Uso: codelab start $agent $project \"tarefa aqui\""
        return 1
    fi

    # Verificar se já existe
    if tmux has-session -t "$name" 2>/dev/null; then
        echo "⚠️  Sessão '$name' já existe. Use 'codelab watch $name' ou 'codelab kill $name'"
        return 1
    fi

    # Criar sessão tmux com tee pra log
    local logfile="$LOG_DIR/${name}_$(date +%Y%m%d_%H%M%S).log"
    
    if [ "$agent" = "claude-i" ]; then
        # Modo interativo — sem task
        tmux new-session -d -s "$name" -c "$workdir" "script -q -c '$agent_cmd' '$logfile'"
    elif [ "$agent" = "codex" ]; then
        tmux new-session -d -s "$name" -c "$workdir" "script -q -c \"codex exec '$task'\" '$logfile'"
    else
        tmux new-session -d -s "$name" -c "$workdir" "script -q -c \"$agent_cmd '$task'\" '$logfile'"
    fi

    echo "✅ Sessão '$name' iniciada"
    echo "   Agent: $agent"
    echo "   Projeto: $workdir"
    [ -n "$task" ] && echo "   Tarefa: $task"
    echo ""
    echo "   Igor pode ver: wsl tmux attach -t $name"
    echo "   NEXO monitora: codelab watch $name"
}

cmd_list() {
    echo "=== CodeLab — Sessões Ativas ==="
    echo ""
    
    local sessions=$(tmux list-sessions -F "#{session_name} #{session_created} #{session_windows} #{session_attached}" 2>/dev/null | grep "^${TMUX_PREFIX}")
    
    if [ -z "$sessions" ]; then
        echo "Nenhuma sessão ativa."
        return
    fi

    printf "%-35s %-12s %-8s %-10s\n" "SESSÃO" "CRIADA" "JANELAS" "ATTACHED"
    printf "%-35s %-12s %-8s %-10s\n" "------" "------" "-------" "--------"
    
    while IFS= read -r line; do
        local name=$(echo "$line" | awk '{print $1}')
        local created=$(date -d @$(echo "$line" | awk '{print $2}') '+%H:%M:%S' 2>/dev/null || echo "?")
        local windows=$(echo "$line" | awk '{print $3}')
        local attached=$(echo "$line" | awk '{print $4}')
        [ "$attached" = "1" ] && attached="sim" || attached="não"
        
        printf "%-35s %-12s %-8s %-10s\n" "$name" "$created" "$windows" "$attached"
    done <<< "$sessions"
    
    echo ""
    echo "Total: $(echo "$sessions" | wc -l) sessão(ões)"
}

cmd_watch() {
    local name="$1"
    
    # Se não tem prefix, adiciona
    if ! echo "$name" | grep -q "^${TMUX_PREFIX}"; then
        # Tentar achar sessão que contém o nome
        local match=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "${TMUX_PREFIX}.*${name}" | head -1)
        [ -n "$match" ] && name="$match"
    fi

    if ! tmux has-session -t "$name" 2>/dev/null; then
        echo "❌ Sessão '$name' não encontrada"
        cmd_list
        return 1
    fi

    # Capturar as últimas 200 linhas
    tmux capture-pane -t "$name" -p -S -200 2>/dev/null | tail -80
}

cmd_send() {
    local name="$1"
    local text="$2"
    
    if ! echo "$name" | grep -q "^${TMUX_PREFIX}"; then
        local match=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "${TMUX_PREFIX}.*${name}" | head -1)
        [ -n "$match" ] && name="$match"
    fi

    if ! tmux has-session -t "$name" 2>/dev/null; then
        echo "❌ Sessão '$name' não encontrada"
        return 1
    fi

    tmux send-keys -t "$name" "$text" Enter
    echo "📤 Enviado para '$name': $text"
}

cmd_sendkeys() {
    local name="$1"
    shift
    local keys="$@"
    
    if ! echo "$name" | grep -q "^${TMUX_PREFIX}"; then
        local match=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "${TMUX_PREFIX}.*${name}" | head -1)
        [ -n "$match" ] && name="$match"
    fi

    tmux send-keys -t "$name" $keys
    echo "⌨️  Keys enviadas para '$name': $keys"
}

cmd_kill() {
    local name="$1"
    
    if ! echo "$name" | grep -q "^${TMUX_PREFIX}"; then
        local match=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "${TMUX_PREFIX}.*${name}" | head -1)
        [ -n "$match" ] && name="$match"
    fi

    tmux kill-session -t "$name" 2>/dev/null
    echo "💀 Sessão '$name' encerrada"
}

cmd_killall() {
    local sessions=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "^${TMUX_PREFIX}")
    if [ -z "$sessions" ]; then
        echo "Nenhuma sessão pra matar."
        return
    fi
    while IFS= read -r name; do
        tmux kill-session -t "$name" 2>/dev/null
        echo "💀 $name"
    done <<< "$sessions"
}

cmd_log() {
    local name="$1"
    local logfile="$LOG_DIR/${name}_full_$(date +%Y%m%d_%H%M%S).log"
    
    if ! echo "$name" | grep -q "^${TMUX_PREFIX}"; then
        local match=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "${TMUX_PREFIX}.*${name}" | head -1)
        [ -n "$match" ] && name="$match"
    fi

    tmux capture-pane -t "$name" -p -S - > "$logfile" 2>/dev/null
    echo "📝 Log salvo: $logfile"
}

# ----- MAIN -----
case "${1:-}" in
    start)   shift; cmd_start "$@" ;;
    list|ls) cmd_list ;;
    watch|w) cmd_watch "$2" ;;
    send|s)  cmd_send "$2" "$3" ;;
    sendkeys|sk) shift; cmd_sendkeys "$@" ;;
    kill|k)  cmd_kill "$2" ;;
    killall) cmd_killall ;;
    attach|a) tmux attach -t "$2" ;;
    log)     cmd_log "$2" ;;
    *)
        echo "🔬 CodeLab — Gerenciador de Coding Agents"
        echo ""
        echo "Uso:"
        echo "  codelab start <agent> <projeto> \"tarefa\"   Iniciar agent"
        echo "  codelab list                                Listar sessões"
        echo "  codelab watch <nome>                        Ver output"
        echo "  codelab send <nome> \"texto\"                 Enviar texto"
        echo "  codelab sendkeys <nome> C-c                 Enviar teclas"
        echo "  codelab kill <nome>                         Matar sessão"
        echo "  codelab killall                             Matar todas"
        echo "  codelab attach <nome>                       Attach (humano)"
        echo "  codelab log <nome>                          Salvar log"
        echo ""
        echo "Agents: claude, claude-i (interativo), codex, opencode"
        echo "Projetos: pesquisa, academy, clawd, sandman"
        ;;
esac
