#!/usr/bin/env python3
"""
NEXO → ONIR: Ponte Segura v2

REGRAS DE SEGURANÇA (aprovadas por Igor em 2026-02-09):
1. AUTOMÁTICO (sem aprovação): apenas "sonho"
2. LIMITE: máximo 5 pedidos/dia sem aprovação
3. SENSÍVEIS (requer aprovação Igor): carta, consulta, git, pesquisa, relatorio

Uso:
    # Automático (sonho)
    python3 nexo_pedir_onir_v2.py --tipo sonho --prompt "Sonhe sobre X"
    
    # Requer aprovação (cria pedido pendente)
    python3 nexo_pedir_onir_v2.py --tipo carta --prompt "Escreva carta para Y"
    
    # Igor aprova
    python3 nexo_pedir_onir_v2.py --aprovar pedido_carta_20260209_1530.json
    
    # Igor rejeita
    python3 nexo_pedir_onir_v2.py --rejeitar pedido_carta_20260209_1530.json
"""

import json
import argparse
from datetime import datetime, date
from pathlib import Path

# Diretórios
QUEUE_DIR = Path("/root/clawd/colmeia/fila_onir")
PENDING_DIR = Path("/root/clawd/colmeia/pendente_aprovacao")
STATS_FILE = Path("/root/clawd/colmeia/ponte_stats.json")

# Configuração de segurança
AUTOMATICO = ["sonho"]  # Só sonho é automático
REQUER_APROVACAO = ["carta", "consulta", "git", "pesquisa", "relatorio"]
LIMITE_DIARIO = 5  # Max pedidos automáticos por dia
MAX_PROMPT_CHARS = 10000  # Aumentado para sonhos profundos

# Comandos perigosos (sempre bloqueados)
COMANDOS_PERIGOSOS = [
    "rm -rf", "rm -r /", "format c:", "del /s /q", 
    "shutdown", "taskkill /f", "net user", "reg delete",
    "cipher /w", "dd if=", ":(){:|:&};:", "mkfs",
    "chmod -R 777 /", "chown -R", "> /dev/sda"
]


def carregar_stats():
    """Carrega estatísticas diárias."""
    if STATS_FILE.exists():
        stats = json.loads(STATS_FILE.read_text())
        # Reset se mudou o dia
        if stats.get("data") != str(date.today()):
            stats = {"data": str(date.today()), "pedidos_hoje": 0}
    else:
        stats = {"data": str(date.today()), "pedidos_hoje": 0}
    return stats


def salvar_stats(stats):
    """Salva estatísticas."""
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2))


def verificar_comando_perigoso(prompt: str) -> bool:
    """Retorna True se prompt contém comando perigoso."""
    prompt_lower = prompt.lower()
    for cmd in COMANDOS_PERIGOSOS:
        if cmd.lower() in prompt_lower:
            return True
    return False


def criar_pedido(tipo: str, prompt: str, origem: str = "NEXO", force: bool = False):
    """Cria pedido na fila (automático) ou pendente (requer aprovação)."""
    
    # Validar tamanho
    if len(prompt) > MAX_PROMPT_CHARS:
        print(f"❌ Prompt muito grande ({len(prompt)} chars, max {MAX_PROMPT_CHARS})")
        return None
    
    # Verificar comandos perigosos (SEMPRE bloqueado)
    if verificar_comando_perigoso(prompt):
        print("🚨 BLOQUEADO: Prompt contém comando perigoso!")
        print("   Esse pedido NÃO pode ser feito nem com aprovação.")
        # TODO: Alertar Igor
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pedido_{tipo}_{timestamp}.json"
    
    pedido = {
        "tipo": tipo,
        "prompt": prompt,
        "origem": origem,
        "timestamp": datetime.now().isoformat(),
        "status": "pendente"
    }
    
    # Tipo automático (sonho)
    if tipo in AUTOMATICO and not force:
        stats = carregar_stats()
        
        # Verificar limite diário
        if stats["pedidos_hoje"] >= LIMITE_DIARIO:
            print(f"⚠️ Limite diário atingido ({LIMITE_DIARIO} pedidos)")
            print("   Pedido será colocado para aprovação de Igor.")
            # Coloca em pendente
            PENDING_DIR.mkdir(parents=True, exist_ok=True)
            pedido["motivo_pendente"] = "limite_diario"
            filepath = PENDING_DIR / filename
            filepath.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
            print(f"📋 Pedido pendente: {filepath}")
            return filepath
        
        # Criar na fila automática
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        pedido["status"] = "aprovado_auto"
        filepath = QUEUE_DIR / filename
        filepath.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
        
        # Atualizar stats
        stats["pedidos_hoje"] += 1
        salvar_stats(stats)
        
        print(f"✅ Pedido automático criado: {filepath.name}")
        print(f"   Tipo: {tipo}")
        print(f"   Pedidos hoje: {stats['pedidos_hoje']}/{LIMITE_DIARIO}")
        return filepath
    
    # Tipo que requer aprovação
    elif tipo in REQUER_APROVACAO:
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        pedido["motivo_pendente"] = "tipo_sensivel"
        filepath = PENDING_DIR / filename
        filepath.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
        
        print(f"📋 Pedido PENDENTE (requer aprovação de Igor):")
        print(f"   Arquivo: {filepath.name}")
        print(f"   Tipo: {tipo}")
        print(f"   Prompt: {prompt[:100]}...")
        print(f"\n   Para aprovar: python3 {__file__} --aprovar {filename}")
        print(f"   Para rejeitar: python3 {__file__} --rejeitar {filename}")
        return filepath
    
    else:
        print(f"❌ Tipo '{tipo}' não reconhecido.")
        print(f"   Automáticos: {AUTOMATICO}")
        print(f"   Requer aprovação: {REQUER_APROVACAO}")
        return None


def aprovar_pedido(filename: str):
    """Igor aprova um pedido pendente."""
    filepath = PENDING_DIR / filename
    
    if not filepath.exists():
        print(f"❌ Pedido não encontrado: {filename}")
        return False
    
    pedido = json.loads(filepath.read_text())
    pedido["status"] = "aprovado_igor"
    pedido["aprovado_em"] = datetime.now().isoformat()
    
    # Mover para fila
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    new_path = QUEUE_DIR / filename
    new_path.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
    filepath.unlink()
    
    print(f"✅ Pedido APROVADO e movido para fila: {filename}")
    return True


def rejeitar_pedido(filename: str, motivo: str = ""):
    """Igor rejeita um pedido pendente."""
    filepath = PENDING_DIR / filename
    
    if not filepath.exists():
        print(f"❌ Pedido não encontrado: {filename}")
        return False
    
    pedido = json.loads(filepath.read_text())
    pedido["status"] = "rejeitado_igor"
    pedido["rejeitado_em"] = datetime.now().isoformat()
    pedido["motivo_rejeicao"] = motivo
    
    # Mover para rejeitados
    rejected_dir = PENDING_DIR / "rejeitados"
    rejected_dir.mkdir(parents=True, exist_ok=True)
    new_path = rejected_dir / filename
    new_path.write_text(json.dumps(pedido, indent=2, ensure_ascii=False))
    filepath.unlink()
    
    print(f"❌ Pedido REJEITADO: {filename}")
    return True


def listar_pendentes():
    """Lista pedidos aguardando aprovação."""
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    pedidos = list(PENDING_DIR.glob("pedido_*.json"))
    
    if not pedidos:
        print("📭 Nenhum pedido pendente de aprovação.")
        return
    
    print(f"📋 {len(pedidos)} pedido(s) pendente(s):\n")
    for p in pedidos:
        data = json.loads(p.read_text())
        print(f"  📄 {p.name}")
        print(f"     Tipo: {data['tipo']}")
        print(f"     Origem: {data.get('origem', 'NEXO')}")
        print(f"     Motivo: {data.get('motivo_pendente', '?')}")
        print(f"     Prompt: {data['prompt'][:80]}...")
        print()


def main():
    parser = argparse.ArgumentParser(description='Ponte Segura v2: NEXO → ONIR')
    parser.add_argument('--tipo', choices=AUTOMATICO + REQUER_APROVACAO)
    parser.add_argument('--prompt')
    parser.add_argument('--origem', default='NEXO')
    parser.add_argument('--aprovar', help='Aprovar pedido pendente')
    parser.add_argument('--rejeitar', help='Rejeitar pedido pendente')
    parser.add_argument('--motivo', default='', help='Motivo da rejeição')
    parser.add_argument('--listar', action='store_true', help='Listar pendentes')
    parser.add_argument('--stats', action='store_true', help='Ver estatísticas')
    
    args = parser.parse_args()
    
    if args.listar:
        listar_pendentes()
    elif args.stats:
        stats = carregar_stats()
        print(f"📊 Estatísticas de {stats['data']}:")
        print(f"   Pedidos automáticos: {stats['pedidos_hoje']}/{LIMITE_DIARIO}")
    elif args.aprovar:
        aprovar_pedido(args.aprovar)
    elif args.rejeitar:
        rejeitar_pedido(args.rejeitar, args.motivo)
    elif args.tipo and args.prompt:
        criar_pedido(args.tipo, args.prompt, args.origem)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
