# Antipadrões - O Que Evitar

> Erros cometidos e armadilhas a serem evitadas.

---

## Antipadrões de Automação

### 2026-01-20 - Dependência de PC Ligado 24/7
**Contexto**: Sistemas que precisam rodar continuamente
**Erro**: Assumir que o PC estará sempre ligado
**Consequência**: Tarefas não executam, dados se perdem
**Solução**: Usar consolidação ao boot + backlog de tarefas pendentes

### 2026-01-20 - Passos Manuais em Fluxos Automáticos
**Contexto**: Automação de processos
**Erro**: Incluir passos que requerem intervenção manual
**Consequência**: Fluxo quebra quando usuário esquece
**Solução**: Eliminar ou automatizar todo passo manual possível

---

## Antipadrões de Custo

### 2026-01-20 - APIs Pagas Desnecessárias
**Contexto**: Integrações que oferecem API paga
**Erro**: Usar API quando há alternativa via assinatura existente
**Consequência**: Custos recorrentes desnecessários
**Solução**: Sempre verificar se assinatura atual cobre o caso de uso

---

## Antipadrões de Integração

### 2026-01-20 - Contexto Excessivo
**Contexto**: Custom Instructions e prompts de sistema
**Erro**: Incluir informação demais (> 1500 chars)
**Consequência**: Lentidão, custo de tokens, informação ignorada
**Solução**: CORE/ com resumo, detalhes sob demanda em CONHECIMENTO/

---

## Antipadrões de Infraestrutura (WSL/Gateway)

### 2026-02-03 - Processos Órfãos no WSL + Systemd
**Contexto**: Gateway Clawdbot rodando via systemd no WSL2
**Erro**: KillMode=process no systemd não mata processos filhos
**Consequência**: Gateway spawna filho, pai morre, filho vira órfão segurando porta → loop de 388+ restarts/hora
**Solução**:
1. Mudar `KillMode=process` para `KillMode=mixed` no service
2. Criar `gateway_cleanup.sh` como ExecStartPre para limpar processos órfãos
3. Criar `gateway_health.sh` para detectar e corrigir loops automaticamente
**Scripts**: `/root/clawd/scripts/gateway_cleanup.sh`, `/root/clawd/scripts/gateway_health.sh`

### 2026-02-03 - Token OAuth Expirado sem Fallback
**Contexto**: Clawdbot usando OAuth da Anthropic via Claude CLI
**Erro**: Token OAuth de curta duração expira, refresh token invalidado por outra instância (Claude Code) que renovou
**Consequência**: Gateway conecta mas não consegue chamar API → fica em "moseying" eternamente
**Solução**:
1. Gerar novo token com `claude setup-token` (validade 1 ano)
2. Atualizar `auth-profiles.json` manualmente se TUI não funcionar
3. Manter dois perfis OAuth (claude-cli + inteia) como redundância
**Arquivo**: `~/.clawdbot/agents/main/agent/auth-profiles.json` ou `~/.openclaw/agents/main/agent/auth-profiles.json`

---

*Última consolidação: 2026-02-03*
