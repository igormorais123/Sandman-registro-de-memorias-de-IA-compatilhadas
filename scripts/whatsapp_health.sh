#!/bin/bash
# Script de health check do WhatsApp
# Verifica conexão e tenta reconectar se necessário

STATUS=$(clawdbot status 2>/dev/null | grep -i whatsapp)

if echo "$STATUS" | grep -q "linked"; then
    echo "WHATSAPP_OK"
    exit 0
fi

# WhatsApp desconectado - tentar reconectar
echo "WHATSAPP_DISCONNECTED - Tentando reconectar..."

# Tentar reconectar
RECONNECT=$(timeout 60 clawdbot channels login --channel whatsapp --account default 2>&1)

if echo "$RECONNECT" | grep -q "Linked"; then
    echo "WHATSAPP_RECONNECTED"
    exit 0
else
    echo "WHATSAPP_ALERT - Falha ao reconectar: $RECONNECT"
    exit 1
fi
