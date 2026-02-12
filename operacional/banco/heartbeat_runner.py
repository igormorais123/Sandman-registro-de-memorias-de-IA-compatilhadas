#!/usr/bin/env python3
"""
Colmeia v6 — Heartbeat Runner
Executa o ciclo completo de heartbeat para um agente.

Uso:
  python heartbeat_runner.py <agent_id>
  python heartbeat_runner.py onir
  python heartbeat_runner.py nexo --dry-run

Ciclo:
  1. Registrar heartbeat
  2. Ler WORKING.md
  3. Checar tarefas (em_progresso, atribuida)
  4. Checar mencoes pendentes
  5. Decidir acao
  6. Atualizar WORKING.md
  7. Registrar log estruturado
"""

import argparse
import json
import sys
import io
import os
import time
from datetime import datetime
from pathlib import Path

# Forcar UTF-8 no stdout (Windows usa cp1252)
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Setup paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
INSTANCIAS_DIR = REPO_ROOT / "instancias"
LOGS_DIR = REPO_ROOT / "operacional" / "logs"

sys.path.insert(0, str(SCRIPT_DIR))
import colmeia_db as db


# Mapeamento agent_id -> nome da pasta em instancias/
AGENT_DIRS = {
    "nexo": "nexo",
    "onir": "onir",
    "sandman": "sandman",
    "helena": "helena",
    "chatgpt": "chatgpt",
    "claude-web": "claude-web",
    "gemini": "gemini",
}


def log_ciclo(agente_id, resultado, detalhes, duracao_ms):
    """Grava log estruturado JSONL do ciclo."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"heartbeat_{hoje}.jsonl"

    entrada = {
        "timestamp": datetime.now().isoformat(),
        "agente": agente_id,
        "resultado": resultado,
        "detalhes": detalhes,
        "duracao_ms": duracao_ms,
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

    return str(log_file)


def ler_working(agente_id):
    """Le o WORKING.md do agente. Retorna conteudo ou None."""
    dir_name = AGENT_DIRS.get(agente_id, agente_id)
    working_path = INSTANCIAS_DIR / dir_name / "WORKING.md"

    if not working_path.exists():
        return None, str(working_path)

    with open(working_path, "r", encoding="utf-8") as f:
        return f.read(), str(working_path)


ZONA_AGENTE_MARCADOR = "<!-- ZONA DO AGENTE -->"


def _extrair_zona_agente(conteudo):
    """Extrai a zona do agente (preservada entre ciclos) do WORKING.md."""
    if not conteudo or ZONA_AGENTE_MARCADOR not in conteudo:
        return ""
    idx = conteudo.index(ZONA_AGENTE_MARCADOR)
    return conteudo[idx:].strip()


def atualizar_working(agente_id, tarefa=None, progresso="", status="aguardando"):
    """Atualiza o WORKING.md do agente preservando a zona do agente."""
    dir_name = AGENT_DIRS.get(agente_id, agente_id)
    working_path = INSTANCIAS_DIR / dir_name / "WORKING.md"
    working_path.parent.mkdir(parents=True, exist_ok=True)

    # Preservar zona do agente existente
    zona_agente = ""
    if working_path.exists():
        with open(working_path, "r", encoding="utf-8") as f:
            zona_agente = _extrair_zona_agente(f.read())

    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    nome = agente_id.upper()

    if tarefa:
        zona_runner = f"""# WORKING.md — {nome}

## Tarefa Atual
- ID: #{tarefa['id']}
- Titulo: {tarefa['titulo']}
- Status: {tarefa['status']}
- Projeto: {tarefa.get('projeto') or '(nenhum)'}

## Progresso (runner)
{progresso}

## Ultima Atualizacao
{agora}"""
    else:
        zona_runner = f"""# WORKING.md — {nome}

## Tarefa Atual
- ID: (nenhuma)
- Titulo: —
- Status: {status}
- Projeto: —

## Progresso (runner)
{progresso or 'Nenhuma tarefa em andamento.'}

## Ultima Atualizacao
{agora}"""

    # Montar conteudo final: zona runner + zona agente
    if zona_agente:
        conteudo = zona_runner + "\n\n" + zona_agente + "\n"
    else:
        conteudo = zona_runner + f"\n\n{ZONA_AGENTE_MARCADOR}\n## Notas do Agente\n(Escreva aqui — esta secao e preservada entre ciclos)\n"

    with open(working_path, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return str(working_path)


def checar_tarefas(agente_id):
    """Retorna tarefas em_progresso e atribuidas do agente."""
    em_progresso = db.listar_tarefas(status="em_progresso", responsavel=agente_id)
    atribuidas = db.listar_tarefas(status="atribuida", responsavel=agente_id)
    return em_progresso, atribuidas


def checar_mencoes(agente_id):
    """Retorna mencoes/notificacoes pendentes do agente."""
    return db.listar_notificacoes(agente_id, apenas_pendentes=True)


def formatar_resumo_tarefa(t):
    """Formata tarefa para log."""
    return f"#{t['id']} [{t['status']}] {t['titulo']}"


def executar_heartbeat(agente_id, dry_run=False):
    """Executa ciclo completo de heartbeat."""
    inicio = time.time()
    resultado = "HEARTBEAT_OK"
    detalhes = {}

    print(f"\n  === HEARTBEAT: @{agente_id} ===")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. Registrar heartbeat
    if not dry_run:
        db.heartbeat(agente_id)
        db.atualizar_status_agente(agente_id, "acordado")
    print(f"  [1/6] Heartbeat registrado")

    # 2. Ler WORKING.md
    working_conteudo, working_path = ler_working(agente_id)
    if working_conteudo is None:
        print(f"  [2/6] WORKING.md NAO ENCONTRADO: {working_path}")
        print(f"        Criando WORKING.md vazio...")
        if not dry_run:
            atualizar_working(agente_id, status="inicializado")
        detalhes["working_md"] = "criado"
    else:
        print(f"  [2/6] WORKING.md carregado ({len(working_conteudo)} chars)")
        detalhes["working_md"] = "existente"

    # 3. Checar tarefas
    em_progresso, atribuidas = checar_tarefas(agente_id)
    print(f"  [3/6] Tarefas: {len(em_progresso)} em_progresso, {len(atribuidas)} atribuida(s)")
    detalhes["tarefas_em_progresso"] = len(em_progresso)
    detalhes["tarefas_atribuidas"] = len(atribuidas)

    for t in em_progresso:
        print(f"        >> {formatar_resumo_tarefa(t)}")
    for t in atribuidas:
        print(f"        -> {formatar_resumo_tarefa(t)}")

    # 4. Checar mencoes
    mencoes = checar_mencoes(agente_id)
    print(f"  [4/6] Mencoes pendentes: {len(mencoes)}")
    detalhes["mencoes_pendentes"] = len(mencoes)

    for m in mencoes:
        print(f"        @ {m['conteudo']}")

    # 5. Decidir acao
    print(f"  [5/6] Decisao:")
    acao_tomada = None

    if em_progresso:
        tarefa = em_progresso[0]
        resultado = "TRABALHO_CONTINUADO"
        acao_tomada = f"Continuar tarefa #{tarefa['id']}: {tarefa['titulo']}"
        print(f"        CONTINUAR tarefa #{tarefa['id']}: {tarefa['titulo']}")
        if not dry_run:
            atualizar_working(agente_id, tarefa=tarefa, progresso="Continuando trabalho do ciclo anterior.")

    elif atribuidas:
        tarefa = atribuidas[0]
        resultado = "TRABALHO_NOVO"
        acao_tomada = f"Aceitar tarefa #{tarefa['id']}: {tarefa['titulo']}"
        print(f"        ACEITAR tarefa #{tarefa['id']}: {tarefa['titulo']}")
        if not dry_run:
            db.atualizar_tarefa(tarefa["id"], status="em_progresso")
            tarefa["status"] = "em_progresso"
            atualizar_working(agente_id, tarefa=tarefa, progresso="Tarefa aceita neste ciclo. Iniciando execucao.")

    elif mencoes:
        resultado = "MENCOES_PROCESSADAS"
        acao_tomada = f"Processar {len(mencoes)} mencao(oes)"
        print(f"        PROCESSAR {len(mencoes)} mencao(oes)")
        if not dry_run:
            db.marcar_todas_entregues(agente_id)
            atualizar_working(agente_id, progresso=f"Processadas {len(mencoes)} mencao(oes) neste ciclo.")

    else:
        resultado = "HEARTBEAT_OK"
        acao_tomada = "Nenhuma acao necessaria"
        print(f"        HEARTBEAT_OK — nenhuma acao necessaria")
        if not dry_run:
            atualizar_working(agente_id, status="aguardando", progresso="Nenhuma tarefa em andamento.")

    detalhes["acao"] = acao_tomada

    # 6. Finalizar
    if not dry_run:
        db.atualizar_status_agente(agente_id, "dormindo")

    duracao_ms = int((time.time() - inicio) * 1000)
    detalhes["duracao_ms"] = duracao_ms

    print(f"  [6/6] Ciclo concluido em {duracao_ms}ms — {resultado}")

    # Gravar log estruturado
    if not dry_run:
        log_path = log_ciclo(agente_id, resultado, detalhes, duracao_ms)
        print(f"        Log: {log_path}")

    print()
    return resultado, detalhes


def main():
    parser = argparse.ArgumentParser(
        description="Colmeia v6 — Heartbeat Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("agente", help="ID do agente (ex: onir, nexo, sandman)")
    parser.add_argument("--dry-run", action="store_true", help="Simular sem alterar banco/arquivos")
    args = parser.parse_args()

    agente_id = args.agente.lower()

    # Validar agente
    agentes = db.listar_agentes()
    ids_validos = [a["id"] for a in agentes]
    if agente_id not in ids_validos:
        print(f"  ERRO: Agente '{agente_id}' nao encontrado.")
        print(f"  Agentes validos: {', '.join(ids_validos)}")
        sys.exit(1)

    # Garantir banco inicializado
    db.inicializar_banco()

    # Executar com captura de exceptions
    try:
        resultado, detalhes = executar_heartbeat(agente_id, dry_run=args.dry_run)
    except Exception as e:
        # Registrar erro no log estruturado
        duracao_ms = 0
        erro_msg = f"{type(e).__name__}: {e}"
        print(f"  ERRO FATAL: {erro_msg}", file=sys.stderr)
        log_ciclo(agente_id, "ERRO", {"erro": erro_msg, "acao": "exception_nao_tratada"}, duracao_ms)
        sys.exit(2)

    # Exit code baseado no resultado
    if resultado == "HEARTBEAT_OK":
        sys.exit(0)
    elif resultado.startswith("TRABALHO"):
        sys.exit(0)
    elif resultado == "MENCOES_PROCESSADAS":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
