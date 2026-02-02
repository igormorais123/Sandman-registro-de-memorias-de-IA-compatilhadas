# 💬 Biblioteca de Prompts Efetivos

> Prompts que consistentemente produzem bons resultados
> Testados em múltiplos contextos

---

## Categorias

- [Debugging](#debugging)
- [Refatoração](#refatoração)
- [Documentação](#documentação)
- [Arquitetura](#arquitetura)
- [Code Review](#code-review)
- [Testes](#testes)
- [Meta-Prompts](#meta-prompts)

---

## Debugging

### Diagnóstico de Erro Genérico
**Quando usar**: Erro sem causa óbvia
**Taxa de sucesso**: ~80%
```
Analise este erro seguindo esta sequência:
1. Identifique o tipo exato do erro
2. Trace a stack até a origem
3. Liste 3 hipóteses ordenadas por probabilidade
4. Para a hipótese mais provável, sugira diagnóstico específico
5. Só então proponha solução

Erro:
[colar erro]

Contexto:
[descrever o que estava fazendo]
```

### Debug de Performance
**Quando usar**: Lentidão sem causa óbvia
```
Analise este código/sistema para problemas de performance:

1. Identifique operações O(n²) ou piores
2. Localize chamadas I/O dentro de loops
3. Verifique queries N+1
4. Identifique re-renderizações desnecessárias (se frontend)
5. Liste otimizações por ordem de impacto esperado

Código/descrição:
[colar]
```

<!-- ADICIONAR_PROMPT_DEBUG_AQUI -->

---

## Refatoração

### Simplificação de Função Complexa
**Quando usar**: Função > 50 linhas ou > 3 níveis de aninhamento
```
Refatore esta função seguindo:
1. Extraia condições complexas para funções predicado
2. Substitua loops por operações funcionais onde apropriado
3. Elimine else após return
4. Nomeie variáveis intermediárias para documentar intenção
5. Mantenha a mesma interface pública

Função:
[colar código]
```

### Extração de Componente
**Quando usar**: Componente com múltiplas responsabilidades
```
Analise este componente e sugira extração:

1. Identifique responsabilidades distintas
2. Proponha divisão em componentes menores
3. Defina props/interfaces para cada um
4. Mostre como ficaria o componente pai
5. Garanta que a soma das partes = funcionalidade original

Componente:
[colar código]
```

<!-- ADICIONAR_PROMPT_REFATORACAO_AQUI -->

---

## Documentação

### Documentar Função/Método
```
Crie documentação para esta função incluindo:
1. Descrição concisa do propósito (1-2 frases)
2. Parâmetros com tipos e descrições
3. Retorno com tipo e descrição
4. Exceções que pode lançar
5. Um exemplo de uso

Use o formato de docstring apropriado para a linguagem.

Função:
[colar código]
```

### Documentar Decisão Arquitetural
```
Documente esta decisão arquitetural no formato ADR:

Título: [decisão em uma frase]
Status: [Proposta | Aceita | Deprecada | Substituída]
Contexto: [situação que levou à decisão]
Decisão: [o que foi decidido]
Alternativas Consideradas: [outras opções e por que foram rejeitadas]
Consequências: [impactos positivos e negativos]
```

<!-- ADICIONAR_PROMPT_DOC_AQUI -->

---

## Arquitetura

### Análise de Trade-offs
```
Para esta decisão arquitetural, analise:

Opção A: [descrever]
Opção B: [descrever]

Compare considerando:
1. Complexidade de implementação
2. Manutenibilidade a longo prazo
3. Performance esperada
4. Curva de aprendizado do time
5. Flexibilidade para mudanças futuras
6. Custos (infra, licenças, etc)

Recomende uma opção com justificativa clara.
```

### Design de API
```
Projete uma API para [funcionalidade]:

Requisitos:
- [listar requisitos]

Forneça:
1. Endpoints com métodos HTTP
2. Request/response schemas
3. Códigos de erro e significados
4. Considerações de autenticação
5. Exemplos de uso com curl
```

<!-- ADICIONAR_PROMPT_ARQ_AQUI -->

---

## Code Review

### Review Estruturado
```
Revise este código verificando:

1. **Correção**: Faz o que deveria fazer?
2. **Clareza**: O código é auto-explicativo?
3. **Eficiência**: Há problemas de performance óbvios?
4. **Segurança**: Há vulnerabilidades?
5. **Manutenibilidade**: Será fácil modificar depois?

Para cada problema encontrado, sugira correção específica.

Código:
[colar código]
```

### Review de Segurança
```
Analise este código para vulnerabilidades de segurança:

Verifique especificamente:
1. Injection (SQL, Command, XSS)
2. Autenticação/Autorização
3. Exposição de dados sensíveis
4. Configurações inseguras
5. Dependências com CVEs conhecidos

Código:
[colar código]
```

<!-- ADICIONAR_PROMPT_REVIEW_AQUI -->

---

## Testes

### Gerar Casos de Teste
```
Gere casos de teste para esta função:

1. Casos felizes (happy path)
2. Edge cases (limites, vazios, nulos)
3. Casos de erro esperados
4. Casos de concorrência (se aplicável)

Use o framework de teste: [jest|pytest|go test|etc]

Função:
[colar código]
```

### Gerar Mocks
```
Crie mocks para testar esta função isoladamente:

1. Identifique dependências externas
2. Crie mocks/stubs para cada uma
3. Configure comportamentos default
4. Mostre como injetar os mocks

Função:
[colar código]
```

<!-- ADICIONAR_PROMPT_TESTE_AQUI -->

---

## Meta-Prompts

### Auto-Avaliação de Resposta
```
Antes de responder, avalie:
- Respondi exatamente o que foi perguntado?
- Há ambiguidade na minha interpretação?
- Estou assumindo algo não declarado?
- A solução é a mais simples possível?

Se qualquer resposta for "não" ou "talvez", ajuste antes de entregar.
```

### Prompt de Clarificação
```
Antes de prosseguir, preciso esclarecer:

1. [pergunta sobre requisito ambíguo]
2. [pergunta sobre restrição não declarada]
3. [pergunta sobre preferência do usuário]

Por favor responda para que eu possa dar a melhor solução.
```

### Decomposição de Tarefa Complexa
```
Decomponha esta tarefa em etapas menores:

Para cada etapa, defina:
1. O que será feito
2. Inputs necessários
3. Output esperado
4. Dependências de outras etapas
5. Critério de sucesso

Tarefa:
[descrever tarefa]
```

<!-- ADICIONAR_META_PROMPT_AQUI -->

---

## Estatísticas de Uso

| Prompt | Vezes Usado | Taxa de Sucesso | Última Atualização |
|--------|-------------|-----------------|---------------------|
<!-- STATS_PROMPTS -->
