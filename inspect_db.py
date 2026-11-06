#!/usr/bin/env python3
"""Inspect the Grova listings DB — list all tables, columns, row counts, and sample data.

Usage:
    python3 inspect_db.py
    python3 inspect_db.py --table field_value
    python3 inspect_db.py --table listing --sample 5

Env vars (or pass as args):
    DB_HOST   default: 127.0.0.1
    DB_PORT   default: 15432
    DB_NAME   default: listings
    DB_USER   default: listings_admin
    DB_PASS   required
    DB_SSL    default: require
"""

import argparse
import os

import psycopg2
import psycopg2.extras


def get_connection(password: str = ""):
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "15432")),
        dbname=os.environ.get("DB_NAME", "listings"),
        user=os.environ.get("DB_USER", "listings_admin"),
        password=password or os.environ.get("DB_PASS", ""),
        sslmode=os.environ.get("DB_SSL", "require"),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def inspect(
    password: str,
    table: str = None,
    sample: int = 2,
    list_only: bool = False,
):
    """Inspect the database. Pass only the password; everything else is optional.

    Examples:
        inspect("your_password")                        # all tables + columns + 2 sample rows
        inspect("your_password", list_only=True)        # just table names and row counts
        inspect("your_password", table="field_value")   # one table in detail
        inspect("your_password", table="listing", sample=5)
        inspect("your_password", table="document", sample=0)  # schema only, no rows
    """
    conn = get_connection(password)
    cur = conn.cursor()
    tables = list_tables(cur)

    print_separator("═")
    print(f"  DATABASE: {os.environ.get('DB_NAME', 'listings')}   ({len(tables)} tables)")
    print_separator("═")
    print(f"  {'Table':<35} {'Rows':>8}")
    print_separator()
    for t in tables:
        count = get_row_count(cur, t["table_name"])
        print(f"  {t['table_name']:<35} {count:>8}")
    print()

    if list_only:
        conn.close()
        return

    if table:
        table_names = [t["table_name"] for t in tables]
        if table not in table_names:
            print(f"ERROR: table '{table}' not found. Available: {', '.join(table_names)}")
            conn.close()
            return
        print_table_detail(cur, table, sample)
    else:
        for t in tables:
            print_table_detail(cur, t["table_name"], sample)

    conn.close()


def list_tables(cur):
    cur.execute("""
        SELECT
            t.table_name,
            obj_description(pc.oid, 'pg_class') AS description
        FROM information_schema.tables t
        JOIN pg_class pc ON pc.relname = t.table_name
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name
    """)
    return cur.fetchall()


def get_row_count(cur, table):
    cur.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
    return cur.fetchone()["cnt"]


def get_columns(cur, table):
    cur.execute("""
        SELECT
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
    """, (table,))
    return cur.fetchall()


def get_indexes(cur, table):
    cur.execute("""
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public' AND tablename = %s
        ORDER BY indexname
    """, (table,))
    return cur.fetchall()


def get_sample(cur, table, n):
    cur.execute(f"SELECT * FROM {table} LIMIT %s", (n,))
    return cur.fetchall()


def print_separator(char="─", width=80):
    print(char * width)


def print_table_detail(cur, table, sample_rows):
    count = get_row_count(cur, table)
    cols = get_columns(cur, table)
    indexes = get_indexes(cur, table)

    print_separator("═")
    print(f"  TABLE: {table}   ({count} rows)")
    print_separator("═")

    print(f"  {'Column':<35} {'Type':<25} {'Nullable':<10} {'Default'}")
    print_separator()
    for c in cols:
        dtype = c["data_type"]
        if c["character_maximum_length"]:
            dtype += f"({c['character_maximum_length']})"
        default = (c["column_default"] or "")[:40]
        print(f"  {c['column_name']:<35} {dtype:<25} {c['is_nullable']:<10} {default}")

    if indexes:
        print()
        print("  Indexes:")
        for idx in indexes:
            print(f"    {idx['indexname']}: {idx['indexdef']}")

    if sample_rows > 0:
        rows = get_sample(cur, table, sample_rows)
        if rows:
            print()
            print(f"  Sample ({min(sample_rows, len(rows))} rows):")
            print_separator()
            for row in rows:
                for k, v in row.items():
                    val = str(v) if v is not None else "NULL"
                    if len(val) > 120:
                        val = val[:117] + "..."
                    print(f"    {k}: {val}")
                print_separator("-")
    print()


DB_PASSWORD = "MkbLy!Rx3Pf8$lB<}iVw6<p+7!bat8mQ"


def main():
    parser = argparse.ArgumentParser(description="Inspect the Grova listings database")
    parser.add_argument("--table", help="Show detail for a specific table only")
    parser.add_argument("--sample", type=int, default=2, help="Number of sample rows per table (0 = schema only)")
    parser.add_argument("--list-only", action="store_true", help="Just list tables and row counts")
    args = parser.parse_args()

    inspect(
        password=DB_PASSWORD,
        table=args.table,
        sample=args.sample,
        list_only=args.list_only,
    )


# if __name__ == "__main__":
#     main()

# from inspect_db import inspect, DB_PASSWORD
# inspect(DB_PASSWORD, list_only=True)
inspect(DB_PASSWORD, table="field_value", sample=5)
