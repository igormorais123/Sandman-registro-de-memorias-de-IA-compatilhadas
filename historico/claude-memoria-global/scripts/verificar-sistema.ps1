# =============================================================================
# Script de Verificacao do Sistema de Memoria - Claude Code (Windows PowerShell)
# =============================================================================
# Uso: .\verificar-sistema.ps1
# Verifica se toda a estrutura do sistema de memoria esta correta
# =============================================================================

$GLOBAL_DIR = "$HOME\.claude-memoria-global"
$erros = 0
$avisos = 0

# Cores para output
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Erro { param($msg) Write-Host "[ERRO] $msg" -ForegroundColor Red; $script:erros++ }
function Write-Aviso { param($msg) Write-Host "[AVISO] $msg" -ForegroundColor Yellow; $script:avisos++ }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  Verificacao do Sistema de Memoria        " -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# 1. Verificar diretorio global
Write-Info "Verificando estrutura global..."

if (Test-Path $GLOBAL_DIR) {
    Write-Success "Diretorio global existe: $GLOBAL_DIR"
} else {
    Write-Erro "Diretorio global NAO existe: $GLOBAL_DIR"
    Write-Host ""
    Write-Host "O sistema de memoria nao esta instalado." -ForegroundColor Red
    exit 1
}

# 2. Verificar arquivos essenciais
$arquivosEssenciais = @(
    "CLAUDE.md",
    "INDICE_GLOBAL.md",
    "CONHECIMENTO_UNIVERSAL.md",
    "CATALOGO_PROJETOS.md",
    "PADROES_CODIGO.md",
    "ANTIPADROES_GLOBAIS.md",
    "PROMPTS_EFETIVOS.md",
    "FERRAMENTAS_RECOMENDADAS.md",
    "META_APRENDIZADO.md",
    "PROTOCOLO_SONO_GLOBAL.md",
    "GUIA_CONSULTA.md"
)

Write-Host ""
Write-Info "Verificando arquivos essenciais..."

foreach ($arquivo in $arquivosEssenciais) {
    $caminho = Join-Path $GLOBAL_DIR $arquivo
    if (Test-Path $caminho) {
        $tamanho = (Get-Item $caminho).Length
        if ($tamanho -gt 100) {
            Write-Success "$arquivo ($tamanho bytes)"
        } else {
            Write-Aviso "$arquivo existe mas parece vazio ($tamanho bytes)"
        }
    } else {
        Write-Erro "$arquivo NAO encontrado"
    }
}

# 3. Verificar diretorios
Write-Host ""
Write-Info "Verificando diretorios..."

$diretorios = @(
    "projetos",
    "consolidado",
    "meta",
    "scripts",
    "temp",
    "template-projeto"
)

foreach ($dir in $diretorios) {
    $caminho = Join-Path $GLOBAL_DIR $dir
    if (Test-Path $caminho) {
        Write-Success "Diretorio: $dir"
    } else {
        Write-Aviso "Diretorio ausente: $dir"
    }
}

# 4. Verificar template de projeto
Write-Host ""
Write-Info "Verificando template de projeto..."

$templateDir = Join-Path $GLOBAL_DIR "template-projeto"
$templateArquivos = @(
    ".memoria\MEMORIA_LONGO_PRAZO.md",
    ".memoria\CONTEXTO_ATIVO.md",
    ".memoria\APRENDIZADOS.md",
    ".memoria\SYNC_GLOBAL.md",
    ".memoria\PROTOCOLO_SONO.md",
    "CLAUDE.md"
)

foreach ($arquivo in $templateArquivos) {
    $caminho = Join-Path $templateDir $arquivo
    if (Test-Path $caminho) {
        Write-Success "Template: $arquivo"
    } else {
        Write-Erro "Template ausente: $arquivo"
    }
}

# 5. Verificar scripts
Write-Host ""
Write-Info "Verificando scripts..."

$scriptsDir = Join-Path $GLOBAL_DIR "scripts"
$scripts = @(
    "sync.sh",
    "check-memory.sh",
    "inicializar-projeto.ps1",
    "verificar-sistema.ps1"
)

foreach ($script in $scripts) {
    $caminho = Join-Path $scriptsDir $script
    if (Test-Path $caminho) {
        Write-Success "Script: $script"
    } else {
        Write-Aviso "Script ausente: $script"
    }
}

# 6. Verificar CLAUDE.md na home
Write-Host ""
Write-Info "Verificando ativacao do sistema..."

$claudeHome = Join-Path $HOME "CLAUDE.md"
if (Test-Path $claudeHome) {
    Write-Success "CLAUDE.md na home existe (sistema ativado)"
} else {
    Write-Aviso "CLAUDE.md na home NAO existe (sistema pode nao ativar automaticamente)"
}

# 7. Verificar projetos registrados
Write-Host ""
Write-Info "Verificando projetos registrados..."

$catalogoFile = Join-Path $GLOBAL_DIR "CATALOGO_PROJETOS.md"
if (Test-Path $catalogoFile) {
    $conteudo = Get-Content $catalogoFile -Raw
    $matches = [regex]::Matches($conteudo, 'projeto_id:\s*(\S+)')
    $numProjetos = $matches.Count

    if ($numProjetos -gt 0) {
        Write-Success "$numProjetos projeto(s) registrado(s)"
        foreach ($match in $matches) {
            Write-Host "       - $($match.Groups[1].Value)" -ForegroundColor Gray
        }
    } else {
        Write-Info "Nenhum projeto registrado ainda"
    }
}

# 8. Sumario
Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  Sumario da Verificacao                   " -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

if ($erros -eq 0 -and $avisos -eq 0) {
    Write-Host "Sistema de memoria TOTALMENTE operacional!" -ForegroundColor Green
} elseif ($erros -eq 0) {
    Write-Host "Sistema operacional com $avisos aviso(s)" -ForegroundColor Yellow
} else {
    Write-Host "Sistema com problemas: $erros erro(s), $avisos aviso(s)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Erros: $erros" -ForegroundColor $(if ($erros -eq 0) { "Green" } else { "Red" })
Write-Host "Avisos: $avisos" -ForegroundColor $(if ($avisos -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

# Retornar codigo de erro se houver erros
if ($erros -gt 0) {
    exit 1
}
exit 0
