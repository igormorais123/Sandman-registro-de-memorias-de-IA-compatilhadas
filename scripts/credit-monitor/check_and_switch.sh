#!/bin/bash
# Credit Monitor - Verifica créditos e muda modelo automaticamente
# Roda via cron a cada 15 minutos

set -e

LOG_FILE="/root/clawd/logs/credit-monitor.log"
CONFIG_FILE="/root/.clawdbot/clawdbot.json"
STATE_FILE="/root/clawd/scripts/credit-monitor/state.json"
ALERT_SENT_FILE="/root/clawd/scripts/credit-monitor/alert_sent"

mkdir -p /root/clawd/logs
mkdir -p /root/clawd/scripts/credit-monitor

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Modelos em ordem de preferência (do melhor pro gratuito)
PREMIUM_MODEL="anthropic/claude-sonnet-4"
FALLBACK_MODELS=(
    "opencode/gpt-5-nano"
    "opencode/glm-4.7-free"
    "google/gemini-2.5-flash"
    "anthropic/claude-3-5-haiku-latest"
)

# Testar se Anthropic está funcionando
test_anthropic() {
    # Pegar a API key do ambiente ou config
    ANTHROPIC_KEY="${ANTHROPIC_API_KEY:-}"
    
    if [ -z "$ANTHROPIC_KEY" ]; then
        # Tentar pegar do clawdbot
        ANTHROPIC_KEY=$(grep -o '"ANTHROPIC_API_KEY"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" 2>/dev/null | cut -d'"' -f4 || true)
    fi
    
    if [ -z "$ANTHROPIC_KEY" ]; then
        log "WARN: Anthropic API key não encontrada, assumindo OK"
        return 0
    fi
    
    # Fazer requisição mínima de teste
    RESPONSE=$(curl -s -w "\n%{http_code}" --max-time 10 \
        -H "x-api-key: $ANTHROPIC_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d '{"model":"claude-3-5-haiku-20241022","max_tokens":1,"messages":[{"role":"user","content":"1"}]}' \
        "https://api.anthropic.com/v1/messages" 2>/dev/null || echo -e "\n000")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | head -n -1)
    
    log "Anthropic test response: HTTP $HTTP_CODE"
    
    # Códigos que indicam problema de créditos
    if [[ "$HTTP_CODE" == "429" ]] || [[ "$HTTP_CODE" == "402" ]] || [[ "$HTTP_CODE" == "403" ]]; then
        if echo "$BODY" | grep -qi "credit\|quota\|billing\|limit\|exceeded"; then
            log "ERROR: Créditos Anthropic esgotados ou limite atingido"
            return 1
        fi
    fi
    
    if [[ "$HTTP_CODE" == "000" ]]; then
        log "WARN: Timeout ao testar Anthropic"
        return 2
    fi
    
    if [[ "$HTTP_CODE" =~ ^2 ]]; then
        log "OK: Anthropic funcionando"
        return 0
    fi
    
    log "WARN: Anthropic retornou HTTP $HTTP_CODE"
    return 0
}

# Pegar modelo atual
get_current_model() {
    # Verificar se tem override de sessão primeiro
    CURRENT=$(jq -r '.agents.defaults.model.name // .agents.defaults.model // "unknown"' "$CONFIG_FILE" 2>/dev/null)
    echo "$CURRENT"
}

# Mudar para modelo de fallback
switch_to_fallback() {
    log "Mudando para modelos de fallback..."
    
    # Criar novo array de fallbacks começando com gratuitos
    FALLBACK_JSON=$(printf '%s\n' "${FALLBACK_MODELS[@]}" | jq -R . | jq -s .)
    
    # Usar clawdbot CLI pra mudar config se disponível
    if command -v clawdbot &> /dev/null; then
        # Patch a config para usar modelo gratuito como padrão
        cat > /tmp/config_patch.json << EOF
{
    "agents": {
        "defaults": {
            "model": {
                "name": "opencode/gpt-5-nano",
                "fallbacks": ["opencode/glm-4.7-free", "google/gemini-2.5-flash", "anthropic/claude-3-5-haiku-latest"]
            }
        }
    }
}
EOF
        
        # Aplicar via jq merge
        jq -s '.[0] * .[1]' "$CONFIG_FILE" /tmp/config_patch.json > /tmp/new_config.json
        cp /tmp/new_config.json "$CONFIG_FILE"
        
        log "Config atualizada para modelo gratuito"
        
        # Sinalizar restart
        touch /root/.clawdbot/restart-sentinel.json
        
        # Tentar restart graceful
        pkill -USR1 -f "clawdbot" 2>/dev/null || true
        
        log "Sinal de restart enviado"
    fi
    
    echo "SWITCHED" > "$STATE_FILE"
}

# Restaurar modelo premium
restore_premium() {
    log "Restaurando modelo premium..."
    
    cat > /tmp/config_patch.json << EOF
{
    "agents": {
        "defaults": {
            "model": {
                "fallbacks": ["anthropic/claude-sonnet-4", "opencode/gpt-5-nano", "opencode/glm-4.7-free", "google/gemini-2.5-flash", "anthropic/claude-3-5-haiku-latest"]
            }
        }
    }
}
EOF
    
    jq -s '.[0] * .[1]' "$CONFIG_FILE" /tmp/config_patch.json > /tmp/new_config.json
    
    # Remover o "name" override se existir
    jq 'del(.agents.defaults.model.name)' /tmp/new_config.json > /tmp/new_config2.json
    cp /tmp/new_config2.json "$CONFIG_FILE"
    
    pkill -USR1 -f "clawdbot" 2>/dev/null || true
    
    rm -f "$STATE_FILE"
    rm -f "$ALERT_SENT_FILE"
    
    log "Modelo premium restaurado"
}

# Enviar alerta pro Igor
send_alert() {
    local message="$1"
    
    # Evitar spam de alertas
    if [ -f "$ALERT_SENT_FILE" ]; then
        LAST_ALERT=$(cat "$ALERT_SENT_FILE")
        NOW=$(date +%s)
        DIFF=$((NOW - LAST_ALERT))
        if [ $DIFF -lt 3600 ]; then
            log "Alerta já enviado há menos de 1h, pulando"
            return
        fi
    fi
    
    log "Enviando alerta: $message"
    
    # Tentar enviar via WhatsApp usando clawdbot
    if command -v clawdbot &> /dev/null; then
        echo "$message" | clawdbot send --channel whatsapp --to "+5561981157120" 2>/dev/null || true
    fi
    
    date +%s > "$ALERT_SENT_FILE"
}

# Main
main() {
    log "=== Credit Monitor Check ==="
    
    # Verificar estado atual
    CURRENT_STATE="normal"
    if [ -f "$STATE_FILE" ]; then
        CURRENT_STATE=$(cat "$STATE_FILE")
    fi
    
    # Testar Anthropic
    if test_anthropic; then
        # Anthropic OK
        if [ "$CURRENT_STATE" == "SWITCHED" ]; then
            log "Anthropic voltou! Restaurando modelo premium..."
            restore_premium
            send_alert "✅ Créditos Anthropic restaurados! Voltando pro Claude."
        fi
        log "Status: Normal"
    else
        # Anthropic com problema
        if [ "$CURRENT_STATE" != "SWITCHED" ]; then
            log "Anthropic com problema! Ativando fallback..."
            switch_to_fallback
            send_alert "⚠️ Créditos Anthropic baixos/esgotados. Mudei automaticamente pra modelo gratuito (GPT-5 Nano). Recarregue os créditos quando puder."
        fi
        log "Status: Fallback ativo"
    fi
    
    log "=== Check completo ==="
}

main "$@"
