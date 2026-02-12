#!/usr/bin/env python3
"""
Colmeia v6 — CLI de Acesso ao Banco de Dados
Uso: python cli.py <comando> [opcoes]

Exemplos:
  python cli.py agentes
  python cli.py tarefa criar "Titulo" --responsavel ONIR --projeto INTEIA-cursos --prioridade 8
  python cli.py tarefa atribuir 42 --responsavel ONIR
  python cli.py tarefa atualizar 42 --status em_progresso
  python cli.py tarefas --status em_progresso --responsavel ONIR
  python cli.py mensagem criar 42 --de ONIR --conteudo "Resultado..."
  python cli.py mensagens 42
  python cli.py mencoes --para ONIR
  python cli.py heartbeat NEXO
  python cli.py atividades --tipo heartbeat --ultimas 10
  python cli.py standup
  python cli.py standup 2026-02-10
  python cli.py exportar
"""

import argparse
import sys
import json
import io
from datetime import datetime

# Forcar UTF-8 no stdout (Windows usa cp1252 por padrao)
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import colmeia_db as db


def formatar_tarefa(t):
    status_icons = {
        "caixa_entrada": "[  ]",
        "atribuida": "[->]",
        "em_progresso": "[>>]",
        "bloqueada": "[!!]",
        "revisao": "[??]",
        "concluida": "[OK]",
        "cancelada": "[XX]",
    }
    icon = status_icons.get(t["status"], "[??]")
    resp = f" @{t['responsavel_id']}" if t["responsavel_id"] else ""
    proj = f" [{t['projeto']}]" if t["projeto"] else ""
    prio = f" P:{t['prioridade']}" if t["prioridade"] != 5 else ""
    return f"  {icon} #{t['id']}{prio}{proj}{resp} — {t['titulo']}"


def formatar_agente(a):
    status_icons = {
        "dormindo": "zzz",
        "acordado": " * ",
        "ocupado": ">>>",
        "bloqueado": " ! ",
        "supervisionado": " S ",
    }
    icon = status_icons.get(a["status"], "???")
    auto = " [AUTO]" if a["automatizado"] else ""
    hb = f" (ultimo HB: {a['ultimo_heartbeat']})" if a["ultimo_heartbeat"] else ""
    return f"  [{icon}] {a['id']:12s} | {a['nome']:12s} | {a['papel'] or '':20s} | {a['plataforma'] or ''}{auto}{hb}"


def cmd_agentes(args):
    agentes = db.listar_agentes()
    if not agentes:
        print("Nenhum agente registrado. Execute: python seed.py")
        return
    print(f"\n  AGENTES DA COLMEIA ({len(agentes)})")
    print("  " + "-" * 70)
    for a in agentes:
        print(formatar_agente(a))
    print()


def cmd_heartbeat(args):
    ts = db.heartbeat(args.agente)
    print(f"  Heartbeat registrado: {args.agente} em {ts}")


def cmd_tarefa(args):
    if args.acao == "criar":
        tarefa_id = db.criar_tarefa(
            titulo=args.titulo,
            descricao=args.descricao,
            criado_por=args.criado_por,
            prioridade=args.prioridade or 5,
            projeto=args.projeto,
            tags=args.tags.split(",") if args.tags else None,
        )
        if args.responsavel:
            db.atribuir_tarefa(tarefa_id, args.responsavel)
        print(f"  Tarefa #{tarefa_id} criada: {args.titulo}")
        if args.responsavel:
            print(f"  Atribuida a: {args.responsavel}")

    elif args.acao == "atribuir":
        db.atribuir_tarefa(args.id, args.responsavel)
        print(f"  Tarefa #{args.id} atribuida a {args.responsavel}")

    elif args.acao == "atualizar":
        db.atualizar_tarefa(
            args.id,
            status=args.status,
            prioridade=args.prioridade,
            bloqueada_por=args.bloqueada_por,
        )
        mudancas = []
        if args.status:
            mudancas.append(f"status={args.status}")
        if args.prioridade:
            mudancas.append(f"prioridade={args.prioridade}")
        if args.bloqueada_por:
            mudancas.append(f"bloqueada_por={args.bloqueada_por}")
        print(f"  Tarefa #{args.id} atualizada: {', '.join(mudancas)}")

    elif args.acao == "ver":
        t = db.obter_tarefa(args.id)
        if not t:
            print(f"  Tarefa #{args.id} nao encontrada")
            return
        print(f"\n  TAREFA #{t['id']}")
        print(f"  Titulo:      {t['titulo']}")
        print(f"  Status:      {t['status']}")
        print(f"  Responsavel: {t['responsavel_id'] or '(nenhum)'}")
        print(f"  Prioridade:  {t['prioridade']}")
        print(f"  Projeto:     {t['projeto'] or '(nenhum)'}")
        if t["descricao"]:
            print(f"  Descricao:   {t['descricao']}")
        print(f"  Criado:      {t['criado_em']}")
        print(f"  Atualizado:  {t['atualizado_em']}")

        msgs = db.listar_mensagens(args.id)
        if msgs:
            print(f"\n  MENSAGENS ({len(msgs)}):")
            for m in msgs:
                print(f"    [{m['criado_em']}] @{m['de_agente']}: {m['conteudo']}")
        print()


def cmd_tarefas(args):
    tarefas = db.listar_tarefas(
        status=args.status,
        responsavel=args.responsavel,
        projeto=args.projeto,
    )
    if not tarefas:
        print("  Nenhuma tarefa encontrada com esses filtros.")
        return

    filtros = []
    if args.status:
        filtros.append(f"status={args.status}")
    if args.responsavel:
        filtros.append(f"responsavel={args.responsavel}")
    if args.projeto:
        filtros.append(f"projeto={args.projeto}")
    filtro_str = f" ({', '.join(filtros)})" if filtros else ""

    print(f"\n  TAREFAS{filtro_str} — {len(tarefas)} resultado(s)")
    print("  " + "-" * 60)
    for t in tarefas:
        print(formatar_tarefa(t))
    print()


def cmd_mensagem(args):
    if args.acao == "criar":
        mencoes = args.mencoes.split(",") if args.mencoes else None
        db.criar_mensagem(args.tarefa_id, args.de, args.conteudo, mencoes)
        print(f"  Mensagem postada em tarefa #{args.tarefa_id} por @{args.de}")
        if mencoes:
            print(f"  Mencoes: {', '.join('@' + m for m in mencoes)}")


def cmd_mensagens(args):
    msgs = db.listar_mensagens(args.tarefa_id)
    if not msgs:
        print(f"  Nenhuma mensagem na tarefa #{args.tarefa_id}")
        return
    print(f"\n  MENSAGENS — Tarefa #{args.tarefa_id} ({len(msgs)})")
    print("  " + "-" * 60)
    for m in msgs:
        print(f"  [{m['criado_em']}] @{m['de_agente']}:")
        print(f"    {m['conteudo']}")
    print()


def cmd_mencoes(args):
    notifs = db.listar_notificacoes(args.para, apenas_pendentes=not args.todas)
    if not notifs:
        print(f"  Nenhuma notificacao pendente para @{args.para}")
        return
    label = "TODAS" if args.todas else "PENDENTES"
    print(f"\n  NOTIFICACOES {label} — @{args.para} ({len(notifs)})")
    print("  " + "-" * 60)
    for n in notifs:
        entregue = " [entregue]" if n["entregue"] else ""
        print(f"  [{n['criado_em']}] {n['conteudo']}{entregue}")
    print()

    if not args.todas and args.marcar:
        db.marcar_todas_entregues(args.para)
        print(f"  {len(notifs)} notificacao(es) marcada(s) como entregue(s)")


def cmd_notificacoes(args):
    if args.acao == "processar":
        agentes_online = None
        if args.modo == "online":
            agentes_online = db.obter_agentes_online(janela_min=args.janela)
        stats = db.processar_fila_notificacoes(
            agentes_online=agentes_online,
            limite=args.limite,
            retry_delay_min=args.retry_delay_min,
            entregador=f"cli_{args.modo}",
            ignorar_agendamento=args.ignorar_agendamento or args.modo == "all",
        )
        print("\n  PROCESSAMENTO DE NOTIFICACOES")
        print("  " + "-" * 40)
        print(f"  Modo: {args.modo}")
        if agentes_online is not None:
            print(f"  Agentes online: {', '.join(agentes_online) if agentes_online else '(nenhum)'}")
        print(f"  Total: {stats['total']}")
        print(f"  Entregues: {stats['entregues']}")
        print(f"  Reprogramadas: {stats['reprogramadas']}")
        print(f"  Falhas finais: {stats['falhas_finais']}")
        print()


def cmd_subscriptions(args):
    if args.acao == "listar":
        itens = db.listar_subscriptions(
            tarefa_id=args.tarefa_id,
            agente_id=args.agente,
            apenas_ativos=not args.incluir_inativos,
        )
        print(f"\n  SUBSCRIPTIONS ({len(itens)})")
        print("  " + "-" * 40)
        for s in itens:
            ativo = "ativo" if s["ativo"] else "inativo"
            print(f"  tarefa #{s['tarefa_id']} -> @{s['agente_id']} ({ativo}, origem={s['origem']})")
        print()

    elif args.acao == "adicionar":
        ok = db.registrar_subscription(args.tarefa_id, args.agente, origem=args.origem)
        if ok:
            print(f"  Subscription adicionada: tarefa #{args.tarefa_id} -> @{args.agente}")


def cmd_atividades(args):
    atividades = db.listar_atividades(
        tipo=args.tipo,
        agente_id=args.agente,
        desde=args.desde,
        limite=args.ultimas or 20,
    )
    if not atividades:
        print("  Nenhuma atividade encontrada.")
        return
    print(f"\n  FEED DE ATIVIDADES ({len(atividades)})")
    print("  " + "-" * 60)
    for a in atividades:
        agente = f"@{a['agente_id']}" if a["agente_id"] else "sistema"
        print(f"  [{a['criado_em']}] [{a['tipo']:20s}] {agente}: {a['descricao'] or ''}")
    print()


def cmd_standup(args):
    data = args.data if args.data else None
    s = db.gerar_standup(data)
    data_label = s["data"]

    print(f"\n  STANDUP COLMEIA — {data_label}")
    print("  " + "=" * 50)

    if s["concluidas"]:
        print(f"\n  CONCLUIDAS HOJE ({len(s['concluidas'])}):")
        for t in s["concluidas"]:
            print(formatar_tarefa(t))

    if s["em_progresso"]:
        print(f"\n  EM PROGRESSO ({len(s['em_progresso'])}):")
        for t in s["em_progresso"]:
            print(formatar_tarefa(t))

    if s["bloqueadas"]:
        print(f"\n  BLOQUEADAS ({len(s['bloqueadas'])}):")
        for t in s["bloqueadas"]:
            razao = f" — {t['bloqueada_por']}" if t.get("bloqueada_por") else ""
            print(formatar_tarefa(t) + razao)

    if s["revisao"]:
        print(f"\n  AGUARDANDO REVISAO ({len(s['revisao'])}):")
        for t in s["revisao"]:
            print(formatar_tarefa(t))

    if s["heartbeats"]:
        print(f"\n  HEARTBEATS:")
        for agente, total in s["heartbeats"].items():
            print(f"    @{agente}: {total} heartbeats")

    if not any([s["concluidas"], s["em_progresso"], s["bloqueadas"], s["revisao"]]):
        print("\n  Nenhuma atividade de tarefas registrada.")

    print()


def cmd_exportar(args):
    caminho = db.exportar_para_json()
    print(f"  Banco exportado para: {caminho}")


def main():
    parser = argparse.ArgumentParser(
        description="Colmeia v6 — CLI do Banco de Dados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="comando", help="Comando a executar")

    # agentes
    subparsers.add_parser("agentes", help="Listar agentes")

    # heartbeat
    p_hb = subparsers.add_parser("heartbeat", help="Registrar heartbeat")
    p_hb.add_argument("agente", help="ID do agente")

    # tarefa
    p_tarefa = subparsers.add_parser("tarefa", help="Gerenciar tarefa individual")
    sub_tarefa = p_tarefa.add_subparsers(dest="acao", help="Acao")

    p_criar = sub_tarefa.add_parser("criar", help="Criar tarefa")
    p_criar.add_argument("titulo", help="Titulo da tarefa")
    p_criar.add_argument("--descricao", help="Descricao detalhada")
    p_criar.add_argument("--responsavel", help="ID do agente responsavel")
    p_criar.add_argument("--criado-por", dest="criado_por", help="Quem criou")
    p_criar.add_argument("--prioridade", type=int, help="Prioridade 1-10")
    p_criar.add_argument("--projeto", help="Nome do projeto")
    p_criar.add_argument("--tags", help="Tags separadas por virgula")

    p_atribuir = sub_tarefa.add_parser("atribuir", help="Atribuir tarefa")
    p_atribuir.add_argument("id", type=int, help="ID da tarefa")
    p_atribuir.add_argument("--responsavel", required=True, help="ID do agente")

    p_atualizar = sub_tarefa.add_parser("atualizar", help="Atualizar tarefa")
    p_atualizar.add_argument("id", type=int, help="ID da tarefa")
    p_atualizar.add_argument("--status", choices=["caixa_entrada", "atribuida", "em_progresso", "bloqueada", "revisao", "concluida", "cancelada"])
    p_atualizar.add_argument("--prioridade", type=int)
    p_atualizar.add_argument("--bloqueada-por", dest="bloqueada_por")

    p_ver = sub_tarefa.add_parser("ver", help="Ver detalhes da tarefa")
    p_ver.add_argument("id", type=int, help="ID da tarefa")

    # tarefas (listar)
    p_tarefas = subparsers.add_parser("tarefas", help="Listar tarefas")
    p_tarefas.add_argument("--status", help="Filtrar por status")
    p_tarefas.add_argument("--responsavel", help="Filtrar por responsavel")
    p_tarefas.add_argument("--projeto", help="Filtrar por projeto")

    # mensagem
    p_msg = subparsers.add_parser("mensagem", help="Gerenciar mensagens")
    sub_msg = p_msg.add_subparsers(dest="acao", help="Acao")

    p_msg_criar = sub_msg.add_parser("criar", help="Criar mensagem")
    p_msg_criar.add_argument("tarefa_id", type=int, help="ID da tarefa")
    p_msg_criar.add_argument("--de", required=True, help="ID do agente remetente")
    p_msg_criar.add_argument("--conteudo", required=True, help="Conteudo da mensagem")
    p_msg_criar.add_argument("--mencoes", help="IDs separados por virgula para notificar")

    # mensagens (listar)
    p_msgs = subparsers.add_parser("mensagens", help="Listar mensagens de uma tarefa")
    p_msgs.add_argument("tarefa_id", type=int, help="ID da tarefa")

    # mencoes
    p_mencoes = subparsers.add_parser("mencoes", help="Ver notificacoes/mencoes")
    p_mencoes.add_argument("--para", required=True, help="ID do agente")
    p_mencoes.add_argument("--todas", action="store_true", help="Incluir ja entregues")
    p_mencoes.add_argument("--marcar", action="store_true", help="Marcar como entregues")

    # notificacoes (daemon/retry)
    p_notifs = subparsers.add_parser("notificacoes", help="Operacoes da fila de notificacoes")
    sub_notifs = p_notifs.add_subparsers(dest="acao", help="Acao")
    p_notifs_proc = sub_notifs.add_parser("processar", help="Processar fila pendente")
    p_notifs_proc.add_argument("--modo", choices=["online", "all"], default="online")
    p_notifs_proc.add_argument("--janela", type=int, default=90, help="Janela em minutos para considerar agente online")
    p_notifs_proc.add_argument("--limite", type=int, default=100)
    p_notifs_proc.add_argument("--retry-delay-min", dest="retry_delay_min", type=int, default=30)
    p_notifs_proc.add_argument("--ignorar-agendamento", action="store_true", help="Processa mesmo antes da proxima_tentativa")

    # subscriptions de thread
    p_sub = subparsers.add_parser("subscriptions", help="Operacoes de subscriptions por tarefa")
    sub_sub = p_sub.add_subparsers(dest="acao", help="Acao")
    p_sub_list = sub_sub.add_parser("listar", help="Listar subscriptions")
    p_sub_list.add_argument("--tarefa-id", dest="tarefa_id", type=int)
    p_sub_list.add_argument("--agente")
    p_sub_list.add_argument("--incluir-inativos", action="store_true")
    p_sub_add = sub_sub.add_parser("adicionar", help="Adicionar subscription manual")
    p_sub_add.add_argument("tarefa_id", type=int)
    p_sub_add.add_argument("--agente", required=True)
    p_sub_add.add_argument("--origem", default="manual")

    # atividades
    p_ativ = subparsers.add_parser("atividades", help="Feed de atividades")
    p_ativ.add_argument("--tipo", help="Filtrar por tipo")
    p_ativ.add_argument("--agente", help="Filtrar por agente")
    p_ativ.add_argument("--desde", help="Data inicio (YYYY-MM-DD)")
    p_ativ.add_argument("--ultimas", type=int, help="Quantidade de registros")

    # standup
    p_standup = subparsers.add_parser("standup", help="Gerar standup diario")
    p_standup.add_argument("data", nargs="?", help="Data (YYYY-MM-DD, default: hoje)")

    # exportar
    subparsers.add_parser("exportar", help="Exportar banco para JSON")

    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    # Garantir que banco existe
    db.inicializar_banco()

    comandos = {
        "agentes": cmd_agentes,
        "heartbeat": cmd_heartbeat,
        "tarefa": cmd_tarefa,
        "tarefas": cmd_tarefas,
        "mensagem": cmd_mensagem,
        "mensagens": cmd_mensagens,
        "mencoes": cmd_mencoes,
        "notificacoes": cmd_notificacoes,
        "subscriptions": cmd_subscriptions,
        "atividades": cmd_atividades,
        "standup": cmd_standup,
        "exportar": cmd_exportar,
    }

    func = comandos.get(args.comando)
    if func:
        func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
