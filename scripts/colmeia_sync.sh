#!/bin/bash
# Sync bidirecional da Colmeia (WSL <-> Windows <-> GitHub)
# Uso: bash colmeia_sync.sh [push|pull|both|fix]
# 
# fix: Resolve branches divergentes automaticamente

set -euo pipefail

MODE=${1:-both}
WSL_REPO="/root/clawd"
WIN_REPO="/mnt/c/Users/IgorPC/Colmeia"
BRANCH="${COLMEIA_BRANCH:-main}"  # Default to main, override with env var

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_ok() {
    log "${GREEN}✓ $1${NC}"
}

log_warn() {
    log "${YELLOW}⚠ $1${NC}"
}

log_err() {
    log "${RED}✗ $1${NC}"
}

# Verifica se há divergência entre local e remote
check_divergence() {
    local repo="$1"
    cd "$repo"
    git fetch origin "$BRANCH" 2>/dev/null
    
    local LOCAL=$(git rev-parse "$BRANCH" 2>/dev/null || echo "")
    local REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")
    local BASE=$(git merge-base "$BRANCH" "origin/$BRANCH" 2>/dev/null || echo "")
    
    if [ -z "$LOCAL" ] || [ -z "$REMOTE" ]; then
        echo "unknown"
    elif [ "$LOCAL" = "$REMOTE" ]; then
        echo "synced"
    elif [ "$LOCAL" = "$BASE" ]; then
        echo "behind"
    elif [ "$REMOTE" = "$BASE" ]; then
        echo "ahead"
    else
        echo "diverged"
    fi
}

# Resolve branches divergentes com rebase inteligente
fix_divergence() {
    local repo="$1"
    cd "$repo"
    
    log "Verificando divergência em $repo..."
    local status=$(check_divergence "$repo")
    
    case "$status" in
        synced)
            log_ok "Branches sincronizadas"
            return 0
            ;;
        behind)
            log "Branch atrás do remote, fazendo pull..."
            git pull --rebase origin "$BRANCH" && log_ok "Pull OK" || {
                log_warn "Rebase falhou, tentando merge..."
                git rebase --abort 2>/dev/null || true
                git pull --no-rebase origin "$BRANCH"
            }
            ;;
        ahead)
            log_ok "Branch à frente do remote (push pendente)"
            return 0
            ;;
        diverged)
            log_warn "Branches divergentes! Tentando rebase..."
            
            # Stash any local changes
            local stashed=false
            if [[ -n $(git status --porcelain) ]]; then
                git stash push -m "colmeia_sync auto-stash $(date '+%Y-%m-%d_%H:%M')"
                stashed=true
            fi
            
            # Try rebase first
            if git pull --rebase origin "$BRANCH" 2>/dev/null; then
                log_ok "Rebase bem sucedido"
            else
                log_warn "Rebase falhou, tentando merge..."
                git rebase --abort 2>/dev/null || true
                
                # Try regular merge
                if git pull --no-rebase origin "$BRANCH" 2>/dev/null; then
                    log_ok "Merge bem sucedido"
                else
                    # Last resort: merge with unrelated histories
                    log_warn "Merge normal falhou, tentando com --allow-unrelated-histories..."
                    git merge origin/"$BRANCH" --allow-unrelated-histories --strategy-option=ours --no-edit -m "merge: resolve divergência automática" || {
                        log_err "FALHA: Divergência não pôde ser resolvida automaticamente"
                        log "Resolva manualmente com: git mergetool"
                        $stashed && git stash pop
                        return 1
                    }
                    log_ok "Merge com históricos não relacionados OK"
                fi
            fi
            
            # Restore stashed changes
            $stashed && git stash pop && log "Stash restaurado"
            ;;
        *)
            log_warn "Status desconhecido: $status"
            ;;
    esac
}

# Sync WSL -> GitHub (sem secrets)
sync_wsl_push() {
    log "WSL: Verificando mudanças..."
    cd "$WSL_REPO"
    
    # Primeiro resolve qualquer divergência
    fix_divergence "$WSL_REPO"
    
    # Nunca adicionar tudo - ser seletivo
    git add -u  # Só arquivos já rastreados
    
    if [[ -n $(git diff --cached --name-only) ]]; then
        log "WSL: Mudanças detectadas, fazendo commit..."
        git commit -m "sync: auto-sync $(date '+%Y-%m-%d %H:%M')"
    fi
    
    log "WSL: Push para GitHub..."
    if git push origin "$BRANCH" 2>&1; then
        log_ok "WSL: Push OK"
    else
        log_err "WSL: Push FALHOU"
        return 1
    fi
}

# Sync GitHub -> Windows
sync_win_pull() {
    if [ ! -d "$WIN_REPO" ]; then
        log_warn "WIN: Repositório não encontrado em $WIN_REPO"
        return 0
    fi
    
    log "WIN: Pull do GitHub..."
    cd "$WIN_REPO"
    
    if git pull --rebase origin "$BRANCH" 2>&1; then
        log_ok "WIN: Pull OK"
    else
        log_warn "WIN: Rebase falhou, tentando merge..."
        git rebase --abort 2>/dev/null || true
        git pull --no-rebase origin "$BRANCH" && log_ok "WIN: Merge OK" || log_err "WIN: Pull FALHOU"
    fi
}

# Sync GitHub -> WSL
sync_wsl_pull() {
    log "WSL: Pull do GitHub..."
    cd "$WSL_REPO"
    fix_divergence "$WSL_REPO"
}

# Modo de diagnóstico
diagnose() {
    log "=== Diagnóstico da Colmeia ==="
    
    log "\n--- WSL ($WSL_REPO) ---"
    cd "$WSL_REPO"
    echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
    echo "Status: $(check_divergence "$WSL_REPO")"
    git status --short | head -10
    
    if [ -d "$WIN_REPO" ]; then
        log "\n--- Windows ($WIN_REPO) ---"
        cd "$WIN_REPO"
        echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
        echo "Status: $(check_divergence "$WIN_REPO")"
        git status --short | head -10
    fi
    
    log "\n--- Configuração Git ---"
    cd "$WSL_REPO"
    echo "pull.rebase: $(git config --get pull.rebase || echo 'not set')"
    echo "merge.ff: $(git config --get merge.ff || echo 'not set')"
}

case $MODE in
    push)
        sync_wsl_push
        sync_win_pull
        ;;
    pull)
        sync_wsl_pull
        sync_win_pull
        ;;
    fix)
        fix_divergence "$WSL_REPO"
        ;;
    diagnose|status)
        diagnose
        ;;
    both|*)
        sync_wsl_push
        sync_win_pull
        ;;
esac

log_ok "Sync completo!"
