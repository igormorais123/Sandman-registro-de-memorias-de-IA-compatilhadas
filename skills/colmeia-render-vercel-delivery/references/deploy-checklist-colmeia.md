# Deploy Checklist Colmeia (Render + Vercel)

## 1. Pre-deploy

1. Confirmar subrotas:
- `https://inteia.com.br/colmeia`
- `https://api.inteia.com.br/colmeia`
2. Backup do banco antes de migration.
3. Confirmar `USE_API=false` por padrao.
4. Confirmar auth/RBAC em `/colmeia/*`.

## 2. Deploy Backend (Render)

1. Aplicar migration.
2. Validar health:
- endpoint legado de health.
- `GET /colmeia/dashboard`.
3. Validar logs de erro pos deploy.

## 3. Deploy Frontend (Vercel)

1. Publicar apenas em `/colmeia`.
2. Confirmar raiz `https://inteia.com.br` intacta.
3. Confirmar consumo da API em `https://api.inteia.com.br/colmeia`.

## 4. Pos-deploy

1. Smoke test:
- criar task
- mover status
- postar mensagem
- listar dashboard
2. Validar auditoria de mutacoes.
3. Monitorar erro 5xx por janela inicial.

## 5. Rollback

1. Seguir `docs/RUNBOOK_ROLLBACK_COLMEIA.md`.
2. Reverter backend, frontend e migration conforme severidade.

