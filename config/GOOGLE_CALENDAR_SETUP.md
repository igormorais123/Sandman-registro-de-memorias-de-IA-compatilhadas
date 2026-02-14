# Google Calendar Setup

## Status Atual
❌ **Credenciais não configuradas**

## Arquivos Necessários
- `/root/clawd/config/google_credentials.json` - OAuth client (baixar do Google)
- `/root/clawd/config/google_token.json` - Token (gerado automaticamente)

## Passos para Configurar

### 1. Google Cloud Console
1. Acesse https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. No menu lateral: **APIs & Services > Library**
4. Busque "Google Calendar API" e **Enable**

### 2. Criar Credenciais OAuth
1. Vá em **APIs & Services > Credentials**
2. Clique em **+ CREATE CREDENTIALS > OAuth 2.0 Client ID**
3. Se pedir, configure a tela de consentimento:
   - User Type: External
   - App name: (qualquer nome)
   - User support email: seu email
   - Developer contact: seu email
4. De volta em Credentials, selecione **Desktop application**
5. Clique em **Download JSON**
6. Salve o arquivo como:
   ```
   /root/clawd/config/google_credentials.json
   ```

### 3. Autorizar (primeira vez)
```bash
python3 /root/clawd/scripts/google_calendar.py --auth
```
Isso abrirá um navegador para login. Autorize o app.

### 4. Testar
```bash
# Ver próximos eventos
python3 /root/clawd/scripts/google_calendar.py --upcoming

# Eventos nas próximas 2 horas
python3 /root/clawd/scripts/google_calendar.py --hours 2

# Saída JSON (para cron jobs)
python3 /root/clawd/scripts/google_calendar.py --json --hours 4
```

## Uso no Cron
O script aceita `--json` para saída estruturada, ideal para cron jobs:

```bash
# Exemplo de uso no cron
python3 /root/clawd/scripts/google_calendar.py --json --hours 2
```

Retorna:
```json
{
  "count": 1,
  "events": [
    {
      "summary": "Reunião",
      "start": "2024-01-15T14:00:00-03:00",
      "location": "Zoom"
    }
  ]
}
```

## Troubleshooting

**Erro "credentials_missing"**: Baixe o JSON do Google Cloud Console

**Erro "token_missing"**: Execute `--auth` para gerar o token

**Token expirado**: O script renova automaticamente, mas se falhar, delete `google_token.json` e execute `--auth` novamente
