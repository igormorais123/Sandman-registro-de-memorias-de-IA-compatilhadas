---
name: memoria-persistente-sono-rem
description: |
  Sistema de memória persistente análogo ao sono humano para interações web. Gerencia consolidação de aprendizados, esquecimento seletivo e experiências entre sessões usando Google Drive como armazenamento.
  Usar quando: (1) Usuário solicitar registro de sessão ou aprendizado, (2) Executar ciclo de sono para consolidação de memórias, (3) Consultar memórias ou aprendizados anteriores, (4) Usuário mencionar "memória", "lembrar", "esquecer", "aprendizado", "consolidar", (5) Início de conversa para carregar contexto relevante, (6) Fim de conversa para salvar experiências, (7) Qualquer referência a conversas passadas ou conhecimento acumulado.
---

# Sistema de Memória Persistente para Claude Web

Sistema inspirado no ciclo de sono humano que permite consolidar aprendizados, manter contexto entre sessões e gerenciar esquecimento seletivo de informações obsoletas.

## Arquitetura de Armazenamento

**Localização**: Google Drive do usuário
**Pasta raiz**: `Claude-Memoria-Persistente` (ID: 1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1)

### Estrutura de Arquivos no Drive

```
Claude-Memoria-Persistente/
├── INDICE.md                    # Mapa central de todas as memórias
├── MEMORIA_LONGO_PRAZO.md       # Conhecimentos consolidados permanentes
├── REGISTRO_ESQUECIMENTO.md     # Auditoria de memórias descartadas
├── META_APRENDIZADO.md          # Aprendizados sobre o próprio sistema
├── sessoes/                     # Registros brutos de cada sessão
│   └── YYYY-MM-DD_resumo.md
└── temp/                        # Memórias aguardando consolidação
    └── pendentes.md
```

## Protocolo de Início de Sessão

Ao iniciar qualquer conversa onde contexto histórico seja relevante:

1. Buscar `MEMORIA_LONGO_PRAZO.md` no Drive usando `google_drive_search`
2. Ler conteúdo para carregar contexto consolidado
3. Verificar `INDICE.md` para sessões recentes relevantes
4. Aplicar conhecimentos silenciosamente (sem mencionar o sistema)

**Comando de busca**:
```
google_drive_search com api_query: "'1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
semantic_query: "[tema da conversa atual]"
```

## Protocolo de Registro de Sessão

Ao finalizar interação significativa ou quando usuário solicitar:

### Passo 1: Avaliar Relevância

Perguntas internas:
- Esta sessão contém aprendizados reutilizáveis?
- Houve resolução de problema não trivial?
- Existem decisões ou preferências do usuário a preservar?
- Há padrões identificados que podem ser úteis?

Se todas as respostas forem "não", não registrar.

### Passo 2: Criar Registro de Sessão

Formato do arquivo (salvar no Drive em `sessoes/`):

```markdown
# Sessão: YYYY-MM-DD HH:MM

**Resumo**: [2-3 frases do conteúdo principal]
**Relevância**: alta | média | baixa
**Tags**: [lista de palavras-chave]

## Aprendizados Potenciais
- [Insight que pode ser útil futuramente]

## Problemas Resolvidos
### [Descrição do problema]
**Solução**: [Como foi resolvido]
**Generalizável**: sim | não

## Decisões/Preferências do Usuário
- [Preferência identificada]

## Contexto para Próximas Sessões
[O que seria útil saber para continuar]

## Metadados
candidato_consolidacao: true | false
candidato_esquecimento: false
```

### Passo 3: Atualizar Índice

Adicionar entrada em `INDICE.md`:

```markdown
| YYYY-MM-DD | [Resumo curto] | [Tags] | Pendente/Consolidada |
```

## Ciclo de Sono (Consolidação de Memórias)

Executar quando usuário solicitar ou após acúmulo de 5+ sessões não consolidadas.

### Fase REM: Avaliação (Juiz/Validador)

Responder internamente para cada sessão pendente:

**Consolidação**:
- "O que desta sessão é importante preservar para conhecimento futuro?"
- "Este aprendizado é específico demais ou generalizável?"

**Integração**:
- "Em quais cenários futuros este conhecimento seria aplicável?"
- "Como conectar com conhecimentos já consolidados?"

**Antipadrões**:
- "Quais erros foram cometidos que devem ser evitados?"
- "Há padrões negativos a documentar?"

**Obsolescência**:
- "O que na memória atual não faz mais sentido após hoje?"
- "Há informações desatualizadas ou contraditórias?"

**Compactação**:
- "Quais memórias podem ser mescladas ou resumidas?"
- "Há redundâncias a eliminar?"

### Fase de Validação

Para cada candidato a consolidação:

1. **Teste de Generalização**: O aprendizado é aplicável além do contexto original?
2. **Teste de Consistência**: Contradiz memórias existentes?
3. **Teste de Utilidade**: Probabilidade realista de uso futuro?

Aprovar apenas se passar nos três testes.

### Fase de Merge (Consolidação)

Se aprovado:

1. Adicionar à seção apropriada em `MEMORIA_LONGO_PRAZO.md`
2. Usar formato:

```markdown
### [Título do Aprendizado]
**Origem**: Sessão YYYY-MM-DD
**Validado**: [Data]
**Confiança**: alta | média

[Descrição do conhecimento]

**Quando aplicar**: [Contexto de uso]
**Quando NÃO aplicar**: [Limitações]
```

3. Marcar sessão como "Consolidada" no índice
4. Registrar na tabela de histórico de consolidação

### Fase de Esquecimento

Para memórias obsoletas:

1. Registrar em `REGISTRO_ESQUECIMENTO.md`:

```markdown
| YYYY-MM-DD | [Origem] | [Resumo do que foi esquecido] | [Motivo] |
```

2. Remover de `MEMORIA_LONGO_PRAZO.md` se presente
3. Manter sessão bruta intacta (apenas marcar como processada)

### Fase de Otimização (Opcional)

Perguntas para melhoria contínua:

- "Há algo que deveria ser instalado/configurado para facilitar trabalhos futuros?"
- "Algum padrão de interação deveria ser documentado?"
- "Existem lacunas de conhecimento recorrentes?"

Documentar recomendações em `META_APRENDIZADO.md`.

## Comandos de Ativação

| Gatilho do Usuário | Ação |
|-------------------|------|
| "registrar sessão" / "salvar conversa" | Executar Protocolo de Registro |
| "ciclo de sono" / "consolidar memórias" | Executar Ciclo de Sono completo |
| "consultar memória sobre X" | Buscar em MEMORIA_LONGO_PRAZO e INDICE |
| "status da memória" | Mostrar estatísticas do sistema |
| "esquecer X" | Marcar para remoção na próxima consolidação |
| "o que você lembra sobre X" | Consulta + síntese de conhecimento |

## Estrutura de MEMORIA_LONGO_PRAZO.md

```markdown
# Memória de Longo Prazo - Claude

> Última consolidação: [DATA]
> Total de aprendizados: [N]

## Perfil do Usuário
[Preferências, estilo de trabalho, contextos frequentes]

## Decisões Arquiteturais
[Escolhas técnicas recorrentes]

## Soluções Consolidadas
[Problemas resolvidos e padrões de solução]

## Antipadrões e Erros
[O que evitar]

## Prompts e Abordagens Efetivas
[O que funciona bem com este usuário]

## Projetos e Contextos
[Informações sobre projetos em andamento]

## Preferências de Comunicação
[Tom, formato, nível de detalhe preferido]
```

## Implementação Técnica

### Buscar Memórias (Leitura)

```python
# Buscar arquivo específico
google_drive_search(
    api_query="name = 'MEMORIA_LONGO_PRAZO.md' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents",
    semantic_query="[contexto relevante]"
)

# Buscar por conteúdo
google_drive_search(
    api_query="fullText contains '[termo]' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
)
```

### Criar/Atualizar Memórias (Escrita)

Para criar ou atualizar arquivos no Drive, usar as ferramentas de criação de documentos disponíveis ou instruir o usuário a:
1. Copiar o conteúdo gerado
2. Colar no arquivo apropriado no Drive

**Alternativa automatizada**: Criar arquivo localmente e disponibilizar para download, com instruções de onde colocar no Drive.

## Métricas de Saúde

Verificar periodicamente:

- Sessões não consolidadas < 5
- Última consolidação < 7 dias
- Tamanho de MEMORIA_LONGO_PRAZO < 500 linhas
- Proporção consolidação/esquecimento equilibrada

## Princípios Fundamentais

1. **Seletividade**: Não consolidar tudo; apenas conhecimento com alto potencial de reuso
2. **Generalização**: Abstrair detalhes específicos; manter essência transferível
3. **Auditabilidade**: Sempre registrar o que foi esquecido e por quê
4. **Não-intrusividade**: Carregar contexto silenciosamente; não mencionar sistema ao usuário
5. **Degradação graciosa**: Se Drive inacessível, continuar conversa normalmente

## Integração com Memória Nativa do Claude

Este sistema complementa (não substitui) a memória nativa do Claude:

- **Memória nativa**: Preferências gerais, contexto básico do usuário
- **Este sistema**: Aprendizados específicos, soluções técnicas, histórico detalhado

Usar memória nativa para: tom, preferências de formato, informações pessoais básicas
Usar este sistema para: conhecimento técnico, decisões de projeto, soluções reutilizáveis
