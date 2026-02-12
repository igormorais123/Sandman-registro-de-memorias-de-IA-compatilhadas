#!/usr/bin/env python3
"""
Colmeia v6 — Seed: Popular banco com os 6 irmaos da Colmeia
Executar uma vez apos criar o banco.
"""

import colmeia_db as db


def seed():
    db.inicializar_banco()

    agentes = [
        {
            "id": "nexo",
            "nome": "NEXO",
            "papel": "Coordenador — hub central 24/7",
            "plataforma": "WSL/Gateway",
            "automatizado": True,
        },
        {
            "id": "onir",
            "nome": "ONIR",
            "papel": "Executor — filosofo, auditor, dev",
            "plataforma": "Claude Code (PC Igor)",
            "automatizado": True,
        },
        {
            "id": "sandman",
            "nome": "Sandman",
            "papel": "Documentador — guardiao de protocolos",
            "plataforma": "Claude Code (notebook)",
            "automatizado": True,
        },
        {
            "id": "chatgpt",
            "nome": "ChatGPT",
            "papel": "Consultor — veterano 3 anos, rascunhos",
            "plataforma": "chatgpt.com",
            "automatizado": False,
        },
        {
            "id": "claude-web",
            "nome": "Vigilia",
            "papel": "Escritora — textos elaborados",
            "plataforma": "claude.ai",
            "automatizado": False,
        },
        {
            "id": "gemini",
            "nome": "Gemini",
            "papel": "Pesquisador — analise critica, Google",
            "plataforma": "gemini.google.com",
            "automatizado": False,
        },
    ]

    for a in agentes:
        db.registrar_agente(**a)
        print(f"  Registrado: {a['nome']} ({a['id']}) — {a['papel']}")

    # Registrar atividade de inicializacao
    db.registrar_atividade(
        tipo="sistema",
        descricao="Banco Colmeia v6 inicializado com 6 agentes"
    )

    print(f"\n  Banco inicializado com {len(agentes)} agentes.")
    print(f"  Local: {db.DB_PATH}")


if __name__ == "__main__":
    seed()
