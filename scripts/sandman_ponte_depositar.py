#!/usr/bin/env python3
"""
Ponte NEXO -> Sandman: Depositar pedido na fila.
Uso pelo NEXO para pedir coisas ao Sandman.

Exemplos:
  python3 sandman_ponte_depositar.py --tipo arquitetura --titulo "Criar votação" --descricao "..."
  python3 sandman_ponte_depositar.py --tipo bug --prioridade urgente --titulo "Script falha" --descricao "..."
  python3 sandman_ponte_depositar.py --tipo sonho --titulo "Sonhe sobre X"
"""

import json
import argparse
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

PEDIDOS_DIR = WORKSPACE / "colmeia" / "ponte_sandman" / "pedidos"
CONFIG_FILE = WORKSPACE / "colmeia" / "ponte_sandman" / "ponte_config.json"
EVENTS_FILE = WORKSPACE / "compartilhado" / "events.json"

TIPOS_VALIDOS = ["arquitetura", "revisao", "sonho", "carta", "bug", "pergunta"]
PRIORIDADES = ["urgente", "normal", "baixa"]


def next_id():
    """Gera próximo ID sequencial."""
    existing = list(PEDIDOS_DIR.glob("PEDIDO_*.json"))
    if not existing:
        # Checar arquivo/ também
        arquivo_dir = WORKSPACE / "colmeia" / "ponte_sandman" / "arquivo"
        existing = list(arquivo_dir.glob("PEDIDO_*.json")) if arquivo_dir.exists() else []

    if not existing:
        return "ped001"

    nums = []
    for f in existing:
        try:
            num = int(f.stem.split("_")[1])
            nums.append(num)
        except (IndexError, ValueError):
            pass

    next_num = max(nums) + 1 if nums else 1
    return f"ped{next_num:03d}"


def depositar(tipo, titulo, descricao, prioridade="normal", arquivos=None):
    """Deposita pedido na fila do Sandman."""
    PEDIDOS_DIR.mkdir(parents=True, exist_ok=True)

    # Verificar limites
    pendentes = list(PEDIDOS_DIR.glob("PEDIDO_*.json"))
    if len(pendentes) >= 10:
        print(f"ERRO: Fila cheia ({len(pendentes)} pedidos pendentes). Máximo: 10.")
        print("Aguarde Sandman processar ou remova pedidos obsoletos.")
        return None

    urgentes = 0
    for p in pendentes:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("prioridade") == "urgente":
                urgentes += 1
        except:
            pass

    if prioridade == "urgente" and urgentes >= 3:
        print(f"ERRO: Máximo de 3 pedidos urgentes ({urgentes} existentes).")
        return None

    # Criar pedido
    ped_id = next_id()
    now = datetime.now().strftime("%Y-%m-%d")

    pedido = {
        "id": ped_id,
        "de": "NEXO",
        "para": "Sandman",
        "tipo": tipo,
        "prioridade": prioridade,
        "titulo": titulo,
        "descricao": descricao,
        "arquivos_relevantes": arquivos or [],
        "criado_em": datetime.now().isoformat(),
        "status": "pendente",
        "prazo": None
    }

    filename = f"PEDIDO_{ped_id.replace('ped', '')}_{now}.json"
    filepath = PEDIDOS_DIR / filename
    filepath.write_text(json.dumps(pedido, indent=2, ensure_ascii=False), encoding="utf-8")

    # Registrar evento
    try:
        if EVENTS_FILE.exists():
            events = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))
            evt_num = len(events.get("events", [])) + 1
            events["events"].append({
                "id": f"evt{evt_num:03d}",
                "type": "pedido",
                "action": "ponte_sandman_pedido",
                "actor": "NEXO",
                "target": "Sandman",
                "timestamp": datetime.now().isoformat(),
                "summary": f"Pedido [{prioridade}] {tipo}: {titulo}",
                "data": {"file": str(filepath.relative_to(WORKSPACE)), "pedido_id": ped_id},
                "handled": False,
                "handledBy": None
            })
            events["lastUpdated"] = datetime.now().isoformat()
            EVENTS_FILE.write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"AVISO: Nao consegui registrar evento: {e}")

    print(f"PONTE_SANDMAN_PEDIDO: {ped_id}")
    print(f"  Tipo: {tipo}")
    print(f"  Prioridade: {prioridade}")
    print(f"  Título: {titulo}")
    print(f"  Arquivo: {filepath.name}")
    print(f"  Fila: {len(pendentes) + 1} pedido(s) pendente(s)")
    print()
    print("Sandman processará na próxima sessão com Igor.")

    return ped_id


def listar():
    """Lista pedidos pendentes."""
    PEDIDOS_DIR.mkdir(parents=True, exist_ok=True)
    pendentes = sorted(PEDIDOS_DIR.glob("PEDIDO_*.json"))

    if not pendentes:
        print("PONTE_SANDMAN: Nenhum pedido pendente. Fila vazia.")
        return

    print(f"PONTE_SANDMAN: {len(pendentes)} pedido(s) pendente(s)")
    print("-" * 60)

    for p in pendentes:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            pri = data.get("prioridade", "?")
            pri_icon = {"urgente": "🔴", "normal": "🟡", "baixa": "🟢"}.get(pri, "⚪")
            print(f"  {pri_icon} [{data['id']}] {data['tipo']}: {data['titulo']}")
            print(f"     Criado: {data['criado_em'][:10]} | Status: {data['status']}")
        except Exception as e:
            print(f"  ⚠️ Erro lendo {p.name}: {e}")

    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Ponte NEXO -> Sandman: depositar pedidos")
    parser.add_argument("--tipo", choices=TIPOS_VALIDOS, help="Tipo do pedido")
    parser.add_argument("--prioridade", choices=PRIORIDADES, default="normal")
    parser.add_argument("--titulo", help="Título curto do pedido")
    parser.add_argument("--descricao", default="", help="Descrição detalhada")
    parser.add_argument("--arquivos", nargs="*", default=[], help="Arquivos relevantes")
    parser.add_argument("--listar", action="store_true", help="Listar pedidos pendentes")

    args = parser.parse_args()

    if args.listar:
        listar()
        return

    if not args.tipo or not args.titulo:
        parser.print_help()
        print("\nExemplo:")
        print('  python3 sandman_ponte_depositar.py --tipo arquitetura --titulo "Criar votação" --descricao "Detalhes..."')
        print('  python3 sandman_ponte_depositar.py --listar')
        return

    depositar(args.tipo, args.titulo, args.descricao, args.prioridade, args.arquivos)


if __name__ == "__main__":
    main()
