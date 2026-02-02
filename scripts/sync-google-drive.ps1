# ============================================
# sync-google-drive.ps1 - Sincronização com Google Drive
# Copia memória local para Google Drive quando disponível
# ============================================

param(
    [string]$DriveLetters = "G,H,I",
    [switch]$Force
)

$memoriaLocal = "C:\Users\IgorPC\.claude-memoria-global"
$pastaDrive = "memoria-ia-unificada"
$logPath = "$memoriaLocal\logs\sync-drive.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $logPath -Append
    Write-Host "$timestamp - $Message"
}

# Procurar Google Drive
$driveFound = $null
foreach ($letter in $DriveLetters.Split(",")) {
    $testPath = "${letter}:\Meu Drive"
    if (Test-Path $testPath) {
        $driveFound = $testPath
        break
    }
    $testPath = "${letter}:\My Drive"
    if (Test-Path $testPath) {
        $driveFound = $testPath
        break
    }
}

if (-not $driveFound) {
    Write-Log "ERRO: Google Drive nao encontrado em $DriveLetters"
    Write-Log "Verifique se Google Drive esta instalado e logado"
    exit 1
}

Write-Log "Google Drive encontrado em: $driveFound"

$destino = "$driveFound\$pastaDrive"

# Criar pasta se não existir
if (-not (Test-Path $destino)) {
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
    Write-Log "Pasta criada: $destino"
}

# Arquivos/pastas para sincronizar
$itens = @(
    "CORE",
    "INDICE_GLOBAL.md",
    "CONHECIMENTO_UNIVERSAL.md",
    "CATALOGO_PROJETOS.md",
    "ANTIPADROES_GLOBAIS.md",
    "PADROES_CODIGO.md",
    "PROMPTS_EFETIVOS.md",
    "PROMPTS_OUTRAS_IAS.md",
    "DECISOES_ARQUITETURAIS.md",
    "FERRAMENTAS_RECOMENDADAS.md",
    "META_APRENDIZADO.md",
    "consolidado",
    "meta"
)

foreach ($item in $itens) {
    $origem = "$memoriaLocal\$item"
    $destinoItem = "$destino\$item"

    if (Test-Path $origem) {
        if (Test-Path $origem -PathType Container) {
            # É pasta - copiar recursivamente
            Copy-Item -Path $origem -Destination $destino -Recurse -Force
            Write-Log "Pasta sincronizada: $item"
        } else {
            # É arquivo
            Copy-Item -Path $origem -Destination $destinoItem -Force
            Write-Log "Arquivo sincronizado: $item"
        }
    } else {
        Write-Log "AVISO: Item nao encontrado: $item"
    }
}

Write-Log "Sincronizacao concluida!"
Write-Log "Destino: $destino"

# Listar conteúdo final
Write-Log "Conteudo sincronizado:"
Get-ChildItem $destino | ForEach-Object { Write-Log "  - $($_.Name)" }
