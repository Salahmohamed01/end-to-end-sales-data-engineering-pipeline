from app.ingestion.ingest_data import load_all_tables
from app.transformation.data_cleaning import (
    explore_data,
    transform_dataframes,
    preview_transformed_data,
)
from app.validation.data_validation import validate_dataframes
from app.warehouse.data_modeling import (
    build_dimensions,
    build_fact_table,
    preview_warehouse,
)
from app.database.db_loader import load_to_database
from app.database.db_optimizer import apply_optimizations
from app.loading.incremental_loader import incremental_load_fact_sales
from app.analytics.analysis import run_analysis
from app.cloud.s3_handler import upload_raw_data_to_s3, list_s3_files
from app.utils.logger import setup_logger


def main():
    logger = setup_logger()
    logger.info("Pipeline started")

    # Phase 2 - Ingestion
    logger.info("Starting data ingestion")
    dataframes = load_all_tables()
    logger.info(f"Loaded {len(dataframes)} tables")

    # Phase 3 - Exploration
    logger.info("Starting data exploration")
    for table_name, df in dataframes.items():
        explore_data(df, table_name)

    # Phase 4 - Transformation
    logger.info("Starting data transformation")
    dataframes = transform_dataframes(dataframes)
    preview_transformed_data(dataframes)

    # Phase 5 - Validation
    logger.info("Starting data validation")
    validate_dataframes(dataframes)

    # Phase 6 - Warehouse Modeling
    logger.info("Building data warehouse")
    dim_customers, dim_products, dim_date = build_dimensions(dataframes)
    fact_sales = build_fact_table(dataframes)
    preview_warehouse(dim_customers, dim_products, dim_date, fact_sales)

    # Phase 7 - Load Dimensions
    logger.info("Loading dimensions to database")
    load_to_database(dim_customers, dim_products, dim_date)

    # Phase 8 - Incremental Load
    logger.info("Starting incremental load")
    incremental_load_fact_sales(fact_sales)

    # Phase 10 - DB Optimization
    logger.info("Applying database optimizations")
    apply_optimizations()

    # Phase 13 - Cloud Upload
    logger.info("Uploading data to S3")
    upload_raw_data_to_s3()
    list_s3_files()

    # Analytics
    logger.info("Starting analysis")
    run_analysis()

    logger.info("Pipeline completed successfully")
    print("\nPipeline completed successfully")


if __name__ == "__main__":
    main()