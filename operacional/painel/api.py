"""
Colmeia v6 — API do Dashboard (FastAPI)
Uso: uvicorn api:app --host 0.0.0.0 --port 8765
Ou: python api.py (modo desenvolvimento)
"""

import sys
import os

# Adicionar diretorio do banco ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "banco"))

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
import colmeia_db as db

app = FastAPI(title="Colmeia v6 — Dashboard API", version="1.0")


@app.on_event("startup")
def startup():
    db.inicializar_banco()


# === AGENTES ===

@app.get("/api/agentes")
def api_agentes():
    return db.listar_agentes()


# === TAREFAS ===

@app.get("/api/tarefas")
def api_tarefas(
    status: Optional[str] = None,
    responsavel: Optional[str] = None,
    projeto: Optional[str] = None,
):
    return db.listar_tarefas(status=status, responsavel=responsavel, projeto=projeto)


@app.get("/api/tarefas/{tarefa_id}")
def api_tarefa(tarefa_id: int):
    tarefa = db.obter_tarefa(tarefa_id)
    if not tarefa:
        return {"erro": "Tarefa nao encontrada"}
    tarefa["mensagens"] = db.listar_mensagens(tarefa_id)
    return tarefa


@app.post("/api/tarefas")
def api_criar_tarefa(
    titulo: str,
    descricao: Optional[str] = None,
    responsavel: Optional[str] = None,
    prioridade: int = 5,
    projeto: Optional[str] = None,
):
    tarefa_id = db.criar_tarefa(
        titulo=titulo,
        descricao=descricao,
        criado_por="igor",
        prioridade=prioridade,
        projeto=projeto,
    )
    if responsavel:
        db.atribuir_tarefa(tarefa_id, responsavel)
    return {"id": tarefa_id, "titulo": titulo}


# === ATIVIDADES ===

@app.get("/api/atividades")
def api_atividades(
    tipo: Optional[str] = None,
    agente: Optional[str] = None,
    desde: Optional[str] = None,
    limite: int = 50,
):
    return db.listar_atividades(tipo=tipo, agente_id=agente, desde=desde, limite=limite)


# === STANDUP ===

@app.get("/api/standup")
def api_standup(data: Optional[str] = None):
    return db.gerar_standup(data)


# === NOTIFICACOES ===

@app.get("/api/notificacoes/{agente_id}")
def api_notificacoes(agente_id: str, todas: bool = False):
    return db.listar_notificacoes(agente_id, apenas_pendentes=not todas)


@app.post("/api/notificacoes/processar")
def api_processar_notificacoes(modo: str = "online", limite: int = 100, retry_delay_min: int = 30, janela_online_min: int = 90):
    agentes_online = None
    if modo == "online":
        agentes_online = db.obter_agentes_online(janela_min=janela_online_min)
    return db.processar_fila_notificacoes(
        agentes_online=agentes_online,
        limite=limite,
        retry_delay_min=retry_delay_min,
        entregador=f"api_{modo}",
        ignorar_agendamento=(modo == "all"),
    )


@app.get("/api/subscriptions")
def api_subscriptions(tarefa_id: Optional[int] = None, agente: Optional[str] = None, incluir_inativos: bool = False):
    return db.listar_subscriptions(
        tarefa_id=tarefa_id,
        agente_id=agente,
        apenas_ativos=not incluir_inativos,
    )


# === SCANNER / URGENCIA ===

@app.get("/api/scanner/{agente_id}")
def api_scanner(agente_id: str):
    return db.scanner_urgencia(agente_id)


# === DASHBOARD CONSOLIDADO ===

@app.get("/api/dashboard")
def api_dashboard():
    return db.gerar_dashboard()


# === DOCUMENTOS ===

@app.get("/api/documentos")
def api_documentos(tipo: Optional[str] = None, autor: Optional[str] = None):
    return db.listar_documentos(tipo=tipo, autor_id=autor)


# === HEARTBEAT (via API) ===

@app.post("/api/heartbeat/{agente_id}")
def api_heartbeat(agente_id: str):
    ts = db.heartbeat(agente_id)
    return {"agente": agente_id, "timestamp": ts}


# === TAREFAS MUTACAO ===

@app.put("/api/tarefas/{tarefa_id}/status")
def api_atualizar_status(tarefa_id: int, status: str):
    db.atualizar_tarefa(tarefa_id, status=status)
    return {"id": tarefa_id, "status": status}


@app.put("/api/tarefas/{tarefa_id}/assign")
def api_atribuir_tarefa(tarefa_id: int, responsavel: str):
    db.atribuir_tarefa(tarefa_id, responsavel)
    return {"id": tarefa_id, "responsavel": responsavel}


# === MENSAGENS MUTACAO ===

@app.post("/api/tarefas/{tarefa_id}/mensagens")
def api_criar_mensagem(tarefa_id: int, de: str, conteudo: str, mencoes: Optional[str] = None):
    lista_mencoes = mencoes.split(",") if mencoes else None
    db.criar_mensagem(tarefa_id, de, conteudo, lista_mencoes)
    return {"tarefa_id": tarefa_id, "de": de}


# === FRONTEND ===

@app.get("/", response_class=HTMLResponse)
def dashboard():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    print("Colmeia v6 Dashboard: http://localhost:8765")
    uvicorn.run(app, host="0.0.0.0", port=8765)
