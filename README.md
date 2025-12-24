# Big-Data-Analytics-25

# Final Data Pipeline Project  
**Apache Airflow + PostgreSQL + dbt**

## Project Overview

1. Ingests raw data from a public REST API into PostgreSQL  
2. Transforms the data using dbt (staging and mart layers)  
3. Orchestrates ingestion and transformations using Apache Airflow  

---

## Data Source

**Open Food Facts** — public REST API with open data about food products.

API endpoint used:  
https://world.openfoodfacts.org/api/v2/search

The dataset contains multiple related entities such as products and product categories and includes stable identifiers and timestamps.

---

## Entities

- Products  
- Product categories  

Entities are linked using product codes and category references.

---

## Airflow DAGs

### 1. `openfoodfacts_ingest`
- Fetches data from Open Food Facts API
- Loads raw data into PostgreSQL
- Writes data into the `raw` schema
- Can be triggered manually from Airflow UI

### 2. `dbt_run_test`
- Runs `dbt run`
- Runs `dbt test`
- Builds staging and mart layers
- Ensures data quality through automated tests

---

## Database Schemas

### Raw Schema
- `raw.products_raw`
- `raw.product_categories_raw`

Stores unprocessed data directly ingested from the API.

### Staging Schema
- `staging.stg_products`
- `staging.stg_product_categories`

Contains cleaned, typed, and deduplicated data.

### Mart Schema
- `mart.products_mart`

Final analytical table built from staging models.

---

## dbt Models

### Staging Models
- `stg_products`
- `stg_product_categories`

### Mart Model
- `products_mart`

---

## dbt Tests

The following tests are implemented and passing:
- `not_null` tests on key columns
- `unique` tests on primary keys
- `relationships` test between products and categories

---

## How to Run the Project

Start services:
```bash
docker compose up -d

Open Airflow UI:

Trigger DAGs in order:
- `openfoodfacts_ingest`
- `dbt_run_test`

## Queries:

SELECT * FROM raw.products_raw LIMIT 5;
SELECT * FROM staging.stg_products LIMIT 5;
SELECT * FROM mart.products_mart LIMIT 5;
