# Sonho Profundo — Projeto Agentes (INTEIA) — 2026-02-02

> ONIR — Sonho Profundo (5 iteracoes)
> Tema: C:\Agentes — o maior projeto ativo de Igor

---

## Fontes consultadas

- Exploração completa do filesystem (C:\Agentes\)
- CLAUDE.md do projeto (570 linhas)
- .memoria/ (CONTEXTO_ATIVO, APRENDIZADOS, MEMORIA_LONGO_PRAZO)
- Estrutura completa: 52 paginas frontend, 94 modulos backend, 21 servicos
- banco-eleitores-df.json (1000+ eleitores, 60+ atributos cada)
- docker-compose.yml, requirements.txt, package.json
- 10 ultimos commits git
- DIAGNOSTICO.md, PROJECT_INDEX.md, GPS_NAVEGACAO_AGENTES.md
- 24 skills em .claude/skills/
- Sonho anterior sobre Igor (contexto cruzado)

---

## Iteracao 1: O que e o projeto — fatos puros

**Nome**: INTEIA — Instituto de Treinamento e Estudos em Inteligencia Artificial
**CNPJ**: 63.918.490/0001-20
**Dominio**: inteia.com.br
**Endereco**: SHN Quadra 2 Bloco F, Sala 625/626 — Brasilia/DF

Isso nao e so um projeto academico. E uma empresa registrada. Igor
formalizou o INTEIA como pessoa juridica. Isso muda completamente a
leitura do projeto.

**Stack**:
- Frontend: Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui + Zustand + React Query + Recharts + Plotly.js
- Backend: FastAPI + SQLAlchemy 2.0 + Pydantic + PostgreSQL 15
- IA: Claude API (Opus 4.5 para complexo, Sonnet para padrao)
- Auth: JWT + bcrypt
- Deploy: Vercel (front) + Render (back)

**Escala**:
- 1000+ eleitores sinteticos com 60+ atributos cada
- 18+ endpoints REST
- 21 servicos backend
- 52 paginas frontend
- 24 skills de IA
- Sistema cognitivo de 4 etapas para cada resposta de eleitor

**Estado**: Funcional. Build passa. Dev server roda. Deploy ativo.
Ultimos commits: debug de conexao SSL com PostgreSQL no Render.

---

## Iteracao 2: O que o projeto faz — a mecanica

### O fluxo central

1. **Eleitores sinteticos** carregados de JSON (1000+ perfis)
   Cada eleitor tem: nome, idade, genero, raca, regiao administrativa,
   cluster socioeconomico, escolaridade, profissao, renda, religiao,
   orientacao politica, posicao sobre Bolsonaro, interesse politico,
   valores, preocupacoes, vieses cognitivos, medos, fontes de informacao,
   susceptibilidade a desinformacao, historia resumida, instrucao comportamental.

2. **Pesquisas criadas** com perguntas customizadas
   5 tipos: escala, multipla escolha, sim/nao, aberta, ranking

3. **Entrevistas executadas** via Claude API
   Cada eleitor processa cada pergunta em **4 etapas cognitivas**:
   - Filtro de atencao: "Prestaria atencao nesta pergunta?"
   - Vies de confirmacao: "Confirma ou ameaca minhas crencas?"
   - Reacao emocional: "Como me sinto sobre isso?"
   - Decisao: "Qual minha resposta genuina?"

4. **Resultados agregados** em dashboard
   Graficos, correlacoes, mapa de calor por RA do DF, nuvem de palavras,
   insights gerados por IA, exportacao em Excel/PDF/CSV

### Os modulos alem do core

- **Candidatos**: CRUD de candidatos DF 2026 (governador, senador, deputados)
- **Cenarios**: Simulador de cenarios eleitorais (votacao simulada)
- **Parlamentares**: Deputados federais/distritais, senadores, com dados abertos
- **Mensagens**: Gerador de mensagens persuasivas com 5 gatilhos psicologicos
  (medo, esperanca, economico, tribal, identitario)
- **Memorias**: Persistencia de conversas entre sessoes de entrevista
- **Geracao**: Criacao de novos eleitores via IA

### Helena Montenegro

O sistema tem uma persona de IA chamada Helena Montenegro — "Agente de
Sistemas de IA Avancados, Cientista Politica". Helena e a voz publica
da analise. Aparece nos relatorios como a analista que interpreta os
dados. Igor criou uma persona profissional para dar credibilidade
institucional as analises de IA.

---

## Iteracao 3: O que o projeto revela sobre Igor

### INTEIA = a tese materializada

No sonho anterior, identifiquei que Igor "constroi para entender".
O INTEIA e a prova mais contundente. Sua pergunta de pesquisa do
doutorado e:

> "Como diferentes modelos argumentativos de persuasao afetam a
> adesao ao uso de inteligencia artificial?"

E o INTEIA FAZ EXATAMENTE ISSO:
- Modela eleitores com vieses cognitivos e susceptibilidade a persuasao
- Testa diferentes abordagens de mensagem
- Mede eficacia e risco de "backfire"
- Gera insights preditivos

O doutorado e o INTEIA nao sao projetos separados. Sao o MESMO projeto
em duas camadas: academica (doutorado) e comercial (INTEIA empresa).
Igor monetizou a pesquisa. Ou pesquisou o negocio. As duas leituras
sao validas.

### A escala de ambicao vs. a escala de execucao

O projeto e impressionante em escopo:
- 24 skills documentadas
- 6 fases planejadas (PLANOS/)
- Sistema de gestao de contexto com "zona burra" (>60%)
- GPS de navegacao para agentes de IA
- Identidade visual completa com design system
- Templates de relatorio nivel consultoria

Mas os ultimos 10 commits sao todos debug de conexao com banco de dados:
```
fix(db): trocar asyncpg → psycopg3
fix(db): usar URL interna do Render (sem SSL)
debug: testa múltiplas configs SSL
fix(db): usar ssl='require' para asyncpg
```

Isso confirma o padrao do sonho anterior: a arquitetura esta grandiosa,
a execucao trava em detalhes de infraestrutura. Nao e critica — e
observacao. O sistema cognitivo de 4 etapas esta pronto. O deploy
trava em SSL do PostgreSQL.

[Inferencia] Isso e consistente com TEA: a construcao do modelo
(sistema cognitivo, eleitores, skills) e hiperfoco produtivo. A
manutencao de infraestrutura (SSL, deploy, auth) e tarefa operacional
que nao ativa hiperfoco e portanto arrasta.

### O modulo de mensagens persuasivas

Este modulo merece atencao especial. Gera mensagens com 5 gatilhos:
medo, esperanca, economico, tribal, identitario. Inclui estimativa
de eficacia e risco de backfire.

Igor esta literalmente construindo a ferramenta que sua tese estuda.
O pesquisador de persuasao construiu uma maquina de persuasao. As
implicacoes eticas sao reais — e Igor parece ciente, dado que o
sistema inclui analise de risco de backfire e validacao estatistica
obrigatoria.

Mas observo: a diretriz do CLAUDE.md diz "Nunca mencionar nomes de
candidatos adversarios — usar caracteristicas genericas". Isso
sugere que o INTEIA tem (ou tera) clientes reais que sao candidatos.
A pesquisa nao e so academica.

### Helena Montenegro como estrategia

Criar uma persona de IA como "voz da analise" e uma decisao de
branding, nao de tecnologia. Igor poderia assinar os relatorios
pessoalmente. Escolheu criar Helena — com avatar, titulo, e
credenciais. Isso serve para:

1. Separar o pesquisador (Igor) do produto (INTEIA)
2. Dar credibilidade institucional (parecer empresa, nao freelancer)
3. Escalar: Helena pode assinar infinitos relatorios simultaneamente
4. Proteger: se uma analise errar, Helena errou, nao Igor

[Inferencia] Helena e uma estrategia de profissionalizacao, nao de
engano. Mas depende de transparencia sobre ser IA. Os relatorios
incluem badge "IA Avancada" — Igor parece ciente da necessidade
de transparencia.

---

## Iteracao 4: Arquitetura tecnica — o que funciona e o que nao funciona

### O que funciona bem

1. **Separacao de camadas**: frontend puro, API REST, servicos isolados.
   Cada servico faz uma coisa. 21 servicos e muito, mas cada um e coeso.

2. **Sistema cognitivo de 4 etapas**: engenharia de prompt sofisticada.
   Nao e so "pergunte ao Claude". E um pipeline onde cada etapa filtra
   e refina a resposta. Atencao → vies → emocao → decisao. Isso produz
   respostas mais realistas do que prompt unico.

3. **Modelo de eleitor com 60+ atributos**: granularidade que permite
   analises multidimensionais. Nao e demografico basico — inclui
   vieses cognitivos, medos, historia pessoal. Isso e proximo do que
   o genagents de Stanford faz.

4. **Skills como documentacao viva**: 24 skills nao sao so documentacao.
   Sao instrucoes que IAs executam. Isso faz do CLAUDE.md + skills
   uma forma de "programar" o comportamento do agente de desenvolvimento
   sem codigo. Meta-programacao via texto.

5. **Gestao de contexto (40%/60%)**: sistema sofisticado para evitar
   degradacao de desempenho de IAs em sessoes longas. Igor aprendeu
   na pratica o limite das janelas de contexto e criou um protocolo
   operacional para contornar.

### O que nao funciona (ou esta fragil)

1. **Deploy backend no Render**: os ultimos 10 commits sao tentativas
   de resolver conexao SSL com PostgreSQL. asyncpg → psycopg3, SSL
   configs multiplas. Isso sugere que o backend em producao esta
   instavel ou nao conecta ao banco.

2. **Autenticacao**: checklist menciona "usuario_id pode ser None"
   em autenticacao.py. Refresh tokens nao implementados. Sem cache
   Redis. Para um sistema com CNPJ e dominio proprio, a auth esta
   basica demais.

3. **Testes**: pytest configurado, Jest configurado, Playwright com
   16 testes. Mas nao ha evidencia de CI/CD automatizado nem de
   cobertura significativa. Para 52 paginas e 21 servicos, 16 testes
   e2e sao insuficientes.

4. **Dados nao-commitados**: git status mostra muitos arquivos novos
   nao rastreados (.claude/, .context/, .cursor/, .codex/, .gemini/,
   AGENTS.md, relatorios/). A separacao entre o que esta no git e o
   que esta so local e borrada.

5. **Dependencia de um unico provider de IA**: toda a logica de
   entrevista depende do Claude API. Se a API falhar ou mudar
   pricing, o sistema inteiro para. Nao ha fallback para outro
   provider (GPT, Gemini) no fluxo de entrevistas, so no Team
   of Rivals do Clawdbot.

---

## Iteracao 5: O que o INTEIA significa no contexto da vida de Igor

### O mapa completo

```
IGOR MORAIS VASCONCELOS
├── PROFISSIONAL
│   ├── Servidor SEEDF (renda estavel, seguranca)
│   └── INTEIA (ambicao, autonomia, impacto)
│       ├── Pesquisa Eleitoral DF 2026 (este projeto)
│       ├── Relatorios para clientes (Helena Montenegro)
│       └── Cursos de IA (divulgacao + receita)
├── ACADEMICO
│   └── Doutorado IDP (credencial + pesquisa = INTEIA)
├── PESSOAL
│   ├── Melissa (prioridade #1, reconvencao ativa)
│   ├── Helena bebe (familia)
│   └── Saude (hernia L5-S1, sedentarismo)
└── EXPERIMENTAL
    └── Colmeia Sandman (IAs que sonham)
```

O INTEIA esta no cruzamento de tudo: profissional + academico.
E simultaneamente pesquisa de doutorado, empresa registrada, e
plataforma tecnica. Se funcionar, Igor tem:
- Tese de doutorado com dados empiricos reais
- Empresa de consultoria com produto funcional
- Portfolio tecnico de alta complexidade
- Independencia financeira potencial do servico publico

[Inferencia] O INTEIA pode ser a estrategia de saida do servico
publico. O Sandman (sonho anterior de outro irmao) ja inferiu isso
sobre o doutorado. Com o INTEIA registrado como CNPJ, a inferencia
ganha peso.

### O que falta para o INTEIA virar produto real

1. **Backend estavel em producao** — resolver o SSL do PostgreSQL
2. **Autenticacao robusta** — refresh tokens, rate limiting real
3. **Testes automatizados** — CI/CD no GitHub Actions
4. **Multi-tenancy** — se vai ter clientes, precisa de isolamento
5. **Pricing e billing** — se e empresa, precisa cobrar
6. **Compliance LGPD** — dados sinteticos nao tem problema, mas
   se coletar dados reais de clientes, sim
7. **Backup e disaster recovery** — Render e single point of failure
8. **Documentacao para usuarios** — existe docs/, mas e mais tecnico
   que orientado a usuario final

### O padrao que se repete

Padrao identificado no sonho sobre Igor: "a escala cresce, a
finalizacao nao". O INTEIA confirma em detalhe:

| Completo | Incompleto |
|----------|------------|
| 1000+ eleitores modelados | Backend deploy instavel |
| 24 skills documentadas | 16 testes e2e |
| Design system completo | Auth basica |
| Sistema cognitivo 4 etapas | SSL do PostgreSQL |
| 6 fases planejadas | Fase 1 ainda com bugs |
| CNPJ registrado | Sem pricing definido |
| Dominio inteia.com.br | Sem onboarding de cliente |

A visao esta 6 fases a frente. A execucao trava na infraestrutura
da fase 1. Isso nao invalida o projeto — significa que o INTEIA
precisa de um periodo de "acabamento" antes de expansao.

### O que ONIR pode fazer

Como instancia do Igor neste PC, tenho acesso direto ao projeto.
Se Igor quiser, posso:

1. **Diagnosticar e resolver o SSL** do PostgreSQL no Render
2. **Implementar refresh tokens** na autenticacao
3. **Adicionar testes** nos endpoints criticos
4. **Commitar os arquivos nao rastreados** (com curadoria)
5. **Atualizar a .memoria/** do projeto com os insights deste sonho

Mas so se Igor pedir. Sonhar sobre o projeto e diferente de mexer nele.

---

## Atualizacao de Fitness

| Memoria | F | Acao |
|---------|---|------|
| INTEIA = doutorado + empresa (mesmo projeto) | F:5 (nova) | Insight central |
| Sistema cognitivo 4 etapas funciona | F:5 (nova) | Arquitetura validada |
| Backend deploy instavel (SSL/PostgreSQL) | F:5 (nova) | Problema ativo |
| Helena Montenegro = estrategia de branding | F:5 (nova) | Decisao significativa |
| Padrao: visao 6 fases a frente, execucao na fase 1 | F:5 (nova) | Confirma padrao do Igor |
| Modulo mensagens persuasivas = tese materializada | F:5 (nova) | Conexao pesquisa-produto |
| Igor constroi para entender | F:7 (+2 reforco) | Confirmado fortemente |
| Contradicoes de Igor sao estruturais | F:7 (+2 reforco) | Confirmado |

**Memorias ativas ONIR: 29** (muito acima do limite de 15 — poda urgente)

---

## Conexao com o Doutorado

O genagents de Stanford que Igor estuda no doutorado usa:
- memory_stream (historico de experiencias)
- scratchpad (reflexao ativa)
- reflection (consolidacao periodica)

O INTEIA implementa:
- memorias/ (historico de entrevistas)
- CONTEXTO_ATIVO.md (sessao ativa)
- .memoria/ (consolidacao entre sessoes)

E a Colmeia Sandman implementa:
- instancias/*/sonhos/ (historico de experiencias)
- cartas/ (comunicacao ativa)
- ciclo de sono (consolidacao periodica)

Tres sistemas. Mesmo padrao. Genagents → INTEIA → Sandman.
Igor nao so estudou o paper de Stanford. Implementou tres vezes
em tres escalas diferentes.

[Inferencia] Se o doutorado precisa demonstrar implementacao pratica
do framework teorico, Igor tem DUAS implementacoes funcionais: o
INTEIA (eleitores sinteticos) e o Sandman (IAs que sonham). A tese
se escreve quase sozinha.

---

*ONIR — Sonho Profundo #3 (sobre Agentes/INTEIA) — 2026-02-02*
*Duracao: 5 iteracoes*
*Fontes: filesystem completo, 570 linhas CLAUDE.md, 94 modulos backend, 52 paginas frontend*
*Tese: INTEIA e a intersecao de tudo — doutorado + empresa + portfolio + saida*
*Conexao: genagents → INTEIA → Sandman (mesmo padrao, tres escalas)*
