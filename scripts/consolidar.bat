@echo off
REM ============================================================
REM Sandman - Script de Consolidacao de Memoria
REM Executa ao ligar o PC via Task Scheduler
REM Repo unico: clawd (identidade + memoria + sonhos)
REM ============================================================

setlocal enabledelayedexpansion

REM Configuracoes
set "REPO_PATH=C:\Users\igorm\clawd"
set "LOG_PATH=%REPO_PATH%\logs"
set "ULTIMA_CONSOLIDACAO=%REPO_PATH%\.ultima_consolidacao"
set "HORAS_MINIMAS=24"

REM Cria pasta de logs se nao existir
if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

REM Nome do arquivo de log com data
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "LOG_FILE=%LOG_PATH%\consolidacao_%datetime:~0,8%_%datetime:~8,4%.log"

echo [%date% %time%] Sandman: Iniciando verificacao... >> "%LOG_FILE%"

REM Navega para o diretorio do repositorio
cd /d "%REPO_PATH%"

REM Verifica se arquivo de ultima consolidacao existe
if not exist "%ULTIMA_CONSOLIDACAO%" (
    echo [%date% %time%] Primeira execucao - criando marcador >> "%LOG_FILE%"
    echo. > "%ULTIMA_CONSOLIDACAO%"
    goto :consolidar
)

REM Calcula horas desde ultima consolidacao
for /f %%i in ('powershell -NoProfile -Command "(New-TimeSpan -Start (Get-Item '%ULTIMA_CONSOLIDACAO%').LastWriteTime -End (Get-Date)).TotalHours"') do set "HORAS=%%i"

REM Remove decimais
for /f "tokens=1 delims=." %%a in ("%HORAS%") do set "HORAS_INT=%%a"

echo [%date% %time%] Horas desde ultima consolidacao: %HORAS_INT% >> "%LOG_FILE%"

if %HORAS_INT% GEQ %HORAS_MINIMAS% (
    goto :consolidar
) else (
    echo [%date% %time%] Menos de %HORAS_MINIMAS%h. Pulando. >> "%LOG_FILE%"
    goto :fim
)

:consolidar
echo [%date% %time%] Sandman: Iniciando ciclo de sono... >> "%LOG_FILE%"

REM Puxa ultimas mudancas do GitHub
git pull origin master >> "%LOG_FILE%" 2>&1

REM Verifica se ha arquivos em ingest/ para processar
set "INGEST_COUNT=0"
for /f %%A in ('dir /b /a-d "%REPO_PATH%\ingest\chatgpt" 2^>nul ^| find /c /v ""') do set "INGEST_COUNT=%%A"

echo [%date% %time%] Arquivos em ingest/chatgpt: %INGEST_COUNT% >> "%LOG_FILE%"

REM Executa Claude Code para ciclo de sono
echo [%date% %time%] Chamando Claude para ciclo de sono... >> "%LOG_FILE%"

echo Ciclo de sono Sandman: 1) Leia Knowledge Graph e execute selecao natural (decair -1, podar F:0, graduar F:10) 2) Verifique ingest/ por novos arquivos 3) Atualize CONTEXTO_ATIVO.md 4) Registre sonho em memoria/sonhos/ 5) Faca commit e push | claude -p >> "%LOG_FILE%" 2>&1

REM Atualiza marcador de ultima consolidacao
echo. > "%ULTIMA_CONSOLIDACAO%"
echo [%date% %time%] Sandman: Ciclo concluido >> "%LOG_FILE%"

REM Commit e push das mudancas
git add -A >> "%LOG_FILE%" 2>&1
git commit -m "sonho: consolidacao automatica %datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%" >> "%LOG_FILE%" 2>&1
git push origin master >> "%LOG_FILE%" 2>&1

:fim
echo [%date% %time%] Sandman: Script finalizado >> "%LOG_FILE%"
endlocal
