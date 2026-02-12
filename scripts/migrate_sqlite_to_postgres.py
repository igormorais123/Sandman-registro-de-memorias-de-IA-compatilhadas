#!/usr/bin/env python3
"""
Colmeia v6 — Migracao SQLite → PostgreSQL
Exporta dados do SQLite local e importa no PostgreSQL (Render).

Uso:
  python migrate_sqlite_to_postgres.py --preview     # mostra SQL sem executar
  python migrate_sqlite_to_postgres.py --url "postgresql://..."  # executa migracao

Requisitos:
  pip install psycopg2-binary
"""

import argparse
import json
import sqlite3
import sys
import io
import os
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "operacional" / "banco" / "colmeia.db"
SCHEMA_PG = SCRIPT_DIR.parent / "operacional" / "banco" / "schema_postgres.sql"

TABELAS = ["agentes", "tarefas", "mensagens", "atividades", "documentos", "notificacoes", "subscriptions_tarefa"]

# Colunas booleanas que precisam de conversao 0/1 → True/False
BOOL_COLS = {
    "agentes": ["automatizado"],
    "notificacoes": ["entregue"],
    "subscriptions_tarefa": ["ativo"],
}


def extrair_dados_sqlite():
    """Extrai todos os dados do SQLite."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    dados = {}
    for tabela in TABELAS:
        try:
            rows = conn.execute(f"SELECT * FROM {tabela}").fetchall()
            dados[tabela] = [dict(r) for r in rows]
        except Exception as e:
            print(f"  AVISO: Tabela {tabela} nao encontrada ({e})")
            dados[tabela] = []
    conn.close()
    return dados


def converter_booleans(tabela, row):
    """Converte 0/1 do SQLite para True/False."""
    cols = BOOL_COLS.get(tabela, [])
    for col in cols:
        if col in row and row[col] is not None:
            row[col] = bool(row[col])
    return row


def gerar_inserts(dados):
    """Gera SQL de INSERT para PostgreSQL."""
    sql_parts = []
    for tabela, rows in dados.items():
        if not rows:
            continue
        sql_parts.append(f"\n-- {tabela}: {len(rows)} registros")
        for row in rows:
            row = converter_booleans(tabela, row)
            colunas = ", ".join(row.keys())
            valores = []
            for v in row.values():
                if v is None:
                    valores.append("NULL")
                elif isinstance(v, bool):
                    valores.append("TRUE" if v else "FALSE")
                elif isinstance(v, (int, float)):
                    valores.append(str(v))
                else:
                    escaped = str(v).replace("'", "''")
                    valores.append(f"'{escaped}'")
            valores_str = ", ".join(valores)
            sql_parts.append(f"INSERT INTO {tabela} ({colunas}) VALUES ({valores_str}) ON CONFLICT DO NOTHING;")

    # Reset sequences
    for tabela in ["tarefas", "mensagens", "atividades", "documentos", "notificacoes", "subscriptions_tarefa"]:
        if dados.get(tabela):
            sql_parts.append(f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), (SELECT COALESCE(MAX(id), 0) FROM {tabela}));")

    return "\n".join(sql_parts)


def executar_migracao(url, schema_sql, insert_sql):
    """Executa migracao no PostgreSQL."""
    try:
        import psycopg2
    except ImportError:
        print("ERRO: psycopg2 nao instalado. Execute: pip install psycopg2-binary")
        sys.exit(1)

    conn = psycopg2.connect(url)
    cur = conn.cursor()

    print("  [1/3] Criando schema...")
    cur.execute(schema_sql)
    conn.commit()

    print("  [2/3] Inserindo dados...")
    cur.execute(insert_sql)
    conn.commit()

    print("  [3/3] Verificando...")
    for tabela in TABELAS:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cur.fetchone()[0]
        print(f"    {tabela}: {count} registros")

    cur.close()
    conn.close()
    print("\n  Migracao concluida com sucesso!")


def main():
    parser = argparse.ArgumentParser(description="Migrar SQLite → PostgreSQL")
    parser.add_argument("--preview", action="store_true", help="Apenas mostra SQL, nao executa")
    parser.add_argument("--url", help="URL do PostgreSQL (ex: postgresql://user:pass@host:5432/db)")
    parser.add_argument("--export-sql", help="Exportar SQL para arquivo")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"ERRO: Banco nao encontrado: {DB_PATH}")
        sys.exit(1)

    print(f"  Fonte: {DB_PATH}")
    dados = extrair_dados_sqlite()

    for tabela, rows in dados.items():
        print(f"    {tabela}: {len(rows)} registros")

    with open(SCHEMA_PG, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    insert_sql = gerar_inserts(dados)

    if args.preview:
        print("\n--- SCHEMA ---")
        print(schema_sql)
        print("\n--- INSERTS ---")
        print(insert_sql)
    elif args.export_sql:
        full_sql = schema_sql + "\n\n" + insert_sql
        with open(args.export_sql, "w", encoding="utf-8") as f:
            f.write(full_sql)
        print(f"\n  SQL exportado para: {args.export_sql}")
    elif args.url:
        executar_migracao(args.url, schema_sql, insert_sql)
    else:
        print("\n  Use --preview para ver SQL, --url para executar, ou --export-sql para arquivo")


if __name__ == "__main__":
    main()
