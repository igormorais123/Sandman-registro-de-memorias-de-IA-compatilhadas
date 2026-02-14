# WhatsApp & Gateway Health Monitoring

## Resumo do Problema (2026-02-12)

### Sintomas
- Logs mostrando "Port 18789 already in use" a cada ~3 segundos
- Loop de retry tentando iniciar gateway que já estava rodando
- WhatsApp desconectando/reconectando

### Causa Raiz
1. **Serviço duplicado**: Existia um serviço antigo `clawdbot-gateway.service` além do `openclaw-gateway.service`
2. **Script desatualizado**: `gateway_health.sh` referenciava `clawdbot-gateway` (versão antiga)
3. **Conflito de porta**: Múltiplas tentativas de iniciar gateway na mesma porta

### Solução Aplicada
1. ✅ Removido serviço duplicado `clawdbot-gateway.service`
2. ✅ Atualizado `gateway_health.sh` para usar `openclaw-gateway`
3. ✅ Criado `whatsapp_health.sh` para monitorar conexão WhatsApp
4. ✅ Adicionado cron job para monitoramento contínuo

---

## Scripts de Health Check

### `/root/clawd/scripts/gateway_health.sh`
Monitora o gateway OpenClaw.

**Retornos:**
- `GATEWAY_OK` - Tudo funcionando
- `GATEWAY_RECOVERED` - Problema corrigido automaticamente
- `GATEWAY_STARTED` - Gateway foi iniciado
- `GATEWAY_ALERT` - Problema que requer atenção

**Funcionalidades:**
- Verifica RPC probe
- Detecta processos duplicados
- Mata processos órfãos
- Reinicia via systemd se necessário

### `/root/clawd/scripts/whatsapp_health.sh`
Monitora conexão WhatsApp.

**Retornos:**
- `WHATSAPP_OK` - Conectado e funcionando
- `WHATSAPP_RECONNECTED` - Reconectou após desconexão
- `WHATSAPP_CONNECTING` - Reconectando (aguardar)
- `WHATSAPP_NEEDS_RELINK` - Precisa escanear QR code novamente
- `WHATSAPP_ALERT` - Problema que requer atenção
- `WHATSAPP_DISABLED` - Canal desabilitado na config
- `WHATSAPP_NOT_CONFIGURED` - Canal não configurado

---

## Cron Jobs

```crontab
# Monitora gateway a cada 10 minutos
*/10 * * * * /bin/bash /root/clawd/scripts/gateway_health.sh >> /root/clawd/memory/gateway-health.log 2>&1

# Monitora WhatsApp a cada 15 minutos
*/15 * * * * /bin/bash /root/clawd/scripts/whatsapp_health.sh >> /root/clawd/memory/whatsapp-health.log 2>&1
```

---

## Troubleshooting Manual

### Gateway não inicia
```bash
# Ver status
openclaw gateway status

# Verificar porta ocupada
lsof -i :18789

# Matar processo se órfão
kill -9 $(lsof -t -i :18789)

# Reiniciar via systemd
systemctl --user restart openclaw-gateway.service
```

### WhatsApp desconectou
```bash
# Ver status
openclaw status | grep WhatsApp

# Se precisa re-linkar
openclaw link whatsapp
```

### Logs
```bash
# Gateway health
tail -50 /root/clawd/memory/gateway-health.log

# WhatsApp health  
tail -50 /root/clawd/memory/whatsapp-health.log

# OpenClaw logs do dia
tail -200 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## Prevenção Futura

1. **Nunca executar `openclaw gateway start` manualmente** se o serviço systemd estiver habilitado
2. **Usar `openclaw gateway status`** para verificar antes de qualquer ação
3. **Monitorar logs** regularmente via cron jobs
4. **Um gateway por máquina** - não criar múltiplos serviços

---

## Arquivos Relacionados
- `/root/.config/systemd/user/openclaw-gateway.service` - Serviço systemd
- `/root/clawd/scripts/gateway_health.sh` - Script de monitoramento gateway
- `/root/clawd/scripts/whatsapp_health.sh` - Script de monitoramento WhatsApp
- `/root/clawd/memory/gateway-health.log` - Log do health check gateway
- `/root/clawd/memory/whatsapp-health.log` - Log do health check WhatsApp
