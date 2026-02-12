@echo off
REM Agenda lembrete para fechamento P032/P033/P034
REM Data alvo: 18/02/2026 09:20 (com repeticao diaria)

set PYTHON=C:\Python314\python.exe
set FECHAMENTO=C:\Users\IgorPC\Colmeia\scripts\fechamento_p032_p034.py

schtasks /delete /tn "Colmeia_Lembrete_Fechamento_P032" /f >nul 2>&1

schtasks /create ^
 /tn "Colmeia_Lembrete_Fechamento_P032" ^
 /tr "%PYTHON% %FECHAMENTO%" ^
 /sc daily ^
 /sd 18/02/2026 ^
 /st 09:20 ^
 /f

if %errorlevel% neq 0 (
  echo ERRO ao criar lembrete de fechamento.
  exit /b 1
)

echo Lembrete criado: Colmeia_Lembrete_Fechamento_P032
schtasks /query /tn "Colmeia_Lembrete_Fechamento_P032" /fo list
