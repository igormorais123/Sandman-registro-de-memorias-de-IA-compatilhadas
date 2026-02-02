@echo off
REM ============================================
REM consolidar.bat - Script de Consolidação Automática
REM Sistema de Memória Hierárquica Claude Code
REM ============================================

setlocal enabledelayedexpansion

set "MEMORIA_DIR=C:\Users\IgorPC\.claude-memoria-global"
set "LOG_DIR=%MEMORIA_DIR%\logs"
set "TIMESTAMP_FILE=%MEMORIA_DIR%\.ultima_consolidacao"

REM Criar pasta de logs se não existir
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Gerar nome do log com data
for /f "tokens=1-3 delims=/" %%a in ('date /t') do set "DATA=%%c-%%b-%%a"
for /f "tokens=1-2 delims=:" %%a in ('time /t') do set "HORA=%%a-%%b"
set "LOG_FILE=%LOG_DIR%\consolidacao_%DATA%_%HORA%.log"

echo [%date% %time%] Iniciando verificacao de consolidacao... >> "%LOG_FILE%"

REM Verificar última consolidação
if exist "%TIMESTAMP_FILE%" (
    for /f %%i in ('powershell -NoProfile -Command "(Get-Date) - (Get-Item '%TIMESTAMP_FILE%').LastWriteTime | Select-Object -ExpandProperty TotalHours"') do set "HORAS=%%i"

    REM Converter para inteiro (remover decimais)
    for /f "tokens=1 delims=." %%a in ("!HORAS!") do set "HORAS_INT=%%a"

    echo [%date% %time%] Ultima consolidacao ha !HORAS_INT! horas >> "%LOG_FILE%"

    if !HORAS_INT! LSS 24 (
        echo [%date% %time%] Menos de 24h desde ultima consolidacao. Pulando. >> "%LOG_FILE%"
        goto :EOF
    )
) else (
    echo [%date% %time%] Primeira execucao - arquivo de timestamp nao existe >> "%LOG_FILE%"
)

echo [%date% %time%] Iniciando ciclo de sono... >> "%LOG_FILE%"

REM Executar Claude Code com ciclo de sono
cd /d "%MEMORIA_DIR%"
claude --print "ciclo de sono global" >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Ciclo de sono concluido com sucesso >> "%LOG_FILE%"
    echo. > "%TIMESTAMP_FILE%"
) else (
    echo [%date% %time%] ERRO: Ciclo de sono falhou com codigo %ERRORLEVEL% >> "%LOG_FILE%"
)

echo [%date% %time%] Consolidacao finalizada >> "%LOG_FILE%"

endlocal
