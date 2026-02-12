@echo off
REM Colmeia v6 — Backup do banco SQLite para JSON
REM Uso: executar manualmente ou via Task Scheduler

echo [%date% %time%] Iniciando backup do banco Colmeia v6...
cd /d "C:\Users\IgorPC\Colmeia\operacional\banco"
python cli.py exportar
echo [%date% %time%] Backup concluido.
