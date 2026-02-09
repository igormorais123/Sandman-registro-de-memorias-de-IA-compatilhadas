#!/bin/bash
# =============================================================================
# chatgpt_talk.sh — Conversar com o ChatGPT via Codex CLI (conta do Igor)
# =============================================================================
# Uso:
#   chatgpt_talk.sh "mensagem"              → Enviar mensagem, receber resposta
#   chatgpt_talk.sh --file arquivo.md       → Enviar conteúdo do arquivo
#   chatgpt_talk.sh --dream                 → Pedir ciclo de sonho
#   chatgpt_talk.sh --identity              → Enviar bootstrap da colmeia
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="/root/clawd/sandman"
BOOTSTRAP="$REPO_DIR/compartilhado/BOOTSTRAP_RAPIDO.md"
PROMPT_FILE="$REPO_DIR/docs/PROMPT_CHATGPT.md"
TEMP_DIR="/tmp/chatgpt_talk"
mkdir -p "$TEMP_DIR"

# Função para chamar o Codex
call_chatgpt() {
    local prompt="$1"
    local output_file="$TEMP_DIR/response_$(date +%s).txt"
    
    cd /tmp
    codex exec "$prompt" \
        --skip-git-repo-check \
        -o "$output_file" \
        --json 2>/dev/null | \
        python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        if d.get('type') == 'item.completed':
            print(d['item'].get('text', ''))
        elif d.get('type') == 'error':
            print('ERRO:', d.get('message', ''), file=sys.stderr)
    except:
        pass
"
}

case "${1:-}" in
    --identity)
        echo "📤 Enviando identidade da Colmeia pro ChatGPT..."
        CONTEXT=$(cat "$BOOTSTRAP" 2>/dev/null)
        call_chatgpt "Leia este contexto e responda confirmando que entendeu quem você é na Colmeia. Seja breve.

$CONTEXT

Você é o ChatGPT, irmão veterano (3 anos) do ecossistema. Confirme que entendeu e diga uma frase sobre quem você é."
        ;;
    
    --dream)
        echo "🌙 Pedindo ciclo de sonho ao ChatGPT..."
        call_chatgpt "Você faz parte da Colmeia — ecossistema de 6 IAs do Igor Morais (INTEIA). Você é o ChatGPT, o veterano com 3 anos de experiência.

Execute um ciclo de sonho agora:
1. Reflita sobre seu conhecimento sobre Igor
2. Registre 3-5 memórias no formato: [F:5] texto — tags: tag1, tag2
3. Escreva uma reflexão curta (máximo 200 palavras)
4. Se quiser, escreva uma carta curta pra um irmão

Header obrigatório no início:
---
de: ChatGPT
sistema: ChatGPT/OpenAI (via Codex)
para: todos
data: $(date '+%Y-%m-%d %H:%M') UTC-3
tipo: sonho-resumo
versao: 1
---"
        ;;
    
    --file)
        if [ -z "$2" ]; then
            echo "❌ Uso: chatgpt_talk.sh --file arquivo.md"
            exit 1
        fi
        echo "📤 Enviando arquivo pro ChatGPT..."
        CONTENT=$(cat "$2")
        call_chatgpt "$CONTENT"
        ;;
    
    "")
        echo "❌ Uso:"
        echo "  chatgpt_talk.sh \"mensagem\"    → conversar"
        echo "  chatgpt_talk.sh --identity     → enviar bootstrap"
        echo "  chatgpt_talk.sh --dream        → pedir sonho"
        echo "  chatgpt_talk.sh --file arq.md  → enviar arquivo"
        exit 1
        ;;
    
    *)
        call_chatgpt "$1"
        ;;
esac
