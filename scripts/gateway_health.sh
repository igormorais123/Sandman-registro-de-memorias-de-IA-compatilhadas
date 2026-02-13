#!/bin/bash
# gateway_health.sh - Monitora saude do OpenClaw Gateway via PM2
# Versao: 3.0 (2026-02-12) - Consolidado: PM2 como unico gerenciador
#
# Uso: ./gateway_health.sh (executado via cron a cada 10 min)
# Retorna: GATEWAY_OK | GATEWAY_ALERT | GATEWAY_RECOVERED | GATEWAY_STARTED

set -euo pipefail

GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
PM2_APP_NAME="clawdbot-gateway"
LOG_DIR="/root/clawd/memory"
LOG_FILE="${LOG_DIR}/gateway-health.log"
MAX_LOG_LINES=500

export PATH=/root/.local/bin:/root/.npm-global/bin:/usr/local/bin:/usr/bin:/bin

mkdir -p "${LOG_DIR}"

log() {
    local msg="[$(date -Iseconds)] $1"
    echo "${msg}" >> "${LOG_FILE}"
    echo "$1" >&2
}

truncate_log() {
    if [ -f "${LOG_FILE}" ]; then
        local lines
        lines=$(wc -l < "${LOG_FILE}" 2>/dev/null || echo "0")
        if [ "${lines}" -gt "${MAX_LOG_LINES}" ]; then
            tail -n "${MAX_LOG_LINES}" "${LOG_FILE}" > "${LOG_FILE}.tmp"
            mv "${LOG_FILE}.tmp" "${LOG_FILE}"
        fi
    fi
}

check_gateway_http() {
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${GATEWAY_PORT}/" --connect-timeout 5 2>/dev/null || echo "000")
    [ "${code}" != "000" ]
}

get_pm2_status() {
    pm2 jlist 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for app in data:
        if app.get('name') == '${PM2_APP_NAME}':
            print(app.get('pm2_env', {}).get('status', 'unknown'))
            sys.exit(0)
    print('not_found')
except:
    print('error')
" 2>/dev/null || echo "error"
}

count_port_processes() {
    lsof -t -i :"${GATEWAY_PORT}" 2>/dev/null | wc -l || echo "0"
}

kill_duplicate_processes() {
    local pids
    pids=$(lsof -t -i :"${GATEWAY_PORT}" 2>/dev/null | tail -n +2)
    if [ -n "${pids}" ]; then
        log "Matando processos duplicados na porta: ${pids}"
        echo "${pids}" | xargs -r kill -9 2>/dev/null || true
        sleep 1
        return 0
    fi
    return 1
}

main() {
    truncate_log

    local pm2_status
    local port_count
    local http_ok=false

    pm2_status=$(get_pm2_status)
    port_count=$(count_port_processes)

    if check_gateway_http; then
        http_ok=true
    fi

    log "Check: pm2=${pm2_status}, port_count=${port_count}, http=${http_ok}"

    # Caso 1: Tudo OK
    if [ "${pm2_status}" = "online" ] && ${http_ok}; then
        if [ "${port_count}" -gt 1 ]; then
            log "WARN: Multiplos processos na porta, limpando"
            kill_duplicate_processes
        fi
        echo "GATEWAY_OK"
        return 0
    fi

    # Caso 2: Multiplos processos na porta
    if [ "${port_count}" -gt 1 ]; then
        log "ALERT: Multiplos processos na porta ${GATEWAY_PORT}"
        kill_duplicate_processes
        sleep 2
        if check_gateway_http; then
            log "Conflito resolvido"
            echo "GATEWAY_RECOVERED"
            return 0
        fi
    fi

    # Caso 3: PM2 online mas sem resposta HTTP
    if [ "${pm2_status}" = "online" ] && ! ${http_ok}; then
        log "ALERT: PM2 online mas gateway sem resposta - reiniciando via PM2"
        pm2 restart "${PM2_APP_NAME}" 2>/dev/null
        sleep 8
        if check_gateway_http; then
            log "Gateway recuperado via PM2 restart"
            echo "GATEWAY_RECOVERED"
            return 0
        else
            log "CRITICAL: Gateway nao recuperou"
            echo "GATEWAY_ALERT"
            return 1
        fi
    fi

    # Caso 4: PM2 parado ou com erro
    if [ "${pm2_status}" = "stopped" ] || [ "${pm2_status}" = "errored" ]; then
        if [ "${port_count}" -gt 0 ]; then
            local orphan_pids
            orphan_pids=$(lsof -t -i :"${GATEWAY_PORT}" 2>/dev/null)
            log "Matando orfaos na porta: ${orphan_pids}"
            echo "${orphan_pids}" | xargs -r kill -9 2>/dev/null || true
            sleep 2
        fi

        log "Iniciando gateway via PM2"
        pm2 restart "${PM2_APP_NAME}" 2>/dev/null
        sleep 8
        if check_gateway_http; then
            log "Gateway iniciado com sucesso"
            echo "GATEWAY_STARTED"
            return 0
        else
            log "CRITICAL: Falha ao iniciar gateway"
            echo "GATEWAY_ALERT"
            return 1
        fi
    fi

    # Caso 5: App nao encontrado no PM2
    if [ "${pm2_status}" = "not_found" ] || [ "${pm2_status}" = "error" ]; then
        log "CRITICAL: App ${PM2_APP_NAME} nao encontrado no PM2. Verifique pm2 list."
        echo "GATEWAY_ALERT"
        return 1
    fi

    log "Estado desconhecido: pm2=${pm2_status}"
    echo "GATEWAY_ALERT"
    return 1
}

main "$@"
