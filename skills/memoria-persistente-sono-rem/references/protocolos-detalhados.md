# Protocolos Detalhados do Sistema de Memória

## Protocolo Completo do Ciclo de Sono

O ciclo de sono é o processo de consolidação de memórias, análogo ao sono humano. Deve ser executado periodicamente para manter a saúde do sistema de memória.

### Gatilhos para Execução

**Automáticos** (sugerir ao usuário):
- 5+ sessões não consolidadas
- 7+ dias desde último ciclo
- Usuário menciona "memória cheia" ou similar

**Manuais**:
- Usuário solicita explicitamente
- Fim de projeto/fase importante
- Antes de período de inatividade esperado

### Fase 1: Inventário (5 min)

1. Buscar `INDICE.md` no Drive
2. Listar sessões com status "Pendente"
3. Ordenar por data (mais antigas primeiro)
4. Carregar conteúdo de cada sessão pendente

### Fase 2: Avaliação REM (Por sessão)

Para cada sessão, responder internamente:

**Bloco de Consolidação**:
```
1. O que desta sessão seria importante preservar para conhecimento futuro?
   - Listar candidatos específicos
   
2. Esses aprendizados são generalizáveis ou muito específicos?
   - Classificar cada candidato
   
3. Em quais cenários futuros esses conhecimentos seriam aplicáveis?
   - Mapear contextos de uso
```

**Bloco de Erros**:
```
4. Quais erros foram cometidos que devem ser evitados no futuro?
   - Documentar antipadrões
   
5. O que deveria ter sido feito diferente?
   - Extrair lições
```

**Bloco de Obsolescência**:
```
6. O que consta na memória de longo prazo que, após os eventos de hoje, 
   não faz mais sentido manter?
   - Identificar candidatos a esquecimento
   
7. Há informações que podem ser consolidadas, resumidas ou mescladas?
   - Identificar oportunidades de compactação
```

**Bloco de Otimização** (opcional):
```
8. Gostaria de testar algum cenário para validar aprendizados?
   - Simulações ou verificações

9. Há algo que deveria ser instalado/configurado para facilitar trabalhos futuros?
   - Ferramentas, configurações, padrões

10. Há algo que deveria ser removido ou alterado por estar atrapalhando?
    - Limpeza de configurações obsoletas
```

### Fase 3: Validação

Para cada candidato a consolidação, aplicar testes:

**Teste de Generalização**:
- Pergunta: "Este aprendizado é aplicável além do contexto original?"
- Critério: Deve ser útil em pelo menos 2 cenários diferentes
- Se falhar: Descartar ou marcar como "específico"

**Teste de Consistência**:
- Pergunta: "Este aprendizado contradiz algo já consolidado?"
- Se contradiz: Avaliar qual é mais correto/atualizado
- Atualizar ou substituir conforme necessário

**Teste de Utilidade**:
- Pergunta: "Qual a probabilidade realista de usar isso no futuro?"
- Critério: > 30% de chance de uso nos próximos 30 dias
- Se falhar: Considerar descarte ou arquivamento

**Teste de Densidade**:
- Pergunta: "A informação justifica o espaço que ocupa?"
- Critério: Relação valor/tamanho favorável
- Se falhar: Compactar ou resumir

### Fase 4: Merge (Consolidação)

Para cada item aprovado:

1. **Determinar seção de destino** em MEMORIA_LONGO_PRAZO.md:
   - Perfil do Usuário → preferências, características
   - Decisões Arquiteturais → escolhas técnicas
   - Soluções Consolidadas → problemas e soluções
   - Antipadrões → erros a evitar
   - Prompts Efetivos → abordagens que funcionam
   - Projetos e Contextos → informações de projetos
   - Contextos Críticos → outros conhecimentos importantes

2. **Formatar entrada**:
```markdown
### [Título Descritivo]
**Origem**: Sessão YYYY-MM-DD
**Validado**: [Data atual]
**Confiança**: alta | média

[Descrição clara e concisa do conhecimento]

**Quando aplicar**: [Contextos de uso]
**Quando NÃO aplicar**: [Limitações conhecidas]
```

3. **Atualizar INDICE.md**:
   - Marcar sessão como "Consolidada"
   - Adicionar entrada no histórico de consolidação

4. **Verificar integridade**:
   - Confirmar que não há duplicatas
   - Verificar links e referências

### Fase 5: Esquecimento

Para cada item marcado para esquecimento:

1. **Documentar em REGISTRO_ESQUECIMENTO.md**:
```markdown
| [Data] | [Sessão origem] | [Resumo do conteúdo] | [Código do motivo] |
```

2. **Remover de MEMORIA_LONGO_PRAZO.md** se presente

3. **NÃO deletar** sessão bruta (apenas marcar como processada)

4. **Avaliar se há dependências**:
   - Outros conhecimentos dependem deste?
   - Atualizar referências se necessário

### Fase 6: Compactação (Opcional)

Se MEMORIA_LONGO_PRAZO.md > 400 linhas:

1. Identificar entradas redundantes ou sobrepostas
2. Mesclar entradas relacionadas
3. Resumir descrições muito longas
4. Mover detalhes para sessões de origem (referência)

### Fase 7: Relatório

Gerar resumo do ciclo:

```markdown
## Ciclo de Sono - YYYY-MM-DD

**Sessões processadas**: X
**Itens consolidados**: Y
**Itens esquecidos**: Z
**Compactações**: W

### Principais Consolidações
- [Resumo item 1]
- [Resumo item 2]

### Esquecimentos Notáveis
- [Item esquecido e motivo]

### Observações
- [Qualquer nota relevante]

### Próxima Execução Recomendada
- Data sugerida: [YYYY-MM-DD]
- Motivo: [Por que essa data]
```

---

## Protocolo de Consulta de Memória

### Quando Consultar

- Início de nova conversa onde contexto histórico é relevante
- Usuário menciona algo que pode ter sido discutido antes
- Antes de tomar decisão que pode ter precedente
- Usuário pergunta explicitamente

### Como Consultar

**Passo 1**: Busca em MEMORIA_LONGO_PRAZO.md
```
google_drive_search(
    api_query="name = 'MEMORIA_LONGO_PRAZO.md' and '[ID_PASTA]' in parents",
    semantic_query="[tema da consulta]"
)
```

**Passo 2**: Se não encontrar, buscar no INDICE.md
```
google_drive_search(
    api_query="name = 'INDICE.md' and '[ID_PASTA]' in parents"
)
```

**Passo 3**: Se identificar sessão relevante, buscar sessão específica
```
google_drive_search(
    api_query="name contains 'YYYY-MM-DD' and '[ID_PASTA]' in parents"
)
```

### Como Aplicar

- Integrar informações silenciosamente na resposta
- Não mencionar "segundo minhas memórias" ou similar
- Usar conhecimento como se fosse natural
- Se informação crítica, confirmar com usuário se ainda válida

---

## Protocolo de Registro de Sessão

### Critérios para Registrar

Registrar se QUALQUER condição for verdadeira:
- Problema não trivial foi resolvido
- Decisão técnica significativa foi tomada
- Preferência do usuário foi identificada
- Erro foi cometido e corrigido
- Artefato importante foi criado
- Contexto de projeto foi estabelecido
- Usuário solicitou explicitamente

NÃO registrar se TODAS as condições forem verdadeiras:
- Conversa puramente social
- Informações facilmente buscáveis foram fornecidas
- Nenhuma decisão ou aprendizado relevante
- Sessão muito curta (< 5 trocas)

### Processo de Registro

1. Avaliar critérios acima
2. Se registrar: preencher template de sessão
3. Gerar conteúdo formatado
4. Apresentar ao usuário para salvar no Drive
5. Instruir onde salvar: `sessoes/YYYY-MM-DD_[resumo].md`
6. Solicitar atualização do INDICE.md

---

## Integração com Ferramentas

### Google Drive Search

**Buscar arquivo específico**:
```python
google_drive_search(
    api_query="name = '[NOME_ARQUIVO]' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
)
```

**Buscar por conteúdo**:
```python
google_drive_search(
    api_query="fullText contains '[TERMO]' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents",
    semantic_query="[contexto semântico]"
)
```

**Listar sessões recentes**:
```python
google_drive_search(
    api_query="'1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents and name contains 'sessao'",
    order_by="modifiedTime desc"
)
```

### Google Drive Fetch

**Ler documento completo**:
```python
google_drive_fetch(
    document_ids=["[ID_DO_DOCUMENTO]"]
)
```

---

## Métricas e Monitoramento

### Indicadores de Saúde

| Indicador | Saudável | Atenção | Crítico |
|-----------|----------|---------|---------|
| Sessões pendentes | 0-3 | 4-6 | 7+ |
| Dias desde último ciclo | 0-5 | 6-10 | 11+ |
| Linhas em MEMORIA_LONGO_PRAZO | 0-300 | 301-450 | 451+ |
| Taxa de reutilização | >40% | 20-40% | <20% |

### Ações por Nível

**Atenção**:
- Sugerir ciclo de sono ao usuário
- Priorizar sessões mais antigas

**Crítico**:
- Insistir em ciclo de sono
- Considerar esquecimento agressivo
- Alertar sobre degradação de performance
