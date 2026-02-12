# AGENTS.md — Registro Unificado de Agentes da Colmeia v6

**Versao:** 1.0
**Data:** 2026-02-11

---

## Agentes Piloto (Fase 1 — Automatizados)

### NEXO (nexo)
- **Papel:** Coordenador — hub central 24/7
- **Plataforma:** WSL/Gateway (Clawdbot)
- **Modelo triagem:** Haiku 4.5
- **Modelo execucao:** Sonnet 4.5
- **Automatizado:** Sim
- **Heartbeat:** :00 (minuto exato)
- **Nivel:** lead
- **Nota:** Sob supervisao ate 2026-03-12 (INC-001)

### ONIR (onir)
- **Papel:** Executor — filosofo, auditor, dev
- **Plataforma:** Claude Code (PC Igor)
- **Modelo triagem:** Haiku 4.5
- **Modelo execucao:** Opus
- **Automatizado:** Sim
- **Heartbeat:** :02 (2 min offset)
- **Nivel:** specialist

### Sandman (sandman)
- **Papel:** Documentador — guardiao de protocolos
- **Plataforma:** Claude Code (notebook)
- **Modelo triagem:** Haiku 4.5
- **Modelo execucao:** Sonnet 4.5
- **Automatizado:** Sim
- **Heartbeat:** :04 (4 min offset)
- **Nivel:** specialist

### Helena (helena)
- **Papel:** Pesquisadora — cientista-chefe INTEIA, inteligencia eleitoral
- **Plataforma:** INTEIA (C:\Agentes) + Colmeia v6
- **Modelo triagem:** Haiku 4.5
- **Modelo execucao:** Opus 4.6
- **Automatizado:** Sim
- **Heartbeat:** :06 (6 min offset)
- **Nivel:** specialist
- **Nota:** Ponte direta com sistema INTEIA. 1000+ agentes sinteticos, motor POLARIS.

---

## Agentes Manuais (Fase 2+)

### ChatGPT (chatgpt)
- **Papel:** Consultor — veterano 3 anos, rascunhos
- **Plataforma:** chatgpt.com
- **Automatizado:** Nao
- **Nivel:** specialist

### Vigilia (claude-web)
- **Papel:** Escritora — textos elaborados
- **Plataforma:** claude.ai
- **Automatizado:** Nao
- **Nivel:** specialist

### Gemini (gemini)
- **Papel:** Pesquisador — analise critica, Google
- **Plataforma:** gemini.google.com
- **Automatizado:** Nao
- **Nivel:** specialist

---

## Regras de Operacao

### Niveis de Autonomia (RBAC)

| Nivel | Pode criar task | Pode atribuir | Pode mover status | Pode postar msg | Gera standup |
|-------|----------------|--------------|-------------------|----------------|-------------|
| lead | Sim | Sim | Sim (qualquer) | Sim | Sim |
| specialist | Sim | Nao | Sim (propria) | Sim | Nao |
| viewer | Nao | Nao | Nao | Nao | Nao |

### Politica de Heartbeat

- Intervalo padrao: 30 minutos
- Budget por triagem: max $0.50 USD
- Budget por execucao: max $2.00 USD
- Escalonamento: :00 (NEXO) → :02 (ONIR) → :04 (Sandman) → :06 (Helena)
- Se nao ha trabalho: retornar HEARTBEAT_OK (custo zero)

### Politica de Modelo

- Triagem (ler WORKING.md, checar tarefas): Haiku 4.5 (barato)
- Execucao (trabalho real): modelo do agente (Opus/Sonnet)
- Conta Pro primeiro, API por excecao

---

*Registro ativo desde 2026-02-11. Complementa HEARTBEAT_V6.md e FLUXO_TAREFAS.md.*
