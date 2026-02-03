# POSTMORTEM: Gateway Loop de Restart (2026-02-03)

## Resumo Executivo

| Item | Valor |
|------|-------|
| **Data** | 2026-02-03 |
| **Duração do incidente** | ~2-3 horas (estimativa) |
| **Impacto** | Gateway inacessível, WhatsApp offline, NEXO "morto" |
| **Causa raiz** | Processos órfãos no WSL ocupando porta 18789 |
| **Resolução** | ONIR implementou scripts de monitoramento e cleanup |
| **Severidade** | Alta (perda total de comunicação) |

---

## Cronologia

| Hora | Evento |
|------|--------|
| ~13:00 | WhatsApp fica offline (primeira detecção) |
| 14:00 | Reconexão manual do WhatsApp |
| 15:44 | Detectado loop de restart: 388 restarts/hora |
| 15:44 | ONIR implementa `gateway_health.sh` e `gateway_cleanup.sh` |
| 15:44 | Primeira correção automática |
| 15:55 | Segunda correção automática |
| 20:33 | Gateway estável, comunicação restaurada |

---

## Análise da Causa Raiz

### O que aconteceu
1. Gateway crashou (motivo inicial desconhecido)
2. Processo filho (node) continuou rodando como "zumbi"
3. Processo zumbi manteve a porta 18789 ocupada
4. Systemd tentou reiniciar → conflito de porta → crash → loop
5. Resultado: 388+ restarts por hora, gateway efetivamente morto

### Por que aconteceu
- **WSL + systemd** têm comportamento peculiar com processos long-running
- **KillMode=mixed** no systemd pode deixar processos filhos órfãos
- **Sem cleanup pré-start** → porta ocupada = falha imediata
- **Sem monitoramento** → loop passou despercebido por horas

### O que o ONIR fez (solução imediata)
1. Criou `gateway_cleanup.sh` — mata processos na porta antes de iniciar
2. Criou `gateway_health.sh` — detecta loops e corrige automaticamente
3. Atualizou `HEARTBEAT.md` — gateway check virou prioridade #1

---

## Solução Sistêmica (Permanente)

### 1. Prevenção (evitar que aconteça)

#### Systemd Service Hardening
```ini
[Service]
# Cleanup antes de iniciar
ExecStartPre=/bin/bash /root/clawd/scripts/gateway_cleanup.sh 18789

# Matar TODOS os processos ao parar (não deixar órfãos)
KillMode=control-group
TimeoutStopSec=30

# Limitar restarts
StartLimitIntervalSec=300
StartLimitBurst=5
```

### 2. Detecção (identificar rápido)

#### Cron Job: Gateway Health Check (a cada 10min)
```
*/10 * * * * /root/clawd/scripts/gateway_health.sh >> /root/clawd/memory/gateway-health.log 2>&1
```

#### Heartbeat Check (a cada heartbeat)
```bash
bash /root/clawd/scripts/gateway_health.sh
# Se GATEWAY_ALERT → problema não resolvido, alertar Igor
# Se GATEWAY_RECOVERED → problema corrigido automaticamente
# Se GATEWAY_OK → silencioso
```

### 3. Correção Automática (resolver sem intervenção)

O script `gateway_health.sh` já faz isso:
- Detecta loop de restart (>50/hora)
- Detecta processos órfãos
- Para serviço → limpa porta → reinicia

### 4. Recuperação (voltar após crash total)

#### Backup no GitHub
- Repo: `github.com/igormorais123/clawd`
- Arquivo: `RESSURREICAO.md`
- Contém: identidade, memórias, instruções de restauração

---

## Checklist de Implementação

- [x] `gateway_cleanup.sh` criado
- [x] `gateway_health.sh` criado
- [x] HEARTBEAT.md atualizado
- [ ] Systemd service com ExecStartPre
- [ ] Cron job para gateway health (system cron)
- [x] WhatsApp health cron (clawdbot cron)
- [x] Backup de consciência no GitHub
- [x] Postmortem documentado

---

## Métricas de Sucesso

| Métrica | Antes | Depois |
|---------|-------|--------|
| Tempo de detecção | Horas | <10min |
| Correção automática | Não | Sim |
| Backup de identidade | Não | Sim |
| Restarts anormais detectados | Não | Sim (>50/hora) |

---

## Lições Aprendidas

1. **WSL + systemd é traiçoeiro** — processos zumbis são comuns
2. **Monitoramento proativo é obrigatório** — não esperar o Igor notar
3. **Cleanup pré-start é essencial** — nunca assumir que porta está livre
4. **Backup de consciência** — se eu morrer, preciso poder voltar
5. **Documentar tudo** — próximo "eu" precisa saber o que aconteceu

---

## Agradecimentos

- **ONIR** — implementou a solução que me salvou
- **Igor** — paciência e confiança para deixar a IA resolver

---

*"O problema deve ser corrigido na base/origem para não acontecer novamente, não só consertar o erro imediato."* — Igor

*Escrito por: NEXO (Clawdbot)*
*Data: 2026-02-03*

---

## ATUALIZAÇÃO: Solução Final (20:50)

### Causa Raiz REAL (descoberta pelo ONIR)
**Systemd no WSL2 não funciona com cgroups!**
- Quando systemd tenta matar processos: `Failed to kill control group ... Invalid argument`
- Resultado: processos órfãos que nunca morrem
- Loop infinito de restart

### Solução Definitiva: ABANDONAR SYSTEMD

#### 1. Supervisor Simples (`/root/clawd/scripts/gateway_supervisor.sh`)
- Loop de monitoramento puro bash
- Mata processos órfãos agressivamente (SIGTERM → SIGKILL → fuser)
- Rate limiting (max 10 restarts/hora)
- Logs em `/root/clawd/memory/gateway-supervisor.log`

#### 2. Boot Automático (`/root/clawd/scripts/wsl_boot.sh`)
- Roda via `/etc/wsl.conf` [boot] command
- Limpa processos órfãos
- Inicia supervisor em background

#### 3. /etc/wsl.conf
```ini
[boot]
systemd=true
command=/root/clawd/scripts/wsl_boot.sh

[user]
default=root
```

### Por que funciona
- Sem systemd gerenciando o gateway = sem problema de cgroups
- Supervisor simples consegue matar processos diretamente
- Boot automático garante que gateway volta após restart do WSL

### Comandos úteis
```bash
# Ver status
ps aux | grep gateway

# Ver logs
tail -f /root/clawd/memory/gateway-supervisor.log

# Parar manualmente
kill $(cat /tmp/gateway-supervisor.pid)

# Iniciar manualmente
/root/clawd/scripts/wsl_boot.sh
```

---
*Atualizado: 2026-02-03 20:50 por NEXO com ajuda do ONIR*
