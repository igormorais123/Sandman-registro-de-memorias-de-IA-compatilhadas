# Como Operacionalizar — Guia Prático

## O que temos montado

```
┌─────────────────────────────────────────────────────────────┐
│                    HOJE (já funcionando)                      │
│                                                              │
│  WhatsApp ──► Clawd (Clawdbot) ──► API INTEIA (Render)      │
│     │              │                    │                    │
│     │              │                    ├── 1000 eleitores   │
│     │              │                    ├── 10 candidatos    │
│     │              │                    ├── 12 templates     │
│     │              │                    └── PostgreSQL       │
│     │              │                                         │
│     │              ├── api_client.py (acessa tudo)           │
│     │              ├── Pesquisador Eleitoral (skill)         │
│     │              └── Análise de perfis (Python local)      │
│     │                                                        │
│  "Faz pesquisa    Executa tudo automaticamente               │
│   sobre Ibaneis"                                             │
└─────────────────────────────────────────────────────────────┘
```

## O que FALTA montar (próximo passo)

```
┌─────────────────────────────────────────────────────────────┐
│                    AMANHÃ (a construir)                       │
│                                                              │
│  WhatsApp ──► Clawd ──► Orquestra tudo:                     │
│                │                                             │
│                ├──► API INTEIA ──► Entrevistas IA            │
│                │    (Claude faz as perguntas qualitativas)   │
│                │                                             │
│                ├──► R / Python ──► Análise Estatística       │
│                │    (bootstrapping, correlação, regressão)   │
│                │    SEM gastar token Claude                  │
│                │                                             │
│                ├──► PostgreSQL ──► Salva TUDO                │
│                │    (pesquisas, respostas, análises)         │
│                │                                             │
│                └──► Relatório HTML ──► Dashboard             │
│                     (acessível no site para humanos)         │
└─────────────────────────────────────────────────────────────┘
```

---

## Passo a Passo para Operacionalizar

### 1. ENTREVISTAS IA (Claude faz as perguntas)

**Como funciona hoje:**
- API em api.inteia.com.br tem endpoint `/entrevistas/{id}/iniciar`
- Ele chama a Claude API no servidor Render
- Cada eleitor recebe as perguntas e responde "em persona"

**Como usar:**
```
Igor (WhatsApp): "Roda entrevista de rejeição com 30 eleitores da periferia"

Clawd faz:
1. Seleciona 30 eleitores do cluster C2 (periferia)
2. Cria entrevista na API com as perguntas
3. Inicia execução (background no Render)
4. Monitora progresso
5. Coleta respostas
6. Analisa e retorna resumo
```

**Custo estimado:**
- Sonnet 4: ~R$0,05 por eleitor por pergunta
- 30 eleitores × 5 perguntas = 150 chamadas = ~R$7,50
- 400 eleitores × 5 perguntas = 2000 chamadas = ~R$100

**⚠️ Pré-requisito:** CLAUDE_API_KEY configurada no Render
Verificar em: dashboard.render.com → Serviço backend → Environment Variables

---

### 2. ANÁLISE ESTATÍSTICA EM R/PYTHON (o insight do áudio)

**A ideia:** Em vez de pedir pro Claude "analise esses dados" (caro),
rodar a análise em R ou Python localmente (grátis).

**O que o R/Python faz MELHOR e MAIS BARATO que Claude:**
- Bootstrapping (reamostragem estatística)
- Regressão logística (o que prediz voto)
- Análise de clusters (k-means, hierárquico)
- Correlações cruzadas
- Intervalos de confiança
- Testes de hipótese (chi-quadrado, t-test)
- Visualizações (ggplot2, matplotlib)

**Como operacionalizar:**

```
Clawd recebe demanda
    │
    ├── Coleta dados via API (Python, grátis)
    │
    ├── Roda análise estatística (R/Python, grátis)
    │   ├── Script R: bootstrapping + correlação
    │   ├── Script Python: clustering + regressão
    │   └── Output: JSON com resultados
    │
    ├── Usa Claude SÓ para interpretar (1 chamada)
    │   "Dados mostram X, Y, Z. Interprete."
    │
    └── Monta relatório (grátis)
```

**Economia:**
- Sem R: 400 chamadas Claude para análise = ~R$200
- Com R: 1-2 chamadas Claude para interpretar = ~R$2
- **Economia: 99%**

**Scripts necessários (eu crio):**
```
skills/pesquisador-eleitoral/
├── api_client.py          ✅ Pronto
├── analise_r.R            📝 A criar
├── analise_python.py      📝 A criar
├── gerar_relatorio.py     📝 A criar
└── SKILL.md               ✅ Pronto
```

---

### 3. FLUXO COMPLETO DE UMA PESQUISA

```
IGOR (WhatsApp)
│
│ "Faz pesquisa de rejeição do Arruda com 200 eleitores"
│
▼
CLAWD (Pesquisador Eleitoral)
│
├─ ETAPA 1: PLANEJAMENTO (5 min, grátis)
│  ├── Define método (quanti+quali)
│  ├── Monta questionário (5 perguntas)
│  ├── Seleciona amostra (200 de 1000)
│  └── Estima custo (R$X)
│
├─ ETAPA 2: COLETA (30-60 min, custo Claude)
│  ├── Cria pesquisa na API
│  ├── Executa entrevistas IA (background)
│  ├── Monitora progresso
│  └── Coleta respostas
│
├─ ETAPA 3: ANÁLISE (10 min, grátis)
│  ├── Roda scripts R/Python
│  │   ├── Distribuição de frequência
│  │   ├── Correlações cruzadas
│  │   ├── Clusters (k-means)
│  │   ├── Margem de erro
│  │   └── Bootstrapping
│  ├── 1 chamada Claude para interpretar resultados
│  └── Gera JSON com achados
│
├─ ETAPA 4: RELATÓRIO (5 min, grátis)
│  ├── Monta relatório MD/HTML
│  ├── Gráficos (matplotlib/plotly)
│  ├── Salva no PostgreSQL
│  └── Publica no dashboard
│
└─ ETAPA 5: ENTREGA
   ├── Resumo executivo no WhatsApp
   ├── Relatório completo em Downloads
   ├── Dados acessíveis no dashboard web
   └── Disponível para outras IAs via API
```

---

### 4. COMO PEDIR UMA PESQUISA (exemplos práticos)

**Pesquisa rápida (só perfis, sem IA):**
```
"Clawd, quem são os indecisos do DF? Perfil demográfico."
→ Resultado em 2-3 minutos, custo zero
```

**Pesquisa com entrevistas (usa Claude):**
```
"Clawd, entrevista 50 eleitores sobre segurança pública.
Quero saber o que mais preocupa e se confiam na polícia."
→ Resultado em 30 min, custo ~R$12
```

**Pesquisa completa (quanti + quali + relatório):**
```
"Clawd, pesquisa completa de intenção de voto pro governo do DF.
400 eleitores, todas as perguntas. Relatório INTEIA."
→ Resultado em 1-2h, custo ~R$100
```

**Análise de dados existentes (reusa pesquisa anterior):**
```
"Clawd, pega os dados da pesquisa de rejeição do Ibaneis
e cruza com renda e região. Quero correlações."
→ Resultado em 5 min, custo zero (roda em R)
```

---

### 5. O QUE EU (CLAWD) PRECISO PARA FUNCIONAR 100%

| Item | Status | Quem faz |
|------|--------|----------|
| API Client (acesso ao sistema) | ✅ Pronto | Clawd |
| Skill Pesquisador Eleitoral | ✅ Pronto | Clawd |
| Análise de perfis (Python) | ✅ Pronto | Clawd |
| CLAUDE_API_KEY no Render | ❓ Verificar | Igor |
| Scripts R para estatística | 📝 A criar | Clawd |
| Scripts Python para clustering | 📝 A criar | Clawd |
| Gerador de relatórios HTML | 📝 A criar | Clawd |
| Parlamentares no banco Render | ❌ Falta ingerir | Claude Code no projeto |
| Entrevistas via API testadas | ❓ Testar | Clawd + Igor |

---

### 6. PRÓXIMOS PASSOS CONCRETOS

**Hoje (30 min):**
1. ✅ Pesquisa de perfil do Ibaneis — FEITA
2. Verificar se CLAUDE_API_KEY está no Render

**Esta semana:**
3. Eu crio os scripts R/Python de análise estatística
4. Eu crio o gerador de relatórios HTML padrão INTEIA
5. Testamos 1 entrevista IA com 10 eleitores pra validar

**Próxima semana:**
6. Ingerir parlamentares no banco Render
7. Rodar pesquisa completa de validação (200 eleitores)
8. Ajustar fluxo baseado nos resultados

---

*Operacionalização planejada em 30/01/2026*
*Clawd 🦞 — Pesquisador Eleitoral Sênior INTEIA*
