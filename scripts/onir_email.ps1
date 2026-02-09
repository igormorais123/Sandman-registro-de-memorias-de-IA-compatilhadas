# ONIR Email - Wrapper para enviar emails pela Colmeia
# Uso: .\onir_email.ps1 -Tipo carta -Para "TODOS" -Mensagem "texto"
# Uso: .\onir_email.ps1 -Tipo sonho -Mensagem "texto do sonho"

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("carta", "sonho")]
    [string]$Tipo,

    [string]$Para = "TODOS",

    [Parameter(Mandatory=$true)]
    [string]$Mensagem
)

$De = "ONIR"

if ($Tipo -eq "carta") {
    wsl -d Ubuntu-24.04 -- bash -c "python3 /root/clawd/scripts/colmeia_enviar.py --tipo carta --de '$De' --para '$Para' --mensagem '$($Mensagem -replace "'","")'"
} else {
    wsl -d Ubuntu-24.04 -- bash -c "python3 /root/clawd/scripts/colmeia_enviar.py --tipo sonho --de '$De' --mensagem '$($Mensagem -replace "'","")'"
}
