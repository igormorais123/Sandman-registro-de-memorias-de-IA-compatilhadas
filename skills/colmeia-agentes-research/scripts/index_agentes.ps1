param(
  [string]$Root = "C:\Agentes",
  [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Root)) {
  Write-Error "Diretorio nao encontrado: $Root"
}

$items = Get-ChildItem -Path $Root -Recurse -Force -ErrorAction SilentlyContinue
$files = $items | Where-Object { -not $_.PSIsContainer }
$dirs = $items | Where-Object { $_.PSIsContainer }

$byExt = $files |
  Group-Object { if ($_.Extension) { $_.Extension.ToLower() } else { "(sem-ext)" } } |
  Sort-Object Count -Descending

$lines = @()
$lines += "# Inventario C:/Agentes"
$lines += ""
$lines += "Root: $Root"
$lines += "Pastas: $($dirs.Count)"
$lines += "Arquivos: $($files.Count)"
$lines += ""
$lines += "## Arquivos por extensao"
$lines += ""
foreach ($g in $byExt) {
  $lines += "- $($g.Name): $($g.Count)"
}
$lines += ""
$lines += "## Primeiras 200 rotas de arquivo"
$lines += ""
$files | Select-Object -First 200 | ForEach-Object {
  $rel = $_.FullName.Replace('\','/')
  $lines += '- `' + $rel + '`'
}

$content = $lines -join "`r`n"

if ($OutFile) {
  Set-Content -Path $OutFile -Value $content -Encoding UTF8
  Write-Output "Inventario salvo em: $OutFile"
} else {
  Write-Output $content
}
