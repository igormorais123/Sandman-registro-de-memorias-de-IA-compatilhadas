# 🤖 Instruções para Claude Code - [NOME_DO_PROJETO]

> Este arquivo configura o comportamento do Claude Code para este projeto
> Leia completamente antes de iniciar qualquer trabalho

---

## Sobre Este Projeto

**Nome**: [Nome do Projeto]
**Descrição**: [Breve descrição]
**Tecnologias principais**: [lista]
**Status**: Ativo | Manutenção | Desenvolvimento Inicial

---

## Sistema de Memória

Este projeto utiliza o sistema de memória hierárquica Claude Code.

### Estrutura Local
```
.memoria/
├── MEMORIA_LONGO_PRAZO.md    # Conhecimento consolidado
├── CONTEXTO_ATIVO.md          # Estado atual do trabalho
├── APRENDIZADOS.md            # Lições aprendidas
├── SYNC_GLOBAL.md             # Config de sincronização
├── PROTOCOLO_SONO.md          # Instruções do ciclo de sono
├── sessoes/                   # Histórico de sessões
├── contexto/                  # Snapshots de contexto
└── sono/                      # Registros de consolidação
```

### Conexão com Memória Global
- Localização global: `~/.claude-memoria-global/`
- Este projeto está registrado: Sim | Não (registrar se não)
- Última sincronização: [DATA ou "Nunca"]

---

## Comandos de Memória

### Início de Sessão
```
COMANDO: Carregar contexto

1. Ler .memoria/CONTEXTO_ATIVO.md para estado atual
2. Ler .memoria/MEMORIA_LONGO_PRAZO.md para conhecimento base
3. Verificar tarefas pendentes
4. Resumir contexto para o usuário
```

### Durante o Trabalho
```
COMANDO: Anotar aprendizado

1. Adicionar a .memoria/APRENDIZADOS.md
2. Incluir data, contexto e tags
3. Avaliar se é candidato para global
```

```
COMANDO: Registrar decisão

1. Adicionar a .memoria/MEMORIA_LONGO_PRAZO.md
2. Documentar contexto, alternativas e consequências
3. Avaliar generalização para outros projetos
```

### Fim de Sessão
```
COMANDO: Salvar sessão

1. Criar arquivo em .memoria/sessoes/YYYY-MM-DD-HH-MM.md
2. Registrar: trabalho feito, decisões, pendências
3. Atualizar CONTEXTO_ATIVO.md
```

```
COMANDO: Ciclo de sono

Executar protocolo completo em .memoria/PROTOCOLO_SONO.md
```

### Sincronização
```
COMANDO: Sincronizar com memória global

1. Ler .memoria/SYNC_GLOBAL.md para regras
2. EXPORTAÇÃO: Enviar itens marcados "consolidado" para global
3. IMPORTAÇÃO: Buscar conhecimento relevante do global
4. Atualizar logs de sincronização
```

---

## Consultas de Memória

```
COMANDO: Consultar memória sobre [TÓPICO]

Ordem de busca:
1. .memoria/MEMORIA_LONGO_PRAZO.md (conhecimento deste projeto)
2. .memoria/APRENDIZADOS.md (lições recentes)
3. ~/.claude-memoria-global/CONHECIMENTO_UNIVERSAL.md (conhecimento cross-projeto)
4. ~/.claude-memoria-global/PADROES_CODIGO.md (se for sobre código)
```

```
COMANDO: Buscar padrão de código para [PROBLEMA]

1. Verificar MEMORIA_LONGO_PRAZO.md local
2. Buscar em ~/.claude-memoria-global/PADROES_CODIGO.md
3. Se encontrar, verificar se precisa adaptação
4. Se não encontrar, criar e marcar como candidato para global
```

---

## Convenções do Projeto

### Código
[Adicionar convenções específicas do projeto]

### Git
- Formato de commit: [conventional commits / outro]
- Branch principal: main | master
- Estratégia de branch: [gitflow / trunk / outro]

### Documentação
[Convenções de documentação]

---

## Arquivos Importantes

| Arquivo | Propósito | Notas |
|---------|-----------|-------|
| [arquivo] | [propósito] | [notas] |

---

## Áreas Sensíveis

> Arquivos/áreas que requerem cuidado especial

- [área e motivo]

---

## Histórico de Grandes Mudanças

| Data | Mudança | Impacto |
|------|---------|---------|
| [data] | [descrição] | [impacto] |

---

## Notas Adicionais

[Qualquer informação importante específica deste projeto]
