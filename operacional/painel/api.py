"""
Colmeia v6 — API do Dashboard (FastAPI)
Uso: uvicorn api:app --host 0.0.0.0 --port 8765
Ou: python api.py (modo desenvolvimento)
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Adicionar diretorio do banco ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "banco"))

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
import colmeia_db as db

LOGS_DIR = Path(__file__).parent.parent / "logs"

app = FastAPI(title="Colmeia v6 — Dashboard API", version="1.0")


@app.on_event("startup")
def startup():
    db.inicializar_banco()


# === HEALTH CHECK ===

@app.get("/api/health")
def api_health():
    """Health check para monitoring (Render, uptime bots, etc.)."""
    try:
        agentes = db.listar_agentes()
        tarefas = db.listar_tarefas()
        return {
            "status": "ok",
            "version": "1.0",
            "agentes": len(agentes),
            "tarefas": len(tarefas),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


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


# === SOAK TEST ===

def _carregar_logs_jsonl(dias=7):
    """Carrega logs JSONL dos ultimos N dias."""
    entradas = []
    hoje = datetime.now()
    for i in range(dias):
        data = (hoje - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"heartbeat_{data}.jsonl"
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entradas.append(json.loads(line))
    return entradas


@app.get("/api/soak-test")
def api_soak_test(dias: int = 7):
    """Retorna KPIs do soak test para monitoramento."""
    entradas = _carregar_logs_jsonl(dias)
    if not entradas:
        return {"status": "sem_dados", "mensagem": "Nenhum log encontrado"}

    total = len(entradas)
    por_agente = defaultdict(list)
    por_resultado = defaultdict(int)
    por_dia = defaultdict(list)

    for e in entradas:
        por_agente[e["agente"]].append(e)
        por_resultado[e["resultado"]] += 1
        dia = e["timestamp"][:10]
        por_dia[dia].append(e)

    sucessos = sum(1 for e in entradas if e["resultado"] != "ERRO")
    taxa_sucesso = round((sucessos / total) * 100, 1)
    duracoes = [e["duracao_ms"] for e in entradas if "duracao_ms" in e]
    duracao_media = round(sum(duracoes) / len(duracoes), 1) if duracoes else 0

    # KPIs por agente
    agentes_stats = {}
    for agente, logs in por_agente.items():
        a_total = len(logs)
        a_sucessos = sum(1 for e in logs if e["resultado"] != "ERRO")
        agentes_stats[agente] = {
            "total": a_total,
            "sucesso": a_sucessos,
            "taxa": round((a_sucessos / a_total * 100), 1) if a_total else 0,
            "trabalho": sum(1 for e in logs if e["resultado"].startswith("TRABALHO")),
        }

    # KPIs por dia
    dias_stats = {}
    for dia, logs in sorted(por_dia.items()):
        d_total = len(logs)
        d_sucesso = sum(1 for e in logs if e["resultado"] != "ERRO")
        dias_stats[dia] = {
            "ciclos": d_total,
            "taxa": round((d_sucesso / d_total * 100), 1) if d_total else 0,
            "agentes_ativos": len(set(e["agente"] for e in logs)),
        }

    timestamps = [e["timestamp"] for e in entradas]
    dias_com_dados = len(por_dia)
    meta_dias = 7
    inicio_soak = "2026-02-11"

    return {
        "status": "em_andamento" if dias_com_dados < meta_dias else "concluido",
        "progresso": f"{dias_com_dados}/{meta_dias} dias",
        "inicio": inicio_soak,
        "fim_previsto": "2026-02-18",
        "periodo": {"primeiro": min(timestamps), "ultimo": max(timestamps)},
        "total_ciclos": total,
        "taxa_sucesso": taxa_sucesso,
        "meta_atingida": taxa_sucesso >= 90,
        "duracao_media_ms": duracao_media,
        "por_resultado": dict(por_resultado),
        "por_agente": agentes_stats,
        "por_dia": dias_stats,
    }


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
