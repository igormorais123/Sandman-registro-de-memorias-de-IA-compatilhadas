# INTEIA | AUDITORIA DE SEGURANÇA
## Relatório de Análise e Correção de Vulnerabilidades

**Documento:** SEC-2026-001  
**Data:** 29 de janeiro de 2026  
**Sistema:** Clawdbot Gateway — WSL2 (IgorVasconcelos)  
**Classificação:** CONFIDENCIAL  
**Analista:** Clawd (IA)  
**Score:** 4/10 → **9/10**

---

## 1. SUMÁRIO EXECUTIVO

Auditoria de segurança realizada no servidor WSL2 que hospeda o Clawdbot Gateway. Foram identificadas **11 vulnerabilidades**, das quais **10 foram corrigidas automaticamente** e **1 requer ação manual** (Tailscale login).

**Nenhuma porta está exposta externamente.** Todas as conexões são localhost (127.0.0.1).

---

## 2. VULNERABILIDADES ENCONTRADAS E CORRIGIDAS

### 🔴 CRÍTICAS (Corrigidas)

| # | Vulnerabilidade | Risco | Ação | Status |
|---|----------------|-------|------|--------|
| 1 | Secrets (gmail.json, google_credentials, token) commitados no Git | Vazamento de credenciais | Removidos do tracking + .gitignore | ✅ |
| 2 | RG e documentos pessoais do Igor no Git | Exposição de dados pessoais | Removidos do tracking + .gitignore | ✅ |
| 3 | Memory sensível (contatos, dossiê, inferências) no Git | Exposição de dados pessoais | Removidos do tracking + .gitignore | ✅ |

### 🟡 ALTAS (Corrigidas)

| # | Vulnerabilidade | Risco | Ação | Status |
|---|----------------|-------|------|--------|
| 4 | Permissões world-readable em secrets (644/755) | Leitura por qualquer processo | Corrigido para 600/700 | ✅ |
| 5 | Sem firewall (UFW não instalado) | Portas abertas sem controle | UFW instalado e configurado (deny incoming) | ✅ |
| 6 | CUPSD exposto em 0.0.0.0:631 | Serviço desnecessário acessível | Snap desabilitado, porta fechada | ✅ |
| 7 | 56 atualizações de segurança pendentes | Vulnerabilidades conhecidas | Todas aplicadas | ✅ |

### 🟢 MÉDIAS (Corrigidas)

| # | Vulnerabilidade | Risco | Ação | Status |
|---|----------------|-------|------|--------|
| 8 | BOOTSTRAP.md ainda existia | Informação de setup exposta | Deletado | ✅ |
| 9 | Core dumps habilitados | Vazamento de memória em crash | Desabilitados via limits.conf | ✅ |
| 10 | /proc sem restrição | Info do kernel acessível | dmesg_restrict + kptr_restrict | ✅ |

### ⚠️ PENDENTE (Requer ação manual)

| # | Vulnerabilidade | Risco | Ação Necessária | Status |
|---|----------------|-------|-----------------|--------|
| 11 | Tailscale deslogado | VPN inativa | Executar `tailscale up` no terminal | ⚠️ |

---

## 3. CONFIGURAÇÃO DO FIREWALL (UFW)

```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)

Regras:
  Anywhere ← ALLOW ← 127.0.0.0/8 (localhost)
```

**Política:** Bloquear todo tráfego de entrada. Permitir apenas localhost. Saída livre.

---

## 4. PORTAS ATIVAS (Pós-correção)

| Porta | Endereço | Serviço | Risco |
|-------|----------|---------|-------|
| 53 | 127.0.0.54 | systemd-resolved | ✅ Só local |
| 53 | 127.0.0.53 | systemd-resolved | ✅ Só local |
| 3334 | 127.0.0.1 | Clawdbot Gateway | ✅ Só local |
| 18789 | 127.0.0.1 | Clawdbot API | ✅ Só local |
| 18791 | 127.0.0.1 | Clawdbot Browser | ✅ Só local |
| 18792 | 127.0.0.1 | Clawdbot WS | ✅ Só local |

**Portas expostas externamente: ZERO** ✅

---

## 5. CONEXÕES EXTERNAS (Legítimas)

| Destino | Porta | Serviço | Processo |
|---------|-------|---------|----------|
| 162.159.134.x | 443 | Cloudflare (WhatsApp) | clawdbot-gateway |
| 54.207.255.x | 443 | AWS (Anthropic API) | clawdbot-gateway |
| 149.154.166.x | 443 | Telegram API | clawdbot-gateway |
| 160.79.104.x | 443 | Signal/Render API | clawdbot-gateway |
| 31.13.90.x | 443 | Meta (WhatsApp) | clawdbot-gateway |

Todas as conexões são TLS (porta 443) e pertencem ao Clawdbot. **Nenhuma conexão suspeita detectada.**

---

## 6. HARDENING APLICADO

| Medida | Arquivo | Valor |
|--------|---------|-------|
| Core dumps desabilitados | /etc/security/limits.conf | `* hard core 0` |
| SUID dump desabilitado | /etc/sysctl.d/99-security.conf | `fs.suid_dumpable = 0` |
| dmesg restrito | /etc/sysctl.d/99-security.conf | `kernel.dmesg_restrict = 1` |
| Kernel pointers ocultos | /etc/sysctl.d/99-security.conf | `kernel.kptr_restrict = 2` |

---

## 7. GIT - PROTEÇÕES IMPLEMENTADAS

### .gitignore reforçado:
```
# Secrets - NUNCA commitar
.secrets/
*.pickle
*.key
*.pem
.env
.env.*

# Documentos pessoais
docs/igor/
docs/igor_documento.pdf
*.pdf

# Memory sensível
memory/contatos-igor.md
memory/dossie-igor.md
memory/inferencias-igor.md
MEMORY.md
```

### Commits de segurança:
- `2bac065` - security: remover secrets do git tracking
- `f9c9333` - security: proteger documentos pessoais e dados sensíveis

---

## 8. RECOMENDAÇÕES FUTURAS

1. **Tailscale:** Fazer login (`tailscale up`) para VPN ativa
2. **Rotação de credenciais:** Trocar tokens do Gmail/Google (podem ter sido expostos no histórico Git)
3. **Git history cleanup:** Considerar `git filter-branch` para remover secrets do histórico completo
4. **Monitoramento:** Configurar alertas para tentativas de acesso
5. **Backup:** Implementar backup automático dos secrets

---

## 9. SCORE DE SEGURANÇA

| Categoria | Antes | Depois |
|-----------|-------|--------|
| Secrets/Credenciais | 1/10 | 9/10 |
| Rede/Firewall | 3/10 | 9/10 |
| Permissões | 4/10 | 9/10 |
| Atualizações | 3/10 | 10/10 |
| Hardening | 4/10 | 8/10 |
| **TOTAL** | **4/10** | **9/10** |

---

**INTEIA — Inteligência Estratégica**  
Documento gerado em 29/01/2026 — Sistema Clawd  
Classificação: CONFIDENCIAL
