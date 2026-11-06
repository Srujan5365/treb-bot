#!/usr/bin/env python3
"""Export Grova listings DB schema + sample data to ListingsDB.xlsx.

One sheet per table. Each sheet has:
  Column A — column name
  Column B — data type
  Column C → onwards — one sample value per row of data

Run:
    python3 create_db_excel.py
"""

import os
import psycopg2
import psycopg2.extras
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

DB_PASSWORD = "MkbLy!Rx3Pf8$lB<}iVw6<p+7!bat8mQ"
OUTPUT_FILE = "ListingsDB.xlsx"
SAMPLE_ROWS = 3


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "15432")),
        dbname=os.environ.get("DB_NAME", "listings"),
        user=os.environ.get("DB_USER", "listings_admin"),
        password=DB_PASSWORD,
        sslmode=os.environ.get("DB_SSL", "require"),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def get_tables(cur):
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    return [r["table_name"] for r in cur.fetchall()]


def get_columns(cur, table):
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """, (table,))
    return cur.fetchall()


def get_sample_data(cur, table, n):
    cur.execute(f"SELECT * FROM {table} LIMIT %s", (n,))
    return cur.fetchall()


def style_header_row(ws, row_num, num_cols):
    header_fill = PatternFill("solid", fgColor="2B5FA8")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=row_num, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")


def style_column_name_cell(cell):
    cell.font = Font(bold=True, size=10)
    cell.fill = PatternFill("solid", fgColor="EBF1FA")
    cell.alignment = Alignment(vertical="center")


def build_excel(password=DB_PASSWORD, output=OUTPUT_FILE, sample_rows=SAMPLE_ROWS):
    conn = get_connection()
    cur = conn.cursor()

    tables = get_tables(cur)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default empty sheet

    # ── Summary sheet ────────────────────────────────────────────────────
    summary = wb.create_sheet("_Summary")
    summary.column_dimensions["A"].width = 30
    summary.column_dimensions["B"].width = 12

    summary.append(["Table", "Row Count"])
    style_header_row(summary, 1, 2)

    for table in tables:
        cur.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
        count = cur.fetchone()["cnt"]
        summary.append([table, count])

    # ── One sheet per table ──────────────────────────────────────────────
    for table in tables:
        cols = get_columns(cur, table)
        samples = get_sample_data(cur, table, sample_rows)

        # Sheet name max 31 chars (Excel limit)
        sheet_name = table[:31]
        ws = wb.create_sheet(sheet_name)

        # Build header row: Column Name | Type | Sample 1 | Sample 2 | Sample 3
        headers = ["Column Name", "Type"] + [f"Sample {i+1}" for i in range(len(samples))]
        ws.append(headers)
        style_header_row(ws, 1, len(headers))
        ws.row_dimensions[1].height = 20

        # One row per column in the table
        for col_info in cols:
            col_name = col_info["column_name"]
            dtype = col_info["data_type"]
            if col_info["character_maximum_length"]:
                dtype += f"({col_info['character_maximum_length']})"

            sample_values = []
            for sample_row in samples:
                val = sample_row.get(col_name)
                if val is None:
                    sample_values.append("")
                else:
                    text = str(val)
                    sample_values.append(text[:200])  # cap long values

            ws.append([col_name, dtype] + sample_values)
            style_column_name_cell(ws.cell(row=ws.max_row, column=1))

        # Column widths
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 28
        for i in range(len(samples)):
            ws.column_dimensions[get_column_letter(3 + i)].width = 45

        # Freeze header row
        ws.freeze_panes = "A2"

    conn.close()

    wb.save(output)
    print(f"Saved: {output}  ({len(tables)} sheets + summary)")


if __name__ == "__main__":
    build_excel()
