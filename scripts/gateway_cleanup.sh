#!/bin/bash
# gateway_cleanup.sh - Limpa processos órfãos antes de iniciar o gateway
# Usado como ExecStartPre no systemd service

PORT=${1:-18789}
MAX_WAIT=10

echo "[$(date -Iseconds)] Gateway cleanup iniciando para porta $PORT"

# Verifica se a porta está ocupada
PID=$(lsof -t -i :$PORT 2>/dev/null | head -1)

if [ -n "$PID" ]; then
    PROC_NAME=$(ps -p $PID -o comm= 2>/dev/null)
    echo "[$(date -Iseconds)] Porta $PORT ocupada por PID $PID ($PROC_NAME)"
    
    # Se for um processo clawdbot/openclaw, tenta terminar gracefully
    if [[ "$PROC_NAME" == *"clawdbot"* ]] || [[ "$PROC_NAME" == *"node"* ]]; then
        echo "[$(date -Iseconds)] Enviando SIGTERM para $PID"
        kill -15 $PID 2>/dev/null
        
        # Aguarda até MAX_WAIT segundos
        for i in $(seq 1 $MAX_WAIT); do
            if ! kill -0 $PID 2>/dev/null; then
                echo "[$(date -Iseconds)] Processo $PID terminou após ${i}s"
                break
            fi
            sleep 1
        done
        
        # Se ainda está rodando, força kill
        if kill -0 $PID 2>/dev/null; then
            echo "[$(date -Iseconds)] Forçando kill -9 em $PID"
            kill -9 $PID 2>/dev/null
            sleep 1
        fi
    fi
fi

# Verifica novamente
if lsof -i :$PORT >/dev/null 2>&1; then
    echo "[$(date -Iseconds)] ERRO: Porta $PORT ainda ocupada após cleanup"
    lsof -i :$PORT
    exit 1
fi

echo "[$(date -Iseconds)] Porta $PORT livre, pronto para iniciar"
exit 0
