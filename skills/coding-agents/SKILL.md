---
name: coding-agents
description: Controlar Claude Code, OpenCode e Codex CLI no PC do Igor. Usar quando Igor pedir para programar, monitorar terminais de coding agents, mandar tarefas de código, continuar trabalho em projetos, ou verificar progresso de agentes rodando.
---

# Coding Agents — Controle Remoto

Controlar Claude Code, OpenCode e Codex CLI como sub-agentes de programação.

## Agentes Disponíveis

| Agente | Comando | Auth | Modelo |
|--------|---------|------|--------|
| **Claude Code** | `claude` | OAuth (plano Max 20x) | claude-opus-4-5 |
| **OpenCode** | `opencode run` | Herda do Claude Code | configurável |
| **Codex CLI** | `codex exec` | OAuth (conta Team) | gpt-5.2-codex |

## Projetos do Igor

| Projeto | Path | Descrição |
|---------|------|-----------|
| pesquisa-eleitoral-df | `/mnt/c/Agentes` | Full-stack Next.js + FastAPI |
| opencode-academy | `/mnt/c/Users/IgorPC/opencode-academy` | Curso interativo |
| clawd (workspace) | `/root/clawd` | Meu workspace |
| sandman (colmeia) | `/root/clawd/sandman` | Repo da Colmeia |

## Padrão: Tarefa Rápida (one-shot)

```bash
# Claude Code — print mode (não interativo)
exec pty:true command:"claude -p 'TAREFA AQUI'" workdir:/mnt/c/Agentes

# Codex CLI — exec mode
exec pty:true command:"codex exec 'TAREFA AQUI'" workdir:/mnt/c/Agentes

# OpenCode — run mode
exec pty:true command:"opencode run 'TAREFA AQUI'" workdir:/mnt/c/Agentes
```

## Padrão: Tarefa Longa (background + monitoramento)

```bash
# 1. Iniciar em background
exec pty:true background:true command:"claude -p 'TAREFA LONGA'" workdir:/mnt/c/Agentes

# 2. Monitorar
process action:log sessionId:XXX
process action:poll sessionId:XXX

# 3. Se precisar enviar input
process action:submit sessionId:XXX data:"yes"

# 4. Matar se necessário
process action:kill sessionId:XXX
```

## Padrão: Modo Interativo (PTY obrigatório)

Para sessões que precisam de input interativo:

```bash
# Claude Code interativo
exec pty:true background:true command:"claude" workdir:/mnt/c/Agentes

# Enviar comandos via send-keys
process action:submit sessionId:XXX data:"/compact"
process action:submit sessionId:XXX data:"Corrigir o bug no login"
```

## Regras

1. **SEMPRE usar pty:true** — agents são apps de terminal interativo
2. **SEMPRE usar workdir** — apontar pro projeto correto
3. **NUNCA rodar em /root/clawd/** — agent vai ler meus arquivos pessoais
4. **Codex precisa de git repo** — se for scratch: `mktemp -d && git init`
5. **Reportar progresso** — mandar update quando milestone ou erro
6. **Claude Code -p** — modo print (não interativo), sai sozinho
7. **Claude Code sem -p** — modo interativo, precisa de input

## Auto-notificação

Para tarefas longas, incluir wake no final do prompt:

```
... sua tarefa aqui.

Quando terminar, execute: openclaw gateway wake --text "Done: [resumo]" --mode now
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Claude Code trava | Verificar auth: `cat ~/.claude/.credentials.json` |
| Codex recusa rodar | Precisa estar em git repo |
| OpenCode sem auth | Herda do Claude Code ou precisa `opencode auth login` |
| Timeout | Usar background:true + monitorar com process:log |
| Output quebrado | Faltou pty:true |
