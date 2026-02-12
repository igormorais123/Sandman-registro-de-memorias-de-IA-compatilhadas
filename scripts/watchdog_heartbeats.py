#!/usr/bin/env python3
"""
Colmeia v6 — Watchdog de Heartbeats
Detecta agentes que pararam de bater heartbeat e alerta.

Uso:
  python watchdog_heartbeats.py                 # verifica todos, limiar 60min
  python watchdog_heartbeats.py --limiar 90     # limiar de 90 minutos
  python watchdog_heartbeats.py --json           # saida JSON
  python watchdog_heartbeats.py --agentes nexo onir sandman helena

Retorna exit code:
  0 = todos os agentes monitorados ativos
  1 = pelo menos um agente inativo
  2 = erro de execucao
"""

import argparse
import json
import sys
import io
import os
from datetime import datetime, timedelta
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "operacional" / "banco"))
import colmeia_db as db

# Agentes que devem estar automatizados (monitorar por padrao)
AGENTES_AUTO = ["nexo", "onir", "sandman", "helena"]


def verificar_heartbeats(agentes_ids, limiar_min=60):
    """Verifica se os agentes bateram heartbeat dentro do limiar."""
    agora = datetime.now()
    limite = agora - timedelta(minutes=limiar_min)
    limite_str = limite.strftime("%Y-%m-%d %H:%M:%S")

    resultados = []
    todos_agentes = db.listar_agentes()
    mapa_agentes = {a["id"]: a for a in todos_agentes}

    for aid in agentes_ids:
        agente = mapa_agentes.get(aid)
        if not agente:
            resultados.append({
                "agente": aid,
                "status": "NAO_ENCONTRADO",
                "ultimo_hb": None,
                "minutos_atras": None,
                "ativo": False,
            })
            continue

        ultimo_hb = agente.get("ultimo_heartbeat")
        if not ultimo_hb:
            resultados.append({
                "agente": aid,
                "status": "SEM_HEARTBEAT",
                "ultimo_hb": None,
                "minutos_atras": None,
                "ativo": False,
            })
            continue

        try:
            hb_dt = datetime.fromisoformat(ultimo_hb)
        except (ValueError, TypeError):
            # Tentar formato alternativo
            try:
                hb_dt = datetime.strptime(ultimo_hb, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                resultados.append({
                    "agente": aid,
                    "status": "HB_INVALIDO",
                    "ultimo_hb": ultimo_hb,
                    "minutos_atras": None,
                    "ativo": False,
                })
                continue

        delta = agora - hb_dt
        minutos_atras = int(delta.total_seconds() / 60)
        ativo = minutos_atras <= limiar_min

        resultados.append({
            "agente": aid,
            "status": "ATIVO" if ativo else "INATIVO",
            "ultimo_hb": ultimo_hb,
            "minutos_atras": minutos_atras,
            "ativo": ativo,
        })

    return resultados


def imprimir_relatorio(resultados, limiar_min):
    """Imprime relatorio do watchdog."""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n  === WATCHDOG HEARTBEATS — Colmeia v6 ===")
    print(f"  Verificacao: {agora}")
    print(f"  Limiar: {limiar_min} minutos")
    print(f"  {'=' * 55}")

    inativos = []
    for r in resultados:
        icon = "[OK]" if r["ativo"] else "[!!]"
        if r["minutos_atras"] is not None:
            tempo = f"{r['minutos_atras']}min atras"
        else:
            tempo = r["status"]

        print(f"  {icon} @{r['agente']:12s}  {r['status']:18s}  {tempo}")
        if not r["ativo"]:
            inativos.append(r["agente"])

    print()
    if inativos:
        print(f"  ALERTA: {len(inativos)} agente(s) inativo(s): {', '.join(inativos)}")
        print(f"  Verificar Task Scheduler e/ou estado do PC.")
    else:
        print(f"  Todos os agentes monitorados estao ativos.")
    print()


def main():
    parser = argparse.ArgumentParser(description="Colmeia v6 — Watchdog de Heartbeats")
    parser.add_argument("--limiar", type=int, default=60, help="Minutos sem heartbeat para considerar inativo (default: 60)")
    parser.add_argument("--agentes", nargs="+", default=AGENTES_AUTO, help="IDs dos agentes a monitorar")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    args = parser.parse_args()

    db.inicializar_banco()
    resultados = verificar_heartbeats(args.agentes, limiar_min=args.limiar)

    if args.json:
        saida = {
            "timestamp": datetime.now().isoformat(),
            "limiar_min": args.limiar,
            "agentes": resultados,
            "todos_ativos": all(r["ativo"] for r in resultados),
        }
        print(json.dumps(saida, ensure_ascii=False, indent=2))
    else:
        imprimir_relatorio(resultados, args.limiar)

    # Exit code: 0 se todos ativos, 1 se algum inativo
    if all(r["ativo"] for r in resultados):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
