#!/bin/bash
# gateway_supervisor.sh - Supervisor simples para gateway no WSL
# Substitui systemd que nao funciona bem com cgroups no WSL2

PIDFILE=/tmp/clawdbot-gateway.pid
LOGFILE=/root/clawd/memory/gateway-supervisor.log
PORT=18789

log() {
    echo "[2026-02-03T20:49:58-03:00] " >> ""
    echo ""
}

cleanup() {
    log "Recebido sinal de parada"
    if [ -f "" ]; then
        PID=
        kill -15 "" 2>/dev/null
        sleep 2
        kill -9 "" 2>/dev/null
        rm -f ""
    fi
    fuser -k /tcp 2>/dev/null
    exit 0
}

trap cleanup SIGTERM SIGINT

start_gateway() {
    fuser -k /tcp 2>/dev/null
    sleep 2
    export HOME=/root
    export PATH="/usr/bin:/usr/local/bin:/root/.npm-global/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/IgorPC/bin:/mnt/c/Program Files/Git/mingw64/bin:/mnt/c/Program Files/Git/usr/local/bin:/mnt/c/Program Files/Git/usr/bin:/mnt/c/Program Files/Git/usr/bin:/mnt/c/Program Files/Git/mingw64/bin:/mnt/c/Program Files/Git/usr/bin:/mnt/c/Users/IgorPC/bin:/mnt/c/Python314/Scripts:/mnt/c/Python314:/mnt/c/Python312/Scripts:/mnt/c/Python312:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0:/mnt/c/WINDOWS/System32/OpenSSH:/mnt/c/Program Files/dotnet:/mnt/c/Program Files/Intel/WiFi/bin:/mnt/c/Program Files/Common Files/Intel/WirelessCommon:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA app/NvDLISR:/mnt/c/Program Files (x86)/HP/Common/HPDestPlgIn:/mnt/c/Program Files/PowerShell/7:/mnt/c/Program Files/nodejs:/mnt/c/ProgramData/chocolatey/bin:/mnt/c/Program Files/GitHub CLI:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/Program Files/WezTerm:/mnt/c/Program Files/Git/cmd:/mnt/c/Users/IgorPC/scoop/shims:/mnt/c/Python314/Scripts:/mnt/c/Python314:/mnt/c/Python312/Scripts:/mnt/c/Python312:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0:/mnt/c/WINDOWS/System32/OpenSSH:/mnt/c/Program Files/dotnet:/mnt/c/Program Files/Intel/WiFi/bin:/mnt/c/Program Files/Common Files/Intel/WirelessCommon:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA app/NvDLISR:/mnt/c/Program Files/Git/cmd:/mnt/c/Program Files (x86)/HP/Common/HPDestPlgIn:/mnt/c/Program Files/PowerShell/7:/mnt/c/Program Files/nodejs:/mnt/c/ProgramData/chocolatey/bin:/mnt/c/Users/IgorPC/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/IgorPC/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/c/Users/IgorPC/.lmstudio/bin:/mnt/c/Users/IgorPC/AppData/Local/Programs/Ollama:/mnt/c/Users/IgorPC/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/IgorPC/AppData/Local/Microsoft/WinGet/Packages/astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe:/mnt/c/Users/IgorPC/AppData/Local/Microsoft/WinGet/Links:/mnt/c/Users/IgorPC/AppData/Local/Programs/Antigravity/bin:/mnt/c/Users/IgorPC/AppData/Roaming/npm:/mnt/c/Users/IgorPC/.local/bin:/mnt/c/Users/IgorPC/AppData/Local/GitHubDesktop/bin:/mnt/c/Users/IgorPC/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin:/mnt/c/Users/IgorPC/AppData/Local/Microsoft/WinGet/Packages/Google.FirebaseCLI_Microsoft.Winget.Source_8wekyb3d8bbwe:/mnt/c/Users/IgorPC/scripts:/mnt/c/Users/IgorPC/scripts:/mnt/c/Users/IgorPC/AppData/Roaming/Python/Python314/Scripts:/mnt/c/Program Files/Git/usr/bin/vendor_perl:/mnt/c/Program Files/Git/usr/bin/core_perl"
    /usr/bin/node /usr/lib/node_modules/openclaw/dist/entry.js gateway --port  &
    echo  > ""
    log "Gateway iniciado PID="
}

log "Supervisor iniciando"
start_gateway

while true; do
    if [ -f "" ]; then
        PID=
        if ! kill -0 "" 2>/dev/null; then
            log "Gateway morreu, reiniciando em 10s..."
            sleep 10
            start_gateway
        fi
    else
        log "PIDFILE nao existe, reiniciando..."
        sleep 5
        start_gateway
    fi
    sleep 30
done
