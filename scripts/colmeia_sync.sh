#!/bin/bash
# Sync bidirecional da Colmeia (WSL <-> Windows <-> GitHub)
# Uso: bash colmeia_sync.sh [push|pull|both]

MODE=${1:-both}
WSL_REPO="/root/clawd"
WIN_REPO="/mnt/c/Users/IgorPC/Colmeia"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Sync WSL -> GitHub (sem secrets)
sync_wsl_push() {
    log "WSL: Verificando mudanças..."
    cd "$WSL_REPO"
    
    # Nunca adicionar tudo - ser seletivo
    git add -u  # Só arquivos já rastreados
    
    if [[ -n $(git diff --cached --name-only) ]]; then
        log "WSL: Mudanças detectadas, fazendo commit..."
        git commit -m "sync: auto-sync $(date '+%Y-%m-%d %H:%M')"
    fi
    
    log "WSL: Push para GitHub..."
    git push origin main 2>&1 && log "WSL: Push OK" || log "WSL: Push FALHOU"
}

# Sync GitHub -> Windows
sync_win_pull() {
    log "WIN: Pull do GitHub..."
    cd "$WIN_REPO"
    git pull origin main 2>&1 && log "WIN: Pull OK" || log "WIN: Pull FALHOU"
}

# Sync GitHub -> WSL
sync_wsl_pull() {
    log "WSL: Pull do GitHub..."
    cd "$WSL_REPO"
    git pull origin main 2>&1 && log "WSL: Pull OK" || log "WSL: Pull FALHOU"
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
