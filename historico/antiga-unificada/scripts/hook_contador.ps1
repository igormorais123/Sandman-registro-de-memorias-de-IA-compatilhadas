# ============================================================
# Hook Contador de Sessoes - Claude Code
# Dispara consolidacao a cada N sessoes
# ============================================================

$ErrorActionPreference = "SilentlyContinue"

# Configuracoes
$repoPath = "C:\Users\IgorPC\Desktop\memoria-ia-unificada"
$contadorPath = Join-Path $repoPath ".contador_sessoes"
$logPath = Join-Path $repoPath "logs"
$sessoesParaConsolidar = 10

# Cria pasta de logs se nao existir
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}

$logFile = Join-Path $logPath "hook_$(Get-Date -Format 'yyyyMMdd').log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$timestamp] $Message"
}

# Le contador atual
$contador = 0
if (Test-Path $contadorPath) {
    $conteudo = Get-Content $contadorPath -ErrorAction SilentlyContinue
    if ($conteudo) {
        $contador = [int]$conteudo
    }
}

# Incrementa contador
$contador++
Set-Content -Path $contadorPath -Value $contador

Write-Log "Sessao #$contador registrada"

# Verifica se deve consolidar
if ($contador -ge $sessoesParaConsolidar) {
    Write-Log "Atingiu $sessoesParaConsolidar sessoes - iniciando consolidacao"

    # Reseta contador
    Set-Content -Path $contadorPath -Value 0

    # Dispara consolidacao em background
    $consolidarScript = Join-Path $repoPath "scripts\consolidar.bat"

    if (Test-Path $consolidarScript) {
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $consolidarScript -WindowStyle Hidden
        Write-Log "Consolidacao disparada em background"
    } else {
        Write-Log "ERRO: Script de consolidacao nao encontrado: $consolidarScript"
    }
} else {
    $restantes = $sessoesParaConsolidar - $contador
    Write-Log "Faltam $restantes sessoes para proxima consolidacao"
}
