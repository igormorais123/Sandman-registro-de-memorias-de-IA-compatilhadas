#!/bin/bash
# =============================================================================
# log_event.sh — Logger estruturado do ecossistema Sandman
# =============================================================================
# Uso: log_event.sh <instancia> <tipo> <mensagem>
#
# Tipos válidos: sonho, carta, sync, erro, conflito, sistema
#
# Output: append em logs/YYYY-MM.log
# Formato: [YYYY-MM-DD HH:MM UTC-3] [instancia] [tipo] mensagem
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$REPO_DIR/logs"

# Cores para terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Tipos válidos
TIPOS_VALIDOS=("sonho" "carta" "sync" "erro" "conflito" "sistema")

usage() {
    echo "Uso: log_event.sh <instancia> <tipo> <mensagem>"
    echo ""
    echo "Instâncias: clawdbot, sandman, onir, chatgpt"
    echo "Tipos: ${TIPOS_VALIDOS[*]}"
    echo ""
    echo "Exemplos:"
    echo "  log_event.sh clawdbot sonho 'Ciclo de sonho executado. 5 memórias processadas.'"
    echo "  log_event.sh sandman sync 'Pull/push concluído com sucesso.'"
    echo "  log_event.sh onir carta 'Carta enviada para clawdbot.'"
    echo "  log_event.sh clawdbot erro 'Falha no push: conflito de merge.'"
}

validar_tipo() {
    local tipo="$1"
    for t in "${TIPOS_VALIDOS[@]}"; do
        if [[ "$t" == "$tipo" ]]; then
            return 0
        fi
    done
    return 1
}

# Verificar argumentos
if [[ $# -lt 3 ]]; then
    echo -e "${RED}Erro: argumentos insuficientes.${NC}"
    usage
    exit 1
fi

INSTANCIA="$1"
TIPO="$2"
shift 2
MENSAGEM="$*"

# Validar tipo
if ! validar_tipo "$TIPO"; then
    echo -e "${RED}Erro: tipo '$TIPO' inválido.${NC}"
    echo "Tipos válidos: ${TIPOS_VALIDOS[*]}"
    exit 1
fi

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Gerar timestamp (UTC-3 = America/Sao_Paulo)
TIMESTAMP=$(TZ="America/Sao_Paulo" date "+%Y-%m-%d %H:%M")
LOG_FILE="$LOG_DIR/$(TZ="America/Sao_Paulo" date "+%Y-%m").log"

# Formatar linha de log
LOG_LINE="[$TIMESTAMP UTC-3] [$INSTANCIA] [$TIPO] $MENSAGEM"

# Append ao arquivo
echo "$LOG_LINE" >> "$LOG_FILE"

# Output colorido no terminal
case "$TIPO" in
    erro|conflito)
        echo -e "${RED}📝 $LOG_LINE${NC}"
        ;;
    sync)
        echo -e "${CYAN}📝 $LOG_LINE${NC}"
        ;;
    sonho)
        echo -e "${GREEN}📝 $LOG_LINE${NC}"
        ;;
    *)
        echo -e "${YELLOW}📝 $LOG_LINE${NC}"
        ;;
esac
