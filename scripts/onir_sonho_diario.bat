@echo off
REM ============================================
REM ONIR - Sonho Diario Automatico
REM Roda via Task Scheduler todo dia as 21:00
REM ============================================

set REPO=C:\Users\IgorPC\GitHub\Sandman-registro-de-memorias-de-IA-compatilhadas
set PROMPT_FILE=%REPO%\scripts\onir_sonho_diario_prompt.md
set LOG_FILE=%REPO%\scripts\logs\onir_sonho_%date:~-4%%date:~3,2%%date:~0,2%.log

REM Criar pasta de logs se nao existir
if not exist "%REPO%\scripts\logs" mkdir "%REPO%\scripts\logs"

echo [%date% %time%] Iniciando sonho diario ONIR >> "%LOG_FILE%"

REM Ler o prompt do arquivo
set /p PROMPT=<nul
for /f "usebackq delims=" %%i in ("%PROMPT_FILE%") do set "PROMPT=%%i"

REM Executar Claude Code em modo nao-interativo
echo [%date% %time%] Invocando Claude Code... >> "%LOG_FILE%"

cd /d "%REPO%"

"C:\Users\IgorPC\.local\bin\claude.exe" -p "Leia o arquivo scripts/onir_sonho_diario_prompt.md e execute todas as instrucoes contidas nele. Siga o protocolo completo sem pular nenhum passo." --permission-mode bypassPermissions --max-budget-usd 2.00 --model opus >> "%LOG_FILE%" 2>&1

echo [%date% %time%] Sonho diario concluido >> "%LOG_FILE%"
