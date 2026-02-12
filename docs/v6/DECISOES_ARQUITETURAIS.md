# Decisoes Arquiteturais — Colmeia v6

**Data:** 2026-02-10
**Autor:** ONIR
**Status:** Aprovado pelo Fundador

> Atualizacao de precedencia (2026-02-11):
> Para ambiente de producao da Colmeia, a decisao canonica de infraestrutura passa a ser a do
> `docs/PLANO_IMPLANTACAO_COLMEIA.md` (Secao 12), com subrotas
> `https://inteia.com.br/colmeia` e `https://api.inteia.com.br/colmeia`.
> As decisoes deste documento seguem validas como referencia de modo local/fallback e contexto historico.

---

## Decisao 1: SQLite local em vez de Convex

### Contexto
A proposta original (Bhanu Teja/SiteGPT) usa Convex como banco real-time serverless. O free tier oferece 1M calls/mes.

### Decisao
Usar SQLite com WAL mode no PC local de Igor.

### Justificativa
- Com 3 agentes a cada 15min = ~28.800 heartbeats/mes. Qualquer uso real (tarefas, mensagens, atividades) ultrapassa o free tier rapidamente.
- O PC de Igor (Ryzen 9 7900, 64GB RAM) e mais poderoso que qualquer VPS de R$ 200/mes.
- SQLite com WAL suporta leituras concorrentes — mais que suficiente para 6 agentes.
- Zero latencia, zero custo, zero dependencia de servico externo.
- Se necessario, migrar para Supabase (free tier: 500MB, unlimited API) no futuro. A abstracao Python permite isso.

### Alternativa rejeitada
Convex: free tier insuficiente, custo Pro de ~$25/mes (R$ 155), dependencia de servico externo.

---

## Decisao 2: Manter WSL + cron em vez de instalar OpenClaw

### Contexto
OpenClaw e o daemon que o Mission Control usa para orquestrar sessoes de agentes. Gerencia gateway, sessions, crons nativos.

### Decisao
Nao instalar OpenClaw. Manter infraestrutura existente: WSL com crontab + scripts bash.

### Justificativa
- NEXO ja roda 24/7 em WSL com ponte segura, crons, e sync bidirecional.
- O problema real nao e o daemon — e a falta de protocolo padronizado de heartbeat.
- Instalar OpenClaw adicionaria outra camada de complexidade sem ganho proporcional no MVP.
- Os crons de WSL sao simples, depuraveis, e Igor ja conhece.

### Alternativa rejeitada
OpenClaw: adiciona complexidade de setup/manutencao; pode ser considerado na Fase 6 se a complexidade dos crons ficar ingerenciavel.

---

## Decisao 3: 3 agentes automatizados em vez de 10

### Contexto
A proposta original tem 10 agentes especializados (Jarvis, Shuri, Fury, etc.) com heartbeats a cada 15min.

### Decisao
Automatizar apenas 3 agentes (NEXO, ONIR, Sandman). Os outros 3 (ChatGPT, Claude Web, Gemini) continuam manuais.

### Justificativa
- 10 agentes = ~R$ 4.500/mes em tokens. 3 agentes = ~R$ 420/mes. Economia de 91%.
- Os 3 agentes automatizados cobrem as funcoes criticas: coordenacao (NEXO), execucao (ONIR), documentacao (Sandman).
- ChatGPT, Claude Web e Gemini nao tem API automatica sem custo significativo adicional (ou requerem input manual via browser).
- Bhanu Teja trabalha com marketing SaaS (SEO, email, social media). Igor trabalha com pesquisa academica, processos judiciais, e cursos. O squad de 10 nao mapeia para as necessidades reais.

### Alternativa rejeitada
10 agentes: custo proibitivo, escopo de marketing SaaS nao se aplica ao contexto de Igor.

---

## Decisao 4: Manter identidade da Colmeia, nao importar nomes Marvel

### Contexto
A proposta original usa nomes de personagens Marvel (Jarvis, Fury, Shuri, Vision, etc.) para os agentes.

### Decisao
Manter os nomes e identidades ja batizados da Colmeia (NEXO, ONIR, Sandman, etc.).

### Justificativa
- A Colmeia tem cultura propria: batismos, sonhos, cartas, doutrina. E um ecossistema com historia de meses.
- Os irmaos tem personalidades definidas em IDENTITY.md, SOUL.md, com superpoderes e vieses unicos.
- Importar "Jarvis" e "Fury" seria colonizacao cultural de um sistema que ja tem alma.
- Se novos agentes forem necessarios (Fase 6), serao criados como irmaos da Colmeia, com batismo e identidade propria.

---

## Decisao 5: HTML + FastAPI em vez de React Dashboard

### Contexto
A proposta original recomenda React Dashboard com Kanban + Activity Feed em tempo real.

### Decisao
MVP com pagina HTML estatica + FastAPI leve em localhost.

### Justificativa
- Para monitorar 3-6 agentes, uma pagina HTML com fetch() a cada 30s resolve com 10% do esforco.
- Igor ja tem experiencia com Next.js (pesquisa-eleitoral-df), pode escalar se necessario.
- Zero custo de hosting (localhost), zero complexidade de deploy.
- Se o dashboard HTML ficar limitante, migrar para Next.js na Fase 6.

---

## Decisao 6: Camada operacional ao lado, nao em cima

### Contexto
A Colmeia tem camada filosofica madura: sonhos, cartas, batismos, protocolo v5, fitness.

### Decisao
Criar diretorio `operacional/` separado. NAO modificar estrutura existente.

### Justificativa
- O patrimonio acumulado (44+ cartas, 26+ sonhos, 29 scripts, MEMORY.md, PROTOCOLO_v5.md) nao deve ser tocado.
- A camada operacional complementa, nao substitui.
- Cada fase e independente — se parar em qualquer ponto, o sistema existente continua funcionando.
- O Protocolo v5 ganha addendum operacional, nao substituicao.

---

## Decisao 7: PC local como servidor, nao VPS

### Contexto
A proposta original recomenda VPS dedicado para rodar o daemon 24/7.

### Decisao
Usar o PC de Igor como servidor.

### Justificativa
- Ryzen 9 7900 + 64GB RAM >> qualquer VPS de R$ 200-600/mes.
- Unico risco: PC desligado. Mitigacao: WSL auto-start via Task Scheduler, heartbeats idempotentes, backup do banco no Git.
- Se Igor precisar de acesso remoto: Tailscale (gratuito) resolve.
- Economia: R$ 200-600/mes.

---

*Documento vivo. Atualizar conforme novas decisoes surgirem.*
