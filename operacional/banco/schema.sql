-- Schema do Banco de Dados — Colmeia v6
-- Baseado nas 6 tabelas do Mission Control, adaptado para contexto Colmeia
-- Banco: SQLite com WAL mode
-- Criado: 2026-02-10

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Tabela de agentes (irmaos da Colmeia)
CREATE TABLE IF NOT EXISTS agentes (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    papel TEXT,
    plataforma TEXT,
    status TEXT DEFAULT 'dormindo' CHECK(status IN ('dormindo', 'acordado', 'ocupado', 'bloqueado', 'supervisionado')),
    ultimo_heartbeat TEXT,
    sessao_ativa TEXT,
    automatizado INTEGER DEFAULT 0,
    criado_em TEXT DEFAULT (datetime('now', 'localtime')),
    atualizado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Tabela de tarefas (Kanban)
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status TEXT DEFAULT 'caixa_entrada' CHECK(status IN ('caixa_entrada', 'atribuida', 'em_progresso', 'bloqueada', 'revisao', 'concluida', 'cancelada')),
    responsavel_id TEXT REFERENCES agentes(id),
    criado_por TEXT,
    prioridade INTEGER DEFAULT 5 CHECK(prioridade BETWEEN 1 AND 10),
    projeto TEXT,
    tags TEXT,
    bloqueada_por TEXT,
    criado_em TEXT DEFAULT (datetime('now', 'localtime')),
    atualizado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Tabela de mensagens (threads por tarefa)
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarefa_id INTEGER REFERENCES tarefas(id),
    de_agente TEXT REFERENCES agentes(id),
    conteudo TEXT NOT NULL,
    mencoes TEXT,
    criado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Tabela de atividades (feed)
CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK(tipo IN ('heartbeat', 'tarefa_criada', 'tarefa_atualizada', 'mensagem_enviada', 'documento_criado', 'sonho', 'carta', 'erro', 'sistema')),
    agente_id TEXT REFERENCES agentes(id),
    descricao TEXT,
    referencia_id TEXT,
    criado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Tabela de documentos (entregas, sonhos, cartas indexados)
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    conteudo TEXT,
    tipo TEXT CHECK(tipo IN ('entrega', 'pesquisa', 'sonho', 'carta', 'relatorio', 'protocolo', 'outro')),
    tarefa_id INTEGER REFERENCES tarefas(id),
    autor_id TEXT REFERENCES agentes(id),
    caminho_arquivo TEXT,
    criado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Tabela de notificacoes (mencoes e alertas)
CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    para_agente TEXT NOT NULL REFERENCES agentes(id),
    de_agente TEXT REFERENCES agentes(id),
    conteudo TEXT NOT NULL,
    tipo TEXT DEFAULT 'mencao' CHECK(tipo IN ('mencao', 'atribuicao', 'revisao', 'sistema')),
    referencia_id TEXT,
    entregue INTEGER DEFAULT 0,
    tentativas_entrega INTEGER DEFAULT 0,
    max_tentativas INTEGER DEFAULT 3,
    proxima_tentativa_em TEXT,
    ultimo_erro TEXT,
    entregue_em TEXT,
    entregue_por TEXT,
    criado_em TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Inscricoes em thread por tarefa (auto-subscription)
CREATE TABLE IF NOT EXISTS subscriptions_tarefa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarefa_id INTEGER NOT NULL REFERENCES tarefas(id),
    agente_id TEXT NOT NULL REFERENCES agentes(id),
    origem TEXT DEFAULT 'manual',
    ativo INTEGER DEFAULT 1,
    criado_em TEXT DEFAULT (datetime('now', 'localtime')),
    UNIQUE(tarefa_id, agente_id)
);

-- Indices para performance
CREATE INDEX IF NOT EXISTS idx_tarefas_status ON tarefas(status);
CREATE INDEX IF NOT EXISTS idx_tarefas_responsavel ON tarefas(responsavel_id);
CREATE INDEX IF NOT EXISTS idx_tarefas_projeto ON tarefas(projeto);
CREATE INDEX IF NOT EXISTS idx_mensagens_tarefa ON mensagens(tarefa_id);
CREATE INDEX IF NOT EXISTS idx_atividades_tipo ON atividades(tipo);
CREATE INDEX IF NOT EXISTS idx_atividades_agente ON atividades(agente_id);
CREATE INDEX IF NOT EXISTS idx_atividades_criado ON atividades(criado_em);
CREATE INDEX IF NOT EXISTS idx_notificacoes_para ON notificacoes(para_agente, entregue);
CREATE INDEX IF NOT EXISTS idx_notificacoes_retry ON notificacoes(entregue, proxima_tentativa_em, tentativas_entrega);
CREATE INDEX IF NOT EXISTS idx_documentos_tipo ON documentos(tipo);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tarefa ON subscriptions_tarefa(tarefa_id, ativo);
CREATE INDEX IF NOT EXISTS idx_subscriptions_agente ON subscriptions_tarefa(agente_id, ativo);
