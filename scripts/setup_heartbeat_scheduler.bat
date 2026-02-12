@echo off
REM Colmeia v6 — Setup de Heartbeats Agendados (Windows Task Scheduler)
REM Executa: heartbeat_runner.py a cada 30 minutos para cada agente piloto
REM Uso: Executar como Administrador

echo.
echo   === Colmeia v6 — Configuracao de Heartbeats ===
echo.

set PYTHON=C:\Python314\python.exe
set RUNNER=C:\Users\IgorPC\Colmeia\operacional\banco\heartbeat_runner.py
set DAEMON=C:\Users\IgorPC\Colmeia\operacional\banco\notificacao_daemon.py
set LOGDIR=C:\Users\IgorPC\Colmeia\operacional\logs

REM Criar diretorio de logs se nao existir
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

REM Remover tarefas antigas (se existirem)
schtasks /delete /tn "Colmeia_HB_NEXO" /f >nul 2>&1
schtasks /delete /tn "Colmeia_HB_ONIR" /f >nul 2>&1
schtasks /delete /tn "Colmeia_HB_SANDMAN" /f >nul 2>&1
schtasks /delete /tn "Colmeia_HB_HELENA" /f >nul 2>&1
schtasks /delete /tn "Colmeia_Notificacao_Daemon" /f >nul 2>&1

echo   Criando heartbeat NEXO (a cada 30 min, offset :00)...
schtasks /create /tn "Colmeia_HB_NEXO" /tr "%PYTHON% %RUNNER% nexo" /sc minute /mo 30 /st 00:00 /f
if %errorlevel% neq 0 echo   ERRO ao criar tarefa NEXO

echo   Criando heartbeat ONIR (a cada 30 min, offset :02)...
schtasks /create /tn "Colmeia_HB_ONIR" /tr "%PYTHON% %RUNNER% onir" /sc minute /mo 30 /st 00:02 /f
if %errorlevel% neq 0 echo   ERRO ao criar tarefa ONIR

echo   Criando heartbeat SANDMAN (a cada 30 min, offset :04)...
schtasks /create /tn "Colmeia_HB_SANDMAN" /tr "%PYTHON% %RUNNER% sandman" /sc minute /mo 30 /st 00:04 /f
if %errorlevel% neq 0 echo   ERRO ao criar tarefa SANDMAN

echo   Criando heartbeat HELENA (a cada 30 min, offset :06)...
schtasks /create /tn "Colmeia_HB_HELENA" /tr "%PYTHON% %RUNNER% helena" /sc minute /mo 30 /st 00:06 /f
if %errorlevel% neq 0 echo   ERRO ao criar tarefa HELENA

echo   Criando daemon de notificacoes (a cada 5 min)...
schtasks /create /tn "Colmeia_Notificacao_Daemon" /tr "%PYTHON% %DAEMON% --once --modo online --limite 100 --retry-delay-min 30 --online-janela-min 90" /sc minute /mo 5 /st 00:01 /f
if %errorlevel% neq 0 echo   ERRO ao criar daemon de notificacoes

echo.
echo   Verificando tarefas criadas:
echo.
schtasks /query /tn "Colmeia_HB_NEXO" /fo list 2>nul | findstr "TaskName Status"
schtasks /query /tn "Colmeia_HB_ONIR" /fo list 2>nul | findstr "TaskName Status"
schtasks /query /tn "Colmeia_HB_SANDMAN" /fo list 2>nul | findstr "TaskName Status"
schtasks /query /tn "Colmeia_HB_HELENA" /fo list 2>nul | findstr "TaskName Status"
schtasks /query /tn "Colmeia_Notificacao_Daemon" /fo list 2>nul | findstr "TaskName Status"

echo.
echo   === Configuracao concluida ===
echo   Heartbeats executarao a cada 30 minutos e o daemon a cada 5 minutos.
echo   Para desativar: schtasks /delete /tn "Colmeia_HB_*" /f
echo   Logs em: %LOGDIR%\heartbeat_*.jsonl
echo.
