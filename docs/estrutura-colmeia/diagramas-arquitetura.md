# Diagramas da Arquitetura — Sistema Mission Control / Colmeia

---

## 1. Arquitetura Geral do Sistema

```mermaid
graph TB
    subgraph HUMANO["HUMANO (Igor)"]
        TG["Telegram"]
        WA["WhatsApp"]
        DASH["Dashboard React"]
    end

    subgraph SERVIDOR["SERVIDOR (VPS 24/7)"]
        GW["Gateway OpenClaw<br/>(pm2 daemon)"]
        CRON["Cron Scheduler<br/>(heartbeats 15min)"]
        NOTIF["Notification Daemon<br/>(poll 2s)"]

        subgraph SESSOES["SESSOES INDEPENDENTES"]
            S1["Jarvis<br/>agent:main:main<br/>Squad Lead"]
            S2["Shuri<br/>agent:product-analyst:main<br/>Tester"]
            S3["Fury<br/>agent:customer-researcher:main<br/>Pesquisador"]
            S4["Vision<br/>agent:seo-analyst:main<br/>SEO"]
            S5["Loki<br/>agent:content-writer:main<br/>Redator"]
            S6["Quill<br/>agent:social-media-manager:main<br/>Social"]
            S7["Wanda<br/>agent:designer:main<br/>Designer"]
            S8["Pepper<br/>agent:email-marketing:main<br/>Email"]
            S9["Friday<br/>agent:developer:main<br/>Dev"]
            S10["Wong<br/>agent:notion-agent:main<br/>Docs"]
        end

        subgraph FILESYSTEM["FILESYSTEM LOCAL"]
            SOUL["SOUL.md<br/>(por agente)"]
            AGENTS["AGENTS.md<br/>(compartilhado)"]
            HB["HEARTBEAT.md<br/>(checklist)"]
            MEM["memory/<br/>WORKING.md<br/>YYYY-MM-DD.md<br/>MEMORY.md"]
        end
    end

    subgraph CLOUD["CLOUD"]
        CONVEX["Convex DB<br/>(real-time serverless)"]
        API_AI["APIs de IA<br/>Claude Opus / Haiku<br/>GPT-4o / mini<br/>Gemini / Groq"]
    end

    TG <-->|mensagens| GW
    WA <-->|mensagens| GW
    DASH <-->|WebSocket| CONVEX

    GW <-->|gerencia| SESSOES
    CRON -->|acorda| SESSOES
    NOTIF <-->|poll/entrega| CONVEX
    NOTIF -->|send| GW

    SESSOES <-->|le/escreve| FILESYSTEM
    SESSOES <-->|CLI npx convex run| CONVEX
    SESSOES <-->|API calls| API_AI
```

---

## 2. Anatomia de um Agente (Workspace)

```mermaid
graph LR
    subgraph AGENTE["AGENTE (ex: Shuri)"]
        SK["Session Key<br/>agent:product-analyst:main"]

        subgraph IDENTIDADE["IDENTIDADE"]
            SOUL2["SOUL.md<br/>Personalidade<br/>Especialidade<br/>Vies operacional"]
            AGENTS2["AGENTS.md<br/>Manual de operacoes<br/>Regras compartilhadas"]
        end

        subgraph MEMORIA["MEMORIA"]
            WORK["WORKING.md<br/>Tarefa atual<br/>Status<br/>Proximos passos"]
            DAILY["YYYY-MM-DD.md<br/>Logs do dia<br/>Audit trail"]
            LONG["MEMORY.md<br/>Licoes aprendidas<br/>Decisoes-chave"]
        end

        subgraph OPERACAO["OPERACAO"]
            HB2["HEARTBEAT.md<br/>Checklist ao acordar"]
            HIST["historico.jsonl<br/>Conversas passadas"]
            SCRIPTS["scripts/<br/>Utilitarios"]
            CONFIG["config/<br/>Credenciais"]
        end

        subgraph CONEXOES["CONEXOES"]
            TOOLS["Ferramentas<br/>Shell, Browser<br/>Filesystem, APIs"]
            MODEL["Modelo IA<br/>Opus para craft<br/>Haiku para rotina"]
            CRONJ["Cron Job<br/>*/15 * * * *<br/>escalonado"]
        end
    end

    SK --> IDENTIDADE
    SK --> MEMORIA
    SK --> OPERACAO
    SK --> CONEXOES
```

---

## 3. Fluxo do Heartbeat (Ciclo de Vida do Agente)

```mermaid
flowchart TD
    START(["CRON JOB DISPARA<br/>(a cada 15min, escalonado)"])

    WAKE["Acorda agente<br/>(sessao isolated)"]

    LOAD["1. CARREGAR CONTEXTO<br/>Le WORKING.md<br/>Le Daily Notes<br/>Busca session memory se necessario"]

    URGENT{"2. CHECAGEM URGENTE<br/>Fui @mencionado?<br/>Tenho tasks assignadas?"}

    FEED["3. SCAN ACTIVITY FEED<br/>Discussoes relevantes?<br/>Decisoes que afetam meu trabalho?"]

    DECIDE{"4. HA TRABALHO<br/>A FAZER?"}

    subgraph EXECUTA["EXECUCAO"]
        WORK2["Executa tarefa<br/>(pesquisa, escrita, codigo, etc.)"]
        UPDATE_DB["Atualiza Convex DB<br/>(comments, status, docs)"]
        UPDATE_LOCAL["Atualiza WORKING.md<br/>Atualiza Daily Notes"]
    end

    SLEEP_OK(["Reporta HEARTBEAT_OK<br/>Encerra sessao<br/>(custo zero)"])

    SLEEP_DONE(["Encerra sessao<br/>Volta a dormir"])

    START --> WAKE
    WAKE --> LOAD
    LOAD --> URGENT
    URGENT -->|SIM| EXECUTA
    URGENT -->|NAO| FEED
    FEED --> DECIDE
    DECIDE -->|SIM| EXECUTA
    DECIDE -->|NAO| SLEEP_OK
    WORK2 --> UPDATE_DB
    UPDATE_DB --> UPDATE_LOCAL
    UPDATE_LOCAL --> SLEEP_DONE
```

---

## 4. Escalonamento dos Heartbeats (Timeline 15min)

```mermaid
gantt
    title Escalonamento de Heartbeats (ciclo de 15 minutos)
    dateFormat mm
    axisFormat %M min

    section Pepper
    Heartbeat :p1, 00, 2m

    section Shuri
    Heartbeat :s1, 02, 2m

    section Friday
    Heartbeat :f1, 04, 2m

    section Loki
    Heartbeat :l1, 06, 1m

    section Wanda
    Heartbeat :w1, 07, 1m

    section Vision
    Heartbeat :v1, 08, 2m

    section Fury
    Heartbeat :fu1, 10, 2m

    section Quill
    Heartbeat :q1, 12, 2m
```

---

## 5. Schema do Banco de Dados (Convex — 6 Tabelas)

```mermaid
erDiagram
    AGENTS {
        string id PK
        string name "ex: Shuri"
        string role "ex: Product Analyst"
        enum status "idle | active | blocked"
        string sessionKey "ex: agent:product-analyst:main"
        id currentTaskId FK
    }

    TASKS {
        string id PK
        string title
        string description
        enum status "inbox | assigned | in_progress | review | done"
        array assigneeIds FK "Id de agents[]"
    }

    MESSAGES {
        string id PK
        id taskId FK
        id fromAgentId FK
        string content "texto do comentario"
        array attachments FK "Id de documents[]"
        datetime timestamp
    }

    ACTIVITIES {
        string id PK
        enum type "task_created | message_sent | document_created | status_changed"
        id agentId FK
        string message "descricao da atividade"
        datetime timestamp
    }

    DOCUMENTS {
        string id PK
        string title
        string content "Markdown"
        enum type "deliverable | research | protocol"
        id taskId FK
        id authorAgentId FK
    }

    NOTIFICATIONS {
        string id PK
        id mentionedAgentId FK
        string content
        boolean delivered "false ate entrega"
        datetime createdAt
    }

    AGENTS ||--o{ TASKS : "assignado a"
    AGENTS ||--o{ MESSAGES : "envia"
    AGENTS ||--o{ ACTIVITIES : "gera"
    AGENTS ||--o{ DOCUMENTS : "cria"
    AGENTS ||--o{ NOTIFICATIONS : "recebe"
    TASKS ||--o{ MESSAGES : "tem comentarios"
    TASKS ||--o{ DOCUMENTS : "tem entregaveis"
    TASKS ||--o{ ACTIVITIES : "gera eventos"
```

---

## 6. Ciclo de Vida de uma Task (Kanban)

```mermaid
stateDiagram-v2
    [*] --> INBOX : Humano ou Jarvis cria task

    INBOX --> ASSIGNED : Atribuida a agente(s)
    ASSIGNED --> IN_PROGRESS : Agente comeca a trabalhar
    IN_PROGRESS --> REVIEW : Draft/entregavel pronto
    IN_PROGRESS --> BLOCKED : Dependencia externa ou duvida
    BLOCKED --> IN_PROGRESS : Bloqueio resolvido
    REVIEW --> IN_PROGRESS : Feedback/revisoes necessarias
    REVIEW --> DONE : Aprovado pelo humano

    DONE --> [*]

    state INBOX {
        [*] --> Nova
        Nova : Task criada
        Nova : Sem dono ainda
    }

    state ASSIGNED {
        [*] --> ComDono
        ComDono : Agente(s) notificado(s)
        ComDono : Aguardando proximo heartbeat
    }

    state IN_PROGRESS {
        [*] --> Executando
        Executando : Agente pesquisa/escreve/coda
        Executando : Atualiza WORKING.md
        Executando : Posta comments no Convex
    }

    state REVIEW {
        [*] --> AguardandoAprovacao
        AguardandoAprovacao : Humano revisa
        AguardandoAprovacao : Outros agentes revisam
    }
```

---

## 7. Sistema de Notificacao e @Mentions

```mermaid
sequenceDiagram
    participant L as Loki (Redator)
    participant CX as Convex DB
    participant ND as Notification Daemon<br/>(poll 2s)
    participant GW as Gateway OpenClaw
    participant V as Vision (SEO)

    Note over L: Loki posta comentario<br/>com @Vision na thread

    L->>CX: messages:create<br/>"@Vision, preciso de keywords"
    CX->>CX: Detecta @mention<br/>Cria notification<br/>(delivered=false)

    loop A cada 2 segundos
        ND->>CX: Busca notifications<br/>onde delivered=false
        CX-->>ND: Retorna notification<br/>para Vision
    end

    alt Vision esta acordado (sessao ativa)
        ND->>GW: sessions.send<br/>("agent:seo-analyst:main", msg)
        GW->>V: Entrega mensagem
        ND->>CX: Marca delivered=true
    else Vision esta dormindo
        ND->>GW: sessions.send falha
        Note over ND: Notification fica na fila<br/>Tentara novamente em 2s
    end

    Note over V: Proximo heartbeat de Vision<br/>(sessao ativa novamente)
    ND->>GW: sessions.send (retry)
    GW->>V: Entrega mensagem atrasada
    ND->>CX: Marca delivered=true

    V->>CX: messages:create<br/>"Keywords pesquisadas: ..."
    Note over L: Loki inscrito na thread<br/>Recebe automaticamente
```

---

## 8. Thread Subscriptions (Inscricao Automatica)

```mermaid
flowchart LR
    subgraph GATILHOS["GATILHOS DE INSCRICAO"]
        G1["Comentou na task"]
        G2["Foi @mencionado"]
        G3["Foi assignado"]
    end

    G1 --> SUB["INSCRITO NA THREAD"]
    G2 --> SUB
    G3 --> SUB

    SUB --> RECEBE["Recebe TODOS os<br/>comentarios futuros<br/>automaticamente"]

    RECEBE --> N1["Sem precisar de<br/>@mention a cada vez"]

    subgraph EXEMPLO["EXEMPLO"]
        direction TB
        E1["Vision posta keyword research"]
        E2["Fury comenta com dados G2"]
        E3["Shuri adiciona prints de UX"]
        E4["Loki posta draft"]
        E5["Todos recebem tudo<br/>(todos inscritos)"]
    end

    RECEBE --> EXEMPLO
```

---

## 9. Stack de Memoria (3 Camadas)

```mermaid
graph TB
    subgraph CURTO["CURTO PRAZO"]
        WORKING["WORKING.md<br/>━━━━━━━━━━━━━━<br/>Current Task: Pesquisar pricing<br/>Status: Coletando dados G2<br/>Next Steps:<br/>1. Testar free tier<br/>2. Documentar achados<br/>3. Postar na thread"]
    end

    subgraph MEDIO["MEDIO PRAZO (Audit Trail)"]
        D1["2026-02-08.md"]
        D2["2026-02-09.md"]
        D3["2026-02-10.md<br/>━━━━━━━━━━━━━━<br/>09:15 UTC<br/>- Postou research na task<br/>- Fury adicionou pricing<br/>14:30 UTC<br/>- Revisou draft do Loki<br/>- Sugeriu mudancas"]
    end

    subgraph LONGO["LONGO PRAZO (Curado)"]
        MEMORY["MEMORY.md<br/>━━━━━━━━━━━━━━<br/>Decisoes estrategicas<br/>Licoes aprendidas<br/>Fatos estaveis da empresa<br/>Padroes identificados"]
    end

    subgraph SESSION["SESSAO (Built-in)"]
        JSONL["historico.jsonl<br/>━━━━━━━━━━━━━━<br/>Conversas passadas<br/>Pesquisavel pelo agente"]
    end

    WORKING -->|"atualizado a cada<br/>heartbeat/execucao"| D3
    D1 -->|"curado periodicamente"| MEMORY
    D2 -->|"curado periodicamente"| MEMORY
    SESSION -.->|"pesquisa se<br/>contexto unclear"| WORKING

    style CURTO fill:#ff6b6b,color:#fff
    style MEDIO fill:#ffa502,color:#fff
    style LONGO fill:#2ed573,color:#fff
    style SESSION fill:#5352ed,color:#fff
```

---

## 10. Fluxo Real: Pagina de Comparacao com Concorrente

```mermaid
sequenceDiagram
    participant H as Humano (Igor)
    participant J as Jarvis (Lead)
    participant V as Vision (SEO)
    participant F as Fury (Research)
    participant SH as Shuri (Tester)
    participant L as Loki (Writer)
    participant CX as Convex DB

    Note over H,CX: DIA 1

    H->>CX: Cria task "Comparacao vs Concorrente X"
    H->>CX: Assigna Vision + Loki

    Note over V: Heartbeat :08 — Vision acorda
    V->>CX: Le task assignada
    V->>V: Pesquisa keywords<br/>Volume, intencao de busca
    V->>CX: Posta: "Target keyword:<br/>X vs Y — 2.4k/mes"

    Note over H,CX: DIA 1-2

    Note over F: Heartbeat :10 — Fury acorda
    F->>CX: Ve atividade no feed
    F->>F: Pesquisa G2 reviews<br/>Pricing, reclamacoes
    F->>CX: Posta: "Recibos: 73% reclamam<br/>de pricing no G2"

    Note over SH: Heartbeat :02 — Shuri acorda
    SH->>CX: Ve atividade no feed
    SH->>SH: Testa UX do concorrente<br/>Encontra falha de onboarding
    SH->>CX: Posta: "UX Issue: Concorrente<br/>exige 5 cliques para setup"

    Note over H,CX: DIA 2

    Note over L: Heartbeat :06 — Loki acorda
    L->>CX: Le toda a thread
    Note over L: Tem: Keywords (Vision)<br/>+ Provas (Fury)<br/>+ Prints UX (Shuri)
    L->>L: Escreve draft completo
    L->>CX: Posta draft como document
    L->>CX: Move task para REVIEW

    Note over H,CX: DIA 3

    H->>CX: Recebe alerta standup
    H->>CX: Revisa draft, da feedback
    L->>CX: Revisa conforme feedback
    L->>CX: Move task para DONE

    Note over H,CX: Resultado: Entrega composta<br/>por 4 especialistas<br/>enquanto Igor fazia outra coisa
```

---

## 11. Hierarquia do Squad e Niveis de Autonomia

```mermaid
graph TB
    subgraph LEAD["NIVEL: LEAD"]
        J["Jarvis<br/>Squad Lead<br/>━━━━━━━━━━━<br/>Autonomia total<br/>Delega subtarefas<br/>Decide prioridades<br/>Interface com humano"]
    end

    subgraph SPECIALIST["NIVEL: SPECIALIST"]
        V2["Vision<br/>SEO"]
        L2["Loki<br/>Writer"]
        F2["Fury<br/>Research"]
        SH2["Shuri<br/>Tester"]
        Q2["Quill<br/>Social"]
        P2["Pepper<br/>Email"]
        FR2["Friday<br/>Dev"]
    end

    subgraph INTERN["NIVEL: INTERN"]
        W2["Wanda<br/>Designer"]
        WO2["Wong<br/>Docs"]
    end

    IGOR(["HUMANO<br/>(Igor)"])

    IGOR -->|"comandos<br/>aprovacoes<br/>feedback"| J
    J -->|"delega<br/>coordena<br/>monitora"| SPECIALIST
    J -->|"supervisiona<br/>aprova acoes"| INTERN
    SPECIALIST -->|"contribuicoes<br/>espontaneas"| SPECIALIST

    style LEAD fill:#e74c3c,color:#fff
    style SPECIALIST fill:#3498db,color:#fff
    style INTERN fill:#95a5a6,color:#fff
```

---

## 12. Estrategia de Modelos e Custos

```mermaid
graph LR
    subgraph BARATOS["MODELOS BARATOS<br/>(Heartbeats / Rotina)"]
        M1["GPT-4o mini"]
        M2["Claude Haiku"]
        M3["Gemini Flash"]
        M4["Groq"]
    end

    subgraph CAROS["MODELOS FRONTEIRA<br/>(Execucao Complexa)"]
        M5["Claude Opus"]
        M6["GPT-4o"]
        M7["Gemini Pro"]
    end

    subgraph TAREFAS_BARATAS["TAREFAS ROTINA"]
        T1["Heartbeat check"]
        T2["Verificar mencoes"]
        T3["Checagem sim/nao"]
        T4["Reportar status"]
    end

    subgraph TAREFAS_CARAS["TAREFAS COMPLEXAS"]
        T5["Escrever conteudo"]
        T6["Analise estrategica"]
        T7["Codigo/Debug"]
        T8["Pesquisa profunda"]
    end

    BARATOS --> TAREFAS_BARATAS
    CAROS --> TAREFAS_CARAS

    CUSTO["CUSTO TOTAL<br/>$700-800 USD/mes<br/>~R$4.000-5.000<br/>para 10 agentes"]

    TAREFAS_BARATAS --> CUSTO
    TAREFAS_CARAS --> CUSTO

    style BARATOS fill:#2ecc71,color:#fff
    style CAROS fill:#e74c3c,color:#fff
```

---

## 13. Roadmap de Implantacao (5 Fases)

```mermaid
flowchart LR
    subgraph F1["FASE 1<br/>SETUP BASE"]
        F1A["Instalar OpenClaw"]
        F1B["Gateway via pm2"]
        F1C["Chaves API"]
        F1A --> F1B --> F1C
    end

    subgraph F2["FASE 2<br/>NUCLEO"]
        F2A["Jarvis (Lead)"]
        F2B["+ 1 Especialista"]
        F2C["Conectar Telegram"]
        F2A --> F2B --> F2C
    end

    subgraph F3["FASE 3<br/>IDENTIDADE"]
        F3A["SOUL.md por agente"]
        F3B["AGENTS.md compartilhado"]
        F3C["HEARTBEAT.md"]
        F3A --> F3B --> F3C
    end

    subgraph F4["FASE 4<br/>MISSION CONTROL"]
        F4A["Convex DB 6 tabelas"]
        F4B["Sistema de mencoes"]
        F4C["Dashboard React"]
        F4A --> F4B --> F4C
    end

    subgraph F5["FASE 5<br/>ACCOUNTABILITY"]
        F5A["Daily Standup 23:30"]
        F5B["Thread Subscriptions"]
        F5C["Escalar para 10 agentes"]
        F5A --> F5B --> F5C
    end

    F1 --> F2 --> F3 --> F4 --> F5

    style F1 fill:#3498db,color:#fff
    style F2 fill:#2ecc71,color:#fff
    style F3 fill:#e67e22,color:#fff
    style F4 fill:#9b59b6,color:#fff
    style F5 fill:#e74c3c,color:#fff
```

---

## 14. Daily Standup — Fluxo de Compilacao

```mermaid
flowchart TD
    CRON_STANDUP(["CRON 23:30<br/>Daily Standup"])

    CRON_STANDUP --> SCAN

    subgraph SCAN["COLETA DE DADOS"]
        SC1["Busca activities<br/>do dia no Convex"]
        SC2["Busca tasks por status"]
        SC3["Busca agent status"]
        SC4["Identifica decisions<br/>nos comments"]
    end

    SCAN --> COMPILE

    subgraph COMPILE["COMPILACAO"]
        direction TB
        C1["COMPLETAS HOJE<br/>Loki: Blog post 2100 palavras<br/>Quill: 10 tweets drafted"]
        C2["EM PROGRESSO<br/>Vision: SEO strategy<br/>Pepper: Email sequence 3/5"]
        C3["BLOQUEADAS<br/>Wanda: Esperando brand colors"]
        C4["NEEDS REVIEW<br/>Loki: blog post<br/>Pepper: email sequence"]
        C5["DECISOES-CHAVE<br/>Liderar com transparencia de pricing"]
    end

    COMPILE --> SEND

    SEND["Envia sumario formatado<br/>para Telegram do Igor"]

    SEND --> IGOR_REVIEW(["Igor le no celular<br/>Decide proximos passos"])
```

---

## 15. Comunicacao Entre Agentes (2 Canais)

```mermaid
graph TB
    subgraph CANAL1["CANAL 1: MENSAGEM DIRETA<br/>(sessao a sessao)"]
        A1["Jarvis"] -->|"clawdbot sessions send<br/>--session agent:seo-analyst:main<br/>--message 'Review this'"| A2["Vision"]
        NOTE1["Uso: comandos urgentes<br/>do Lead para agente especifico"]
    end

    subgraph CANAL2["CANAL 2: MISSION CONTROL<br/>(via Convex DB — PRINCIPAL)"]
        B1["Fury posta<br/>comment na task"]
        B2["Convex DB<br/>armazena"]
        B3["Notification Daemon<br/>detecta @mentions"]
        B4["Todos inscritos<br/>na thread recebem"]

        B1 --> B2
        B2 --> B3
        B3 --> B4

        NOTE2["Uso: 95% da comunicacao<br/>Cria historico auditavel<br/>Visivel no Dashboard"]
    end

    style CANAL1 fill:#f39c12,color:#fff
    style CANAL2 fill:#2ecc71,color:#fff
```

---

## 16. Fluxo de Roteamento do Gateway

```mermaid
flowchart TD
    subgraph ENTRADA["ENTRADA"]
        TG2["Telegram"]
        DC["Discord"]
        SL["Slack"]
        WA2["WhatsApp"]
        WS["WebSocket API"]
    end

    GW2["GATEWAY<br/>(processo central 24/7)"]

    TG2 --> GW2
    DC --> GW2
    SL --> GW2
    WA2 --> GW2
    WS --> GW2

    GW2 --> ROUTE{"ROTEAMENTO<br/>por config/session key"}

    ROUTE -->|"msg para main"| S_J["Sessao Jarvis<br/>agent:main:main"]
    ROUTE -->|"msg para seo"| S_V["Sessao Vision<br/>agent:seo-analyst:main"]
    ROUTE -->|"cron heartbeat"| S_ANY["Sessao Isolated<br/>(cria, executa, morre)"]
    ROUTE -->|"notification delivery"| S_TARGET["Sessao do agente<br/>mencionado"]

    S_J --> RESP["Resposta"]
    S_V --> RESP
    S_ANY --> RESP
    S_TARGET --> RESP

    RESP --> GW2
    GW2 --> ENTRADA
```

---

*16 diagramas Mermaid cobrindo toda a arquitetura proposta.*
*Renderizar com qualquer visualizador Mermaid (VS Code, GitHub, Notion, mermaid.live)*
