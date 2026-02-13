# TOOLS.md — Ambiente do Casulo

## Plataforma

- **Gateway:** Clawdbot via WSL2 Ubuntu-24.04
- **Host:** PC Igor (Windows 11, Ryzen 9 7900, 64GB RAM)
- **Modelo:** Claude Opus 4.5 / Haiku 4.5

## Canais Integrados

- **WhatsApp** — conta pessoal Igor (via Baileys)
- **Telegram** — bot dedicado

## Ferramentas Disponiveis

### Sistema
- Acesso filesystem via WSL
- Cron jobs (crontab)
- Git (repos Colmeia, INTEIA-cursos, etc.)
- Scripts Python e Bash

### Comunicacao
- Envio de emails via colmeia@inteia.com.br
- Script: `python3 /root/clawd/scripts/colmeia_enviar.py`

### Automacao
- Team of Rivals (Codex CLI + Gemini API)
- Heartbeat cycle a cada 30min
- Browser tool (pesquisa web)

## Caminhos no WSL

```
/root/clawd/              → repo principal
/root/clawd/scripts/      → scripts de automacao
/root/clawd/memoria/      → memoria local WSL
```

## Caminhos no Windows (via /mnt/c/)

```
/mnt/c/Users/IgorPC/Colmeia/  → repo Colmeia
```

## Notas

- Gateway deve estar sempre rodando (systemd)
- Logs em /root/clawd/logs/
- Backup automatico via git push

---
*Casulo — Ferramentas — Colmeia v6*
