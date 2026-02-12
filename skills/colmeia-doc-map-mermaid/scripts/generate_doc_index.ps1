$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path ".").Path
$out = Join-Path $repoRoot "docs/INDICE_DOCUMENTOS_COMPLETO.md"

$files = rg --files | rg '\.(md|txt)$' | Sort-Object
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$lines = @()
$lines += "# Indice Completo de Documentos"
$lines += ""
$lines += "Gerado em: $date"
$lines += ""
$lines += "Total de arquivos: $($files.Count)"
$lines += ""
$lines += "## Lista completa"
$lines += ""

foreach ($f in $files) {
  $lines += '- `' + ($f.Replace('\','/')) + '`'
}

Set-Content -Path $out -Value ($lines -join "`r`n") -Encoding UTF8
Write-Output "Indice atualizado em: $out"
