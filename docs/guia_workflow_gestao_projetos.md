# Guia de Workflow: Gestão de Projetos de Longo Prazo

Este guia detalha o processo completo para gerenciar projetos que requerem múltiplas sessões.

## Índice

1. [Filosofia do Sistema](#filosofia-do-sistema)
2. [Iniciando um Novo Projeto](#iniciando-um-novo-projeto)
3. [Continuando um Projeto Existente](#continuando-um-projeto-existente)
4. [Gerenciando Tarefas](#gerenciando-tarefas)
5. [Padrões de Comunicação](#padrões-de-comunicação)
6. [Resolução de Problemas](#resolução-de-problemas)

---

## Filosofia do Sistema

### Princípios Fundamentais

1. **Memória Persistente via Arquivos**
   - Claude não lembra entre sessões
   - PROJECT_SPEC.md e PROGRESS.md são a memória do projeto
   - Mantenha-os sempre atualizados

2. **Progresso Incremental**
   - Pequenos passos são mais seguros que grandes saltos
   - Uma tarefa por vez, bem feita
   - Commit frequente = progresso preservado

3. **Verificação Obrigatória**
   - Nunca assuma que funciona - teste
   - Nunca marque completo sem verificar
   - Regressões são caras de corrigir

4. **Documentação como Código**
   - Specs e progresso são tão importantes quanto código
   - Atualize docs junto com implementação
   - Docs desatualizados são piores que sem docs

---

## Iniciando um Novo Projeto

### Passo 1: Definir o Escopo

Antes de qualquer código, responda:
- O que este projeto faz?
- Quem vai usar?
- Qual o critério de "pronto"?

### Passo 2: Criar PROJECT_SPEC.md

```markdown
# Exemplo Mínimo Viável

## Objetivo
CLI para converter arquivos Markdown em HTML

## Funcionalidades
1. Ler arquivo .md
2. Converter para HTML
3. Salvar arquivo .html

## Stack
- Node.js
- marked (parser MD)

## Critério de Sucesso
- `node cli.js input.md` gera `input.html`
```

### Passo 3: Criar PROGRESS.md

Decomponha em tarefas:

```markdown
# Progresso: MD to HTML CLI

## Status: Não Iniciado
Última atualização: 2024-01-15

## Tarefas

### Setup
- [ ] 1. npm init
- [ ] 2. Instalar marked
- [ ] 3. Criar estrutura de arquivos

### Core
- [ ] 4. Ler arquivo de entrada
- [ ] 5. Converter MD para HTML
- [ ] 6. Salvar arquivo de saída

### Polish
- [ ] 7. Tratamento de erros
- [ ] 8. Mensagens de ajuda (--help)
```

### Passo 4: Primeiro Commit

```bash
git init
git add PROJECT_SPEC.md PROGRESS.md
git commit -m "docs: initial project specification"
```

---

## Continuando um Projeto Existente

### Ritual de Início de Sessão

Sempre que retomar um projeto:

```markdown
## Checklist de Retomada

1. [ ] Abrir PROJECT_SPEC.md
   - Relembrar objetivo e escopo
   - Verificar se specs ainda estão válidas

2. [ ] Abrir PROGRESS.md
   - Ver última sessão
   - Identificar tarefas completas
   - Encontrar próxima tarefa

3. [ ] Verificar estado do código
   - git status
   - npm run build (ou equivalente)
   - Garantir que está em estado funcional

4. [ ] Identificar tarefa atual
   - Primeira tarefa não marcada
   - Verificar dependências
   - Entender escopo da tarefa
```

### Comando Rápido para Claude

> "Leia PROJECT_SPEC.md e PROGRESS.md e me diga: qual o objetivo do projeto, quantas tarefas estão completas, e qual é a próxima tarefa?"

---

## Gerenciando Tarefas

### Anatomia de uma Boa Tarefa

```markdown
- [ ] **5. Implementar autenticação JWT**
  - Descrição: Sistema de login com tokens JWT
  - Depende de: #3 (modelo de usuário), #4 (API base)
  - Critério: Login retorna token válido por 24h
  - Arquivos: src/auth/*, src/middleware/auth.ts
```

Elementos essenciais:
- **Número sequencial**: Para referência fácil
- **Nome claro**: Ação + objeto
- **Descrição**: O que exatamente fazer
- **Dependências**: O que precisa estar pronto antes
- **Critério**: Como saber que está feito

### Marcando Tarefa como Completa

**ANTES de marcar, verifique:**

```bash
# 1. Código compila?
npm run build

# 2. Linting passa?
npm run lint

# 3. Testes passam? (se houver)
npm run test

# 4. Funciona manualmente?
# [testar a funcionalidade]
```

**DEPOIS de verificar:**

```markdown
# Atualizar PROGRESS.md

- [x] **5. Implementar autenticação JWT**
  - Descrição: Sistema de login com tokens JWT
  - Completo em: 2024-01-15
  - Notas: Usando biblioteca jsonwebtoken, tokens expiram em 24h
```

### Adicionando Novas Tarefas

Durante implementação, podem surgir novas necessidades:

```markdown
# Se descobrir nova tarefa necessária:

### Tarefas Adicionadas Durante Desenvolvimento
- [ ] **9. [NOVO] Adicionar rate limiting na API**
  - Motivo: Descoberto durante implementação de auth
  - Prioridade: Média
  - Adicionado em: 2024-01-15
```

### Pulando Tarefas (Com Cautela)

Às vezes uma tarefa está bloqueada. Documente:

```markdown
- [ ] **6. Integrar com API externa** ⏸️ BLOQUEADO
  - Bloqueador: Aguardando credenciais de acesso
  - Bloqueado desde: 2024-01-15
  - Ação necessária: Contatar admin para obter API key
```

---

## Padrões de Comunicação

### Frases Úteis para Claude

**Iniciar sessão:**
> "Estou retomando o projeto [nome]. Leia os arquivos PROJECT_SPEC.md e PROGRESS.md e me oriente sobre a próxima tarefa."

**Verificar progresso:**
> "Qual o status atual do projeto? Quantas tarefas completas e pendentes?"

**Completar tarefa:**
> "Acabei de implementar a tarefa #5. Execute os testes, e se tudo passar, atualize PROGRESS.md marcando como completa."

**Encontrar problemas:**
> "Estou tendo dificuldade com a tarefa #7. Me explique o que já foi feito e sugira próximos passos."

**Encerrar sessão:**
> "Preciso parar por hoje. Atualize PROGRESS.md com um resumo do que fizemos e identifique claramente a próxima tarefa."

---

## Resolução de Problemas

### Problema: Não sei por onde começar

**Solução**: Verifique as dependências no PROGRESS.md
- Encontre tarefas sem dependências não completas
- Se todas têm dependências, priorize as bloqueadoras

### Problema: Tarefa muito grande

**Solução**: Decomponha em subtarefas

```markdown
# Antes (muito grande)
- [ ] 5. Implementar sistema de pagamentos

# Depois (decomposta)
- [ ] 5a. Integrar SDK do Stripe
- [ ] 5b. Criar modelo de transação
- [ ] 5c. Implementar checkout básico
- [ ] 5d. Adicionar webhooks de confirmação
- [ ] 5e. Testar fluxo completo
```

### Problema: PROGRESS.md desatualizado

**Solução**: Reconciliar estado

```markdown
1. Liste arquivos modificados: git log --oneline -20
2. Compare com PROGRESS.md
3. Atualize tarefas baseado no código real
4. Documente a reconciliação
```

### Problema: Projeto abandonado há muito tempo

**Solução**: Sessão de reconhecimento

```markdown
1. Ler PROJECT_SPEC.md - objetivo ainda é válido?
2. Ler PROGRESS.md - onde parou?
3. git log - o que foi feito depois do último update?
4. npm install && npm run build - projeto ainda funciona?
5. Atualizar PROGRESS.md com estado real
6. Decidir: continuar, pivotar, ou arquivar
```

---

## Fluxo Visual

```
┌─────────────────────────────────────────────────────────┐
│                    INÍCIO DE SESSÃO                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │  Ler PROJECT_SPEC.md  │
              │  Ler PROGRESS.md      │
              └───────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │  Identificar próxima  │
              │  tarefa disponível    │
              └───────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │    Implementar        │
              │    tarefa             │
              └───────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │    Verificar          │
              │    (build, lint, test)│
              └───────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        ┌──────────┐            ┌──────────────┐
        │  Passou  │            │  Falhou      │
        └──────────┘            └──────────────┘
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │ Marcar completa  │      │ Corrigir erros   │
    │ em PROGRESS.md   │      │ e tentar de novo │
    └──────────────────┘      └──────────────────┘
              │                         │
              ▼                         │
    ┌──────────────────┐               │
    │ Mais tarefas?    │◄──────────────┘
    └──────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
┌────────┐        ┌────────────┐
│  Sim   │        │    Não     │
└────────┘        └────────────┘
    │                   │
    │                   ▼
    │         ┌──────────────────┐
    │         │ Projeto completo!│
    │         │ Atualizar status │
    │         └──────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│           CONTINUAR OU ENCERRAR SESSÃO                   │
│  - Atualizar PROGRESS.md                                 │
│  - Commitar código                                       │
│  - Documentar próximos passos                            │
└─────────────────────────────────────────────────────────┘
```

---

## Conclusão

Este sistema é simples por design. A complexidade está no projeto, não na gestão.

**Lembre-se:**
- Arquivos são a memória
- Verificação previne retrabalho
- Progresso documentado é progresso preservado
