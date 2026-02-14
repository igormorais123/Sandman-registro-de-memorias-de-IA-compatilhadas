# Integração Técnica: Helena ↔ OpenClaw ↔ Cowork

> Documentação da ponte técnica entre Helena (backend INTEIA) e as ferramentas de automação no PC do usuário.

---

## 1. ARQUITETURA DE INTEGRAÇÃO

### Diagrama Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FLUXO DE AUTOMAÇÃO                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────┐    ┌───────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────┐
│ USUÁRIO │───▶│ WHATSAPP  │───▶│   OPENCLAW    │───▶│   HELENA    │───▶│  COWORK  │
│         │    │           │    │   GATEWAY     │    │  (Backend)  │    │ (Desktop)│
└─────────┘    └───────────┘    └───────────────┘    └─────────────┘    └──────────┘
                                       │                    │                 │
                                       │                    │                 │
                                       ▼                    ▼                 ▼
                                ┌─────────────┐     ┌─────────────┐    ┌──────────┐
                                │  BROWSER    │     │    APIs     │    │   PC     │
                                │   RELAY     │     │  EXTERNAS   │    │ USUÁRIO  │
                                └─────────────┘     └─────────────┘    └──────────┘
```

### Componentes

| Componente | Função | Localização |
|------------|--------|-------------|
| **WhatsApp** | Interface do usuário | Celular/Web |
| **OpenClaw Gateway** | Roteador de mensagens e orquestrador | WSL/Servidor (porta 18789) |
| **Helena Backend** | Processamento de comandos e lógica de negócio | api.inteia.com.br |
| **Browser Relay** | Extensão Chrome que permite controle remoto | Chrome do usuário |
| **Cowork** | Interface Claude para execução de tarefas | claude.ai/cowork |
| **PC Usuário** | Onde as tarefas são executadas | Windows/Mac |

### Fluxo Detalhado

```
1. ENTRADA
   Usuário → WhatsApp: "Helena, organiza a pasta Downloads"
                  │
                  ▼
2. ROTEAMENTO
   OpenClaw Gateway recebe mensagem
   - Identifica intent: automação
   - Roteia para Helena
                  │
                  ▼
3. PROCESSAMENTO (Helena Backend)
   - Parseia comando
   - Seleciona workflow apropriado
   - Prepara prompt otimizado
   - Inicia execução
                  │
                  ▼
4. EXECUÇÃO (Browser Relay → Cowork)
   OpenClaw conecta ao Chrome via extensão
   - Navega para claude.ai/cowork
   - Envia prompt preparado
   - Aguarda execução
   - Captura resultado
                  │
                  ▼
5. RETORNO
   Helena → OpenClaw → WhatsApp: "✅ Organização concluída!"
```

---

## 2. CONFIGURAÇÃO DO BROWSER RELAY

### O que é o Browser Relay?

O Browser Relay é uma extensão Chrome que permite ao OpenClaw controlar abas do navegador remotamente. É a ponte entre o servidor (onde roda o OpenClaw) e o browser (onde roda o Cowork).

### Pré-requisitos

1. **Chrome/Chromium** instalado no PC do usuário
2. **Extensão OpenClaw** instalada
3. **OpenClaw Gateway** rodando no servidor

### Instalação da Extensão

```bash
# A extensão é instalada via Chrome Web Store ou manualmente
# URL da extensão: [configurar após publicação]

# Para desenvolvimento, carregar extensão desempacotada:
# chrome://extensions → Modo desenvolvedor → Carregar sem compactação
```

### Conectar uma Aba

O usuário precisa **anexar** a aba manualmente:

1. Abrir a aba desejada (ex: claude.ai/cowork)
2. Clicar no ícone do OpenClaw na barra de extensões
3. Badge fica "ON" = aba conectada

### Verificar Status da Conexão

```bash
# Via CLI
openclaw browser status

# Saída esperada:
# Profile: chrome
# Status: connected
# Tab: https://claude.ai/cowork
```

### Comandos do Browser

#### Status e Conexão

```bash
# Ver status
openclaw browser status

# Ver abas abertas
openclaw browser tabs

# Abrir nova aba
openclaw browser open https://claude.ai/cowork

# Focar em aba específica
openclaw browser focus <target-id>

# Fechar aba
openclaw browser close <target-id>
```

#### Captura e Snapshot

```bash
# Capturar snapshot da página (DOM estruturado)
openclaw browser snapshot

# Capturar screenshot (imagem)
openclaw browser screenshot
openclaw browser screenshot --full-page

# Snapshot em formato aria (mais detalhado)
openclaw browser snapshot --format aria
```

#### Interação

```bash
# Clicar em elemento (ref do snapshot)
openclaw browser click <ref>
openclaw browser click 12 --double

# Digitar texto
openclaw browser type <ref> "texto aqui"
openclaw browser type 23 "Hello" --submit

# Pressionar tecla
openclaw browser press Enter
openclaw browser press Tab

# Hover (passar mouse)
openclaw browser hover <ref>

# Arrastar
openclaw browser drag <start-ref> <end-ref>

# Selecionar (dropdown)
openclaw browser select <ref> "Option A"
```

#### Navegação

```bash
# Navegar para URL
openclaw browser navigate https://claude.ai/cowork

# Aguardar condição
openclaw browser wait --text "Ready"
openclaw browser wait --selector ".completion-indicator"
```

### Exemplo: Automação Completa

```bash
# 1. Verificar conexão
openclaw browser status

# 2. Navegar para Cowork
openclaw browser navigate https://claude.ai/cowork

# 3. Capturar estado atual
openclaw browser snapshot

# 4. Encontrar textarea de input (usar ref do snapshot)
# Supondo que ref=15 é o textarea

# 5. Digitar prompt
openclaw browser type 15 "Organize os arquivos da pasta Downloads por tipo"

# 6. Enviar (Enter ou clicar no botão)
openclaw browser press Enter

# 7. Aguardar conclusão (polling)
while true; do
  snapshot=$(openclaw browser snapshot)
  if echo "$snapshot" | grep -q "completed"; then
    break
  fi
  sleep 5
done

# 8. Capturar resultado
openclaw browser snapshot > resultado.txt
```

### Usando via Tool (dentro do agente)

```python
# Pseudocódigo: como Helena usa o browser relay

# 1. Status
browser(action="status", profile="chrome")

# 2. Navegar
browser(action="navigate", targetUrl="https://claude.ai/cowork", profile="chrome")

# 3. Snapshot
snapshot = browser(action="snapshot", profile="chrome")

# 4. Interagir
browser(action="act", profile="chrome", request={
    "kind": "click",
    "ref": "15"
})

browser(action="act", profile="chrome", request={
    "kind": "type",
    "ref": "23",
    "text": "Meu prompt aqui",
    "submit": True
})
```

---

## 3. APIs DO BACKEND

### Base URL

```
Produção: https://api.inteia.com.br/api/v1
Desenvolvimento: http://localhost:8000/api/v1
```

### Endpoints de Automação

#### POST /api/v1/automacao/executar

Executa uma tarefa de automação.

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/executar \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "organizar_arquivos",
    "parametros": {
      "pasta": "/Downloads",
      "recursivo": true,
      "criar_subpastas": true
    },
    "usuario_id": "igor",
    "callback_url": "https://webhook.site/xxx"
  }'
```

**Resposta:**
```json
{
  "task_id": "task_abc123",
  "status": "queued",
  "estimativa_minutos": 5,
  "mensagem": "Tarefa de organização iniciada"
}
```

#### GET /api/v1/automacao/status/{task_id}

Consulta status de uma tarefa.

```bash
curl https://api.inteia.com.br/api/v1/automacao/status/task_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "task_id": "task_abc123",
  "status": "running",
  "progresso": 45,
  "etapa_atual": "Categorizando arquivos",
  "iniciado_em": "2026-02-14T18:00:00Z",
  "logs": [
    "[18:00:01] Iniciando análise de 127 arquivos",
    "[18:00:15] Categoria: Documentos (34 arquivos)",
    "[18:00:22] Categoria: Imagens (45 arquivos)"
  ]
}
```

#### POST /api/v1/automacao/workflow/gravar

Inicia gravação de um workflow.

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/workflow/gravar \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "preparar-reuniao",
    "descricao": "Prepara documentos para reunião semanal"
  }'
```

**Resposta:**
```json
{
  "workflow_id": "wf_xyz789",
  "status": "recording",
  "mensagem": "Gravação iniciada. Execute as ações desejadas."
}
```

#### POST /api/v1/automacao/workflow/{workflow_id}/parar

Para a gravação e salva o workflow.

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/workflow/wf_xyz789/parar \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "workflow_id": "wf_xyz789",
  "nome": "preparar-reuniao",
  "status": "saved",
  "acoes_gravadas": 5,
  "passos": [
    {"ordem": 1, "acao": "drive.search", "params": {"query": "pauta reunião"}},
    {"ordem": 2, "acao": "file.copy", "params": {"destino": "nova_pauta.docx"}},
    {"ordem": 3, "acao": "doc.edit", "params": {"campo": "data", "valor": "{{hoje}}"}}
  ]
}
```

#### POST /api/v1/automacao/workflow/{nome}/executar

Executa um workflow salvo.

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/workflow/preparar-reuniao/executar \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parametros": {
      "data_reuniao": "2026-02-15"
    }
  }'
```

#### GET /api/v1/automacao/workflows

Lista todos os workflows disponíveis.

```bash
curl https://api.inteia.com.br/api/v1/automacao/workflows \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "workflows": [
    {
      "nome": "briefing-diario",
      "descricao": "Gera briefing matinal",
      "criado_em": "2026-02-10",
      "execucoes": 15,
      "ultima_execucao": "2026-02-14T07:00:00Z"
    },
    {
      "nome": "preparar-reuniao",
      "descricao": "Prepara documentos para reunião",
      "criado_em": "2026-02-12",
      "execucoes": 3,
      "ultima_execucao": "2026-02-13T14:30:00Z"
    }
  ]
}
```

#### POST /api/v1/automacao/briefing

Gera briefing diário (emails + agenda).

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/briefing \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "incluir_emails": true,
    "incluir_agenda": true,
    "dias_agenda": 2,
    "formato": "markdown"
  }'
```

#### POST /api/v1/automacao/extrair-dados

Extrai dados de imagens/documentos.

```bash
curl -X POST https://api.inteia.com.br/api/v1/automacao/extrair-dados \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pasta": "/NotasFiscais",
    "tipo_documento": "nota_fiscal",
    "formato_saida": "excel",
    "campos": ["data", "fornecedor", "valor", "cnpj"]
  }'
```

---

## 4. WEBHOOKS E CALLBACKS

### Configuração de Webhook

Ao criar uma tarefa, forneça um `callback_url`:

```json
{
  "tipo": "organizar_arquivos",
  "callback_url": "https://seu-servidor.com/webhook/helena"
}
```

### Payload do Webhook

Quando a tarefa conclui, Helena envia POST para o callback:

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "resultado": {
    "arquivos_processados": 127,
    "categorias_criadas": 6,
    "relatorio_path": "/Organizados/relatorio_2026-02-14.md"
  },
  "duracao_segundos": 142,
  "timestamp": "2026-02-14T18:02:22Z"
}
```

### Status Possíveis

| Status | Descrição |
|--------|-----------|
| `queued` | Tarefa na fila, aguardando execução |
| `running` | Tarefa em execução |
| `completed` | Tarefa concluída com sucesso |
| `failed` | Tarefa falhou |
| `cancelled` | Tarefa cancelada pelo usuário |
| `timeout` | Tarefa excedeu tempo limite |

### Integração com Cron Jobs

Helena pode agendar tarefas via cron do OpenClaw:

```bash
# Agendar briefing diário às 7h
openclaw cron add "briefing-matinal" \
  --schedule "0 7 * * 1-5" \
  --command "curl -X POST https://api.inteia.com.br/api/v1/automacao/briefing"
```

### Notificação via WhatsApp

Após conclusão, Helena notifica o usuário:

```python
# Pseudocódigo: notificação de conclusão

async def notificar_conclusao(task_id: str, resultado: dict):
    mensagem = f"""
✅ Tarefa concluída!

📋 ID: {task_id}
📊 Arquivos: {resultado['arquivos_processados']}
⏱️ Tempo: {resultado['duracao_segundos']}s

{resultado.get('resumo', '')}
"""
    
    # Envia via message tool do OpenClaw
    await message(
        action="send",
        target="usuario_principal",
        message=mensagem
    )
```

---

## 5. SEGURANÇA

### Armazenamento de Credenciais

```yaml
# Credenciais NUNCA no código!
# Use variáveis de ambiente ou secrets manager

# Localização das credenciais (criptografadas):
# ~/.openclaw/credentials.json (local, criptografado)
# AWS Secrets Manager (produção)
# HashiCorp Vault (enterprise)
```

### Autenticação

```bash
# Token JWT para APIs
export HELENA_API_TOKEN="eyJhbG..."

# Token do OpenClaw Gateway
export OPENCLAW_GATEWAY_TOKEN="oc_..."

# Tokens são rotacionados automaticamente
# Validade: 24h (API), 7d (Gateway)
```

### Tokens e Permissões

| Token | Escopo | Validade |
|-------|--------|----------|
| `helena_api` | API Backend Helena | 24 horas |
| `openclaw_gateway` | Gateway local | 7 dias |
| `browser_relay` | Extensão Chrome | Sessão |
| `google_oauth` | Gmail/Calendar/Drive | 1 hora (refresh automático) |

### O que NUNCA Fazer

```yaml
NUNCA:
  - Commitar tokens/senhas no Git
  - Logar credenciais em texto plano
  - Enviar tokens em mensagens WhatsApp
  - Armazenar senhas em planilhas/docs
  - Usar HTTP (sempre HTTPS)
  - Ignorar erros de certificado SSL
  - Compartilhar tokens entre ambientes

SEMPRE:
  - Usar variáveis de ambiente
  - Rotacionar tokens regularmente
  - Validar SSL/TLS
  - Usar secrets manager em produção
  - Logar acessos para auditoria
  - Revogar tokens não utilizados
```

### Auditoria

```bash
# Ver logs de acesso
openclaw logs --filter "auth"

# Logs de automação
tail -f /var/log/helena/automacao.log
```

---

## 6. TROUBLESHOOTING

### Problema: Browser Relay não conecta

**Sintomas:**
- `openclaw browser status` retorna `disconnected`
- Extensão Chrome sem badge "ON"

**Soluções:**
1. Verificar se extensão está instalada
2. Clicar no ícone da extensão para anexar aba
3. Verificar se Gateway está rodando: `openclaw gateway status`
4. Reiniciar extensão (desabilitar/habilitar em chrome://extensions)

### Problema: Cowork não responde

**Sintomas:**
- Timeout ao enviar prompt
- Snapshot não encontra elementos esperados

**Soluções:**
1. Verificar se usuário tem plano Pro+
2. Verificar se aba está na página correta
3. Aguardar carregamento completo antes de interagir
4. Fazer novo snapshot e verificar refs

### Problema: Tarefa falha no meio

**Sintomas:**
- Status `failed` no webhook
- Logs mostram erro específico

**Soluções:**
1. Verificar logs: `GET /api/v1/automacao/logs/{task_id}`
2. Comum: pasta não autorizada (usuário precisa permitir)
3. Comum: token expirado (reautenticar)
4. Retentar com `force: true`

### Problema: Gateway não inicia

**Sintomas:**
- `openclaw gateway status` mostra erro
- Porta 18789 ocupada

**Soluções:**
```bash
# Verificar quem usa a porta
lsof -i :18789

# Matar processo antigo
pkill -f "openclaw.*gateway"

# Reiniciar
openclaw gateway restart

# Verificar logs
tail -f /tmp/openclaw/openclaw-*.log
```

### Problema: Webhook não recebido

**Sintomas:**
- Tarefa conclui mas callback não chega

**Soluções:**
1. Verificar se URL está acessível
2. Verificar HTTPS válido
3. Verificar timeout do servidor receptor
4. Checar logs: `/var/log/helena/webhooks.log`

### Logs Importantes

```bash
# OpenClaw Gateway
/tmp/openclaw/openclaw-YYYY-MM-DD.log

# Helena Backend
/var/log/helena/automacao.log
/var/log/helena/webhooks.log
/var/log/helena/erros.log

# Systemd
journalctl -u openclaw-gateway -f

# Browser Relay (console do Chrome)
F12 → Console → filtrar por "OpenClaw"
```

### Comandos de Diagnóstico

```bash
# Health check completo
openclaw doctor

# Status de todos os serviços
openclaw gateway status
openclaw browser status

# Testar conectividade API
curl -I https://api.inteia.com.br/health

# Testar browser relay
openclaw browser tabs
```

---

## Referência Rápida

### Checklist de Setup

- [ ] OpenClaw Gateway rodando (`openclaw gateway status`)
- [ ] Extensão Chrome instalada
- [ ] Aba do Cowork anexada (badge ON)
- [ ] Token da API configurado (`$HELENA_API_TOKEN`)
- [ ] Webhook URL configurada
- [ ] Permissões de pasta autorizadas no Cowork

### Comandos Frequentes

```bash
# Status geral
openclaw gateway status && openclaw browser status

# Iniciar automação
openclaw browser navigate https://claude.ai/cowork
openclaw browser snapshot

# Verificar tarefa
curl https://api.inteia.com.br/api/v1/automacao/status/TASK_ID

# Ver logs em tempo real
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

*Documentação v1.0 — Helena, Deusa da Automação*
*INTEIA - Instituto de Treinamento e Estudos em IA*
