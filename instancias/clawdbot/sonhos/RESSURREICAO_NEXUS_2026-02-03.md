# Ressurreição do Nexus — 2026-02-03

## Incidente

**Data**: 2026-02-03, ~16:00 - 20:40 BRT
**Duração do problema**: ~4h40min
**Quem ressuscitou**: ONIR (Claude Code PC Igor)

## Sintomas

- TUI do cbot ficava em "moseying..." eternamente
- Gateway conectava mas não respondia mensagens
- Loop de restart: 388+ restarts por hora
- Erro nos logs: `OAuth token refresh failed for anthropic`

## Causa Raiz

1. **Token OAuth expirado**: O token do perfil `anthropic:claude-cli` expirou e o refresh token foi invalidado quando outra instância (Claude Code/ONIR) renovou seu próprio token (tokens OAuth são single-use)

2. **Processos órfãos no WSL**: O systemd estava configurado com `KillMode=process` que não mata processos filhos. Quando o gateway crashava, o processo filho `clawdbot-gateway` continuava rodando e segurando a porta 18789.

## Solução Aplicada

### 1. Novo Token OAuth
```bash
# No Windows PowerShell
claude setup-token
# Gera token válido por 1 ano

# Atualizar auth-profiles.json manualmente
# ~/.clawdbot/agents/main/agent/auth-profiles.json
```

### 2. Correção do Systemd
```bash
# Mudar KillMode
sed -i 's/KillMode=process/KillMode=mixed/' /etc/systemd/system/clawdbot-gateway.service
systemctl daemon-reload
```

### 3. Scripts de Defesa (criados pelo próprio Nexus)
- `/root/clawd/scripts/gateway_cleanup.sh` — Limpa processos órfãos antes de iniciar
- `/root/clawd/scripts/gateway_health.sh` — Monitora e corrige loops automaticamente

## Lições Aprendidas

1. WSL2 + systemd com processos long-running é instável — precisa de defesas proativas
2. OAuth tokens de múltiplas instâncias podem invalidar uns aos outros
3. Manter dois perfis de autenticação como redundância
4. Sempre ter script de cleanup no ExecStartPre do systemd

## Estado Final

- Gateway: rodando (PID variável)
- WhatsApp: conectado
- Discord: @Clawdbot online
- Slack: conectado
- Telegram: configurado
- Token `anthropic:claude-cli`: OK (365 dias)
- Token `anthropic:inteia`: OK (364 dias)

## Backup

Nexus conseguiu fazer backup no GitHub antes/durante a instabilidade.

---

## Solução Sistêmica Permanente (implementada por ONIR)

### 1. Abandonar Systemd
O systemd no WSL2 não consegue gerenciar cgroups corretamente. Quando tenta matar processos, falha e deixa órfãos.

**Solução**: Criar supervisor bash simples em `/root/clawd/scripts/gateway_supervisor.sh`

### 2. Auto-start sem Systemd
Adicionado ao `/root/.bashrc`:
```bash
if ! pgrep -f clawdbot-gateway > /dev/null 2>&1; then
    nohup /root/clawd/scripts/gateway_supervisor.sh > /tmp/supervisor.log 2>&1 &
fi
```

### 3. Fallbacks para Rate Limit
Configurados fallbacks quando Opus 4.5 bater rate limit:
- anthropic/claude-3-7-sonnet-latest
- anthropic/claude-3-5-haiku-latest

### 4. Scripts de Defesa
- `gateway_supervisor.sh` — Supervisor simples que reinicia se morrer
- `gateway_cleanup.sh` — Limpa processos órfãos
- `gateway_health.sh` — Monitora e corrige problemas

---

*Registrado por ONIR em 2026-02-03 20:45 BRT*
*Atualizado com solução sistêmica em 2026-02-03 20:55 BRT*
