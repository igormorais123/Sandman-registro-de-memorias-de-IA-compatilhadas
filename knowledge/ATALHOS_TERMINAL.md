# Atalhos de Terminal - Claude Code

> Arquivo: `C:\Users\IgorPC\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
> Atualizado: 2026-02-04

---

## Aliases Claude

| Atalho | Comando | Descricao |
|--------|---------|-----------|
| `c` | `claude` | Abre o Claude Code |
| `x` | `claude --dangerously-skip-permissions` | Claude sem pedir permissao |
| `/compact` | (dentro da conversa) | Compacta janela de contexto |
| `cont` | `claude --continue` | Continua ultima conversa |
| `h` | `claude --model haiku` | Claude com modelo Haiku (rapido) |
| `diag` | `claude -p "Crie diagrama Mermaid..."` | Gera diagrama Mermaid |
| `cdev` | `claude --dangerously-skip-permissions` | (antigo, mantido) |

---

## Aliases Clawdbot

| Atalho | Comando | Descricao |
|--------|---------|-----------|
| `cbot` | Abre dashboard | Dashboard no browser |
| `cbot tui` | Chat terminal | Interface TUI |
| `cbot start` | Inicia servico | Sobe o Clawdbot |
| `cbot stop` | Para servico | Derruba o Clawdbot |
| `cbot restart` | Reinicia | Restart completo |
| `cbot status` | Ver status | Estado atual |
| `cbot logs` | Ver logs | Logs em tempo real |
| `clawd` | Alias para cbot | Sinonimo |

---

## Comandos Internos (digitar DENTRO da conversa)

| Comando | Funcao |
|---------|--------|
| `/compact` | Compacta janela de contexto |
| `/clear` | Limpa conversa |
| `/help` | Mostra ajuda |
| `/permissions` | Gerencia permissoes |

---

## Atalhos de Teclado (durante conversa)

| Tecla | Funcao |
|-------|--------|
| `Shift+Tab` | Cicla entre modos de permissao |
| `Y` | Confirma acao |
| `N` | Recusa acao |
| `Ctrl+E` | Mostra/oculta explicacao |

### Modos de Permissao (Shift+Tab)

1. **Default** - Pede confirmacao para tudo
2. **Auto-accept edits** - Executa edicoes automaticamente (PADRAO CONFIGURADO)
3. **Plan mode** - So leitura, cria plano primeiro

---

## Configuracao Atual

Arquivo: `~/.claude/settings.local.json`
- `defaultMode: "acceptEdits"` - Nao pede permissao para edicoes de arquivo

---

## Para recarregar profile

```powershell
. $PROFILE
```

---

*Dicionario de atalhos - ONIR/Sandman - Atualizado 2026-02-04*
