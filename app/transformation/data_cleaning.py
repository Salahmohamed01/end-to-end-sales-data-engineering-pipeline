import pandas as pd


def explore_data(df, table_name):
    print(f"\n--- Exploring {table_name} ---")
    print("\nShape:")
    print(df.shape)
    print("\nColumns:")
    print(list(df.columns))
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicates:")
    print(df.duplicated().sum())


def transform_dataframes(dataframes):
    # --- Customers ---
    if "customers" in dataframes:
        df = dataframes["customers"]
        df["signup_date"] = pd.to_datetime(df["signup_date"])
        df["city"] = df["city"].str.strip().str.title()
        dataframes["customers"] = df

    # --- Orders ---
    if "orders" in dataframes:
        df = dataframes["orders"]
        df["order_date"] = pd.to_datetime(df["order_date"])
        dataframes["orders"] = df

    # --- Order Items ---
    if "order_items" in dataframes:
        df = dataframes["order_items"]
        df["total_amount"] = df["qty"] * df["price"]

        # Remove invalid rows
        before = len(df)
        df = df[df["qty"] > 0]
        df = df[df["price"] > 0]
        after = len(df)

        if before != after:
            print(f"Removed {before - after} invalid rows from order_items")

        dataframes["order_items"] = df

    # --- Products ---
    if "products" in dataframes:
        df = dataframes["products"]
        df = df[df["price"] > 0]
        dataframes["products"] = df

    return dataframes


def preview_transformed_data(dataframes):
    print("\n================ TRANSFORMED DATA PREVIEW ================\n")

    if "customers" in dataframes:
        print("Customers Data Types After Transformation:")
        print(dataframes["customers"].dtypes)
        print(dataframes["customers"].head(), "\n")

    if "orders" in dataframes:
        print("Orders Data Types After Transformation:")
        print(dataframes["orders"].dtypes)
        print(dataframes["orders"].head(), "\n")

    if "order_items" in dataframes:
        print("Order Items After Adding total_amount:")
        print(dataframes["order_items"].dtypes)
        print(dataframes["order_items"].head(), "\n")