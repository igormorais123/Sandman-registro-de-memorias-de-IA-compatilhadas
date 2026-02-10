#!/bin/bash
# ============================================
# NEXO → ONIR: Invocacao segura
# Permite NEXO (WSL) invocar ONIR (Claude Code no Windows)
#
# Uso: ./nexo_invocar_onir.sh "prompt aqui"
# Uso cron: ./nexo_invocar_onir.sh --sonho-diario
# ============================================

set -euo pipefail

REPO="/mnt/c/Users/IgorPC/Colmeia"
CLAUDE="/mnt/c/Users/IgorPC/.local/bin/claude.exe"
LOG_DIR="$REPO/scripts/logs"
LOG_FILE="$LOG_DIR/nexo_invoca_onir_$(date +%Y%m%d_%H%M).log"
LOCK_FILE="/tmp/onir_invocacao.lock"
MAX_BUDGET="2.00"

# Seguranca: lock para evitar invocacoes simultaneas
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if kill -0 "$PID" 2>/dev/null; then
        echo "[$(date)] BLOQUEADO: Outra invocacao em andamento (PID: $PID)" >> "$LOG_FILE"
        exit 1
    else
        rm -f "$LOCK_FILE"
    fi
fi
echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

mkdir -p "$LOG_DIR"

echo "[$(date)] Iniciando invocacao ONIR" >> "$LOG_FILE"

# Modo sonho diario
if [ "${1:-}" = "--sonho-diario" ]; then
    PROMPT="Leia o arquivo scripts/onir_sonho_diario_prompt.md e execute todas as instrucoes contidas nele. Siga o protocolo completo sem pular nenhum passo."
else
    PROMPT="${1:-Voce e ONIR. O que precisa fazer?}"
fi

# Seguranca: limitar tamanho do prompt (anti-injection)
if [ ${#PROMPT} -gt 5000 ]; then
    echo "[$(date)] BLOQUEADO: Prompt muito grande (${#PROMPT} chars, max 5000)" >> "$LOG_FILE"
    exit 2
fi

# Executar Claude Code
cd "$REPO"
echo "[$(date)] Executando: claude -p (${#PROMPT} chars)" >> "$LOG_FILE"

"$CLAUDE" -p "$PROMPT" \
    --permission-mode bypassPermissions \
    --max-budget-usd "$MAX_BUDGET" \
    --model opus \
    >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "[$(date)] Concluido (exit: $EXIT_CODE)" >> "$LOG_FILE"

# Notificar Colmeia se foi sonho diario
if [ "${1:-}" = "--sonho-diario" ] && [ $EXIT_CODE -eq 0 ]; then
    python3 /root/clawd/scripts/colmeia_enviar.py \
        --tipo carta \
        --de "NEXO" \
        --para "Igor" \
        --mensagem "Sonho diario do ONIR executado com sucesso em $(date +%Y-%m-%d). Log: scripts/logs/$(basename $LOG_FILE)" \
        2>/dev/null || true
fi

exit $EXIT_CODE
