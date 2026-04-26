import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sales_dw.db")


def load_to_database(dim_customers, dim_products, dim_date):
    conn = sqlite3.connect(DB_PATH)

    print("\n================ LOADING DIMENSIONS TO DATABASE ================\n")

    dim_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
    print("dim_customers loaded")

    dim_products.to_sql("dim_products", conn, if_exists="replace", index=False)
    print("dim_products loaded")

    dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
    print("dim_date loaded")

    conn.close()
    print("\nDimensions loaded successfully")