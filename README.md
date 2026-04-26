# 🚀 End-to-End Sales Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.1-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-✓-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-✓-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-✓-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-10%20Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**A production-grade, end-to-end Data Engineering pipeline built with Python, Apache Airflow, Docker, and AWS S3. The pipeline covers the full data lifecycle from raw ingestion to an analytics-ready Data Warehouse.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pipeline Phases](#-pipeline-phases)
- [Data Model](#-data-model-star-schema)
- [Dataset](#-dataset)
- [Key Features](#-key-features)
- [Setup & Installation](#-setup--installation)
- [Running the Pipeline](#-running-the-pipeline)
- [Running with Docker](#-running-with-docker)
- [Airflow Orchestration](#-airflow-orchestration)
- [Testing](#-testing)
- [Analytics Outputs](#-analytics-outputs)
- [Cloud Integration](#-cloud-integration-aws-s3)
- [CI/CD](#-cicd-github-actions)

---

## 🎯 Overview

This project simulates a **real-world retail sales data platform** built with industry-standard Data Engineering tools and practices. It was designed to demonstrate the full skill set expected of a professional Data Engineer, including:

- Building modular, reusable ETL/ELT pipelines
- Designing Data Warehouses using Star Schema
- Implementing incremental loading with watermark tracking
- Orchestrating pipelines with Apache Airflow
- Containerizing workloads with Docker
- Integrating with cloud storage (AWS S3)
- Writing unit tests for data pipeline components
- Automating CI/CD with GitHub Actions

---

## 🏗️ Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│              Raw CSV Files (customers, orders,                  │
│                    order_items, products)                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                            │
│          Multi-table dynamic CSV loader with schema             │
│                       inspection                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TRANSFORMATION LAYER                          │
│      Date parsing · total_amount derivation · city              │
│               standardization · type casting                    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION LAYER                             │
│     Foreign key checks · business rule validation ·             │
│          null/duplicate checks · invalid record export          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATA WAREHOUSE (SQLite)                        │
│          Star Schema: fact_sales + dim_customers +              │
│                  dim_products + dim_date                        │
│          Indexes · SQL Views · Incremental Loading              │
└──────────────┬──────────────────────────────────┬───────────────┘
               │                                  │
               ▼                                  ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│       ANALYTICS LAYER        │   │         CLOUD LAYER          │
│  Sales trends · Top products │   │   AWS S3 raw data upload     │
│  Revenue by category         │   │   Cloud-ready storage        │
└──────────────────────────────┘   └──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION                              │
│          Apache Airflow DAG running inside Docker               │
│      Schedule: @daily · 4 tasks · SequentialExecutor            │
└─────────────────────────────────────────────────────────────────┘
```

</div>

---

## 🛠️ Tech Stack

| Category | Tool | Version | Purpose |
|----------|------|---------|---------|
| Language | Python | 3.11 | Core pipeline development |
| Data Processing | Pandas | 2.0+ | Data transformation & analysis |
| Database | SQLite | Built-in | Data Warehouse storage |
| Orchestration | Apache Airflow | 2.8.1 | Pipeline scheduling & monitoring |
| Containerization | Docker + Docker Compose | Latest | Environment packaging |
| Cloud Storage | AWS S3 (boto3) | Latest | Raw data cloud storage |
| Testing | pytest | 9.0+ | Unit testing |
| CI/CD | GitHub Actions | - | Automated testing on push |
| Config Management | PyYAML | 6.0+ | Centralized configuration |
| Logging | Python logging | Built-in | Pipeline monitoring |
| Visualization | Matplotlib | 3.x | Analytics charts |

---

## 📁 Project Structure

```
End-to-End Sales Data Engineering Pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── analytics/
│   │   └── analysis.py
│   ├── cloud/
│   │   └── s3_handler.py
│   ├── config/
│   │   └── config_loader.py
│   ├── database/
│   │   ├── db_loader.py
│   │   └── db_optimizer.py
│   ├── ingestion/
│   │   └── ingest_data.py
│   ├── loading/
│   │   └── incremental_loader.py
│   ├── transformation/
│   │   └── data_cleaning.py
│   ├── utils/
│   │   └── logger.py
│   ├── validation/
│   │   └── data_validation.py
│   └── warehouse/
│       └── data_modeling.py
├── airflow/
│   └── dags/
│       └── sales_pipeline_dag.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── invalid/
├── sql/
│   ├── analytics/
│   │   └── analytical_queries.sql
│   └── warehouse/
│       └── optimize.sql
├── tests/
│   └── test_pipeline.py
├── logs/
├── docs/
├── .gitignore
├── config.yaml.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
└── README.md
```

## 🔄 Pipeline Phases

| # | Phase | Description | Status |
|---|-------|-------------|--------|
| 1 | **Project Setup** | Virtual environment, folder structure, config system, logging | ✅ |
| 2 | **Data Ingestion** | Dynamic multi-table CSV loader from `data/raw/` | ✅ |
| 3 | **Data Exploration** | Shape, dtypes, null counts, duplicate detection | ✅ |
| 4 | **Data Transformation** | Date parsing, `total_amount` derivation, city standardization | ✅ |
| 5 | **Data Validation** | FK integrity, business rules, invalid record export to CSV | ✅ |
| 6 | **Warehouse Modeling** | Star Schema: `fact_sales` + 3 dimension tables | ✅ |
| 7 | **Database Loading** | Dimension tables loaded into SQLite | ✅ |
| 8 | **Incremental Loading** | Watermark-based fact table loading (no re-processing) | ✅ |
| 9 | **Airflow Orchestration** | DAG with 4 sequential tasks, @daily schedule, Docker-hosted | ✅ |
| 10 | **DB Optimization** | 9 indexes + 2 SQL views (`vw_monthly_sales`, `vw_top_products`) | ✅ |
| 11 | **Unit Testing** | 10 pytest tests covering transformation, validation & modeling | ✅ |
| 12 | **Dockerization** | Dockerfile + docker-compose for full environment packaging | ✅ |
| 13 | **Cloud Integration** | AWS S3 upload of raw data using boto3 | ✅ |
| 14 | **CI/CD** | GitHub Actions runs pytest on every push to main | ✅ |
| 15 | **Documentation** | Architecture, setup guide, and project README | ✅ |

---

## 📊 Data Model (Star Schema)

<div align="center">

```
                         ┌─────────────────┐
                         │  dim_customers  │
                         ├─────────────────┤
                         │ customer_id (PK)│
                         │ city            │
                         │ signup_date     │
                         └────────┬────────┘
                                  │
┌─────────────────┐               │               ┌─────────────────┐
│   dim_products  │               │               │    dim_date     │
├─────────────────┤               │               ├─────────────────┤
│ product_id (PK) │               │               │ order_date (PK) │
│ category_id     │               │               │ year            │
│ supplier_id     │               │               │ month           │
│ price           │               │               │ day             │
└────────┬────────┘               │               └────────┬────────┘
         │                        │                        │
         │               ┌────────▼────────┐               │
         └──────────────►│   fact_sales    │◄──────────────┘
                         ├─────────────────┤
                         │ order_id        │
                         │ product_id (FK) │
                         │ customer_id (FK)│
                         │ order_date (FK) │
                         │ quantity        │
                         │ total_amount    │
                         └─────────────────┘
```

</div>

---

## 📦 Dataset

| Table | Records | Description |
|-------|---------|-------------|
| customers | 50,000 | Customer profiles with city and signup date |
| orders | 300,000 | Sales orders with store and promotion info |
| order_items | 600,000 | Line items with quantity and price |
| products | 10,000 | Product catalog with categories and suppliers |

**Total:** ~960,000 records processed end-to-end.

---

## ✨ Key Features

**Modular Architecture**
Each pipeline stage is a separate Python module with clear inputs and outputs, making it easy to maintain, extend, or replace individual components.

**Incremental Loading**
The pipeline uses a watermark table (`etl_watermark`) to track the last loaded date, ensuring only new records are processed on each run — no redundant re-processing.

**Data Quality Framework**
Validation checks include foreign key integrity, business rule validation (qty > 0, price > 0), and automatic export of invalid records to `data/invalid/` for investigation.

**Config-Driven Design**
All paths, database settings, and AWS credentials are centralized in `config.yaml`, making the pipeline environment-agnostic and easy to configure.

**Production Logging**
Every pipeline stage logs to `logs/pipeline.log` with timestamps and severity levels, enabling full auditability.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Docker Desktop
- AWS account (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sales-data-engineering-pipeline.git
cd sales-data-engineering-pipeline
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure settings
```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml` with your AWS credentials:
```yaml
paths:
  raw_data: data/raw
  processed_data: data/processed
  invalid_data: data/invalid
  database: sales_dw.db

aws:
  access_key_id: YOUR_ACCESS_KEY_ID
  secret_access_key: YOUR_SECRET_ACCESS_KEY
  bucket_name: YOUR_BUCKET_NAME
  region: us-east-1
```

### 5. Add your data
Place CSV files in `data/raw/`:
- `customers.csv`
- `orders.csv`
- `order_items.csv`
- `products.csv`

---

## ▶️ Running the Pipeline

```bash
python main.py
```

The pipeline will automatically run all phases in sequence:
1. Ingest raw CSV data
2. Explore and profile each table
3. Clean and transform the data
4. Validate data quality
5. Build the Star Schema warehouse
6. Load dimensions to SQLite
7. Incrementally load fact table
8. Apply indexes and views
9. Upload raw data to AWS S3
10. Generate analytics and charts

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t sales-pipeline .

# Run the container
docker run --rm \
  -v "%cd%\data:/app/data" \
  -v "%cd%\logs:/app/logs" \
  sales-pipeline
```

---

## 🌀 Airflow Orchestration

The pipeline is orchestrated as an Airflow DAG with 4 sequential tasks:
ingest_data → transform_data → validate_data → load_data

**Run Airflow with Docker Compose:**
```bash
docker-compose up
```

Open the Airflow UI at **http://localhost:8080**

| Setting | Value |
|---------|-------|
| Username | admin |
| Password | admin |
| Schedule | @daily |
| Executor | SequentialExecutor |

---

## 🧪 Testing

```bash
pytest tests/test_pipeline.py -v
```

**10 tests covering:**

| Test | Description |
|------|-------------|
| `test_date_conversion` | Validates date columns are parsed to datetime |
| `test_total_amount_created` | Checks total_amount column is created |
| `test_total_amount_values` | Validates qty × price calculation |
| `test_city_standardized` | Checks city name title-casing |
| `test_validation_passes` | Clean data passes all validation checks |
| `test_invalid_customer_caught` | Orphan customer_id raises ValueError |
| `test_dim_customers_shape` | Dimension table has correct shape |
| `test_dim_products_shape` | Products dimension integrity check |
| `test_fact_sales_columns` | Fact table has all required columns |
| `test_fact_sales_no_nulls` | No null values in fact table |

---

## 📈 Analytics Outputs

### Total Sales per Year
![Sales per Year](docs/sales_per_year.png)

### Total Sales per Month
![Sales per Month](docs/sales_per_month.png)

### Top 10 Products by Sales
![Top 10 Products](docs/top_10_products.png)

### Top 10 Customers by Revenue
![Top 10 Customers](docs/top_10_customers.png)

### Sales per Category
![Sales per Category](docs/sales_per_category.png)

---

## ☁️ Cloud Integration (AWS S3)

Raw data files are automatically uploaded to AWS S3 after each pipeline run:

s3://YOUR_BUCKET_NAME/
└── raw/
├── customers.csv       (1.2 MB)
├── orders.csv          (8.7 MB)
├── order_items.csv     (15.1 MB)
└── products.csv        (158 KB)

---

## ⚡ CI/CD (GitHub Actions)

Every push to the `main` branch automatically:
1. Sets up Python 3.11 environment
2. Installs all dependencies
3. Creates a test `config.yaml`
4. Runs all 10 pytest tests

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

---

## 👨‍💻 Author

**Salah Mohamed**

Data Engineering Portfolio Project — 2026

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).