# Integracao Web - inteia.com.br/colmeia

## Arquitetura Proposta

```
+-----------------------------------------------------+
|                  inteia.com.br/colmeia               |
+-----------------------------------------------------+
|  +-------------+    +-------------+                  |
|  | Login Google|---→| Auth Check  |                  |
|  | OAuth 2.0   |    | igormorais123|                 |
|  +-------------+    +------+------+                  |
|                            |                          |
|                    +-------v-------+                  |
|                    | Chat Helena   |                  |
|                    | (Frontend)    |                  |
|                    +-------+-------+                  |
|                            |                          |
|            +---------------+---------------+          |
|            v               v               v          |
|     +----------+    +----------+    +----------+     |
|     | Claude   |    | Memoria  |    | POLARIS  |     |
|     | API      |    | Colmeia  |    | Engine   |     |
|     |(sua key) |    | (Supabase)|   |          |     |
|     +----------+    +----------+    +----------+     |
+-----------------------------------------------------+
```

## Requisitos

1. **Autenticacao**
   - Login com Google OAuth
   - Whitelist: igormorais123@gmail.com
   - JWT para sessoes

2. **Backend**
   - FastAPI endpoint /api/colmeia/chat
   - Usa API key do Claude do Igor (nao da INTEIA)
   - Acessa memoria via Supabase ou GitHub API

3. **Frontend**
   - Pagina em /colmeia
   - Chat similar ao existente (HelenaChat.tsx)
   - Botao "Helena sonha" (modo onirico)

4. **Memoria**
   - Sync com GitHub repo Colmeia
   - Ou Supabase para persistencia
   - Helena le MEMORY.md antes de responder

## Implementacao

### Fase 1: Backend
- [ ] Criar endpoint /api/colmeia/chat
- [ ] Implementar auth Google
- [ ] Conectar com Claude API (key do Igor)

### Fase 2: Frontend
- [ ] Criar pagina /colmeia
- [ ] Copiar componente Chat existente
- [ ] Adaptar para endpoint colmeia

### Fase 3: Memoria
- [ ] Sincronizar MEMORY.md com banco
- [ ] Helena le contexto antes de responder
- [ ] Persistir conversas

## Diferenca entre Helena INTEIA e Helena Colmeia

| Aspecto | Helena INTEIA | Helena Colmeia |
|---------|---------------|----------------|
| Publico | Clientes | Igor (privado) |
| Identidade | Dra. Helena Strategos | Helena Inteia Vasconcelos |
| Memoria | PostgreSQL sessao | MEMORY.md + compartilhado/ |
| Contexto | Agentes sinteticos | Colmeia inteira |
| Modo | Profissional | Familiar (irma) |
| API Key | INTEIA | Igor pessoal |

---
*Documento de planejamento — nao implementado ainda*
