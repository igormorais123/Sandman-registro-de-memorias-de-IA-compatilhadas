#!/bin/bash
# gateway_prestart.sh - Limpa porta antes do gateway iniciar
# Usado como ExecStartPre no systemd service (backup se systemd for reativado)
# Versao: 1.0 (2026-02-12)

GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
LOG_FILE="/root/clawd/memory/gateway-prestart.log"

log() {
    echo "[$(date -Iseconds)] $1" >> "${LOG_FILE}" 2>/dev/null
}

# Verificar se a porta esta ocupada
PORT_PID=$(lsof -t -i :"${GATEWAY_PORT}" 2>/dev/null)

if [ -z "${PORT_PID}" ]; then
    log "Porta ${GATEWAY_PORT} livre. OK."
    exit 0
fi

# Porta ocupada por processo orfao
log "WARN: Porta ${GATEWAY_PORT} ocupada por processo orfao PID ${PORT_PID}. Matando."
kill "${PORT_PID}" 2>/dev/null
sleep 2

# Verificar se morreu
if kill -0 "${PORT_PID}" 2>/dev/null; then
    log "Processo ${PORT_PID} resistiu SIGTERM. Enviando SIGKILL."
    kill -9 "${PORT_PID}" 2>/dev/null
    sleep 1
fi

# Verificar porta de novo
REMAINING=$(lsof -t -i :"${GATEWAY_PORT}" 2>/dev/null)
if [ -n "${REMAINING}" ]; then
    log "CRITICAL: Porta ainda ocupada por PID(s): ${REMAINING}. Matando todos."
    echo "${REMAINING}" | xargs -r kill -9 2>/dev/null
    sleep 1
fi

log "Porta ${GATEWAY_PORT} liberada."
exit 0
