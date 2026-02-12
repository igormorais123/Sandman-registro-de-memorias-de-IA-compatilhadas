# Fluxo de Tarefas — Colmeia v6 (Kanban)

**Versao:** 1.0
**Data:** 2026-02-10

---

## Estados

```
CAIXA_ENTRADA --> ATRIBUIDA --> EM_PROGRESSO --> REVISAO --> CONCLUIDA
                                     |
                                     v
                                 BLOQUEADA
                                     |
                                     v
                              EM_PROGRESSO (desbloqueada)

Estado terminal alternativo: CANCELADA
```

| Status | Significado | Quem muda |
|--------|-----------|-----------|
| caixa_entrada | Tarefa criada, sem dono | Igor ou qualquer agente |
| atribuida | Tem responsavel, aguardando proximo heartbeat | Igor, NEXO (coordenador) |
| em_progresso | Agente trabalhando ativamente | Agente responsavel |
| bloqueada | Dependencia externa ou duvida | Agente (com motivo) |
| revisao | Entrega pronta, aguardando aprovacao | Agente ao concluir |
| concluida | Aprovada pelo Igor | Igor |
| cancelada | Nao sera mais feita | Igor |

---

## Prioridades (1-10)

| Faixa | Significado | Compatibilidade Fitness |
|-------|-----------|------------------------|
| 9-10 | Urgente (Melissa, judicial, prazo hoje) | F:9-10 (sabedoria) |
| 7-8 | Alta (cursos, entregas da semana) | F:7-8 (consolidado) |
| 5-6 | Normal (desenvolvimento, melhorias) | F:5-6 (ativo) |
| 3-4 | Baixa (nice-to-have, exploracao) | F:3-4 (declinando) |
| 1-2 | Backlog (quando der) | F:1-2 (arquivo) |

---

## Comandos Rapidos

### Criar tarefa
```bash
python cli.py tarefa criar "Titulo" --projeto INTEIA-cursos --prioridade 8 --responsavel onir
```

### Ver todas em progresso
```bash
python cli.py tarefas --status em_progresso
```

### Ver tarefas de um agente
```bash
python cli.py tarefas --responsavel onir
```

### Ver detalhes + mensagens
```bash
python cli.py tarefa ver 42
```

### Fluxo completo de uma tarefa
```bash
# 1. Criar
python cli.py tarefa criar "Pesquisar artigos sobre masking autista" --projeto reconvencao --prioridade 9 --criado-por igor

# 2. Atribuir
python cli.py tarefa atribuir 1 --responsavel onir

# 3. Agente aceita e trabalha
python cli.py tarefa atualizar 1 --status em_progresso

# 4. Agente posta resultado
python cli.py mensagem criar 1 --de onir --conteudo "5 artigos encontrados: Cage 2019, Evans 2024..."

# 5. Agente move para revisao
python cli.py tarefa atualizar 1 --status revisao

# 6. Igor aprova
python cli.py tarefa atualizar 1 --status concluida
```

### Standup
```bash
python cli.py standup           # hoje
python cli.py standup 2026-02-10  # data especifica
```

---

## Projetos Ativos (para tag --projeto)

| Projeto | Descricao |
|---------|-----------|
| pesquisa-eleitoral | Pesquisa eleitoral DF (producao) |
| reconvencao | Caso judicial Igor/Melissa (SENSIVEL) |
| INTEIA-cursos | Plataforma de cursos IA |
| brislin | Backend traducao transcultural |
| colmeia-v6 | Evolucao da propria Colmeia |
| doutorado | Pesquisa academica Igor |

---

*Documentacao operacional. Complementa o Protocolo v5.*
