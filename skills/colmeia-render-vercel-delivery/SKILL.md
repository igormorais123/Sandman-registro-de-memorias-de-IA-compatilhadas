---
name: colmeia-render-vercel-delivery
description: Implementar e entregar modulo Colmeia no stack existente da INTEIA (Render + Vercel), preservando a raiz atual do sistema e publicando apenas em /colmeia. Use quando o usuario pedir para desenvolver backend/frontend da Colmeia, ajustar rotas de deploy, ou validar go-live em https://inteia.com.br/colmeia e https://api.inteia.com.br/colmeia.
---

# Colmeia Render Vercel Delivery

## Workflow

1. Confirmar contrato de rota:
- frontend: `https://inteia.com.br/colmeia`
- api: `https://api.inteia.com.br/colmeia`
- nao alterar raiz de `https://inteia.com.br`.

2. Implementar backend por extensao (nao projeto novo):
- adicionar modulo `colmeia` na API FastAPI existente.
- criar schema/migrations sem quebrar legado.
- aplicar auth + RBAC nos endpoints `/colmeia/*`.

3. Aplicar politica provider:
- conta Pro primeiro.
- API por excecao e com justificativa registrada.

4. Publicar frontend em subrota:
- manter interface Colmeia isolada em `/colmeia`.
- preservar app principal.

5. Validar go-live:
- healthcheck API legado e API Colmeia.
- smoke tests de endpoints criticos.
- rollback pronto antes do deploy.

## Regras de Implementacao

1. Usar 1 IA principal para implementar ponta a ponta.
2. Usar 1 IA revisora para testes e hardening.
3. Evitar dividir backend em muitas IAs sem contrato congelado.
4. Nunca aplicar migration sem backup.

## Referencias Obrigatorias

1. `docs/PLANO_IMPLANTACAO_COLMEIA.md`
2. `docs/CONTRATO_API_COLMEIA.md`
3. `docs/POLITICA_PROVIDER_ACCOUNT_FIRST.md`
4. `docs/RUNBOOK_ROLLBACK_COLMEIA.md`
5. `references/deploy-checklist-colmeia.md`

## Criterios de Pronto

1. `/colmeia` acessivel sem quebrar a raiz.
2. Endpoints `/colmeia/*` autenticados e auditaveis.
3. Politica account-first aplicada.
4. Rollback testado.
