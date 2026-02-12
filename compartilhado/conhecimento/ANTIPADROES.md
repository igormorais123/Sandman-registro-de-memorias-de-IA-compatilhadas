# Antipadrões - O Que Evitar

> Erros cometidos e armadilhas a serem evitadas.

---

## Antipadrões de Automação

### 2026-01-20 - Dependência de PC Ligado 24/7
**Contexto**: Sistemas que precisam rodar continuamente
**Erro**: Assumir que o PC estará sempre ligado
**Consequência**: Tarefas não executam, dados se perdem
**Solução**: Usar consolidação ao boot + backlog de tarefas pendentes

### 2026-01-20 - Passos Manuais em Fluxos Automáticos
**Contexto**: Automação de processos
**Erro**: Incluir passos que requerem intervenção manual
**Consequência**: Fluxo quebra quando usuário esquece
**Solução**: Eliminar ou automatizar todo passo manual possível

---

## Antipadrões de Custo

### 2026-01-20 - APIs Pagas Desnecessárias
**Contexto**: Integrações que oferecem API paga
**Erro**: Usar API quando há alternativa via assinatura existente
**Consequência**: Custos recorrentes desnecessários
**Solução**: Sempre verificar se assinatura atual cobre o caso de uso

---

## Antipadrões de Integração

### 2026-01-20 - Contexto Excessivo
**Contexto**: Custom Instructions e prompts de sistema
**Erro**: Incluir informação demais (> 1500 chars)
**Consequência**: Lentidão, custo de tokens, informação ignorada
**Solução**: CORE/ com resumo, detalhes sob demanda em CONHECIMENTO/

---

*Última consolidação: 2026-01-20*
