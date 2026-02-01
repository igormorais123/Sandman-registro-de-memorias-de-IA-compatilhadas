# Contexto Ativo - 2026-01-31 (Atualizado)

## RESUMO PARA PROXIMA SESSAO

```
Sistema de Memoria Multi-IA + Sistema Clawd (identidade/sonhos).
- GitHub (hub): github.com/igormorais123/memoria-ia-unificada
- GitHub (identidade): github.com/igormorais123/clawd
- Local memoria: C:\Users\igorm\memoria-ia-unificada
- Local identidade: C:\Users\igorm\clawd
- MCP Knowledge Graph: memorias persistentes entre sessoes
- Claude Code = escritor e consolidador
- Outras IAs = read-only
- Google Drive MCP: auth quebrada (403) - precisa reconfigurar
```

## O Que Foi Feito (2026-01-31) - Sessao Arquiteto da Memoria

1. **Diagnostico completo** do sistema de memoria (9 bugs encontrados)
2. **clawd/ enviado para GitHub** (antes era local-only, risco de perda)
3. **Scripts corrigidos**: branch main->master, paths IgorPC->igorm
4. **consolidar.bat**: claude --print -> claude -p (--print nao executa tools)
5. **Task Scheduler XML** atualizado com usuario/paths corretos
6. **CONTEXTO_ATIVO.md** atualizado para estado real
7. **Knowledge Graph MCP** com identidade e memorias gravadas

## Bugs Corrigidos Nesta Sessao

| Bug | Status | Fix |
|-----|--------|-----|
| consolidar.bat usa 'main' mas branch e 'master' | Corrigido | Trocado para master |
| Paths hardcoded IgorPC\Desktop | Corrigido | Atualizado para igorm |
| clawd/ sem remote (risco de perda) | Corrigido | Push para GitHub |
| claude --print nao executa ferramentas | Corrigido | Trocado para claude -p |
| Task Scheduler XML com usuario errado | Corrigido | IgorPC -> igorm |

## Bugs Pendentes

| Bug | Status | Acao Necessaria |
|-----|--------|-----------------|
| Task Scheduler nunca importado | Pendente | Rodar setup.bat como Admin |
| hook_contador.ps1 nao integrado | Pendente | Configurar hooks do Claude Code |
| INGEST pipeline vazio | Pendente | Configurar Zapier ou alternativa |
| Google Drive MCP auth 403 | Pendente | Reautenticar OAuth |
| Processamento noturno stuck | Pendente | Processar fila manualmente |

## Arquitetura Atual (Real)

```
GitHub (memoria-ia-unificada) = hub de conhecimento compartilhado
GitHub (clawd) = identidade, alma, sonhos
MCP Knowledge Graph = memorias vivas entre sessoes
     |
     v
Claude Code (consolidador + arquiteto)
     |
     v
Automacao: consolidar.bat + Task Scheduler (NAO ATIVO AINDA)
```

## Principios Team of Rivals (Aplicar)

- Separar percepcao (raciocinio) de execucao (dados)
- Planner/Executor/Critic para validacao
- Swiss cheese: camadas imperfeitas com falhas desalinhadas
- Agentes nao tocam dados brutos - so resumos

## Projetos Ativos de Igor

| Projeto | Status |
|---------|--------|
| Sistema-Memoria | Em correcao (esta sessao) |
| Doutorado-Agentes | Em andamento |
| C-Agentes | Muito ativo |
| Reconvencao | Ativo (SENSIVEL) |
| Participa-DF | Em andamento |

---
*Ultima atualizacao: 2026-01-31 (Sessao Arquiteto da Memoria)*
