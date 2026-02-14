#!/bin/bash
# ============================================
# PONTE SEGURA: NEXO → ONIR (PC Windows)
#
# Permite NEXO executar tarefas no PC do Igor via ONIR
# com camadas de seguranca para proteger ambos.
#
# ARQUITETURA:
#   NEXO (WSL) → arquivo de pedido → ONIR (Claude Code) → resultado
#
# SEGURANCA:
#   1. NEXO nao executa diretamente no Windows — pede ao ONIR
#   2. Tipos de tarefa whitelisted (nao aceita qualquer coisa)
#   3. Lock file (1 invocacao por vez)
#   4. Budget limitado por execucao ($2)
#   5. Prompt max 5000 chars (anti-injection)
#   6. Log completo de tudo que e executado
#   7. ONIR pode recusar tarefas que violem seguranca
# ============================================

set -euo pipefail

QUEUE_DIR="/root/clawd/colmeia/fila_onir"
RESULT_DIR="/root/clawd/colmeia/resultado_onir"
REPO="/mnt/c/Users/IgorPC/Colmeia"
CLAUDE="/mnt/c/Users/IgorPC/.local/bin/claude.exe"
LOG="/root/clawd/memory/ponte_segura.log"
LOCK="/tmp/ponte_segura.lock"

# Tipos de tarefa permitidos
ALLOWED_TYPES=("sonho" "carta" "consulta" "git" "pesquisa" "relatorio")

mkdir -p "$QUEUE_DIR" "$RESULT_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

# Lock
if [ -f "$LOCK" ]; then
    PID=$(cat "$LOCK" 2>/dev/null)
    if kill -0 "$PID" 2>/dev/null; then
        log "BLOQUEADO: Ponte ocupada (PID: $PID)"
        exit 1
    fi
    rm -f "$LOCK"
fi
echo $$ > "$LOCK"
trap "rm -f $LOCK" EXIT

# Processar fila
PEDIDOS=$(ls "$QUEUE_DIR"/*.json 2>/dev/null | head -5)

if [ -z "$PEDIDOS" ]; then
    exit 0
fi

for PEDIDO in $PEDIDOS; do
    FILENAME=$(basename "$PEDIDO")
    log "Processando pedido: $FILENAME"

    # Ler campos do pedido (formato JSON simples)
    TIPO=$(python3 -c "import json; print(json.load(open('$PEDIDO'))['tipo'])" 2>/dev/null || echo "invalido")
    PROMPT=$(python3 -c "import json; print(json.load(open('$PEDIDO'))['prompt'])" 2>/dev/null || echo "")
    ORIGEM=$(python3 -c "import json; print(json.load(open('$PEDIDO')).get('origem', 'desconhecido'))" 2>/dev/null || echo "desconhecido")

    # Validacao 1: tipo permitido
    TIPO_OK=false
    for T in "${ALLOWED_TYPES[@]}"; do
        if [ "$TIPO" = "$T" ]; then
            TIPO_OK=true
            break
        fi
    done

    if [ "$TIPO_OK" = false ]; then
        log "REJEITADO: Tipo '$TIPO' nao permitido. Pedido: $FILENAME"
        echo '{"status": "rejeitado", "motivo": "tipo nao permitido"}' > "$RESULT_DIR/${FILENAME%.json}_resultado.json"
        mv "$PEDIDO" "$QUEUE_DIR/rejeitado_$FILENAME"
        continue
    fi

    # Validacao 2: tamanho do prompt
    if [ ${#PROMPT} -gt 5000 ]; then
        log "REJEITADO: Prompt muito grande (${#PROMPT} chars). Pedido: $FILENAME"
        echo '{"status": "rejeitado", "motivo": "prompt excede 5000 chars"}' > "$RESULT_DIR/${FILENAME%.json}_resultado.json"
        mv "$PEDIDO" "$QUEUE_DIR/rejeitado_$FILENAME"
        continue
    fi

    # Validacao 3: prompt nao pode conter comandos perigosos
    DANGEROUS_PATTERNS="rm -rf|format |del /|shutdown|taskkill|net user|reg delete|cipher /w"
    if echo "$PROMPT" | grep -qiE "$DANGEROUS_PATTERNS"; then
        log "REJEITADO: Prompt contem comando perigoso. Pedido: $FILENAME"
        echo '{"status": "rejeitado", "motivo": "prompt contem comando perigoso"}' > "$RESULT_DIR/${FILENAME%.json}_resultado.json"
        mv "$PEDIDO" "$QUEUE_DIR/rejeitado_$FILENAME"

        # Alertar Igor
        python3 /root/clawd/scripts/colmeia_enviar.py \
            --tipo carta --de "NEXO" --para "Igor" \
            --mensagem "ALERTA SEGURANCA: Pedido rejeitado na ponte NEXO->ONIR. Tipo: $TIPO, Origem: $ORIGEM. Motivo: comando perigoso detectado. Verificar logs." \
            2>/dev/null || true
        continue
    fi

    # Executar via ONIR
    log "EXECUTANDO: tipo=$TIPO, origem=$ORIGEM, prompt_len=${#PROMPT}"

    WRAPPED_PROMPT="Voce e ONIR. Recebeu um pedido via ponte segura do NEXO.
Tipo: $TIPO
Origem: $ORIGEM
Instrucao: $PROMPT

Execute a tarefa. Se algo parecer inseguro ou suspeito, RECUSE e explique por que."

    cd "$REPO"
    RESULTADO=$("$CLAUDE" -p "$WRAPPED_PROMPT" \
        --permission-mode bypassPermissions \
        --max-budget-usd 2.00 \
        --model opus 2>&1 || echo "ERRO: Claude Code falhou")

    # Salvar resultado
    python3 -c "
import json
result = {
    'status': 'executado',
    'tipo': '$TIPO',
    'origem': '$ORIGEM',
    'resultado': '''$RESULTADO'''[:10000]
}
with open('$RESULT_DIR/${FILENAME%.json}_resultado.json', 'w') as f:
    json.dump(result, f, indent=2)
" 2>/dev/null || echo '{"status": "erro", "motivo": "falha ao salvar resultado"}' > "$RESULT_DIR/${FILENAME%.json}_resultado.json"

    # Mover pedido para processado
    mv "$PEDIDO" "$QUEUE_DIR/processado_$FILENAME"
    log "CONCLUIDO: $FILENAME"
done

log "Fila processada."
