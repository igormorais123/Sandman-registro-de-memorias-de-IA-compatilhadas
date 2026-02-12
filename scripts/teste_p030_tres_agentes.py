#!/usr/bin/env python3
"""
Colmeia v6 - P030
Teste colaborativo com 3 agentes piloto (nexo, onir, sandman).

Fluxo:
1. Cria uma tarefa compartilhada.
2. Atribui para NEXO.
3. Publica mensagem com mencoes para ONIR e SANDMAN.
4. Executa heartbeat dos 3 agentes em paralelo.
5. Gera evidencias em JSON para auditoria.
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BANCO_DIR = REPO_ROOT / "operacional" / "banco"
LOG_DIR = REPO_ROOT / "operacional" / "logs"
HEARTBEAT_RUNNER = BANCO_DIR / "heartbeat_runner.py"

sys.path.insert(0, str(BANCO_DIR))
import colmeia_db as db  # noqa: E402


AGENTES = ["nexo", "onir", "sandman"]


def run_heartbeat(agente_id: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(HEARTBEAT_RUNNER), agente_id],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "agente": agente_id,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    db.inicializar_banco()

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    titulo = f"P030 - colaboracao 3 agentes ({agora})"
    tarefa_id = db.criar_tarefa(
        titulo=titulo,
        descricao="Teste colaborativo automatizado para P030",
        criado_por="igor",
        prioridade=8,
        projeto="colmeia-v6",
        tags=["p030", "teste", "colaboracao"],
    )
    db.atribuir_tarefa(tarefa_id, "nexo")
    db.criar_mensagem(
        tarefa_id,
        de_agente="nexo",
        conteudo="Abrindo thread colaborativa para P030.",
        mencoes=["onir", "sandman"],
    )

    resultados = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(run_heartbeat, a): a for a in AGENTES}
        for fut in as_completed(futs):
            resultados.append(fut.result())

    # Evidencias
    subs = db.listar_subscriptions(tarefa_id=tarefa_id)
    notifs_onir = db.listar_notificacoes("onir", apenas_pendentes=False)
    notifs_sandman = db.listar_notificacoes("sandman", apenas_pendentes=False)
    recorte_notifs = [n for n in (notifs_onir + notifs_sandman) if str(n.get("referencia_id")) == str(tarefa_id)]

    ok_heartbeats = all(r["exit_code"] == 0 for r in resultados)
    ok_subs = set(s["agente_id"] for s in subs) >= {"nexo", "onir", "sandman"}
    ok_notifs = len(recorte_notifs) >= 2
    sucesso = ok_heartbeats and ok_subs and ok_notifs

    payload = {
        "timestamp": datetime.now().isoformat(),
        "teste": "P030",
        "tarefa_id": tarefa_id,
        "titulo": titulo,
        "resultados_heartbeat": resultados,
        "subscriptions": subs,
        "notificacoes_recorte": recorte_notifs,
        "checks": {
            "heartbeats_exit_0": ok_heartbeats,
            "subscriptions_tres_agentes": ok_subs,
            "notificacoes_thread": ok_notifs,
        },
        "sucesso": sucesso,
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    out_file = LOG_DIR / f"teste_p030_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"P030 arquivo: {out_file}")
    print(f"P030 sucesso: {sucesso}")
    return 0 if sucesso else 1


if __name__ == "__main__":
    raise SystemExit(main())
