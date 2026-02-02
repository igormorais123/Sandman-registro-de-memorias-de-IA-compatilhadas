# ⚠️ Antipadrões Globais

> Erros comuns identificados em múltiplos projetos
> O que evitar sempre - aprenda com os erros dos outros

---

## Índice por Categoria

- [Arquitetura](#arquitetura)
- [Código](#código)
- [Segurança](#segurança)
- [Performance](#performance)
- [DevOps](#devops)
- [Processo](#processo)

---

## Arquitetura

### Migração de Cloud Storage Sem Backup Prévio
**Descrição**: Desinstalar um serviço de cloud storage (OneDrive, Dropbox, etc.) antes de migrar completamente os dados para outro.
**Por que é ruim**:
- Pastas especiais (Desktop, Documents) ficam inacessíveis
- Dados podem parecer "perdidos" (estão em local antigo não sincronizado)
- Difícil rollback se processo for interrompido
**Alternativa correta**:
1. Manter serviço antigo instalado durante migração
2. Copiar dados para novo serviço
3. Verificar integridade da cópia
4. Reconfigurar pastas especiais
5. Só então desinstalar serviço antigo
**Projetos afetados**: Conserto-PC (2026-01-08)

### Operações Longas em Sistema Instável
**Descrição**: Iniciar operações que não podem ser interrompidas em um sistema que apresenta crashes frequentes.
**Por que é ruim**:
- Operação interrompida pode deixar sistema em estado inconsistente
- Perda de progresso
- Difícil recuperação
**Alternativa correta**:
1. Dividir operação em etapas pequenas e verificáveis
2. Criar checkpoints a cada etapa
3. Documentar progresso em arquivo
4. Resolver instabilidade antes de operações críticas
**Projetos afetados**: Conserto-PC (múltiplas sessões)

### Dependência de PC Ligado 24/7
**Descrição**: Projetar sistemas que precisam rodar continuamente.
**Por que é ruim**:
- PC doméstico não fica ligado 24/7
- Tarefas não executam quando PC está desligado
- Dados podem se perder entre sessões
**Alternativa correta**:
1. Usar consolidação ao boot + backlog de tarefas pendentes
2. Aceitar trade-off de latência em troca de custo $0
3. Verificar última execução e rodar se necessário
**Projetos afetados**: Sistema-Memoria (2026-01-20)

### Passos Manuais em Fluxos Automáticos
**Descrição**: Incluir etapas que requerem intervenção humana.
**Por que é ruim**:
- Usuário esquece de executar
- Fluxo quebra silenciosamente
- Difícil debugar quando falha
**Alternativa correta**:
1. Automatizar todo passo possível
2. Se manual é inevitável, criar lembrete/alerta
3. Documentar claramente o que é manual
**Projetos afetados**: Sistema-Memoria (2026-01-20)

### APIs Pagas Quando Assinatura Existe
**Descrição**: Usar API paga quando já possui assinatura do serviço.
**Por que é ruim**:
- Custos recorrentes desnecessários
- Duplicação de gastos
- Complexidade adicional de billing
**Alternativa correta**:
1. Verificar se assinatura atual cobre o caso de uso
2. Usar interface/CLI em vez de API quando possível
3. Ex: Claude Max + Claude Code = Opus 4.5 sem custo de API
**Projetos afetados**: Sistema-Memoria (2026-01-20)

<!-- ADICIONAR_ANTIPADRAO_ARQ_AQUI -->

---

## Código

### [Nome do Antipadrão]
**Descrição**: [O que é feito errado]
**Exemplo ruim**:
```[linguagem]
// código problemático
```
**Exemplo correto**:
```[linguagem]
// código correto
```
**Projetos afetados**: [Onde foi identificado]

<!-- ADICIONAR_ANTIPADRAO_CODIGO_AQUI -->

---

## Segurança

### [Nome do Antipadrão]
**Descrição**: [O que é feito errado]
**Risco**: [Crítico | Alto | Médio | Baixo]
**Vetor de ataque**: [Como pode ser explorado]
**Mitigação**: [Como corrigir]

<!-- ADICIONAR_ANTIPADRAO_SEC_AQUI -->

---

## Performance

### [Nome do Antipadrão]
**Descrição**: [O que é feito errado]
**Impacto**: [Consequência mensurável]
**Solução**: [Otimização recomendada]
**Projetos afetados**: [Onde foi identificado]

<!-- ADICIONAR_ANTIPADRAO_PERF_AQUI -->

---

## DevOps

### [Nome do Antipadrão]
**Descrição**: [O que é feito errado]
**Consequência**: [O que pode dar errado]
**Prática correta**: [O que fazer em vez disso]

<!-- ADICIONAR_ANTIPADRAO_DEVOPS_AQUI -->

---

## Processo

### [Nome do Antipadrão]
**Descrição**: [O que é feito errado]
**Por que acontece**: [Causa raiz comum]
**Consequência**: [Impacto no projeto]
**Solução**: [Processo melhorado]

<!-- ADICIONAR_ANTIPADRAO_PROCESSO_AQUI -->

---

## Hall da Vergonha (Aprendizados Dolorosos)

| Data | Projeto | Erro Cometido | Impacto | Lição Aprendida |
|------|---------|---------------|---------|-----------------|
| 2026-01-08 | Conserto-PC | Desinstalar OneDrive antes de migrar dados | Pastas do Desktop sumiram, configurações perdidas | SEMPRE fazer backup/cópia completa antes de desinstalar cloud storage |
| 2026-01-08 | Conserto-PC | Executar tarefas longas em PC instável | Múltiplas interrupções por reinício, trabalho perdido | Dividir em etapas curtas, documentar progresso |
| 2026-01-20 | Sistema-Memoria | Contexto excessivo em Custom Instructions | Lentidão, tokens desperdiçados | CORE/ < 1500 chars, detalhes sob demanda |
| 2026-01-20 | Sistema-Memoria | Planejar API quando tinha assinatura | Custo desnecessário planejado | Sempre verificar se assinatura cobre o caso |
<!-- HALL_VERGONHA -->

---

## Checklist de Revisão Anti-Antipadrões

Antes de finalizar qualquer trabalho significativo, verificar:

- [ ] Sem secrets hardcoded ou em logs
- [ ] Sem queries N+1 ou loops com I/O
- [ ] Sem dependências circulares introduzidas
- [ ] Sem código duplicado significativo
- [ ] Sem tratamento silencioso de erros
- [ ] Sem dados sensíveis em URLs ou parâmetros GET
- [ ] Sem bloqueio de thread principal com operações síncronas
- [ ] Sem configurações de desenvolvimento em produção
