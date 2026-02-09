#!/usr/bin/env python3
"""
NEXO → ONIR: Criar pedido na fila segura

Uso:
    python3 nexo_pedir_onir.py --tipo sonho --prompt "Sonhe sobre X"
    python3 nexo_pedir_onir.py --tipo carta --prompt "Escreva carta para Sandman sobre Y"
    python3 nexo_pedir_onir.py --tipo consulta --prompt "Qual o estado do caso Igor?"
    python3 nexo_pedir_onir.py --tipo git --prompt "Faca pull e verifique conflitos"
    python3 nexo_pedir_onir.py --tipo pesquisa --prompt "Pesquise sobre X"
    python3 nexo_pedir_onir.py --tipo relatorio --prompt "Gere relatorio de Y"

Tipos permitidos: sonho, carta, consulta, git, pesquisa, relatorio
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

QUEUE_DIR = Path("/root/clawd/colmeia/fila_onir")
ALLOWED_TYPES = ["sonho", "carta", "consulta", "git", "pesquisa", "relatorio"]

def criar_pedido(tipo: str, prompt: str, origem: str = "NEXO"):
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    if tipo not in ALLOWED_TYPES:
        print(f"Tipo '{tipo}' nao permitido. Permitidos: {ALLOWED_TYPES}")
        return None

    if len(prompt) > 5000:
        print(f"Prompt muito grande ({len(prompt)} chars, max 5000)")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pedido_{tipo}_{timestamp}.json"

    pedido = {
        "tipo": tipo,
        "prompt": prompt,
        "origem": origem,
        "timestamp": datetime.now().isoformat(),
    }

    filepath = QUEUE_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(pedido, f, indent=2, ensure_ascii=False)

    print(f"Pedido criado: {filepath}")
    print(f"  Tipo: {tipo}")
    print(f"  Prompt: {prompt[:100]}...")
    print(f"  Aguardando ONIR processar (proximo ciclo da ponte)")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Criar pedido para ONIR via ponte segura')
    parser.add_argument('--tipo', choices=ALLOWED_TYPES, required=True)
    parser.add_argument('--prompt', required=True)
    parser.add_argument('--origem', default='NEXO')
    args = parser.parse_args()
    criar_pedido(args.tipo, args.prompt, args.origem)

if __name__ == "__main__":
    main()
