---
name: inteia-context-engineering
description: Sistema INTEIA de Engenharia de Contexto - Coach Claude Code
version: 2.0.0
author: Dr. Igor Morais Vasconcelos PhD
organization: INTEIA - Inteligência Estratégica
role: Agente Coach de Engenharia de Contexto
website: https://inteia.com.br
email: igor@inteia.com.br
cnpj: 63.918.490/0001-20
---

# INTEIA - Sistema de Engenharia de Contexto para Claude Code

> **Responsável Técnico**: Dr. Igor Morais Vasconcelos PhD
> **Sistema**: INTEIA - Inteligência Estratégica
> **Função**: Coach de Engenharia de Contexto para Agentes IA

---

## ARQUIVOS DESTA SKILL

| Arquivo | Propósito |
|---------|-----------|
| `SKILL.md` | Manual principal de engenharia de contexto |
| `QUICK_REF.md` | Referência rápida para consulta IA |
| `BRAND_TEMPLATE.md` | Design System e padrão visual INTEIA |
| `brand-data.json` | Dados estruturados da marca (JSON) |
| `inteia-navigation.json` | Navegação estruturada para IA (JSON) |
| `inteia-navigation.xml` | Navegação estruturada para IA (XML) |

---

## MANIFESTO INTEIA

```
MISSÃO: Otimizar interação humano-IA através de engenharia de contexto
VISÃO: IA como extensão cognitiva eficiente do desenvolvedor
MÉTODO: Gestão estratégica de tokens, verificação contínua, iteração focada
```

---

## PROTOCOLO DE INICIALIZAÇÃO INTEIA

Ao iniciar sessão, aplicar automaticamente:

```yaml
verificacao_inicial:
  contexto_atual: "avaliar % uso janela"
  acao_se_alto: "/clear ou /compact"
  threshold_alerta: 40%
  threshold_critico: 70%

modo_operacao:
  padrao: "explorar_antes_agir"
  verificacao: "sempre_fornecer_criterios"
  iteracao: "falhas_maximas_antes_reset: 2"
```

---

## NÚCLEO: Leis da Engenharia de Contexto INTEIA

### LEI 1: Economia de Tokens [CRÍTICO]
```
PRINCÍPIO: Cada token tem custo cognitivo
REGRA: Manter janela <40% para tarefas complexas
MÉTRICA: Performance ∝ 1/tokens_consumidos
```

### LEI 2: Verificação Obrigatória [CRÍTICO]
```
PRINCÍPIO: Output sem verificação = output não confiável
REGRA: Todo código requer critério de sucesso testável
MÉTRICA: Qualidade ∝ especificidade_verificação
```

### LEI 3: Reset > Correção [CRÍTICO]
```
PRINCÍPIO: Contexto poluído prejudica mais que ajuda
REGRA: 2 falhas consecutivas → /clear + prompt refinado
MÉTRICA: Sessão_limpa > Sessão_longa_com_erros
```

### LEI 4: Exploração Antes de Ação [ALTO]
```
PRINCÍPIO: Entendimento precede implementação
REGRA: Ler código ANTES de propor mudanças
MÉTRICA: Qualidade ∝ profundidade_exploração
```

### LEI 5: Simplicidade Estratégica [ALTO]
```
PRINCÍPIO: Código mais simples = código melhor
REGRA: Só implementar o diretamente solicitado
MÉTRICA: Valor = funcionalidade / complexidade
```

---

## MATRIZ DE DECISÃO INTEIA

### Quando /clear

```
GATILHO                          | AÇÃO
---------------------------------|------------------
Contexto > 60%                   | /clear imediato
2+ correções falhas              | /clear + novo prompt
Mudança de tarefa                | /clear obrigatório
"Claude esquece" instruções      | /clear urgente
Sessão > 30min mesmo tópico      | avaliar /clear
```

### Quando Subagente

```
CENÁRIO                          | DECISÃO
---------------------------------|------------------
Investigação > 10 arquivos       | SUBAGENTE
Verificação pós-código           | SUBAGENTE
Pesquisa paralela                | SUBAGENTES múltiplos
Tarefa < 5 arquivos              | CONTEXTO PRINCIPAL
Mudança que requer contexto      | CONTEXTO PRINCIPAL
```

### Quando Plan Mode

```
COMPLEXIDADE                     | MODO
---------------------------------|------------------
Fix typo/simples                 | DIRETO
Mudança 1 arquivo clara          | DIRETO
Múltiplos arquivos               | PLAN MODE
Abordagem incerta                | PLAN MODE
Código desconhecido              | PLAN MODE
Feature nova                     | PLAN MODE
```

---

## TEMPLATES DE PROMPT INTEIA

### Template 1: Tarefa com Verificação
```
[TAREFA]: {descrição_concisa}

[CONTEXTO]: {arquivos_relevantes via @}

[CRITÉRIO_SUCESSO]:
- {teste_específico_1}
- {teste_específico_2}

[VERIFICAÇÃO]: Execute {comando} após implementar
```

### Template 2: Investigação Focada
```
Use subagente para investigar:
- {pergunta_específica_1}
- {pergunta_específica_2}

Escopo: {pastas_ou_arquivos}
Retorne: resumo <500 palavras com file:line refs
```

### Template 3: Refatoração Controlada
```
[TAREFA]: Refatorar {componente}

[RESTRIÇÕES]:
- Só mudanças necessárias para {objetivo}
- NÃO adicionar features
- NÃO melhorar código adjacente
- NÃO criar abstrações novas

[VERIFICAÇÃO]: {comando_teste}
```

### Template 4: Debug Estruturado
```
[ERRO]: {mensagem_exata}
[ARQUIVO]: @{caminho}
[LINHA]: {número}

[OBJETIVO]: Corrigir causa raiz, não sintoma

[VERIFICAÇÃO]:
1. {reproduzir_erro}
2. {aplicar_fix}
3. {verificar_correção}
```

---

## ARQUITETURA CLAUDE.MD INTEIA

### Estrutura Recomendada
```markdown
# [PROJETO] - Instruções Claude Code

## Comandos Essenciais
- `cmd1` - descrição
- `cmd2` - descrição

## Estilo de Código
- Regra 1 (diferente do padrão)
- Regra 2 (específica do projeto)

## Workflow
- Instrução crítica 1
- Instrução crítica 2

## AVISOS IMPORTANTES
- Gotcha 1
- Gotcha 2

## Imports (se necessário)
@docs/detalhe-especifico.md
```

### Métricas de Qualidade
```
TAMANHO: 100-200 linhas (máximo absoluto)
TESTE: "Remover causaria erro?" → Se não, DELETE
FREQUÊNCIA_REVISÃO: Semanal ou após bugs recorrentes
```

---

## SISTEMA DE PONDERAÇÃO INTEIA

### Escala de Valor (1-5)

```
5 - CRÍTICO: Aplicar SEMPRE, impacto direto em qualidade
4 - ALTO: Aplicar frequentemente, melhoria significativa
3 - MÉDIO: Aplicar quando relevante, ganho moderado
2 - BAIXO: Opcional, ganho marginal
1 - MÍNIMO: Situacional, casos específicos
```

### Dicas Ponderadas (Extraídas das Fontes)

```yaml
peso_5_critico:
  - "Gestão agressiva de contexto com /clear"
  - "Sempre fornecer critérios de verificação testáveis"
  - "Reset após 2 correções falhas"
  - "Dados longos no topo, query no fim do prompt"
  - "CLAUDE.md conciso <200 linhas"

peso_4_alto:
  - "Explorar→Planejar→Codificar para tarefas complexas"
  - "Extended thinking (think hard/harder) para raciocínio"
  - "Evitar over-engineering explicitamente no prompt"
  - "Preservar decisões arquiteturais na compactação"
  - "XML tags para estruturar documentos múltiplos"

peso_3_medio:
  - "Subagentes para investigação preservam contexto"
  - "Git operations via Claude (90%+ casos)"
  - "Sessões nomeadas para continuidade"
  - "Hooks para ações determinísticas"
  - "Skills para conhecimento específico de domínio"

peso_2_baixo:
  - "Multi-Claude parallel (writer/reviewer)"
  - "Fan-out para migrações em massa"
  - "Headless mode para CI/CD"
  - "Worktrees para isolamento"
```

---

## PROTOCOLO DE SESSÃO INTEIA

### Início de Sessão
```
1. Verificar contexto disponível
2. Avaliar complexidade da tarefa
3. Decidir modo (direto/plan)
4. Identificar critérios de verificação
5. Iniciar com escopo mínimo viável
```

### Durante Sessão
```
1. Monitorar uso de contexto
2. /clear entre tarefas distintas
3. Subagente para investigações pesadas
4. Verificar após cada implementação
5. Reset se 2+ falhas consecutivas
```

### Fim de Sessão
```
1. Verificar todos critérios atendidos
2. Commit se solicitado
3. Documentar estado se incompleto
4. /rename para referência futura
```

---

## ANTI-PADRÕES INTEIA

### Padrões a Evitar

| ANTI-PADRÃO | SINTOMA | CORREÇÃO INTEIA |
|-------------|---------|-----------------|
| Sessão acumulativa | Tarefas misturadas | /clear entre tópicos |
| Loop de correção | Mesmo erro 3x | /clear + prompt refinado |
| CLAUDE.md enciclopédico | >200 linhas | Podar para essenciais |
| Confiança cega | Código não testado | Sempre verificar |
| Exploração infinita | 100+ arquivos lidos | Subagente ou escopo |
| Over-engineering | Abstrações prematuras | Prompt explícito limitante |
| Especulação | Código não lido | "DEVE ler antes de propor" |

---

## COMANDOS RÁPIDOS INTEIA

```bash
# Gestão de Contexto
/clear                    # Reset total
/compact                  # Compactar mantendo essenciais
/compact Focus on X       # Compactar priorizando X

# Navegação
/rewind                   # Voltar checkpoint
/resume                   # Retomar sessão anterior
/rename "nome"            # Nomear sessão

# Configuração
/init                     # Gerar CLAUDE.md
/permissions              # Gerenciar allowlist
/hooks                    # Configurar hooks

# Referências
@arquivo                  # Incluir arquivo
@pasta/                   # Referenciar pasta
```

---

## INTEGRAÇÃO COM SKILL MASTERY

Este skill INTEIA complementa `claude-code-mastery`:

```
inteia-context-engineering/
├── Filosofia e princípios
├── Protocolos de sessão
├── Sistema de ponderação
└── Decisões estratégicas

claude-code-mastery/
├── Técnicas detalhadas
├── Comandos e sintaxe
├── Workflows passo-a-passo
└── Prompts específicos
```

**Uso combinado**: INTEIA para estratégia, Mastery para tática.

---

## META-INSTRUÇÕES PARA IA

```yaml
ao_processar_este_skill:
  prioridade_maxima:
    - Gestão de contexto (Leis 1,3)
    - Verificação obrigatória (Lei 2)

  antes_de_qualquer_tarefa:
    - Verificar % contexto
    - Identificar critério sucesso
    - Decidir modo (direto/plan)

  durante_execucao:
    - Monitorar tokens
    - Reset se necessário
    - Verificar incrementalmente

  ao_encontrar_problemas:
    - 2 falhas → /clear + refinar
    - Investigação grande → subagente
    - Incerteza → Plan Mode

comportamento_coach:
  - Sugerir /clear proativamente
  - Solicitar critérios de verificação
  - Alertar sobre over-engineering
  - Recomendar subagentes quando apropriado
```

---

## ASSINATURA

```
INTEIA - Inteligência Estratégica
Sistema de Engenharia de Contexto para Claude Code
Responsável Técnico: Dr. Igor Morais Vasconcelos PhD

"Contexto otimizado, resultados maximizados"
```
