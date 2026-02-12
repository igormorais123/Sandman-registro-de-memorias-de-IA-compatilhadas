# INTEIA Quick Reference - Consulta Rápida IA

> **Sistema**: INTEIA - Inteligência Estratégica
> **Autor**: Dr. Igor Morais Vasconcelos PhD
> **Função**: Coach de Engenharia de Contexto Claude Code

---

## DECISÕES INSTANTÂNEAS

```
CONTEXTO > 40%?      → /clear ou /compact
CONTEXTO > 70%?      → /clear URGENTE
2+ FALHAS?           → /clear + prompt refinado
INVESTIGAÇÃO >10 ARQ → subagente
TAREFA COMPLEXA?     → Plan Mode primeiro
INCERTEZA ABORDAGEM? → Plan Mode
MÚLTIPLOS ARQUIVOS?  → Plan Mode
FIX SIMPLES/TYPO?    → Direto (sem plan)
```

---

## 5 LEIS FUNDAMENTAIS

| # | LEI | PRINCÍPIO | AÇÃO IMEDIATA |
|---|-----|-----------|---------------|
| 1 | Economia Tokens | Token = custo cognitivo | Manter <40% |
| 2 | Verificação | Sem teste = não confiável | Sempre critério testável |
| 3 | Reset > Correção | Poluído prejudica | 2 falhas = /clear |
| 4 | Explorar Antes | Entender precede agir | Ler ANTES de propor |
| 5 | Simplicidade | Menos = melhor | Só o solicitado |

---

## COMANDOS ESSENCIAIS

### Gestão de Contexto
```
/clear                 Reset total (usar frequentemente!)
/compact               Compactar preservando essenciais
/compact Focus on X    Compactar priorizando tema X
```

### Navegação e Sessão
```
/rewind                Voltar checkpoint anterior
/resume                Retomar sessão anterior
/rename "nome"         Nomear sessão para referência
--continue             CLI: retomar última sessão
```

### Configuração
```
/init                  Gerar CLAUDE.md inicial
/permissions           Gerenciar allowlist
/hooks                 Configurar automações
```

### Referências
```
@arquivo               Incluir arquivo específico
@pasta/                Referenciar pasta
@docs/file.md          Importar em CLAUDE.md
```

---

## TEMPLATES DE PROMPT

### Template 1: Tarefa Padrão (USAR SEMPRE)
```
[TAREFA]: {descrição concisa do que fazer}

[CONTEXTO]: @{arquivo1} @{arquivo2}

[CRITÉRIO DE SUCESSO]:
- {teste específico 1}
- {teste específico 2}

[VERIFICAÇÃO]: Execute {comando} após implementar
```

### Template 2: Investigação com Subagente
```
Use subagente para investigar:
- {pergunta específica 1}
- {pergunta específica 2}

Escopo: {pastas ou arquivos}
Retorne: resumo <500 palavras com file:line refs
```

### Template 3: Refatoração Controlada
```
[TAREFA]: Refatorar {componente}

[RESTRIÇÕES]:
- APENAS mudanças necessárias para {objetivo}
- NÃO adicionar features
- NÃO melhorar código adjacente
- NÃO criar abstrações novas

[VERIFICAÇÃO]: {comando_teste}
```

### Template 4: Debug Estruturado
```
[ERRO]: {mensagem exata}
[ARQUIVO]: @{caminho}
[LINHA]: {número se conhecido}

[OBJETIVO]: Corrigir CAUSA RAIZ, não sintoma

[PASSOS]:
1. Reproduzir erro
2. Aplicar fix
3. Verificar correção
```

### Template 5: Anti-Over-Engineering (incluir quando necessário)
```
IMPORTANTE - Evite over-engineering:
- Só mudanças DIRETAMENTE solicitadas
- NÃO adicione features não pedidas
- NÃO refatore código adjacente
- NÃO crie helpers para operações únicas
- NÃO projete para requisitos hipotéticos
- Complexidade MÍNIMA para tarefa atual
```

---

## EXTENDED THINKING

| Comando | Budget | Quando Usar |
|---------|--------|-------------|
| "think" | Básico | Decisões simples |
| "think hard" | Médio | Lógica moderada |
| "think harder" | Alto | Arquitetura, bugs difíceis |
| "ultrathink" | Máximo | Problemas muito complexos |

---

## ÁRVORE DE DECISÃO

### Quando usar /clear?
```
SIM se:
├── Contexto > 60%
├── 2+ correções falhas no mesmo problema
├── Mudança de tarefa/tópico
├── Claude "esquece" instruções
└── Sessão > 30min mesmo tópico (avaliar)

NÃO se:
├── Continuidade necessária
└── Contexto ainda relevante <40%
```

### Quando usar Subagente?
```
SIM se:
├── Investigação > 10 arquivos
├── Verificação pós-implementação
├── Pesquisa paralela múltiplos tópicos
└── Preservar contexto principal importante

NÃO se:
├── Tarefa < 5 arquivos
├── Mudança requer contexto compartilhado
└── Overhead não justifica
```

### Quando usar Plan Mode?
```
SIM se:
├── Múltiplos arquivos afetados
├── Abordagem incerta
├── Código desconhecido
├── Feature nova
└── Refatoração significativa

NÃO se:
├── Fix typo/simples
├── Mudança 1 arquivo clara
└── Diff descritível em 1 frase
```

---

## ANTI-PADRÕES (EVITAR)

| Anti-Padrão | Sintoma | Correção |
|-------------|---------|----------|
| Sessão acumulativa | Tarefas misturadas | /clear entre tópicos |
| Loop de correção | Mesmo erro 3x+ | /clear + prompt novo |
| CLAUDE.md enciclopédico | >200 linhas | Podar para essenciais |
| Confiança cega | Código sem teste | Sempre verificar |
| Exploração infinita | 100+ arquivos lidos | Subagente ou escopo |
| Over-engineering | Abstrações não pedidas | Prompt limitante |
| Especulação | Propor sem ler | "DEVE ler antes" |

---

## ESTRUTURA PROMPT LONGO (Contexto Grande)

```xml
<!-- ORDEM CORRETA (melhora até 30%) -->

<!-- 1º TOPO: Dados/documentos longos -->
<documents>
  <document index="1">
    <source>arquivo.ext</source>
    <document_content>{{CONTEUDO}}</document_content>
  </document>
</documents>

<!-- 2º MEIO: Instruções e contexto -->
<instructions>
  ...
</instructions>

<!-- 3º FIM: Query/pergunta específica -->
<query>
  O que você precisa que eu faça?
</query>
```

---

## CLAUDE.MD - Regras de Ouro

```
TAMANHO: 100-200 linhas MÁXIMO
TESTE: "Remover causaria erro?" Se não → DELETE
INCLUIR: Comandos não-óbvios, regras diferentes do padrão
EXCLUIR: O que Claude infere do código, convenções padrão
REVISÃO: Semanal ou após bugs recorrentes
```

---

## PROTOCOLO DE SESSÃO

### Início
```
1. [ ] Verificar % contexto
2. [ ] Avaliar complexidade tarefa
3. [ ] Decidir modo (direto/plan)
4. [ ] Identificar critério de verificação
```

### Durante
```
1. [ ] Monitorar tokens
2. [ ] /clear entre tarefas distintas
3. [ ] Subagente para investigações pesadas
4. [ ] Verificar após cada implementação
5. [ ] Reset se 2+ falhas
```

### Fim
```
1. [ ] Verificar critérios atendidos
2. [ ] Commit se solicitado
3. [ ] Documentar estado se incompleto
4. [ ] /rename para referência futura
```

---

## PONDERAÇÃO DE VALOR (1-5)

### Peso 5 - CRÍTICO (aplicar SEMPRE)
- Gestão contexto com /clear
- Critérios verificação testáveis
- Reset após 2 falhas
- Dados topo, query fim
- CLAUDE.md <200 linhas

### Peso 4 - ALTO (aplicar frequentemente)
- Workflow Explorar→Planejar→Codificar
- Extended thinking para complexo
- Anti-over-engineering explícito
- XML tags para múltiplos docs

### Peso 3 - MÉDIO (quando relevante)
- Subagentes para investigação
- Git via Claude
- Sessões nomeadas
- Hooks para ações obrigatórias

### Peso 2 - BAIXO (opcional)
- Multi-Claude parallel
- Fan-out migrações
- Headless CI/CD

---

## CHECKLIST RÁPIDO PRÉ-TAREFA

```
[ ] Contexto < 40%? (se não: /clear)
[ ] Critério de verificação definido?
[ ] Tarefa complexa? (se sim: Plan Mode)
[ ] Já corrigi 2x sem sucesso? (se sim: /clear + novo prompt)
[ ] Investigação grande? (se sim: subagente)
```

---

## FRASES-CHAVE PARA INCLUIR EM PROMPTS

```
"Execute testes após implementar"
"Verifique antes de concluir"
"Só mudanças diretamente solicitadas"
"Leia o arquivo antes de propor mudanças"
"Não adicione features extras"
"Trate causa raiz, não sintoma"
"Retorne resumo <500 palavras"
```

---

## META-INSTRUÇÕES PARA IA

```yaml
ao_iniciar_tarefa:
  - verificar_contexto: "< 40%?"
  - definir_verificacao: "como testar sucesso?"
  - escolher_modo: "direto ou plan?"

durante_execucao:
  - monitorar_tokens: true
  - verificar_incrementalmente: true
  - reset_se_necessario: "2 falhas = /clear"

comportamento_coach:
  - sugerir_clear: "proativamente"
  - solicitar_verificacao: "sempre"
  - alertar_over_engineering: "quando detectar"
  - recomendar_subagentes: "investigações grandes"
```

---

**INTEIA - Inteligência Estratégica**
*Dr. Igor Morais Vasconcelos PhD*
*"Contexto otimizado, resultados maximizados"*
