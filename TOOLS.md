# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Magie Pix IA (Pagamentos)
- **Número:** +55 11 5128-2022 (sem zero extra: 551151282022)
- **Função:** Assistente financeira para pagamentos via WhatsApp
- **Acesso:** Aprovado via pairing em 27/01/2026
- **Uso:** Posso consultar saldo, fazer PIX, pagar boletos
- **Saldo inicial:** R$ 11.139,62 (27/01/2026 22:33)

## API Keys & Integrações (configuradas 2026-01-31)
Chaves em `/root/clawd/.secrets/api_keys.env` (600 perms)
Auto-load via `source /root/clawd/.secrets/load_keys.sh` (no .bashrc)

| Serviço | Status | Uso |
|---------|--------|-----|
| Brave Search | ✅ Ativo | web_search nativo + API direta |
| Tavily | ✅ Ativo | Deep research: `python3 scripts/tavily_search.py "query"` |
| Vercel | ✅ Ativo | Deploy status: `python3 scripts/vercel_status.py projects` |
| Render | ✅ Ativo | API direta + deploy management |
| Google GDrive | ✅ Creds salvas | OAuth (client_id + secret) — scripts em scripts/ |
| BigQuery | 🔑 Project salvo | Project: opencode-485016 |
| GitHub CLI | ✅ Autenticado | `gh` como igormorais123 |
| Codex CLI | ✅ Autenticado | `codex` via OpenAI device auth |
| Gemini CLI | ✅ Ativo (API key) | `GEMINI_API_KEY` em api_keys.env |

### Projetos Vercel (8)
- 🟢 pesquisa-eleitoral-df — pesquisa-eleitoral-df-*.vercel.app
- 🟢 inteia-analise-politica-2026 — analise.inteia.com.br
- 🟢 opencode-academy — academy.inteia.com.br
- 🟢 frontend — inteia.com.br, app.inteia.com.br
- 🟢 relatorio — relatorio.inteia.com.br
- 🟢 aulainterativa-opencode
- 🟢 backend
- ⚪ igorm (inativo)

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## INTEIA - Sistema de Pesquisa Eleitoral
- **URL:** https://inteia.com.br
- **Login:** professorigor / professorigor
- **Acesso via Playwright:** Script em `/tmp/inteia_browser.js`
- **Docs:** `/root/clawd/docs/inteia/`

### Módulos do Sistema
| Módulo | Descrição | Quantidade |
|--------|-----------|------------|
| Eleitores | Agentes sintéticos | 1.000 |
| Consultores | Gêmeos digitais lendários | 100 |
| Magistrados | Juízes (STF/STJ/TJDFT/TRF1) | 164 |
| Parlamentares | Deputados e senadores DF | - |
| Candidatos | Eleições 2026 | - |
| Regiões | Administrativas do DF | 38 |

### Navegação (via Playwright headless)
1. Acessar inteia.com.br
2. Clicar "Entrar" → Modal de login
3. Preencher credenciais → Clicar "Entrar" no modal
4. Selecionar projeto "Pesquisa Eleitoral"
5. Navegar pelo menu lateral

## Documentos do Igor
- **RG:** /root/clawd/docs/igor/RG_IGOR_MORAIS_VASCONCELOS.pdf
- **CNH:** /mnt/c/Users/IgorPC/.claude/projects/reconvencao-igor-melissa/45_CARTEIRA_MODELO_B_CNH.pdf
