import pandas as pd


def build_dimensions(dataframes):
    customers_df = dataframes["customers"].copy()
    products_df = dataframes["products"].copy()
    orders_df = dataframes["orders"].copy()

    # Dim Customers
    dim_customers = customers_df[
        ["customer_id", "city", "signup_date"]
    ].drop_duplicates()

    # Dim Products
    dim_products = products_df[
        ["product_id", "category_id", "supplier_id", "price"]
    ].drop_duplicates()

    # Dim Date
    dim_date = orders_df[["order_date"]].drop_duplicates()
    dim_date["year"] = dim_date["order_date"].dt.year
    dim_date["month"] = dim_date["order_date"].dt.month
    dim_date["day"] = dim_date["order_date"].dt.day

    return dim_customers, dim_products, dim_date


def build_fact_table(dataframes):
    orders_df = dataframes["orders"]
    order_items_df = dataframes["order_items"]

    # Merge orders + order_items
    fact_sales = order_items_df.merge(
        orders_df,
        on="order_id",
        how="inner"
    )

    # Select needed columns
    fact_sales = fact_sales[
        [
            "order_id",
            "product_id",
            "customer_id",
            "order_date",
            "qty",
            "total_amount",
        ]
    ]

    fact_sales.rename(columns={"qty": "quantity"}, inplace=True)

    return fact_sales


def preview_warehouse(dim_customers, dim_products, dim_date, fact_sales):
    print("\n================ DATA WAREHOUSE PREVIEW ================\n")

    print("Dim Customers:")
    print(dim_customers.head(), "\n")

    print("Dim Products:")
    print(dim_products.head(), "\n")

    print("Dim Date:")
    print(dim_date.head(), "\n")

    print("Fact Sales:")
    print(fact_sales.head(), "\n")