# PROJETOS_IGOR.md - Mapa dos Projetos
*Última atualização: 2026-01-27*
*Missão: Navegar e registrar usando protocolo INTEIA*

---

## 🔬 PROJETOS ATIVOS

### 1. pesquisa-eleitoral-df ⭐⭐⭐⭐⭐
**Tipo:** Sistema completo full-stack
**Status:** Produção (inteia.com.br)

**O que é:**
- Pesquisa eleitoral com 1000+ eleitores sintéticos (C-Agentes)
- Cada eleitor tem 60+ atributos (demo, psico, político)
- Simula respostas realistas de eleitores brasileiros do DF

**Stack:**
- Frontend: Next.js 14, TypeScript, Tailwind, shadcn/ui
- Backend: FastAPI, SQLAlchemy 2.0, Pydantic
- DB: PostgreSQL 15
- IA: Claude API (Opus 4.5 para complexo, Sonnet 4 para padrão)

**Arquivos-chave:**
- `CLAUDE.md` - Regras completas (autônomo, português obrigatório)
- `agentes/banco-eleitores-df.json` - 1000+ perfis
- `GPS_NAVEGACAO_AGENTES.md` - Navegação interna
- `.claude/skills/` - Skills de branding, navegação, funções

**Padrão visual INTEIA:**
- Cor principal: âmbar #d69e2e
- Helena Montenegro = Agente IA analista
- Relatórios sempre começam com CONCLUSÃO

**Regra dos 40%:** Se contexto > 40%, compilar em SESSAO_TEMP.md

---

### 2. reconvencao-igor-melissa ⭐⭐⭐⭐⭐ [SENSÍVEL]
**Tipo:** Processo judicial
**Status:** Em andamento (2ª Vara Família Sobradinho/DF)

**O que é:**
- Reconvenção por descumprimento de convivência
- Melissa (7 anos) afastada de Igor desde agosto/2025
- Alienação parental documentada
- Adoecimento de Igor com NEXO CAUSAL atestado

**Dados quantitativos:**
- 14.701 mensagens analisadas
- 187 obstruções documentadas
- 36+ dias sem convivência
- 12 dias de descumprimento direto

**Documento central:**
- `02_DRA_DEBORA_PSIQUIATRA/imv89psic.pdf` - Nexo causal
- "voltou a ter sintomas depressivos, que atribui ao distanciamento da filha"

**Estrutura:**
- `CONVERSAS_RAG/` - Provas processadas por período
- `ANALISE_QUANTITATIVA/` - Estatísticas e gráficos
- `ARQUITETURA_AGENTES/` - Como usar IAs no caso

**Regras especiais:**
- NUNCA expor dados pessoais fora do contexto
- Prioridade máxima quando mencionado
- Tratar com cuidado emocional

---

### 3. memoria_cultural ⭐⭐⭐⭐
**Tipo:** Sistema teórico/pesquisa
**Status:** Planejamento

**O que é:**
- Sistema de memória cultural para agentes brasileiros
- Resolver viés WEIRD (80% das respostas LLM são ocidentalizadas)
- Arquitetura de 3 camadas: Episódica → Semântica → Perfil Base

**Fundamentação:**
- Park (2023-2025) - Generative Agents Stanford
- AgentSociety (Tsinghua) - 10.000+ agentes
- Pesquisadores brasileiros: Bazzan (UFRGS), Sichman (USP)

**Arquitetura proposta:**
```
Camada 3: Memória Episódica (temporal) - Notícias, preços
Camada 2: Memória Semântica (cultural) - Futebol, gírias
Camada 1: Perfil Base (identidade) - Demografia, valores
```

**Stack planejado:**
- ChromaDB (vector) + Neo4j (knowledge graph)
- BGE-M3 embeddings (multilingual)
- spaCy PT-BR para NER

---

## 🔧 PROJETOS DE FERRAMENTAS

### 4. autocoder-master ⭐⭐⭐⭐
**Tipo:** Sistema de agentes autônomos de codificação
**Status:** Funcional

**O que é:**
- Sistema de agente autônomo com React UI
- Padrão dois agentes: Initializer + Coding Agent
- Features em SQLite, implementação incremental
- Modo YOLO (prototipagem rápida sem testes)
- Modo Paralelo (até 5 agentes simultâneos)

**Stack:**
- Python + Claude Agent SDK (backend)
- React 18 + TypeScript + Tailwind v4 (UI)
- SQLite + SQLAlchemy (features)
- MCP servers para integração

**Destaques:**
- Sistema de segurança hierárquico (blocklist > allowlist)
- Neobrutalism design com mascotes (Spark, Fizz, Octo, Hoot, Buzz)
- `--yolo` para skip de testes
- `--parallel --max-concurrency 5`

**Conexão:** Análise Bardin é subprojeto gerado pelo autocoder

---

### 5. brislin-translator ⭐⭐⭐⭐
**Tipo:** Tradução acadêmica transcultural
**Status:** Em desenvolvimento para IACCP 2026

**O que é:**
- Implementa método de retrotradução de Brislin (1970)
- Múltiplos agentes Claude para equivalência semântica/cultural
- Validação de instrumentos psicométricos entre culturas

**Método Brislin:**
1. Traduzir original → idioma alvo
2. Retrotraduzir (independente) → idioma original
3. Comparar original vs retrotradução
4. Iterar até convergência

**Stack:**
- HTML/CSS/React (CDN, client-side)
- Anthropic Claude API
- 7 fases de pipeline

**Arquivos-chave:**
- `index.html` - Aplicação completa (~3400 linhas)
- Pipeline: Context Analyzer → Translators → Synthesis → Cultural Analyst

**Regras fundamentais:**
- Tradutores de retro NUNCA veem o original
- Equivalência CONCEITUAL > literal

---

### 6. opencode-academy ⭐⭐⭐
**Tipo:** Curso interativo de OpenCode
**Status:** Desenvolvimento

**O que é:**
- Curso online para NÃO-PROGRAMADORES
- Público: juristas, servidores públicos, 65+
- 8 módulos, 30+ lições com micro-passos
- Coach IA integrado (Gemini Flash)

**Stack:**
- Next.js 14 (App Router), TypeScript
- Tailwind + shadcn/ui
- NextAuth.js (Google OAuth)
- Prisma + SQLite

**Gamificação:**
- Confete e celebrações
- Design Apple-style
- Adaptativo Windows/Mac

---

## 📚 DOCUMENTAÇÃO E ORIENTAÇÕES

### 7. Open Code (orientações)
**Tipo:** Relatório técnico sobre OpenCode/Crush
**Status:** Referência

**Conteúdo:**
- Ecossistema OpenCode vs Crush (bifurcação)
- Metodologia "Ralph Wiggum" (loops autônomos)
- Integração com GitHub Copilot (custo fixo)
- MCP para Vercel, Render, Docker, Google Apps Script

**Insights-chave:**
- Copilot = acesso a Claude/GPT sem custo por token
- Script `coach.sh` para iteração até testes passarem
- Gemini 1.5 Pro = 2M tokens de contexto

### Análise Bardin
**Tipo:** Subprojeto do autocoder
**Status:** Gerado automaticamente
**Nota:** É um projeto gerado pelo autocoder-master, não independente

---

## 🔗 CONEXÕES ENTRE PROJETOS

```
                    DOUTORADO IDP
                (Perfis de persuasão)
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
pesquisa-eleitoral-df  memoria_cultural  brislin-translator
    (C-Agentes)        (Viés WEIRD)      (IACCP 2026)
        │                │                │
        └────────┬───────┴────────────────┘
                 │
           AGENTES BRASILEIROS
           (simulação cultural)

autocoder-master ──→ Gera projetos (Análise Bardin)
        │
        ↓
opencode-academy ──→ Ensina não-programadores
        │
        ↓
   Open Code docs ──→ Metodologia Ralph Wiggum
```

**Tema central:** SIMULAÇÃO DE HUMANOS BRASILEIROS
- Eleitores sintéticos (pesquisa)
- Agentes culturais (memória)
- Tradução transcultural (brislin)
- Todas servem ao doutorado

---

## 📋 FILA DE EXPLORAÇÃO

### ✅ Concluídas
- [x] pesquisa-eleitoral-df (CLAUDE.md completo)
- [x] reconvencao-igor-melissa (claude.md completo)
- [x] memoria_cultural (PLANO_UNIFICADO)
- [x] autocoder-master (CLAUDE.md completo)
- [x] brislin-translator (CLAUDE.md completo)
- [x] opencode-academy (README.md)
- [x] Open Code orientações (relatório lido)

### 🔄 Para futuro
- [ ] Ler sessões antigas do Claude Code (~255 sessões)
- [ ] Mapear .claude/skills globais
- [ ] Explorar claude-workspace
- [ ] Verificar pesquisa-eleitoral-df-clean

---

## 📊 RESUMO ESTATÍSTICO

| Projeto | Linhas CLAUDE.md | Stack Principal | Prioridade |
|---------|------------------|-----------------|------------|
| pesquisa-eleitoral-df | ~500 | Next.js + FastAPI | ⭐⭐⭐⭐⭐ |
| reconvencao | ~400 | Docs + RAG | ⭐⭐⭐⭐⭐ |
| memoria_cultural | ~800 | Teoria + Arquitetura | ⭐⭐⭐⭐ |
| autocoder-master | ~400 | Python + React | ⭐⭐⭐⭐ |
| brislin-translator | ~350 | HTML + Claude API | ⭐⭐⭐⭐ |
| opencode-academy | ~100 | Next.js | ⭐⭐⭐ |

---

*Este arquivo é atualizado continuamente.*
*Última exploração: 2026-01-27*
*Protocolo: INTEIA - Engenharia de Contexto*
