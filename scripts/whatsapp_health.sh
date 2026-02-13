#!/bin/bash
#===============================================================================
# whatsapp_health.sh - OpenClaw WhatsApp Channel Health Check
# 
# Verifica a saúde da conexão WhatsApp.
# Uso: ./whatsapp_health.sh [--verbose] [--auto-fix] [--json]
#===============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/whatsapp_health_$(date +%Y-%m-%d).log"
STATE_FILE="/tmp/openclaw_whatsapp_health_state"
MAX_RECONNECT_ATTEMPTS=3
RECONNECT_COOLDOWN_SECONDS=60

# Parse args
VERBOSE=false
AUTO_FIX=false
JSON_OUTPUT=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v) VERBOSE=true; shift ;;
        --auto-fix|-f) AUTO_FIX=true; shift ;;
        --json|-j) JSON_OUTPUT=true; shift ;;
        *) shift ;;
    esac
done

mkdir -p "$LOG_DIR"

log() {
    local level="$1"
    shift
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
    echo "$msg" >> "$LOG_FILE"
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        if [[ "$VERBOSE" == "true" ]] || [[ "$level" == "ERROR" ]] || [[ "$level" == "WARN" ]]; then
            echo "$msg" >&2
        fi
    fi
}

get_whatsapp_status() {
    local output
    output=$(timeout 15 openclaw status 2>&1) || return 1
    echo "$output" | grep -E "^│ WhatsApp" | head -1
}

check_gateway_health() {
    pgrep -f "node.*gateway" > /dev/null 2>&1 && \
    ss -tlnp 2>/dev/null | grep -q ":${OPENCLAW_GATEWAY_PORT:-18789}"
}

get_reconnect_count() {
    if [[ -f "$STATE_FILE" ]]; then
        local content state_date count
        content=$(cat "$STATE_FILE" 2>/dev/null) || { echo "0"; return; }
        state_date=$(echo "$content" | awk '{print $1}')
        count=$(echo "$content" | awk '{print $2}')
        count=${count:-0}
        if [[ "$state_date" == "$(date +%Y-%m-%d)" ]]; then
            echo "$count"
            return
        fi
    fi
    echo "0"
}

increment_reconnect_count() {
    echo "$(date +%Y-%m-%d) $(($(get_reconnect_count) + 1))" > "$STATE_FILE"
}

check_reconnect_cooldown() {
    local cooldown_file="/tmp/openclaw_whatsapp_last_reconnect"
    if [[ -f "$cooldown_file" ]]; then
        local last_time now diff
        last_time=$(cat "$cooldown_file")
        now=$(date +%s)
        diff=$((now - last_time))
        [[ $diff -lt $RECONNECT_COOLDOWN_SECONDS ]] && return 1
    fi
    return 0
}

attempt_reconnect() {
    local count
    count=$(get_reconnect_count)
    
    if [[ $count -ge $MAX_RECONNECT_ATTEMPTS ]]; then
        log "ERROR" "Max reconnect attempts reached today"
        return 1
    fi
    
    check_reconnect_cooldown || { log "WARN" "Cooldown active"; return 1; }
    
    log "INFO" "Attempting WhatsApp reconnection ($((count + 1))/$MAX_RECONNECT_ATTEMPTS)"
    increment_reconnect_count
    echo "$(date +%s)" > /tmp/openclaw_whatsapp_last_reconnect
    
    if systemctl --user restart openclaw-gateway.service 2>/dev/null; then
        log "INFO" "Gateway restart initiated"
        sleep 10
        return 0
    fi
    
    log "ERROR" "Reconnect failed"
    return 1
}

main() {
    log "INFO" "Starting WhatsApp health check"
    
    local status="healthy"
    local issues=()
    local enabled="OFF"
    local linked=false
    local phone=""
    local auth_age=""
    
    # Pre-check gateway
    if ! check_gateway_health; then
        log "ERROR" "Gateway not healthy"
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            echo '{"status":"error","healthy":false,"error":"gateway_unhealthy"}'
        else
            echo "ERROR: Gateway not healthy"
        fi
        exit 1
    fi
    
    # Get WhatsApp status
    local status_line
    status_line=$(get_whatsapp_status) || status_line=""
    
    if [[ -z "$status_line" ]]; then
        log "ERROR" "Could not get WhatsApp status"
        issues+=("status_unavailable")
        status="error"
    else
        log "INFO" "Status: $status_line"
        
        # Parse status
        [[ "$status_line" =~ "│ ON" ]] && enabled="ON"
        [[ "$status_line" =~ "linked" ]] && linked=true
        [[ "$status_line" =~ \+([0-9]+) ]] && phone="+${BASH_REMATCH[1]}"
        [[ "$status_line" =~ auth[[:space:]]([0-9]+[smh]|just[[:space:]]now) ]] && auth_age="${BASH_REMATCH[1]}"
        
        # Check enabled
        if [[ "$enabled" != "ON" ]]; then
            issues+=("disabled")
            status="disabled"
            log "WARN" "WhatsApp channel disabled"
        fi
        
        # Check linked
        if [[ "$linked" != "true" ]]; then
            issues+=("not_linked")
            status="unhealthy"
            log "ERROR" "WhatsApp not linked"
        fi
        
        # Check state
        if [[ "$status_line" =~ "│ OK" ]]; then
            log "INFO" "WhatsApp state: OK"
        elif [[ "$status_line" =~ "│ ERROR" ]]; then
            issues+=("error_state")
            status="unhealthy"
            log "ERROR" "WhatsApp in error state"
        elif [[ "$status_line" =~ "│ DISCONNECTED" ]]; then
            issues+=("disconnected")
            status="unhealthy"
            log "ERROR" "WhatsApp disconnected"
        fi
    fi
    
    # Auto-fix
    if [[ "$AUTO_FIX" == "true" ]] && [[ "$status" == "unhealthy" ]]; then
        if attempt_reconnect; then
            status="recovery_initiated"
        else
            status="recovery_failed"
        fi
    fi
    
    log "INFO" "Health check complete: status=$status"
    
    # Output
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        local healthy="false"
        [[ "$status" == "healthy" || "$status" == "recovery_initiated" ]] && healthy="true"
        echo "{\"status\":\"$status\",\"healthy\":$healthy,\"enabled\":\"$enabled\",\"linked\":$linked,\"phone\":\"$phone\",\"auth_age\":\"$auth_age\"}"
    else
        case "$status" in
            healthy)
                echo "WHATSAPP_OK"
                exit 0
                ;;
            pending|recovery_initiated)
                echo "WHATSAPP_PENDING: $status"
                exit 0
                ;;
            disabled)
                echo "WHATSAPP_DISABLED"
                exit 0
                ;;
            *)
                echo "WHATSAPP_FAIL: ${issues[*]:-unknown}"
                exit 1
                ;;
        esac
    fi
}

main "$@"
