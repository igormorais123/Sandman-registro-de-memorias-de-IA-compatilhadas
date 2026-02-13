#!/bin/bash
# gateway_health.sh - Monitora saúde do OpenClaw Gateway via SYSTEMD
# Versão: 4.0 (2026-02-13) - Migrado de PM2 para systemd
#
# Retorna: GATEWAY_OK | GATEWAY_ALERT | GATEWAY_RECOVERED

set -euo pipefail

GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
SERVICE_NAME="openclaw-gateway"
LOG_FILE="/root/clawd/memory/gateway-health.log"

log() {
    echo "[$(date -Iseconds)] $1" >> "${LOG_FILE}" 2>/dev/null || true
    echo "$1"
}

# Verificar se systemd user está disponível
check_systemd() {
    systemctl --user is-active "${SERVICE_NAME}" 2>/dev/null
}

# Verificar se porta está respondendo
check_http() {
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${GATEWAY_PORT}/" --connect-timeout 5 2>/dev/null || echo "000")
    [ "${code}" != "000" ]
}

# Tentar recuperar
recover() {
    log "Tentando recuperar gateway..."
    systemctl --user restart "${SERVICE_NAME}" 2>/dev/null
    sleep 5
    if check_http; then
        log "GATEWAY_RECOVERED"
        echo "GATEWAY_RECOVERED"
        exit 0
    fi
    return 1
}

main() {
    local status
    status=$(check_systemd || echo "inactive")
    local http_ok=false
    check_http && http_ok=true

    # Caso 1: Tudo OK
    if [ "$status" = "active" ] && [ "$http_ok" = "true" ]; then
        log "GATEWAY_OK (systemd=active, http=ok)"
        echo "GATEWAY_OK"
        exit 0
    fi

    # Caso 2: Serviço ativo mas HTTP falhou - pode ser transitório
    if [ "$status" = "active" ] && [ "$http_ok" = "false" ]; then
        log "HTTP não responde, aguardando..."
        sleep 3
        if check_http; then
            log "GATEWAY_OK (recuperou sozinho)"
            echo "GATEWAY_OK"
            exit 0
        fi
        # Tentar restart
        if recover; then
            exit 0
        fi
    fi

    # Caso 3: Serviço não está ativo
    if [ "$status" != "active" ]; then
        log "Serviço inativo (status=$status), tentando iniciar..."
        if recover; then
            exit 0
        fi
    fi

    # Falha total
    log "GATEWAY_ALERT (status=$status, http=$http_ok)"
    echo "GATEWAY_ALERT"
    exit 1
}

main "$@"
