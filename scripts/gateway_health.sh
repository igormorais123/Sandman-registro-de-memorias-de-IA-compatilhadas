#!/bin/bash
# gateway_health.sh - Monitora saúde do gateway e corrige problemas
# Usado pelo heartbeat para detectar loops de restart e outros problemas

LOG_FILE="/root/clawd/memory/gateway-health.log"
STATE_FILE="/root/clawd/memory/gateway-health-state.json"

# Função para log
log() {
    echo "[$(date -Iseconds)] $1" >> "$LOG_FILE"
    echo "$1"
}

# Verifica se o gateway responde
check_gateway_response() {
    curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/health 2>/dev/null
}

# Conta restarts recentes (última hora)
count_recent_restarts() {
    journalctl -u clawdbot-gateway --since "1 hour ago" --no-pager 2>/dev/null | grep -c "restart counter" || echo "0"
}

# Verifica estado do systemd
check_systemd_state() {
    systemctl is-active clawdbot-gateway 2>/dev/null
}

# Verifica processos na porta
check_port_processes() {
    lsof -t -i :18789 2>/dev/null | wc -l
}

# Main
GATEWAY_RESPONSE=$(check_gateway_response)
RESTART_COUNT=$(count_recent_restarts)
SYSTEMD_STATE=$(check_systemd_state)
PORT_PROCS=$(check_port_processes)

# Diagnóstico
if [ "$GATEWAY_RESPONSE" == "200" ] || [ "$GATEWAY_RESPONSE" == "000" ]; then
    # Gateway responde (000 pode ser HTML sem status)
    GATEWAY_OK=true
else
    GATEWAY_OK=false
fi

# Detecta problemas
PROBLEM=""

# 1. Loop de restart (mais de 50 restarts/hora é anormal)
if [ "$RESTART_COUNT" -gt 50 ]; then
    PROBLEM="RESTART_LOOP"
    log "GATEWAY_ALERT: Loop de restart detectado ($RESTART_COUNT restarts/hora)"
fi

# 2. Systemd failed mas porta ocupada (processo órfão)
if [ "$SYSTEMD_STATE" == "failed" ] && [ "$PORT_PROCS" -gt 0 ]; then
    PROBLEM="ORPHAN_PROCESS"
    log "GATEWAY_ALERT: Processo órfão detectado (systemd=failed mas porta ocupada)"
fi

# 3. Systemd failed e porta livre (gateway morto)
if [ "$SYSTEMD_STATE" == "failed" ] && [ "$PORT_PROCS" -eq 0 ]; then
    PROBLEM="GATEWAY_DEAD"
    log "GATEWAY_ALERT: Gateway morto (systemd=failed, porta livre)"
fi

# Ações corretivas automáticas
if [ -n "$PROBLEM" ]; then
    log "Problema detectado: $PROBLEM - Iniciando correção automática"
    
    case "$PROBLEM" in
        RESTART_LOOP|ORPHAN_PROCESS)
            # Para tudo, limpa, reinicia
            log "Parando serviço e limpando..."
            systemctl stop clawdbot-gateway 2>/dev/null
            sleep 2
            bash /root/clawd/scripts/gateway_cleanup.sh 18789
            sleep 1
            systemctl daemon-reload
            systemctl start clawdbot-gateway
            sleep 3
            ;;
        GATEWAY_DEAD)
            # Só reinicia
            log "Reiniciando gateway..."
            systemctl daemon-reload
            systemctl start clawdbot-gateway
            sleep 3
            ;;
    esac
    
    # Verifica se corrigiu
    NEW_RESPONSE=$(check_gateway_response)
    NEW_STATE=$(check_systemd_state)
    
    if [ "$NEW_STATE" == "active" ]; then
        log "GATEWAY_RECOVERED: Problema corrigido automaticamente"
        echo "GATEWAY_RECOVERED"
    else
        log "GATEWAY_ALERT: Falha na correção automática - requer intervenção"
        echo "GATEWAY_ALERT"
    fi
else
    # Tudo OK
    echo "GATEWAY_OK"
fi
