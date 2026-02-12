#!/bin/bash
# ============================================================
# Colmeia v6 — Heartbeat de Agente
# Uso: heartbeat_agente.sh <agente_id> <modelo_triagem>
# Exemplo: heartbeat_agente.sh nexo haiku
#
# Executado via cron a cada 15 minutos (escalonado):
#   */15 * * * *     heartbeat_agente.sh nexo haiku
#   2-62/15 * * * *  heartbeat_agente.sh onir haiku
#   4-64/15 * * * *  heartbeat_agente.sh sandman haiku
# ============================================================

set -euo pipefail

AGENTE="${1:?Uso: heartbeat_agente.sh <agente_id> <modelo>}"
MODELO="${2:-haiku}"

# Caminhos
COLMEIA_DIR="/mnt/c/Users/IgorPC/Colmeia"
BANCO_DIR="$COLMEIA_DIR/operacional/banco"
CLI="python3 $BANCO_DIR/cli.py"
WORKING="$COLMEIA_DIR/instancias/$AGENTE/WORKING.md"
LOG_DIR="$COLMEIA_DIR/logs"
LOG_FILE="$LOG_DIR/heartbeat_$(date +%Y%m%d).log"

# Garantir diretorio de logs
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$AGENTE] $*" >> "$LOG_FILE"
}

log "=== HEARTBEAT INICIO (modelo: $MODELO) ==="

# 1. Registrar heartbeat no banco
cd "$BANCO_DIR"
$CLI heartbeat "$AGENTE" >> "$LOG_FILE" 2>&1

# 2. Checar tarefas em progresso
TAREFAS_PROGRESSO=$($CLI tarefas --responsavel "$AGENTE" --status em_progresso 2>/dev/null || true)

# 3. Checar tarefas atribuidas (novas)
TAREFAS_NOVAS=$($CLI tarefas --responsavel "$AGENTE" --status atribuida 2>/dev/null || true)

# 4. Checar mencoes pendentes
MENCOES=$($CLI mencoes --para "$AGENTE" 2>/dev/null || true)

# 5. Decidir acao
TEM_TRABALHO=false

if echo "$TAREFAS_PROGRESSO" | grep -q "resultado(s)"; then
    if ! echo "$TAREFAS_PROGRESSO" | grep -q "0 resultado"; then
        TEM_TRABALHO=true
        log "Tarefas em progresso encontradas"
    fi
fi

if echo "$TAREFAS_NOVAS" | grep -q "resultado(s)"; then
    if ! echo "$TAREFAS_NOVAS" | grep -q "0 resultado"; then
        TEM_TRABALHO=true
        log "Tarefas novas atribuidas encontradas"
    fi
fi

if echo "$MENCOES" | grep -q "PENDENTES"; then
    if ! echo "$MENCOES" | grep -q "Nenhuma"; then
        TEM_TRABALHO=true
        log "Mencoes pendentes encontradas"
    fi
fi

if [ "$TEM_TRABALHO" = true ]; then
    log "HA TRABALHO — iniciando execucao..."

    # Ler contexto do WORKING.md se existir
    CONTEXTO=""
    if [ -f "$WORKING" ]; then
        CONTEXTO=$(cat "$WORKING")
    fi

    # Montar prompt de execucao
    PROMPT="Voce e $AGENTE da Colmeia. Acordou no heartbeat.

TAREFAS EM PROGRESSO:
$TAREFAS_PROGRESSO

TAREFAS NOVAS:
$TAREFAS_NOVAS

MENCOES PENDENTES:
$MENCOES

WORKING.MD ATUAL:
$CONTEXTO

Execute a tarefa mais urgente. Ao terminar:
1. Atualize o banco via cli.py
2. Atualize seu WORKING.md
3. Se concluiu tarefa, mova para revisao"

    # Executar via Claude CLI (budget limitado)
    # O modelo e selecionado baseado no parametro
    log "Invocando Claude CLI (modelo: $MODELO, budget: $2.00)..."

    # Placeholder: aqui entra a invocacao real do Claude Code ou API
    # claude --model "$MODELO" --max-cost 2.00 --prompt "$PROMPT"
    log "EXECUCAO PLACEHOLDER — implementar invocacao real na Fase 6"

else
    log "HEARTBEAT_OK — nenhum trabalho pendente"
fi

log "=== HEARTBEAT FIM ==="
