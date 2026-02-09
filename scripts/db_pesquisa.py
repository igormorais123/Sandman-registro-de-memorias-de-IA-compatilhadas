#!/usr/bin/env python3
"""
Wrapper do api_client.py da skill pesquisador-eleitoral.
Para uso rápido nos heartbeats e cron jobs.

Uso: python3 db_pesquisa.py [stats|candidatos|pesquisas|health]
"""
import subprocess, sys

API_CLIENT = "/root/clawd/skills/pesquisador-eleitoral/api_client.py"

CMD_MAP = {
    "stats": "estatisticas",
    "eleitores": "eleitores --limit 5",
    "candidatos": "candidatos", 
    "pesquisas": "pesquisas",
    "health": "login",
}

cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
api_cmd = CMD_MAP.get(cmd, cmd)
subprocess.run(f"python3 {API_CLIENT} {api_cmd}", shell=True)
