$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Colmeia v6 - Setup Scheduler (PowerShell) ==="
Write-Host ""

$python = "C:\Python314\python.exe"
$runner = "C:\Users\IgorPC\Colmeia\operacional\banco\heartbeat_runner.py"
$daemon = "C:\Users\IgorPC\Colmeia\operacional\banco\notificacao_daemon.py"

if (-not (Test-Path $python)) {
  throw "Python nao encontrado em $python"
}

$commands = @(
  "schtasks /create /tn `"Colmeia_HB_NEXO`" /tr `"$python $runner nexo`" /sc minute /mo 30 /st 00:00 /f",
  "schtasks /create /tn `"Colmeia_HB_ONIR`" /tr `"$python $runner onir`" /sc minute /mo 30 /st 00:02 /f",
  "schtasks /create /tn `"Colmeia_HB_SANDMAN`" /tr `"$python $runner sandman`" /sc minute /mo 30 /st 00:04 /f",
  "schtasks /create /tn `"Colmeia_Notificacao_Daemon`" /tr `"$python $daemon --once --modo online --limite 100 --retry-delay-min 30 --online-janela-min 90`" /sc minute /mo 5 /st 00:01 /f"
)

foreach ($cmd in $commands) {
  Write-Host "> $cmd"
  cmd /c $cmd | Out-Host
}

Write-Host ""
Write-Host "Tarefas:"
cmd /c "schtasks /query /tn `"Colmeia_HB_NEXO`" /fo list" | Out-Host
cmd /c "schtasks /query /tn `"Colmeia_HB_ONIR`" /fo list" | Out-Host
cmd /c "schtasks /query /tn `"Colmeia_HB_SANDMAN`" /fo list" | Out-Host
cmd /c "schtasks /query /tn `"Colmeia_Notificacao_Daemon`" /fo list" | Out-Host

Write-Host ""
Write-Host "Concluido."
