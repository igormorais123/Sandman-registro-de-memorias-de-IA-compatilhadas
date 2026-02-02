@echo off
schtasks /create /tn "ConsolidacaoMemoriaClaudeCode" /xml "C:\Users\IgorPC\.claude-memoria-global\scripts\consolidacao-memoria.xml" /f
if %ERRORLEVEL% EQU 0 (
    echo Tarefa agendada criada com sucesso!
) else (
    echo ERRO ao criar tarefa. Codigo: %ERRORLEVEL%
    echo Tente executar como Administrador.
)
pause
