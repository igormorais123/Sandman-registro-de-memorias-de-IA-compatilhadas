# Skill: Sistema de Gestão de Projetos de Longo Prazo

## Metadados

```yaml
name: skilldelongoprazosistema
description: Sistema de gestão para projetos complexos que requerem múltiplas sessões
triggers:
  - "projeto de longo prazo"
  - "projeto complexo"
  - "múltiplas sessões"
  - "gestão de projeto"
  - "decomposição de tarefas"
  - "/longterm"
  - "/projeto"
```

## Quando Usar Esta Skill

Use este sistema quando:
- O projeto levará **mais de uma sessão** para completar
- Existem **múltiplas tarefas interdependentes**
- Você precisa **retomar trabalho** de sessões anteriores
- O escopo é **complexo demais** para manter na memória

**NÃO use** para:
- Tarefas simples que cabem em uma sessão
- Correções pontuais de bugs
- Perguntas e respostas rápidas

## Workflow em 5 Fases

### Fase 1: Especificação (Início do Projeto)

Antes de escrever código, crie um documento de especificação:

1. Crie o arquivo `PROJECT_SPEC.md` na raiz do projeto
2. Use o template em `references/project-spec-template.md`
3. Defina claramente:
   - Objetivo do projeto
   - Funcionalidades principais
   - Tecnologias a usar
   - Critérios de sucesso

```markdown
# Exemplo de estrutura mínima
## Objetivo
[Uma frase clara do que o projeto faz]

## Funcionalidades
1. [Feature 1]
2. [Feature 2]
...

## Stack Técnica
- [Tecnologia 1]
- [Tecnologia 2]
```

### Fase 2: Decomposição (Quebrar em Tarefas)

Transforme a especificação em tarefas gerenciáveis:

1. Crie o arquivo `PROGRESS.md` na raiz do projeto
2. Liste todas as tarefas em ordem lógica de execução
3. Use o formato de checklist:

```markdown
# Progresso do Projeto

## Status: Em Andamento
Última atualização: [DATA]

## Tarefas

### Setup (Prioridade: Alta)
- [ ] 1. Configurar ambiente de desenvolvimento
- [ ] 2. Criar estrutura de diretórios
- [ ] 3. Instalar dependências

### Core (Prioridade: Alta)
- [ ] 4. Implementar [feature principal]
- [ ] 5. Implementar [feature secundária]

### Finalização (Prioridade: Média)
- [ ] 6. Testes
- [ ] 7. Documentação
```

### Fase 3: Execução (Uma Tarefa por Vez)

Para cada tarefa:

1. **Leia PROGRESS.md** para ver onde parou
2. **Identifique a próxima tarefa** não marcada
3. **Implemente completamente** antes de passar adiante
4. **Não pule tarefas** - siga a ordem definida

```markdown
# Ao iniciar uma sessão, sempre:
1. Ler PROGRESS.md
2. Verificar última tarefa completa
3. Começar a próxima tarefa pendente
```

### Fase 4: Verificação (Antes de Marcar Feito)

**NUNCA marque uma tarefa como completa sem verificar:**

1. O código compila/executa sem erros?
2. A funcionalidade está funcionando como esperado?
3. Não quebrou nada que funcionava antes?

```bash
# Verificações típicas
npm run build    # ou equivalente
npm run lint     # verificar qualidade
npm run test     # se houver testes
```

### Fase 5: Atualização de Progresso

Após verificar, atualize o PROGRESS.md:

1. Marque a tarefa como completa: `- [x]`
2. Adicione notas se necessário
3. Atualize a data de última modificação
4. Identifique a próxima tarefa

```markdown
# Antes
- [ ] 4. Implementar autenticação

# Depois
- [x] 4. Implementar autenticação
  - Notas: Usando JWT, tokens expiram em 24h
```

## Melhores Práticas

### Ao Iniciar Cada Sessão

```markdown
## Checklist de Início de Sessão
1. [ ] Ler PROJECT_SPEC.md para lembrar o objetivo
2. [ ] Ler PROGRESS.md para ver status atual
3. [ ] Identificar próxima tarefa a executar
4. [ ] Verificar se há bloqueadores
```

### Durante a Implementação

- **Foco em uma tarefa**: Complete antes de iniciar outra
- **Commits frequentes**: Salve progresso regularmente
- **Documente decisões**: Adicione notas em PROGRESS.md
- **Não refatore demais**: Foque no escopo definido

### Ao Encerrar Sessão

```markdown
## Checklist de Fim de Sessão
1. [ ] Tarefa atual está completa ou em ponto seguro?
2. [ ] PROGRESS.md está atualizado?
3. [ ] Código está commitado?
4. [ ] Próxima tarefa está clara?
```

### Gestão de Dependências

Se uma tarefa depende de outra:

```markdown
- [ ] 5. Implementar dashboard
  - Depende de: #3 (autenticação), #4 (API)
```

Execute as dependências primeiro.

## Templates Disponíveis

- `references/project-spec-template.md` - Template para especificação
- `references/progress-template.md` - Template para rastreamento
- `references/workflow-guide.md` - Guia detalhado do processo

## Comandos Rápidos

| Ação | Comando/Instrução |
|------|-------------------|
| Iniciar projeto | "Criar especificação para [projeto]" |
| Ver status | "Mostrar progresso do projeto" |
| Próxima tarefa | "Qual a próxima tarefa?" |
| Marcar completa | "Marcar tarefa [N] como completa" |
| Adicionar tarefa | "Adicionar tarefa: [descrição]" |

## Exemplo Completo

```markdown
# PROJECT_SPEC.md
## Objetivo
Criar um CLI para gerenciar notas em Markdown

## Funcionalidades
1. Criar notas
2. Listar notas
3. Buscar por conteúdo
4. Exportar para PDF

## Stack
- Node.js
- Commander.js (CLI)
- SQLite (armazenamento)
```

```markdown
# PROGRESS.md
## Status: Em Andamento
Última atualização: 2024-01-15

## Tarefas

### Setup
- [x] 1. Inicializar projeto Node.js
- [x] 2. Configurar TypeScript
- [x] 3. Instalar dependências

### Core
- [x] 4. Implementar comando 'create'
- [ ] 5. Implementar comando 'list'    <- PRÓXIMA
- [ ] 6. Implementar comando 'search'
- [ ] 7. Implementar comando 'export'

### Finalização
- [ ] 8. Escrever testes
- [ ] 9. Documentar uso no README
```

## Princípios Fundamentais

1. **Especifique antes de codificar** - Clareza economiza tempo
2. **Decomponha em tarefas pequenas** - Progresso visível motiva
3. **Uma tarefa por vez** - Foco produz qualidade
4. **Verifique antes de marcar feito** - Evite retrabalho
5. **Documente o progresso** - Sessões futuras agradecem
