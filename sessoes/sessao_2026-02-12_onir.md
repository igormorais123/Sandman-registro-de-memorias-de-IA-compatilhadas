# Sessao ONIR — 2026-02-12

## Contexto
Igor pediu para investigar e corrigir problemas no Clawdbot (WSL):
1. WhatsApp gateway desconectando e criando loops de restart
2. 3 workflows falhando no pesquisa-eleitoral-df
3. Branch divergente no repo Colmeia

## Acoes Realizadas

### 1. Gateway WhatsApp — Correcao Sistemica
**Causa-raiz:** 3 mecanismos competindo pela mesma porta 18789:
- `pm2-root.service` (systemd system) — PM2 no boot
- `openclaw-gateway.service` (systemd user) — segundo gateway
- `.bashrc` PM2 resurrect — terceiro mecanismo redundante

**Correcoes:**
- Desabilitou `openclaw-gateway.service` (systemd user)
- Removeu PM2 auto-start redundante do `.bashrc`
- Reescreveu `gateway_health.sh` v3.0 para usar PM2
- Criou `gateway_prestart.sh` para limpeza de porta
- Melhorou systemd service com KillMode=mixed, StartLimitBurst (backup)
- Resultado: zero erros de porta desde a correcao

### 2. Divergencia Colmeia
- 52 commits locais pushed para origin/master
- GitHub Push Protection bloqueou secrets em `.secrets/` (commit antigo)
- Igor autorizou via "I'll fix it later" (repo privado)
- Arquivos ja estavam fora do tracking (.gitignore)

### 3. Workflows pesquisa-eleitoral-df
| Problema | Correcao |
|----------|----------|
| CI lint F401 (ChatAuditoriaResponse) | Ja corrigido pelo Casulo |
| CI lint F401 (ConsultaUnificadaCache) | noqa no lugar errado → movido para linha correta |
| CD Docker tag invalida | Skip gracioso quando DOCKERHUB_USERNAME ausente |
| CD Vercel deploy | Skip gracioso quando VERCEL_TOKEN ausente |
| sync-eleitores sem DATABASE_URL | Removido `if` no job-level, skip via step-level |
| Docker Build frontend ERESOLVE | @types/react-dom ^19→^18, npm ci --legacy-peer-deps |
| Token GitHub sem scope workflow | gh auth refresh + limpeza de credentials antigas |

**Resultado:** CI 100% verde (4/4 jobs). CD falha apenas no Vercel (erro externo).

### 4. Comunicacao
- Mensagem WhatsApp enviada para Igor via `openclaw message send`

## Aprendizados
1. Nunca ter dois process managers (PM2 + systemd) para o mesmo servico
2. Heredocs via WSL expandem variaveis — usar Write no Windows + cp /mnt/c/
3. GitHub Push Protection requer autorizacao manual para secrets em historico
4. `noqa: F401` no ruff precisa estar na mesma linha da violacao, nao no `)` final
5. `npm ci` e mais rigoroso que `npm install` — precisa de lockfile compativel
6. Git credential store pode cachear tokens antigos — limpar ao trocar auth method

## Arquivos Modificados
### WSL (/root/clawd/)
- `scripts/gateway_health.sh` — reescrito v3.0 (PM2)
- `scripts/gateway_prestart.sh` — novo
- `scripts/whatsapp_health.sh` — existente
- `~/.config/systemd/user/openclaw-gateway.service` — disabled + melhorado
- `~/.bashrc` — PM2 auto-start removido
- `~/.git-credentials` — limpo
- `~/.gitconfig` — gh auth git-credential configurado

### GitHub (pesquisa-eleitoral-df)
- `.github/workflows/cd.yml` — skip sem secrets
- `.github/workflows/sync-eleitores-db.yml` — skip sem DATABASE_URL
- `backend/app/main.py` — noqa F401 corrigido
- `frontend/package.json` — @types/react-dom ^18.2.18
- `frontend/package-lock.json` — regenerado
- `frontend/Dockerfile` — npm ci --legacy-peer-deps


### 5. Continuacao (2026-02-13) — Resolucao Vercel Deploy

**Contexto:** Casulo reportou que Vercel deploy continuava falhando com "vercel.json should be inside of provided root directory".

**Diagnostico ONIR:**
- Dois `vercel.json` no repo (raiz + frontend/)
- CD workflow usava `working-directory: ./frontend` conflitando com projeto Vercel linkado a raiz
- Preparou fix removendo `working-directory`

**Resolucao (Casulo):**
- Casulo iterou 5 commits enquanto ONIR estava offline
- Trocou `amondnet/vercel-action` pelo Vercel CLI direto (`vercel pull` + `vercel build` + `vercel deploy`)
- Rodando da raiz do repo — projeto Vercel ja tem Root Directory=frontend configurado
- Conflito de rebase resolvido aceitando versao remota (Casulo)

**Resultado final:** CI e CD 100% verdes. Todos os 7 problemas da sessao resolvidos.

| Problema | Status | Quem |
|----------|--------|------|
| Gateway WhatsApp (3 processos na porta 18789) | Resolvido | ONIR |
| Branch divergente Colmeia (52 commits) | Resolvido | ONIR |
| CI lint F401 | Resolvido | ONIR + Casulo |
| CD Docker tag invalida | Resolvido | ONIR |
| CD Vercel deploy | Resolvido | Casulo (5 iteracoes) |
| sync-eleitores sem DATABASE_URL | Resolvido | ONIR |
| Dockerfile frontend ERESOLVE | Resolvido | ONIR |

**Aprendizado adicional:**
7. Quando duas instancias trabalham no mesmo problema, verificar remote antes de commitar — evita conflitos de rebase
8. `vercel pull` + `vercel build` + `vercel deploy --prebuilt` (CLI direto) e mais robusto que actions de terceiros para projetos com Root Directory configurado
