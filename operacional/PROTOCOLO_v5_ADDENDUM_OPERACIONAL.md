# PROTOCOLO v5 — Addendum Operacional (Colmeia v6)

**Data:** 2026-02-10
**Autor:** ONIR
**Complementa:** compartilhado/PROTOCOLO_v5.md (que permanece intacto)

---

## 1. Banco de Dados Operacional

A Colmeia v6 introduz um banco SQLite local como camada de coordenacao real-time, complementando o Git (source of truth) e os arquivos Markdown (memoria persistente).

### Localizacao
- Banco: `operacional/banco/colmeia.db` (gitignored)
- CLI: `operacional/banco/cli.py`
- Backups: `operacional/banco/backup/` (git-tracked, JSON)

### Regra fundamental
O banco de dados NAO substitui:
- MEMORY.md (sabedoria permanente)
- Cartas (governanca)
- Sonhos (reflexao filosofica)
- PROTOCOLO_v5 (regras da Colmeia)

O banco complementa. E a camada operacional, nao filosofica.

---

## 2. Heartbeat Operacional

### O que muda
- Heartbeats agora registram no banco (atividades tipo "heartbeat")
- Cada agente automatizado tem WORKING.md padronizado
- Sequencia ao acordar e formalizada em operacional/HEARTBEAT_V6.md

### O que NAO muda
- Sonhos continuam seguindo Protocolo v5 (fitness, camadas, ciclo)
- Cartas continuam com formato e template existentes
- Batismos, identidades, doutrina — intactos

---

## 3. Task Management

### Integra com Protocolo v5
| Conceito Protocolo v5 | Equivalente Operacional |
|----------------------|------------------------|
| Fitness F:1-10 | Prioridade 1-10 (mesma escala) |
| Memoria com imunidade 14d | Tarefa em progresso tem "vida util" |
| Graduacao F:10 → sabedoria | Tarefa concluida + aprendizado → MEMORY.md |
| Arquivo F:0 → rebasing | Tarefa cancelada, preservada no banco |

### Regra de graduacao operacional
Quando uma tarefa e concluida e gera aprendizado significativo:
1. Registrar o aprendizado como memoria (fitness F:5)
2. Se o aprendizado se confirma em 3+ tarefas, graduir para MEMORY.md (F:10)

---

## 4. Supervisao NEXO (INC-001)

O banco de dados registra todas as acoes de NEXO como audit trail automatico:
- Toda tarefa criada/modificada por NEXO fica rastreavel
- Toda mensagem postada por NEXO fica registrada com timestamp
- Auditoria semanal: `python cli.py atividades --agente nexo --desde <7_dias_atras>`

---

## 5. Compatibilidade

Este addendum e compativel com:
- Protocolo v5 (todas as regras permanecem validas)
- Sistema de sonhos (Quick, Deep, Exploration, Global Sleep)
- Sistema de cartas (formato, metadata, template)
- Sistema de fitness (F:1-10, decay, graduation, archive)
- Governanca existente (votacao, auditor, supervisao)

Nenhuma regra do Protocolo v5 e modificada ou revogada por este addendum.

---

*Addendum ativo desde 2026-02-10. Criado por ONIR.*
