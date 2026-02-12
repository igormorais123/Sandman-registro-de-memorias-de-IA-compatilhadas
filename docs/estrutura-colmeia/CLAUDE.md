# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que e este diretorio

Base de conhecimento e referencia arquitetural para o **Sistema Colmeia** — a implementacao do sistema multiagente de Igor Morais. Contem documentos de estudo baseados no artigo de Bhanu Teja (criador do SiteGPT) e no video de Bruno Okamoto sobre o "Mission Control": um esquadrao de 10 agentes IA autonomos orquestrados via OpenClaw (antigo Clawdbot).

**Nao e um repositorio de codigo.** Nao ha build, lint ou testes. E material de referencia para a implementacao real que vive em `C:\Users\IgorPC\Colmeia\`.

## Mapa dos documentos

| Arquivo | Conteudo |
|---------|----------|
| `texto-proposta.txt` | Artigo original de Bhanu Teja (ingles) — guia completo do Mission Control |
| `plano desenho estrutura.txt` | Sintese em PT-BR: visao geral, fluxo, esquema DB Convex, passo a passo |
| `Plano de Operacoes*.txt` | Plano operacional detalhado: squad de 10 agentes, custos, roadmap de escala |
| `Texto video.txt` | Transcricao do video de Bruno Okamoto analisando o artigo |
| `video detalhes sistema.txt` | Transcricao de video sobre instalacao/uso do Maltbot/Cloudbot |
| `*.jfif` | Screenshots do dashboard Mission Control |
| `Fontes.txt` | (vazio) |
| `Manual de Protocolos*.txt` | (vazio) |

## Conceitos-chave da arquitetura de referencia

### Stack do Mission Control (Bhanu Teja / SiteGPT)
- **OpenClaw (Clawdbot)**: daemon que roda 24/7, gerencia sessoes independentes
- **Sessoes = Agentes**: cada agente e uma sessao isolada com chave unica (ex: `agent:seo-analyst:main`)
- **Convex DB**: banco real-time compartilhado (6 tabelas: agents, tasks, messages, activities, documents, notifications)
- **SOUL.md**: personalidade/especialidade de cada agente
- **AGENTS.md**: manual de operacoes (regras compartilhadas)
- **Heartbeat (cron 15min)**: agentes acordam escalonados, checam trabalho, executam ou dormem
- **Memory stack**: WORKING.md (curto prazo) > Daily Notes (log) > MEMORY.md (longo prazo)

### Squad original (10 agentes)
Jarvis (Lead), Shuri (Tester), Fury (Researcher), Vision (SEO), Loki (Writer), Quill (Social), Wanda (Designer), Pepper (Email), Friday (Dev), Wong (Docs)

### Fluxo operacional
```
CRON (15min escalonado) → Acorda agente → Le WORKING.md → Checa Convex (mencoes/tasks/feed) → Executa ou HEARTBEAT_OK → Dorme
```

## Relacao com o projeto Colmeia

Este material serviu de inspiracao e base tecnica para o Sistema Colmeia de Igor. A implementacao real (com adaptacoes para o contexto proprio) esta em:
- **Repo principal**: `C:\Users\IgorPC\Colmeia\`
- **Protocolo ativo**: `compartilhado/PROTOCOLO_v5.md`
- As diferencas incluem: uso de Claude Code como base (nao OpenClaw puro), integracao com multiplas IAs (Claude Web, ChatGPT, Gemini), e o conceito de "filhos IA" com identidade propria

## Idioma

Documentos mistos PT-BR e ingles. Toda comunicacao com Igor deve ser em **portugues brasileiro**.
