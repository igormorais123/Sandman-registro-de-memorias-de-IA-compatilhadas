# 🌙 Protocolo do Ciclo de Sono Global

> Consolidação cross-projeto - executar semanalmente ou quando apropriado

---

## Comando de Ativação

```
COMANDO: Ciclo de sono global
```

ou

```
claude "ciclo de sono global"
```

---

## Pré-Requisitos

- [ ] Ao menos um projeto registrado no catálogo
- [ ] Projetos ativos sincronizados recentemente
- [ ] Ambiente estável (sem tarefas urgentes pendentes)

---

## Fases do Ciclo Global

### FASE 1: Inventário (5-10 min)

**Ações**:
1. Listar todos os projetos em `CATALOGO_PROJETOS.md`
2. Para cada projeto ativo:
   - Verificar última sincronização
   - Identificar candidatos pendentes de exportação
   - Coletar itens marcados para global

**Perguntas-guia**:
- "Quais projetos tiveram atividade desde o último sono global?"
- "Há candidatos de exportação acumulados?"
- "Algum projeto foi arquivado ou abandonado?"

**Output esperado**:
```markdown
## Inventário do Sono Global - [DATA]

### Projetos Ativos
| Projeto | Última Sync | Candidatos Pendentes | Prioridade |
|---------|-------------|---------------------|------------|
| [nome]  | [data]      | [número]            | [alta/média/baixa] |

### Projetos para Arquivar
- [lista se houver]
```

---

### FASE 2: Análise Cross-Projeto (10-15 min)

**Perguntas a responder**:

#### 2.1 Padrões Emergentes
- "Quais soluções apareceram em múltiplos projetos?"
- "Há código duplicado que deveria virar padrão global?"
- "Identifico estruturas similares em diferentes contextos?"

#### 2.2 Contradições
- "Há conhecimentos conflitantes entre projetos?"
- "Qual versão é mais correta/atualizada?"
- "Decisões diferentes para problemas similares - há uma melhor?"

#### 2.3 Lacunas
- "Que conhecimento um projeto tem que outros precisariam?"
- "Há erros em um projeto já resolvidos em outro?"
- "Oportunidades de transferência de aprendizado?"

**Output esperado**:
```markdown
## Análise Cross-Projeto

### Padrões Identificados
1. [padrão] - presente em: [projetos]
   - Candidato para consolidação: Sim/Não

### Contradições Encontradas
1. [descrição] - projetos: [A] vs [B]
   - Resolução proposta: [qual adotar]

### Transferências Recomendadas
1. De [projeto A] para [projeto B]: [conhecimento]
```

---

### FASE 3: Consolidação Universal (15-20 min)

**Ações de consolidação**:

#### 3.1 Promover Padrões Validados
```
SE solução funcionou em 2+ projetos:
   → Adicionar a PADROES_CODIGO.md
   → Registrar projetos de origem
   → Marcar nível de confiança
```

#### 3.2 Generalizar Aprendizados
```
PARA CADA candidato de exportação:
   1. Remover referências específicas do projeto
   2. Abstrair para forma genérica
   3. Adicionar a CONHECIMENTO_UNIVERSAL.md
   4. Registrar projeto de origem
```

#### 3.3 Atualizar Matriz de Conhecimento
```
PARA CADA projeto:
   1. Revisar especialidades declaradas
   2. Atualizar baseado em atividade recente
   3. Corrigir CATALOGO_PROJETOS.md
```

#### 3.4 Consolidar Antipadrões
```
SE mesmo erro apareceu em múltiplos projetos:
   → Promover para ANTIPADROES_GLOBAIS.md
   → Registrar como "validado em N projetos"
```

---

### FASE 4: Limpeza Global (10-15 min)

#### 4.1 Identificar Conhecimento Obsoleto
- Tecnologias que nenhum projeto mais usa
- Soluções substituídas por melhores
- Referências a versões antigas de libs/frameworks

#### 4.2 Compactar Memória
- Mesclar itens redundantes
- Resumir históricos muito longos
- Remover duplicatas entre arquivos

#### 4.3 Arquivar Projetos Inativos
```
SE projeto sem atividade > 90 dias:
   → Mover para seção "Arquivados" no catálogo
   → Preservar conhecimento contribuído
   → Remover da lista de sincronização ativa
```

**Checklist de limpeza**:
- [ ] Conhecimento obsoleto identificado e marcado
- [ ] Duplicatas removidas
- [ ] Projetos inativos arquivados
- [ ] Links internos verificados

---

### FASE 5: Meta-Análise (5-10 min)

#### 5.1 Atualizar META_APRENDIZADO.md

```markdown
### Sessão de Sono Global - [DATA]

**Métricas desta sessão**:
- Projetos processados: X
- Conhecimentos consolidados: Y
- Padrões promovidos: Z
- Antipadrões identificados: W
- Itens arquivados: V

**Observações**:
- [insights sobre o processo]
```

#### 5.2 Avaliar Eficácia do Sistema

**Perguntas**:
- "O conhecimento consolidado está sendo reutilizado?"
- "O formato atual facilita a consulta?"
- "Há fricção desnecessária no processo?"

#### 5.3 Registrar Melhorias Propostas

```markdown
### Melhorias Identificadas

| Área | Problema | Melhoria Proposta | Prioridade |
|------|----------|-------------------|------------|
| [área] | [problema] | [solução] | [alta/média/baixa] |
```

---

## Checklist Pós-Sono Global

### Arquivos Atualizados
- [ ] `INDICE_GLOBAL.md` - dashboard atualizado
- [ ] `CONHECIMENTO_UNIVERSAL.md` - novos itens adicionados
- [ ] `PADROES_CODIGO.md` - novos padrões promovidos
- [ ] `ANTIPADROES_GLOBAIS.md` - novos antipadrões
- [ ] `CATALOGO_PROJETOS.md` - status dos projetos atualizado
- [ ] `META_APRENDIZADO.md` - métricas registradas

### Qualidade
- [ ] Nenhuma contradição não resolvida
- [ ] Links internos funcionando
- [ ] Formato consistente em todos os arquivos
- [ ] Datas atualizadas onde relevante

### Comunicação
- [ ] Resumo do sono disponível para referência
- [ ] Conhecimento importante destacado

---

## Template de Resumo do Sono Global

```markdown
# Resumo do Ciclo de Sono Global
**Data**: [DATA]
**Duração**: [X minutos]

## Projetos Processados
- [lista]

## Principais Consolidações
1. [item mais importante]
2. [segundo mais importante]
3. [terceiro mais importante]

## Ações Tomadas
- [X] conhecimentos promovidos para global
- [Y] padrões de código consolidados
- [Z] antipadrões identificados
- [W] projetos arquivados

## Próximo Sono Global
**Sugerido para**: [data sugerida]
**Prioridade**: [alta/média/baixa]
**Foco recomendado**: [área que precisa atenção]
```

---

## Frequência Recomendada

| Cenário | Frequência |
|---------|------------|
| Desenvolvimento ativo em múltiplos projetos | Semanal |
| Desenvolvimento ativo em um projeto | Quinzenal |
| Manutenção/baixa atividade | Mensal |
| Após grande milestone em qualquer projeto | Imediato |

---

## Troubleshooting

### "Muito conhecimento acumulado"
→ Aumentar frequência do sono
→ Ser mais seletivo na consolidação
→ Usar tags para filtrar relevância

### "Pouco conhecimento novo"
→ Verificar se projetos estão exportando
→ Revisar critérios de consolidação local
→ Pode ser normal em períodos de baixa atividade

### "Contradições frequentes"
→ Estabelecer fonte de verdade por domínio
→ Documentar contexto das diferenças
→ Pode indicar evolução natural do conhecimento
