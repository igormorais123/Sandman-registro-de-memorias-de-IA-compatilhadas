param(
  [Parameter(Mandatory = $true)]
  [string]$Pattern,
  [string]$Root = "C:\Agentes",
  [int]$MaxResults = 300,
  [switch]$ExactWord
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Root)) {
  Write-Error "Diretorio nao encontrado: $Root"
}

$allowed = @("*.md", "*.txt", "*.json", "*.csv", "*.tsv")
$all = @()
foreach ($f in $allowed) {
  $all += Get-ChildItem -Path $Root -Recurse -File -Filter $f -ErrorAction SilentlyContinue
}

if (-not $all) {
  Write-Output "Nenhum arquivo suportado encontrado em $Root"
  exit 0
}

if ($ExactWord) {
  $escaped = [Regex]::Escape($Pattern)
  # Palavra exata com fronteira de palavra.
  $regex = "\b$escaped\b"
  $matches = $all | Select-String -Pattern $regex -CaseSensitive:$false -ErrorAction SilentlyContinue
} else {
  $matches = $all | Select-String -Pattern $Pattern -CaseSensitive:$false -SimpleMatch -ErrorAction SilentlyContinue
}

if (-not $matches) {
  Write-Output "Sem resultados para: $Pattern"
  exit 0
}

$count = 0
foreach ($m in $matches) {
  if ($count -ge $MaxResults) { break }
  $path = $m.Path.Replace('\','/')
  $line = $m.Line.Trim()
  Write-Output ("{0}:{1}: {2}" -f $path, $m.LineNumber, $line)
  $count++
}

Write-Output ""
Write-Output "Resultados exibidos: $count"
