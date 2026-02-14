# Configuração Google OAuth - Passo a Passo

## O que você precisa fazer (5 minutos):

### 1. Acessar Google Cloud Console
Abra: https://console.cloud.google.com/

### 2. Criar Projeto (se não tiver)
- Clique em "Select a project" → "New Project"
- Nome: `clawd-assistant`
- Criar

### 3. Habilitar APIs
Vá em: https://console.cloud.google.com/apis/library

Habilite:
- **Google Calendar API** (busque e clique Enable)
- **Gmail API** (busque e clique Enable)

### 4. Criar Credenciais OAuth
Vá em: https://console.cloud.google.com/apis/credentials

1. Clique **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
2. Se pedir, configure a "OAuth consent screen" primeiro:
   - User Type: **External**
   - App name: `Clawd Assistant`
   - Email: seu email
   - Salvar
3. Volte em Credentials → Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: `clawd-cli`
   - Create
4. **BAIXE O JSON** (botão de download)
5. Renomeie para `credentials.json`

### 5. Enviar o arquivo
Envie o `credentials.json` para mim pelo WhatsApp ou coloque em:
`/root/clawd/scripts/credentials.json`

---

Depois disso, eu faço o resto automaticamente!
