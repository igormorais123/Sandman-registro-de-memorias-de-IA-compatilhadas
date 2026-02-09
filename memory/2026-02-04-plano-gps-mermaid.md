# PLANO: GPS com Diagramas Mermaid

**Data:** 2026-02-04
**Projetos:** Pesquisa Eleitoral DF + Reconvenção Melissa

---

## 🎯 OBJETIVO

Criar sistema de diagramas Mermaid que funciona como "GPS" para IAs navegarem os projetos. 
AI processa Mermaid ~10x mais rápido que texto descritivo.

---

## 📁 ESTRUTURA PROPOSTA

### Para cada projeto:

```
projeto/
├── ai/
│   └── diagrams/
│       ├── 00_OVERVIEW.md          # Visão geral do projeto
│       ├── 01_FOLDER_MAP.md        # Mapa de pastas
│       ├── 02_DATA_FLOW.md         # Fluxo de dados
│       ├── 03_USER_FLOWS.md        # Jornadas do usuário
│       ├── 04_API_ROUTES.md        # Rotas da API (se app)
│       ├── 05_DECISION_TREES.md    # Árvores de decisão
│       └── README.md               # Como usar os diagramas
```

---

## 📊 DIAGRAMAS POR PROJETO

### PROJETO 1: Pesquisa Eleitoral DF

| Diagrama | Conteúdo | Prioridade |
|----------|----------|------------|
| 00_OVERVIEW | Sistema completo: Frontend ↔ Backend ↔ DB ↔ Claude API | 🔴 Alta |
| 01_FOLDER_MAP | Estrutura de pastas com propósito de cada uma | 🔴 Alta |
| 02_DATA_FLOW | Eleitor → Entrevista → Resposta → Agregação → Relatório | 🔴 Alta |
| 03_ENTREVISTA_FLOW | Fluxo completo de uma entrevista | 🟡 Média |
| 04_API_ROUTES | Todas as rotas do backend | 🟡 Média |
| 05_CONSULTORES | Fluxo de consulta aos consultores lendários | 🟡 Média |
| 06_DEPLOY | Fluxo de deploy Vercel + Render | 🟢 Baixa |

### PROJETO 2: Reconvenção Melissa

| Diagrama | Conteúdo | Prioridade |
|----------|----------|------------|
| 00_OVERVIEW | Estrutura do caso: Partes, Documentos, Timeline | 🔴 Alta |
| 01_FOLDER_MAP | Onde está cada tipo de documento | 🔴 Alta |
| 02_CASO_FLOW | Fluxo processual: Petições → Audiências → Decisões | 🔴 Alta |
| 03_ARGUMENTOS | Árvore de argumentos Igor vs Thaís | 🟡 Média |
| 04_PROVAS | Mapa de provas por categoria | 🟡 Média |
| 05_CONSULTORES | Mapa de especialistas e suas áreas | 🟡 Média |
| 06_TIMELINE | Linha do tempo do caso | 🟢 Baixa |

---

## 🔧 EXEMPLO DE DIAGRAMA

### 01_FOLDER_MAP.md (Pesquisa Eleitoral)

```markdown
# Mapa de Pastas - Pesquisa Eleitoral DF

## Navegação Rápida

graph TD
    ROOT[pesquisa-eleitoral-df/] --> BACKEND[backend/]
    ROOT --> FRONTEND[frontend/]
    ROOT --> AGENTES[agentes/]
    ROOT --> SCRIPTS[scripts/]
    ROOT --> DOCS[docs/]
    
    BACKEND --> B_API[app/api/rotas/]
    BACKEND --> B_SERV[app/servicos/]
    BACKEND --> B_MOD[app/modelos/]
    
    FRONTEND --> F_COMP[src/components/]
    FRONTEND --> F_APP[src/app/]
    FRONTEND --> F_SERV[src/services/]
    
    AGENTES --> AG_JSON[*.json - Dados eleitores]
    
    click B_API "#api-rotas"
    click F_COMP "#componentes"

## Decisão: Onde Editar?

flowchart TD
    Q1{O que preciso fazer?}
    Q1 -->|Modificar API| API[backend/app/api/rotas/]
    Q1 -->|Modificar UI| UI[frontend/src/components/]
    Q1 -->|Dados eleitores| DATA[agentes/*.json]
    Q1 -->|Lógica IA| IA[backend/app/servicos/claude_servico.py]
    Q1 -->|Deploy| DEPLOY[Ver 06_DEPLOY.md]
```

---

## 📋 PLANO DE EXECUÇÃO

### Fase 1: Setup (30 min)
- [ ] Criar pasta `ai/diagrams/` em ambos os projetos
- [ ] Criar README.md com instruções de uso
- [ ] Criar template base para diagramas

### Fase 2: Pesquisa Eleitoral (2h)
- [ ] 00_OVERVIEW.md - Visão geral do sistema
- [ ] 01_FOLDER_MAP.md - Mapa de pastas
- [ ] 02_DATA_FLOW.md - Fluxo de dados

### Fase 3: Reconvenção (2h)
- [ ] 00_OVERVIEW.md - Visão geral do caso
- [ ] 01_FOLDER_MAP.md - Mapa de documentos
- [ ] 02_CASO_FLOW.md - Fluxo processual

### Fase 4: Testes (30 min)
- [ ] Testar carregamento dos diagramas no Claude Code
- [ ] Verificar se navegação está clara
- [ ] Ajustar baseado em feedback

---

## 💡 COMO USAR (após implementado)

```bash
# Carregar todos os diagramas no contexto
claude /append-system-prompt "$(cat ai/diagrams/*.md)"

# Ou criar alias
alias cpe='cd /mnt/c/Agentes && claude /append-system-prompt "$(cat ai/diagrams/*.md)"'
alias cre='cd /mnt/c/Users/IgorPC/.claude/projects/reconvencao-igor-melissa && claude /append-system-prompt "$(cat ai/diagrams/*.md)"'
```

---

## ⏱️ ESTIMATIVA

| Projeto | Tempo | Complexidade |
|---------|-------|--------------|
| Pesquisa Eleitoral | 2-3h | Média (app full-stack) |
| Reconvenção | 1-2h | Baixa (documentos) |
| **Total** | **3-5h** | - |

---

*Posso começar agora ou quer revisar/ajustar o plano primeiro?*
