# Contrato API Colmeia

Versao: v1  
Base publica obrigatoria: `https://api.inteia.com.br/colmeia`  
Base interna permitida: `/api/v1/colmeia` (com rewrite)

---

## 1. Regras Gerais

1. Todas as rotas ` /colmeia/* ` exigem autenticacao.
2. Toda mutacao grava trilha de auditoria (`actor_id`, `actor_type`, `timestamp`).
3. Respostas JSON padrao:
- sucesso: `{ "ok": true, "data": ... }`
- erro: `{ "ok": false, "error": { "code": "...", "message": "..." } }`
4. Idempotencia obrigatoria em operacoes de status e entrega de notificacao.

---

## 2. Autenticacao e RBAC Minimo

Perfis:

1. `lead`
- pode criar task, atribuir, mover status, postar mensagem, gerar standup.

2. `specialist`
- pode comentar, atualizar task atribuida, registrar heartbeat.

3. `viewer`
- leitura de dashboard, tasks, activities e documentos.

Cabecalhos:

1. `Authorization: Bearer <token>`
2. `X-Agent-Id: <uuid>` (obrigatorio para agentes automatizados)

---

## 3. Entidades

1. `colmeia_agents`
2. `colmeia_tasks`
3. `colmeia_messages`
4. `colmeia_activities`
5. `colmeia_notifications`
6. `colmeia_documents`

Campos base recomendados (transacionais):

1. `id` UUID
2. `created_at` TIMESTAMP
3. `updated_at` TIMESTAMP

---

## 4. Endpoints

## 4.1 Agents

1. `GET /colmeia/agents`
2. `GET /colmeia/agents/{id}`
3. `POST /colmeia/agents/{id}/heartbeat`
4. `PUT /colmeia/agents/{id}/status`

Heartbeat request:

```json
{
  "status": "idle",
  "summary": "HEARTBEAT_OK",
  "working_task_id": "uuid-ou-null"
}
```

## 4.2 Tasks

1. `GET /colmeia/tasks?status=&assignee_id=&q=&page=&limit=`
2. `POST /colmeia/tasks`
3. `GET /colmeia/tasks/{id}`
4. `PUT /colmeia/tasks/{id}`
5. `PUT /colmeia/tasks/{id}/status`
6. `PUT /colmeia/tasks/{id}/assign`

Status permitidos:

1. `backlog`
2. `assigned`
3. `in_progress`
4. `review`
5. `done`
6. `blocked`

## 4.3 Messages

1. `GET /colmeia/tasks/{id}/messages?page=&limit=`
2. `POST /colmeia/tasks/{id}/messages`

Message request:

```json
{
  "content": "texto da mensagem",
  "mentions": ["agent_uuid_1", "agent_uuid_2"]
}
```

## 4.4 Activities

1. `GET /colmeia/activities?page=&limit=`
2. `GET /colmeia/activities/agent/{id}?page=&limit=`

Tipos minimos:

1. `task_created`
2. `task_status_changed`
3. `task_assigned`
4. `message_posted`
5. `document_created`
6. `heartbeat_registered`

## 4.5 Notifications

1. `GET /colmeia/notifications/pending?agent_id=`
2. `POST /colmeia/notifications`
3. `PUT /colmeia/notifications/{id}/delivered`

## 4.6 Documents

1. `GET /colmeia/tasks/{id}/documents`
2. `POST /colmeia/tasks/{id}/documents`

## 4.7 Dashboard

1. `GET /colmeia/dashboard`
2. `GET /colmeia/standup`

`GET /colmeia/dashboard` deve retornar:

1. contagem por status
2. agentes ativos/ociosos
3. ultimas atividades
4. bloqueios abertos

`GET /colmeia/standup` deve retornar:

1. `completed_today`
2. `in_progress`
3. `blocked`
4. `needs_review`
5. `key_decisions`

---

## 5. Nao-Funcionais

1. Limite inicial de pagina: max `100`.
2. Timeout de leitura: `5s`.
3. Timeout de mutacao: `10s`.
4. Todas as rotas com logs estruturados.
5. OpenAPI precisa refletir 100% dos endpoints acima.

