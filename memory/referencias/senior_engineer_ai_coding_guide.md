# Senior Engineer's Guide to AI Coding

**Fonte:** How I AI Podcast - John Lindquist (egghead.io)
**Video:** https://youtu.be/LvLdNkgO-N0
**Processado:** 2026-02-04

---

## 🎯 RESUMO EXECUTIVO

O vídeo ensina técnicas avançadas para engenheiros seniores usarem Claude Code e Cursor de forma mais eficiente. Foco em: **context loading**, **custom hooks**, e **automação**.

---

## 1. 📊 DIAGRAMAS MERMAID COMO CONTEXTO

### Por que usar:
- AI processa diagramas Mermaid **muito melhor** que humanos
- Comprime lógica complexa em poucas linhas de texto
- Elimina necessidade de file reads e codebase exploration
- Resultados muito mais rápidos e confiáveis

### Como implementar:

```bash
# Criar pasta de memória/diagramas no repo
mkdir -p ai/diagrams

# Carregar todos os diagramas no system prompt
claude /append-system-prompt "$(cat ai/diagrams/*.md)"
```

### Estrutura sugerida:
```
projeto/
├── ai/
│   └── diagrams/
│       ├── auth-flow.md
│       ├── database-ops.md
│       └── user-actions.md
```

### Quando gerar diagramas:
- **NÃO** no início do projeto
- **SIM** após código funcionando (spike → working → diagram)
- Pode ser automatizado em GitHub Actions no merge de PRs

---

## 2. ⚡ ALIASES PARA EFICIÊNCIA

### Exemplos (zsh/bash):

```bash
# Claude com bypass de permissões (perigoso mas rápido)
alias x='claude --dangerously-skip-permissions'

# Claude com modelo Haiku (rápido, menos inteligente)
alias h='claude --model haiku'

# Claude com diagramas pré-carregados
alias cdi='claude /append-system-prompt "$(cat ai/diagrams/*.md)"'

# Claude para projeto específico
alias cproj='claude /append-system-prompt "$(cat projeto-x/context/*.md)"'
```

### Benefício:
- Comandos de 1-2 letras para workflows frequentes
- Lançar versões específicas de Claude instantaneamente

---

## 3. 🛑 STOP HOOKS (Game Changer!)

### O que são:
Hooks que rodam **quando Claude termina uma tarefa**, antes de devolver controle ao usuário.

### Configuração:

```bash
# Ver opções de hooks
claude /hooks

# Adicionar stop hook
claude /hooks add stop
```

### Arquivo de configuração:
`.claude/settings.local.json` (local) ou `.claude/settings.json` (time)

### Exemplo de Stop Hook (TypeScript):

```typescript
// claude-hooks/index.ts
import { HookInput } from '@anthropic-ai/claude-code-sdk';

const input: HookInput = JSON.parse(process.stdin.read());

// 1. Verificar se houve mudanças de arquivos
if (input.filesChanged) {
  
  // 2. Rodar type check
  const result = execSync('bun type-check --quiet', { encoding: 'utf-8' });
  
  if (result.includes('error')) {
    // 3a. Se tem erro, mandar de volta pro Claude corrigir
    console.log(JSON.stringify({
      block: true,
      message: `Please fix TypeScript errors:\n${result}`
    }));
  } else {
    // 3b. Se não tem erro, auto-commit
    console.log(JSON.stringify({
      message: "Please commit these changes with a descriptive message"
    }));
  }
}
```

### Casos de uso para Stop Hooks:
- ✅ TypeScript/type check
- ✅ Linting/formatting
- ✅ Verificar dependências circulares
- ✅ Checar código duplicado
- ✅ Complexidade de código
- ✅ Auto-commit se tudo OK
- ✅ Gerar documentação automática

### IMPORTANTE:
- Use `console.log()` para comunicar com Claude
- Use `console.error()` para debug (não interfere)
- Hooks locais vs compartilhados com time

---

## 4. 🎤 DICTATION/VOZ

John usa dictation **constantemente**:
- Mais rápido que digitar
- Brain dump direto no terminal
- Qualquer ideia → novo terminal → falar → AI implementa

---

## 5. 🛠️ CLIs CUSTOMIZADAS

### Filosofia:
> "Build every idea you have"

### Exemplo mostrado:
CLI que gera imagens de websites via Gemini com prompts pré-configurados.

### Por que CLI > Web UI:
- UI constrita = menos distrações
- Não precisa de localhost/browser
- Foco no essencial
- Mais rápido para prototipar

---

## 6. 🧠 MINDSET PARA ENGENHEIROS SENIORES

### Pergunta-chave:
> "Se eu tivesse infinitos juniors disponíveis 24/7, que fariam o trabalho que eu faria se tivesse tempo ilimitado e zero reuniões — o que eu faria quando um ticket chegasse?"

### Resposta típica:
1. Investigar quem escreveu o código
2. Ver histórico de mudanças
3. Criar tech spec detalhado
4. Identificar riscos
5. Publicar para review do time
6. Pedir feedback de senior

**TUDO ISSO pode ser um prompt!**

### Workflow automático sugerido:
- Issue aberta → Claude automaticamente:
  - Encontra arquivos relevantes
  - Identifica quem tocou
  - Analisa impactos/riscos
  - Gera primeiro rascunho de solução
  - Cria documentação

---

## 7. 🔄 QUANDO CLAUDE "SAI DOS TRILHOS"

### Sinais:
- Você quer ir para um lado, Claude insiste em outro
- Múltiplas correções não resolvem

### Solução:
1. **Exportar conversa** (comando export)
2. **Jogar em outro modelo** (ChatGPT, Gemini Deep Think)
3. Pedir "segunda opinião" sobre onde deu errado
4. **Reverter para commit anterior**
5. **Começar de novo** com prompt revisado

> "Starting over works every time"

### Prevenção:
- Usar **Planning Mode** (disponível em Claude Code e Cursor)
- Elimina grande parte do "drift"

---

## 8. 📝 APLICAÇÕES PARA CLAWDBOT

### Implementar agora:

1. **Criar pasta `ai/diagrams/`** no workspace com:
   - Diagrama do fluxo do Gateway
   - Diagrama de sessões
   - Diagrama de plugins/canais

2. **Alias para carregar contexto:**
   ```bash
   alias cdiag='claude /append-system-prompt "$(cat /root/clawd/ai/diagrams/*.md)"'
   ```

3. **Stop hook para TypeScript** (se aplicável aos projetos)

4. **Automatizar documentação** após PRs

### Ideias futuras:
- CLI para gerar briefings
- Hook que verifica segurança antes de commit
- Diagrama automático de novos features

---

## 🔗 RECURSOS

- **Newsletter:** AI Dev Essentials (John Lindquist)
- **Cursos:** egghead.io
- **Sponsor:** WorkOS (enterprise features for AI apps)
- **Sponsor:** Tines (workflow automation)

---

*Processado por NEXO — 2026-02-04*
