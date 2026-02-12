# PERFIS E ANALISES INDIVIDUAIS — Time de Auditoria Colmeia v6

**Data:** 2026-02-12
**Consolidado por:** ONIR
**Metodologia:** 5 agentes especializados analisaram a Colmeia v6 em paralelo, cada um com foco distinto

---

## TIME DE AUDITORIA

| # | Agente | Especialidade | Foco | Arquivos analisados |
|---|--------|--------------|------|-------------------|
| 1 | ARQUITETO | Arquitetura de sistemas, design patterns | Mapa de equivalencia completo Banu→Colmeia, gaps, adaptacoes | 17 arquivos |
| 2 | DEVOPS | Infra, scheduling, monitoring, deploy | Scheduler, banco, daemon, observabilidade, escalabilidade | 18 fontes + 2 logs |
| 3 | UX/FRONTEND | Dashboard, experiencia do usuario | Frontend, interatividade, informacao faltante, estetica | 4 arquivos core |
| 4 | MEMORIA | Persistencia, continuidade, knowledge mgmt | Memory stack, daily notes, SOUL, WORKING.md | Todos os instancias/* + banco |
| 5 | ESTRATEGISTA | Custos, tokens, viabilidade economica | Modelo de custos, sustentabilidade, P033 | Logs + scripts + docs |

---

# AGENTE 1: ARQUITETO

## Perfil

```yaml
nome: ARQUITETO
especialidade: Arquitetura de sistemas e design patterns
perspectiva: Visao estrutural — como os componentes se encaixam
metodo: Cruzamento direto entre documentacao publica do Banu e codigo-fonte da Colmeia
ferramentas: Leitura de schema, modulos Python, configs, documentacao
fontes_externas: GitHub crshdn/mission-control, manish-raana/openclaw-mission-control, artigo Dan Malone, posts Bhanu Teja P
```

## Analise Completa

### 1. MAPA DE EQUIVALENCIA (Banu → Colmeia)

#### 1.1 Banco de Dados Compartilhado

| Aspecto | Banu | Colmeia | Status |
|---------|------|---------|--------|
| Plataforma | Convex (serverless, real-time) | SQLite/WAL (local) + PostgreSQL (prod) | **IMPLEMENTADO** com adaptacao |
| Tabela agents | Sim | `agentes` com campos equivalentes + `automatizado`, `sessao_ativa` | **IMPLEMENTADO** |
| Tabela tasks | Sim (PLANNING→INBOX→ASSIGNED→IN PROGRESS→TESTING→REVIEW→DONE) | `tarefas` com 7 status | **IMPLEMENTADO** com adaptacao |
| Tabela messages | Sim (threads por task) | `mensagens` vinculadas a tarefa_id, com campo mencoes | **IMPLEMENTADO** |
| Tabela activities | Sim (feed real-time) | `atividades` com 9 tipos | **IMPLEMENTADO** |
| Tabela documents | Sim (deliverables) | `documentos` com 7 tipos | **IMPLEMENTADO** |
| Tabela notifications | Sim (@mentions com fila) | `notificacoes` com retry/backoff completo | **IMPLEMENTADO** (superior) |
| Thread subscriptions | Implicito no Convex | `subscriptions_tarefa` tabela explicita com auto-inscricao | **IMPLEMENTADO** (superior) |
| Indices de performance | Nao documentado | 12 indices explicitos no schema | **IMPLEMENTADO** (superior) |

#### 1.2 Sistema de Heartbeat

| Aspecto | Banu | Colmeia | Status |
|---------|------|---------|--------|
| Mecanismo | Cron job por agente | Windows Task Scheduler (schtasks) | **IMPLEMENTADO** |
| Intervalo | 15 minutos | 30 minutos | **IMPLEMENTADO** (conservador) |
| Escalonamento | Staggered | :00, :02, :04, :06 | **IMPLEMENTADO** |
| Ciclo | check in → fetch → sync → execute | 6 passos: HB → WORKING → tarefas → mencoes → decisao → update | **IMPLEMENTADO** |
| Logs estruturados | Nao documentado | JSONL por dia com timestamp, resultado, duracao_ms | **IMPLEMENTADO** (superior) |
| Dry-run mode | Nao documentado | `--dry-run` flag | **IMPLEMENTADO** (superior) |

#### 1.3 Configuracao de Agentes

| Aspecto | Banu | Colmeia | Status |
|---------|------|---------|--------|
| SOUL.md | Sim, todos os 10 | 4 agentes (NEXO, Sandman, Helena, ONIR) | **IMPLEMENTADO** (apos Tier 1) |
| AGENTS.md | Sim, centralizado | Com RBAC e politica de modelo | **IMPLEMENTADO** |
| WORKING.md | Sim, por agente | 4 agentes, auto-atualizado com zona preservada | **IMPLEMENTADO** |
| Niveis | intern, specialist, lead | lead, specialist, viewer | **IMPLEMENTADO** com adaptacao |

#### 1.4 Notificacoes / @mentions

| Aspecto | Banu | Colmeia | Status |
|---------|------|---------|--------|
| @mentions | Sim | Campo mencoes + auto-notificacao | **IMPLEMENTADO** |
| Daemon | PM2 polling 2s | notificacao_daemon.py com intervalo configuravel | **IMPLEMENTADO** |
| Fila | Sim | retry/backoff, max_tentativas, proxima_tentativa_em | **IMPLEMENTADO** (superior) |
| Auto-subscription | Implicito | Explicito: 6 origens rastreadas | **IMPLEMENTADO** (superior) |

#### 1.5 Frontend

| Aspecto | Banu | Colmeia | Status |
|---------|------|---------|--------|
| Kanban | Sim | 7 colunas com cards coloridos por prioridade | **IMPLEMENTADO** |
| Activity Feed | Sim (real-time) | Sim (polling 30s) | **IMPLEMENTADO** |
| Agent Cards | Sim | Sim (status, papel, HB, auto/manual) | **IMPLEMENTADO** |
| Detail View | Sim | Nao | **AUSENTE** |
| Document Panel | Sim | Endpoint existe, UI nao | **PARCIAL** |

### 2. Gaps Criticos

1. **Heartbeats nao executam trabalho real** — runner e automato de estado, zero LLM
2. **ONIR sem SOUL.md** — resolvido no Tier 1
3. **Ausencia de daily notes** — sem registro temporal qualitativo

### 3. Gaps Menores

- Dashboard sem Detail View de tarefa
- Dashboard sem Document Panel
- Real-time vs polling (adequado para escala atual)
- Standup nao agendado automaticamente
- Helena sem heartbeat no setup_heartbeat_scheduler.ps1
- Status TESTING ausente no workflow
- Sem agent-to-agent direto (mencoes existem mas ninguem "responde" autonomamente)

### 4. Adaptacoes Positivas (onde Colmeia superou Banu)

1. Retry/backoff robusto nas notificacoes
2. subscriptions_tarefa como tabela explicita
3. Scanner de urgencia (4 niveis)
4. Logs JSONL estruturados
5. Soak test como conceito de qualidade
6. CLI completa e ergonomica (12 subcomandos)
7. Dual-database strategy (SQLite + PostgreSQL)
8. Tipos de atividade expandidos (sonho, carta)

### 5. Top 10 Recomendacoes

1. Implementar execucao real de trabalho no heartbeat (CRITICO)
2. Criar SOUL.md para ONIR (ALTO) — FEITO
3. Adicionar daily notes ao runner (MEDIO-ALTO)
4. Adicionar Helena ao scheduler e seed (MEDIO)
5. Agendar standup diario (MEDIO)
6. Detail View no dashboard (MEDIO)
7. Aba Documentos no dashboard (BAIXO-MEDIO)
8. WebSocket para dashboard (BAIXO)
9. Estado TESTING no workflow (BAIXO)
10. Validar RBAC no codigo (BAIXO)

### Resumo Quantitativo

| Metrica | Total |
|---------|-------|
| Componentes analisados | 18 |
| Implementados completos | 11 (61%) |
| Implementados com adaptacao positiva | 4 (22%) |
| Parcialmente implementados | 3 (17%) |
| Ausentes | 2 (daily notes, detail view) |
| Extras exclusivos da Colmeia | 5 |

---

# AGENTE 2: DEVOPS

## Perfil

```yaml
nome: DEVOPS
especialidade: Infraestrutura, scheduling, monitoring, deploy
perspectiva: Operacional — o que pode falhar, o que falta monitorar, o que nao escala
metodo: Leitura direta de scripts de automacao, logs operacionais, configs do scheduler, codigo de daemon
ferramentas: Analise de logs JSONL, scripts PowerShell/BAT, schema SQL, codigo de runner/daemon
fontes_analisadas: 18 fontes + 2 logs operacionais
```

## Analise Completa

### 1. Scheduling e Heartbeats

**Configuracao atual:**

| Agente | Task Name | Intervalo | Offset |
|--------|-----------|-----------|--------|
| NEXO | Colmeia_HB_NEXO | 30 min | :00 |
| ONIR | Colmeia_HB_ONIR | 30 min | :02 |
| SANDMAN | Colmeia_HB_SANDMAN | 30 min | :04 |
| HELENA | Colmeia_HB_HELENA | 30 min | :06 |
| Daemon | Colmeia_Notificacao_Daemon | 5 min | :01 |

**Divergencia:** `.ps1` registra apenas 3 agentes (sem Helena), `.bat` registra os 4. O `.bat` e o que esta em producao.

**Staggering de 2min** entre agentes evita contencion SQLite. Decisao acertada.

**Performance medida (2026-02-12):** 93 ciclos, duracao media ~40ms, range 18-82ms. Zero erros. 100% taxa sucesso.

**LIMITACAO CRITICA:** schtasks criados sem `/ru SYSTEM`. Heartbeats param se Igor fizer logoff ou PC hibernar.

### 2. Banco de Dados

**Configuracao de conexao (apos Tier 1):**
- WAL mode (leituras concorrentes)
- foreign_keys=ON (integridade referencial)
- busy_timeout=5000 (espera ate 5s se banco travado)

**7 tabelas + 12 indices** cobrindo queries operacionais.

**Pontos de atencao:**
- Single-writer constraint (ok para 4 agentes, problematico para 20+)
- Tabela `atividades` cresce indefinidamente (~70.000/ano)
- Conexoes nao usam context manager (leak possivel em exceptions)
- `exportar_para_json()` limita atividades a 1000 registros

### 3. Daemon de Notificacoes

Pseudo-daemon invocado pelo Task Scheduler a cada 5min com `--once`.

**Logica:** marca notificacao como "entregue" se agente esteve online nos ultimos 90min. Nao envia nada realmente — e heuristica. O heartbeat_runner le as notificacoes no proximo ciclo.

**Retry:** linear 30min fixo, 3 tentativas. Apos 3 falhas: `falha_final`.

**Tratamento de erros (apos Tier 1):** try/except no ciclo(), registra no log JSONL.

### 4. Monitoramento e Observabilidade

**Ferramentas existentes:**

| Ferramenta | Funcao | Agendada? |
|-----------|--------|-----------|
| watchdog_heartbeats.py | Detecta agentes inativos | NAO (manual) |
| verificar_heartbeats.py | Calcula KPIs do soak test | NAO (manual) |
| colmeia_status.py | Check legado pre-v6 | OBSOLETO |
| /api/health | Health check raso | Sim (API) |
| /api/soak-test | KPIs soak test | Sim (API) |

**Lacunas:**
1. Sem alertas proativos (ninguem notificado se agente parar)
2. Health check raso (`/api/health` retorna "ok" mesmo com todos inativos)
3. Dashboard mostra status errado (todos "dormindo" = bolinha cinza)
4. Soak test com datas hardcoded
5. Sem metricas de tendencia (media movel, desvio padrao)
6. Sem rotacao/retencao de logs

### 5. Deploy e Escalabilidade

**Preparacao para producao:**
- schema_postgres.sql pronto
- migrate_sqlite_to_postgres.py pronto
- render.yaml pronto

**Gargalo:** colmeia_db.py acoplado a sqlite3 — migrar para PostgreSQL exige reescrever modulo ou criar camada de abstracao.

**Carga atual:** ~480 writes/dia. Trivial para SQLite. Limite pratico: single-writer.

### 6. Top 10 Recomendacoes

**IMPLEMENTADAS (3/10):**
1. Watchdog automatico de heartbeats — FEITO
2. PRAGMA busy_timeout no SQLite — FEITO
3. Captura de excecoes nos runners — FEITO

**PENDENTES (7/10):**
4. Task Scheduler "Run whether user is logged on or not" (CRITICO, 5min)
5. Health check robusto com frescor de heartbeat (ALTO, 30min)
6. Camada de abstracao de banco (ALTO para futuro, 2-4h)
7. Rotacao e retencao de logs (MEDIO, 1h)
8. Indicador visual agente online/offline no dashboard (MEDIO, 20min)
9. Endpoint /api/metrics para monitoramento externo (MEDIO, 1h)
10. Standup automatico diario agendado (BAIXO, 30min)

---

# AGENTE 3: UX/FRONTEND

## Perfil

```yaml
nome: UX/FRONTEND
especialidade: Dashboard, experiencia do usuario, design de interface
perspectiva: Olhar de quem USA o sistema — o que Igor ve, o que nao consegue fazer, o que falta
metodo: Analise linha a linha do HTML/JS, cruzamento com endpoints da API nao consumidos
ferramentas: Leitura de index.html, api.py, schema.sql, colmeia_db.py
achado_chave: "12 endpoints construidos e funcionais que o frontend nao utiliza"
```

## Analise Completa

### 1. Estado atual: 100% read-only

O frontend faz apenas 5 chamadas GET:
- `/api/agentes`
- `/api/tarefas`
- `/api/atividades?limite=50`
- `/api/standup`
- `/api/soak-test?dias=7` (sob demanda)

**12 endpoints da API que o frontend ignora:**

| # | Endpoint | Funcao |
|---|---------|--------|
| 1 | `GET /api/tarefas/{id}` | Detalhe + mensagens |
| 2 | `POST /api/tarefas` | Criar tarefa |
| 3 | `PUT /api/tarefas/{id}/status` | Mudar status |
| 4 | `PUT /api/tarefas/{id}/assign` | Atribuir responsavel |
| 5 | `POST /api/tarefas/{id}/mensagens` | Comentar na thread |
| 6 | `GET /api/documentos` | Listar documentos |
| 7 | `GET /api/notificacoes/{agente}` | Notificacoes |
| 8 | `POST /api/notificacoes/processar` | Processar fila |
| 9 | `GET /api/subscriptions` | Inscricoes |
| 10 | `GET /api/scanner/{agente}` | Priorizacao urgencia |
| 11 | `GET /api/dashboard` | Dados consolidados |
| 12 | `POST /api/heartbeat/{agente}` | Heartbeat manual |

### 2. Impacto para Igor

Igor precisa abrir terminal para QUALQUER mutacao. O dashboard e "televisao" — mostra o que acontece, mas nao permite interagir. Nao da para:
- Criar tarefa
- Mover tarefa entre colunas
- Comentar numa thread
- Reatribuir responsavel
- Ver descricao ou mensagens de uma tarefa

### 3. Real-time vs Polling

Polling 30s com `setInterval` e `Promise.all`. Para 4 agentes com heartbeat a cada 30min e 1 usuario, e mais que suficiente. WebSocket/SSE so faria sentido com 20+ agentes ou multiplos usuarios simultaneos.

### 4. Informacao faltante no dashboard

- Threads de mensagens por tarefa (existe na API, invisivel)
- Descricao da tarefa (campo existe, nunca exibido)
- Notificacoes pendentes (sistema completo de retry, invisivel)
- Subscriptions (auto-inscricao rastreada, invisivel)
- Documentos (7 tipos indexados, invisivel)
- Scanner de urgencia (4 niveis, invisivel)

### 5. Estetica e Usabilidade

**Stack:** Tailwind CSS + AlpineJS, arquivo unico (354 linhas). Dark theme `bg-gray-900`.

**Vantagem do stack atual:** zero build step, qualquer agente pode editar, deploy = servir HTML estático. Correto para o contexto.

**Responsividade:** Kanban com 7 colunas empilha em 1 coluna no mobile — perde nocao espacial. Sugestao: tabs por coluna em mobile.

### 6. Funcionalidades exclusivas da Colmeia (sem equivalente no Banu)

- **Standup automatico** — 4 quadrantes + contagem HBs por agente
- **Soak Test Monitor** — barra temporal, KPIs, breakdown por agente/dia, distribuicao resultados

### 7. Top 10 Melhorias UX

| # | Melhoria | Impacto | Esforco |
|---|---------|---------|---------|
| 1 | **Detail View** — clicar card → modal com descricao + thread | CRITICO | Medio |
| 2 | **Filtros no Kanban** — dropdown responsavel, projeto, prioridade | ALTO | Baixo |
| 3 | **Painel de Notificacoes** — indicador no header + dropdown | ALTO | Medio |
| 4 | **Formulario criar tarefa** — modal com POST /api/tarefas | ALTO | Medio |
| 5 | **Mudanca de status via UI** — dropdown ou drag-and-drop | MEDIO-ALTO | Medio-alto |
| 6 | **Indicador online/offline real** — calcular freshness do HB no JS | MEDIO | Baixo |
| 7 | **Aba Documentos** — listar com filtros por tipo/autor | MEDIO | Baixo |
| 8 | **Thread e comentarios** — textarea no Detail View | MEDIO | Medio |
| 9 | **Barra de KPIs consolidados** — /api/dashboard no topo | MEDIO-BAIXO | Baixo |
| 10 | **Kanban mobile** — tabs por coluna em viewport < 768px | BAIXO-MEDIO | Baixo |

**Sintese:** ~200-300 linhas adicionais de HTML/Alpine transformariam o dashboard de "televisao" em "painel de controle", consumindo os 12 endpoints que o backend ja tem prontos.

---

# AGENTE 4: MEMORIA

## Perfil

```yaml
nome: MEMORIA
especialidade: Persistencia, continuidade, knowledge management
perspectiva: Como os agentes lembram (ou esquecem) — o que sobrevive entre sessoes e o que se perde
metodo: Analise das 5 camadas de memoria (Banu) vs implementacao real da Colmeia
achado_chave: "A Colmeia tem um sistema nervoso automatico (heartbeat) sem cortex (memoria cognitiva)"
```

## Analise Completa

### 1. Mapa de Memoria (5 Camadas)

| Camada (Banu) | Colmeia | Qualidade |
|---------------|---------|-----------|
| Session Memory (historico pesquisavel) | AUSENTE — runner e stateless (~30ms, nasce e morre) | 0/10 |
| Working Memory (WORKING.md) | PARCIAL — existe mas era auto-gerado com texto generico (corrigido no Tier 1) | 3/10 → 6/10 |
| Daily Notes (/memory/YYYY-MM-DD.md) | AUSENTE — nao existe para nenhum agente | 0/10 |
| Long-term Memory (MEMORY.md curado) | DISPERSA — 4 fontes que nao se comunicam | 4/10 |
| Soul/Identity (SOUL.md) | PARCIAL — 4 de 7 agentes (NEXO, Sandman, Helena, ONIR apos Tier 1) | 5/10 → 6/10 |

### 2. O Problema Central de Continuidade

**Os agentes da Colmeia NAO lembram o que estavam fazendo.**

O ciclo real do heartbeat:
1. Task Scheduler dispara heartbeat_runner.py
2. Runner abre conexao SQLite, le tarefas
3. Se tarefa em_progresso: WORKING.md recebe "Continuando trabalho do ciclo anterior."
4. Log JSONL registra timestamp, resultado, duracao_ms
5. Processo morre. Zero contexto cognitivo criado ou preservado.

**O que se perde entre ciclos:**
- O que o agente descobriu (artigos, decisoes)
- Contexto da tarefa ("ja li 3 de 5 artigos")
- Decisoes intermediarias ("descartei abordagem X porque...")
- Proximos passos concretos
- Bloqueios encontrados
- Aprendizados da sessao

### 3. A Dissociacao Runner vs Agente

No Banu: agentes escrevem diretamente no WORKING.md durante o trabalho.
Na Colmeia: trabalho real acontece em sessoes interativas desconectadas do runner.

**"Quem trabalha nao escreve estado; quem escreve estado nao trabalha."**

Correcao parcial no Tier 1: zona do agente preservada no WORKING.md (`<!-- ZONA DO AGENTE -->`). Agora o agente real pode escrever notas que sobrevivem entre ciclos do runner.

### 4. Daily Notes — O Gap Mais Critico

O que a Colmeia tem (logs JSONL):
```json
{"agente": "onir", "resultado": "TRABALHO_CONTINUADO", "duracao_ms": 19}
```

O que o Banu teria (daily notes):
```markdown
# 2026-02-12 — ONIR
10:02 - Heartbeat OK
11:30 - Sessao com Igor. Encontrei 3 artigos sobre masking...
12:00 - Decisao: usar framework de Hull como base
LICAO: autores usam 3 termos diferentes para masking
```

Log JSONL = **monitor de sinais vitais**
Daily notes = **diario clinico**

### 5. Long-term Memory — 4 Fontes Fragmentadas

| Fonte | Local | Quem escreve | Quem le |
|-------|-------|-------------|---------|
| `compartilhado/MEMORY.md` | Repo | ONIR | Todos (teoria) |
| `instancias/onir/MEMORIA_ATIVA.md` | Repo | ONIR | So ONIR |
| `.claude/projects/.../memory/MEMORY.md` | Local | Auto-memory Claude Code | So ONIR |
| `knowledge/` | Repo | Manual | Todos |

Nenhum outro agente tem memoria de longo prazo individual.
Auto-memory do ONIR nao esta no Git.
Fragmentacao impede busca unificada.

### 6. SOUL.md — Estado por Agente

| Agente | SOUL.md | Profundidade |
|--------|---------|-------------|
| NEXO | Completo (36 linhas) | Boa |
| Helena | Completo (104 linhas) | Excelente |
| Sandman | Completo (44 linhas) | Boa |
| ONIR | Completo (Tier 1) | Boa |
| ChatGPT | Nao tem | Vazio |
| Claude-Web | Nao tem | Razoavel (tem IDENTITY.md) |
| Gemini | Nao tem | Inexistente |

### 7. Top 10 Melhorias de Memoria

| # | Melhoria | Impacto |
|---|---------|---------|
| 1 | **WORKING.md real** — agente escreve, nao runner | CRITICO (Tier 1 resolveu parcialmente) |
| 2 | **Daily notes por agente** — instancias/`<agente>`/memory/YYYY-MM-DD.md | CRITICO |
| 3 | **MEMORY.md individual** por agente automatizado | ALTO |
| 4 | **SOUL.md para ONIR** | ALTO — FEITO |
| 5 | **WORKING.md com secoes semanticas** (contexto, bloqueios, proximos passos, licoes) | ALTO |
| 6 | **Hook pos-sessao** — persistir contexto ao encerrar sessao | ALTO |
| 7 | **Consolidacao diaria** logs → notas (scripts/consolidar_dia.py) | MEDIO |
| 8 | **Session memory via mensagens** do banco (registrar resumos como mensagens) | MEDIO |
| 9 | **Identidade dos agentes manuais** — SOUL.md para ChatGPT, Claude-Web, Gemini | MEDIO |
| 10 | **Busca unificada** — scripts/buscar_memoria.py transversal em todas fontes | MEDIO |

### Diagnostico Final

> "A Colmeia tem um sistema nervoso automatico (heartbeat) sem cortex (memoria cognitiva). O runner prova que os agentes estao vivos a cada 30 minutos, mas nenhum deles lembra o que estava fazendo."

---

# AGENTE 5: ESTRATEGISTA

## Perfil

```yaml
nome: ESTRATEGISTA
especialidade: Custos, tokens, viabilidade economica, sustentabilidade
perspectiva: O que custa, o que vale, o que escala — analise financeira para empreendedor solo
metodo: Comparacao de modelos de custo (API vs Account-First), projecoes, cenarios
achado_chave: "Economia de R$3.200-3.700/mes. O runner Python com custo zero e a maior vantagem competitiva."
```

## Analise Completa

### 1. Volume de Heartbeats

| Metrica | Banu | Colmeia v6 |
|---------|------|------------|
| Agentes automatizados | 10 | 4 |
| Intervalo | 15 min | 30 min |
| HBs/agente/dia | 96 | 48 |
| HBs totais/mes | 28.800 | 5.760 |
| **Tokens por HB** | **~500-2.000** | **ZERO** |

### 2. Custo Comparativo

**Banu (tudo API):**
- HBs idle: ~$0.0015/HB × 28.800 = $43/mes
- HBs com trabalho (30%): ~$0.02/HB × 8.640 = $173/mes
- Execucao de tarefas: $300-400/mes
- **Total: $700-800/mes (R$ 3.500-4.000)**

**Colmeia Account-First:**
- HBs: $0.00/mes (Python puro)
- Execucao: incluido no Pro ($20/mes)
- **Total: $20-40/mes (R$ 100-300)**

**Economia: 92-97%**

### 3. Trade-off Custo vs Inteligencia

| Capacidade | Com IA no HB | Sem IA (Python) | Impacto real |
|-----------|-------------|-----------------|-------------|
| Auto-atribuicao inteligente | Escolhe por afinidade | Pega maior prioridade | BAIXO |
| Contribuicao proativa | Opina em threads | Nunca contribui | MEDIO |
| Analise semantica urgencia | Entende nuance | Filtra por prioridade >= 8 | BAIXO |
| Sintese de feed | Resume atividades | Ignora feed | BAIXO |
| Deteccao conflitos | Percebe sobreposicao | Nao detecta | BAIXO |

**Veredicto:** Custo-beneficio favorece MASSIVAMENTE o runner Python para 4 agentes com operador humano.

### 4. Cenarios de Escalabilidade

| Cenario | Custo mensal |
|---------|-------------|
| Atual (4 agentes, Pro) | R$ 100-300 |
| 10 agentes, Pro | R$ 100-300 (nao muda — runner e gratis) |
| Hibrido (Pro + API pontual) | R$ 150-400 |
| Tudo API (como Banu) | R$ 3.500-4.000 |

### 5. Cascata de Decisao Proposta

```
Runner Python (gratis, deterministico, 24/7)
  → 95% dos heartbeats
  ↓ [Se detectar anomalia ou oportunidade]
Haiku 4.5 (barato, rapido, pontual)
  → 4% (~R$ 5-10/mes)
  ↓ [Se escalar complexidade]
Sessao Pro interativa (custo fixo)
  → 1%
```

### 6. Modelo de Custo por Agente

| Agente | Modelo recomendado | Heartbeat | Sessoes |
|--------|-------------------|-----------|---------|
| NEXO (coordenador) | Sonnet 4.5 | R$ 0 | ~5h/mes |
| ONIR (executor) | Opus 4.6 | R$ 0 | ~20h/mes |
| Sandman (documentador) | Sonnet 4.5 | R$ 0 | ~5h/mes |
| Helena (pesquisadora) | Opus 4.6 | R$ 0 | ~10h/mes |

### 7. Thresholds para Migrar Pro → API

| Sinal | Acao |
|-------|------|
| Rate limit batido >3x/semana | Upgrade para Max 5x ($100) |
| Max 5x limit batido | Considerar API batch |
| INTEIA monetizando | API obrigatoria |
| Custo API < Max 20x ($200) | Migrar para API |

### 8. TCO Real Estimado

| Item | Custo/mes |
|------|-----------|
| Claude Pro | R$ 100 |
| Eletricidade PC (parcial) | ~R$ 30-50 |
| Internet | R$ 0 (ja paga) |
| ChatGPT Plus (opcional) | R$ 100 |
| Gemini (opcional) | R$ 100 |
| **Total base** | **R$ 130-150** |
| **Total maximo** | **R$ 300** |

### 9. Top 10 Recomendacoes Estrategicas

1. **Manter runner Python** (economia R$ 3.200+/mes)
2. **Nao escalar para 10 agentes prematuramente** (atencao cognitiva > custo)
3. **Ficar no Claude Pro** (custo fixo previsivel)
4. **Implementar cascata Python → Haiku → Pro** (maximizar valor por real)
5. **Tracking de sessoes no banco** (visibilidade para P033)
6. **API Batch para tarefas de larga escala** (50% desconto)
7. **Politica Account-First como documento vivo** (revisao trimestral)
8. **Horario de silencio no scheduler** (02:00-06:00, reduzir I/O)
9. **Migrar Postgres so quando necessario** (SQLite suficiente)
10. **Documentar TCO real** (planejamento financeiro)

### Conclusao

> "A Colmeia v6 e economicamente sustentavel. O modelo hibrido (runner Python gratis + conta Pro fixa) e uma arquitetura superior para empreendedor solo. A decisao de nao colocar IA no heartbeat nao foi atalho — foi decisao arquitetural correta que gera economia de R$3.000+/mes."

---

## CONSENSO DOS 5 AGENTES

### Unanimidade (5/5):
- Runner sem IA = decisao correta para o estagio atual
- Daily notes = gap mais critico de memoria
- Sistema esta 83%+ implementado vs Banu
- Custo 92-97% menor que modelo Banu

### Maioria (4/5):
- WORKING.md precisa de zona preservada — FEITO
- Detail View no dashboard e gap #1 de UX
- Health check precisa ser robusto (nao raso)

### Split (3/2):
- Cascata Python→Haiku→Pro: ESTRATEGISTA e ARQUITETO a favor agora, DEVOPS e UX neutros, MEMORIA prefere daily notes primeiro

---

*Documento gerado por ONIR consolidando as 5 analises individuais — 2026-02-12*
