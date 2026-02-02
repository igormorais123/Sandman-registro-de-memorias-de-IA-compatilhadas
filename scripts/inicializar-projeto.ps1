# =============================================================================
# Script de Inicialização de Memória - Claude Code (Windows PowerShell)
# =============================================================================
# Uso: .\inicializar-projeto.ps1 [caminho-do-projeto]
# Se não especificar caminho, usa o diretório atual
# =============================================================================

param(
    [string]$ProjetoCaminho = (Get-Location).Path
)

$GLOBAL_DIR = "$HOME\.claude-memoria-global"
$TEMPLATE_DIR = "$GLOBAL_DIR\template-projeto"

# Cores para output
function Write-Success { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host $msg -ForegroundColor Yellow }
function Write-Erro { param($msg) Write-Host $msg -ForegroundColor Red }

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  Sistema de Memoria Hierarquica - Init    " -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# Verificar se o diretório global existe
if (-not (Test-Path $GLOBAL_DIR)) {
    Write-Erro "ERRO: Diretorio de memoria global nao encontrado!"
    Write-Erro "Esperado: $GLOBAL_DIR"
    Write-Host ""
    Write-Info "Execute primeiro a configuracao do sistema global."
    exit 1
}

# Verificar se o template existe
if (-not (Test-Path $TEMPLATE_DIR)) {
    Write-Erro "ERRO: Template de projeto nao encontrado!"
    Write-Erro "Esperado: $TEMPLATE_DIR"
    exit 1
}

# Verificar se o projeto existe
if (-not (Test-Path $ProjetoCaminho)) {
    Write-Erro "ERRO: Caminho do projeto nao existe!"
    Write-Erro "Caminho: $ProjetoCaminho"
    exit 1
}

$MEMORIA_DIR = Join-Path $ProjetoCaminho ".memoria"

Write-Info "Projeto: $ProjetoCaminho"
Write-Info "Memoria: $MEMORIA_DIR"
Write-Host ""

# Verificar se já existe .memoria
if (Test-Path $MEMORIA_DIR) {
    Write-Warning "AVISO: Diretorio .memoria ja existe!"
    $resposta = Read-Host "Deseja sobrescrever? (s/N)"
    if ($resposta -ne "s" -and $resposta -ne "S") {
        Write-Info "Operacao cancelada."
        exit 0
    }
    Remove-Item -Recurse -Force $MEMORIA_DIR
}

# Criar estrutura
Write-Info "Criando estrutura de memoria..."

# Copiar template
Copy-Item -Recurse "$TEMPLATE_DIR\.memoria" $MEMORIA_DIR

# Criar diretório de sessões
$sessoesDir = Join-Path $MEMORIA_DIR "sessoes"
if (-not (Test-Path $sessoesDir)) {
    New-Item -ItemType Directory -Path $sessoesDir | Out-Null
}

# Obter nome do projeto
$nomeProjeto = Split-Path $ProjetoCaminho -Leaf
$dataAtual = Get-Date -Format "yyyy-MM-dd"
$projetoId = $nomeProjeto.ToLower() -replace '\s+', '-'

# Atualizar SYNC_GLOBAL.md com dados do projeto
$syncFile = Join-Path $MEMORIA_DIR "SYNC_GLOBAL.md"
if (Test-Path $syncFile) {
    $conteudo = Get-Content $syncFile -Raw
    $conteudo = $conteudo -replace '\[GERAR_UUID_OU_NOME_UNICO\]', $projetoId
    $conteudo = $conteudo -replace '\[Nome Legivel do Projeto\]', $nomeProjeto
    $conteudo = $conteudo -replace '\[/caminho/absoluto/do/projeto\]', $ProjetoCaminho
    $conteudo = $conteudo -replace 'YYYY-MM-DD', $dataAtual
    Set-Content $syncFile $conteudo
}

# Criar CLAUDE.md local se não existir na raiz do projeto
$claudeMdLocal = Join-Path $ProjetoCaminho "CLAUDE.md"
if (-not (Test-Path $claudeMdLocal)) {
    $claudeTemplate = Join-Path $TEMPLATE_DIR "CLAUDE.md"
    if (Test-Path $claudeTemplate) {
        Copy-Item $claudeTemplate $claudeMdLocal
        # Atualizar com dados do projeto
        $conteudo = Get-Content $claudeMdLocal -Raw
        $conteudo = $conteudo -replace '\[NOME_DO_PROJETO\]', $nomeProjeto
        $conteudo = $conteudo -replace '\[Nome do Projeto\]', $nomeProjeto
        Set-Content $claudeMdLocal $conteudo
    }
}

Write-Success "Estrutura de memoria criada!"
Write-Host ""

# Registrar no catálogo global
Write-Info "Registrando no catalogo global..."

$catalogoFile = Join-Path $GLOBAL_DIR "CATALOGO_PROJETOS.md"
$novaEntrada = @"

### $nomeProjeto
``````yaml
projeto_id: $projetoId
caminho: $ProjetoCaminho
tipo: [definir]
tecnologias: [definir]
dominio: [definir]
data_registro: $dataAtual
ultima_atividade: $dataAtual
status: ativo

especialidades:
  - [a definir]

contribuicoes_globais: []
``````
"@

# Adicionar ao catálogo
Add-Content $catalogoFile $novaEntrada

# Atualizar índice global
$indiceFile = Join-Path $GLOBAL_DIR "INDICE_GLOBAL.md"
if (Test-Path $indiceFile) {
    $conteudo = Get-Content $indiceFile -Raw
    $novaLinha = "| $nomeProjeto | $ProjetoCaminho | $dataAtual | 0 |`n<!-- NOVO_PROJETO_AQUI -->"
    $conteudo = $conteudo -replace '<!-- NOVO_PROJETO_AQUI -->', $novaLinha

    # Atualizar contador de projetos
    if ($conteudo -match '\| Projetos registrados \| (\d+) \|') {
        $atual = [int]$Matches[1]
        $novo = $atual + 1
        $conteudo = $conteudo -replace "\| Projetos registrados \| $atual \|", "| Projetos registrados | $novo |"
    }

    Set-Content $indiceFile $conteudo
}

Write-Success "Projeto registrado no catalogo global!"
Write-Host ""

# Sumário final
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Inicializacao Completa!                  " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Info "Estrutura criada:"
Write-Host "  $MEMORIA_DIR\"
Write-Host "    ├── CONTEXTO_ATIVO.md"
Write-Host "    ├── MEMORIA_LONGO_PRAZO.md"
Write-Host "    ├── APRENDIZADOS.md"
Write-Host "    ├── SYNC_GLOBAL.md"
Write-Host "    ├── PROTOCOLO_SONO.md"
Write-Host "    └── sessoes\"
Write-Host ""
Write-Info "Proximos passos:"
Write-Host "  1. Edite .memoria/SYNC_GLOBAL.md com detalhes do projeto"
Write-Host "  2. Atualize CLAUDE.md com instrucoes especificas"
Write-Host "  3. Comece a trabalhar - a memoria sera preenchida automaticamente"
Write-Host ""
Write-Info "Comandos disponiveis:"
Write-Host '  "carregar contexto"    - Carrega estado do projeto'
Write-Host '  "registrar sessao"     - Salva aprendizados'
Write-Host '  "ciclo de sono"        - Consolida memoria'
Write-Host ""
