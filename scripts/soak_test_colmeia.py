#!/usr/bin/env python3
"""
Colmeia v6 - P032
Soak test de estabilidade do heartbeat/notificacoes.

Executa ciclos automatizados e emite relatorio JSON.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BANCO_DIR = REPO_ROOT / "operacional" / "banco"
LOG_DIR = REPO_ROOT / "operacional" / "logs"
HEARTBEAT_RUNNER = BANCO_DIR / "heartbeat_runner.py"
DAEMON = BANCO_DIR / "notificacao_daemon.py"

AGENTES = ["nexo", "onir", "sandman"]


def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def ciclo(cycle_idx: int, retry_delay_min: int) -> dict:
    heartbeat_results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {
            ex.submit(run_cmd, [sys.executable, str(HEARTBEAT_RUNNER), a]): a
            for a in AGENTES
        }
        for fut in as_completed(futs):
            agente = futs[fut]
            code, out, err = fut.result()
            heartbeat_results.append(
                {"agente": agente, "exit_code": code, "stdout": out, "stderr": err}
            )

    dcode, dout, derr = run_cmd(
        [
            sys.executable,
            str(DAEMON),
            "--once",
            "--modo",
            "online",
            "--limite",
            "100",
            "--retry-delay-min",
            str(retry_delay_min),
            "--online-janela-min",
            "90",
        ]
    )

    return {
        "cycle": cycle_idx,
        "timestamp": datetime.now().isoformat(),
        "heartbeats": heartbeat_results,
        "daemon": {"exit_code": dcode, "stdout": dout, "stderr": derr},
    }


def calcular_metricas(ciclos: list[dict]) -> dict:
    total_hb = 0
    hb_ok = 0
    daemon_ok = 0
    for c in ciclos:
        if c["daemon"]["exit_code"] == 0:
            daemon_ok += 1
        for h in c["heartbeats"]:
            total_hb += 1
            if h["exit_code"] == 0:
                hb_ok += 1

    taxa = (hb_ok / total_hb * 100) if total_hb else 0.0
    return {
        "ciclos": len(ciclos),
        "heartbeats_total": total_hb,
        "heartbeats_ok": hb_ok,
        "heartbeat_success_rate": round(taxa, 1),
        "daemon_ok": daemon_ok,
        "meta_90": taxa >= 90.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Soak test Colmeia v6")
    parser.add_argument("--cycles", type=int, default=10, help="Quantidade de ciclos")
    parser.add_argument("--interval-sec", type=int, default=10, help="Intervalo entre ciclos")
    parser.add_argument("--retry-delay-min", type=int, default=30, help="Delay de retry do daemon")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    inicio = datetime.now()
    ciclos = []

    for i in range(1, args.cycles + 1):
        ciclos.append(ciclo(i, args.retry_delay_min))
        if i < args.cycles:
            time.sleep(args.interval_sec)

    fim = datetime.now()
    metricas = calcular_metricas(ciclos)
    payload = {
        "inicio": inicio.isoformat(),
        "fim": fim.isoformat(),
        "duracao_segundos": int((fim - inicio).total_seconds()),
        "parametros": vars(args),
        "metricas": metricas,
        "ciclos": ciclos,
    }

    out_file = LOG_DIR / f"soak_p032_{inicio.strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Soak report: {out_file}")
    print(f"Heartbeat success rate: {metricas['heartbeat_success_rate']}%")
    print(f"Meta >= 90%: {metricas['meta_90']}")
    return 0 if metricas["meta_90"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
