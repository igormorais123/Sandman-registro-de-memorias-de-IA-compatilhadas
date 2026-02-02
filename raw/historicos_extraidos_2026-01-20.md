# Historicos Extraidos dos Projetos Claude Code
**Data de Extracao**: 2026-01-20
**Fonte**: Arquivos JSONL de sessoes do Claude Code

---

## 1. PROJETO C--Agentes (Sistema Eleitoral DF)

### 1.1 Problemas Encontrados e Solucoes

#### Migracao de Banco de Dados (400 para 1000 amostras)
- **Problema**: Inconsistencia de dados ao escalar de 400 para 1000 amostras de eleitores
- **Solucao**: Atualizacao sistematica de coerencia dos dados, validacao estatistica completa
- **Aprendizado**: Sempre validar coerencia estatistica ao escalar datasets
- **Tags**: #database #migracao #validacao #consolidado

#### Coerencia de Personagens com Dados Demograficos
- **Problema**: Historias de personagens nao correspondiam aos dados demograficos
- **Solucao**: Implementar validacao cruzada entre dados demograficos e narrativas
- **Aprendizado**: Dados sinteticos precisam de validacao de coerencia interna
- **Tags**: #dados-sinteticos #validacao #consolidado

#### Bugs na Pagina de Validacao
- **Problema**: Tooltips nao funcionavam, mapeamento de dados incorreto
- **Solucao**: Correcoes de mapeamento (moto/motocicleta, centro-direita/centro_direita)
- **Aprendizado**: Normalizar valores de campos antes de comparacoes
- **Tags**: #frontend #mapeamento #bugs #consolidado

#### Terminal Travado / Crash Recovery
- **Problema**: Terminal travava durante trabalho intensivo no simulador eleitoral
- **Solucao**: Implementar recuperacao de estado e checkpoints
- **Aprendizado**: Sessoes longas precisam de mecanismos de recuperacao
- **Tags**: #estabilidade #recuperacao #consolidado

#### Seguranca de API Keys
- **Problema**: Chaves de API expostas no codigo
- **Solucao**: Redacao de chaves, atualizacao de .gitignore, linting
- **Aprendizado**: Sempre usar variaveis de ambiente para secrets
- **Tags**: #seguranca #api-keys #boas-praticas #consolidado

#### Progress Calculation Bug
- **Problema**: Progresso de entrevistas mostrando mais de 201%
- **Solucao**: Corrigir calculo de progresso no sistema de entrevistas
- **Aprendizado**: Validar limites de valores calculados (0-100%)
- **Tags**: #bug #calculo #validacao #consolidado

### 1.2 Decisoes Arquiteturais

1. **Migracao JSON para PostgreSQL**: Decisao de migrar dados de eleitores de JSON para PostgreSQL para melhor escalabilidade
2. **Sistema de Validacao Estatistica**: Implementacao de metricas academicas para validar representatividade dos dados
3. **Arquitetura de Simulacao Eleitoral**: Uso de Claude API para simulacao de agentes cognitivos
4. **Sistema de Filtros Dinamicos**: Dashboard com filtros de grupos de eleitores em tempo real

### 1.3 Padroes que Funcionaram

- Uso de subagentes para tarefas paralelas
- Validacao estatistica continua durante geracao de dados
- Mapeamento explicito de valores entre frontend e backend
- Commits automaticos com sync do GitHub

---

## 2. PROJETO C--Users-IgorPC (Geral/PC)

### 2.1 Problemas de Hardware/Sistema

#### Configuracao de Monitor HP VGA
- **Problema**: Monitor VGA nao configurando corretamente
- **Solucao**: Ajustes de resolucao e DPI
- **Tags**: #hardware #monitor #windows #consolidado

#### Problemas de Internet/WiFi
- **Problema**: Quedas de conexao durante uploads pesados no Google Drive
- **Solucao**: Atualizacao de driver WiFi resolveu latencia
- **Aprendizado**: Drivers desatualizados causam instabilidade de rede
- **Tags**: #wifi #drivers #rede #consolidado

#### PC Reiniciando Sozinho
- **Problema**: Computador reiniciando durante execucao de tarefas do Claude Code
- **Solucao**: Diagnostico de estabilidade do sistema, verificacao de recursos
- **Tags**: #estabilidade #hardware #diagnostico

#### GPU e Compatibilidade de Hardware
- **Problema**: Conflitos de configuracao de GPU
- **Solucao**: Diagnostico de compatibilidade e resolucao de conflitos
- **Tags**: #gpu #hardware #compatibilidade

#### Espaco em Disco
- **Problema**: Disco cheio durante processamento RAG de documentos
- **Solucao**: Limpeza de disco e gerenciamento de espaco
- **Aprendizado**: Monitorar espaco antes de operacoes intensivas
- **Tags**: #disco #espaco #monitoramento #consolidado

### 2.2 Projetos de Desenvolvimento

#### Sistema de Memoria Hierarquica
- Implementacao completa de sistema de memoria persistente para Claude Code
- Recuperacao de historico de sessoes antigas
- Integracao com GitHub para sincronizacao
- **Aprendizado**: Memoria contextual melhora significativamente a continuidade
- **Tags**: #memoria #sistema #arquitetura #consolidado

#### Processamento RAG de Documentos
- Pipeline de processamento de documentos para casos juridicos
- Extracao, organizacao e tokenizacao de documentos
- **Aprendizado**: RAG tem limitacoes, considerar gerenciamento de contexto dinamico
- **Tags**: #rag #documentos #ia #consolidado

#### Skill de Investigacao Legal
- Desenvolvimento de skill com gerenciamento de contexto dinamico
- Analise de conversas WhatsApp para casos juridicos
- **Tags**: #skill #legal #investigacao

### 2.3 Configuracoes

#### MCP Filesystem Server
- Configuracao de caminhos para C:\Agentes
- **Tags**: #mcp #configuracao

#### Docker e GitHub
- Integracao VS Code com Docker e GitHub
- **Tags**: #docker #github #devops

#### Google Drive Migration
- Migracao de OneDrive para Google Drive
- Resolucao de erros de acesso ao Desktop
- **Tags**: #cloud #migracao #google-drive

---

## 3. PROJETO participa-df-ouvidoria

### 3.1 Contexto
- Sistema de analise de demandas de ouvidoria do DF
- Integracao com plataforma Participa DF

### 3.2 Trabalho Identificado
- Processamento de demandas
- Dashboard de analise
- **Tags**: #ouvidoria #governo #dashboard

---

## 4. APRENDIZADOS CONSOLIDADOS CROSS-PROJETO

### 4.1 Padrao de Erros Recorrentes

1. **Mapeamento de Dados Inconsistente**
   - Valores com formatos diferentes entre frontend/backend
   - Solucao: Normalizar valores, usar enums ou constantes compartilhadas

2. **Espaco em Disco Insuficiente**
   - Operacoes falham silenciosamente quando disco esta cheio
   - Solucao: Verificar espaco antes de operacoes pesadas

3. **Drivers Desatualizados**
   - Causam instabilidade de rede e hardware
   - Solucao: Manter drivers atualizados, especialmente WiFi e GPU

4. **API Keys Expostas**
   - Risco de seguranca em commits
   - Solucao: .gitignore + variaveis de ambiente

5. **Validacao de Limites**
   - Calculos sem validacao de limites (ex: progresso > 100%)
   - Solucao: Sempre clampar valores calculados

### 4.2 Solucoes que Funcionaram Bem

1. **Validacao Estatistica Continua**: Para dados sinteticos, validar metricas durante geracao
2. **Subagentes Paralelos**: Usar Task tool para operacoes independentes
3. **Checkpoints de Estado**: Salvar estado para recuperacao de crashes
4. **Memoria Hierarquica**: Sistema de contexto persistente entre sessoes
5. **Sincronizacao com GitHub**: Manter codigo sempre atualizado remotamente

### 4.3 Decisoes Arquiteturais Importantes

1. **PostgreSQL vs JSON**: Migrar para banco relacional para dados que vao escalar
2. **RAG vs Contexto Dinamico**: Para documentos grandes, considerar gerenciamento inteligente de contexto
3. **Skills Customizadas**: Encapsular logica repetitiva em skills reutilizaveis
4. **Sistema de Memoria**: Manter historico estruturado de decisoes e aprendizados

---

## 5. ANTIPADROES IDENTIFICADOS

1. **Nao validar coerencia de dados sinteticos** - Gera inconsistencias dificeis de debugar
2. **Commits sem verificar secrets** - Risco de exposicao de credenciais
3. **Ignorar warnings de espaco em disco** - Causa falhas em cascata
4. **Sessoes longas sem checkpoints** - Perde todo o trabalho em crashes
5. **Mapeamentos implicitos frontend/backend** - Causa bugs sutis de dados

---

## 6. FERRAMENTAS E TECNOLOGIAS UTILIZADAS

### Frontend
- React + TypeScript
- Tailwind CSS
- Tooltips customizados

### Backend
- Python (linting com ruff/black)
- Node.js
- PostgreSQL (migracao de JSON)
- Claude API

### DevOps
- Docker
- GitHub (sync automatico)
- Windows 11

### Claude Code
- Subagentes para tarefas paralelas
- Sistema de memoria hierarquica
- Skills customizadas

---

## 7. METRICAS DE SESSAO

- **Total de projetos analisados**: 4
- **Total de arquivos JSONL identificados**: 100+
- **Principais temas**:
  - Sistema eleitoral simulado com IA
  - Manutencao e configuracao de PC
  - Sistema de memoria para IA
  - Ouvidoria do governo DF
- **Periodo aproximado**: Janeiro 2026

---

*Arquivo gerado automaticamente pelo sistema de memoria hierarquica*
*Requer validacao humana antes de consolidacao permanente*
