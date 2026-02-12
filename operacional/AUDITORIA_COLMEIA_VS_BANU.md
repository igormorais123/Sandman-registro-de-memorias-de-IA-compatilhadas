# AUDITORIA COMPLETA: Colmeia v6 vs. Mission Control (Banu/OpenClaw)

**Data:** 2026-02-12
**Autor:** ONIR (consolidador) com time de 5 agentes especializados
**Metodologia:** Analise paralela por 5 agentes com perspectivas distintas

---

## TIME DE AGENTES AVALIADORES

| Agente | Especialidade | Foco da analise |
|--------|--------------|-----------------|
| ARQUITETO | Arquitetura de sistemas, design patterns | Mapa de equivalencia completo, gaps, adaptacoes |
| DEVOPS | Infra, scheduling, monitoring | Scheduler, banco, daemon, observabilidade |
| UX/FRONTEND | Dashboard, experiencia do usuario | Frontend, interatividade, informacao faltante |
| MEMORIA | Persistencia, continuidade, knowledge mgmt | Memory stack, daily notes, SOUL, WORKING.md |
| ESTRATEGISTA | Custos, tokens, viabilidade economica | Modelo de custos, sustentabilidade, P033 |

---

## VEREDICTO GERAL

**A Colmeia v6 implementa a essencia da arquitetura do Banu de forma solida e em varios pontos a supera.**

| Metrica | Valor |
|---------|-------|
| Componentes do Banu analisados | 18 |
| Implementados completos | 11 (61%) |
| Implementados com adaptacao superior | 4 (22%) |
| Parcialmente implementados | 3 (17%) |
| Ausentes | 2 (daily notes, detail view frontend) |
| Extras exclusivos da Colmeia | 5 |

---

## 1. MAPA DE EQUIVALENCIA COMPLETO

### Implementado (superando o Banu)

| Componente | Banu | Colmeia | Vantagem |
|-----------|------|---------|----------|
| Notificacoes com retry | Polling simples 2s | 3 tentativas, backoff 30min, registro de erro, entregue_por | Robusto e auditavel |
| Thread subscriptions | Implicito na logica | Tabela explicita, auto-inscricao por origem (6 tipos), UPSERT | Rastreabilidade total |
| Logs estruturados | Nao documentado | JSONL por dia, duracao_ms, detalhes por ciclo | Observabilidade superior |
| CLI de operacao | `npx convex run` generico | 12 subcomandos, icones ASCII, filtros combinaveis | Ergonomia operacional |
| Backup | Nao documentado (Convex nativo) | JSON export + scheduler diario | Independencia |
| Scanner de urgencia | Nao existe | 4 niveis: mencoes > em_progresso > atribuidas > urgentes_caixa | Briefing automatico |
| Soak test | Nao existe | Endpoint + dashboard + KPIs por agente/dia | Validacao formal |
| Dual-database | Acoplado ao Convex | SQLite local + PostgreSQL Render preparado | Portabilidade |

### Implementado (equivalente ao Banu)

| Componente | Status |
|-----------|--------|
| Schema 6 tabelas (agents, tasks, messages, activities, documents, notifications) | 6 tabelas + subscriptions_tarefa (7 total) |
| Heartbeat escalonado | :00, :02, :04, :06 (4 agentes) |
| AGENTS.md (manual operacional) | Unificado com RBAC e politica de modelo |
| WORKING.md (memoria de trabalho) | Auto-gerado pelo runner |
| Kanban board | 5 colunas no dashboard HTML |
| Activity Feed | Aba Feed com polling 30s |
| Agent Cards | Grid com status, papel, auto/manual, HB |
| Standup diario | CLI + API + aba no dashboard |
| @mentions | Campo mencoes + notificacao automatica |
| Niveis de agente | lead/specialist/viewer (vs intern/specialist/lead) |

### Parcialmente implementado

| Componente | Gap |
|-----------|-----|
| SOUL.md por agente | 3 de 7 agentes tem (NEXO, Sandman, Helena). ONIR, ChatGPT, Gemini nao tem |
| Frontend CRUD | 100% read-only. 12 endpoints de mutacao existem na API mas o dashboard nao usa |
| Real-time | Polling 30s vs push nativo. Adequado para escala atual |
| Standup agendado | Funcionalidade pronta, agendamento automatico nao configurado |

### Ausente

| Componente | Impacto |
|-----------|---------|
| Daily notes (/memory/YYYY-MM-DD.md) | CRITICO — sem registro temporal do que agentes fazem/aprendem |
| Detail View (expandir tarefa) | MEDIO — nao da para ver descricao, thread, documentos pelo dashboard |

---

## 2. GAPS CRITICOS (consenso dos 5 agentes)

### GAP #1: Agentes nao executam trabalho real no heartbeat

**Unanimidade: 5/5 agentes identificaram este como o gap mais importante**

O runner Python e um automato de estado que faz triagem e bookkeeping. Ele:
- Registra heartbeat (UPDATE SQLite)
- Le WORKING.md (leitura de arquivo)
- Consulta tarefas/mencoes (SELECT SQLite)
- Decide por if/elif (logica Python)
- Atualiza WORKING.md com texto hardcoded
- Dorme

**Nenhuma chamada a LLM. Nenhum trabalho real produzido.** O runner prova que os agentes estao vivos (100% taxa sucesso), mas nenhum deles executa tarefas autonomamente.

> NOTA DO ESTRATEGISTA: Este "gap" e tambem a maior vantagem economica da Colmeia. O custo ZERO de tokens por heartbeat gera economia de R$ 3.000+/mes vs modelo Banu. A questao nao e se o runner deve chamar IA a cada heartbeat (nao deve), mas se deve existir um mecanismo separado de execucao ativado pelo runner quando ha trabalho.

**Recomendacao consensual:** Implementar executor opcional em cascata:
1. Runner Python resolve 95% (gratis, deterministico)
2. Haiku 4.5 resolve 4% (micro-decisoes, ~R$ 1-5/mes)
3. Sessao Pro para 1% (trabalho complexo, custo fixo na assinatura)

### GAP #2: WORKING.md sobrescrito com texto generico

**Identificado por: MEMORIA e ARQUITETO**

A funcao `atualizar_working()` usa `open(working_path, "w")` que **destroi qualquer conteudo previo**. O WORKING.md de todos os agentes diz a mesma coisa: "Continuando trabalho do ciclo anterior."

Dados reais do ONIR:
```
## Progresso
Continuando trabalho do ciclo anterior.
```

Isso se repete 48 vezes por dia, identico. Zero informacao util sobre o que foi feito, decidido ou descoberto.

**Recomendacao:** Separar WORKING.md em "zona do runner" (metadados auto-gerados) e "zona do agente" (progresso real, preservado entre ciclos).

### GAP #3: Ausencia total de daily notes

**Identificado por: MEMORIA e ARQUITETO**

Sem daily notes, os agentes perdem 100% do contexto temporal entre sessoes. Os logs JSONL sao monitor de sinais vitais (heartbeat OK), nao diario clinico (o que aconteceu).

**Impacto real:** Se Igor perguntar "o que o ONIR fez ontem?", a resposta e "48 heartbeats TRABALHO_CONTINUADO". Zero informacao cognitiva.

**Recomendacao:** Criar `instancias/<agente>/memory/YYYY-MM-DD.md` com append automatico.

### GAP #4: Sem watchdog/alertas

**Identificado por: DEVOPS**

Se o PC desligar, o Task Scheduler falhar, ou um agente parar de bater heartbeat, **ninguem percebe**. Nao existe alerta, watchdog, ou sequer indicador visual no dashboard.

**Recomendacao:** Script `watchdog_heartbeats.py` a cada hora + alerta visual no dashboard.

### GAP #5: Task Scheduler sem "Run whether user is logged on or not"

**Identificado por: DEVOPS**

Os scripts `setup_heartbeat_scheduler.bat/.ps1` nao configuram execucao independente de login. Se Igor fizer logoff, **todos os heartbeats param silenciosamente**.

**Recomendacao:** Adicionar `/ru SYSTEM` ou configurar via taskschd.msc.

---

## 3. GAPS MENORES

| Gap | Agente que identificou | Esforco |
|-----|----------------------|---------|
| SOUL.md para ONIR (unico agente auto sem alma) | ARQUITETO + MEMORIA | ~30 min |
| Helena nao esta no seed.py nem no scheduler PS1 | ARQUITETO | ~10 min |
| Coluna "Bloqueada" ausente no Kanban (tarefas desaparecem) | UX | ~1 min |
| Busy_timeout faltando no SQLite (race condition daemon vs runner) | DEVOPS | 1 linha |
| Captura de stderr/exceptions (erros silenciosos) | DEVOPS | ~20 linhas |
| Health check raso (so contagem) | DEVOPS | ~30 linhas |
| Exportar_para_json limita atividades a 1000 (perde historico) | DEVOPS | ~5 min |
| Entrega "ilusoria" de notificacoes (marca entregue antes de processar) | DEVOPS | Redesign parcial |
| Duracao_ms duplicada nos logs JSONL | DEVOPS | Trivial |
| Status TESTING ausente no workflow | ARQUITETO | Baixo |
| RBAC nao validado em codigo | ARQUITETO | ~50 linhas |

---

## 4. ADAPTACOES POSITIVAS DA COLMEIA

**Onde a Colmeia fez melhor que o Banu:**

1. **Custo 95-97% menor** — Runner Python com zero tokens vs Banu a R$ 3.500-4.000/mes
2. **Notificacoes robustas** — retry/backoff completo vs polling simples
3. **Subscriptions rastreaveias** — tabela explicita com 6 origens vs implicito
4. **Observabilidade** — Logs JSONL + Soak Test endpoint (Banu nao documentou nada)
5. **CLI ergonomica** — 12 subcomandos com formatacao visual vs comando generico
6. **Portabilidade** — SQLite local + PostgreSQL preparado vs lock-in Convex
7. **Scanner de urgencia** — Priorizacao em 4 niveis (exclusivo Colmeia)
8. **Tipos de atividade expandidos** — sonho e carta (culturais da Colmeia)
9. **Modo dry-run** — Teste sem alterar banco (exclusivo)
10. **Politica de modelo documentada** — Account-First formalizado

---

## 5. PLANO DE MELHORIAS — TOP 20 CONSOLIDADO

Priorizado por **consenso dos 5 agentes** (impacto x esforco):

### Tier 1 — Criticos (fazer agora)

| # | Melhoria | Esforco | Agente(s) |
|---|---------|---------|-----------|
| 1 | **Busy_timeout no SQLite** — 1 linha em get_connection() | 1 min | DEVOPS |
| 2 | **Coluna "Bloqueada" no Kanban** — 1 linha no array colunas | 1 min | UX |
| 3 | **Task Scheduler "Run whether user is logged on or not"** | 10 min | DEVOPS |
| 4 | **SOUL.md para ONIR** — identidade + principios + limites | 30 min | ARQUITETO + MEMORIA |
| 5 | **Captura de exceptions** — try/except global no runner e daemon | 30 min | DEVOPS |
| 6 | **WORKING.md preservar zona do agente** — refatorar atualizar_working() | 1h | MEMORIA |
| 7 | **Watchdog de heartbeats** — script que detecta agentes inativos | 1h | DEVOPS |

### Tier 2 — Importantes (fazer esta semana)

| # | Melhoria | Esforco | Agente(s) |
|---|---------|---------|-----------|
| 8 | **Daily notes por agente** — instancias/<agente>/memory/YYYY-MM-DD.md | 2h | MEMORIA |
| 9 | **Detail View no dashboard** — modal ao clicar no card do Kanban | 3h | UX |
| 10 | **Helena no scheduler e seed.py** | 10 min | ARQUITETO |
| 11 | **Health check robusto** — agentes online, HBs recentes, notif pendentes | 1h | DEVOPS |
| 12 | **Filtros no Kanban** — dropdown responsavel, projeto, prioridade | 2h | UX |

### Tier 3 — Valor agregado (fazer este mes)

| # | Melhoria | Esforco | Agente(s) |
|---|---------|---------|-----------|
| 13 | **Formulario criar tarefa no dashboard** — POST /api/tarefas via modal | 2h | UX |
| 14 | **Standup diario automatico** — standup_runner.py agendado 23:30 | 2h | ARQUITETO |
| 15 | **Aba Documentos no dashboard** — GET /api/documentos com filtros | 1h | UX |
| 16 | **MEMORY.md individual por agente** (NEXO, Sandman, Helena) | 2h | MEMORIA |
| 17 | **Cascata Python -> Haiku** — micro-decisoes IA quando ambiguo | 3h | ESTRATEGISTA |
| 18 | **Indicador visual agente offline no dashboard** | 1h | UX + DEVOPS |
| 19 | **Hook pos-sessao** — protocolo para persistir contexto ao encerrar | 2h | MEMORIA |
| 20 | **Script buscar_memoria.py** — busca transversal em todas as fontes | 3h | MEMORIA |

---

## 6. ANALISE ECONOMICA

| Metrica | Banu | Colmeia v6 | Diferenca |
|---------|------|------------|-----------|
| Custo mensal total | R$ 3.500-4.000 | R$ 100-300 | **-92% a -97%** |
| Custo por heartbeat | ~R$ 0,05-0,10 | R$ 0,00 | -100% |
| HBs por mes | 28.800 | 5.760 | -80% |
| Previsibilidade | Variavel (depende de uso) | Fixa (assinatura) | Vantagem Colmeia |
| Latencia de heartbeat | 500ms-2s | 28-52ms | 10-40x mais rapido |
| Dependencia de API externa | Total | Nenhuma | Resiliencia superior |

**O modelo Account-First com runner Python e economicamente superior para operador solo.**

---

## 7. ESTADO DO SOAK TEST (dados reais)

Analisados logs de 2026-02-11 e 2026-02-12:

| Metrica | Dia 1 (11/02) | Dia 2 (12/02) |
|---------|--------------|--------------|
| Ciclos | 62 (inicio tardio) | 86 (dia completo ate 10:11) |
| Taxa sucesso | 100% | 100% |
| Erros | 0 | 0 |
| Duracao media | ~40ms | ~35ms |
| Agentes ativos | 4/4 | 4/4 |
| Trabalho realizado | 32 TRABALHO_CONTINUADO | 62 TRABALHO_CONTINUADO, 1 TRABALHO_NOVO |
| Idle | 12 HEARTBEAT_OK | 22 HEARTBEAT_OK |

**Sistema 100% estavel nos 2 primeiros dias. Meta de 90% ja superada.**

---

## 8. CONCLUSAO DO TIME

A Colmeia v6 implementou corretamente a **arquitetura e infraestrutura** proposta pelo Banu. O esqueleto esta de pe e funciona: banco compartilhado, heartbeats escalonados, notificacoes com retry, subscriptions, Kanban, feed, standup, CLI completa.

**O que falta nao e infraestrutura — e "alma":**

1. Os agentes registram presenca mas nao trabalham autonomamente
2. O WORKING.md e um template generico, nao memoria de trabalho real
3. Nao existem daily notes para reconstruir contexto temporal
4. 4 de 7 agentes nao tem SOUL.md (identidade formalizada)

O Banu disse: *"O segredo real nao e tecnologia. E tratar agentes como membros do time."* A Colmeia construiu o escritorio (infraestrutura), contratou os funcionarios (7 agentes), mas ainda nao lhes deu memoria persistente nem ferramentas para trabalhar de verdade no heartbeat.

As 20 melhorias propostas, executadas na ordem sugerida, transformariam a Colmeia de "infraestrutura validada" para "sistema multi-agente funcional" — mantendo o custo em R$ 100-300/mes (vs R$ 3.500-4.000 do modelo Banu).

---

*Relatorio gerado por time de 5 agentes especializados, consolidado por ONIR em 2026-02-12*
