# Manual Colmeia Atual (v6 operacional)

Data de referencia: 12/02/2026  
Escopo: estado real da Colmeia no repositorio local.

---

## 1. O que e a Colmeia hoje

A Colmeia atual e um sistema multiagente operacional com:

1. Orquestracao de tarefas em banco local (SQLite/WAL).
2. Heartbeat automatico escalonado por agente.
3. Fila de notificacoes com retry/backoff.
4. Dashboard/API local para monitoramento e operacao.
5. Logs estruturados para auditoria e fechamento de aceite.

Status atual do plano:

1. 31/34 tarefas concluidas (91%).
2. `P032` (soak 7 dias) em andamento.
3. `P033` e `P034` pendentes de fechamento final.

Fonte oficial de status: `operacional/CHECKLIST_EXECUCAO.md`.

---

## 2. O que a Colmeia faz

Funcoes principais em producao local:

1. Gerenciar agentes, tarefas, mensagens, atividades, documentos e notificacoes.
2. Executar ciclo autonomo por agente:
   carregar contexto, checar tarefas, processar mencoes, registrar progresso.
3. Priorizar urgencias por scanner (`mentions`, atribuicoes, prioridades).
4. Publicar feed de atividades e standup diario.
5. Medir saude do sistema via logs e KPI de heartbeat.

Nao faz ainda (como canonico publico):

1. Rotas publicas definitivas em `https://inteia.com.br/colmeia`.
2. API publica definitiva em `https://api.inteia.com.br/colmeia` com auth/RBAC comprovado.

---

## 3. Arquitetura atual

Camadas:

1. Operacao: `operacional/`
2. Banco e regras: `operacional/banco/`
3. API/dashboard: `operacional/painel/`
4. Automacoes: `scripts/`
5. Instancias de agentes: `instancias/`

Banco de dados:

1. Arquivo: `operacional/banco/colmeia.db`
2. Schema: `operacional/banco/schema.sql`
3. Tabelas principais:
   `agentes`, `tarefas`, `mensagens`, `atividades`, `documentos`, `notificacoes`, `subscriptions_tarefa`

API local:

1. Arquivo: `operacional/painel/api.py`
2. Start: `operacional/painel/start_painel.bat`
3. URL local: `http://localhost:8765`

---

## 4. Agentes e papeis

Registro oficial: `operacional/AGENTS.md`

Automatizados (heartbeat):

1. `nexo` (lead) offset `:00`
2. `onir` offset `:02`
3. `sandman` offset `:04`
4. `helena` offset `:06`

Manuais:

1. `chatgpt`
2. `claude-web` (Vigilia)
3. `gemini`

Politica de modelos:

1. Triagem: Haiku 4.5
2. Execucao: Sonnet/Opus por perfil
3. Regra global: conta Pro primeiro, API por excecao

Referencia: `docs/POLITICA_PROVIDER_ACCOUNT_FIRST.md`.

---

## 5. Operacao diaria (resumo pratico)

### 5.1 Iniciar painel

1. Rodar `operacional/painel/start_painel.bat`
2. Abrir `http://localhost:8765`

### 5.2 Comandos CLI principais

Arquivo: `operacional/banco/cli.py`

1. Listar agentes:
   `python operacional/banco/cli.py agentes`
2. Listar tarefas:
   `python operacional/banco/cli.py tarefas --status em_progresso`
3. Criar tarefa:
   `python operacional/banco/cli.py tarefa criar "Titulo" --responsavel nexo --criado-por igor --prioridade 8 --projeto colmeia-v6`
4. Postar mensagem:
   `python operacional/banco/cli.py mensagem criar 10 --de onir --conteudo "Atualizacao" --mencoes sandman`
5. Processar fila de notificacoes:
   `python operacional/banco/cli.py notificacoes processar --modo online`
6. Standup:
   `python operacional/banco/cli.py standup`

### 5.3 Runner de heartbeat manual

1. `python operacional/banco/heartbeat_runner.py nexo`
2. `python operacional/banco/heartbeat_runner.py onir`

Referencia operacional: `operacional/HEARTBEAT_V6.md`.

---

## 6. Automacoes agendadas

Setup:

1. `scripts/setup_heartbeat_scheduler.bat`
2. `scripts/setup_heartbeat_scheduler.ps1`

Tarefas esperadas no Windows Scheduler:

1. `Colmeia_HB_NEXO`
2. `Colmeia_HB_ONIR`
3. `Colmeia_HB_SANDMAN`
4. `Colmeia_HB_HELENA`
5. `Colmeia_Notificacao_Daemon`

Lembrete de fechamento:

1. `Colmeia_Lembrete_Fechamento_P032`
2. Primeira execucao prevista: 18/02/2026 09:20
3. Script disparado: `scripts/fechamento_p032_p034.py`

---

## 7. Endpoints API atuais

Arquivo: `operacional/painel/api.py`

Endpoints principais:

1. `GET /api/health`
2. `GET /api/agentes`
3. `GET /api/tarefas`
4. `POST /api/tarefas`
5. `PUT /api/tarefas/{id}/status`
6. `PUT /api/tarefas/{id}/assign`
7. `POST /api/tarefas/{id}/mensagens`
8. `GET /api/atividades`
9. `GET /api/notificacoes/{agente_id}`
10. `POST /api/notificacoes/processar`
11. `GET /api/subscriptions`
12. `GET /api/scanner/{agente_id}`
13. `GET /api/dashboard`
14. `GET /api/standup`
15. `GET /api/soak-test`

---

## 8. Logs, auditoria e qualidade

Logs:

1. Heartbeat: `operacional/logs/heartbeat_YYYY-MM-DD.jsonl`
2. Notificacoes: `operacional/logs/notificacao_YYYY-MM-DD.jsonl`

Relatorios:

1. Auditoria operacional: `operacional/AUDITORIA_FISCAL_PLANO.md`
2. Progresso de fase: `operacional/PROGRESSO_FASE1.md`
3. Analise de custo parcial: `operacional/P033_ANALISE_CUSTO.md`
4. Relatorio de aceite: `operacional/RELATORIO_ACEITE.md`

KPIs de saude:

1. `python scripts/verificar_heartbeats.py --dias 1`
2. `python scripts/verificar_heartbeats.py --dias 7`

---

## 9. Skills da Colmeia (uso atual)

Guia oficial: `docs/GUIA_USO_SKILLS_COLMEIA.md`

Skills custom da Colmeia:

1. `colmeia-doc-map-mermaid`
   - mapear docs e gerar Mermaid
2. `colmeia-render-vercel-delivery`
   - preparar entrega em Render/Vercel e `/colmeia`
3. `colmeia-agentes-research`
   - pesquisar `C:\Agentes`, consultar Helena, analise quanti/quali

Skills adicionais presentes no repositorio:

1. `memoria-persistente-sono-rem`
2. `gestao_projetos_longo_prazo.md`

Acionamento tipico por prompt:

1. `Use $colmeia-doc-map-mermaid ...`
2. `Use $colmeia-render-vercel-delivery ...`
3. `Use $colmeia-agentes-research ...`

---

## 10. Fechamento do ciclo atual (P032-P034)

Objetivo:

1. Encerrar soak de 7 dias.
2. Fechar custo real.
3. Fechar aceite formal.

Comando unico de fechamento:

1. `python scripts/fechamento_p032_p034.py`

O que ele roda:

1. `python scripts/verificar_heartbeats.py --dias 7`
2. `python scripts/analise_custo_p033.py --dias 7`
3. `python scripts/gerar_relatorio_aceite.py --dias 7`

Saida:

1. `operacional/FECHAMENTO_P032_P034_YYYY-MM-DD.md`

Depois:

1. Abrir `operacional/RELATORIO_ACEITE.md`
2. Marcar decisao: GO / GO COM RESSALVAS / NO-GO
3. Assinar.

---

## 11. Limites e pendencias estrategicas

Pendencias tecnicas principais:

1. Validar implantacao canonica publica (`/colmeia`) em Render/Vercel.
2. Comprovar auth/RBAC em rota publica final.
3. Consolidar P033/P034 apos fim do soak.

Risco principal:

1. Divergencia entre piloto local estavel e ambiente publico ainda nao homologado.

---

## 12. Arquivos de referencia rapida

1. `operacional/CHECKLIST_EXECUCAO.md`
2. `operacional/AGENTS.md`
3. `operacional/HEARTBEAT_V6.md`
4. `operacional/painel/api.py`
5. `operacional/banco/cli.py`
6. `docs/PLANO_IMPLANTACAO_COLMEIA.md`
7. `docs/POLITICA_PROVIDER_ACCOUNT_FIRST.md`
8. `docs/RUNBOOK_ROLLBACK_COLMEIA.md`
9. `docs/GUIA_USO_SKILLS_COLMEIA.md`
