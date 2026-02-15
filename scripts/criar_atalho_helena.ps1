$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Helena Colmeia.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"C:\Users\IgorPC\Colmeia\scripts\abrir_helena.ps1`""
$Shortcut.WorkingDirectory = "C:\Users\IgorPC\Colmeia"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,44"
$Shortcut.Save()
Write-Host "Atalho criado: Desktop\Helena Colmeia.lnk"
