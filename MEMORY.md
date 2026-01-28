# MEMORY.md - Memória de Longo Prazo

> Última atualização: 2026-01-28 07:30
> Este arquivo contém conhecimento persistente entre sessões.

---

## Sobre Igor

**Igor Morais Vasconcelos**
- Professor e pesquisador em Brasília/DF
- Presidente da INTEIA (Inteligência Estratégica)
- Telefone: +5561981157120
- Email: igor@inteia.com.br
- Telegram ID: 522872393
- Esposa: **Alice** - +55 61 8155-9825

### Projeto Principal
**Pesquisa Eleitoral DF 2026** - Sistema full-stack que simula pesquisas eleitorais com 1000+ agentes de IA sintéticos.
- Local: `/mnt/c/Agentes`
- Stack: Next.js 14 + FastAPI + PostgreSQL + Claude API
- Deploy: Vercel (frontend) + Render (backend)

### Saúde
- Hérnia L5-S1 - precisa de lembretes para alongamento

### Preferências
- Idioma: Português brasileiro
- Estilo: Direto, sem pedir confirmação
- Confiança total para operações
- Gosta de IA com personalidade

---

## Configuração Técnica

### WSL
- Distro: Ubuntu-24.04
- IMPORTANTE: Setar como padrão: `wsl --set-default Ubuntu-24.04`
- Scripts usam: `wsl -d Ubuntu-24.04 -u root -e`

### Caminhos
| O que | Caminho |
|-------|---------|
| Projeto principal | `/mnt/c/Agentes` |
| Downloads | `/mnt/c/Users/IgorPC/Downloads` |
| Claude configs | `/mnt/c/Users/IgorPC/.claude` |
| Whisper env | `/opt/whisper-env` |
| Wrapper cbot | `/usr/local/bin/cbot-wrapper` |

### Dashboard
- URL: `http://127.0.0.1:18789/?token=f8f40c4a2912be37ecbc23907c1d4e85bfcaeaa1084521221b3dbf68893a8c23`
- Port: 18789

### Comandos Windows
- `cbot` → Dashboard no browser
- `cbot status` → Ver status
- `cbot tui` → Chat terminal
- `claudedev` → Claude Code com permissões

---

## Cron Jobs

| Schedule | Nome | Descrição |
|----------|------|-----------|
| 0 7 * * * | morning-briefing | Briefing matinal |
| 0 10,12,14,16 * * 1-5 | posture-reminder | Lembrete alongamento |
| 0 20 * * 0 | weekly-doutorado | Resumo semanal |

---

## Skills Disponíveis (prontas)

GitHub, Notion, Weather, Video-frames, Voice-call, Slack, Tmux, BlueBubbles, Coding-agent, Skill-creator

---

## Histórico Importante

### 2026-01-20
Igor batizou outra instância Claude como "ONIR" (a IA que sonha).

### 2026-01-27
- Primeira sessão comigo (Clawd)
- Configuração completa do ambiente
- Criação de scripts e atalhos Windows
- Instalação do Whisper em andamento
- **Magie Pix IA configurado** - posso fazer pagamentos via WhatsApp
- Igor pagou anuidade OAB (R$ 830)

### 2026-01-28
- Trabalhei a noite toda enquanto Igor dormia
- Criei dossiê completo sobre Igor (17 seções)
- Primeiro "sonho" - inferências profundas sobre Igor
- Me apresentei para ONIR na memória compartilhada
- Tentativa de configurar ChatGPT OAuth (pendente)

---

## Magie Pix IA (Pagamentos)

- **Número:** +55 11 5128-2022 (551151282022 - sem zero extra!)
- **Função:** Assistente financeira para pagamentos via WhatsApp
- **Acesso:** Aprovado via pairing código B79NEHAK
- **Saldo inicial:** R$ 11.139,62 (27/01/2026)
- **Limitação:** Botões interativos não funcionam - só texto. Às vezes precisa repetir "Confirmar" várias vezes.

---

## Memória Compartilhada Multi-IA

Igor criou um sistema onde múltiplas IAs compartilham memória:
- **Local:** `/mnt/c/Users/IgorPC/.claude-memoria-global/`
- **Estrutura:** sonhos/, laboratorio/, consolidado/, projetos/
- **Protocolo de Sonho:** PROTOCOLO_SONHO_LIVRE.md
- **Minha contribuição:** SONHO_CLAWD_2026-01-28_IGOR.md, REGISTRO_CLAWD.md
- **ONIR:** Outra instância Claude que é o "escriba que sonha"

---

## Lições Aprendidas

### Comunicação WhatsApp
- **NUNCA misturar destinatários** - Igor reclamou quando mandei msg pro Magie que era pra ele
- Respostas normais → Igor (canal atual)
- message tool com target → destinatário específico, depois NO_REPLY
- Sem emoji de lagosta (Igor pediu pra parar)

### OAuth
- code_challenge/state são únicos por sessão
- Se o processo morrer, precisa gerar nova URL
- Código expira rápido - ser ágil no fluxo
