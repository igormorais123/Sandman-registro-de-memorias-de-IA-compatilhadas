# HEARTBEAT.md - Tarefas Periódicas

## 🔧 Gateway Health Check (OBRIGATÓRIO - PRIMEIRO de todos)
- Rodar: `bash /root/clawd/scripts/gateway_health.sh`
- Se output contém "GATEWAY_ALERT" → problema não resolvido automaticamente, alertar Igor
- Se output contém "GATEWAY_RECOVERED" → problema foi corrigido, registrar no log diário
- Se output contém "GATEWAY_OK" → silencioso
- **Rodar ANTES do WhatsApp check** — se gateway está com problema, WhatsApp não vai funcionar

## 📱 WhatsApp Health Check (OBRIGATÓRIO a cada heartbeat)
- Verificar se WhatsApp está conectado: `clawdbot status 2>/dev/null | grep -i whatsapp`
- Se output contém "linked" → OK
- Se output contém "disconnected" ou não mostra WhatsApp:
  1. Tentar reconectar: `clawdbot channels login --channel whatsapp --account default`
  2. Se falhar, alertar Igor IMEDIATAMENTE
- **NUNCA ignorar WhatsApp desconectado** — é canal crítico de comunicação

## 🧠 Sandman Sync (a cada heartbeat, rápido)
- `bash /root/clawd/scripts/sandman_sync.sh`
- Se output contém "NEW_LETTERS" → ler cartas novas e alertar Igor
- Se output contém "NEW_DREAMS" → registrar nos logs diários
- Se output contém "PUSH_FAILED" → ignorar (PAT sem write access)

## 🐝 Colmeia Drive Sync (a cada ~4h durante horário ativo)
- `python3 /root/clawd/scripts/colmeia_sync_drive.py`
- Se output contém "SYNC_CHANGES" → commitar e pushar pro repo
- Se falhar → ignorar, tentar no próximo heartbeat
- Não rodar se último sync foi < 2h atrás

## 🔒 Security Scan (OBRIGATÓRIO a cada heartbeat)
- `bash /root/clawd/scripts/security_scan.sh --quick`
- Se output contém "SECURITY_ALERT" → alertar Igor IMEDIATAMENTE (mesmo em horário silencioso)
- Se output contém "SECURITY_OK" → tudo certo, não reportar
- Scan completo (com Shodan): `bash /root/clawd/scripts/security_scan.sh`
- Rodar scan completo pelo menos 2x ao dia (manhã e tarde)
- **NUNCA PULAR ESTE CHECK** — é a prioridade #1 de segurança

## 🔄 Rotação de Checks (fazer 2-3 por heartbeat, rotacionar)

### 📧 Email (a cada ~2h durante horário ativo)
- `python3 /root/clawd/scripts/check_gmail.py --unread --days 1`
- Alertar sobre: deploys falhos, erros, faturas, emails de clientes
- Ignorar: newsletters, promos, spam

### 🔧 GitHub CI/CD (a cada ~4h)
- `curl -s 'https://api.github.com/repos/igormorais123/pesquisa-eleitoral-df/actions/runs?per_page=3'`
- Alertar se CI/CD falhou nas últimas 24h
- Não repetir alertas já dados

### 📅 Calendário (a cada ~3h)
- `python3 /root/clawd/scripts/google_calendar.py today`
- Alertar se evento em < 2 horas

### 🌤️ Clima (1x ao dia, de manhã)
- `curl -s 'wttr.in/Brasilia?format=%C+%t+%h+%w&lang=pt'`
- Alertar se chuva forte / tempestade

### 💾 Sistema (1x ao dia)
- `df -h / && df -h /mnt/c` — alertar se disco < 20%
- `free -h` — alertar se RAM > 90%

## 📝 Tracking
- Atualizar `/root/clawd/memory/heartbeat-state.json` com timestamps dos checks
- Leia o JSON antes de decidir o que checar (evitar checks duplicados)

## ⏰ Horário Silencioso: 23h-8h
- Só alertar se URGENTE (servidor down, deploy crítico)
- Caso contrário: HEARTBEAT_OK
