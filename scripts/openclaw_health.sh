#!/bin/bash
#===============================================================================
# openclaw_health.sh - OpenClaw Full System Health Check
# 
# Verifica a saúde completa do sistema OpenClaw (gateway + canais).
# Uso: ./openclaw_health.sh [--verbose] [--auto-fix] [--json]
#===============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/openclaw_health_$(date +%Y-%m-%d).log"

# Parse args
VERBOSE=""
AUTO_FIX=""
JSON_OUTPUT=""
for arg in "$@"; do
    case $arg in
        --verbose|-v) VERBOSE="--verbose" ;;
        --auto-fix|-f) AUTO_FIX="--auto-fix" ;;
        --json|-j) JSON_OUTPUT="true" ;;
    esac
done

mkdir -p "$LOG_DIR"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg" >> "$LOG_FILE"
    [[ -n "$VERBOSE" ]] && echo "$msg"
}

main() {
    log "Starting full OpenClaw health check"
    
    local gateway_status="unknown"
    local whatsapp_status="unknown"
    local overall_status="healthy"
    local issues=()
    
    # 1. Gateway health check (must pass first)
    log "Checking gateway health..."
    if "${SCRIPT_DIR}/gateway_health.sh" $VERBOSE $AUTO_FIX > /tmp/gateway_health_result.json 2>&1; then
        gateway_status="healthy"
        log "Gateway: healthy"
    else
        gateway_status=$(cat /tmp/gateway_health_result.json 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unhealthy")
        overall_status="unhealthy"
        issues+=("gateway_$gateway_status")
        log "Gateway: $gateway_status"
    fi
    
    # 2. WhatsApp health check (only if gateway is healthy)
    if [[ "$gateway_status" == "healthy" ]] || [[ "$gateway_status" == "recovered" ]]; then
        log "Checking WhatsApp health..."
        if "${SCRIPT_DIR}/whatsapp_health.sh" $VERBOSE $AUTO_FIX --json > /tmp/whatsapp_health_result.json 2>&1; then
            whatsapp_status="healthy"
            log "WhatsApp: healthy"
        else
            whatsapp_status=$(cat /tmp/whatsapp_health_result.json 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unhealthy")
            if [[ "$whatsapp_status" != "disabled" ]]; then
                overall_status="degraded"
                issues+=("whatsapp_$whatsapp_status")
            fi
            log "WhatsApp: $whatsapp_status"
        fi
    else
        whatsapp_status="skipped"
        log "WhatsApp: skipped (gateway unhealthy)"
    fi
    
    log "Full health check complete: overall=$overall_status gateway=$gateway_status whatsapp=$whatsapp_status"
    
    # Output
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        local issues_json="[]"
        if [[ ${#issues[@]} -gt 0 ]]; then
            issues_json='["'$(IFS='","'; echo "${issues[*]}")'"]'
        fi
        cat <<EOF
{
  "status": "$overall_status",
  "timestamp": "$(date -Iseconds)",
  "components": {
    "gateway": "$gateway_status",
    "whatsapp": "$whatsapp_status"
  },
  "issues": $issues_json
}
EOF
    else
        echo "═══════════════════════════════════════"
        echo "  OpenClaw Health Check"
        echo "═══════════════════════════════════════"
        echo "  Gateway:  ${gateway_status^^}"
        echo "  WhatsApp: ${whatsapp_status^^}"
        echo "───────────────────────────────────────"
        echo "  Overall:  ${overall_status^^}"
        if [[ ${#issues[@]} -gt 0 ]]; then
            echo "  Issues:   ${issues[*]}"
        fi
        echo "═══════════════════════════════════════"
    fi
    
    [[ "$overall_status" == "healthy" ]] && exit 0 || exit 1
}

main "$@"
