# Runbook Rollback Colmeia

Versao: v1  
Ambiente alvo: Render (API) + Vercel (frontend)  
Rotas alvo: `https://inteia.com.br/colmeia` e `https://api.inteia.com.br/colmeia`

---

## 1. Objetivo

Reverter rapidamente o modulo Colmeia sem afetar a raiz de `inteia.com.br` nem os endpoints legados de `api.inteia.com.br`.

---

## 2. Gatilhos de Rollback

Executar rollback se ocorrer qualquer um:

1. erro 5xx persistente em `/colmeia/*` por mais de 5 minutos;
2. queda de healthcheck da API principal;
3. migration causando erro em tabelas legadas;
4. regressao grave de autenticacao/autorizacao;
5. aumento de latencia critico em endpoints principais da INTEIA.

---

## 3. Pre-Deploy Obrigatorio

1. Backup logico do PostgreSQL antes de migration.
2. Tag de release antes do deploy (`pre-colmeia-<timestamp>`).
3. Smoke tests prontos para:
- `https://api.inteia.com.br/health`
- `https://api.inteia.com.br/colmeia/dashboard`
- rotas legadas criticas
4. Confirmar que `inteia.com.br` raiz esta intacta.

---

## 4. Sequencia de Rollback (ordem obrigatoria)

## Etapa A - Contencao

1. Congelar novos deploys.
2. Desativar jobs/heartbeats que escrevem em `/colmeia`.
3. Ativar banner de manutencao no `/colmeia` se necessario.

## Etapa B - Aplicacao

1. Reverter API para release anterior estavel no Render.
2. Reverter frontend `/colmeia` no Vercel para build anterior estavel.
3. Validar healthcheck da API e homepage raiz.

## Etapa C - Banco

1. Se migration foi aplicada e causou impacto:
- rodar migration de downgrade, ou
- restaurar backup (ultimo caso).
2. Validar integridade das tabelas legadas.

## Etapa D - Validacao Pos-Rollback

1. Testar `https://api.inteia.com.br/health`.
2. Testar endpoint legado critico.
3. Testar `https://inteia.com.br` raiz.
4. Confirmar que `/colmeia` voltou ao estado estavel anterior.

---

## 5. Matriz de Decisao Rapida

1. Falha so no frontend `/colmeia`:
- rollback apenas no Vercel.

2. Falha so na API `/colmeia` sem impacto legado:
- rollback da API no Render.

3. Falha com impacto no banco legado:
- rollback API + rollback/downgrade de migration + restauracao se necessario.

---

## 6. Comunicacao de Incidente

Registro minimo:

1. timestamp de inicio e fim;
2. sintoma observado;
3. servicos impactados;
4. causa provavel;
5. acao de rollback executada;
6. status final;
7. acao preventiva para evitar recorrencia.

---

## 7. Reentrada Segura

Antes de novo deploy do Colmeia:

1. corrigir causa raiz;
2. executar testes em staging/local equivalente;
3. reaplicar migration somente com backup novo;
4. liberar deploy progressivo;
5. monitorar por janela de estabilizacao.

