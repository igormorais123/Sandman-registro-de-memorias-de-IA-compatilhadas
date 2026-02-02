# Sistema de Memória Unificada Multi-IA

Repositório central para compartilhamento de memória entre múltiplas IAs (Claude, ChatGPT, Gemini, Copilot).

## Arquitetura

```
GitHub (Hub Central)
       │
       ├── Claude Code (Lê/Escreve - Consolidador)
       ├── Claude Web/Desktop (Lê)
       ├── ChatGPT (Lê + Contribui via Zapier)
       ├── Gemini (Lê via import)
       └── Copilot (Lê nativamente)
```

## Estrutura

```
├── CORE/                    # Resumo (< 1500 chars cada)
│   ├── PERFIL.md           # Identidade do usuário
│   ├── INSTRUCOES.md       # O que todas IAs devem saber
│   └── CONTEXTO_ATIVO.md   # Estado atual
├── CONHECIMENTO/           # Aprendizados consolidados
│   ├── PADROES.md          # O que funciona
│   ├── ANTIPADROES.md      # O que evitar
│   └── DECISOES.md         # Decisões arquiteturais
├── SESSOES/                # Histórico por data/IA
├── INGEST/                 # Entrada de contribuições
│   └── chatgpt/            # Via Zapier
├── scripts/                # Automação
│   ├── consolidar.bat      # Script principal
│   ├── hook_contador.ps1   # Contador de sessões
│   └── consolidacao-memoria.xml # Task Scheduler
└── logs/                   # Logs de execução
```

## Setup

### 1. Task Scheduler (Consolidação ao Boot)

```powershell
# Importar tarefa agendada
schtasks /create /xml "scripts\consolidacao-memoria.xml" /tn "ConsolidacaoMemoriaIA"
```

### 2. Custom Instructions (ChatGPT)

Adicione nas Custom Instructions:
```
Consulte github.com/[usuario]/memoria-ia-unificada para contexto sobre decisões e padrões anteriores.
```

### 3. Zapier (ChatGPT → GitHub)

1. Criar conta em zapier.com (free tier)
2. Trigger: ChatGPT Tasks
3. Action: Create file in Google Drive → pasta INGEST/chatgpt/

## Uso

### Consolidação Manual
```bash
claude --print "ciclo de sono"
```

### Verificar Status
```bash
type .contador_sessoes
type .ultima_consolidacao
```

## Custo

| Item | Custo |
|------|-------|
| Claude Max | $0 (já tem) |
| GitHub | $0 |
| Zapier | $0 (free tier) |
| **Total** | **$0** |

---

*Sistema de Memória Multi-IA v2.0*
