# Credenciais Google Calendar

Este diretório armazena credenciais para integração com Google Calendar.

## Arquivos Esperados

| Arquivo | Descrição |
|---------|-----------|
| `google_calendar_credentials.json` | Credenciais OAuth2 (baixado do Google Console) |
| `google_calendar_token.json` | Token de acesso (gerado automaticamente) |
| `google_service_account.json` | Service Account (alternativa para automação) |

## Configuração OAuth2 (Recomendado para uso pessoal)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie ou selecione um projeto
3. Vá em **APIs & Services > Library**
4. Procure e ative **Google Calendar API**
5. Vá em **APIs & Services > Credentials**
6. Clique em **Create Credentials > OAuth client ID**
7. Se solicitado, configure a tela de consentimento OAuth:
   - User Type: External (ou Internal se for Workspace)
   - Preencha nome do app e email
   - Em Scopes, adicione: `https://www.googleapis.com/auth/calendar.readonly`
   - Adicione seu email como usuário de teste
8. Volte para Credentials e crie OAuth client ID:
   - Application type: **Desktop app**
   - Nome: qualquer um
9. Baixe o JSON e salve como `google_calendar_credentials.json` aqui

### Primeira Autorização

```bash
python3 /root/clawd/scripts/google_calendar.py --list
```

Um navegador abrirá para autorização. Após autorizar, o token será salvo automaticamente.

## Configuração Service Account (Para automação/servidor)

1. No Google Console, vá em **APIs & Services > Credentials**
2. **Create Credentials > Service account**
3. Dê um nome e crie
4. Baixe a chave JSON e salve como `google_service_account.json` aqui
5. Copie o email da Service Account (algo@projeto.iam.gserviceaccount.com)
6. No Google Calendar:
   - Abra Configurações > Configurações do calendário
   - Em "Compartilhar com pessoas específicas", adicione o email da Service Account
   - Dê permissão de leitura

## Segurança

⚠️ **NUNCA** commit estes arquivos no git!

O `.gitignore` já deve ignorar este diretório:
```
credentials/
*.json
```

## Testar

```bash
# Verificar status das credenciais
python3 /root/clawd/scripts/google_calendar.py --check-creds

# Listar eventos de hoje
python3 /root/clawd/scripts/google_calendar.py --list

# Próximos compromissos (2h)
python3 /root/clawd/scripts/google_calendar.py --upcoming
```
