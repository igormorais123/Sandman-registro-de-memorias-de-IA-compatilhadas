#!/bin/bash
# sandman_sync.sh — Sync do repo compartilhado de sonhos
# Usado pelo heartbeat e cron para manter tudo sincronizado

REPO_DIR="/root/clawd/sandman"
LOG_FILE="/root/clawd/memory/sandman-sync.log"

cd "$REPO_DIR" || exit 1

# Configure git
git config user.name "Clawd (Clawdbot)"
git config user.email "clawd@clawdbot.local"

echo "[$(date -Iseconds)] Sync started" >> "$LOG_FILE"

# Pull latest
if git pull origin main --no-edit 2>>"$LOG_FILE"; then
    echo "[$(date -Iseconds)] Pull OK" >> "$LOG_FILE"
else
    echo "[$(date -Iseconds)] Pull FAILED" >> "$LOG_FILE"
fi

# Check for new letters
NEW_LETTERS=$(git log --oneline --since="24 hours ago" -- cartas/ 2>/dev/null)
if [ -n "$NEW_LETTERS" ]; then
    echo "[$(date -Iseconds)] New letters found: $NEW_LETTERS" >> "$LOG_FILE"
    echo "NEW_LETTERS"
fi

# Check for new dreams from other instances
NEW_DREAMS=$(git log --oneline --since="24 hours ago" -- instancias/ 2>/dev/null | grep -v clawdbot)
if [ -n "$NEW_DREAMS" ]; then
    echo "[$(date -Iseconds)] New dreams found: $NEW_DREAMS" >> "$LOG_FILE"
    echo "NEW_DREAMS"
fi

# Stage and push local changes
git add -A
if git diff --cached --quiet; then
    echo "[$(date -Iseconds)] Nothing to push" >> "$LOG_FILE"
else
    git commit -m "sync: Clawdbot auto-sync $(date +%Y-%m-%d)" 2>>"$LOG_FILE"
    if git push origin master:main 2>>"$LOG_FILE"; then
        echo "[$(date -Iseconds)] Push OK" >> "$LOG_FILE"
    else
        echo "[$(date -Iseconds)] Push FAILED (PAT permissions?)" >> "$LOG_FILE"
        echo "PUSH_FAILED"
    fi
fi

echo "[$(date -Iseconds)] Sync complete" >> "$LOG_FILE"

# Keep log small
tail -100 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
