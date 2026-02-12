#!/usr/bin/env python3
"""
Colmeia v6 - Daemon de Notificacoes

Processa notificacoes pendentes com retry.

Uso:
  python notificacao_daemon.py --once
  python notificacao_daemon.py --interval 60
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import colmeia_db as db


SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOGS_DIR = REPO_ROOT / "operacional" / "logs"


def log_execucao(payload):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"notificacao_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ciclo(args):
    inicio = time.time()
    try:
        agentes_online = None
        if args.modo == "online":
            agentes_online = db.obter_agentes_online(janela_min=args.online_janela_min)

        stats = db.processar_fila_notificacoes(
            agentes_online=agentes_online,
            limite=args.limite,
            retry_delay_min=args.retry_delay_min,
            entregador="daemon_online" if args.modo == "online" else "daemon_all",
            ignorar_agendamento=args.modo == "all",
        )

        duracao_ms = int((time.time() - inicio) * 1000)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "modo": args.modo,
            "agentes_online": agentes_online if agentes_online is not None else "all",
            "stats": stats,
            "duracao_ms": duracao_ms,
        }
        log_execucao(payload)
        print(json.dumps(payload, ensure_ascii=False))

    except Exception as e:
        duracao_ms = int((time.time() - inicio) * 1000)
        erro_payload = {
            "timestamp": datetime.now().isoformat(),
            "modo": args.modo,
            "stats": {"erro": f"{type(e).__name__}: {e}"},
            "duracao_ms": duracao_ms,
        }
        log_execucao(erro_payload)
        import sys
        print(f"ERRO no ciclo de notificacoes: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Colmeia v6 - Daemon de notificacoes")
    parser.add_argument("--once", action="store_true", help="Executa um ciclo e finaliza")
    parser.add_argument("--interval", type=int, default=60, help="Intervalo entre ciclos em segundos")
    parser.add_argument("--limite", type=int, default=100, help="Maximo de notificacoes por ciclo")
    parser.add_argument("--retry-delay-min", type=int, default=30, help="Atraso para proxima tentativa")
    parser.add_argument("--online-janela-min", type=int, default=90, help="Janela de heartbeat para considerar online")
    parser.add_argument("--modo", choices=["online", "all"], default="online", help="Entrega apenas para online ou para todos")
    args = parser.parse_args()

    db.inicializar_banco()

    if args.once:
        ciclo(args)
        return

    while True:
        ciclo(args)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
