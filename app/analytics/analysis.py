import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sales_dw.db")

plt.style.use("ggplot")


def run_analysis():
    print("\n================ DATA ANALYSIS ================\n")

    conn = sqlite3.connect(DB_PATH)

    # 1. Sales per Year
    query1 = """
    SELECT d.year, SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.order_date
    GROUP BY d.year
    ORDER BY d.year
    """
    sales_per_year = pd.read_sql(query1, conn)
    print("Total Sales per Year:")
    print(sales_per_year, "\n")

    plt.figure(figsize=(10, 6))
    plt.bar(sales_per_year["year"].astype(str), sales_per_year["total_sales"])
    plt.title("Total Sales per Year", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Total Sales")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # 2. Sales per Month
    query2 = """
    SELECT d.month, SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.order_date
    GROUP BY d.month
    ORDER BY d.month
    """
    sales_per_month = pd.read_sql(query2, conn)
    print("Total Sales per Month:")
    print(sales_per_month, "\n")

    plt.figure(figsize=(10, 6))
    plt.plot(sales_per_month["month"], sales_per_month["total_sales"], marker='o')
    plt.title("Total Sales per Month", fontsize=14)
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 3. Top 10 Products
    query3 = """
    SELECT f.product_id, SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    GROUP BY f.product_id
    ORDER BY total_sales DESC
    LIMIT 10
    """
    top_products = pd.read_sql(query3, conn)
    print("Top 10 Products:")
    print(top_products, "\n")

    plt.figure(figsize=(10, 6))
    plt.bar(top_products["product_id"].astype(str), top_products["total_sales"])
    plt.title("Top 10 Products by Sales", fontsize=14)
    plt.xlabel("Product ID")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # 4. Top 10 Customers
    query4 = """
    SELECT f.customer_id, SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    GROUP BY f.customer_id
    ORDER BY total_sales DESC
    LIMIT 10
    """
    top_customers = pd.read_sql(query4, conn)
    print("Top 10 Customers:")
    print(top_customers, "\n")

    plt.figure(figsize=(10, 6))
    plt.bar(top_customers["customer_id"].astype(str), top_customers["total_sales"])
    plt.title("Top 10 Customers", fontsize=14)
    plt.xlabel("Customer ID")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # 5. Sales per Category
    query5 = """
    SELECT p.category_id, SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.category_id
    ORDER BY total_sales DESC
    """
    sales_per_category = pd.read_sql(query5, conn)
    print("Sales per Category:")
    print(sales_per_category, "\n")

    plt.figure(figsize=(10, 6))
    plt.bar(sales_per_category["category_id"].astype(str), sales_per_category["total_sales"])
    plt.title("Sales per Category", fontsize=14)
    plt.xlabel("Category ID")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    conn.close()
    print("\nAnalysis completed successfully")


if __name__ == "__main__":
    run_analysis()