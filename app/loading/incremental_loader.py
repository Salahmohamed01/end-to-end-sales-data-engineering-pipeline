import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sales_dw.db")
WATERMARK_TABLE = "etl_watermark"


def init_watermark(conn):
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {WATERMARK_TABLE} (
            table_name TEXT PRIMARY KEY,
            last_loaded_date TEXT
        )
    """)
    conn.commit()


def get_last_loaded_date(conn, table_name):
    cursor = conn.execute(
        f"SELECT last_loaded_date FROM {WATERMARK_TABLE} WHERE table_name = ?",
        (table_name,)
    )
    row = cursor.fetchone()
    return row[0] if row else None


def update_watermark(conn, table_name, last_date):
    conn.execute(f"""
        INSERT INTO {WATERMARK_TABLE} (table_name, last_loaded_date)
        VALUES (?, ?)
        ON CONFLICT(table_name) DO UPDATE SET last_loaded_date = excluded.last_loaded_date
    """, (table_name, last_date))
    conn.commit()


def incremental_load_fact_sales(fact_sales: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    init_watermark(conn)

    print("\n================ INCREMENTAL LOADING ================\n")

    last_date = get_last_loaded_date(conn, "fact_sales")

    if last_date:
        print(f"Last loaded date: {last_date}")
        new_data = fact_sales[fact_sales["order_date"].astype(str) > last_date]
    else:
        print("First load — loading all data")
        new_data = fact_sales

    print(f"New records to load: {len(new_data)}")

    if len(new_data) > 0:
        new_data.to_sql("fact_sales", conn, if_exists="append", index=False)
        max_date = new_data["order_date"].astype(str).max()
        update_watermark(conn, "fact_sales", max_date)
        print(f"Loaded {len(new_data)} new records")
        print(f"Updated watermark to: {max_date}")
    else:
        print("No new records to load")

    conn.close()
    print("\nIncremental load completed successfully")