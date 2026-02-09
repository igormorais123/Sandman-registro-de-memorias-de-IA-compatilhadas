#!/usr/bin/env python3
"""
INTEIA API Client — Pesquisador Eleitoral

Cliente Python para interagir com a API de Pesquisa Eleitoral DF 2026.
Usado pelo Clawd (Clawdbot) e por outras instâncias Claude Code.

Uso:
    python3 api_client.py login
    python3 api_client.py eleitores [--filtro chave=valor] [--limit N]
    python3 api_client.py eleitor <id>
    python3 api_client.py candidatos
    python3 api_client.py templates
    python3 api_client.py template <id>
    python3 api_client.py pesquisas [--status STATUS]
    python3 api_client.py pesquisa <id>
    python3 api_client.py criar-pesquisa --titulo TITULO --tipo TIPO --perguntas ARQUIVO.json
    python3 api_client.py iniciar-pesquisa <id> --eleitores IDS
    python3 api_client.py respostas <pesquisa_id>
    python3 api_client.py status-pesquisa <id>
    python3 api_client.py estatisticas

API Base: https://api.inteia.com.br
Auth: JWT Bearer token (1h expiry)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# ============================================
# CONFIGURAÇÃO
# ============================================

API_BASE = os.environ.get("INTEIA_API_URL", "https://api.inteia.com.br")
API_USER = os.environ.get("INTEIA_API_USER", "professorigor")
API_PASS = os.environ.get("INTEIA_API_PASS", "professorigor")
TOKEN_FILE = Path(__file__).parent / ".token_cache"


# ============================================
# HTTP CLIENT (sem dependências externas)
# ============================================

def _request(method: str, path: str, data: dict = None, token: str = None,
             params: dict = None) -> dict:
    """Faz requisição HTTP e retorna JSON."""
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urlencode(params)

    body = None
    if data:
        body = json.dumps(data).encode("utf-8")

    req = Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"❌ HTTP {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"❌ Conexão falhou: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ============================================
# AUTENTICAÇÃO
# ============================================

def login(usuario: str = API_USER, senha: str = API_PASS) -> str:
    """Faz login e retorna JWT token. Cacheia em arquivo."""
    # Verificar cache
    if TOKEN_FILE.exists():
        cached = json.loads(TOKEN_FILE.read_text())
        if cached.get("expires_at", 0) > time.time():
            return cached["token"]

    resp = _request("POST", "/api/v1/auth/login", {
        "usuario": usuario,
        "senha": senha,
    })
    token = resp["access_token"]

    # Cachear (expira em 50min para margem de segurança)
    TOKEN_FILE.write_text(json.dumps({
        "token": token,
        "expires_at": time.time() + 3000,
    }))
    return token


def get_token() -> str:
    """Obtém token (do cache ou fazendo login)."""
    return login()


# ============================================
# ELEITORES
# ============================================

def listar_eleitores(filtros: dict = None, pagina: int = 1,
                     por_pagina: int = 20) -> dict:
    """Lista eleitores com filtros opcionais."""
    token = get_token()
    params = {"pagina": pagina, "por_pagina": por_pagina}
    if filtros:
        params.update(filtros)
    return _request("GET", "/api/v1/eleitores/", token=token, params=params)


def obter_eleitor(eleitor_id: str) -> dict:
    """Obtém perfil completo de um eleitor."""
    token = get_token()
    return _request("GET", f"/api/v1/eleitores/{eleitor_id}", token=token)


def estatisticas_eleitores() -> dict:
    """Obtém estatísticas de distribuição dos eleitores."""
    token = get_token()
    return _request("GET", "/api/v1/eleitores/estatisticas", token=token)


# ============================================
# CANDIDATOS
# ============================================

def listar_candidatos() -> list:
    """Lista todos os candidatos DF 2026."""
    token = get_token()
    return _request("GET", "/api/v1/candidatos/", token=token)


# ============================================
# TEMPLATES
# ============================================

def listar_templates() -> list:
    """Lista templates de pesquisa disponíveis."""
    token = get_token()
    return _request("GET", "/api/v1/templates/", token=token)


def obter_template(template_id: str) -> dict:
    """Obtém template completo com perguntas."""
    token = get_token()
    return _request("GET", f"/api/v1/templates/{template_id}", token=token)


# ============================================
# PESQUISAS
# ============================================

def criar_pesquisa(titulo: str, tipo: str = "mista",
                   descricao: str = "", perguntas: list = None,
                   instrucao_geral: str = None) -> dict:
    """Cria uma nova pesquisa."""
    token = get_token()
    data = {
        "titulo": titulo,
        "tipo": tipo,
        "descricao": descricao,
    }
    if perguntas:
        data["perguntas"] = perguntas
    if instrucao_geral:
        data["instrucao_geral"] = instrucao_geral
    return _request("POST", "/api/v1/pesquisas/", data=data, token=token)


def listar_pesquisas(status: str = None, pagina: int = 1,
                     por_pagina: int = 20) -> dict:
    """Lista pesquisas com filtros."""
    token = get_token()
    params = {"pagina": pagina, "por_pagina": por_pagina}
    if status:
        params["status"] = status
    return _request("GET", "/api/v1/pesquisas/", token=token, params=params)


def obter_pesquisa(pesquisa_id: int) -> dict:
    """Obtém pesquisa completa com perguntas e respostas."""
    token = get_token()
    return _request("GET", f"/api/v1/pesquisas/{pesquisa_id}", token=token)


def iniciar_pesquisa(pesquisa_id: int, eleitor_ids: list = None,
                     amostra_tamanho: int = None) -> dict:
    """Inicia execução de uma pesquisa."""
    token = get_token()
    data = {}
    if eleitor_ids:
        data["eleitor_ids"] = eleitor_ids
    if amostra_tamanho:
        data["amostra_tamanho"] = amostra_tamanho
    return _request("POST", f"/api/v1/pesquisas/{pesquisa_id}/iniciar",
                     data=data, token=token)


def pausar_pesquisa(pesquisa_id: int) -> dict:
    """Pausa uma pesquisa em execução."""
    token = get_token()
    return _request("POST", f"/api/v1/pesquisas/{pesquisa_id}/pausar", token=token)


def retomar_pesquisa(pesquisa_id: int) -> dict:
    """Retoma uma pesquisa pausada."""
    token = get_token()
    return _request("POST", f"/api/v1/pesquisas/{pesquisa_id}/retomar", token=token)


def respostas_pesquisa(pesquisa_id: int, pagina: int = 1,
                       por_pagina: int = 100) -> dict:
    """Obtém respostas de uma pesquisa."""
    token = get_token()
    params = {"pagina": pagina, "por_pagina": por_pagina}
    return _request("GET", f"/api/v1/pesquisas/{pesquisa_id}/respostas",
                     token=token, params=params)


def status_pesquisa(pesquisa_id: int) -> dict:
    """Obtém status atual de uma pesquisa."""
    token = get_token()
    return _request("GET", f"/api/v1/pesquisas/{pesquisa_id}/status", token=token)


# ============================================
# ENTREVISTAS
# ============================================

def criar_entrevista(titulo: str, perguntas: list,
                     eleitor_ids: list = None,
                     tipo: str = "mista",
                     tipo_respondente: str = "eleitor") -> dict:
    """Cria uma nova entrevista."""
    token = get_token()
    data = {
        "titulo": titulo,
        "tipo": tipo,
        "perguntas": perguntas,
        "tipo_respondente": tipo_respondente,
    }
    if eleitor_ids:
        data["eleitores_ids"] = eleitor_ids
    return _request("POST", "/api/v1/entrevistas/", data=data, token=token)


def executar_entrevista(entrevista_id: str) -> dict:
    """Inicia execução de uma entrevista."""
    token = get_token()
    return _request("POST", f"/api/v1/entrevistas/{entrevista_id}/executar", token=token)


def obter_entrevista(entrevista_id: str) -> dict:
    """Obtém entrevista com resultados."""
    token = get_token()
    return _request("GET", f"/api/v1/entrevistas/{entrevista_id}", token=token)


# ============================================
# RESULTADOS
# ============================================

def obter_resultados(pesquisa_id: int) -> dict:
    """Obtém análise completa de uma pesquisa."""
    token = get_token()
    return _request("GET", f"/api/v1/resultados/{pesquisa_id}", token=token)


# ============================================
# CLI
# ============================================

def main():
    parser = argparse.ArgumentParser(description="INTEIA API Client")
    sub = parser.add_subparsers(dest="comando")

    # login
    sub.add_parser("login", help="Testar autenticação")

    # eleitores
    p_el = sub.add_parser("eleitores", help="Listar eleitores")
    p_el.add_argument("--limit", type=int, default=10)
    p_el.add_argument("--filtro", nargs="*", help="chave=valor")

    # eleitor
    p_e1 = sub.add_parser("eleitor", help="Obter eleitor por ID")
    p_e1.add_argument("id")

    # estatisticas
    sub.add_parser("estatisticas", help="Estatísticas dos eleitores")

    # candidatos
    sub.add_parser("candidatos", help="Listar candidatos")

    # templates
    sub.add_parser("templates", help="Listar templates")
    p_t = sub.add_parser("template", help="Obter template")
    p_t.add_argument("id")

    # pesquisas
    p_ps = sub.add_parser("pesquisas", help="Listar pesquisas")
    p_ps.add_argument("--status", default=None)

    # pesquisa
    p_p = sub.add_parser("pesquisa", help="Obter pesquisa")
    p_p.add_argument("id", type=int)

    # respostas
    p_r = sub.add_parser("respostas", help="Respostas de pesquisa")
    p_r.add_argument("id", type=int)

    # criar-pesquisa
    p_cp = sub.add_parser("criar-pesquisa", help="Criar pesquisa")
    p_cp.add_argument("--titulo", required=True)
    p_cp.add_argument("--tipo", default="mista")
    p_cp.add_argument("--descricao", default="")
    p_cp.add_argument("--perguntas", help="Arquivo JSON com perguntas")

    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    if args.comando == "login":
        token = login()
        print(f"✅ Login OK — Token: {token[:20]}...")

    elif args.comando == "eleitores":
        filtros = {}
        if args.filtro:
            for f in args.filtro:
                k, v = f.split("=", 1)
                filtros[k] = v
        r = listar_eleitores(filtros, por_pagina=args.limit)
        print(f"📊 Total: {r.get('total', '?')}")
        for e in r.get("eleitores", []):
            print(f"  [{e.get('id','')}] {e.get('nome','')} | "
                  f"{e.get('regiao_administrativa','')} | "
                  f"{e.get('cluster_socioeconomico','')}")

    elif args.comando == "eleitor":
        r = obter_eleitor(args.id)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif args.comando == "estatisticas":
        r = estatisticas_eleitores()
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif args.comando == "candidatos":
        r = listar_candidatos()
        items = r if isinstance(r, list) else r.get("candidatos", r.get("items", []))
        print(f"📊 Total: {len(items)}")
        for c in items:
            print(f"  {c.get('nome','')} | {c.get('partido','')} | {c.get('cargo','')}")

    elif args.comando == "templates":
        r = listar_templates()
        items = r if isinstance(r, list) else r.get("templates", [])
        print(f"📋 Total: {len(items)}")
        for t in items:
            print(f"  [{t.get('id','')}] {t.get('titulo', t.get('nome',''))} | "
                  f"{t.get('categoria','')}")

    elif args.comando == "template":
        r = obter_template(args.id)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif args.comando == "pesquisas":
        r = listar_pesquisas(status=args.status)
        print(f"📊 Total: {r.get('total', '?')}")
        for p in r.get("pesquisas", []):
            print(f"  [{p.get('status','')}] {p.get('titulo','')} | "
                  f"eleitores: {p.get('total_eleitores',0)}")

    elif args.comando == "pesquisa":
        r = obter_pesquisa(args.id)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif args.comando == "respostas":
        r = respostas_pesquisa(args.id)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif args.comando == "criar-pesquisa":
        perguntas = None
        if args.perguntas:
            perguntas = json.loads(Path(args.perguntas).read_text())
        r = criar_pesquisa(args.titulo, args.tipo, args.descricao, perguntas)
        print(f"✅ Pesquisa criada: ID={r.get('id')}")
        print(json.dumps(r, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
