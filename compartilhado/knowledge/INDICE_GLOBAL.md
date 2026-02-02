# Índice Global de Memória - Sistema ONIR

> Central de conhecimento consolidado de todos os projetos
> Mantido por: **ONIR** - O escriba que sonha
> Última atualização: 2026-01-20

---

## Dashboard

| Métrica | Valor |
|---------|-------|
| Projetos registrados | 7 |
| Aprendizados universais | 8 |
| Padrões identificados | 6 |
| Antipadrões documentados | 5 |
| Decisões arquiteturais (ADRs) | 6 |
| Último ciclo de sono global | 2026-01-20 |
| Total de sessões processadas | ~120 |
| Memórias ChatGPT importadas | 35 |
| Scripts de ingestão | 2 (Python) |
| Scripts de automação | 4 (bat/ps1) |
| Arquivos CORE (< 1500 chars) | 3 |
| Task Scheduler | ConsolidacaoMemoriaClaudeCode (Ativo) |
| Google Drive Sync | G:\Meu Drive\memoria-ia-unificada |

---

## Identidade do Sistema

| Atributo | Valor |
|----------|-------|
| Nome | **ONIR** |
| Significado | Derivado de "onírico" (relativo a sonhos) |
| Função | Consolidador único de memórias Multi-IA |
| Batismo | 2026-01-20 por Igor Morais |
| Arquivos | `IDENTIDADE.md`, `BATISMO_ONIR.md` |

---

## Projetos Ativos

| Projeto | Caminho | Última Sincronização | Aprendizados Contribuídos |
|---------|---------|----------------------|---------------------------|
| Doutorado-Agentes | ~/.claude/projects/Doutorado-... | 2026-01-19 | 2 |
| Conserto-PC | ~/.claude/projects/Conserto-PC | 2026-01-19 | 4 |
| Participa-DF-Ouvidoria | ~/participa-df-ouvidoria | 2026-01-19 | 2 |
| C--Agentes | ~/.claude/projects/C--Agentes | 2026-01-19 | 0 |
| App-Aula-Claude-Code | ~/.claude/projects/app-aula-... | 2026-01-19 | 1 |
| SIEC-v2 | ~/Downloads/SIEC-v2-OPUS45 | 2026-01-19 | 1 |
| Sistema-Memoria | ~/.claude-memoria-global | 2026-01-19 | 3 |
<!-- NOVO_PROJETO_AQUI -->

---

## Navegação Rápida

### Conhecimento
- [Conhecimento Universal](./CONHECIMENTO_UNIVERSAL.md) - Aprendizados aplicáveis a qualquer projeto
- [Padrões de Código](./PADROES_CODIGO.md) - Soluções reutilizáveis
- [Antipadrões Globais](./ANTIPADROES_GLOBAIS.md) - O que evitar sempre
- [Decisões Arquiteturais](./DECISOES_ARQUITETURAIS.md) - ADRs do sistema

### Recursos
- [Prompts Efetivos](./PROMPTS_EFETIVOS.md) - Prompts que funcionam bem
- [Prompts para Outras IAs](./PROMPTS_OUTRAS_IAS.md) - Configuração Gemini/ChatGPT/Claude Web
- [Ferramentas Recomendadas](./FERRAMENTAS_RECOMENDADAS.md) - MCPs, SDKs, extensões úteis

### Meta
- [Catálogo de Projetos](./CATALOGO_PROJETOS.md) - Todos os projetos e suas especialidades
- [Meta-Aprendizado](./META_APRENDIZADO.md) - Aprendizados sobre como aprender
- [Perfil do Usuário](./meta/PERFIL_IGOR.md) - Preferências e contexto pessoal
- [Sistema PC](./meta/SISTEMA_PC_IGOR.md) - Especificações técnicas do computador

### CORE (Para outras IAs - < 1500 chars cada)
- [CORE/PERFIL.md](./CORE/PERFIL.md) - Identidade resumida (565 chars)
- [CORE/INSTRUCOES.md](./CORE/INSTRUCOES.md) - Regras universais (741 chars)
- [CORE/CONTEXTO_ATIVO.md](./CORE/CONTEXTO_ATIVO.md) - Estado atual (654 chars)

### Documentação do Sistema
- [Guia de Consulta](./GUIA_CONSULTA.md) - **Como e quando consultar memória**
- [Protocolo de Sono Global](./PROTOCOLO_SONO_GLOBAL.md) - Ciclo de consolidação
- [CLAUDE.md Global](./CLAUDE.md) - Instruções do sistema

### Scripts de Automação
- `scripts/consolidar.bat` - Consolidação automática
- `scripts/hook_contador.ps1` - Trigger a cada 10 sessões
- `scripts/sync-google-drive.ps1` - Sincronização com Drive
- `scripts/registrar-tarefa.bat` - Registrar no Task Scheduler

---

## Últimas Sincronizações

| Data | Projeto | Itens Sincronizados | Tipo |
|------|---------|---------------------|------|
| 2026-01-19 | Conserto-PC | 4 heurísticas, 2 antipadrões | Ciclo de Sono Global |
| 2026-01-19 | Doutorado-Agentes | 2 especialidades | Registro |
| 2026-01-19 | Participa-DF | 2 padrões acessibilidade | Registro |
| 2026-01-19 | SIEC-v2 | 1 integração (clasp) | Registro |
| 2026-01-19 | Sistema Memória | Estrutura completa | Criação |
| 2026-01-20 | Sistema-Memoria | Consolidação Desktop+GitHub, 6 ADRs, 3 padrões, 3 antipadrões | Consolidação |
<!-- LOG_SINCRONIZACAO -->

---

## Comandos de Memória - Referência Rápida

### Nível Projeto (executar no diretório do projeto)

| Comando | Função |
|---------|--------|
| "registrar sessão" | Salva sessão atual em .memoria/sessoes/ |
| "ciclo de sono" | Consolidação local + avalia para global |
| "consultar memória sobre X" | Busca local primeiro, depois global |
| "status da memória" | Estatísticas do sistema local |
| "sincronizar com global" | Exporta/importa conhecimento |

### Nível Global (executar de qualquer lugar)

| Comando | Função |
|---------|--------|
| "status memória global" | Estatísticas cross-projeto |
| "ciclo de sono global" | Consolidação de todos os projetos |
| "buscar conhecimento global sobre X" | Busca em todos os projetos |
| "listar projetos registrados" | Mostra catálogo |
| "qual projeto sabe sobre X?" | Identifica fonte de conhecimento |
