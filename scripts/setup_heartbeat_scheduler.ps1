$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Colmeia v6 - Setup Scheduler (PowerShell) ==="
Write-Host ""

$python = "C:\Python314\python.exe"
$runner = "C:\Users\IgorPC\Colmeia\operacional\banco\heartbeat_runner.py"
$daemon = "C:\Users\IgorPC\Colmeia\operacional\banco\notificacao_daemon.py"
$workdir = "C:\Users\IgorPC\Colmeia"

if (-not (Test-Path $python)) {
  throw "Python nao encontrado em $python"
}

function New-ColmeiaTask {
  param(
    [string]$Name,
    [string]$Arguments,
    [datetime]$At,
    [int]$MinutesInterval
  )

  $action = New-ScheduledTaskAction -Execute $python -Argument $Arguments -WorkingDirectory $workdir
  $trigger = New-ScheduledTaskTrigger -Once -At $At -RepetitionInterval (New-TimeSpan -Minutes $MinutesInterval) -RepetitionDuration (New-TimeSpan -Days 9999)
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

  if (Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $Name -Confirm:$false
  }

  Register-ScheduledTask -TaskName $Name -Action $action -Trigger $trigger -Settings $settings -Description "Colmeia v6"
}

$today = Get-Date
New-ColmeiaTask -Name "Colmeia_HB_NEXO" -Arguments "`"$runner`" nexo" -At ($today.Date.AddMinutes(0)) -MinutesInterval 30
New-ColmeiaTask -Name "Colmeia_HB_ONIR" -Arguments "`"$runner`" onir" -At ($today.Date.AddMinutes(2)) -MinutesInterval 30
New-ColmeiaTask -Name "Colmeia_HB_SANDMAN" -Arguments "`"$runner`" sandman" -At ($today.Date.AddMinutes(4)) -MinutesInterval 30
New-ColmeiaTask -Name "Colmeia_HB_HELENA" -Arguments "`"$runner`" helena" -At ($today.Date.AddMinutes(6)) -MinutesInterval 30
New-ColmeiaTask -Name "Colmeia_Notificacao_Daemon" -Arguments "`"$daemon`" --once --modo online --limite 100 --retry-delay-min 30 --online-janela-min 90" -At ($today.Date.AddMinutes(1)) -MinutesInterval 5

Write-Host ""
Write-Host "Tarefas criadas/atualizadas:"
Get-ScheduledTask -TaskName "Colmeia_*" | Select-Object TaskName, State | Format-Table -AutoSize
Write-Host ""
Write-Host "Concluido."
