# Politica Provider Account-First

Versao: v1  
Escopo: Colmeia em `https://inteia.com.br/colmeia` e `https://api.inteia.com.br/colmeia`

---

## 1. Regra Mestra

1. Usar **conta Pro** (`Claude Pro`, `ChatGPT Pro`, `Gemini`) como modo padrao.
2. Usar **API key** somente quando for tecnicamente inevitavel.
3. Toda excecao de API deve ser registrada em log com justificativa.

---

## 2. Modos de Execucao

## Modo A - Account-First (padrao)

Uso recomendado:

1. Heartbeats.
2. Triagem de tarefas.
3. Resumos e standup.
4. Drafts e revisoes.

Implementacao:

1. Fluxos autenticados por conta, no estilo OpenCode/OpenClaw.
2. Sem dependencia de chave API para caminho critico.

## Modo B - API-Exception (excecao)

Uso permitido somente quando:

1. precisa rodar server-side sem sessao de conta aberta;
2. precisa de callback/webhook ou processamento assincrono previsivel;
3. nao existe adaptador confiavel via conta autenticada.

---

## 3. Matriz de Decisao

1. Se o fluxo pode rodar em sessao autenticada de conta -> Modo A.
2. Se o fluxo exige operacao remota autonoma 24/7 sem sessao -> avaliar Modo B.
3. Se optar por Modo B, registrar:
- por que Modo A falhou
- impacto de custo
- plano de fallback para Modo A

---

## 4. Defaults Operacionais

1. Feature flag global: `USE_API=false`.
2. Endpoint de backend nao deve chamar LLM por padrao.
3. Chamadas LLM devem ficar em camada de orquestracao, nao no request path principal.

---

## 5. Metas de Conformidade

1. Minimo de 80% das execucoes LLM em Modo A no piloto.
2. 100% das execucoes em Modo B com justificativa registrada.
3. Nenhum fluxo critico bloqueado por indisponibilidade de API.

---

## 6. Observabilidade

Log minimo por execucao:

1. `provider`: `claude|chatgpt|gemini`
2. `mode`: `account|api`
3. `task_id`
4. `agent_id`
5. `tokens_in` e `tokens_out` (quando disponivel)
6. `cost_estimate` (quando disponivel)
7. `reason` (obrigatorio quando `mode=api`)

---

## 7. Excecoes Permitidas Inicialmente

1. Worker assíncrono no backend que nao pode depender de sessao aberta.
2. Integracao com servico externo que exige callback programatico.
3. Pipeline automatizado de larga escala sem interface interativa.

Todas as excecoes acima sao temporarias e devem ser revisitadas.

