"""
Colmeia v6 — Modulo de Acesso ao Banco de Dados
Banco: SQLite com WAL mode
Uso: importar como modulo ou via cli.py
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "colmeia.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


def get_connection():
    """Retorna conexao com WAL mode e foreign keys habilitados."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def inicializar_banco():
    """Cria tabelas se nao existem."""
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    _aplicar_migracoes_runtime(conn)
    conn.close()


def _agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _colunas_tabela(conn, tabela):
    rows = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return {r["name"] for r in rows}


def _aplicar_migracoes_runtime(conn):
    """Migra banco existente sem apagar dados."""
    cols = _colunas_tabela(conn, "notificacoes")
    alteracoes = [
        ("tentativas_entrega", "INTEGER DEFAULT 0"),
        ("max_tentativas", "INTEGER DEFAULT 3"),
        ("proxima_tentativa_em", "TEXT"),
        ("ultimo_erro", "TEXT"),
        ("entregue_em", "TEXT"),
        ("entregue_por", "TEXT"),
    ]
    for col, ddl in alteracoes:
        if col not in cols:
            conn.execute(f"ALTER TABLE notificacoes ADD COLUMN {col} {ddl}")

    conn.execute(
        """CREATE TABLE IF NOT EXISTS subscriptions_tarefa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa_id INTEGER NOT NULL REFERENCES tarefas(id),
            agente_id TEXT NOT NULL REFERENCES agentes(id),
            origem TEXT DEFAULT 'manual',
            ativo INTEGER DEFAULT 1,
            criado_em TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(tarefa_id, agente_id)
        )"""
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_tarefa ON subscriptions_tarefa(tarefa_id, ativo)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_agente ON subscriptions_tarefa(agente_id, ativo)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_notificacoes_retry ON notificacoes(entregue, proxima_tentativa_em, tentativas_entrega)")
    conn.commit()


# === AGENTES ===

def registrar_agente(id, nome, papel, plataforma, automatizado=False):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO agentes (id, nome, papel, plataforma, automatizado, atualizado_em) VALUES (?, ?, ?, ?, ?, ?)",
        (id, nome, papel, plataforma, int(automatizado), _agora())
    )
    conn.commit()
    conn.close()


def listar_agentes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM agentes ORDER BY nome").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def atualizar_status_agente(id, status):
    conn = get_connection()
    conn.execute(
        "UPDATE agentes SET status = ?, atualizado_em = ? WHERE id = ?",
        (status, _agora(), id)
    )
    conn.commit()
    conn.close()


def heartbeat(agente_id):
    """Registra heartbeat de um agente."""
    agora = _agora()
    conn = get_connection()
    conn.execute(
        "UPDATE agentes SET ultimo_heartbeat = ?, atualizado_em = ? WHERE id = ?",
        (agora, agora, agente_id)
    )
    conn.execute(
        "INSERT INTO atividades (tipo, agente_id, descricao, criado_em) VALUES (?, ?, ?, ?)",
        ("heartbeat", agente_id, f"Heartbeat de {agente_id}", agora)
    )
    conn.commit()
    conn.close()
    return agora


# === TAREFAS ===

def _agente_existe(conn, agente_id):
    """Verifica se um agente existe no banco."""
    if not agente_id:
        return False
    row = conn.execute("SELECT 1 FROM agentes WHERE id = ?", (agente_id,)).fetchone()
    return row is not None


def criar_tarefa(titulo, descricao=None, criado_por=None, prioridade=5, projeto=None, tags=None):
    conn = get_connection()
    agora = _agora()
    tags_json = json.dumps(tags) if tags else None
    cursor = conn.execute(
        """INSERT INTO tarefas (titulo, descricao, criado_por, prioridade, projeto, tags, criado_em, atualizado_em)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (titulo, descricao, criado_por, prioridade, projeto, tags_json, agora, agora)
    )
    tarefa_id = cursor.lastrowid
    # Se criado_por nao e um agente (ex: igor/humano), nao referenciar como agente_id
    agente_id = criado_por if _agente_existe(conn, criado_por) else None
    conn.execute(
        "INSERT INTO atividades (tipo, agente_id, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?)",
        ("tarefa_criada", agente_id, f"Tarefa criada por {criado_por or 'sistema'}: {titulo}", str(tarefa_id), agora)
    )
    conn.commit()
    conn.close()
    return tarefa_id


def atribuir_tarefa(tarefa_id, responsavel_id):
    conn = get_connection()
    agora = _agora()
    conn.execute(
        "UPDATE tarefas SET responsavel_id = ?, status = 'atribuida', atualizado_em = ? WHERE id = ?",
        (responsavel_id, agora, tarefa_id)
    )
    conn.execute(
        "INSERT INTO notificacoes (para_agente, conteudo, tipo, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?)",
        (responsavel_id, f"Tarefa #{tarefa_id} atribuida a voce", "atribuicao", str(tarefa_id), agora)
    )
    registrar_subscription(tarefa_id, responsavel_id, origem="atribuicao", conn=conn)
    conn.execute(
        "INSERT INTO atividades (tipo, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?)",
        ("tarefa_atualizada", f"Tarefa #{tarefa_id} atribuida a {responsavel_id}", str(tarefa_id), agora)
    )
    conn.commit()
    conn.close()


def atualizar_tarefa(tarefa_id, status=None, prioridade=None, bloqueada_por=None):
    conn = get_connection()
    agora = _agora()
    updates = ["atualizado_em = ?"]
    params = [agora]

    if status:
        updates.append("status = ?")
        params.append(status)
    if prioridade is not None:
        updates.append("prioridade = ?")
        params.append(prioridade)
    if bloqueada_por is not None:
        updates.append("bloqueada_por = ?")
        params.append(bloqueada_por)

    params.append(tarefa_id)
    conn.execute(f"UPDATE tarefas SET {', '.join(updates)} WHERE id = ?", params)

    if status:
        conn.execute(
            "INSERT INTO atividades (tipo, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?)",
            ("tarefa_atualizada", f"Tarefa #{tarefa_id} >> {status}", str(tarefa_id), agora)
        )

    conn.commit()
    conn.close()


def listar_tarefas(status=None, responsavel=None, projeto=None):
    conn = get_connection()
    query = "SELECT * FROM tarefas WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if responsavel:
        query += " AND responsavel_id = ?"
        params.append(responsavel)
    if projeto:
        query += " AND projeto = ?"
        params.append(projeto)

    query += " ORDER BY prioridade DESC, criado_em DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obter_tarefa(tarefa_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# === MENSAGENS ===

def criar_mensagem(tarefa_id, de_agente, conteudo, mencoes=None):
    conn = get_connection()
    agora = _agora()
    mencoes_json = json.dumps(mencoes) if mencoes else None
    conn.execute(
        "INSERT INTO mensagens (tarefa_id, de_agente, conteudo, mencoes, criado_em) VALUES (?, ?, ?, ?, ?)",
        (tarefa_id, de_agente, conteudo, mencoes_json, agora)
    )
    conn.execute(
        "INSERT INTO atividades (tipo, agente_id, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?)",
        ("mensagem_enviada", de_agente, f"Mensagem em tarefa #{tarefa_id}", str(tarefa_id), agora)
    )

    # Auto-subscription dos participantes da thread.
    registrar_subscription(tarefa_id, de_agente, origem="autor_mensagem", conn=conn)
    tarefa = conn.execute("SELECT responsavel_id, criado_por FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if tarefa:
        if tarefa["responsavel_id"]:
            registrar_subscription(tarefa_id, tarefa["responsavel_id"], origem="responsavel", conn=conn)
        if tarefa["criado_por"] and _agente_existe(conn, tarefa["criado_por"]):
            registrar_subscription(tarefa_id, tarefa["criado_por"], origem="criador", conn=conn)

    # Criar notificacoes para mencoes
    mencionados = set()
    if mencoes:
        for agente in mencoes:
            mencionado = agente.strip()
            if not mencionado:
                continue
            mencionados.add(mencionado)
            registrar_subscription(tarefa_id, mencionado, origem="mencao", conn=conn)
            conn.execute(
                "INSERT INTO notificacoes (para_agente, de_agente, conteudo, tipo, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?, ?)",
                (mencionado, de_agente, f"@{mencionado} mencionado em tarefa #{tarefa_id}", "mencao", str(tarefa_id), agora)
            )

    inscritos = listar_subscriptions(tarefa_id=tarefa_id, apenas_ativos=True, conn=conn)
    for s in inscritos:
        destino = s["agente_id"]
        if destino == de_agente or destino in mencionados:
            continue
        conn.execute(
            "INSERT INTO notificacoes (para_agente, de_agente, conteudo, tipo, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?, ?)",
            (destino, de_agente, f"Nova mensagem na tarefa #{tarefa_id}", "sistema", str(tarefa_id), agora)
        )

    conn.commit()
    conn.close()


def listar_mensagens(tarefa_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM mensagens WHERE tarefa_id = ? ORDER BY criado_em ASC",
        (tarefa_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# === ATIVIDADES ===

def registrar_atividade(tipo, agente_id=None, descricao=None, referencia_id=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO atividades (tipo, agente_id, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?)",
        (tipo, agente_id, descricao, referencia_id, _agora())
    )
    conn.commit()
    conn.close()


def listar_atividades(tipo=None, agente_id=None, desde=None, limite=50):
    conn = get_connection()
    query = "SELECT * FROM atividades WHERE 1=1"
    params = []

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)
    if agente_id:
        query += " AND agente_id = ?"
        params.append(agente_id)
    if desde:
        query += " AND criado_em >= ?"
        params.append(desde)

    query += " ORDER BY criado_em DESC LIMIT ?"
    params.append(limite)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# === DOCUMENTOS ===

def criar_documento(titulo, tipo, autor_id=None, conteudo=None, tarefa_id=None, caminho_arquivo=None):
    conn = get_connection()
    agora = _agora()
    # Validar autor_id contra tabela de agentes (FK)
    autor_valido = autor_id if _agente_existe(conn, autor_id) else None
    cursor = conn.execute(
        """INSERT INTO documentos (titulo, conteudo, tipo, tarefa_id, autor_id, caminho_arquivo, criado_em)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (titulo, conteudo, tipo, tarefa_id, autor_valido, caminho_arquivo, agora)
    )
    doc_id = cursor.lastrowid
    conn.execute(
        "INSERT INTO atividades (tipo, agente_id, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?)",
        ("documento_criado", autor_valido, f"Documento criado: {titulo}" + (f" (autor original: {autor_id})" if autor_id != autor_valido else ""), str(doc_id), agora)
    )
    conn.commit()
    conn.close()
    return doc_id


def listar_documentos(tipo=None, autor_id=None):
    conn = get_connection()
    query = "SELECT * FROM documentos WHERE 1=1"
    params = []

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)
    if autor_id:
        query += " AND autor_id = ?"
        params.append(autor_id)

    query += " ORDER BY criado_em DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# === NOTIFICACOES ===

def listar_notificacoes(para_agente, apenas_pendentes=True):
    conn = get_connection()
    query = "SELECT * FROM notificacoes WHERE para_agente = ?"
    params = [para_agente]

    if apenas_pendentes:
        query += " AND entregue = 0"

    query += " ORDER BY criado_em DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def marcar_notificacao_entregue(notificacao_id, entregue_por="manual"):
    conn = get_connection()
    conn.execute(
        """UPDATE notificacoes
           SET entregue = 1,
               entregue_em = ?,
               entregue_por = ?,
               proxima_tentativa_em = NULL
           WHERE id = ?""",
        (_agora(), entregue_por, notificacao_id),
    )
    conn.commit()
    conn.close()


def marcar_todas_entregues(para_agente):
    conn = get_connection()
    conn.execute(
        """UPDATE notificacoes
           SET entregue = 1,
               entregue_em = ?,
               entregue_por = ?,
               proxima_tentativa_em = NULL
           WHERE para_agente = ? AND entregue = 0""",
        (_agora(), "manual_lote", para_agente),
    )
    conn.commit()
    conn.close()


def listar_notificacoes_para_entrega(limite=100, agora=None, ignorar_agendamento=False):
    conn = get_connection()
    agora = agora or _agora()
    if ignorar_agendamento:
        rows = conn.execute(
            """SELECT * FROM notificacoes
               WHERE entregue = 0
                 AND tentativas_entrega < max_tentativas
               ORDER BY criado_em ASC
               LIMIT ?""",
            (limite,),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT * FROM notificacoes
               WHERE entregue = 0
                 AND tentativas_entrega < max_tentativas
                 AND (proxima_tentativa_em IS NULL OR proxima_tentativa_em <= ?)
               ORDER BY criado_em ASC
               LIMIT ?""",
            (agora, limite),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def registrar_tentativa_entrega(
    notificacao_id,
    sucesso,
    entregue_por="daemon",
    erro=None,
    retry_delay_min=30,
):
    conn = get_connection()
    atual = conn.execute(
        "SELECT tentativas_entrega, max_tentativas FROM notificacoes WHERE id = ?",
        (notificacao_id,),
    ).fetchone()
    if not atual:
        conn.close()
        return {"ok": False, "motivo": "notificacao_nao_encontrada"}

    tentativas = (atual["tentativas_entrega"] or 0) + 1
    max_tentativas = atual["max_tentativas"] or 3
    if sucesso:
        conn.execute(
            """UPDATE notificacoes
               SET entregue = 1,
                   tentativas_entrega = ?,
                   entregue_em = ?,
                   entregue_por = ?,
                   ultimo_erro = NULL,
                   proxima_tentativa_em = NULL
               WHERE id = ?""",
            (tentativas, _agora(), entregue_por, notificacao_id),
        )
        conn.execute(
            "INSERT INTO atividades (tipo, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?)",
            ("sistema", f"Notificacao #{notificacao_id} entregue por {entregue_por}", str(notificacao_id), _agora()),
        )
        conn.commit()
        conn.close()
        return {"ok": True, "status": "entregue", "tentativas": tentativas}

    if tentativas >= max_tentativas:
        conn.execute(
            """UPDATE notificacoes
               SET tentativas_entrega = ?,
                   ultimo_erro = ?,
                   proxima_tentativa_em = NULL
               WHERE id = ?""",
            (tentativas, erro or "falha", notificacao_id),
        )
        conn.execute(
            "INSERT INTO atividades (tipo, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?)",
            ("erro", f"Notificacao #{notificacao_id} excedeu max_tentativas", str(notificacao_id), _agora()),
        )
        conn.commit()
        conn.close()
        return {"ok": False, "status": "falha_final", "tentativas": tentativas}

    proxima = datetime.now().timestamp() + (retry_delay_min * 60)
    proxima_str = datetime.fromtimestamp(proxima).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """UPDATE notificacoes
           SET tentativas_entrega = ?,
               ultimo_erro = ?,
               proxima_tentativa_em = ?
           WHERE id = ?""",
        (tentativas, erro or "falha", proxima_str, notificacao_id),
    )
    conn.execute(
        "INSERT INTO atividades (tipo, descricao, referencia_id, criado_em) VALUES (?, ?, ?, ?)",
        ("sistema", f"Notificacao #{notificacao_id} reprogramada para {proxima_str}", str(notificacao_id), _agora()),
    )
    conn.commit()
    conn.close()
    return {"ok": False, "status": "reprogramada", "tentativas": tentativas, "proxima_tentativa_em": proxima_str}


# === SCANNER DE URGENCIA ===

def scanner_urgencia(agente_id):
    """Retorna itens urgentes para um agente, priorizados.
    Ordem: mencoes pendentes > tarefas em_progresso > tarefas atribuidas > tarefas alta prioridade na caixa.
    """
    conn = get_connection()
    resultado = {
        "mencoes": [],
        "em_progresso": [],
        "atribuidas": [],
        "urgentes_caixa": [],
    }

    # Mencoes pendentes
    resultado["mencoes"] = [dict(r) for r in conn.execute(
        "SELECT * FROM notificacoes WHERE para_agente = ? AND entregue = 0 ORDER BY criado_em ASC",
        (agente_id,)
    ).fetchall()]

    # Tarefas em progresso do agente
    resultado["em_progresso"] = [dict(r) for r in conn.execute(
        "SELECT * FROM tarefas WHERE responsavel_id = ? AND status = 'em_progresso' ORDER BY prioridade DESC",
        (agente_id,)
    ).fetchall()]

    # Tarefas atribuidas ao agente
    resultado["atribuidas"] = [dict(r) for r in conn.execute(
        "SELECT * FROM tarefas WHERE responsavel_id = ? AND status = 'atribuida' ORDER BY prioridade DESC",
        (agente_id,)
    ).fetchall()]

    # Tarefas urgentes na caixa de entrada (prioridade >= 8, sem dono)
    resultado["urgentes_caixa"] = [dict(r) for r in conn.execute(
        "SELECT * FROM tarefas WHERE status = 'caixa_entrada' AND responsavel_id IS NULL AND prioridade >= 8 ORDER BY prioridade DESC",
    ).fetchall()]

    conn.close()
    return resultado


def gerar_dashboard():
    """Retorna dados consolidados para o dashboard."""
    conn = get_connection()

    # Contagem por status
    contagem_status = {}
    for row in conn.execute("SELECT status, COUNT(*) as total FROM tarefas GROUP BY status").fetchall():
        contagem_status[row["status"]] = row["total"]

    # Agentes ativos (com heartbeat nas ultimas 2 horas)
    agentes = [dict(r) for r in conn.execute("SELECT * FROM agentes ORDER BY nome").fetchall()]

    # Ultimas 20 atividades
    atividades = [dict(r) for r in conn.execute(
        "SELECT * FROM atividades ORDER BY criado_em DESC LIMIT 20"
    ).fetchall()]

    # Bloqueios abertos
    bloqueios = [dict(r) for r in conn.execute(
        "SELECT * FROM tarefas WHERE status = 'bloqueada'"
    ).fetchall()]

    conn.close()

    return {
        "contagem_status": contagem_status,
        "agentes": agentes,
        "atividades_recentes": atividades,
        "bloqueios": bloqueios,
        "total_tarefas": sum(contagem_status.values()) if contagem_status else 0,
    }


def criar_notificacao(para_agente, conteudo, tipo="sistema", de_agente=None, referencia_id=None):
    """Cria uma notificacao para um agente."""
    conn = get_connection()
    agora = _agora()
    conn.execute(
        "INSERT INTO notificacoes (para_agente, de_agente, conteudo, tipo, referencia_id, criado_em) VALUES (?, ?, ?, ?, ?, ?)",
        (para_agente, de_agente, conteudo, tipo, referencia_id, agora)
    )
    conn.commit()
    conn.close()


def contar_notificacoes_pendentes(para_agente):
    """Conta notificacoes nao entregues."""
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as total FROM notificacoes WHERE para_agente = ? AND entregue = 0",
        (para_agente,)
    ).fetchone()
    conn.close()
    return row["total"]


# === SUBSCRIPTIONS ===

def registrar_subscription(tarefa_id, agente_id, origem="manual", conn=None):
    if not agente_id:
        return False
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    conn.execute(
        """INSERT INTO subscriptions_tarefa (tarefa_id, agente_id, origem, ativo, criado_em)
           VALUES (?, ?, ?, 1, ?)
           ON CONFLICT(tarefa_id, agente_id) DO UPDATE SET ativo = 1""",
        (tarefa_id, agente_id, origem, _agora()),
    )

    if close_conn:
        conn.commit()
        conn.close()
    return True


def listar_subscriptions(tarefa_id=None, agente_id=None, apenas_ativos=True, conn=None):
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    query = "SELECT * FROM subscriptions_tarefa WHERE 1=1"
    params = []
    if tarefa_id is not None:
        query += " AND tarefa_id = ?"
        params.append(tarefa_id)
    if agente_id:
        query += " AND agente_id = ?"
        params.append(agente_id)
    if apenas_ativos:
        query += " AND ativo = 1"
    query += " ORDER BY criado_em ASC"

    rows = conn.execute(query, params).fetchall()
    if close_conn:
        conn.close()
    return [dict(r) for r in rows]


def obter_agentes_online(janela_min=90):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, ultimo_heartbeat FROM agentes WHERE ultimo_heartbeat IS NOT NULL"
    ).fetchall()
    conn.close()

    limite = datetime.now().timestamp() - (janela_min * 60)
    ativos = []
    for r in rows:
        try:
            ts = datetime.strptime(r["ultimo_heartbeat"], "%Y-%m-%d %H:%M:%S").timestamp()
            if ts >= limite:
                ativos.append(r["id"])
        except ValueError:
            continue
    return ativos


def processar_fila_notificacoes(
    agentes_online=None,
    limite=100,
    retry_delay_min=30,
    entregador="daemon",
    ignorar_agendamento=False,
):
    pendentes = listar_notificacoes_para_entrega(limite=limite, ignorar_agendamento=ignorar_agendamento)
    stats = {
        "total": len(pendentes),
        "entregues": 0,
        "reprogramadas": 0,
        "falhas_finais": 0,
        "ignoradas": 0,
    }

    online_set = set(agentes_online) if agentes_online is not None else None

    for n in pendentes:
        destino = n["para_agente"]
        if online_set is not None and destino not in online_set:
            r = registrar_tentativa_entrega(
                n["id"],
                sucesso=False,
                entregue_por=entregador,
                erro="agente_offline",
                retry_delay_min=retry_delay_min,
            )
        else:
            r = registrar_tentativa_entrega(
                n["id"],
                sucesso=True,
                entregue_por=entregador,
            )

        status = r.get("status")
        if status == "entregue":
            stats["entregues"] += 1
        elif status == "reprogramada":
            stats["reprogramadas"] += 1
        elif status == "falha_final":
            stats["falhas_finais"] += 1
        else:
            stats["ignoradas"] += 1

    return stats


# === STANDUP ===

def gerar_standup(data=None):
    """Gera resumo do standup para uma data (default: hoje)."""
    if not data:
        data = datetime.now().strftime("%Y-%m-%d")

    desde = f"{data} 00:00:00"
    ate = f"{data} 23:59:59"

    conn = get_connection()

    concluidas = conn.execute(
        "SELECT * FROM tarefas WHERE status = 'concluida' AND atualizado_em BETWEEN ? AND ?",
        (desde, ate)
    ).fetchall()

    em_progresso = conn.execute(
        "SELECT * FROM tarefas WHERE status = 'em_progresso'"
    ).fetchall()

    bloqueadas = conn.execute(
        "SELECT * FROM tarefas WHERE status = 'bloqueada'"
    ).fetchall()

    revisao = conn.execute(
        "SELECT * FROM tarefas WHERE status = 'revisao'"
    ).fetchall()

    heartbeats = conn.execute(
        "SELECT agente_id, COUNT(*) as total FROM atividades WHERE tipo = 'heartbeat' AND criado_em BETWEEN ? AND ? GROUP BY agente_id",
        (desde, ate)
    ).fetchall()

    conn.close()

    return {
        "data": data,
        "concluidas": [dict(r) for r in concluidas],
        "em_progresso": [dict(r) for r in em_progresso],
        "bloqueadas": [dict(r) for r in bloqueadas],
        "revisao": [dict(r) for r in revisao],
        "heartbeats": {r["agente_id"]: r["total"] for r in heartbeats}
    }


# === EXPORTACAO ===

def exportar_para_json(caminho=None):
    """Exporta banco completo para JSON (backup)."""
    if not caminho:
        caminho = DB_DIR / "backup" / f"colmeia_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    conn = get_connection()
    dados = {
        "exportado_em": _agora(),
        "agentes": [dict(r) for r in conn.execute("SELECT * FROM agentes").fetchall()],
        "tarefas": [dict(r) for r in conn.execute("SELECT * FROM tarefas").fetchall()],
        "mensagens": [dict(r) for r in conn.execute("SELECT * FROM mensagens").fetchall()],
        "atividades": [dict(r) for r in conn.execute("SELECT * FROM atividades ORDER BY id DESC LIMIT 1000").fetchall()],
        "documentos": [dict(r) for r in conn.execute("SELECT * FROM documentos").fetchall()],
        "notificacoes": [dict(r) for r in conn.execute("SELECT * FROM notificacoes").fetchall()],
    }
    conn.close()

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return str(caminho)


# Inicializar banco ao importar
if not DB_PATH.exists():
    inicializar_banco()
else:
    conn = get_connection()
    _aplicar_migracoes_runtime(conn)
    conn.close()
