@echo off
REM ============================================================
REM Colmeia v6 — Standup Diario
REM Uso: executar manualmente ou via Task Scheduler (23:30)
REM Compila atividades do dia e exibe resumo
REM ============================================================

echo.
echo ============================================================
echo   STANDUP DIARIO — Colmeia v6
echo   Data: %date%
echo ============================================================
echo.

cd /d "C:\Users\IgorPC\Colmeia\operacional\banco"
python cli.py standup

echo.
echo ============================================================
echo   Para enviar via Telegram, configure o bot em scripts/
echo ============================================================
