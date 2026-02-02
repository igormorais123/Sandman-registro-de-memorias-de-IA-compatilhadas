# Guia Completo de Consulta de Memória

> Manual detalhado para o Claude Code sobre COMO e QUANDO consultar o sistema de memória
> Este documento é a referência autoritativa para o processo de decisão

---

## Princípio Fundamental

```
ANTES DE RESPONDER QUALQUER PERGUNTA OU EXECUTAR QUALQUER TAREFA:
→ Pergunte-se: "Já sei algo sobre isso?"
→ Consulte a memória relevante
→ Aplique o conhecimento encontrado
→ Só então prossiga com a tarefa
```

---

## Algoritmo de Consulta

### Pseudocódigo do Processo de Decisão

```python
def processar_solicitacao(usuario_input):
    # 1. CLASSIFICAR A SOLICITAÇÃO
    tipo = classificar_tipo(usuario_input)  # debug, feature, arquitetura, config, etc.
    projeto = detectar_projeto_atual()      # Verifica se existe .memoria/

    # 2. DETERMINAR ESCOPO DE BUSCA
    if projeto and projeto.tem_memoria():
        escopo = "LOCAL_PRIMEIRO"
    else:
        escopo = "APENAS_GLOBAL"

    # 3. EXECUTAR CONSULTA
    conhecimento = []

    if escopo == "LOCAL_PRIMEIRO":
        # Consulta local ordenada por relevância
        conhecimento += buscar_local(projeto, tipo)

    # Sempre complementar com global
    conhecimento += buscar_global(tipo)

    # 4. APLICAR CONHECIMENTO
    if conhecimento:
        contexto_enriquecido = aplicar_conhecimento(usuario_input, conhecimento)
        return executar_tarefa(contexto_enriquecido)
    else:
        return executar_tarefa(usuario_input)  # Sem contexto adicional

    # 5. AVALIAR REGISTRO
    if resultado.contem_aprendizado():
        sugerir_registro(resultado)
```

---

## Mapeamento: Tipo de Tarefa → Arquivos a Consultar

### 1. DEBUG / CORREÇÃO DE BUGS

```
PRIORIDADE ALTA:
├── LOCAL: .memoria/CONTEXTO_ATIVO.md
│   └── Buscar: estado atual, problemas conhecidos, trabalho recente
├── LOCAL: .memoria/APRENDIZADOS.md
│   └── Buscar: erros similares, soluções anteriores
└── GLOBAL: ANTIPADROES_GLOBAIS.md
    └── Buscar: erros comuns relacionados à tecnologia/domínio

PRIORIDADE MÉDIA:
├── GLOBAL: CONHECIMENTO_UNIVERSAL.md
│   └── Buscar: técnicas de debugging, heurísticas
└── LOCAL: .memoria/sessoes/ (se erro persistente)
    └── Buscar: histórico de tentativas anteriores
```

### 2. NOVA FEATURE / IMPLEMENTAÇÃO

```
PRIORIDADE ALTA:
├── LOCAL: .memoria/MEMORIA_LONGO_PRAZO.md
│   └── Buscar: decisões arquiteturais, padrões do projeto
├── GLOBAL: PADROES_CODIGO.md
│   └── Buscar: soluções similares, templates
└── LOCAL: .memoria/CONTEXTO_ATIVO.md
    └── Buscar: estado atual, dependências, restrições

PRIORIDADE MÉDIA:
├── GLOBAL: CONHECIMENTO_UNIVERSAL.md
│   └── Buscar: boas práticas, princípios aplicáveis
└── GLOBAL: CATALOGO_PROJETOS.md
    └── Buscar: projetos com features similares
```

### 3. REFATORAÇÃO

```
PRIORIDADE ALTA:
├── LOCAL: .memoria/MEMORIA_LONGO_PRAZO.md
│   └── Buscar: razões das decisões originais, restrições
├── LOCAL: .memoria/APRENDIZADOS.md
│   └── Buscar: problemas anteriores com o código
├── GLOBAL: PADROES_CODIGO.md
│   └── Buscar: padrões alvo, melhores práticas
└── GLOBAL: ANTIPADROES_GLOBAIS.md
    └── Buscar: o que evitar na refatoração
```

### 4. DECISÃO ARQUITETURAL

```
PRIORIDADE ALTA:
├── LOCAL: .memoria/MEMORIA_LONGO_PRAZO.md
│   └── Buscar: decisões anteriores, contexto do projeto
├── GLOBAL: CONHECIMENTO_UNIVERSAL.md
│   └── Buscar: princípios de arquitetura, trade-offs
└── GLOBAL: CATALOGO_PROJETOS.md
    └── Buscar: como outros projetos resolveram

PRIORIDADE MÉDIA:
└── GLOBAL: ANTIPADROES_GLOBAIS.md
    └── Buscar: decisões que deram errado
```

### 5. CONFIGURAÇÃO / SETUP

```
PRIORIDADE ALTA:
├── LOCAL: .memoria/CONTEXTO_ATIVO.md
│   └── Buscar: ambiente atual, dependências
├── GLOBAL: FERRAMENTAS_RECOMENDADAS.md
│   └── Buscar: configs recomendadas, pegadinhas
└── GLOBAL: PADROES_CODIGO.md
    └── Buscar: configs padrão (tsconfig, eslint, etc.)
```

### 6. AJUDA COM PROMPTS / COMO PERGUNTAR

```
PRIORIDADE ALTA:
└── GLOBAL: PROMPTS_EFETIVOS.md
    └── Buscar: prompts por categoria, taxa de sucesso

PRIORIDADE MÉDIA:
└── GLOBAL: META_APRENDIZADO.md
    └── Buscar: o que funciona melhor
```

---

## Estratégias de Busca

### Busca por Palavras-Chave

```
TÉCNICA: Extrair termos relevantes e buscar em arquivos

Exemplo - Usuário: "O login não está funcionando após atualização do JWT"

Termos a buscar:
- "login"
- "JWT" / "token"
- "autenticação" / "auth"
- "atualização" / "migration"

Arquivos a verificar:
1. CONTEXTO_ATIVO.md → "JWT", "token", "auth"
2. APRENDIZADOS.md → "login", "autenticação"
3. ANTIPADROES_GLOBAIS.md → "JWT", "token"
4. CONHECIMENTO_UNIVERSAL.md → "autenticação"
```

### Busca por Contexto Temporal

```
TÉCNICA: Quando o problema é recente, priorizar sessões recentes

Exemplo - Usuário: "Aquele bug que vimos ontem voltou"

Ordem de busca:
1. .memoria/sessoes/[data-recente].md
2. CONTEXTO_ATIVO.md → seção "Problemas Atuais"
3. APRENDIZADOS.md → entradas recentes
```

### Busca por Similaridade

```
TÉCNICA: Encontrar problemas/soluções similares mesmo com termos diferentes

Exemplo - Usuário: "A página está lenta"

Termos relacionados a buscar:
- "performance"
- "lento" / "slow"
- "otimização"
- "render" / "renderização"
- "carregamento" / "loading"
- Tecnologia específica (React, Node, etc.)
```

---

## Formato de Aplicação do Conhecimento

### Quando encontrar informação relevante:

```markdown
## Contexto da Memória

Encontrei informações relevantes no sistema de memória:

### De [ARQUIVO]:
> [Citação ou resumo do conhecimento encontrado]

### Aplicação:
[Como este conhecimento se aplica à situação atual]

---

Prosseguindo com a tarefa considerando este contexto...
```

### Exemplo Prático:

```markdown
## Contexto da Memória

Encontrei informações relevantes no sistema de memória:

### De ANTIPADROES_GLOBAIS.md:
> "JWT refresh tokens: Nunca armazenar em localStorage.
> Usar httpOnly cookies. Erro comum que causa vulnerabilidades XSS."

### De APRENDIZADOS.md (projeto atual):
> "2026-01-15: Migramos de localStorage para cookies httpOnly
> após auditoria de segurança. Ver PR #142."

### Aplicação:
O bug atual pode estar relacionado à migração de tokens.
Verificar se o código antigo não foi reintroduzido.

---

Vou investigar os handlers de autenticação...
```

---

## Gatilhos para Registro de Novo Conhecimento

### Durante a execução, identificar:

| Gatilho | Ação | Destino |
|---------|------|---------|
| "Isso não está documentado em lugar nenhum" | Registrar descoberta | CONHECIMENTO_UNIVERSAL |
| "Esse erro me pegou de surpresa" | Documentar armadilha | ANTIPADROES_GLOBAIS |
| "Essa solução é elegante e reutilizável" | Extrair padrão | PADROES_CODIGO |
| "Decidimos X porque Y" | Documentar decisão | MEMORIA_LONGO_PRAZO (local) |
| "Aprendi que..." | Capturar aprendizado | APRENDIZADOS (local) |
| "Esse prompt funcionou muito bem" | Salvar prompt | PROMPTS_EFETIVOS |

### Formato para Novos Registros

```markdown
### [DATA] - [Título Descritivo]

**Contexto**:
[Situação que levou à descoberta]

**Problema/Desafio**:
[O que estava tentando resolver]

**Solução/Insight**:
[O que funcionou ou foi aprendido]

**Aplicação futura**:
[Quando este conhecimento deve ser consultado]

**Tags**: #tipo #tecnologia #confianca-alta

**Origem**: [Projeto] - [Sessão/Data]
```

---

## Ciclo Completo de uma Sessão

### 1. INÍCIO DA SESSÃO

```
□ Detectar projeto atual
□ Verificar existência de .memoria/
□ Ler CONTEXTO_ATIVO.md (se existir)
□ Entender estado atual do trabalho
```

### 2. DURANTE A SESSÃO

```
Para cada solicitação:
□ Classificar tipo de tarefa
□ Consultar memória relevante (ver mapeamentos acima)
□ Aplicar conhecimento encontrado
□ Executar tarefa
□ Identificar gatilhos de registro
□ Marcar conhecimento para registro posterior
```

### 3. FIM DA SESSÃO

```
□ Registrar aprendizados identificados
□ Atualizar CONTEXTO_ATIVO.md
□ Marcar candidatos para sincronização global
□ Sugerir ciclo de sono se apropriado
```

---

## Comandos de Memória - Implementação

### "carregar contexto"

```
AÇÃO:
1. Ler .memoria/CONTEXTO_ATIVO.md
2. Ler .memoria/MEMORIA_LONGO_PRAZO.md (resumo)
3. Apresentar estado atual ao usuário
4. Listar tarefas pendentes se houver
```

### "consultar memória sobre X"

```
AÇÃO:
1. Extrair termos de busca de X
2. Buscar em arquivos locais (se existir .memoria/)
3. Buscar em arquivos globais
4. Consolidar e apresentar resultados
5. Indicar fonte de cada informação
```

### "registrar sessão"

```
AÇÃO:
1. Coletar aprendizados marcados durante sessão
2. Criar/atualizar .memoria/sessoes/[DATA].md
3. Atualizar APRENDIZADOS.md se houver insights
4. Atualizar CONTEXTO_ATIVO.md com estado final
```

### "ciclo de sono"

```
AÇÃO:
1. Executar protocolo em .memoria/PROTOCOLO_SONO.md
2. Consolidar sessões recentes
3. Promover conhecimento validado
4. Limpar informação obsoleta
5. Identificar candidatos para global
6. Atualizar métricas
```

### "sincronizar com global"

```
AÇÃO:
1. Ler .memoria/SYNC_GLOBAL.md para regras
2. Identificar itens com #candidato-global
3. Verificar critérios de exportação
4. Adicionar a arquivos globais apropriados
5. Importar conhecimento global relevante
6. Registrar sincronização
```

---

## Métricas de Qualidade

### A memória está funcionando bem quando:

- [ ] Conhecimento é consultado antes de tarefas
- [ ] Erros documentados não se repetem
- [ ] Soluções são reutilizadas entre projetos
- [ ] Decisões têm contexto documentado
- [ ] Ciclos de sono são executados regularmente

### Sinais de problema:

- [ ] Mesmo erro acontece múltiplas vezes
- [ ] Conhecimento não é encontrado quando deveria
- [ ] Memória muito grande sem consolidação
- [ ] Projetos não sincronizam com global
- [ ] Informação desatualizada causa confusão

---

## Troubleshooting

### "Não encontrei nada relevante"

```
VERIFICAR:
1. Termos de busca muito específicos? → Generalizar
2. Arquivo correto? → Rever mapeamento de tipos
3. Conhecimento existe mas com outros termos? → Sinônimos
4. É conhecimento novo? → Registrar após resolver
```

### "Informação conflitante"

```
RESOLVER:
1. Verificar datas → Mais recente geralmente vale
2. Verificar tags → #validado > #experimental
3. Verificar origem → Local > Global para especificidades
4. Se persistir → Registrar conflito, perguntar usuário
```

### "Memória muito grande"

```
AÇÃO:
1. Executar ciclo de sono
2. Arquivar conhecimento antigo não usado
3. Consolidar entradas redundantes
4. Remover informação obsoleta
```

---

*Guia de Consulta v1.0 - Sistema de Memória Hierárquica*
