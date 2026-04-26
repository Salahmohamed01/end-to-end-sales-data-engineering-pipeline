import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sales_dw.db")


def apply_optimizations():
    conn = sqlite3.connect(DB_PATH)

    print("\n================ DATABASE OPTIMIZATION ================\n")

    # Indexes
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_customers_id ON dim_customers(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_customers_city ON dim_customers(city)",
        "CREATE INDEX IF NOT EXISTS idx_products_id ON dim_products(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_products_category ON dim_products(category_id)",
        "CREATE INDEX IF NOT EXISTS idx_date ON dim_date(order_date)",
        "CREATE INDEX IF NOT EXISTS idx_date_year ON dim_date(year)",
        "CREATE INDEX IF NOT EXISTS idx_fact_customer_id ON fact_sales(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_product_id ON fact_sales(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_order_date ON fact_sales(order_date)",
    ]

    for stmt in statements:
        conn.execute(stmt)
        print(f"Applied: {stmt.split('ON')[1].strip()}")

    # Views
    conn.execute("""
        CREATE VIEW IF NOT EXISTS vw_monthly_sales AS
        SELECT d.year, d.month, SUM(f.total_amount) AS revenue, COUNT(*) AS num_orders
        FROM fact_sales f
        JOIN dim_date d ON f.order_date = d.order_date
        GROUP BY d.year, d.month
    """)
    print("Created view: vw_monthly_sales")

    conn.execute("""
        CREATE VIEW IF NOT EXISTS vw_top_products AS
        SELECT f.product_id, p.category_id, SUM(f.total_amount) AS revenue
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY f.product_id
        ORDER BY revenue DESC
    """)
    print("Created view: vw_top_products")

    conn.commit()
    conn.close()

    print("\nDatabase optimization completed successfully ✅")