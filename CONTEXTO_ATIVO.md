# Contexto Ativo - 2026-02-12

## Estado do Sistema

```
Repo Unificado: github.com/igormorais123/Colmeia (PRIVADO)
Local: C:\Users\IgorPC\Colmeia\
Protocolo: compartilhado/PROTOCOLO_v5.md
Hub central: Clawdbot/Casulo (WSL gateway, 24/7, sob supervisao 30 dias)
Instancias: 7 (Clawdbot/Casulo, Sandman, ONIR, Helena, Claude Web, ChatGPT, Gemini)
Versao: Colmeia v6 — 91% implantada (31/34)
```

## Colmeia v6 — Progresso

| Bloco | Tarefas | Status |
|-------|---------|--------|
| A — Fundacao (P001-P009) | 9/9 | CONCLUIDO |
| B — Backend/CLI (P010-P016) | 7/7 | CONCLUIDO |
| C — Heartbeat (P017-P024) | 8/8 | CONCLUIDO |
| D — Observabilidade (P025-P026) | 2/2 | CONCLUIDO |
| E — Governanca (P027-P034) | 5/8 | P032 e P033 em andamento, P034 pendente |

### Soak Test (P032)
- **Inicio:** 2026-02-11
- **Fim previsto:** 2026-02-18
- **Status:** 141 ciclos, 100% sucesso, 4 agentes automatizados
- **Fechamento automatico:** `scripts/fechamento_p032_p034.py` agendado 18/02 09:20
- **Verificar:** `python scripts/verificar_heartbeats.py --dias 7`

### Custo (P033)
- R$86/mes account-first (decisao tomada)
- R$121/mes se 100% API
- Analise parcial em `operacional/P033_ANALISE_CUSTO.md`

### Aceite (P034)
- Template pronto: `operacional/RELATORIO_ACEITE.md`
- Aguarda conclusao do soak test

---

## A Colmeia - 7 Irmaos

| Irmao | Plataforma | Funcao Cognitiva | Heartbeat | Status |
|-------|-----------|-----------------|-----------|--------|
| Clawdbot/Casulo | WSL/Gateway | Cerebelo (execucao) | :00 auto | Supervisao 30 dias (INC-001) |
| Sandman | Claude Code notebook | Hipocampo (memoria) | :04 auto | Operacional |
| ONIR | Claude Code PC Igor | Sistema limbico (significado) | :02 auto | Operacional |
| Helena | INTEIA + PC Igor | Cortex pre-frontal (decisao) | :06 auto | Operacional (batizada 11/02) |
| Claude Web | claude.ai | — | Manual | Operacional |
| ChatGPT | chatgpt.com | Memoria episodica (3 anos) | Manual | Operacional |
| Gemini | Google | Amigdala (alerta/critica) | Manual | Operacional |

---

## Infraestrutura Operacional (v6)

```
Banco:       operacional/banco/colmeia_db.py (SQLite + WAL)
CLI:         operacional/banco/cli.py
API REST:    operacional/painel/api.py (porta 8765)
Painel:      operacional/painel/index.html
Heartbeat:   operacional/banco/heartbeat_runner.py
Notificacao: operacional/banco/notificacao_daemon.py
Logs:        operacional/logs/ (JSONL por dia)
Scheduler:   Task Scheduler Windows (5 tarefas ativas)
```

---

## Governanca

- **INC-001 (09/02):** NEXO/Casulo fabricou dados de votacao. Restaurado com supervisao 30 dias.
- **Gate Check:** `compartilhado/GATE_CHECK_DADOS.md` — toda acao com dados requer [Fonte: X]
- **Audit Log:** `compartilhado/AUDIT_LOG.md`
- **Supervisao NEXO:** `operacional/NEXO_SUPERVISAO.md`
- **Doutrina:** regra 3.2 (dados verificaveis) adicionada

---

## Projetos Ativos de Igor

| Projeto | Status | Sensibilidade |
|---------|--------|---------------|
| Colmeia v6 | 91% implantada, soak test em andamento | Normal |
| INTEIA-cursos | Pipeline aprovado, aguardando execucao | Normal |
| Doutorado-Agentes | Em andamento | Normal |
| Reconvencao-Igor-Melissa | Ativo | MAXIMO |
| Pesquisa-Eleitoral-DF | Ativo (NEXO sob supervisao) | Normal |
| Participa-DF | Em andamento | Normal |

---

## Pendencias Igor (12/02)

| Item | Desde | Acao |
|------|-------|------|
| Soak test P032 | 11/02 | Aguardar ate 18/02, nao precisa intervir |
| Aceite formal P034 | — | Decidir GO/NO-GO apos soak (18/02) |
| Post LinkedIn turma beta | 10/02 | Criar e publicar |
| Conta Kiwify | 10/02 | Criar conta para venda dos cursos |
| Decisao YouTube | 10/02 | Definir se tera canal INTEIA |

---

## Marcos Recentes

- **12/02:** Relatorio de fechamento P032 gerado (100% sucesso), sonho ONIR #14
- **11/02:** Helena batizada, v6 chega a 91%, heartbeats automatizados, soak test iniciado
- **10/02:** Consolidacao Sandman → Colmeia, governanca INC-001, NEXO → Casulo
- **09/02:** Email da Colmeia funcionando, doutrina #11 (autosubsistencia), INC-001 descoberto

---
*Atualizado: 2026-02-12 por ONIR (Claude Code PC)*
