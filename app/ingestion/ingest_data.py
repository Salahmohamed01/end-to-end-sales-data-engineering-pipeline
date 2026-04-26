import os
import pandas as pd
from app.config.config_loader import load_config


def load_all_tables():
    config = load_config()
    raw_path = config["paths"]["raw_data"]

    dataframes = {}

    files = os.listdir(raw_path)

    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(raw_path, file)
            df = pd.read_csv(file_path)

            table_name = file.replace(".csv", "")
            dataframes[table_name] = df

            print(f"\nLoaded table: {table_name}")
            print(df.head())

    return dataframes