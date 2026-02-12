# ============================================================
# Sandman - Hook Contador de Sessoes
# Dispara consolidacao a cada N sessoes
# ============================================================

$ErrorActionPreference = "SilentlyContinue"

$repoPath = "C:\Users\IgorPC\clawd"
$contadorPath = Join-Path $repoPath ".contador_sessoes"
$logPath = Join-Path $repoPath "logs"
$sessoesParaConsolidar = 10

if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}

$logFile = Join-Path $logPath "hook_$(Get-Date -Format 'yyyyMMdd').log"

function Write-Log {
    param([string]$Message)
    Add-Content -Path $logFile -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
}

$contador = 0
if (Test-Path $contadorPath) {
    $conteudo = Get-Content $contadorPath -ErrorAction SilentlyContinue
    if ($conteudo) { $contador = [int]$conteudo }
}

$contador++
Set-Content -Path $contadorPath -Value $contador
Write-Log "Sandman: Sessao #$contador"

if ($contador -ge $sessoesParaConsolidar) {
    Write-Log "Sandman: $sessoesParaConsolidar sessoes - disparando sonho"
    Set-Content -Path $contadorPath -Value 0
    $script = Join-Path $repoPath "scripts\consolidar.bat"
    if (Test-Path $script) {
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $script -WindowStyle Hidden
        Write-Log "Sandman: Sonho disparado"
    } else {
        Write-Log "Sandman: ERRO: $script nao encontrado"
    }
} else {
    Write-Log "Sandman: Faltam $($sessoesParaConsolidar - $contador) para proximo sonho"
}
