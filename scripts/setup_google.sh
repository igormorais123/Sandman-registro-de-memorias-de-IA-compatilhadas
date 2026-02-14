#!/bin/bash
# setup_google.sh - Configura Google Calendar e Gmail
# Versão: 1.0 (2026-02-13)

set -e

SCRIPT_DIR="/root/clawd/scripts"
CREDS_FILE="${SCRIPT_DIR}/credentials.json"

echo "🔧 Setup Google APIs"
echo ""

# Verificar se credentials.json existe
if [ ! -f "$CREDS_FILE" ]; then
    echo "❌ Arquivo credentials.json não encontrado!"
    echo ""
    echo "Por favor:"
    echo "1. Acesse: https://console.cloud.google.com/apis/credentials"
    echo "2. Crie um OAuth client ID (Desktop app)"
    echo "3. Baixe o JSON e salve como: $CREDS_FILE"
    exit 1
fi

echo "✅ credentials.json encontrado"
echo ""

# Configurar gcalcli
export PATH="$PATH:/root/.local/bin"

echo "📅 Configurando Google Calendar..."
echo "Uma janela do navegador vai abrir. Autorize o acesso."
echo ""

# Copiar credentials para onde gcalcli espera
mkdir -p ~/.config/gcalcli
cp "$CREDS_FILE" ~/.config/gcalcli/oauth_client_secrets.json

# Tentar autenticar
gcalcli --client-id="$(cat $CREDS_FILE | python3 -c "import sys,json; print(json.load(sys.stdin)['installed']['client_id'])")" list 2>&1 || {
    echo ""
    echo "Se não abriu o navegador automaticamente, copie o link acima e cole no browser."
    echo "Depois de autorizar, o terminal vai mostrar seus calendários."
}

echo ""
echo "✅ Setup completo!"
