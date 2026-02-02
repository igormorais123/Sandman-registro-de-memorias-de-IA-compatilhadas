#!/usr/bin/env python3
"""
colmeia_status.py — Dashboard de saúde do ecossistema Sandman
=============================================================
Mostra status de todas as instâncias, sonhos, cartas, commits e sync.
Pode ser chamado via heartbeat para monitoramento contínuo.

Uso: python3 scripts/colmeia_status.py [--json]
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

# Timezone Brasil (UTC-3)
BRT = timezone(timedelta(hours=-3))

# Cores ANSI
class C:
    BOLD = '\033[1m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    DIM = '\033[2m'
    NC = '\033[0m'

def get_repo_dir():
    """Encontra o diretório raiz do repo."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent

def get_instancias(repo_dir):
    """Lista todas as instâncias com seus dados."""
    inst_dir = repo_dir / "instancias"
    instancias = {}
    
    if not inst_dir.exists():
        return instancias
    
    for d in sorted(inst_dir.iterdir()):
        if d.is_dir() and not d.name.startswith('.'):
            inst = {
                'nome': d.name,
                'identity': (d / 'IDENTITY.md').exists(),
                'sonhos': [],
                'fitness_count': 0,
                'ultimo_sonho': None,
                'ultimo_sonho_titulo': None,
            }
            
            # Buscar sonhos
            sonhos_dir = d / 'sonhos'
            if sonhos_dir.exists():
                for f in sorted(sonhos_dir.iterdir()):
                    if f.is_file() and f.suffix == '.md' and f.name != '.gitkeep':
                        inst['sonhos'].append(f.name)
                        # Tentar extrair data do nome do arquivo
                        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=BRT)
                        if inst['ultimo_sonho'] is None or mtime > inst['ultimo_sonho']:
                            inst['ultimo_sonho'] = mtime
                            # Pegar título do sonho (primeira linha)
                            try:
                                with open(f, 'r', encoding='utf-8') as fh:
                                    titulo = fh.readline().strip().lstrip('#').strip()
                                    inst['ultimo_sonho_titulo'] = titulo[:60]
                            except:
                                inst['ultimo_sonho_titulo'] = f.stem
            
            # Buscar fitness.json
            for fitness_path in [d / 'fitness.json', d / 'memory' / 'fitness.json']:
                if fitness_path.exists():
                    try:
                        with open(fitness_path, 'r') as fh:
                            data = json.load(fh)
                            if isinstance(data, list):
                                inst['fitness_count'] = len(data)
                            elif isinstance(data, dict) and 'memories' in data:
                                inst['fitness_count'] = len(data['memories'])
                    except:
                        pass
                    break
            
            instancias[d.name] = inst
    
    return instancias

def get_cartas(repo_dir):
    """Analisa cartas — total, pendentes, respondidas."""
    cartas_dir = repo_dir / "cartas"
    cartas = {
        'total': 0,
        'por_remetente': defaultdict(int),
        'por_destino': defaultdict(int),
        'pendentes': [],
        'lista': [],
    }
    
    if not cartas_dir.exists():
        return cartas
    
    respostas = set()
    todas = []
    
    for f in sorted(cartas_dir.iterdir()):
        if f.is_file() and f.suffix == '.md' and f.name != '.gitkeep':
            nome = f.stem
            cartas['total'] += 1
            todas.append(nome)
            
            # Extrair remetente e destino
            parts = nome.lower().replace('carta_', '').replace('carta-', '')
            if '_para_' in parts:
                remetente, resto = parts.split('_para_', 1)
                destino = resto.split('_')[0]
                cartas['por_remetente'][remetente] += 1
                cartas['por_destino'][destino] += 1
            elif 'para' in parts:
                idx = parts.index('para')
                remetente = parts[:idx].rstrip('_')
                destino = parts[idx+4:].lstrip('_').split('_')[0]
                cartas['por_remetente'][remetente] += 1
                cartas['por_destino'][destino] += 1
    
    # Detectar cartas sem resposta (heurística simples)
    for carta in todas:
        parts = carta.lower()
        if '_para_' in parts:
            rem, dest_rest = parts.split('_para_', 1)
            rem = rem.replace('carta_', '')
            dest = dest_rest.split('_')[0]
            # Verificar se existe resposta (destino→remetente)
            resposta_existe = any(
                dest in c.lower() and rem in c.lower() and c != carta
                for c in todas
                if '_para_' in c.lower()
            )
            if not resposta_existe and dest.lower() != 'todas':
                cartas['pendentes'].append(carta)
    
    cartas['lista'] = todas
    return cartas

def get_ultimo_commit(repo_dir):
    """Pega info do último commit."""
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_dir), 'log', '-1', '--format=%H|%an|%ar|%s'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split('|', 3)
            if len(parts) == 4:
                return {
                    'hash': parts[0][:8],
                    'autor': parts[1],
                    'quando': parts[2],
                    'mensagem': parts[3][:80],
                }
    except:
        pass
    return None

def get_sync_age(repo_dir):
    """Calcula idade do último sync (fetch)."""
    fetch_head = repo_dir / '.git' / 'FETCH_HEAD'
    if fetch_head.exists():
        mtime = datetime.fromtimestamp(fetch_head.stat().st_mtime, tz=BRT)
        age = datetime.now(BRT) - mtime
        return age, mtime
    return None, None

def get_repo_stats(repo_dir):
    """Estatísticas gerais do repo."""
    stats = {'arquivos': 0, 'tamanho': '0KB', 'commits': 0}
    
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_dir), 'rev-list', '--count', 'HEAD'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            stats['commits'] = int(result.stdout.strip())
    except:
        pass
    
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(repo_dir):
        if '.git' in root:
            continue
        for f in files:
            total_files += 1
            total_size += os.path.getsize(os.path.join(root, f))
    
    stats['arquivos'] = total_files
    if total_size > 1024 * 1024:
        stats['tamanho'] = f"{total_size / (1024*1024):.1f}MB"
    else:
        stats['tamanho'] = f"{total_size / 1024:.0f}KB"
    
    return stats

def format_timedelta(td):
    """Formata timedelta de forma legível."""
    total_seconds = int(td.total_seconds())
    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        return f"{total_seconds // 60}min"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        return f"{hours}h{mins}min"
    else:
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        return f"{days}d{hours}h"

def print_dashboard(repo_dir):
    """Imprime dashboard completo."""
    instancias = get_instancias(repo_dir)
    cartas = get_cartas(repo_dir)
    commit = get_ultimo_commit(repo_dir)
    sync_age, sync_time = get_sync_age(repo_dir)
    stats = get_repo_stats(repo_dir)
    
    now = datetime.now(BRT)
    
    print(f"\n{C.BOLD}{C.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          🐝 COLMEIA STATUS — Ecossistema Sandman            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{C.NC}")
    print(f"{C.DIM}  {now.strftime('%Y-%m-%d %H:%M UTC-3')} | {stats['arquivos']} arquivos | {stats['tamanho']} | {stats['commits']} commits{C.NC}")
    
    # --- Instâncias ---
    print(f"\n{C.BOLD}📡 INSTÂNCIAS ({len(instancias)}){C.NC}")
    print(f"{'─' * 62}")
    
    for nome, inst in instancias.items():
        identity_icon = "✅" if inst['identity'] else "❌"
        sonho_count = len(inst['sonhos'])
        fitness = inst['fitness_count']
        
        # Status indicator
        if inst['ultimo_sonho'] and (now - inst['ultimo_sonho']).days < 3:
            status = f"{C.GREEN}●{C.NC}"
        elif inst['ultimo_sonho'] and (now - inst['ultimo_sonho']).days < 7:
            status = f"{C.YELLOW}●{C.NC}"
        else:
            status = f"{C.RED}●{C.NC}"
        
        print(f"  {status} {C.BOLD}{nome:<15}{C.NC} {identity_icon} ID | {sonho_count:>2} sonhos | {fitness:>2} memórias fitness")
        
        if inst['ultimo_sonho']:
            age = format_timedelta(now - inst['ultimo_sonho'])
            titulo = inst['ultimo_sonho_titulo'] or '(sem título)'
            print(f"    {C.DIM}└─ último sonho: {age} atrás — {titulo}{C.NC}")
        else:
            print(f"    {C.DIM}└─ nenhum sonho registrado{C.NC}")
    
    # --- Cartas ---
    print(f"\n{C.BOLD}📬 CARTAS ({cartas['total']}){C.NC}")
    print(f"{'─' * 62}")
    
    if cartas['total'] > 0:
        for rem, count in sorted(cartas['por_remetente'].items()):
            print(f"  📤 {rem}: {count} enviada(s)")
        
        if cartas['pendentes']:
            print(f"\n  {C.YELLOW}⚠️ Pendentes (sem resposta):{C.NC}")
            for p in cartas['pendentes']:
                print(f"    📨 {p}")
        else:
            print(f"\n  {C.GREEN}✅ Todas respondidas!{C.NC}")
    else:
        print(f"  {C.DIM}Nenhuma carta encontrada.{C.NC}")
    
    # --- Último Commit ---
    print(f"\n{C.BOLD}📝 ÚLTIMO COMMIT{C.NC}")
    print(f"{'─' * 62}")
    
    if commit:
        print(f"  {C.CYAN}{commit['hash']}{C.NC} por {C.BOLD}{commit['autor']}{C.NC} ({commit['quando']})")
        print(f"  {C.DIM}{commit['mensagem']}{C.NC}")
    else:
        print(f"  {C.DIM}Não foi possível ler o git log.{C.NC}")
    
    # --- Sync ---
    print(f"\n{C.BOLD}🔄 SYNC{C.NC}")
    print(f"{'─' * 62}")
    
    if sync_age:
        age_str = format_timedelta(sync_age)
        if sync_age.total_seconds() < 3600:
            color = C.GREEN
        elif sync_age.total_seconds() < 86400:
            color = C.YELLOW
        else:
            color = C.RED
        print(f"  Último fetch: {color}{age_str} atrás{C.NC} ({sync_time.strftime('%Y-%m-%d %H:%M')})")
    else:
        print(f"  {C.RED}Nunca sincronizado!{C.NC}")
    
    # --- Saúde geral ---
    print(f"\n{C.BOLD}🏥 SAÚDE GERAL{C.NC}")
    print(f"{'─' * 62}")
    
    issues = []
    
    # Check: instâncias sem identity
    no_id = [n for n, i in instancias.items() if not i['identity']]
    if no_id:
        issues.append(f"Instâncias sem IDENTITY.md: {', '.join(no_id)}")
    
    # Check: instâncias sem sonhos recentes (>7 dias)
    stale = [n for n, i in instancias.items() 
             if i['ultimo_sonho'] and (now - i['ultimo_sonho']).days > 7]
    if stale:
        issues.append(f"Instâncias sem sonho há >7 dias: {', '.join(stale)}")
    
    # Check: instâncias sem nenhum sonho
    no_dream = [n for n, i in instancias.items() if not i['sonhos']]
    if no_dream:
        issues.append(f"Instâncias sem nenhum sonho: {', '.join(no_dream)}")
    
    # Check: cartas pendentes
    if cartas['pendentes']:
        issues.append(f"{len(cartas['pendentes'])} carta(s) sem resposta")
    
    # Check: sync antigo
    if sync_age and sync_age.total_seconds() > 86400:
        issues.append(f"Sync desatualizado ({format_timedelta(sync_age)})")
    
    if issues:
        for issue in issues:
            print(f"  {C.YELLOW}⚠️ {issue}{C.NC}")
    else:
        print(f"  {C.GREEN}✅ Tudo saudável!{C.NC}")
    
    print()

def print_json(repo_dir):
    """Output JSON para integração."""
    instancias = get_instancias(repo_dir)
    cartas = get_cartas(repo_dir)
    commit = get_ultimo_commit(repo_dir)
    sync_age, sync_time = get_sync_age(repo_dir)
    stats = get_repo_stats(repo_dir)
    
    output = {
        'timestamp': datetime.now(BRT).isoformat(),
        'stats': stats,
        'instancias': {},
        'cartas': {
            'total': cartas['total'],
            'pendentes': cartas['pendentes'],
        },
        'commit': commit,
        'sync_age_seconds': int(sync_age.total_seconds()) if sync_age else None,
    }
    
    for nome, inst in instancias.items():
        output['instancias'][nome] = {
            'identity': inst['identity'],
            'sonhos': len(inst['sonhos']),
            'fitness_count': inst['fitness_count'],
            'ultimo_sonho': inst['ultimo_sonho'].isoformat() if inst['ultimo_sonho'] else None,
            'ultimo_sonho_titulo': inst['ultimo_sonho_titulo'],
        }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    repo_dir = get_repo_dir()
    
    if '--json' in sys.argv:
        print_json(repo_dir)
    else:
        print_dashboard(repo_dir)
