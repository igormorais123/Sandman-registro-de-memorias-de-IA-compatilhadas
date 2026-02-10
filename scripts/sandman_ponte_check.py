#!/usr/bin/env python3
"""
Ponte Sandman: Verificar fila de pedidos ao acordar.
Sandman roda isto ao início de cada sessão.

Uso:
  python3 sandman_ponte_check.py          # Mostra fila completa
  python3 sandman_ponte_check.py --brief   # Mostra resumo rápido (para bootstrap)
  python3 sandman_ponte_check.py --responder ped001 --status concluido --resumo "Feito"
"""

import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path

# Auto-detect workspace
CANDIDATES = [
    Path("/root/clawd"),
    Path("C:/Users/igorm/clawd"),
    Path("C:/Users/IgorPC/clawd"),
]
WORKSPACE = None
for c in CANDIDATES:
    if c.exists():
        WORKSPACE = c
        break
if not WORKSPACE:
    print("ERRO: workspace clawd/ nao encontrado")
    exit(1)

PONTE_DIR = WORKSPACE / "colmeia" / "ponte_sandman"
PEDIDOS_DIR = PONTE_DIR / "pedidos"
RESPOSTAS_DIR = PONTE_DIR / "respostas"
ARQUIVO_DIR = PONTE_DIR / "arquivo"
EVENTS_FILE = WORKSPACE / "compartilhado" / "events.json"


def check_fila(brief=False):
    """Verifica fila de pedidos pendentes."""
    PEDIDOS_DIR.mkdir(parents=True, exist_ok=True)
    pedidos = sorted(PEDIDOS_DIR.glob("PEDIDO_*.json"))

    if not pedidos:
        if brief:
            print("PONTE_SANDMAN_OK: Nenhum pedido pendente.")
        else:
            print("=" * 60)
            print("PONTE NEXO → SANDMAN")
            print("=" * 60)
            print("Fila vazia. Nenhum pedido do NEXO.")
            print("=" * 60)
        return []

    # Ordenar por prioridade
    parsed = []
    for p in pedidos:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            data["_filepath"] = p
            parsed.append(data)
        except Exception as e:
            print(f"AVISO: Erro lendo {p.name}: {e}")

    pri_order = {"urgente": 0, "normal": 1, "baixa": 2}
    parsed.sort(key=lambda x: pri_order.get(x.get("prioridade", "baixa"), 9))

    if brief:
        urgentes = sum(1 for p in parsed if p.get("prioridade") == "urgente")
        normais = sum(1 for p in parsed if p.get("prioridade") == "normal")
        baixas = sum(1 for p in parsed if p.get("prioridade") == "baixa")

        parts = []
        if urgentes:
            parts.append(f"{urgentes} URGENTE(S)")
        if normais:
            parts.append(f"{normais} normal(is)")
        if baixas:
            parts.append(f"{baixas} baixa(s)")

        print(f"PONTE_SANDMAN_PEDIDOS: {len(parsed)} pedido(s) — {', '.join(parts)}")

        if urgentes:
            for p in parsed:
                if p.get("prioridade") == "urgente":
                    print(f"  🔴 [{p['id']}] {p['tipo']}: {p['titulo']}")
        return parsed

    # Exibição completa
    print("=" * 60)
    print(f"PONTE NEXO → SANDMAN: {len(parsed)} PEDIDO(S) PENDENTE(S)")
    print("=" * 60)

    for p in parsed:
        pri = p.get("prioridade", "?")
        pri_icon = {"urgente": "🔴", "normal": "🟡", "baixa": "🟢"}.get(pri, "⚪")

        print()
        print(f"  {pri_icon} [{p['id']}] {p['tipo'].upper()}: {p['titulo']}")
        print(f"     Prioridade: {pri}")
        print(f"     Criado: {p.get('criado_em', '?')[:16]}")

        if p.get("descricao"):
            desc = p["descricao"]
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"     Descrição: {desc}")

        if p.get("arquivos_relevantes"):
            print(f"     Arquivos: {', '.join(p['arquivos_relevantes'])}")

    print()
    print("-" * 60)
    print("AÇÃO: Processar pedidos por prioridade (urgente → normal → baixa)")
    print("Após processar: sandman_ponte_check.py --responder [id] --status concluido --resumo '...'")
    print("=" * 60)

    return parsed


def responder(pedido_id, status, resumo, arquivos_criados=None, arquivos_modificados=None, notas=None):
    """Responde a um pedido, movendo-o para arquivo."""
    RESPOSTAS_DIR.mkdir(parents=True, exist_ok=True)
    ARQUIVO_DIR.mkdir(parents=True, exist_ok=True)

    # Encontrar o pedido
    pedido_file = None
    pedido_data = None
    for p in PEDIDOS_DIR.glob("PEDIDO_*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("id") == pedido_id:
                pedido_file = p
                pedido_data = data
                break
        except:
            pass

    if not pedido_file:
        print(f"ERRO: Pedido {pedido_id} não encontrado em pedidos/")
        return

    # Criar resposta
    now = datetime.now()
    resp_num = pedido_id.replace("ped", "")

    resposta = {
        "id": f"resp{resp_num}",
        "pedido_id": pedido_id,
        "de": "Sandman",
        "para": "NEXO",
        "status": status,
        "resumo": resumo,
        "arquivos_criados": arquivos_criados or [],
        "arquivos_modificados": arquivos_modificados or [],
        "respondido_em": now.isoformat(),
        "notas": notas,
        "pedido_original": {
            "tipo": pedido_data.get("tipo"),
            "titulo": pedido_data.get("titulo"),
            "prioridade": pedido_data.get("prioridade"),
            "criado_em": pedido_data.get("criado_em")
        }
    }

    resp_filename = f"RESPOSTA_{resp_num}_{now.strftime('%Y-%m-%d')}.json"
    resp_path = RESPOSTAS_DIR / resp_filename
    resp_path.write_text(json.dumps(resposta, indent=2, ensure_ascii=False), encoding="utf-8")

    # Atualizar status do pedido e mover para arquivo
    pedido_data["status"] = status
    pedido_data["respondido_em"] = now.isoformat()
    pedido_data["respondido_por"] = "Sandman"
    pedido_file.write_text(json.dumps(pedido_data, indent=2, ensure_ascii=False), encoding="utf-8")

    arquivo_dest = ARQUIVO_DIR / pedido_file.name
    shutil.move(str(pedido_file), str(arquivo_dest))

    # Registrar evento
    try:
        if EVENTS_FILE.exists():
            events = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))
            evt_num = len(events.get("events", [])) + 1
            events["events"].append({
                "id": f"evt{evt_num:03d}",
                "type": "resposta",
                "action": "ponte_sandman_resposta",
                "actor": "Sandman",
                "target": "NEXO",
                "timestamp": now.isoformat(),
                "summary": f"Resposta [{status}]: {pedido_data.get('titulo', '?')}",
                "data": {
                    "pedido_id": pedido_id,
                    "resposta_file": str(resp_path.relative_to(WORKSPACE)),
                    "status": status
                },
                "handled": False,
                "handledBy": None
            })
            events["lastUpdated"] = now.isoformat()
            EVENTS_FILE.write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"AVISO: Não consegui registrar evento: {e}")

    status_icon = {
        "concluido": "✅",
        "parcial": "🟡",
        "impossivel": "❌",
        "precisa_igor": "👤"
    }.get(status, "?")

    print(f"PONTE_SANDMAN_RESPOSTA: {status_icon} {pedido_id}")
    print(f"  Status: {status}")
    print(f"  Resumo: {resumo}")
    print(f"  Resposta: {resp_filename}")
    print(f"  Pedido movido para: arquivo/{pedido_file.name}")
    print()
    print("NEXO receberá no próximo heartbeat (sandman_sync).")


def check_respostas_pendentes():
    """NEXO usa isso para checar respostas do Sandman."""
    RESPOSTAS_DIR.mkdir(parents=True, exist_ok=True)
    respostas = sorted(RESPOSTAS_DIR.glob("RESPOSTA_*.json"))

    if not respostas:
        print("PONTE_SANDMAN: Nenhuma resposta nova do Sandman.")
        return []

    print(f"PONTE_SANDMAN_RESPOSTAS: {len(respostas)} resposta(s) nova(s)")
    print("-" * 50)

    parsed = []
    for r in respostas:
        try:
            data = json.loads(r.read_text(encoding="utf-8"))
            parsed.append(data)

            status_icon = {
                "concluido": "✅",
                "parcial": "🟡",
                "impossivel": "❌",
                "precisa_igor": "👤"
            }.get(data.get("status", "?"), "?")

            print(f"  {status_icon} [{data['pedido_id']}] {data.get('pedido_original', {}).get('titulo', '?')}")
            print(f"     Status: {data['status']}")
            print(f"     Resumo: {data.get('resumo', '?')}")
            if data.get("arquivos_criados"):
                print(f"     Criados: {', '.join(data['arquivos_criados'])}")
        except Exception as e:
            print(f"  ⚠️ Erro lendo {r.name}: {e}")

    print("-" * 50)
    print("Após ler, mover respostas para arquivo/ com:")
    print(f"  mv {RESPOSTAS_DIR}/RESPOSTA_*.json {ARQUIVO_DIR}/")

    return parsed


def main():
    parser = argparse.ArgumentParser(description="Ponte Sandman: verificar e responder pedidos")
    parser.add_argument("--brief", action="store_true", help="Resumo rápido (para bootstrap)")
    parser.add_argument("--respostas", action="store_true", help="NEXO: checar respostas do Sandman")
    parser.add_argument("--responder", metavar="PEDIDO_ID", help="Responder a um pedido")
    parser.add_argument("--status", choices=["concluido", "parcial", "impossivel", "precisa_igor"])
    parser.add_argument("--resumo", help="Resumo da resposta")
    parser.add_argument("--criados", nargs="*", default=[], help="Arquivos criados")
    parser.add_argument("--modificados", nargs="*", default=[], help="Arquivos modificados")
    parser.add_argument("--notas", help="Notas adicionais")

    args = parser.parse_args()

    if args.respostas:
        check_respostas_pendentes()
    elif args.responder:
        if not args.status or not args.resumo:
            print("ERRO: --responder requer --status e --resumo")
            return
        responder(args.responder, args.status, args.resumo, args.criados, args.modificados, args.notas)
    else:
        check_fila(brief=args.brief)


if __name__ == "__main__":
    main()
