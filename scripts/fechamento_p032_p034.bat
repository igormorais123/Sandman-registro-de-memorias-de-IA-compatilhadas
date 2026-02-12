@echo off
cd /d "C:\Users\IgorPC\Colmeia"
C:\Python314\python.exe scripts\fechamento_p032_p034.py
if %errorlevel% neq 0 (
  echo.
  echo Fechamento com erro. Verifique o arquivo gerado em operacional\FECHAMENTO_P032_P034_*.md
  exit /b 1
)
echo.
echo Fechamento executado com sucesso.
