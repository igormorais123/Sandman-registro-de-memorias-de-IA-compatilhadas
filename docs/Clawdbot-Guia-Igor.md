# Clawdbot/Moltbot - Guia Completo para Igor

> **Resumo**: Clawdbot (agora Moltbot) é um assistente IA pessoal que roda no seu próprio hardware, acessível via WhatsApp, Telegram, Discord e outros. Funciona 24/7 como um "funcionário IA" com memória persistente e acesso ao sistema.

---

## O Que É o Clawdbot

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA CLAWDBOT                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [WhatsApp] [Telegram] [Discord] [Slack] [iMessage]           │
│        │          │          │        │        │               │
│        └──────────┴──────────┴────────┴────────┘               │
│                          │                                      │
│                    ┌─────▼─────┐                                │
│                    │  GATEWAY  │  ◄── Sempre ativo (daemon)    │
│                    │ Port 18789│                                │
│                    └─────┬─────┘                                │
│                          │                                      │
│              ┌───────────┴───────────┐                         │
│              │                       │                          │
│        ┌─────▼─────┐          ┌─────▼─────┐                    │
│        │  AGENTE   │          │  BROWSER  │                    │
│        │ Claude/GPT│          │  Control  │                    │
│        └─────┬─────┘          └───────────┘                    │
│              │                                                  │
│    ┌─────────┴─────────┐                                       │
│    │                   │                                        │
│ [Memória]  [Shell]  [Arquivos]  [Skills]  [Cron Jobs]         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Diferença do Claude Code**: Claude Code é para desenvolvimento no terminal. Clawdbot é para automação pessoal 24/7 via chat.

---

## Instalação no Windows (WSL2)

### Pré-requisitos

```bash
# 1. Verificar Node >= 22
node --version

# 2. Se não tiver, instalar via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 22
nvm use 22
```

### Instalação

```bash
# Instalar Moltbot (nome atual do Clawdbot)
npm install -g moltbot@latest

# Executar wizard de configuração
moltbot onboard --install-daemon
```

### Configuração com Claude Code (sua assinatura)

```bash
# Gerar token do Claude Code
claude setup-token

# Colar no Moltbot quando solicitado
# Escolher: "Anthropic token (paste setup-token)"
```

### Verificar instalação

```bash
moltbot doctor
```

---

## Ideias de Uso Personalizadas para Igor

### 1. Assistente de Doutorado via WhatsApp

**Problema**: Você está na SEEDF, lembra de algo do doutorado, mas não pode abrir o PC.

**Solução com Clawdbot**:
```
WhatsApp → "Clawdbot, adicione ao meu backlog do doutorado:
           revisar literatura sobre persuasão em ambientes públicos"

WhatsApp → "Me dê um resumo do último artigo que li sobre adesão à IA"

WhatsApp → "Quais são os próximos deadlines do meu doutorado?"
```

**Configuração sugerida**:
```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-5",
    "workspace": "C:/Users/IgorPC/Doutorado-Agentes"
  },
  "memory": {
    "enabled": true,
    "dailyNotes": true
  }
}
```

---

### 2. Briefings Matinais Automáticos

**Problema**: Você acorda e quer saber o que tem para fazer sem abrir 5 apps.

**Solução com Clawdbot** (Cron Job):
```json
{
  "cron": {
    "morning-briefing": {
      "schedule": "0 7 * * *",
      "task": "Gere meu briefing matinal: clima em Brasília, compromissos do dia, tarefas pendentes do doutorado, lembretes sobre Melissa e Helena",
      "deliverTo": "whatsapp:+55XXXXXXXXXXX"
    }
  }
}
```

**Resultado às 7h no WhatsApp**:
```
Bom dia Igor! Seu briefing de 27/01:

CLIMA: Brasília 24°C, chuva à tarde
COMPROMISSOS: Reunião SEEDF 14h
DOUTORADO: Deadline revisão literatura em 5 dias
FAMÍLIA: Consulta Helena amanhã 10h
SAÚDE: Lembrete de alongamento (hérnia L5-S1)
```

---

### 3. Integração com Sistema de Memória IA

**Problema**: Você tem memória no Google Drive mas outras IAs não acessam facilmente.

**Solução**: Clawdbot como ponte para o sistema de memória:

```json
{
  "agent": {
    "workspace": "G:/Meu Drive/memoria-ia-unificada"
  },
  "memory": {
    "path": "G:/Meu Drive/memoria-ia-unificada/CORE/CONTEXTO_ATIVO.md"
  }
}
```

**Comandos via chat**:
```
"Clawdbot, o que está no contexto ativo?"
"Atualize meu contexto: estou focando no Participa-DF esta semana"
"Adicione à memória de longo prazo: decisão de usar Next.js 15"
```

---

### 4. Assistente para Participa-DF

**Problema**: Você está no ônibus e tem uma ideia para o app de ouvidoria.

**Solução**:
```
WhatsApp → "Clawdbot, no projeto Participa-DF, crie um issue:
           implementar leitor de tela para formulário de denúncia"

WhatsApp → "Qual é o status atual do Participa-DF?"

WhatsApp → "Liste os componentes que precisam de WCAG 2.1"
```

---

### 5. Pesquisa Automatizada

**Problema**: Você precisa de artigos sobre persuasão + IA + servidores públicos.

**Solução**:
```
WhatsApp → "Clawdbot, pesquise artigos recentes sobre:
           - AI adoption in public sector
           - Persuasion technology government
           - Resistance to AI implementation
           Salve um resumo em G:/Meu Drive/memoria-ia-unificada/pesquisa/"
```

---

### 6. Monitoramento de Saúde (Hérnia L5-S1)

**Cron Job para lembretes**:
```json
{
  "cron": {
    "posture-reminder": {
      "schedule": "0 */2 * * 1-5",
      "task": "Envie lembrete gentil para Igor levantar e fazer alongamento",
      "deliverTo": "whatsapp:+55XXXXXXXXXXX"
    }
  }
}
```

---

### 7. Automação de Código via Chat

**Do celular**:
```
WhatsApp → "Clawdbot, no genagents, rode os testes"
← "Testes executados: 47/50 passando. 3 falhas em test_persuasion.py"

WhatsApp → "O que está falhando?"
← "Erro em linha 234: mock de servidor não inicializado..."

WhatsApp → "Corrija e faça commit"
← "Corrigido. Commit: 'fix: initialize server mock before tests'"
```

---

## Skills Recomendadas para Instalar

```bash
# Produtividade
npx clawdhub@latest install obsidian-notes     # Integração Obsidian
npx clawdhub@latest install google-calendar    # Calendário
npx clawdhub@latest install todoist            # Tarefas

# Desenvolvimento
npx clawdhub@latest install github-pr          # Pull Requests
npx clawdhub@latest install conventional-commits
npx clawdhub@latest install claude-code        # Integração Claude Code

# Pesquisa
npx clawdhub@latest install brave-search       # Busca web
npx clawdhub@latest install academic-research  # Papers acadêmicos
npx clawdhub@latest install exa-search         # Busca neural

# Automação
npx clawdhub@latest install browser-automation
npx clawdhub@latest install web-scraper

# Casa/Família
npx clawdhub@latest install reminders
npx clawdhub@latest install meal-planner
```

---

## Configuração Completa Sugerida

Arquivo: `~/.clawdbot/moltbot.json`

```json5
{
  // Modelo principal (usa sua assinatura Claude)
  "agent": {
    "model": "anthropic/claude-opus-4-5",
    "workspace": "C:/Users/IgorPC",
    "name": "Jarvis"  // ou nome que preferir
  },

  // Memória persistente
  "memory": {
    "enabled": true,
    "dailyNotes": true,
    "longTermPath": "G:/Meu Drive/memoria-ia-unificada/CORE/CONTEXTO_ATIVO.md"
  },

  // Sessões
  "session": {
    "idleMinutes": 120  // 2 horas antes de expirar
  },

  // Canais de comunicação
  "providers": {
    "whatsapp": {
      "enabled": true
      // Configurar via QR code no onboard
    },
    "telegram": {
      "enabled": true,
      "botToken": "SEU_TOKEN_BOT"
    }
  },

  // Segurança
  "dmPolicy": "pairing",  // Requer aprovação para novos contatos

  // Tarefas automáticas
  "cron": {
    "morning-briefing": {
      "schedule": "0 7 * * *",
      "task": "Gere briefing matinal: clima Brasília, compromissos, doutorado, família",
      "deliverTo": "whatsapp:+55XXXXXXXXXXX"
    },
    "posture-reminder": {
      "schedule": "0 10,12,14,16 * * 1-5",
      "task": "Lembre Igor de levantar e alongar (hérnia L5-S1)",
      "deliverTo": "whatsapp:+55XXXXXXXXXXX"
    },
    "weekly-doutorado": {
      "schedule": "0 20 * * 0",
      "task": "Resuma progresso semanal do doutorado e sugira próximos passos",
      "deliverTo": "whatsapp:+55XXXXXXXXXXX"
    }
  },

  // Sub-agentes para tarefas paralelas
  "agents": {
    "defaults": {
      "subagents": {
        "model": "anthropic/claude-sonnet-4"  // Mais barato para sub-tarefas
      }
    }
  }
}
```

---

## Segurança Importante

### Riscos Identificados

1. **Gateway exposto**: Nunca use `bind: "0.0.0.0"` sem autenticação
2. **Credenciais**: Não commite `~/.clawdbot/` em repositórios
3. **DM Policy**: Mantenha `"pairing"` para evitar estranhos enviando comandos

### Configuração Segura

```json5
{
  "gateway": {
    "bind": "loopback",  // Apenas localhost
    // OU com Tailscale:
    "bind": "tailnet",
    "allowTailscale": true
  },
  "dmPolicy": "pairing",
  "allowFrom": [
    "+55SEUNUMERO"  // Apenas seu número
  ]
}
```

---

## Comandos Úteis

```bash
# Iniciar gateway
moltbot gateway --verbose

# Enviar mensagem de teste
moltbot message send --to +55NUMERO --message "Teste"

# Executar tarefa diretamente
moltbot agent --message "Liste meus arquivos recentes" --thinking high

# Diagnóstico
moltbot doctor

# Ver logs
moltbot logs --follow

# Aprovar novo dispositivo
moltbot pairing approve whatsapp ABC123
```

---

## Integração com Seu Sistema de Memória

### Sincronização Automática

Adicione ao seu `consolidar.bat`:

```batch
:: Após consolidação, notificar Clawdbot
moltbot message send --to +55SEUNUMERO --message "Memória consolidada. Novo contexto disponível."
```

### Comandos via Chat

```
"Clawdbot, execute ciclo de sono global"
→ Roda o script de consolidação

"Clawdbot, sincronize com Google Drive"
→ Executa sync-google-drive.ps1

"Clawdbot, qual o status da memória?"
→ Lê INDICE_GLOBAL.md e reporta
```

---

## Casos de Uso Avançados

### 1. Agente de Pesquisa Acadêmica

```
"Clawdbot, pesquise no Google Scholar artigos de 2024-2025 sobre
'AI resistance public sector' e salve resumos em formato BibTeX"
```

### 2. Monitor de Repositórios

```json5
{
  "cron": {
    "check-repos": {
      "schedule": "0 9 * * *",
      "task": "Verifique PRs e issues nos repos: genagents, participa-df. Resuma pendências.",
      "deliverTo": "telegram:@igormorais"
    }
  }
}
```

### 3. Transcrição de Reuniões

```
"Clawdbot, transcreva o áudio em C:/Users/IgorPC/reuniao.mp3
e extraia action items"
```

### 4. Automação de Formulários (Cuidado!)

```
"Clawdbot, preencha o formulário de frequência da SEEDF
com os dados padrão"
// Requer skill browser-automation + cuidado com dados sensíveis
```

---

## Próximos Passos

1. [ ] Instalar Moltbot via WSL2
2. [ ] Configurar autenticação com Claude Code (`claude setup-token`)
3. [ ] Conectar WhatsApp via QR code
4. [ ] Testar comando básico
5. [ ] Instalar skills prioritárias
6. [ ] Configurar cron jobs de briefing
7. [ ] Integrar com sistema de memória

---

## Links Úteis

- **Site oficial**: https://clawd.bot/
- **GitHub**: https://github.com/clawdbot/clawdbot
- **Documentação**: https://docs.molt.bot/
- **Skills**: https://github.com/VoltAgent/awesome-clawdbot-skills
- **Showcase**: https://clawd.bot/showcase

---

*Gerado em 2026-01-27 | Baseado no vídeo de Wes Roth e documentação oficial*
