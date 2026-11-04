"""Cria e popula o banco no Neon (PostgreSQL) a partir dos scripts de BD I.

Uso:
    export DATABASE_URL="postgresql://usuario:senha@host/db?sslmode=require"
    python setup_db.py            # recria tudo (apaga as tabelas do projeto)
"""
import os
import re
import sys
import unicodedata

import psycopg2

DDL = "sql/SQL_MINECRAFT.sql"
POPULATE = "sql/POPULATE_MINECRAFT.sql"


def sem_acento(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def normaliza_nome(texto: str) -> str:
    return sem_acento(texto).lower()


def main() -> None:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        sys.exit("Defina a variável de ambiente DATABASE_URL antes de rodar.")

    with open(DDL, encoding="utf-8") as f:
        ddl = normaliza_nome(f.read())  # o DDL não tem textos de dados

    with open(POPULATE, encoding="utf-8") as f:
        populate = f.read()

    tabelas = re.findall(r"create table (\w+)", ddl)

    # Em cada INSERT só o cabeçalho (antes de VALUES) é normalizado.
    inserts = []
    for stmt in populate.split(";"):
        stmt = stmt.strip()
        if not stmt:
            continue
        if "VALUES" in stmt.upper():
            i = stmt.upper().index("VALUES")
            inserts.append(normaliza_nome(stmt[:i]) + stmt[i:])
        else:
            inserts.append(stmt)

    conn = psycopg2.connect(dsn)
    try:
        with conn.cursor() as cur:
            for t in reversed(tabelas):
                cur.execute(f"DROP TABLE IF EXISTS {t} CASCADE")
            
            print("1. Criando tabelas (DDL)...")
            cur.execute(ddl)
            
            print("2. Povoando as tabelas (POPULATE)...")
            for stmt in inserts:
                cur.execute(stmt)
            
            print(f"\n{len(tabelas)} tabelas criadas, {len(inserts)} cargas executadas.\n")
            for t in tabelas:
                cur.execute(f"SELECT COUNT(*) FROM {t}")
                print(f"  {t:<24} {cur.fetchone()[0]:>3} linhas")
        conn.commit()
        print("\nBanco de dados montado com sucesso!")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
