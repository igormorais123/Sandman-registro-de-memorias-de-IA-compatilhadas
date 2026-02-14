#!/bin/bash
# whatsapp_health.sh - Verifica saúde do WhatsApp via openclaw status
# Versão: 2.1 (2026-02-13) - Corrigido grep

set -euo pipefail

LOG_FILE="/root/clawd/memory/whatsapp-health.log"

log() {
    echo "[$(date -Iseconds)] $1" >> "${LOG_FILE}" 2>/dev/null || true
    echo "$1"
}

main() {
    local output
    output=$(openclaw status 2>&1)
    
    # Verificar se WhatsApp está OK ou LINKED na tabela de canais
    if echo "$output" | grep -E "WhatsApp.*ON.*OK|WhatsApp.*LINKED" > /dev/null 2>&1; then
        log "WHATSAPP_OK"
        echo "WHATSAPP_OK"
        exit 0
    fi
    
    # Verificar se está na tabela de Health
    if echo "$output" | grep -E "WhatsApp.*LINKED|WhatsApp.*OK" > /dev/null 2>&1; then
        log "WHATSAPP_OK"
        echo "WHATSAPP_OK"
        exit 0
    fi
    
    log "WHATSAPP_ALERT"
    echo "WHATSAPP_ALERT"
    exit 1
}

main "$@"
