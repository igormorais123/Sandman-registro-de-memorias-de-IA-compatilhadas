@echo off
REM ============================================================
REM Setup do Sistema de Memoria Multi-IA
REM Execute como Administrador para registrar Task Scheduler
REM ============================================================

echo.
echo ========================================
echo  Setup - Sistema de Memoria Multi-IA
echo ========================================
echo.

set "REPO_PATH=C:\Users\IgorPC\Desktop\memoria-ia-unificada"

REM Verifica se esta no diretorio correto
if not exist "%REPO_PATH%\scripts\consolidacao-memoria.xml" (
    echo ERRO: Execute este script de dentro do repositorio
    echo Caminho esperado: %REPO_PATH%
    pause
    exit /b 1
)

echo [1/4] Criando arquivos de controle...
echo. > "%REPO_PATH%\.ultima_consolidacao"
echo 0 > "%REPO_PATH%\.contador_sessoes"
echo       OK

echo [2/4] Registrando tarefa no Task Scheduler...
schtasks /create /xml "%REPO_PATH%\scripts\consolidacao-memoria.xml" /tn "ConsolidacaoMemoriaIA" /f
if %errorlevel% neq 0 (
    echo       AVISO: Falha ao registrar tarefa. Execute como Administrador.
) else (
    echo       OK
)

echo [3/4] Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo       AVISO: Git nao encontrado. Instale Git para versionamento.
) else (
    echo       OK
)

echo [4/4] Verificando Claude CLI...
claude --version >nul 2>&1
if %errorlevel% neq 0 (
    echo       AVISO: Claude CLI nao encontrado. Instale para consolidacao.
) else (
    echo       OK
)

echo.
echo ========================================
echo  Setup Concluido!
echo ========================================
echo.
echo Proximos passos:
echo.
echo 1. Criar repositorio no GitHub:
echo    gh repo create memoria-ia-unificada --private
echo.
echo 2. Inicializar e fazer push:
echo    cd %REPO_PATH%
echo    git init
echo    git add -A
echo    git commit -m "Setup inicial do sistema de memoria"
echo    git remote add origin https://github.com/[seu-usuario]/memoria-ia-unificada.git
echo    git push -u origin main
echo.
echo 3. Configurar Zapier (opcional - para ChatGPT):
echo    - Acesse zapier.com
echo    - Crie Zap: ChatGPT Tasks -^> Google Drive -^> INGEST/chatgpt/
echo.
echo 4. Configurar Custom Instructions no ChatGPT:
echo    "Consulte github.com/[usuario]/memoria-ia-unificada"
echo.
pause
