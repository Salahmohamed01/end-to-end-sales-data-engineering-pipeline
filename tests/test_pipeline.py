import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.transformation.data_cleaning import transform_dataframes
from app.validation.data_validation import validate_dataframes
from app.warehouse.data_modeling import build_dimensions, build_fact_table


# =====================
# Fixtures
# =====================

@pytest.fixture
def sample_dataframes():
    customers = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "city": ["Mumbai", "Delhi", "Pune"],
        "signup_date": ["2021-01-01", "2022-05-10", "2020-03-15"]
    })

    orders = pd.DataFrame({
        "order_id": [101, 102, 103],
        "customer_id": [1, 2, 3],
        "store_id": [10, 20, 30],
        "order_date": ["2023-01-01", "2023-06-15", "2023-09-20"],
        "promotion_id": [1, 2, 3]
    })

    order_items = pd.DataFrame({
        "order_item_id": [1, 2, 3],
        "order_id": [101, 102, 103],
        "product_id": [501, 502, 503],
        "qty": [2, 3, 1],
        "price": [100, 200, 300]
    })

    products = pd.DataFrame({
        "product_id": [501, 502, 503],
        "category_id": [1, 2, 3],
        "supplier_id": [10, 20, 30],
        "price": [100, 200, 300]
    })

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "products": products
    }


# =====================
# Transformation Tests
# =====================

def test_date_conversion(sample_dataframes):
    result = transform_dataframes(sample_dataframes)
    assert str(result["customers"]["signup_date"].dtype) == "datetime64[us]"
    assert str(result["orders"]["order_date"].dtype) == "datetime64[us]"


def test_total_amount_created(sample_dataframes):
    result = transform_dataframes(sample_dataframes)
    assert "total_amount" in result["order_items"].columns


def test_total_amount_values(sample_dataframes):
    result = transform_dataframes(sample_dataframes)
    df = result["order_items"]
    assert (df["total_amount"] == df["qty"] * df["price"]).all()


def test_city_standardized(sample_dataframes):
    result = transform_dataframes(sample_dataframes)
    cities = result["customers"]["city"].tolist()
    assert all(c == c.title() for c in cities)


# =====================
# Validation Tests
# =====================

def test_validation_passes(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    try:
        validate_dataframes(dataframes)
        passed = True
    except ValueError:
        passed = False
    assert passed


def test_invalid_customer_caught(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    dataframes["orders"].loc[0, "customer_id"] = 9999
    try:
        validate_dataframes(dataframes)
        passed = True
    except ValueError:
        passed = False
    assert not passed


# =====================
# Warehouse Tests
# =====================

def test_dim_customers_shape(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    dim_customers, _, _ = build_dimensions(dataframes)
    assert len(dim_customers) == 3
    assert "customer_id" in dim_customers.columns


def test_dim_products_shape(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    _, dim_products, _ = build_dimensions(dataframes)
    assert len(dim_products) == 3
    assert "product_id" in dim_products.columns


def test_fact_sales_columns(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    fact_sales = build_fact_table(dataframes)
    expected_cols = ["order_id", "product_id", "customer_id", "order_date", "quantity", "total_amount"]
    for col in expected_cols:
        assert col in fact_sales.columns


def test_fact_sales_no_nulls(sample_dataframes):
    dataframes = transform_dataframes(sample_dataframes)
    fact_sales = build_fact_table(dataframes)
    assert fact_sales.isnull().sum().sum() == 0