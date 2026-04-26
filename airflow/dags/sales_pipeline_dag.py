from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the project root to path
sys.path.insert(0, "/opt/airflow")

from app.ingestion.ingest_data import load_all_tables
from app.transformation.data_cleaning import (
    explore_data,
    transform_dataframes,
)
from app.validation.data_validation import validate_dataframes
from app.warehouse.data_modeling import build_dimensions, build_fact_table
from app.database.db_loader import load_to_database
from app.loading.incremental_loader import incremental_load_fact_sales

default_args = {
    "owner": "data_engineer",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "sales_pipeline",
    default_args=default_args,
    description="End-to-End Sales Data Engineering Pipeline",
    schedule="@daily",
    catchup=False,
)


def task_ingest(**kwargs):
    dataframes = load_all_tables()
    print(f"Ingested {len(dataframes)} tables")


def task_transform(**kwargs):
    dataframes = load_all_tables()
    for table_name, df in dataframes.items():
        explore_data(df, table_name)
    dataframes = transform_dataframes(dataframes)
    print("Transformation completed")


def task_validate(**kwargs):
    dataframes = load_all_tables()
    dataframes = transform_dataframes(dataframes)
    validate_dataframes(dataframes)
    print("Validation completed")


def task_load(**kwargs):
    dataframes = load_all_tables()
    dataframes = transform_dataframes(dataframes)
    dim_customers, dim_products, dim_date = build_dimensions(dataframes)
    fact_sales = build_fact_table(dataframes)
    load_to_database(dim_customers, dim_products, dim_date)
    incremental_load_fact_sales(fact_sales)
    print("Loading completed")


ingest_task = PythonOperator(
    task_id="ingest_data",
    python_callable=task_ingest,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=task_transform,
    dag=dag,
)

validate_task = PythonOperator(
    task_id="validate_data",
    python_callable=task_validate,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data",
    python_callable=task_load,
    dag=dag,
)

ingest_task >> transform_task >> validate_task >> load_task