# Plano de Implantacao da Estrutura Colmeia

Versao: execucao continua (sem prazo fixo)  
Escopo: implantar a estrutura proposta nos materiais de `docs/estrutura-colmeia` dentro da realidade atual da Colmeia (`compartilhado/PROTOCOLO_v5.md`, 6 irmaos, memoria em camadas).

---

## 1. Objetivo Executivo

Transformar a Colmeia de um ecossistema com memoria e protocolos fortes para uma operacao multiagente com:

- coordenacao orientada a tarefas (kanban + threads)
- execucao autonoma com heartbeat escalonado
- notificacoes confiaveis entre agentes
- visibilidade diaria para decisao do Igor
- governanca de custo, seguranca e accountability

---

## 2. Principios de Implantacao

1. Escalar por maturidade, nao por entusiasmo.
2. Comecar com 3 agentes piloto antes de expandir para 6/10.
3. Se nao foi escrito, nao existe operacionalmente.
4. Modelos caros apenas para trabalho de alto valor.
5. Toda automacao deve gerar trilha de auditoria.
6. Politica de provedor: **conta Pro primeiro, API por excecao**.

---

## 3. Arquitetura-Alvo (adaptada para Colmeia)

1. Camada de orquestracao:
- Hub central (`Clawdbot`) coordenando tarefas e heartbeats.

2. Camada de colaboracao:
- Banco compartilhado para `agents`, `tasks`, `messages`, `activities`, `documents`, `notifications`.

3. Camada de identidade e memoria:
- `SOUL.md`, `AGENTS.md`, `HEARTBEAT.md`, `memory/WORKING.md`, daily logs, `MEMORY.md`.

4. Camada de supervisao:
- Dashboard minimo (feed + kanban + status de agentes + documentos).
- Standup diario automatico para o Igor.

5. Camada de execucao de modelos (provider layer):
- Modo A (preferencial): autenticacao por conta (`Claude Pro`, `ChatGPT Pro`, `Gemini`) via fluxos tipo OpenCode/OpenClaw.
- Modo B (contingencia): API key apenas quando o caso for inevitavel.

---

## 4. Roadmap por Maturidade (sem prazo)

## Fase 1 - Fundacao e Piloto

Objetivo: operar com 3 agentes de forma estavel.

Escopo:
- `Clawdbot` (lead)
- `ONIR`
- `Sandman`

Entregas:
- Documento canonico de arquitetura e governanca.
- Padrao unico de workspace operacional por agente.
- Backend compartilhado minimo em producao.
- Heartbeat 30 min escalonado com logs (reduzir para 15 min apenas apos estabilidade).

Definition of Done:
- 3 agentes com heartbeat rodando 7 dias seguidos.
- >=90% dos ciclos com saida valida (`trabalho` ou `HEARTBEAT_OK`).
- Fluxo completo funcionando: criar task -> atribuir -> comentar -> mover status.

## Fase 2 - Coordenacao e Observabilidade

Objetivo: fechar comunicacao assíncrona confiavel e visao executiva.

Escopo:
- manter 3 agentes estaveis
- integrar `ChatGPT` e `Gemini` no fluxo assíncrono

Entregas:
- Daemon de notificacoes com retry.
- Thread subscriptions automaticas.
- Dashboard operacional minimo.
- Standup diario automatizado.

Definition of Done:
- >=95% das mencoes entregues em ate 1 ciclo.
- Tempo medio de primeira resposta de task < 20 min.
- Standup entregue por 14 dias consecutivos.

## Fase 3 - Escala e Governanca

Objetivo: escalar para 6 agentes com controle de custo e risco.

Escopo:
- operar os 6 irmaos dentro da mesma disciplina de task/memoria
- preparar trilha para squad especializado de 10 papeis

Entregas:
- Politica de autonomia por nivel (`intern`, `specialist`, `lead`).
- Politica de roteamento de modelos por tipo de tarefa.
- Matriz de permissoes e auditoria por acao.
- Rotina mensal de revisao de memoria e protocolo.

Definition of Done:
- 6 agentes operando estavel por 14 dias.
- Custo mensal dentro do teto acordado.
- Sem acao externa critica sem log de auditoria.

---

## 5. RACI (macro)

Legenda: R = Responsible, A = Accountable, C = Consulted, I = Informed

| Frente | Igor | Clawdbot | Sandman | ONIR |
|---|---|---|---|---|
| Arquitetura e prioridade | A | R | C | C |
| Protocolos e guardrails | C | C | A/R | C |
| Orquestracao operacional | I | A/R | C | C |
| Curadoria de memoria | I | C | C | A/R |
| Qualidade de sintese/documentacao | I | C | C | A/R |
| Aprovacao de rollout | A | R | C | C |

---

## 6. KPIs de Operacao

1. Heartbeat success rate.
2. Tempo de primeira resposta por task.
3. Throughput semanal (tasks concluidas).
4. Taxa de bloqueios > 24h.
5. Custo por agente e por task.
6. Taxa de retrabalho em review.

---

## 7. Backlog da Proxima Semana

1. Consolidar schema final das 6 tabelas.
2. Padronizar arquivos operacionais dos 3 agentes piloto.
3. Ativar heartbeat escalonado com checklist unico.
4. Implementar fluxo minimo task/comentario/status.
5. Publicar 1o standup diario automatizado.

---

## 8. Riscos e Mitigacoes

1. Fragmentacao de contexto:
- Mitigacao: WORKING.md obrigatorio por ciclo + links para task ativa.

2. Custo explodindo:
- Mitigacao: roteamento de modelo por classe de tarefa + teto mensal.

3. Autonomia sem controle:
- Mitigacao: niveis de autonomia + auditoria de acoes externas.

4. Sobrecarga do Igor:
- Mitigacao: standup diario objetivo + backlog priorizado por impacto.

---

## 9. Criterios de Go/No-Go por Fase

Fase 1 -> Fase 2:
- estabilidade de heartbeat comprovada
- fluxo minimo de tarefas validado

Fase 2 -> Fase 3:
- notificacao confiavel + dashboard + standup estaveis

Fase 3 -> Escala 10 agentes:
- 6 agentes operando com qualidade e custo sob controle por pelo menos 1 ciclo completo (14 dias)

---

## 10. Proximo Passo Imediato

Executar o kickoff da Fase 1 por dependencias, em paralelo maximo:

1. Padronizacao de arquivos operacionais.
2. Backend compartilhado minimo.
3. Heartbeat em producao.
4. Fluxo de task ponta a ponta.
5. Revisao executiva + ajustes.

---

## 11. Plano Tatico do Piloto (nivel tarefa)

Escopo operacional: `Clawdbot` + `Sandman` + `ONIR`

| ID | Tarefa | Dono | Entregavel | Criterio de pronto |
|---|---|---|---|---|
| P001 | Criar estrutura de trabalho em `operacional/mission-control/` | Clawdbot | Pastas e arquivos base | Estrutura versionada no repo |
| P002 | Definir contrato de dados v0.1 (task/message/activity) | Sandman | `CONTRATO_DADOS.md` | Campos obrigatorios aprovados |
| P003 | Definir fluxo de status oficial | Sandman | Workflow documentado | Sem ambiguidades de transicao |
| P004 | Definir catalogo de eventos operacionais | ONIR | Lista de eventos | Cobertura total do ciclo de task |
| P005 | Criar template `SOUL_PILOTO.md` | Sandman | Template pronto | Identidade operacional clara |
| P006 | Criar template `AGENTS_PILOTO.md` | Sandman | Template pronto | Regras de operacao definidas |
| P007 | Criar template `HEARTBEAT_PILOTO.md` | Clawdbot | Checklist padrao | Passo-a-passo unico por ciclo |
| P008 | Criar template `WORKING_PILOTO.md` | ONIR | Template pronto | Current/Status/Next padronizados |
| P009 | Aplicar templates nos 3 agentes piloto | Clawdbot | Arquivos por agente | 100% aderente ao padrao |
| P010 | Provisionar backend compartilhado | Clawdbot | Ambiente ativo | CRUD basico responde |
| P011 | Implementar entidade `agents` + seed | Clawdbot | Schema e dados iniciais | 3 agentes cadastrados |
| P012 | Implementar entidade `tasks` | Clawdbot | Schema + operacoes | Create/assign/move funcionando |
| P013 | Implementar entidade `messages` | Clawdbot | Thread por task | Post/list funcionando |
| P014 | Implementar entidade `activities` | Clawdbot | Event log | Eventos gravados corretamente |
| P015 | Implementar entidade `notifications` | Clawdbot | Fila de notificacao | Campo `delivered` operacional |
| P016 | Criar CLI minima (`task:create`, `task:move`, `msg:post`) | Clawdbot | Scripts operacionais | Fluxo ponta a ponta via CLI |
| P017 | Implementar `heartbeat:run --agent <id>` | Clawdbot | Runner de heartbeat | Retorna `WORKED` ou `HEARTBEAT_OK` |
| P018 | Validar leitura obrigatoria de `WORKING.md` | Clawdbot | Regra no runner | Sem arquivo -> erro explicito |
| P019 | Implementar scanner de urgencia (`mentions/assigned`) | Clawdbot | Modulo de prioridade | Urgencias processadas primeiro |
| P020 | Implementar scanner de feed (`activities`) | Clawdbot | Modulo de contexto | Reacao a eventos relevantes |
| P021 | Persistir atualizacao de `WORKING.md` ao fim do ciclo | ONIR | Escrita automatica | Retomada correta no ciclo seguinte |
| P022 | Configurar agendamento escalonado (00/02/04) | Clawdbot | Cron ativo | Sem colisao entre agentes |
| P023 | Implementar daemon de notificacao (poll + retry) | Clawdbot | Servico de entrega | Retry funcional para agente off |
| P024 | Implementar inscricao automatica em thread | Clawdbot | Regras de subscription | Comentarios futuros chegam aos inscritos |
| P025 | Implementar logs estruturados por ciclo | ONIR | `logs/mission-control/*.jsonl` | Auditoria por execucao disponivel |
| P026 | Implementar standup diario (23:30) | ONIR | Script de compilacao | Resumo diario entregue |
| P027 | Definir politica de roteamento de modelos | Sandman | `POLITICA_MODELOS.md` | Conta Pro primeiro, API por excecao com justificativa |
| P028 | Definir politica de autonomia por nivel | Sandman | `POLITICA_AUTONOMIA.md` | Regras de acao externa claras |
| P029 | Criar teste A (task simples, 1 agente) | ONIR | Cenario automatizado | Passa sem intervencao manual |
| P030 | Criar teste B (task colaborativa, 3 agentes) | ONIR | Cenario automatizado | Handoff e thread funcionando |
| P031 | Criar teste C (agente dormindo + retry) | Clawdbot | Cenario automatizado | Notificacao entregue no ciclo seguinte |
| P032 | Executar soak test de estabilidade | Clawdbot | Relatorio de estabilidade | >=90% de sucesso no heartbeat |
| P033 | Ajustar gargalos de custo/token | Sandman | Afinacao de configuracao | Custo medio/ciclo reduzido |
| P034 | Encerrar aceite formal do piloto v0.1 | Igor | Ata de aceite | KPIs minimos atingidos |

### 11.1 KPIs minimos de aceite do piloto

1. Heartbeat success rate >= 90% em 48h.
2. Tempo medio da primeira resposta por task <= 20 min.
3. Entrega de notificacao >= 95% com retry.
4. Standup entregue diariamente por 7 dias.
5. Minimo de 5 tasks completas sem quebra de fluxo.

### 11.2 Ordem real de execucao

1. Bloco A - Fundacao: `P001` a `P009`.
2. Bloco B - Backend e CLI: `P010` a `P016`.
3. Bloco C - Heartbeat e notificacoes: `P017` a `P024`.
4. Bloco D - Observabilidade: `P025` a `P026`.
5. Bloco E - Governanca e validacao: `P027` a `P034`.

### 11.3 Regra de velocidade de execucao

1. Tudo que nao tem dependencia direta deve rodar em paralelo.
2. Gate unico por bloco: so avanca de bloco quando os criterios de pronto do bloco atual forem atendidos.
3. Prioridade maxima para automacao e remocao de gargalo humano.

---

## 12. Ajuste Estrategico Aprovado (Render + Vercel + Vibe Coding 100% IA)

Diretriz: **nao criar stack nova**. Estender a infraestrutura que ja esta em producao.

Status canonico:

1. Esta secao e a decisao vigente para producao da Colmeia.
2. Quando houver conflito com decisoes anteriores, prevalece esta secao para ambiente produtivo.
3. Arquitetura local (SQLite/localhost) permanece como fallback e ambiente de desenvolvimento.

### 12.1 Infraestrutura de referencia (oficial)

1. Frontend (Vercel):
- URL: `https://inteia.com.br`

2. Backend (Render):
- URL base: `https://api.inteia.com.br`
- Docs: `https://api.inteia.com.br/docs`

3. Banco:
- PostgreSQL do Render ja em uso pela API atual.

### 12.1.1 Contrato de URL publica (obrigatorio)

Restricao de produto:

1. A raiz atual de `https://inteia.com.br` nao pode ser alterada.
2. O modulo Colmeia deve viver em subrota dedicada no site.
3. A API da Colmeia deve viver em subrota dedicada no dominio de API.

URLs canonicas:

1. Frontend Colmeia: `https://inteia.com.br/colmeia`
2. API Colmeia: `https://api.inteia.com.br/colmeia`

Regra de compatibilidade:

1. Endpoints internos podem manter versao (`/api/v1/...`) no codigo.
2. Publicamente, deve existir roteamento para `https://api.inteia.com.br/colmeia/*`.
3. Se necessario, usar rewrite no gateway para mapear:
- `https://api.inteia.com.br/colmeia/*` -> rota interna versionada.

### 12.2 Decisao de arquitetura

1. Substituir a ideia de backend separado por **modulo Colmeia dentro da API existente**.
2. Reaproveitar autenticacao, deploy, observabilidade e banco ja operacionais.
3. Evitar novo provedor (ex: Supabase) para nao duplicar custo, stack e manutencao.

### 12.3 Mudancas no backlog (impacto direto)

1. `P010-P016` deixam de ser "projeto de backend novo".
2. `P010-P016` passam a ser "extensao do backend FastAPI existente".
3. Reducao de risco: menos infraestrutura nova, mais foco em dominio Colmeia.

### 12.4 Modelo de dados (schema Colmeia no PostgreSQL existente)

Tabelas alvo:

1. `colmeia_agents`
2. `colmeia_tasks`
3. `colmeia_messages`
4. `colmeia_activities`
5. `colmeia_notifications`
6. `colmeia_documents`

Regras minimas:

1. Todas com `id` UUID.
2. `created_at` e `updated_at` nas entidades transacionais.
3. Indices em campos de consulta frequente (`status`, `agente_id`, `task_id`, `created_at`).
4. Chaves estrangeiras entre tasks/messages/activities/documents/notifications.

### 12.5 Endpoints do modulo Colmeia (na API atual)

Prefixo publico obrigatorio: `/colmeia`

Prefixo interno permitido: `/api/v1/colmeia` (com rewrite)

Agentes:

1. `GET /colmeia/agents`
2. `GET /colmeia/agents/{id}`
3. `POST /colmeia/agents/{id}/heartbeat`
4. `PUT /colmeia/agents/{id}/status`

Tasks:

1. `GET /colmeia/tasks`
2. `POST /colmeia/tasks`
3. `GET /colmeia/tasks/{id}`
4. `PUT /colmeia/tasks/{id}`
5. `PUT /colmeia/tasks/{id}/status`
6. `PUT /colmeia/tasks/{id}/assign`

Messages:

1. `GET /colmeia/tasks/{id}/messages`
2. `POST /colmeia/tasks/{id}/messages`

Activities:

1. `GET /colmeia/activities`
2. `GET /colmeia/activities/agent/{id}`

Notifications:

1. `GET /colmeia/notifications/pending`
2. `POST /colmeia/notifications`
3. `PUT /colmeia/notifications/{id}/delivered`

Documents:

1. `GET /colmeia/tasks/{id}/documents`
2. `POST /colmeia/tasks/{id}/documents`

Dashboard:

1. `GET /colmeia/dashboard`
2. `GET /colmeia/standup`

### 12.6 Estrutura de codigo sugerida (seguir padrao do projeto existente)

Backend:

1. `backend/app/modelos/colmeia/`
2. `backend/app/schemas/colmeia/`
3. `backend/app/servicos/colmeia/`
4. `backend/app/api/rotas/colmeia/`

Registro de rotas:

1. incluir router Colmeia no agregador principal de rotas.

Migrations:

1. criar migration das 6 tabelas.
2. criar migration de indices.
3. aplicar migration no ambiente Render.

### 12.7 Fluxo de implementacao 100% IA (sem codificacao manual do Igor)

Modelo recomendado para reduzir retrabalho:

1. IA principal (Codex ou Claude Code) implementa ponta a ponta: modelos, migrations, schemas, servicos e rotas.
2. IA revisora (segunda IA) faz code review, testes de contrato e checklist de deploy.

Modelo alternativo (somente se necessario):

1. Divisao por multiplas IAs em paralelo, desde que exista contrato tecnico congelado antes da codificacao.

Gate de merge:

1. OpenAPI atualizada com rotas Colmeia.
2. Testes de contrato passando.
3. Migration aplicada sem quebrar tabelas existentes.
4. Healthcheck da API mantido.

### 12.8 Ajuste de heartbeat no piloto

1. Comecar com heartbeat de 30 minutos para controle de custo.
2. Reduzir para 15 minutos apenas apos estabilidade comprovada de KPI.
3. Manter regra de escalonamento para evitar pico simultaneo.

### 12.9 Disponibilidade de ONIR e Sandman no piloto

Como sao instancias sob demanda, operar em modo hibrido:

1. `Clawdbot` = always-on e responsavel por continuidade.
2. `ONIR` e `Sandman` = janelas operacionais definidas quando necessario.
3. Quando `ONIR`/`Sandman` estiverem offline, tasks seguem no fluxo com `Clawdbot` + fila.

### 12.10 Prompt-base para iniciar uma IA de codificacao no repositorio da API

```text
Objetivo: estender a API existente em https://api.inteia.com.br com o modulo Colmeia, sem criar projeto novo.

Infra existente:
- Frontend: https://inteia.com.br (Vercel)
- Backend: https://api.inteia.com.br (Render/FastAPI)
- Docs: https://api.inteia.com.br/docs
- Banco: PostgreSQL do Render ja em uso

Implementar no backend atual:
1) 6 entidades: colmeia_agents, colmeia_tasks, colmeia_messages, colmeia_activities, colmeia_notifications, colmeia_documents
2) rotas /api/v1/colmeia conforme contrato do plano
3) endpoint de heartbeat, status kanban, dashboard e standup
4) migrations e indices
5) testes de contrato e smoke test

Regras:
- seguir padroes ja existentes do projeto
- nao quebrar endpoints atuais
- nao criar stack nova
- entregar tudo pronto para deploy no Render
- manter frontend em `https://inteia.com.br/colmeia`
- manter API publica em `https://api.inteia.com.br/colmeia`
```

---

## 13. Politica de Provedores (Conta Pro primeiro, API por excecao)

Objetivo: minimizar uso de API paga e priorizar creditos de contas Pro, mantendo automacao.

### 13.1 Modos operacionais

1. Modo A - Account-first (padrao)
- Usar autenticacao de conta nos provedores (Claude/ChatGPT/Gemini), como em fluxos OpenCode/OpenClaw.
- Prioritario para triagem, heartbeat, classificacao e execucao assistida.

2. Modo B - API-exception (somente quando obrigatorio)
- Ativar API key apenas para partes sem alternativa tecnica viavel em conta autenticada.
- Toda excecao deve ser registrada com justificativa tecnica.

### 13.2 Regra de decisao para uso de API

API so e permitida quando TODOS os criterios abaixo forem verdadeiros:

1. Execucao precisa ser server-side sem sessao humana aberta.
2. Fluxo requer chamada programatica previsivel (webhook, worker, cron remoto, callback assincrono).
3. Nao existe adaptador confiavel via conta autenticada para esse caso.

Se qualquer criterio falhar, manter em Modo A.

### 13.3 Matriz de aplicacao inicial

1. Heartbeat de agentes:
- Preferencial: Modo A.
- API: evitar.

2. Geração de standup:
- Preferencial: Modo A.
- API: evitar.

3. Endpoints do backend Colmeia:
- Preferencial: sem chamadas LLM no request path.
- API: apenas se houver etapa de inferencia realmente obrigatoria.

4. Notificacoes e fila:
- Preferencial: logica deterministica sem LLM.
- API: nao obrigatoria.

### 13.4 Backlog adicional para account-first

1. P035 - Mapear no ambiente atual todos os fluxos que ja usam conta Pro (Claude, ChatGPT, Gemini).
2. P036 - Criar `POLITICA_PROVIDER_ACCOUNT_FIRST.md` com regras de excecao de API.
3. P037 - Implementar chave de feature flag: `USE_API=false` por padrao.
4. P038 - Instrumentar logs para medir quantas execucoes usaram conta vs API.
5. P039 - Criar runbook de degradacao: se API falhar, cair para modo conta.

### 13.5 Criterio de aceite da politica

1. No piloto, >=80% das execucoes de LLM devem rodar em Modo A (conta Pro).
2. Toda chamada API no piloto deve ter registro de justificativa.
3. Nenhum endpoint critico deve depender exclusivamente de API sem fallback.

---

## 14. Controles Criticos Ausentes (adicionados)

### 14.1 Rollback operacional

1. Criar migration de rollback para cada migration de schema Colmeia.
2. Fazer backup logico antes de aplicar migration em producao.
3. Em falha de deploy: rollback de app + rollback de migration + validacao de healthcheck.

### 14.2 Autenticacao e autorizacao

1. Endpoints `/colmeia/*` exigem autenticacao.
2. Adotar RBAC minimo:
- lead pode criar/atribuir/mover tasks
- specialist pode comentar/atualizar propria task
- leitura de dashboard por perfis autorizados
3. Registrar `agent_id` e trilha de auditoria em todas as mutacoes.

### 14.3 Seguranca de migration

1. Nunca aplicar migration nova sem backup previo.
2. Aplicar primeiro em ambiente de validacao/staging quando disponivel.
3. Rodar smoke tests obrigatorios pos-migration.

### 14.4 Artefatos normativos desta versao

1. `docs/CONTRATO_API_COLMEIA.md`
2. `docs/POLITICA_PROVIDER_ACCOUNT_FIRST.md`
3. `docs/RUNBOOK_ROLLBACK_COLMEIA.md`

---

## 15. Plano Final Consolidado

### 15.1 Estado atual

1. Arquitetura canonica definida para producao:
- `https://inteia.com.br/colmeia`
- `https://api.inteia.com.br/colmeia`
2. Politica provider definida:
- conta Pro primeiro
- API por excecao com justificativa
3. Contrato de API, rollback e controle de migration documentados.
4. Skills de operacao criadas e validadas.

### 15.2 Criterios de conclusao do plano

1. Bloco A a E executados com criterios de pronto atendidos.
2. KPIs minimos do piloto cumpridos.
3. Endpoints `/colmeia/*` autenticados e auditaveis.
4. Rollback testado em simulacao.
5. Relatorio de aceite assinado por Igor.

### 15.3 Ordem de execucao final

1. Executar Bloco A (`P001` a `P009`) e validar.
2. Executar Bloco B (`P010` a `P016`) com migration segura.
3. Executar Bloco C (`P017` a `P024`) com heartbeat inicial de 30 min.
4. Executar Bloco D (`P025` a `P026`) e validar dashboard/standup.
5. Executar Bloco E (`P027` a `P034`) e emitir aceite final.

### 15.4 Regra de governanca final

1. Sem decisao conflitante entre documentos.
2. Se houver conflito novo, `docs/PLANO_IMPLANTACAO_COLMEIA.md` prevalece para producao.
3. Decisoes legadas ficam como referencia historica/local fallback.
