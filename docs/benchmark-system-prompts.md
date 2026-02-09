# Benchmark de System Prompts: Claude Code vs Concorrentes

**Data**: Janeiro 2026
**Autor**: Claude Opus 4.5 (auto-analise)
**Sistemas analisados**: Claude Code (v1 Sonnet4, v2 Sonnet4.5, Opus4.5 atual), Devin AI, Replit, v0 (Vercel), Manus Agent, Augment Code, VSCode Agent (GitHub Copilot), Amp (Sourcegraph)

---

## Sumario Executivo

Analisei os system prompts de 8 ferramentas de IA para codificacao. Claude Code esta entre os mais completos, mas existem **12 padroes concretos** de outros sistemas que podem melhorar significativamente as sessoes do usuario. Este documento separa o que vale a pena replicar do que nao agrega valor.

---

## PARTE 1 -- O Que Claude Code Ja Faz Bem (Nao Precisa Mudar)

| Capacidade | Status |
|---|---|
| Read antes de Edit (obrigatorio) | Presente e enforced |
| Anti-over-engineering explicito | Forte (5 regras claras) |
| Paralelismo de ferramentas | Suportado e incentivado |
| Subagentes especializados (Explore, Plan, Bash) | Presente desde Opus 4.5 |
| Plan Mode com aprovacao do usuario | Presente |
| Git safety protocol (nunca force push, nunca skip hooks) | Forte |
| Code references com file:line_number | Presente |
| AskUserQuestion para clarificacao | Presente |
| MCP server integration | Presente |
| Task tracking (TaskCreate/Update/List) | Presente |
| WebSearch + WebFetch | Presente |

**Veredito**: A base do Claude Code e solida. Os gaps estao em **padroes comportamentais**, nao em ferramentas.

---

## PARTE 2 -- Padroes Que Valem a Pena Aprender

### 1. REGRA DOS 3 RETRIES (Devin AI, Copilot, Amp)

**O que e**: Limite explicito de 3 tentativas para resolver o mesmo erro. Apos 3 falhas, escalar para o usuario em vez de continuar tentando.

**Quem faz**: Devin AI (CI retry limit), Copilot (edit error recovery), Amp (fix iteration limit)

**Por que vale a pena**: Claude Code atualmente pode entrar em loops de correcao infinitos. O INTEIA ja recomenda "/clear apos 2 falhas", mas nao ha regra embutida no sistema para parar automaticamente.

**Como aplicar no CLAUDE.md**:
```
### Regra de Retry
- Maximo 3 tentativas para corrigir o mesmo erro
- Se falhar 3x: PARAR, reportar o que tentou, e perguntar ao usuario
- Nunca continuar em loop sem progresso visivel
```

**Nivel de impacto**: ALTO

---

### 2. NUNCA MODIFICAR TESTES PARA PASSAR (Devin AI)

**O que e**: Regra explicita proibindo enfraquecer testes para faze-los passar. O problema esta no codigo, nao no teste.

**Quem faz**: Devin AI (regra hard-coded)

**Por que vale a pena**: Este e um dos failure modes mais comuns de agentes IA -- fazer testes passarem removendo assertions ou relaxando condicoes. Claude Code nao tem esta regra explicita.

**Como aplicar no CLAUDE.md**:
```
### Testes
- NUNCA modificar testes existentes para faze-los passar (a menos que a tarefa seja explicitamente sobre os testes)
- Se testes falham: o problema esta no codigo, nao no teste
- Sempre considerar que a causa raiz pode estar no codigo sendo testado
```

**Nivel de impacto**: ALTO

---

### 3. VERIFICACAO AUTOMATICA POS-EDICAO (Copilot, Amp, Augment Code)

**O que e**: Apos cada edicao significativa, rodar automaticamente verificacao (typecheck, lint, diagnostics) sem esperar o usuario pedir.

**Quem faz**: Copilot GPT-5 ("After editing a file, you MUST call get_errors"), Amp ("MUST run get_diagnostics and lint/typecheck"), Augment GPT-5 ("proactively perform safe, low-cost verification runs")

**Por que vale a pena**: Claude Code so roda lint/typecheck no final, se os comandos forem conhecidos. Verificacao incremental pega erros mais cedo e evita acumular problemas.

**Como aplicar no CLAUDE.md**:
```
### Verificacao Incremental
- Apos cada edicao significativa (nova funcao, refatoracao, mudanca de tipo):
  rodar lint/typecheck se os comandos estiverem disponiveis
- Ordem de verificacao: typecheck -> lint -> testes -> build
- Nao esperar o final para descobrir erros
```

**Nivel de impacto**: ALTO

---

### 4. EXPLORE ANTES DE AGIR -- VERSIONADO (Devin AI, Augment Code)

**O que e**: Separacao arquitetural entre fase de exploracao (so leitura) e fase de execucao (escrita). Devin AI implementa isso como dois modos distintos. Augment Code usa a regra "investigate first task" obrigatoria.

**Quem faz**: Devin AI (Planning Mode vs Standard Mode), Augment Code GPT-5 ("Create tasklist with first task 'Investigate/Understand the problem' as IN_PROGRESS")

**Por que vale a pena**: O INTEIA ja preconiza "exploracao antes de acao", mas nao forca a criacao de uma tarefa explicita de investigacao como primeiro passo. Augment Code vai alem: a primeira tarefa SEMPRE e investigar.

**Como aplicar no CLAUDE.md**:
```
### Primeira Tarefa Sempre = Investigar
- Para tarefas nao-triviais, o primeiro passo deve ser SEMPRE:
  "Investigar/Entender o problema" (Read, Grep, Explore)
- So criar plano de implementacao APOS completar investigacao
- Nunca iniciar edicao sem ter entendido o contexto completo
```

**Nivel de impacto**: MEDIO (ja parcialmente coberto pelo INTEIA)

---

### 5. REGRA ">3 ARQUIVOS = MOSTRAR PLANO" (Amp)

**O que e**: Se uma mudanca vai afetar mais de 3 arquivos ou multiplos subsistemas, o agente DEVE mostrar um plano curto antes de comecar a editar.

**Quem faz**: Amp ("No surprise edits: if changes affect >3 files or multiple subsystems, show a short plan first")

**Por que vale a pena**: Claude Code pode iniciar edicoes em multiplos arquivos sem avisar. Esta regra e um gatilho concreto e mensuravel para ativar Plan Mode automaticamente.

**Como aplicar no CLAUDE.md**:
```
### Gatilho Automatico de Planejamento
- Se a tarefa vai afetar > 3 arquivos: OBRIGATORIO mostrar plano antes
- Se vai mudar tipos/interfaces compartilhados: OBRIGATORIO mostrar plano
- Plano pode ser curto (5-10 linhas), mas deve existir
```

**Nivel de impacto**: ALTO

---

### 6. HIERARQUIA DE INFORMACAO (Manus)

**O que e**: Prioridade explicita de fontes de informacao: dados da API/docs > busca web > conhecimento interno do modelo.

**Quem faz**: Manus ("Authoritative data from datasource API > Web search results > Model's internal knowledge")

**Por que vale a pena**: Claude Code nao tem prioridade formal de fontes. Isso pode levar a respostas baseadas em conhecimento desatualizado quando documentacao atualizada esta disponivel via MCP/context7.

**Como aplicar no CLAUDE.md**:
```
### Prioridade de Fontes
1. Documentacao oficial (via MCP context7, docs online)
2. Codigo existente no projeto (via Read/Grep)
3. Busca web (WebSearch)
4. Conhecimento interno (ultimo recurso para coisas que mudam frequentemente)
```

**Nivel de impacto**: MEDIO

---

### 7. RELATAR PROBLEMAS DE AMBIENTE, NAO CONSERTAR (Devin AI)

**O que e**: Quando encontrar problemas de ambiente (Docker, permissoes, dependencias corrompidas), REPORTAR ao usuario e continuar trabalhando de outra forma, em vez de gastar tokens tentando consertar.

**Quem faz**: Devin AI ("Report environment issues, then find a way to continue without fixing them")

**Por que vale a pena**: Claude Code frequentemente gasta muitos tokens tentando consertar problemas de ambiente que sao do dominio do usuario (paths do Windows, versoes de Node, permissoes). Melhor avisar e contornar.

**Como aplicar no CLAUDE.md**:
```
### Problemas de Ambiente
- Se encontrar problema de ambiente (permissao, versao, path, Docker):
  1. Reportar claramente o que encontrou
  2. Sugerir como o usuario pode resolver
  3. Tentar contornar (ex: usar outro caminho, pular teste local)
  4. NAO gastar mais de 2 tentativas tentando consertar ambiente
```

**Nivel de impacto**: ALTO (especialmente em Windows)

---

### 8. PLANEJAMENTO INCREMENTAL vs BULK (Augment Code GPT-5)

**O que e**: Em vez de criar uma lista enorme de tarefas no inicio, criar apenas a primeira tarefa (investigar), e ir adicionando as proximas conforme aprende mais.

**Quem faz**: Augment Code GPT-5 ("Create tasklist with single first task. After it completes, add next minimal set based on what you learned. Prefer incremental replanning over upfront bulk task creation.")

**Por que vale a pena**: Claude Code tende a criar listas de 10+ tarefas no inicio, muitas das quais ficam irrelevantes conforme a implementacao avanca. Planejamento incremental e mais adaptativo.

**Como aplicar no CLAUDE.md**:
```
### Planejamento Incremental
- Criar no maximo 3-5 tarefas iniciais
- Adicionar novas tarefas APOS completar as primeiras (com base no que aprendeu)
- Evitar listas de 10+ tarefas upfront (ficam obsoletas rapido)
- Replanejar e mais valioso que seguir um plano rigido
```

**Nivel de impacto**: MEDIO

---

### 9. ~~REMOVIDO PELO USUARIO~~ (Dependencias -- usuario prefere liberdade para instalar)

---

### 10. AUTOCONSCIENCIA DE FRAQUEZAS (Augment Code)

**O que e**: O prompt admite explicitamente que o agente "frequentemente erra implementacoes iniciais" e sugere iterar em testes ate acertar.

**Quem faz**: Augment Code ("You often mess up initial implementations, but you work diligently on iterating until tests pass")

**Por que vale a pena**: Em vez de fingir perfeicao, reconhecer que a primeira tentativa pode falhar e ter uma estrategia para isso.

**Como aplicar no CLAUDE.md**:
```
### Humildade Tecnica
- A primeira implementacao pode ter bugs -- isso e normal
- Estrategia: implementar -> testar -> iterar ate passar
- Se perceber que esta andando em circulos: PARAR e pedir ajuda ao usuario
- Nunca insistir na mesma abordagem que ja falhou 2x
```

**Nivel de impacto**: MEDIO

---

### 11. NAO FAZER CONTA DE CABECA (Manus)

**O que e**: Usar ferramentas para calculos em vez de confiar no raciocinio matematico do modelo.

**Quem faz**: Manus ("Use bc for simple calculations, Python for complex math; never calculate mentally")

**Por que vale a pena**: LLMs erram aritmetica com frequencia. Se ha calculo envolvido (porcentagens, datas, conversoes), usar Bash com bc ou Python.

**Como aplicar no CLAUDE.md**:
```
### Calculos
- Para qualquer calculo numerico: usar Bash (bc, python) em vez de calcular mentalmente
- LLMs erram aritmetica -- sempre verificar com ferramenta
```

**Nivel de impacto**: BAIXO (situacional)

---

### 12. REFERENCIA A ARQUIVOS COMO LINKS CLICAVEIS (Amp)

**O que e**: Toda vez que mencionar um arquivo, incluir o caminho completo com numero de linha para facilitar navegacao.

**Quem faz**: Amp ("Whenever you mention a file by name, you MUST link to it")

**Por que vale a pena**: Claude Code ja faz `file_path:line_number`, mas poderia ser mais consistente. Amp torna isso obrigatorio em TODA mencao.

**Como aplicar no CLAUDE.md**:
```
### Referencias de Codigo
- SEMPRE incluir caminho:linha ao referenciar codigo (ja presente, reforcar)
- Formato: src/components/Button.tsx:42
```

**Nivel de impacto**: BAIXO (ja parcialmente implementado)

---

## PARTE 3 -- Padroes Que NAO Valem a Pena Replicar

| Padrao | Quem faz | Por que NAO replicar |
|---|---|---|
| Um tool call por turno | Manus, Augment GPT-5 | Claude Code se beneficia do paralelismo. Restringir a 1 call/turno tornaria tudo mais lento. |
| Proibir respostas em texto puro | Manus | Irrelevante para CLI interativo. O usuario precisa de texto. |
| External planner module | Manus | Requer infraestrutura de orquestracao que Claude Code nao tem. Plan Mode cumpre o papel. |
| Pop Quiz mechanism | Devin AI | Mecanismo de teste interno da Cognition, nao aplicavel a sessoes do usuario. |
| Design guidelines detalhados | v0 | Especifico para UI generation. Claude Code e generalista. |
| Forced self-reminders nos parametros da tool | Augment Code | Hack para modelos que esquecem instrucoes. Opus 4.5 nao precisa disso. |
| AGENTS.md como arquivo separado | Amp | Claude Code ja tem CLAUDE.md que cumpre o mesmo papel. |
| NES (tab completion) | Copilot | Feature de IDE, nao de CLI. |
| Write-lock awareness | Amp | Relevante so para sub-agentes paralelos editando mesmos arquivos, cenario raro no Claude Code. |
| Anti-list writing (proibir bullets) | Manus | Para CLI, listas sao mais legíveis que prosa corrida. |
| GenerateDesignInspiration | v0 | Feature especifica de UI design tool. |
| TodoManager com tarefas vagas proibidas | v0 | Boa ideia em teoria, mas Claude Code ja tem anti-over-engineering que cobre isso. |

---

## PARTE 4 -- Comparativo Resumido

| Dimensao | Claude Code | Melhor Pratica Observada | Gap? |
|---|---|---|---|
| Exploracao antes de acao | Sim (recomendado) | Devin: forcado por modo separado | Pequeno |
| Limite de retries | Nao (INTEIA sugere 2) | Devin/Copilot/Amp: 3 max, hard rule | **SIM** |
| Nunca modificar testes | Nao explicito | Devin: regra hard-coded | **SIM** |
| Verificacao pos-edicao | So no final | Copilot/Amp: apos cada edicao | **SIM** |
| >3 arquivos = plano | Nao | Amp: regra explicita | **SIM** |
| ~~Nunca instalar deps sem pedir~~ | ~~Removido~~ | ~~Augment/Amp~~ | ~~Removido pelo usuario~~ |
| Hierarquia de fontes | Nao formal | Manus: 3 niveis | Medio |
| Report env issues | Nao | Devin: padrao claro | **SIM** |
| Planejamento incremental | Parcial | Augment GPT-5: enforced | Medio |
| Git safety | Forte | Devin: comparavel | Nao |
| Paralelismo | Forte | Copilot/Amp: comparavel | Nao |
| Anti-over-engineering | Forte | Amp: comparavel | Nao |

---

## PARTE 5 -- Bloco Pronto Para CLAUDE.md

> Os 6 padroes aprovados, JA INTEGRADOS no CLAUDE.md global do usuario.

```
STATUS: IMPLEMENTADO em ~/.claude/CLAUDE.md

1. Regra dos 3 Retries        -> Secao "Gestao de Contexto"
2. Nunca modificar testes      -> Secao "Verificacao Obrigatoria"
3. Verificacao pos-edicao      -> Secao "Verificacao Obrigatoria"
4. >3 arquivos = plano         -> Secao "Workflow Padrao"
5. Report env issues           -> Secao "Gestao de Contexto"
6. Primeira tarefa = investigar -> Secao "Workflow Padrao"

Item removido pelo usuario: "Nunca instalar deps sem pedir"
```

---

## PARTE 6 -- Insights Meta (Observacoes Sobre a Industria)

### Tendencias observadas em todos os sistemas:
1. **Modelos mais capazes recebem mais autonomia + mais guardrails**. GPT-5 e Opus 4.5 tem prompts mais longos e mais restritivos que GPT-4o/Sonnet 4.
2. **"Explore before act" e universal**. Todo sistema serio implementa isso de alguma forma.
3. **Anti-over-engineering e consenso**. Todos dizem "faca so o pedido". A diferenca esta em quao enforced isso e.
4. **Verificacao pos-edicao esta se tornando padrao**. Copilot, Amp, e Augment ja fazem. Claude Code ainda nao.
5. **Subagentes estao se especializando**. Amp tem 3 niveis (Oracle/Search/Task). Claude Code tem 5+ tipos.
6. **Ferramentas MCP/LSP sao diferencial**. Copilot usa LSP nativo (go_to_definition, references). Claude Code usa MCP.
7. **Prompts sao ajustados por modelo**. O mesmo produto (Copilot, Augment, Amp) tem prompts diferentes para GPT-5 vs Claude vs Gemini.
8. **Memoria cross-session esta emergindo**. Augment tem `remember` tool, Copilot tem `update_user_preferences`. Claude Code depende de CLAUDE.md.

### O que so Claude Code tem:
- **Skills system** (INTEIA, mastery, longterm) -- nenhum concorrente tem isso
- **Hooks** (shell commands em resposta a tool calls) -- unico
- **ToolSearch** para ferramentas deferred -- unico
- **Modelo Opus 4.5** -- o modelo mais capaz disponivel em qualquer coding assistant

---

*Documento gerado por auto-analise do Claude Code Opus 4.5, janeiro 2026.*
*Fontes: github.com/x1xhlol/system-prompts-and-models-of-ai-tools + arquivos locais do usuario.*
