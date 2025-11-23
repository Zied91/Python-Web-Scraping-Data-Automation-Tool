# airflow/dags/crypto_stock_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
import os

# Allow Airflow to import your project modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, ROOT)

from scrapers.crypto_scraper import CryptoScraper
from scrapers.stock_scraper import StockScraper
from utils.exporter import save_data
from utils.history import append_to_history
from utils.chart_generator import (
    create_crypto_price_chart,
    create_crypto_change_chart,
    create_crypto_price_trend,
    create_stock_price_chart,
    create_stock_price_trend
)

import yaml


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

dag = DAG(
    dag_id="crypto_stock_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False
)


# =============== TASK FUNCTIONS ================= #

def scrape_crypto(**context):
    with open(f"{ROOT}/config.yaml") as f:
        config = yaml.safe_load(f)

    scraper = CryptoScraper()
    data = scraper.run(config["crypto_sources"][0]["url"])

    save_data(data, f"{ROOT}/data/crypto_prices.csv")


def scrape_stocks(**context):
    with open(f"{ROOT}/config.yaml") as f:
        config = yaml.safe_load(f)

    scraper = StockScraper()
    results = []

    for symbol in config["stocks_sources"][0]["symbols"]:
        results.append(scraper.run_for_symbol(symbol))

    save_data(results, f"{ROOT}/data/stock_prices.csv")


def update_crypto_history(**context):
    append_to_history(
        f"{ROOT}/data/crypto_prices.csv",
        f"{ROOT}/data/crypto_history.csv",
        "name"
    )


def update_stock_history(**context):
    append_to_history(
        f"{ROOT}/data/stock_prices.csv",
        f"{ROOT}/data/stock_history.csv",
        "symbol"
    )


def generate_charts(**context):
    # Crypto charts
    create_crypto_price_chart(f"{ROOT}/data/crypto_prices.csv")
    create_crypto_change_chart(f"{ROOT}/data/crypto_prices.csv")
    create_crypto_price_trend(f"{ROOT}/data/crypto_history.csv")

    # Stock charts
    create_stock_price_chart(f"{ROOT}/data/stock_prices.csv")
    create_stock_price_trend(f"{ROOT}/data/stock_history.csv")


# =============== AIRFLOW TASKS ================= #

task_crypto_scrape = PythonOperator(
    task_id="scrape_crypto",
    python_callable=scrape_crypto,
    dag=dag
)

task_stock_scrape = PythonOperator(
    task_id="scrape_stocks",
    python_callable=scrape_stocks,
    dag=dag
)

task_crypto_history = PythonOperator(
    task_id="update_crypto_history",
    python_callable=update_crypto_history,
    dag=dag
)

task_stock_history = PythonOperator(
    task_id="update_stock_history",
    python_callable=update_stock_history,
    dag=dag
)

task_generate_charts = PythonOperator(
    task_id="generate_charts",
    python_callable=generate_charts,
    dag=dag
)


# ====== TASK DEPENDENCIES (PIPELINE FLOW) ====== #

(task_crypto_scrape >> task_crypto_history)
(task_stock_scrape >> task_stock_history)
(task_crypto_history >> task_generate_charts)
(task_stock_history >> task_generate_charts)
