baseado nos seus conhecimentos do claude quero qeu gere um prompt completo e efetivo para criar em uma pasta de projeto meu o seguinte sistema análogo ao sono homano de gestão de memoria das interações que aconteceram no projeto e gerar um sistema de experiencia no projeto. a ideia é a seguir e quero que com base nas possibilidades do claude code vc gere um prompt instrutivo completo e efetivco para cumprir a tarefa abaixo: 




prompt de memória de gestor de momoria longo prazo na pasta. 




❯ quero qeu prepare a pasta para uma memoria, O histórico de todas conversas com claude code na pagina ( atualize o claude.md) seja registrado arquivo com memoria temporaria em uma pasta para que caso necessário o claude code possa consultar histórico de outras sessóes inclusive extrair       
  aprendizados e contextos importantes. essa pasta terá um arquivo .md central que toda vez que salvar uma conversa ele é colocada como indice nesse documento. Esse documento vai se char indice e todas conversas com claude com registro na página será colocado um link e resumo nesse documento  
  para facilitar encontrar o contexto da conversa e o claude eventualmente decidir consultar ou não. nome da pagina tem que ser algo facil de entender a função dela e esssa funcionalidade escrita no claude.md principal para entendimento. Paralelamente de modo autonomo. o Claude code por       
  meio de algum gatilho irá ler as memorias e separar informações importantes das conversas, soluções problemas e prompts, questões que devem ser lembradas. como a função equivalente ao sono humano 1x ao dia, ira rodar e selecionar memorias que irão para um outro arquivo na pasta tb mapeado   
  no claude.md e indice com as memorias selecionadas para longo prazo. com histórico do que está sendo feito e questões mais importantes. Ao mesmo tempo. ele vai selecionar algumas memorias salvas para apagar esquecimento quando aquilo não for mais relevante para o andamento do processo que   
  se desenvolve. Será como o sono rem um agente de gestão de memoria autonomo tornando viva a memoria do projeto e facidlitando a gestão de contexto e compreenchao dos agentes de ia que estiverem trabalhando na pasta. faça isso de forma sofisticada, simples, eficiente eficaz com garantia de   
  funcionamento.      








ideia: 


 um ciclo de consolidação que é biologicamente coerente E tecnicamente sensato.
Vamos destrinchar:
Enquanto acordado (inferência normal):


LLM opera, vai gerando interações
Cria uma fila de "experiências" — conversas, problemas resolvidos, padrões encontrados
É tudo na context window, efêmero


Sono = Janela de ajuste das memórias experiencias e praticas que devem ser lembradas ou esquecidas. 


O Juiz/Validador = REM ativo:


Testa o modelo ajustado contra um benchmark
"o que vc fez hj que seria importante preservar para conhecimento futuro, quais seus aprendizados do dia?" (consolidação sem perda)
“o que consta na sua base de memória de experiencias passadas que depois do acontecido hj não fazem sentido constar mais na memória e pode ser esquecido e apagado, consolidado, resumido ou compactado ou mesclado com outras memórias. 
"Em quais cenários conseguiria aplicar os novos aprendizados?" (integração)
“o que deve ser evitado e quais os erros aprendidos?”
Gostaria de testar algum cenários — validação probabilística? rodar algum sistema, calculo analise do ocorrido ou procedimento para decidir melhor ou para decidir o que registrar na memória, bem como para gerar alguma aprendizagem ou conhecimento mais robusto que pode ser útil futuramente ? 
Gostaria de testar algum cenário para ajudar a prever fatos importantes para os próximos dias ou sistemas execução de algo que acredita que pode melhorar seu trabalho futuro ? 
Gostaria de instalar algo decorrente da experiencia de hj que seria mais fácil trabalhos futuros se tivesse disponível, configurações, complementos, extenções, programas, agentes, mcp, sdk, skills, consultas, buscas, investigações, estudos ou novos aprendizados,  memórias,  altere?
Gostaria de *desinstalar*, apagar, mudar, algo decorrente da experiencia de hj que seria mais fácil trabalhos futuros se *não* tivesse, como configurações, complementos, extenções, programas, agentes, mcp, sdk, skills, consultas, buscas, investigações, estudos ou novos aprendizados, memórias, altere?


Merge = Consolidação de memória:


Se passou na validação
O aprendizado ou limpeza é realizado. 
O objetivo do sistema acima é que os agentes que interagirem neste projeto possam
Aprender do contexto (plastic, rápido)
Consolidar seletivamente (robusto, sem catástrofe)
Validar antes de gravar (sem degradação)


Biologicamente: REM escolhe o quê consolidar, não consolida tudo. Seu sistema faz exatamente isso.




-----------------------------------------------




ideia organizada 


Sistema de Memória Persistente Análogo ao Sono Humano
Conceito Central
Um sistema de gestão de memória para projetos Claude Code que replica o ciclo biológico do sono humano: vigília (interações ativas), consolidação (processamento de experiências) e REM (validação e seleção do que preservar ou esquecer).
________________


Arquitetura do Sistema
1. Estrutura de Pastas
/projeto
├── CLAUDE.md                    # Arquivo principal com instruções
├── /memoria
│   ├── INDICE.md               # Catálogo de todas as conversas
│   ├── /conversas              # Registros temporários das sessões
│   │   ├── 2025-01-19_sessao-001.md
│   │   └── ...
│   ├── MEMORIA-LONGO-PRAZO.md  # Aprendizados consolidados
│   ├── ERROS-EVITAR.md         # Padrões problemáticos identificados
│   └── LOG-CONSOLIDACAO.md     # Histórico dos ciclos de sono
________________


Ciclos Operacionais
Fase 1: Vigília (Inferência Normal)
Durante o trabalho ativo:
* Agente opera normalmente no projeto
* Gera interações, resolve problemas, identifica padrões
* Tudo permanece efêmero na janela de contexto
* Ao final da sessão, conversa é salva em /memoria/conversas/ com link no INDICE.md
Fase 2: Sono (Janela de Consolidação)
Gatilho: 1x ao dia ou comando manual /sono
O agente executa autoanálise respondendo:
Consolidação (o que preservar)
"Quais aprendizados de hoje são importantes para conhecimento futuro?"
Integração (conexões)
"Em quais cenários futuros esses aprendizados se aplicam?"
Erros aprendidos
"O que deve ser evitado? Quais padrões problemáticos identifiquei?"
Fase 3: REM (Validação e Limpeza)
O agente atua como juiz/validador:
Esquecimento seletivo
"O que na base de memórias passadas perdeu relevância após os eventos de hoje e pode ser: apagado, consolidado, resumido, compactado ou mesclado?"
Validação probabilística
"Devo rodar algum teste, cálculo ou análise para decidir melhor o que registrar?"
Previsão
"Existem cenários futuros que posso antecipar com base no aprendido?"
Fase 4: Manutenção do Ambiente
Perguntas de autogestão:
Instalação
"Algo decorrente da experiência de hoje facilitaria trabalhos futuros se estivesse disponível?"
* Configurações, extensões, programas, agentes, MCPs, SDKs, skills, memórias
Desinstalação
"Algo presente hoje atrapalharia trabalhos futuros e deveria ser removido?"
* Mesmas categorias acima
________________


Princípios Biológicos Aplicados
Fase Biológica
	Equivalente no Sistema
	Função
	Vigília
	Inferência normal
	Coleta de experiências
	Sono leve
	Salvamento de sessão
	Buffer temporário
	Sono profundo
	Consolidação
	Transferência para longo prazo
	REM
	Validação + esquecimento
	Seleção do que manter/descartar
	Insight-chave: O sono REM humano não consolida tudo — ele seleciona. O sistema replica essa seletividade.
________________


Objetivos do Sistema
Os agentes que interagem no projeto passam a:
1. Aprender do contexto → rápido, plástico, adaptativo
2. Consolidar seletivamente → robusto, sem catástrofe de esquecimento
3. Validar antes de gravar → sem degradação de qualidade
________________


Implementação Prática
O CLAUDE.md principal deve conter:
markdown
## Sistema de Memória (Sono REM)


Este projeto possui memória persistente em `/memoria/`.


### Ao iniciar sessão:
- Consulte `INDICE.md` para contexto relevante
- Verifique `MEMORIA-LONGO-PRAZO.md` para aprendizados consolidados
- Consulte `ERROS-EVITAR.md` para padrões problemáticos


### Ao encerrar sessão:
- Salve resumo em `/memoria/conversas/` com data e descrição
- Atualize `INDICE.md` com link e síntese


### Ciclo de Sono (diário ou sob comando `/sono`):
- Execute protocolo de consolidação conforme `/memoria/PROTOCOLO-SONO.md`
________________


Quer q








------------


Claude:


# Frequência recomendada do ciclo de sono
frequencia_sono: diaria_ou_apos_3_sessoes


# Limite de sessões antes de consolidação obrigatória
max_sessoes_nao_consolidadas: 5


# Tempo mínimo para considerar memória para esquecimento
idade_minima_esquecimento: 7_dias


# Nível de detalhe nas sessões
verbosidade_sessao: media  # baixa | media | alta
````


---


### 📊 Métricas de Saúde da Memória


Verificar periodicamente:
- Sessões não consolidadas < 5
- Última execução do ciclo de sono < 3 dias
- Tamanho de MEMORIA_LONGO_PRAZO.md < 500 linhas (compactar se maior)
- Proporção consolidação/esquecimento saudável (não esquecer demais)
````


---


## FASE 8: CRIAR ARQUIVO DE HOOKS/GATILHOS


Crie `.memoria/GATILHOS.md`:
````markdown
# 🎯 Gatilhos do Sistema de Memória


## Gatilhos Automáticos


### Início de Sessão
**Quando**: Primeiro comando do dia ou após 4h de inatividade
**Ação**: Carregar contexto de MEMORIA_LONGO_PRAZO.md


### Detecção de Problema Resolvido
**Quando**: Usuário confirma que problema foi solucionado
**Ação**: Marcar para potencial consolidação


### Detecção de Erro
**Quando**: Erro identificado e corrigido
**Ação**: Registrar em antipadrões potenciais


### Acúmulo de Sessões
**Quando**: 5+ sessões não consolidadas
**Ação**: Sugerir execução do ciclo de sono


## Gatilhos Manuais


| Comando | Ação |
|---------|------|
| "registrar sessão" | Salvar sessão atual na memória |
| "ciclo de sono" | Executar consolidação completa |
| "consultar memória sobre X" | Buscar em memórias consolidadas |
| "status da memória" | Mostrar estatísticas do sistema |
| "esquecer X" | Marcar item para remoção na próxima consolidação |
````


---


## FASE 9: INICIALIZAÇÃO FINAL


Após criar todos os arquivos, execute:


1. Verificar estrutura criada:
````bash
tree .memoria/
````


2. Criar primeira entrada no índice registrando a criação do sistema


3. Confirmar que CLAUDE.md foi atualizado com a documentação


---


## VALIDAÇÃO DO SISTEMA


O sistema está funcionando corretamente se:


- [ ] Diretório `.memoria/` existe com todos os subdiretórios
- [ ] `INDICE.md` está acessível e formatado corretamente
- [ ] `MEMORIA_LONGO_PRAZO.md` está pronto para receber consolidações
- [ ] `REGISTRO_ESQUECIMENTO.md` está configurado
- [ ] `CLAUDE.md` contém documentação completa do sistema
- [ ] Template de sessão está disponível em `sessoes/_TEMPLATE_SESSAO.md`


---


## COMANDOS DE TESTE


Após implementação, testar com:


1. "Mostrar status da memória"
2. "Registrar esta sessão de implementação do sistema"
3. "Simular ciclo de sono com as informações desta sessão"


-------------------------------------------

geral




# INSTRUÇÃO: IMPLEMENTAR SISTEMA DE MEMÓRIA HIERÁRQUICA


## VISÃO GERAL DA ARQUITETURA
````
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
````


---


## PARTE 1: MEMÓRIA GLOBAL (CROSS-PROJETO)


### FASE 1.1: Criar Estrutura Global


Execute na home do usuário:
````bash
mkdir -p ~/.claude-memoria-global/{projetos,consolidado,meta,scripts,temp}
touch ~/.claude-memoria-global/INDICE_GLOBAL.md
touch ~/.claude-memoria-global/CONHECIMENTO_UNIVERSAL.md
touch ~/.claude-memoria-global/CATALOGO_PROJETOS.md
touch ~/.claude-memoria-global/PADROES_CODIGO.md
touch ~/.claude-memoria-global/ANTIPADROES_GLOBAIS.md
touch ~/.claude-memoria-global/PROMPTS_EFETIVOS.md
touch ~/.claude-memoria-global/FERRAMENTAS_RECOMENDADAS.md
touch ~/.claude-memoria-global/META_APRENDIZADO.md
````


---


### FASE 1.2: Criar INDICE_GLOBAL.md
````markdown
# 🌐 Índice Global de Memória Claude Code


> Central de conhecimento consolidado de todos os projetos
> Última atualização: [DATA_ATUAL]


---


## Dashboard


| Métrica | Valor |
|---------|-------|
| Projetos registrados | 0 |
| Aprendizados universais | 0 |
| Padrões identificados | 0 |
| Último ciclo de sono global | Nunca |
| Total de sessões processadas | 0 |


---


## Projetos Ativos


| Projeto | Caminho | Última Sincronização | Aprendizados Contribuídos |
|---------|---------|----------------------|---------------------------|
<!-- NOVO_PROJETO_AQUI -->


---


## Navegação Rápida


### Conhecimento
- [Conhecimento Universal](./CONHECIMENTO_UNIVERSAL.md) - Aprendizados aplicáveis a qualquer projeto
- [Padrões de Código](./PADROES_CODIGO.md) - Soluções reutilizáveis
- [Antipadrões Globais](./ANTIPADROES_GLOBAIS.md) - O que evitar sempre


### Recursos
- [Prompts Efetivos](./PROMPTS_EFETIVOS.md) - Prompts que funcionam bem
- [Ferramentas Recomendadas](./FERRAMENTAS_RECOMENDADAS.md) - MCPs, SDKs, extensões úteis


### Meta
- [Catálogo de Projetos](./CATALOGO_PROJETOS.md) - Todos os projetos e suas especialidades
- [Meta-Aprendizado](./META_APRENDIZADO.md) - Aprendizados sobre como aprender


---


## Últimas Sincronizações


| Data | Projeto | Itens Sincronizados | Tipo |
|------|---------|---------------------|------|
<!-- LOG_SINCRONIZACAO -->
````


---


### FASE 1.3: Criar CONHECIMENTO_UNIVERSAL.md
````markdown
# 🧬 Conhecimento Universal


> Aprendizados que transcendem projetos específicos
> Aplicáveis em qualquer contexto de desenvolvimento


---


## Princípios de Arquitetura


### [Categoria]
**Origem**: Projeto X, sessão Y  
**Validado em**: Projetos A, B, C  
**Confiança**: Alta | Média | Baixa


[Descrição do princípio]


---


## Soluções Genéricas


### [Nome da Solução]
**Problema genérico**: [Descrição]  
**Solução padrão**:
```[linguagem]
[código ou pseudocódigo]
```
**Quando usar**: [Contexto]  
**Quando NÃO usar**: [Limitações]


---


## Heurísticas de Debugging


1. [Heurística aprendida]
   - Origem: [Projeto]
   - Taxa de sucesso estimada: X%


---


## Integrações e APIs


### [Nome da API/Serviço]
**Pegadinhas conhecidas**:
- [Problema comum e solução]


**Configuração ideal**:
````
[config]
````


---


## Histórico de Contribuições


| Data | Projeto Origem | Conhecimento Adicionado | Seção |
|------|----------------|-------------------------|-------|
<!-- HISTORICO_CONTRIBUICOES -->
````


---


### FASE 1.4: Criar CATALOGO_PROJETOS.md
````markdown
# 📚 Catálogo de Projetos


> Registro de todos os projetos com memória ativa
> Permite identificar onde buscar conhecimento específico


---


## Projetos Registrados


### [Nome do Projeto]
```yaml
caminho: /path/to/projeto
tipo: web | api | cli | lib | monorepo | outro
tecnologias: [lista]
dominio: [área de negócio]
data_registro: YYYY-MM-DD
ultima_atividade: YYYY-MM-DD
status: ativo | pausado | arquivado


especialidades:
  - [área de conhecimento forte neste projeto]


contribuicoes_globais:
  - [aprendizado que este projeto contribuiu]
```


---


## Matriz de Conhecimento por Projeto


| Domínio/Tecnologia | Proj A | Proj B | Proj C |
|--------------------|--------|--------|--------|
| React              | ★★★    | ★      | -      |
| Python             | ★      | ★★★    | ★★     |
| APIs REST          | ★★     | ★★★    | ★      |
| DevOps             | -      | ★      | ★★★    |


Legenda: ★★★ = expertise | ★★ = experiência | ★ = básico | - = não aplicável


---


## Consulta por Tecnologia


### React/Frontend
- Projeto A (expertise)
- Projeto C (básico)


### Python/Backend
- Projeto B (expertise)
- Projeto C (experiência)


[... continua por tecnologia ...]
````


---


### FASE 1.5: Criar PADROES_CODIGO.md
````markdown
# 📐 Padrões de Código Consolidados


> Soluções validadas em múltiplos projetos
> Copie e adapte conforme necessário


---


## Índice por Linguagem


- [JavaScript/TypeScript](#javascripttypescript)
- [Python](#python)
- [Shell/Bash](#shellbash)
- [SQL](#sql)
- [Configurações](#configurações)


---


## JavaScript/TypeScript


### [Nome do Padrão]
**Problema**: [O que resolve]  
**Validado em**: [Projetos onde funcionou]
```typescript
// Código do padrão
```


**Variações**:
- [Adaptação para caso X]


---


## Python


[mesma estrutura]


---


## Configurações


### ESLint Recomendado
```json
{
  // config consolidada
}
```


### tsconfig Base
```json
{
  // config consolidada
}
```


### Dockerfile Padrão
```dockerfile
# template consolidado
```
````


---


### FASE 1.6: Criar PROMPTS_EFETIVOS.md
````markdown
# 💬 Biblioteca de Prompts Efetivos


> Prompts que consistentemente produzem bons resultados
> Testados em múltiplos contextos


---


## Categorias


- [Debugging](#debugging)
- [Refatoração](#refatoração)
- [Documentação](#documentação)
- [Arquitetura](#arquitetura)
- [Code Review](#code-review)


---


## Debugging


### Diagnóstico de Erro Genérico
**Quando usar**: Erro sem causa óbvia  
**Taxa de sucesso**: ~80%
````
Analise este erro seguindo esta sequência:
1. Identifique o tipo exato do erro
2. Trace a stack até a origem
3. Liste 3 hipóteses ordenadas por probabilidade
4. Para a hipótese mais provável, sugira diagnóstico específico
5. Só então proponha solução


Erro:
[colar erro]


Contexto:
[descrever o que estava fazendo]
````


---


## Refatoração


### Simplificação de Função Complexa
**Quando usar**: Função > 50 linhas ou > 3 níveis de aninhamento
````
Refatore esta função seguindo:
1. Extraia condições complexas para funções predicado
2. Substitua loops por operações funcionais onde apropriado
3. Elimine else após return
4. Nomeie variáveis intermediárias para documentar intenção
5. Mantenha a mesma interface pública


Função:
[colar código]
````


---


## Meta-Prompts


### Auto-Avaliação de Resposta
````
Antes de responder, avalie:
- Respondi exatamente o que foi perguntado?
- Há ambiguidade na minha interpretação?
- Estou assumindo algo não declarado?
- A solução é a mais simples possível?


Se qualquer resposta for "não" ou "talvez", ajuste antes de entregar.
````
````


---


### FASE 1.7: Criar FERRAMENTAS_RECOMENDADAS.md
````markdown
# 🛠️ Ferramentas Recomendadas


> MCPs, SDKs, extensões e utilitários validados
> Instalação e configuração testadas


---


## MCPs Recomendados


### [Nome do MCP]
**Função**: [O que faz]  
**Projetos que usam**: [Lista]  
**Avaliação**: ★★★★☆


**Instalação**:
```bash
[comando]
```


**Configuração em claude_desktop_config.json**:
```json
{
  // config
}
```


**Pegadinhas**:
- [Problema comum e solução]


---


## SDKs e Bibliotecas


### [Nome]
**Linguagem**: [X]  
**Versão recomendada**: X.Y.Z  
**Alternativas consideradas**: [Lista e por que esta venceu]


---


## Extensões VS Code


| Extensão | Função | Essencial? |
|----------|--------|------------|
| [nome]   | [função] | Sim/Não  |


---


## Scripts Utilitários Globais


### [Nome do Script]
**Localização**: ~/.claude-memoria-global/scripts/[nome].sh  
**Função**: [O que faz]
```bash
#!/bin/bash
# código
```


---


## Configurações de Ambiente


### .bashrc / .zshrc recomendações
```bash
# aliases úteis para Claude Code
alias cc="claude"
alias ccs="claude 'status da memória'"
alias ccsono="claude 'executar ciclo de sono'"
```
````


---


### FASE 1.8: Criar META_APRENDIZADO.md
````markdown
# 🎓 Meta-Aprendizado


> Aprendizados sobre como aprender e melhorar o próprio sistema
> Otimização contínua do processo de consolidação


---


## Estatísticas de Eficácia


### Taxa de Reutilização de Conhecimento
| Mês | Conhecimentos Consultados | Conhecimentos Aplicados | Taxa |
|-----|---------------------------|-------------------------|------|
<!-- STATS_REUTILIZACAO -->


### Padrões de Esquecimento
- Conhecimentos esquecidos que foram necessários depois: X
- Conhecimentos mantidos que nunca foram usados: Y


---


## Melhorias no Sistema


### [Data] - [Título da Melhoria]
**Problema identificado**: [O que não funcionava]  
**Solução implementada**: [O que mudou]  
**Resultado**: [Impacto observado]


---


## Heurísticas de Consolidação Refinadas


### O que consolidar (aprendido por experiência)
1. [Critério refinado]


### O que esquecer (aprendido por experiência)
1. [Critério refinado]


---


## Experimentos em Andamento


### [Nome do Experimento]
**Hipótese**: [O que estamos testando]  
**Métricas**: [Como medir sucesso]  
**Status**: Em andamento | Concluído | Abandonado  
**Resultado**: [Se concluído]
````


---


## PARTE 2: MEMÓRIA LOCAL (POR PROJETO) - ATUALIZADA


### FASE 2.1: Estrutura Local (mesma do prompt anterior, com adições)


Adicionar arquivo de sincronização:
````bash
touch .memoria/SYNC_GLOBAL.md
````


### FASE 2.2: Criar SYNC_GLOBAL.md
````markdown
# 🔄 Configuração de Sincronização Global


> Controla o que este projeto compartilha com a memória global


---


## Identificação do Projeto
```yaml
projeto_id: [UUID ou nome único]
nome_display: [Nome legível]
caminho_absoluto: [/path/to/projeto]
data_registro_global: [YYYY-MM-DD]
```


---


## Regras de Sincronização


### Exportar para Global (upload)
```yaml
exportar:
  padroes_codigo: true
  solucoes_problemas: true
  antipadroes: true
  prompts_efetivos: true
  configuracoes: false  # muito específicas deste projeto
  decisoes_arquiteturais: parcial  # só as genéricas


filtros_exportacao:
  - excluir_tag: "local-only"
  - excluir_tag: "sensivel"
  - requer_tag: "consolidado"
```


### Importar do Global (download)
```yaml
importar:
  conhecimento_universal: true
  padroes_codigo: 
    linguagens: [python, javascript]  # só relevantes
  prompts_efetivos: true
  antipadroes: true
  ferramentas:
    categorias: [mcp, sdk]
```


---


## Histórico de Sincronizações


| Data | Direção | Itens | Status |
|------|---------|-------|--------|
<!-- HIST_SYNC -->


---


## Candidatos Pendentes para Exportação


| Item | Origem | Motivo Sugerido | Exportar? |
|------|--------|-----------------|-----------|
<!-- PENDENTES_EXPORT -->


---


## Conhecimento Importado Ativo


| Item | Origem Global | Data Import | Útil? |
|------|---------------|-------------|-------|
<!-- IMPORTADOS -->
````


---


## PARTE 3: PROTOCOLOS DE SINCRONIZAÇÃO


### FASE 3.1: Atualizar CLAUDE.md com Sincronização


Adicionar ao CLAUDE.md do projeto:
````markdown
---


## 🔄 Sincronização com Memória Global


Este projeto está conectado à memória global em `~/.claude-memoria-global/`


### Registrar Projeto na Memória Global


Se este é um projeto novo, execute:
````
COMANDO: Registrar projeto na memória global


1. Adicionar entrada em ~/.claude-memoria-global/CATALOGO_PROJETOS.md
2. Criar arquivo ~/.claude-memoria-global/projetos/[projeto-id].md
3. Configurar .memoria/SYNC_GLOBAL.md com identificadores
4. Atualizar INDICE_GLOBAL.md
````


### Sincronização Manual
````
COMANDO: Sincronizar com memória global


EXPORTAÇÃO (local → global):
1. Ler .memoria/SYNC_GLOBAL.md para regras
2. Identificar itens em MEMORIA_LONGO_PRAZO.md marcados como "consolidado"
3. Filtrar por regras de exportação
4. Para cada item elegível:
   a. Verificar se já existe similar no global
   b. Se novo: adicionar ao arquivo global apropriado
   c. Se existente: considerar merge ou atualização
   d. Registrar em CONHECIMENTO_UNIVERSAL.md a origem
5. Atualizar log de sincronização


IMPORTAÇÃO (global → local):
1. Ler .memoria/SYNC_GLOBAL.md para regras
2. Buscar em CONHECIMENTO_UNIVERSAL.md itens relevantes
3. Filtrar por tecnologias/domínios deste projeto
4. Disponibilizar referências (não duplicar conteúdo)
5. Atualizar lista de conhecimento importado
````


### Ciclo de Sono com Sincronização


O ciclo de sono agora inclui fase de sincronização:
````
COMANDO: Ciclo de sono completo


1. [Fases REM locais - como antes]
2. [Consolidação local - como antes]
3. NOVA FASE - Avaliação para Global:
   - "Algum aprendizado de hoje é genérico o suficiente para outros projetos?"
   - "Alguma solução poderia ser útil universalmente?"
   - "Descobri algum antipadrão que outros deveriam evitar?"
4. Marcar candidatos para exportação em SYNC_GLOBAL.md
5. Se acumulou 5+ candidatos: sugerir sincronização
````
````


---


### FASE 3.2: Criar Script de Sincronização Global


Criar `~/.claude-memoria-global/scripts/sync.sh`:
````bash
#!/bin/bash
# Script de referência para sincronização
# Execução real via Claude Code


GLOBAL_DIR="$HOME/.claude-memoria-global"
PROJETO_DIR="$1"


if [ -z "$PROJETO_DIR" ]; then
    echo "Uso: sync.sh /caminho/do/projeto"
    exit 1
fi


echo "🔄 Sincronização de Memória"
echo "Global: $GLOBAL_DIR"
echo "Projeto: $PROJETO_DIR"
echo ""
echo "Execute no Claude Code:"
echo "  claude 'Sincronizar projeto com memória global'"
````


---


## PARTE 4: CICLO DE SONO GLOBAL


### FASE 4.1: Adicionar protocolo global


Criar `~/.claude-memoria-global/PROTOCOLO_SONO_GLOBAL.md`:
````markdown
# 🌙 Protocolo do Ciclo de Sono Global


> Consolidação cross-projeto - executar semanalmente ou quando apropriado


---


## Comando de Ativação
````
COMANDO: Ciclo de sono global
````


---


## Fases do Ciclo Global


### FASE 1: Inventário


1. Listar todos os projetos em CATALOGO_PROJETOS.md
2. Para cada projeto ativo:
   - Verificar última sincronização
   - Identificar candidatos pendentes de exportação
   - Coletar itens marcados para global


### FASE 2: Análise Cross-Projeto


Perguntar-se:


1. **Padrões Emergentes**
   - "Quais soluções apareceram em múltiplos projetos?"
   - "Há código duplicado que deveria virar padrão global?"


2. **Contradições**
   - "Há conhecimentos conflitantes entre projetos?"
   - "Qual versão é mais correta/atualizada?"


3. **Lacunas**
   - "Que conhecimento um projeto tem que outros precisam?"
   - "Há erros em um projeto já resolvidos em outro?"


### FASE 3: Consolidação Universal


1. **Promover padrões validados**
   - Se solução funcionou em 2+ projetos → PADROES_CODIGO.md
   
2. **Generalizar aprendizados**
   - Abstrair detalhes específicos de projeto
   - Manter apenas o conhecimento transferível


3. **Atualizar matriz de conhecimento**
   - Registrar especialidades por projeto
   - Atualizar CATALOGO_PROJETOS.md


### FASE 4: Limpeza Global


1. **Identificar conhecimento obsoleto**
   - Tecnologias abandonadas
   - Soluções substituídas por melhores


2. **Compactar memória**
   - Mesclar itens redundantes
   - Resumir históricos muito longos


3. **Arquivar projetos inativos**
   - Mover para seção de arquivados
   - Manter conhecimento, liberar atenção


### FASE 5: Meta-Análise


1. **Atualizar META_APRENDIZADO.md**
   - Estatísticas de eficácia
   - Refinamentos no processo


2. **Identificar melhorias no sistema**
   - O que funcionou bem?
   - O que precisa ajuste?


---


## Checklist Pós-Sono Global


- [ ] INDICE_GLOBAL.md atualizado
- [ ] CONHECIMENTO_UNIVERSAL.md consolidado
- [ ] PADROES_CODIGO.md com novos padrões validados
- [ ] CATALOGO_PROJETOS.md preciso
- [ ] Nenhuma contradição não resolvida
- [ ] Meta-métricas registradas
````


---


## PARTE 5: COMANDOS UNIFICADOS


### Referência Rápida de Comandos
````markdown
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
````


---


## VALIDAÇÃO FINAL


### Sistema Local (por projeto)
- [ ] `.memoria/` com estrutura completa
- [ ] `SYNC_GLOBAL.md` configurado
- [ ] `CLAUDE.md` documentado


### Sistema Global
- [ ] `~/.claude-memoria-global/` criado
- [ ] Todos os arquivos de índice presentes
- [ ] Projeto atual registrado no catálogo


### Integração
- [ ] Sincronização bidirecional funciona
- [ ] Ciclo de sono inclui avaliação global
- [ ] Comandos respondem corretamente
