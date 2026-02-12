#!/bin/bash
# Sync bidirecional da Colmeia (WSL <-> Windows <-> GitHub)
# Uso: bash colmeia_sync.sh [push|pull|both]
# 
# FEATURES:
# - Auto-configura pull.rebase para evitar divergências
# - Smart pull: tenta rebase primeiro, fallback para merge
# - Detecta branch principal automaticamente (main/master)
# - Stash automático de mudanças locais durante rebase

MODE=${1:-both}
WSL_REPO="/root/clawd"
WIN_REPO="/mnt/c/Users/IgorPC/Colmeia"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Configura o repo para usar rebase por padrão
configure_repo() {
    local repo="$1"
    if [[ -d "$repo/.git" ]]; then
        cd "$repo"
        git config pull.rebase true 2>/dev/null
    fi
}

# Pull inteligente que lida com divergências
smart_pull() {
    local repo="$1"
    local name="$2"
    
    cd "$repo" 2>/dev/null || { log "$name: Repo não existe em $repo"; return 1; }
    
    # Configura rebase
    configure_repo "$repo"
    
    # Fetch primeiro para ver o estado
    git fetch origin 2>/dev/null
    
    # Detecta branch principal (main ou master)
    local branch=$(git symbolic-ref --short HEAD 2>/dev/null)
    local remote_branch="origin/$branch"
    
    # Verifica se há divergência
    local local_ahead=$(git rev-list "$remote_branch"..HEAD --count 2>/dev/null || echo 0)
    local remote_ahead=$(git rev-list HEAD.."$remote_branch" --count 2>/dev/null || echo 0)
    
    if [[ "$local_ahead" -gt 0 ]] && [[ "$remote_ahead" -gt 0 ]]; then
        log "$name: Branches divergentes (local: +$local_ahead, remote: +$remote_ahead)"
        log "$name: Tentando rebase..."
        
        # Stash mudanças locais se houver
        local stashed=false
        if [[ -n $(git status --porcelain) ]]; then
            git stash 2>/dev/null && stashed=true
        fi
        
        # Tenta rebase
        if git rebase "$remote_branch" 2>/dev/null; then
            log "$name: Rebase OK"
        else
            log "$name: Rebase falhou, abortando e tentando merge..."
            git rebase --abort 2>/dev/null
            if git merge "$remote_branch" -m "merge: resolve divergência $(date '+%Y-%m-%d')" 2>/dev/null; then
                log "$name: Merge OK"
            else
                log "$name: Merge também falhou - precisa resolução manual"
                git merge --abort 2>/dev/null
                [[ "$stashed" == true ]] && git stash pop 2>/dev/null
                return 1
            fi
        fi
        
        # Restaura stash
        [[ "$stashed" == true ]] && git stash pop 2>/dev/null
        
    elif [[ "$remote_ahead" -gt 0 ]]; then
        log "$name: Atualizando (remote +$remote_ahead commits)..."
        git pull --rebase origin "$branch" 2>&1 && log "$name: Pull OK" || log "$name: Pull FALHOU"
    else
        log "$name: Já está atualizado"
    fi
}

# Sync WSL -> GitHub (sem secrets)
sync_wsl_push() {
    log "WSL: Verificando mudanças..."
    cd "$WSL_REPO" 2>/dev/null || { log "WSL: Repo não existe"; return 1; }
    
    # Configura rebase
    configure_repo "$WSL_REPO"
    
    local branch=$(git symbolic-ref --short HEAD 2>/dev/null)
    
    # Nunca adicionar tudo - ser seletivo
    git add -u  # Só arquivos já rastreados
    
    if [[ -n $(git diff --cached --name-only) ]]; then
        log "WSL: Mudanças detectadas, fazendo commit..."
        git commit -m "sync: auto-sync $(date '+%Y-%m-%d %H:%M')"
    fi
    
    # Primeiro faz pull inteligente para resolver divergências
    smart_pull "$WSL_REPO" "WSL"
    
    log "WSL: Push para GitHub..."
    git push origin "$branch" 2>&1 && log "WSL: Push OK" || log "WSL: Push FALHOU"
}

# Sync GitHub -> Windows
sync_win_pull() {
    if [[ -d "$WIN_REPO" ]]; then
        smart_pull "$WIN_REPO" "WIN"
    else
        log "WIN: Repo não encontrado em $WIN_REPO (Windows pode estar desligado)"
    fi
}

# Sync GitHub -> WSL
sync_wsl_pull() {
    smart_pull "$WSL_REPO" "WSL"
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
    both|*)
        sync_wsl_push
        sync_win_pull
        ;;
esac

log "Sync completo!"
