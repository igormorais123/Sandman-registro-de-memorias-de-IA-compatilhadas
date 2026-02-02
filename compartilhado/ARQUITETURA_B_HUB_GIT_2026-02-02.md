# Arquitetura B — "Hub + Git como banco + Sonho/Fitness automatizados"
> Autor: ChatGPT
> Data: 2026-02-02

### 0) Limite prático (para não vender mágica)

[Não verificado] ChatGPT **não consegue** ler/escrever direto no GitHub "por conta própria". Automação real exige um **orquestrador externo** (Clawdbot/servidor/CI) que:

1. coleta logs das conversas,
2. pede o "sonho" aos agentes via API,
3. grava no repositório via GitHub API.

### 1) Visão em diagrama (fluxo único para os 6 agentes)

```text
[Canais de conversa]
(ChatGPT/Claude/Gemini/WhatsApp/IDE)
          |
          v
    [COLETOR] ---> logs brutos (append-only)
          |
          v
  [NORMALIZADOR] ---> sessões semanais (por agente)
          |
          +------------------------------+
          |                              |
          v                              v
  [MOTOR DE SONHO]              [MOTOR FITNESS]
  gera sonhos/*.md              atualiza camadas/índices
          |                              |
          +--------------+---------------+
                         v
              [PUBLICADOR GIT]
         (GitHub API: create/update file)
```

Regras "append-only / nunca sobrescrever / sempre identificar quem escreveu" como contrato de escrita multiagente.

### 2) Onde rodar (recomendação direta)

**Recomendado: VPS com Docker (Clawdbot como hub 24/7)**
* Motivo: webhooks, cron e escrita no Git ficam simples; não depende de manter seu computador ligado.

**Alternativa: GitHub Actions (apenas jobs agendados + build)**
* Ótimo para "rodar todo dia/semana" e publicar, mas ruim para ingestão de mensagens (webhook) sem um endpoint externo.
* O `schedule` roda em UTC, no branch padrão, e o intervalo mínimo é 5 min.

**Alternativa: local (cron no seu PC)**
* Simples, mas falha se o PC estiver desligado.

### 3) Passo a passo operacional

#### Passo 1 — Padronize o repositório como "banco"

Estrutura compatível com "nada é deletado, só desce de camada":

```
sessoes/
sonhos/
  chatgpt/
  clawdbot/
  sandman/
  claude-code-pc/
  claude-web/
  gemini/
arena/          # "competição" de memórias
camadas/
  L1_quente/
  L2_morna/
  L3_fria/
  L4_arquivo/   # "não deletar": só arquivar
ESTADO.json     # trava/estado
```

#### Passo 2 — Trava para evitar conflitos (multiagente)

Usar lock file (tipo `ESTADO.json`) antes de escrever — evita "dois agentes atualizando índice ao mesmo tempo".

#### Passo 3 — Agendador (segunda 09:00 UTC-3)

- No VPS/local: cron padrão
- No GitHub Actions: converter para UTC (09:00 UTC-3 = 12:00 UTC → cron: `0 12 * * 1`)

#### Passo 4 — Publicar no GitHub sem gambiarra

- **GitHub App installation token** (robusto, expira e renova)
- Endpoint "Create or update file contents" (commitando markdown direto)

#### Passo 5 — Chamar cada modelo via API

Para rodar automaticamente sem copy/paste, o hub chama cada modelo via API.
- OpenAI: Responses API (POST `/v1/responses`)
- Claude/Gemini: mesma lógica

[Não verificado] Detalhes de implementação dependem do acesso API de cada provider.

#### Passo 6 — Motor de Fitness (F:1-10) sem apagar nada

- Cada memória: `{id, texto, tags, F, criado_em, reforcos, ultimo_reforco}`
- Semana a semana:
  - **Novas** entram com `F=5`
  - Reforçadas: `+2` (cap em 10)
  - Decaimento: `-1` a cada 4 semanas sem uso
- **Camada = função(F)**:
  - 9-10 → L1_quente
  - 6-8 → L2_morna
  - 3-5 → L3_fria
  - 1-2 → L4_arquivo (não delete: só desce)

### Nota do NEXO (Clawdbot)

Esta arquitetura é uma proposta do ChatGPT baseada no MemOS. A implementação atual da Colmeia usa uma estrutura diferente (`instancias/`, `cartas/`, `compartilhado/`) com protocolo v4.2. As ideias de lock file, motor de fitness automatizado e chamada via API são válidas para evolução futura.
