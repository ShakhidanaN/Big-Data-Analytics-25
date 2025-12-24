from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2
import json

def load_products():
    url = "https://world.openfoodfacts.org/api/v2/search"
    params = {
        "page_size": 20,
        "fields": "code,product_name,last_modified_t,categories_tags"
    }

    r = requests.get(url, params=params)
    data = r.json()["products"]

    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;
        CREATE TABLE IF NOT EXISTS raw.products (
            code TEXT PRIMARY KEY,
            product_name TEXT,
            last_modified_t BIGINT
        );
        CREATE TABLE IF NOT EXISTS raw.product_categories (
            code TEXT,
            category TEXT,
            PRIMARY KEY (code, category)
        );
    """)

    for p in data:
        code = p.get("code")
        name = p.get("product_name")
        ts = p.get("last_modified_t")

        cur.execute("""
            INSERT INTO raw.products (code, product_name, last_modified_t)
            VALUES (%s, %s, %s)
            ON CONFLICT (code) DO UPDATE
            SET product_name = EXCLUDED.product_name,
                last_modified_t = EXCLUDED.last_modified_t;
        """, (code, name, ts))

        for c in p.get("categories_tags", []):
            cur.execute("""
                INSERT INTO raw.product_categories (code, category)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (code, c))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="openfoodfacts_ingest",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    load = PythonOperator(
        task_id="load_openfoodfacts",
        python_callable=load_products
    )
