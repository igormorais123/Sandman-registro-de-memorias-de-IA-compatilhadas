@echo off
REM ============================================================
REM Sandman - Setup do Sistema de Memoria
REM Execute como Administrador
REM ============================================================

echo.
echo ========================================
echo  Sandman - Setup
echo ========================================
echo.

set "REPO_PATH=C:\Users\IgorPC\clawd"

if not exist "%REPO_PATH%\SOUL.md" (
    echo ERRO: clawd nao encontrado em %REPO_PATH%
    pause
    exit /b 1
)

echo [1/4] Criando arquivos de controle...
echo. > "%REPO_PATH%\.ultima_consolidacao"
echo 0 > "%REPO_PATH%\.contador_sessoes"
echo       OK

echo [2/4] Registrando Sandman no Task Scheduler...
schtasks /create /xml "%REPO_PATH%\scripts\consolidacao-memoria.xml" /tn "SandmanMemoria" /f
if %errorlevel% neq 0 (
    echo       AVISO: Execute como Administrador.
) else (
    echo       OK
)

echo [3/4] Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (echo       AVISO: Git nao encontrado.) else (echo       OK)

echo [4/4] Verificando Claude CLI...
claude --version >nul 2>&1
if %errorlevel% neq 0 (echo       AVISO: Claude CLI nao encontrado.) else (echo       OK)

echo.
echo ========================================
echo  Sandman ativo!
echo ========================================
echo  Sonhos automaticos ao ligar o PC.
echo  Manual: claude (em %REPO_PATH%) + "ciclo de sono"
echo.
pause
