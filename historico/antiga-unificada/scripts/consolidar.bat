@echo off
REM ============================================================
REM Script de Consolidacao de Memoria Multi-IA
REM Executa ao ligar o PC via Task Scheduler
REM ============================================================

setlocal enabledelayedexpansion

REM Configuracoes
set "REPO_PATH=C:\Users\IgorPC\Desktop\memoria-ia-unificada"
set "LOG_PATH=%REPO_PATH%\logs"
set "ULTIMA_CONSOLIDACAO=%REPO_PATH%\.ultima_consolidacao"
set "HORAS_MINIMAS=24"

REM Cria pasta de logs se nao existir
if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

REM Nome do arquivo de log com data
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "LOG_FILE=%LOG_PATH%\consolidacao_%datetime:~0,8%_%datetime:~8,4%.log"

echo [%date% %time%] Iniciando verificacao de consolidacao... >> "%LOG_FILE%"

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
    echo [%date% %time%] Menos de %HORAS_MINIMAS%h desde ultima consolidacao. Pulando. >> "%LOG_FILE%"
    goto :fim
)

:consolidar
echo [%date% %time%] Iniciando consolidacao... >> "%LOG_FILE%"

REM Puxa ultimas mudancas do GitHub (se repo ja existe)
git pull origin main >> "%LOG_FILE%" 2>&1

REM Verifica se ha arquivos em INGEST/ para processar
set "INGEST_COUNT=0"
for /f %%A in ('dir /b /a-d "%REPO_PATH%\INGEST\chatgpt" 2^>nul ^| find /c /v ""') do set "INGEST_COUNT=%%A"

echo [%date% %time%] Arquivos em INGEST/chatgpt: %INGEST_COUNT% >> "%LOG_FILE%"

REM Executa Claude Code para consolidacao
echo [%date% %time%] Chamando Claude Code para consolidacao... >> "%LOG_FILE%"

REM Cria arquivo de sessao do dia
set "SESSAO_FILE=%REPO_PATH%\SESSOES\%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_consolidacao.md"

REM Comando de consolidacao para Claude
claude --print "Execute o ciclo de consolidacao de memoria: 1) Verifique INGEST/ por novos arquivos e processe-os 2) Atualize CORE/CONTEXTO_ATIVO.md com estado atual 3) Consolide aprendizados em CONHECIMENTO/ se houver 4) Crie registro em SESSOES/ com data de hoje 5) Faca commit e push das mudancas" >> "%LOG_FILE%" 2>&1

REM Atualiza marcador de ultima consolidacao
echo. > "%ULTIMA_CONSOLIDACAO%"
echo [%date% %time%] Consolidacao concluida >> "%LOG_FILE%"

REM Commit e push das mudancas
git add -A >> "%LOG_FILE%" 2>&1
git commit -m "Consolidacao automatica %datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%" >> "%LOG_FILE%" 2>&1
git push origin main >> "%LOG_FILE%" 2>&1

:fim
echo [%date% %time%] Script finalizado >> "%LOG_FILE%"
endlocal
