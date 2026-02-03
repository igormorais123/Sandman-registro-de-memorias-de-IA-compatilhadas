#!/bin/bash
# wsl_boot.sh - Script de inicialização do WSL
# Roda automaticamente quando WSL inicia
#
# Instalação:
#   1. Adicionar ao /etc/wsl.conf:
#      [boot]
#      command=/root/clawd/scripts/wsl_boot.sh
#
#   2. Ou adicionar ao Windows Task Scheduler:
#      wsl -d Ubuntu-24.04 -u root /root/clawd/scripts/wsl_boot.sh

LOG=/root/clawd/memory/wsl-boot.log
SUPERVISOR_PID_FILE=/tmp/gateway-supervisor.pid

log() {
    echo "[$(date -Iseconds)] $1" >> "$LOG"
}

log "========================================="
log "WSL Boot iniciando"
log "========================================="

# Verifica se supervisor já está rodando
if [ -f "$SUPERVISOR_PID_FILE" ]; then
    PID=$(cat "$SUPERVISOR_PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        log "Supervisor já rodando (PID=$PID)"
        exit 0
    fi
fi

# Mata qualquer processo órfão na porta do gateway
log "Limpando processos órfãos..."
fuser -k 18789/tcp 2>/dev/null
sleep 2

# Inicia o supervisor em background
log "Iniciando gateway supervisor..."
nohup /root/clawd/scripts/gateway_supervisor.sh > /dev/null 2>&1 &
SUPERVISOR_PID=$!
echo $SUPERVISOR_PID > "$SUPERVISOR_PID_FILE"

log "Supervisor iniciado (PID=$SUPERVISOR_PID)"

# Aguarda um pouco e verifica
sleep 10
if kill -0 $SUPERVISOR_PID 2>/dev/null; then
    log "Boot completo - supervisor rodando"
else
    log "ERRO: Supervisor morreu após iniciar!"
fi

exit 0
