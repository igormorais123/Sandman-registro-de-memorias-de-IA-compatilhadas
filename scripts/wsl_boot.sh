#!/bin/bash
# wsl_boot.sh - Script de boot do WSL
# Executado automaticamente via /etc/wsl.conf [boot] command
# Versao: 1.0 (2026-02-13)

LOG="/root/clawd/memory/wsl-boot.log"

log() {
    echo "[2026-02-13T08:40:44-03:00] " >> "" 2>/dev/null
}

log "=== WSL BOOT START ==="

# Aguardar systemd inicializar
sleep 3

# Garantir que PM2 nao inicie (legado removido)
if command -v pm2 &>/dev/null; then
    pm2 kill 2>/dev/null
    log "PM2 killed (legacy)"
fi

# Verificar se openclaw-gateway vai iniciar via systemd
if systemctl --user -M root@ is-enabled openclaw-gateway.service &>/dev/null; then
    log "openclaw-gateway.service esta habilitado (systemd gerencia)"
else
    log "WARN: openclaw-gateway.service nao habilitado"
fi

# Limpar locks orfaos
rm -f /tmp/openclaw_whatsapp_last_reconnect 2>/dev/null
rm -f /tmp/openclaw_whatsapp_health_state 2>/dev/null

log "=== WSL BOOT COMPLETE ==="
