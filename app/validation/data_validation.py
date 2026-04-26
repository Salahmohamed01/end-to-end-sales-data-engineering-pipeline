import pandas as pd
import os
from app.config.config_loader import load_config


def save_invalid_records(df, filename):
    config = load_config()
    invalid_path = config["paths"]["invalid_data"]

    if not os.path.exists(invalid_path):
        os.makedirs(invalid_path)

    if len(df) > 0:
        filepath = os.path.join(invalid_path, filename)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} invalid records to {filepath}")


def validate_dataframes(dataframes):
    customers_df = dataframes["customers"]
    orders_df = dataframes["orders"]
    order_items_df = dataframes["order_items"]
    products_df = dataframes["products"]

    print("\n================ DATA VALIDATION ================\n")

    validation_passed = True

    # 1) Invalid customer_id in orders
    invalid_customers = orders_df[
        ~orders_df["customer_id"].isin(customers_df["customer_id"])
    ]
    print(f"Invalid customer_id records in orders: {len(invalid_customers)}")
    if len(invalid_customers) > 0:
        save_invalid_records(invalid_customers, "invalid_orders_customers.csv")
        validation_passed = False

    # 2) Invalid order_id in order_items
    invalid_orders = order_items_df[
        ~order_items_df["order_id"].isin(orders_df["order_id"])
    ]
    print(f"Invalid order_id records in order_items: {len(invalid_orders)}")
    if len(invalid_orders) > 0:
        save_invalid_records(invalid_orders, "invalid_order_items_orders.csv")
        validation_passed = False

    # 3) Invalid product_id in order_items
    invalid_products = order_items_df[
        ~order_items_df["product_id"].isin(products_df["product_id"])
    ]
    print(f"Invalid product_id records in order_items: {len(invalid_products)}")
    if len(invalid_products) > 0:
        save_invalid_records(invalid_products, "invalid_order_items_products.csv")
        validation_passed = False

    # 4) Invalid qty
    invalid_qty = order_items_df[order_items_df["qty"] <= 0]
    print(f"Invalid qty records in order_items: {len(invalid_qty)}")
    if len(invalid_qty) > 0:
        save_invalid_records(invalid_qty, "invalid_qty.csv")
        validation_passed = False

    # 5) Invalid price
    invalid_price = order_items_df[order_items_df["price"] <= 0]
    print(f"Invalid price records in order_items: {len(invalid_price)}")
    if len(invalid_price) > 0:
        save_invalid_records(invalid_price, "invalid_price.csv")
        validation_passed = False

    # Validation summary
    print("\n================ VALIDATION SUMMARY ================")
    if validation_passed:
        print("All validation checks passed successfully ✅")
    else:
        print("Some validation checks FAILED ❌ — check data/invalid/ folder")
        raise ValueError("Pipeline stopped due to validation failures")