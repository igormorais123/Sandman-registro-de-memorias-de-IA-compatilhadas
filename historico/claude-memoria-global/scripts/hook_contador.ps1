# ============================================
# hook_contador.ps1 - Contador de Sessões
# Dispara consolidação a cada 10 sessões
# Sistema de Memória Hierárquica Claude Code
# ============================================

$ErrorActionPreference = "SilentlyContinue"

$memoriaDir = "C:\Users\IgorPC\.claude-memoria-global"
$contadorPath = "$memoriaDir\.contador_sessoes"
$logPath = "$memoriaDir\logs\hook_contador.log"

# Criar pasta de logs se não existir
$logDir = Split-Path $logPath -Parent
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Função para log
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $logPath -Append
}

# Ler contador atual
$contador = 0
if (Test-Path $contadorPath) {
    $conteudo = Get-Content $contadorPath -ErrorAction SilentlyContinue
    if ($conteudo) {
        $contador = [int]$conteudo
    }
}

# Incrementar
$contador++
Set-Content $contadorPath $contador

Write-Log "Sessao #$contador registrada"

# Verificar se atingiu 10 sessões
if ($contador -ge 10) {
    Write-Log "Atingiu 10 sessoes - disparando consolidacao em background"

    # Resetar contador
    Set-Content $contadorPath 0

    # Disparar consolidação em background (não bloqueia)
    $scriptPath = "$memoriaDir\scripts\consolidar.bat"
    if (Test-Path $scriptPath) {
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "`"$scriptPath`"" -WindowStyle Hidden
        Write-Log "Consolidacao disparada via consolidar.bat"
    } else {
        # Fallback: chamar claude diretamente
        Start-Process -FilePath "claude" -ArgumentList "--print", "`"ciclo de sono global`"" -WindowStyle Hidden
        Write-Log "Consolidacao disparada via claude --print"
    }
}
