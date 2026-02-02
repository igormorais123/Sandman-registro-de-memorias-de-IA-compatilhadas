# 🧠 Sistema de Memória Hierárquica Claude Code

> Instruções globais para o sistema de memória persistente
> Este arquivo é carregado quando não há projeto específico ativo

---

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMÓRIA GLOBAL                                │
│              ~/.claude-memoria-global/                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Aprendizados cross-projeto | Padrões universais | Meta-conhecimento ││
│  └─────────────────────────────────────────────────────────────┘│
│                          ▲                                       │
│              ┌───────────┼───────────┐                          │
│              │           │           │                          │
│         sincroniza   sincroniza  sincroniza                     │
│              │           │           │                          │
│              ▼           ▼           ▼                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ Projeto A   │ │ Projeto B   │ │ Projeto C   │               │
│  │ .memoria/   │ │ .memoria/   │ │ .memoria/   │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estrutura Global

```
~/.claude-memoria-global/
├── CLAUDE.md                      # Este arquivo
├── INDICE_GLOBAL.md               # Dashboard e navegação
├── CONHECIMENTO_UNIVERSAL.md      # Aprendizados cross-projeto
├── CATALOGO_PROJETOS.md           # Registro de todos os projetos
├── PADROES_CODIGO.md              # Soluções reutilizáveis
├── ANTIPADROES_GLOBAIS.md         # O que evitar sempre
├── PROMPTS_EFETIVOS.md            # Prompts que funcionam bem
├── FERRAMENTAS_RECOMENDADAS.md    # MCPs, SDKs, extensões
├── META_APRENDIZADO.md            # Aprendizados sobre o sistema
├── PROTOCOLO_SONO_GLOBAL.md       # Consolidação cross-projeto
├── projetos/                      # Arquivos por projeto
├── consolidado/                   # Conhecimento consolidado
├── meta/                          # Metadados do sistema
├── scripts/                       # Scripts utilitários
├── temp/                          # Arquivos temporários
└── template-projeto/              # Template para novos projetos
```

---

## Comandos Disponíveis

### Nível Global

| Comando | Descrição |
|---------|-----------|
| `status memória global` | Estatísticas cross-projeto |
| `ciclo de sono global` | Consolidação de todos os projetos |
| `buscar conhecimento global sobre X` | Busca em todos os projetos |
| `listar projetos registrados` | Mostra catálogo |
| `qual projeto sabe sobre X?` | Identifica fonte de conhecimento |
| `registrar novo projeto` | Adiciona projeto ao catálogo |

### Sonho Livre (Processamento Criativo)

| Comando | Descrição |
|---------|-----------|
| `sonhe rápido sobre X` | Sonho de 15-20min focado em tema |
| `sonho profundo` | Sonho de 40-60min, tema amplo |
| `explore livremente` | Sonho sem limites, total liberdade |
| `continue o último sonho` | Retoma sonho anterior |
| `responda pergunta N` | Foca em pergunta da fila pendente |
| `ver perguntas pendentes` | Lista perguntas aguardando exploração |

**Arquivos de sonho:** `~/.claude-memoria-global/sonhos/`
**Protocolo:** `PROTOCOLO_SONHO_LIVRE.md`

### Nível Projeto (quando em diretório com .memoria/)

| Comando | Descrição |
|---------|-----------|
| `carregar contexto` | Carrega estado do projeto |
| `ciclo de sono` | Consolidação local |
| `registrar sessão` | Salva sessão atual |
| `consultar memória sobre X` | Busca local e global |
| `sincronizar com global` | Exporta/importa conhecimento |

---

## Protocolos

### Inicializar Memória em Novo Projeto

```
COMANDO: Inicializar sistema de memória

1. Copiar estrutura de ~/.claude-memoria-global/template-projeto/
2. Configurar .memoria/SYNC_GLOBAL.md com dados do projeto
3. Personalizar CLAUDE.md do projeto
4. Registrar projeto em ~/.claude-memoria-global/CATALOGO_PROJETOS.md
5. Criar entrada em ~/.claude-memoria-global/projetos/[projeto].md
```

### Registrar Projeto Existente

```
COMANDO: Registrar projeto na memória global

1. Verificar se .memoria/ existe (criar se não)
2. Adicionar entrada em CATALOGO_PROJETOS.md
3. Configurar SYNC_GLOBAL.md
4. Atualizar INDICE_GLOBAL.md
```

### Sincronização Bidirecional

```
COMANDO: Sincronizar com memória global

EXPORTAÇÃO (projeto → global):
1. Ler .memoria/SYNC_GLOBAL.md para regras
2. Identificar itens em MEMORIA_LONGO_PRAZO.md com tag "consolidado"
3. Filtrar conforme regras de exportação
4. Para cada item elegível:
   a. Verificar duplicidade no global
   b. Se novo: adicionar ao arquivo global apropriado
   c. Se existente: avaliar merge/atualização
   d. Registrar origem em CONHECIMENTO_UNIVERSAL.md
5. Atualizar log de sincronização

IMPORTAÇÃO (global → projeto):
1. Ler .memoria/SYNC_GLOBAL.md para regras
2. Buscar em CONHECIMENTO_UNIVERSAL.md itens relevantes
3. Filtrar por tecnologias/domínios do projeto
4. Disponibilizar referências (não duplicar)
5. Atualizar lista de conhecimento importado
```

### Ciclo de Sono Local

```
COMANDO: Ciclo de sono

Executar fases conforme .memoria/PROTOCOLO_SONO.md:
1. REM 1: Coleta de fragmentos da sessão
2. REM 2: Processamento e classificação
3. REM 3: Consolidação em arquivos apropriados
4. REM 4: Limpeza de conteúdo temporário
5. REM 5: Avaliação para memória global
```

### Ciclo de Sono Global

```
COMANDO: Ciclo de sono global

Executar fases conforme PROTOCOLO_SONO_GLOBAL.md:
1. Inventário de todos os projetos
2. Análise cross-projeto
3. Consolidação universal
4. Limpeza global
5. Meta-análise
```

---

## Hierarquia de Busca

Ao buscar informação, seguir esta ordem:

1. **Memória local do projeto** (se em projeto)
   - .memoria/MEMORIA_LONGO_PRAZO.md
   - .memoria/APRENDIZADOS.md
   - .memoria/CONTEXTO_ATIVO.md

2. **Memória global**
   - CONHECIMENTO_UNIVERSAL.md
   - PADROES_CODIGO.md (se for sobre código)
   - ANTIPADROES_GLOBAIS.md (se for sobre problemas)
   - PROMPTS_EFETIVOS.md (se for sobre prompts)

3. **Projetos relacionados**
   - Consultar CATALOGO_PROJETOS.md
   - Buscar em projetos com tecnologias similares

---

## Critérios de Consolidação

### O que consolidar localmente
- Decisões arquiteturais do projeto
- Padrões específicos do codebase
- Soluções de problemas recorrentes
- Conhecimento do domínio de negócio
- Configurações que funcionam

### O que promover para global
- Soluções que funcionaram em 2+ projetos
- Padrões de código genéricos
- Antipadrões identificados múltiplas vezes
- Prompts com alta taxa de sucesso
- Descobertas técnicas não documentadas oficialmente

### O que NÃO manter
- Código muito específico do domínio
- Soluções temporárias/workarounds
- Informação facilmente encontrável
- Detalhes de implementação voláteis

---

## Tags do Sistema

### Para classificação
- `#consolidado` - Pronto para memória de longo prazo
- `#candidato-global` - Avaliar para exportação
- `#local-only` - Nunca exportar
- `#sensivel` - Contém info sensível
- `#validado` - Testado e confirmado
- `#experimental` - Ainda em validação

### Para tipo de conhecimento
- `#decisao` - Decisão arquitetural
- `#padrao` - Padrão de código
- `#antipadrao` - O que evitar
- `#solucao` - Resolução de problema
- `#config` - Configuração
- `#dominio` - Conhecimento de negócio

---

## Manutenção do Sistema

### Verificação de Integridade
```bash
~/.claude-memoria-global/scripts/check-memory.sh
```

### Backup Recomendado
- Incluir `~/.claude-memoria-global/` em backups
- Incluir `.memoria/` de cada projeto no git (se apropriado)

### Limpeza Periódica
- Executar ciclo de sono global mensalmente
- Arquivar projetos inativos > 90 dias
- Remover conhecimento obsoleto

---

## Métricas de Saúde

O sistema está saudável quando:
- [ ] Todos os arquivos de índice existem
- [ ] Projetos ativos estão sincronizados recentemente
- [ ] Sem contradições não resolvidas entre projetos
- [ ] Ciclo de sono executado regularmente
- [ ] Conhecimento está sendo reutilizado

---

## Troubleshooting

### "Memória não encontrada"
→ Verificar se ~/.claude-memoria-global/ existe
→ Executar script de verificação
→ Reconstruir estrutura se necessário

### "Projeto não sincroniza"
→ Verificar .memoria/SYNC_GLOBAL.md
→ Confirmar registro em CATALOGO_PROJETOS.md
→ Verificar regras de exportação/importação

### "Conhecimento duplicado"
→ Executar ciclo de sono global
→ Consolidar entradas duplicadas manualmente
→ Ajustar critérios de consolidação

---

## Evolução do Sistema

Este sistema é projetado para evoluir. Registrar em META_APRENDIZADO.md:
- O que funciona bem
- O que precisa melhorar
- Experimentos em andamento
- Métricas de eficácia
