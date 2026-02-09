# 🔧 Setup de Integrações — O que falta

## ✅ Já Funcionando
| Integração | Status | Detalhes |
|---|---|---|
| WhatsApp | ✅ | DM + grupos (allowlist) |
| Telegram | ✅ | DM + grupos, streaming |
| Discord | ✅ | Grupos (allowlist) |
| Slack | ✅ | Socket mode |
| Voice Call | ✅ | Twilio (+12172828852) |
| Gmail | ✅ | check_gmail.py — emails não lidos |
| Google Calendar | ✅ | google_calendar.py — eventos e lembretes |
| API Pesquisa Eleitoral | ✅ | api_client.py — 1000 eleitores, 10 candidatos |
| GitHub Monitor | ✅ | github_monitor.py — status CI/CD (API pública) |
| System Health | ✅ | system_health.py — disco, RAM, CPU, serviços |
| Morning Briefing | ✅ | morning_briefing.py — newsletter matinal combinada |
| Clima Brasília | ✅ | wttr.in (sem API key) |
| Cron: Briefing 7h | ✅ | Email + calendar + GitHub + clima + sistema |
| Cron: GitHub CI 3x/dia | ✅ | 9h, 14h, 19h |
| Cron: Calendar 5x/dia | ✅ | Alertas de eventos < 2h |
| Cron: Postura 4x/dia | ✅ | 10h, 12h, 14h, 16h (seg-sex) |
| Cron: Doutorado semanal | ✅ | Dom 20h |

## 🟡 Precisa de Ação do Igor

### 1. 🔍 Brave Search API (Web Search)
**Impacto:** Alto — permite busca web nos heartbeats e conversas
**Esforço:** 2 min
**Como:**
1. Acesse https://brave.com/search/api/
2. Crie conta (free tier = 2000 queries/mês)
3. Gere API key
4. Rode no terminal: `clawdbot configure --section web`
5. Cole a key quando pedido

### 2. 🐙 GitHub CLI (`gh`) Auth  
**Impacto:** Alto — permite corrigir CI/CD, criar PRs, issues
**Esforço:** 1 min
**Como:**
```bash
gh auth login
# Escolha: GitHub.com → HTTPS → Login with browser
```

### 3. 🧠 Memory Search (Embeddings)
**Impacto:** Médio — busca semântica na memória
**Esforço:** 5 min
**Como:** Precisa de API key OpenAI ou Google para gerar embeddings.
```bash
# Opção 1: OpenAI
export OPENAI_API_KEY="sk-..."

# Opção 2: Google
export GOOGLE_API_KEY="AI..."
```
Adicionar em `/root/.clawdbot/.env`

### 4. 📝 Notion API (opcional)
**Impacto:** Médio — organização de projetos
**Esforço:** 10 min
**Como:** Criar integration em https://www.notion.so/my-integrations

### 5. 💾 Espaço em Disco C:
**Impacto:** ⚠️ Alerta — 83% usado, 162GB livres
**Sugestão:** Limpar node_modules, caches, temp files
```powershell
# No PowerShell:
npx npkill  # Remove node_modules interativamente
```

## 📊 Cron Jobs Ativos
```
0 7 * * *         → Briefing matinal (WhatsApp)
0 9,14,19 * * 1-6 → GitHub CI check
0 8,10,12,14,16   → Calendar reminder (2h)
0 10,12,14,16 1-5 → Postura/alongamento
0 20 * * 0        → Resumo doutorado semanal
```

## 📁 Scripts Disponíveis
```
/root/clawd/scripts/
├── check_gmail.py        — Emails não lidos
├── google_calendar.py    — Eventos do calendário
├── github_monitor.py     — Status CI/CD do GitHub
├── system_health.py      — Health check do sistema
├── morning_briefing.py   — Briefing combinado
└── db_pesquisa.py        — Wrapper API pesquisa eleitoral

/root/clawd/skills/pesquisador-eleitoral/
└── api_client.py         — Cliente completo da API INTEIA
```
