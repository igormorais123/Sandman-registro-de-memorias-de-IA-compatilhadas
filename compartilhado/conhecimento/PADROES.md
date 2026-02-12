# Padrões de Código e Arquitetura

> Soluções que funcionaram bem e devem ser reutilizadas.

---

## Padrões de Automação

### 2026-01-20 - Consolidação via Task Scheduler
**Contexto**: Automação de tarefas recorrentes no Windows
**Padrão**:
- Usar Task Scheduler para tarefas que devem rodar ao ligar PC
- Criar arquivos .bat para lógica de negócio
- Usar PowerShell para scripts mais complexos
**Aplicação**: Qualquer tarefa que precise rodar periodicamente sem intervenção

---

## Padrões de Integração Multi-IA

### 2026-01-20 - GitHub como Hub Central
**Contexto**: Compartilhar informação entre múltiplas IAs
**Padrão**:
- GitHub para versionamento e acesso universal
- Arquivos Markdown para máxima compatibilidade
- Estrutura CORE/ para informações essenciais (< 1500 chars)
- Estrutura CONHECIMENTO/ para detalhes sob demanda
**Aplicação**: Qualquer sistema que precise ser consultado por múltiplas IAs

---

## Padrões de Documentação

### Formato de Registro
```markdown
### [DATA] - [Título]
**Contexto**: [Situação]
**Padrão/Solução**: [O que fazer]
**Aplicação**: [Quando usar]
```

---

*Última consolidação: 2026-01-20*
