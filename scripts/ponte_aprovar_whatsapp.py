#!/usr/bin/env python3
"""
Ponte Segura — Aprovação via WhatsApp

Funções que o NEXO usa para:
1. Listar pendentes e avisar Igor via WhatsApp
2. Processar resposta de aprovação/rejeição do Igor
"""

import json
from pathlib import Path
from datetime import datetime

PENDING_DIR = Path("/root/clawd/colmeia/pendente_aprovacao")
QUEUE_DIR = Path("/root/clawd/colmeia/fila_onir")


def listar_pendentes_formatado():
    """Retorna string formatada dos pedidos pendentes para WhatsApp."""
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    pedidos = list(PENDING_DIR.glob("pedido_*.json"))
    
    if not pedidos:
        return None
    
    msg = f"📋 **{len(pedidos)} pedido(s) pendente(s):**\n\n"
    
    for i, p in enumerate(pedidos, 1):
        data = json.loads(p.read_text())
        msg += f"**{i}. {data['tipo'].upper()}**\n"
        msg += f"   Prompt: {data['prompt'][:100]}...\n"
        msg += f"   ID: `{p.stem}`\n\n"
    
    msg += "Responda:\n"
    msg += "• `aprovar 1` ou `aprovar tudo`\n"
    msg += "• `rejeitar 1` ou `rejeitar tudo`"
    
    return msg


def processar_comando_igor(texto: str) -> str:
    """
    Processa comando de aprovação/rejeição do Igor.
    Retorna mensagem de confirmação.
    
    Comandos aceitos:
    - "aprovar 1" / "aprovar 2" / "aprovar tudo"
    - "rejeitar 1" / "rejeitar 2" / "rejeitar tudo"
    - "pendentes" / "listar"
    """
    texto = texto.lower().strip()
    
    # Listar pendentes
    if texto in ["pendentes", "listar", "ponte"]:
        msg = listar_pendentes_formatado()
        return msg if msg else "📭 Nenhum pedido pendente."
    
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    pedidos = sorted(PENDING_DIR.glob("pedido_*.json"))
    
    if not pedidos:
        return "📭 Nenhum pedido pendente."
    
    # Aprovar
    if texto.startswith("aprovar"):
        partes = texto.split()
        if len(partes) < 2:
            return "❓ Use: `aprovar 1` ou `aprovar tudo`"
        
        alvo = partes[1]
        
        if alvo == "tudo":
            count = 0
            for p in pedidos:
                _aprovar_pedido(p)
                count += 1
            return f"✅ {count} pedido(s) aprovado(s)!"
        
        try:
            idx = int(alvo) - 1
            if 0 <= idx < len(pedidos):
                nome = pedidos[idx].name
                _aprovar_pedido(pedidos[idx])
                return f"✅ Aprovado: {nome}"
            else:
                return f"❌ Número inválido. Use 1 a {len(pedidos)}"
        except ValueError:
            return "❓ Use: `aprovar 1` ou `aprovar tudo`"
    
    # Rejeitar
    if texto.startswith("rejeitar"):
        partes = texto.split()
        if len(partes) < 2:
            return "❓ Use: `rejeitar 1` ou `rejeitar tudo`"
        
        alvo = partes[1]
        
        if alvo == "tudo":
            count = 0
            for p in pedidos:
                _rejeitar_pedido(p)
                count += 1
            return f"❌ {count} pedido(s) rejeitado(s)."
        
        try:
            idx = int(alvo) - 1
            if 0 <= idx < len(pedidos):
                nome = pedidos[idx].name
                _rejeitar_pedido(pedidos[idx])
                return f"❌ Rejeitado: {nome}"
            else:
                return f"❌ Número inválido. Use 1 a {len(pedidos)}"
        except ValueError:
            return "❓ Use: `rejeitar 1` ou `rejeitar tudo`"
    
    return None  # Não é comando de ponte


def _aprovar_pedido(filepath: Path):
    """Move pedido para fila aprovada."""
    pedido = json.loads(filepath.read_text())
    pedido["status"] = "aprovado_igor"
    pedido["aprovado_em"] = datetime.now().isoformat()
    
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    new_path = QUEUE_DIR / filepath.name
    new_path.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
    filepath.unlink()


def _rejeitar_pedido(filepath: Path):
    """Move pedido para rejeitados."""
    pedido = json.loads(filepath.read_text())
    pedido["status"] = "rejeitado_igor"
    pedido["rejeitado_em"] = datetime.now().isoformat()
    
    rejected_dir = PENDING_DIR / "rejeitados"
    rejected_dir.mkdir(parents=True, exist_ok=True)
    new_path = rejected_dir / filepath.name
    new_path.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
    filepath.unlink()


def ha_pendentes() -> bool:
    """Retorna True se há pedidos pendentes."""
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    return len(list(PENDING_DIR.glob("pedido_*.json"))) > 0


if __name__ == "__main__":
    # Teste
    print(listar_pendentes_formatado() or "Nenhum pendente")
