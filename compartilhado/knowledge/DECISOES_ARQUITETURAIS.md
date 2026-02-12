# Decisões Arquiteturais (ADRs)

> Registro de decisões importantes e seu racional
> NÃO reverter sem análise completa

---

## Sistema de Memória Multi-IA

### DEC-001: Google Drive como Hub Central
**Data**: 2026-01-20
**Status**: Aprovada
**Decisão**: Usar Google Drive (não GitHub) como fonte principal de verdade

**Alternativas Consideradas**:
| Opção | Prós | Contras |
|-------|------|---------|
| **GitHub** | Versionamento, todas IAs leem, Copilot nativo | Gemini não tem live link, ChatGPT read-only |
| **Google Drive** | Live link Gemini, Connected Apps ChatGPT, mobile nativo | Versionamento fraco |
| Notion | Boa API, estruturada | Custo, complexidade |
| Arquivo local | Simples | Sem acesso remoto |

**Racional**:
- Único storage com live link no Gemini Gems
- Connected Apps funciona no ChatGPT
- MCP disponível para Claude
- Sync local é transparente via Google Drive Desktop
- App mobile nativo

**Consequências**:
- GitHub usado apenas para backup/versão pública
- Sync automático via script PowerShell

---

### DEC-002: Claude Code como Consolidador Único
**Data**: 2026-01-20
**Status**: Aprovada
**Decisão**: Apenas Claude Code escreve na memória; outras IAs são read-only

**Alternativas Consideradas**:
| Opção | Prós | Contras |
|-------|------|---------|
| **Claude Code único** | Sem conflitos, usa Claude Max ($0) | Só consolida com PC ligado |
| Cada IA consolida | Paralelo | Conflitos, inconsistência |
| GitHub Actions + API | 24/7 | Custo de API (~$5-20/mês) |
| Cloudflare Workers | 24/7, cheap | Complexidade, ainda usa API |

**Racional**:
- Usa assinatura Claude Max existente (custo $0)
- Acesso ao Opus 4.5 sem API
- Execução local mais rápida
- Evita conflitos de escrita

**Consequências**:
- Task Scheduler necessário para automação
- Consolidação só ocorre quando PC está ligado
- Hook de sessão como complemento

---

### DEC-003: Zero Passos Manuais
**Data**: 2026-01-20
**Status**: Aprovada
**Decisão**: Eliminar qualquer passo que requeira ação manual do usuário

**Racional**:
- Passos manuais são esquecidos e quebram o sistema
- Automação total garante consistência
- Usuário deve apenas usar as IAs normalmente

**Consequências**:
- Algumas IAs são completamente read-only
- Task Scheduler + hooks + sync automático
- Setup inicial é o único momento manual

---

### DEC-004: Arquivos CORE < 1500 caracteres
**Data**: 2026-01-20
**Status**: Aprovada
**Decisão**: Manter cada arquivo em CORE/ com menos de 1500 caracteres

**Racional**:
- Custom Instructions do ChatGPT têm limite
- Contexto leve não consome tokens excessivos
- Informação densa é mais útil que verbosa

**Consequências**:
- Detalhes ficam em arquivos separados (sob demanda)
- CORE/ contém apenas resumo essencial
- Referências a URLs em vez de conteúdo inline

---

### DEC-005: Consolidação Dual (Boot + Sessões)
**Data**: 2026-01-20
**Status**: Aprovada
**Decisão**: Consolidar automaticamente ao ligar PC E a cada 10 sessões

**Alternativas Consideradas**:
| Opção | Prós | Contras |
|-------|------|---------|
| Só boot | Simples | Pode demorar se PC fica ligado |
| Só sessões | Frequente | Não executa se PC reiniciou |
| **Boot + sessões** | Cobertura completa | Dois triggers |
| Tempo fixo (cron) | Previsível | Pode rodar com PC idle |

**Racional**:
- Boot garante que sempre roda ao usar PC
- Sessões garante frequência em uso intenso
- Verificação de 24h evita redundância

**Consequências**:
- Task Scheduler: ConsolidacaoMemoriaClaudeCode
- Hook: hook_contador.ps1
- Arquivo .ultima_consolidacao como controle

---

## Projetos Específicos

### DEC-ORACULO-001: Web Speech API para Entrada de Voz
**Data**: 2026-01-20
**Projeto**: Participa-DF / ORÁCULO DF
**Status**: Proposta
**Decisão**: Usar Web Speech API nativa do browser (não API externa)

**Racional**:
- Custo $0 (browser built-in)
- Funciona em Chrome/Edge
- Sem dependência de serviço externo

**Consequências**:
- Não funciona em Firefox/Safari
- Qualidade pode variar
- Fallback para entrada de texto necessário

---

## Template para Novas Decisões

```markdown
### DEC-XXX: [Título da Decisão]
**Data**: YYYY-MM-DD
**Projeto**: [Nome do projeto ou "Global"]
**Status**: [Proposta | Em discussão | Aprovada | Obsoleta]
**Decisão**: [Resumo em uma frase]

**Contexto**:
[Por que essa decisão precisou ser tomada]

**Alternativas Consideradas**:
| Opção | Prós | Contras |
|-------|------|---------|

**Racional**:
[Por que esta opção foi escolhida]

**Consequências**:
[O que muda por causa desta decisão]
```

---

*Última atualização: 2026-01-20*
