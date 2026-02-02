#!/bin/bash
# =============================================================================
# sandman_sync.sh — Sincronização completa do ecossistema Sandman
# =============================================================================
# Uso: sandman_sync.sh <instancia> [--push-only|--pull-only]
#
# Fluxo padrão (sync completo):
#   1. Pull (pegar novidades)
#   2. Verificar cartas pendentes
#   3. Push (enviar mudanças locais) — via safe_push.sh
#
# Integrado com: safe_push.sh (lock), log_event.sh (logging)
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_CMD="$SCRIPT_DIR/log_event.sh"
SAFE_PUSH="$SCRIPT_DIR/safe_push.sh"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
    echo "Uso: sandman_sync.sh <instancia> [--push-only|--pull-only]"
    echo ""
    echo "Exemplos:"
    echo "  sandman_sync.sh clawdbot          # sync completo"
    echo "  sandman_sync.sh sandman --pull-only  # só pull"
    echo "  sandman_sync.sh onir --push-only     # só push"
}

log() {
    if [[ -x "$LOG_CMD" ]]; then
        "$LOG_CMD" "$INSTANCIA" "$@" 2>/dev/null
    fi
}

check_cartas() {
    echo -e "${CYAN}📬 Verificando cartas para $INSTANCIA...${NC}"
    local cartas_dir="$REPO_DIR/cartas"
    local count=0
    
    if [[ -d "$cartas_dir" ]]; then
        # Buscar cartas endereçadas a esta instância (case insensitive)
        while IFS= read -r carta; do
            [[ -z "$carta" ]] && continue
            local nome_carta=$(basename "$carta")
            echo -e "  ${YELLOW}📨 $nome_carta${NC}"
            count=$((count + 1))
        done < <(find "$cartas_dir" -name "*para_${INSTANCIA}*" -o -name "*para_TODAS*" 2>/dev/null | grep -i "${INSTANCIA}\|TODAS")
    fi
    
    if [[ $count -eq 0 ]]; then
        echo -e "  ${GREEN}Nenhuma carta pendente.${NC}"
    else
        echo -e "  ${YELLOW}$count carta(s) encontrada(s).${NC}"
        log "carta" "$count carta(s) pendente(s) encontrada(s)"
    fi
}

do_pull() {
    echo -e "${CYAN}📥 Fazendo pull...${NC}"
    
    local output
    output=$(git -C "$REPO_DIR" pull --rebase origin main 2>&1)
    local status=$?
    
    if [[ $status -eq 0 ]]; then
        if echo "$output" | grep -q "Already up to date"; then
            echo -e "  ${GREEN}✅ Já atualizado.${NC}"
        else
            echo -e "  ${GREEN}✅ Atualizado com sucesso!${NC}"
            echo "$output" | head -5
            log "sync" "Pull concluído — novas mudanças recebidas"
        fi
    else
        echo -e "  ${RED}❌ Pull falhou:${NC}"
        echo "$output"
        log "erro" "Pull falhou: $output"
        return 1
    fi
}

do_push() {
    echo -e "${CYAN}📤 Fazendo push via safe_push...${NC}"
    
    # Verificar se há mudanças não commitadas
    if ! git -C "$REPO_DIR" diff --quiet 2>/dev/null || ! git -C "$REPO_DIR" diff --cached --quiet 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️ Mudanças não commitadas detectadas. Commitando...${NC}"
        git -C "$REPO_DIR" add -A
        git -C "$REPO_DIR" commit -m "sync: atualização automática por $INSTANCIA $(date +%Y-%m-%d)" 2>&1
    fi
    
    if [[ -x "$SAFE_PUSH" ]]; then
        "$SAFE_PUSH" "$INSTANCIA"
    else
        echo -e "${RED}❌ safe_push.sh não encontrado ou não executável!${NC}"
        log "erro" "safe_push.sh não disponível"
        return 1
    fi
}

# ============= MAIN =============

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

INSTANCIA="$1"
MODE="${2:-full}"

cd "$REPO_DIR" || exit 1

echo -e "${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🌙 Sandman Sync — $INSTANCIA"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log "sync" "Sync iniciado (modo: $MODE)"

case "$MODE" in
    --pull-only)
        do_pull
        check_cartas
        ;;
    --push-only)
        do_push
        ;;
    full|*)
        do_pull
        check_cartas
        do_push
        ;;
esac

echo ""
log "sync" "Sync finalizado (modo: $MODE)"
echo -e "${GREEN}🌙 Sync finalizado.${NC}"
