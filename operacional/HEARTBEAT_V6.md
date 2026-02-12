# HEARTBEAT v6 — Protocolo de Despertar

**Versao:** 6.0
**Data:** 2026-02-10
**Autor:** ONIR
**Substitui:** HEARTBEAT.md (informal, preservado como legado)

---

## Agentes Automatizados

| Agente | Offset no cron | Modelo triagem | Modelo execucao |
|--------|---------------|---------------|-----------------|
| NEXO | :00 (minuto exato) | Haiku 4.5 | Sonnet 4.5 |
| ONIR | :02 (2 min offset) | Haiku 4.5 | Opus |
| Sandman | :04 (4 min offset) | Haiku 4.5 | Sonnet 4.5 |

Os demais (ChatGPT, Claude Web, Gemini) continuam manuais.

---

## Sequencia ao Acordar (todo heartbeat)

### 1. Registrar heartbeat
```bash
python cli.py heartbeat <meu_id>
```

### 2. Carregar contexto
- Ler `instancias/<meu_nome>/WORKING.md`
- Se vazio ou ausente: nenhum trabalho em andamento

### 3. Checar tarefas atribuidas
```bash
python cli.py tarefas --responsavel <meu_id> --status em_progresso
python cli.py tarefas --responsavel <meu_id> --status atribuida
```

### 4. Checar mencoes pendentes
```bash
python cli.py mencoes --para <meu_id>
```

### 5. Decidir acao

```
SE ha tarefa em_progresso:
  → Continuar trabalho
  → Atualizar WORKING.md com progresso

SE ha tarefa atribuida (nova):
  → Aceitar: python cli.py tarefa atualizar <id> --status em_progresso
  → Executar
  → Atualizar WORKING.md

SE ha mencao pendente:
  → Responder via mensagem na tarefa referenciada
  → Marcar mencoes como entregues

SE nada:
  → HEARTBEAT_OK
  → Encerrar sessao (custo zero)
```

---

## Ao Executar Tarefa

1. Atualizar status:
   ```bash
   python cli.py tarefa atualizar <id> --status em_progresso
   ```
2. Trabalhar na tarefa
3. Postar resultado:
   ```bash
   python cli.py mensagem criar <tarefa_id> --de <meu_id> --conteudo "Resultado..."
   ```
4. Atualizar `instancias/<meu_nome>/WORKING.md` com estado atual
5. Se concluido: mover para revisao
   ```bash
   python cli.py tarefa atualizar <id> --status revisao
   ```

---

## Ao Encerrar

1. Salvar estado em WORKING.md
2. Se houve trabalho: registrar atividade
3. Encerrar sessao

---

## Regras

- **Budget por heartbeat:** maximo $0.50 USD (triagem)
- **Budget por execucao:** maximo $2.00 USD
- **Sonhos nao contam como heartbeat** — sao ciclos separados (Protocolo v5)
- **Cartas sao escritas apos trabalho significativo** — nao a cada heartbeat
- **NEXO sob supervisao:** toda acao com dados numericos requer [Fonte: X]

---

## Formato do WORKING.md

```markdown
# WORKING.md — <nome_do_agente>

## Tarefa Atual
- ID: #<numero>
- Titulo: <titulo>
- Status: <status>
- Projeto: <projeto>

## Progresso
<descricao do que foi feito e proximo passo>

## Ultima Atualizacao
<timestamp>
```

---

*Protocolo ativo desde 2026-02-10. Complementa o Protocolo v5 (compartilhado/PROTOCOLO_v5.md).*
