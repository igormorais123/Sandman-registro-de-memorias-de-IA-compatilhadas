#!/bin/bash
# =============================================================================
# safe_push.sh — Push seguro com lock file para o ecossistema Sandman
# =============================================================================
# Uso: safe_push.sh <instancia> [mensagem_commit]
#
# Funcionalidades:
# - Lock file para evitar push simultâneo de múltiplas instâncias
# - Retry automático com pull --rebase em caso de conflito
# - Logging integrado via log_event.sh
# - Timeout de 5 minutos para locks stale
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOCK_FILE="$REPO_DIR/.write-lock"
LOG_CMD="$SCRIPT_DIR/log_event.sh"
MAX_RETRIES=3
LOCK_TIMEOUT=300  # 5 minutos em segundos

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

usage() {
    echo "Uso: safe_push.sh <instancia> [mensagem_commit]"
    echo ""
    echo "Se mensagem_commit não for fornecida, faz push dos commits existentes."
    echo ""
    echo "Exemplos:"
    echo "  safe_push.sh clawdbot 'sonho: ciclo 2026-02-02'"
    echo "  safe_push.sh sandman"
}

log() {
    local tipo="$1"
    local msg="$2"
    if [[ -x "$LOG_CMD" ]]; then
        "$LOG_CMD" "$INSTANCIA" "$tipo" "$msg" 2>/dev/null
    fi
}

get_lock_age() {
    if [[ ! -f "$LOCK_FILE" ]]; then
        echo "-1"
        return
    fi
    local lock_ts
    lock_ts=$(head -1 "$LOCK_FILE" 2>/dev/null | grep -oP '\d+' | head -1)
    if [[ -z "$lock_ts" ]]; then
        echo "999999"  # lock corrompido = stale
        return
    fi
    local now
    now=$(date +%s)
    echo $((now - lock_ts))
}

acquire_lock() {
    local age
    age=$(get_lock_age)
    
    if [[ "$age" -ge 0 && "$age" -lt "$LOCK_TIMEOUT" ]]; then
        local owner
        owner=$(sed -n '2p' "$LOCK_FILE" 2>/dev/null || echo "desconhecido")
        echo -e "${YELLOW}⏳ Lock ativo por '$owner' (${age}s atrás). Aguardando...${NC}"
        log "sync" "Aguardando lock de '$owner' (${age}s)"
        
        # Esperar até o lock expirar ou ser removido
        local waited=0
        while [[ -f "$LOCK_FILE" ]]; do
            sleep 5
            waited=$((waited + 5))
            age=$(get_lock_age)
            if [[ "$age" -ge "$LOCK_TIMEOUT" || "$age" -lt 0 ]]; then
                echo -e "${YELLOW}⚠️ Lock expirado (stale). Sobrescrevendo.${NC}"
                log "conflito" "Lock stale de '$owner' removido após ${age}s"
                break
            fi
            if [[ "$waited" -ge "$LOCK_TIMEOUT" ]]; then
                echo -e "${RED}❌ Timeout aguardando lock.${NC}"
                log "erro" "Timeout aguardando lock de '$owner'"
                return 1
            fi
        done
    elif [[ "$age" -ge "$LOCK_TIMEOUT" ]]; then
        local owner
        owner=$(sed -n '2p' "$LOCK_FILE" 2>/dev/null || echo "desconhecido")
        echo -e "${YELLOW}⚠️ Lock stale de '$owner' (${age}s). Sobrescrevendo.${NC}"
        log "conflito" "Lock stale de '$owner' removido"
    fi
    
    # Criar lock
    echo "$(date +%s)" > "$LOCK_FILE"
    echo "$INSTANCIA" >> "$LOCK_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOCK_FILE"
    
    echo -e "${GREEN}🔒 Lock adquirido por '$INSTANCIA'${NC}"
    return 0
}

release_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        rm -f "$LOCK_FILE"
        echo -e "${GREEN}🔓 Lock liberado.${NC}"
    fi
}

do_push() {
    local retry=0
    
    while [[ $retry -lt $MAX_RETRIES ]]; do
        echo -e "${CYAN}📤 Tentativa de push ($((retry + 1))/$MAX_RETRIES)...${NC}"
        
        if git -C "$REPO_DIR" push origin main 2>&1; then
            echo -e "${GREEN}✅ Push concluído com sucesso!${NC}"
            log "sync" "Push concluído com sucesso"
            return 0
        else
            retry=$((retry + 1))
            echo -e "${YELLOW}⚠️ Push falhou. Tentando pull --rebase...${NC}"
            log "sync" "Push falhou, tentando rebase (tentativa $retry)"
            
            if ! git -C "$REPO_DIR" pull --rebase origin main 2>&1; then
                echo -e "${RED}❌ Rebase falhou. Pode haver conflitos manuais.${NC}"
                log "erro" "Rebase falhou — possível conflito manual"
                git -C "$REPO_DIR" rebase --abort 2>/dev/null
                return 1
            fi
        fi
    done
    
    echo -e "${RED}❌ Push falhou após $MAX_RETRIES tentativas.${NC}"
    log "erro" "Push falhou após $MAX_RETRIES tentativas"
    return 1
}

# ============= MAIN =============

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

INSTANCIA="$1"
COMMIT_MSG="$2"

cd "$REPO_DIR" || exit 1

# Se há mensagem de commit, fazer commit primeiro
if [[ -n "$COMMIT_MSG" ]]; then
    echo -e "${CYAN}📝 Commitando: $COMMIT_MSG${NC}"
    git add -A
    git commit -m "$COMMIT_MSG" 2>&1 || true
fi

# Verificar se há algo para push
if git diff --quiet origin/main..HEAD 2>/dev/null; then
    echo -e "${GREEN}✅ Nada para push. Repo já está atualizado.${NC}"
    exit 0
fi

# Adquirir lock
if ! acquire_lock; then
    echo -e "${RED}❌ Não foi possível adquirir o lock. Abortando.${NC}"
    exit 1
fi

# Push com cleanup garantido
trap release_lock EXIT

if do_push; then
    exit 0
else
    exit 1
fi
