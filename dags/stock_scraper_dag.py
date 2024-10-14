# Importation des modules nécessaires -  stock_scraper_dag.py

import sys
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('.\scrapers\stock_data_scraper.py')

from scrapers.stock_data_scraper import StockDataScraper

from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Defining the argumens
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 25),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Creating the DAG Object
dag = DAG(
    'stock_data_scraper',
    default_args=default_args,
    description='Scrape stock data and load it into BigQuery',
    schedule_interval='@daily',
)

# Defining our function
def scrape_and_load_data():
    project_id = os.environ["PROJECT_ID"]
    dataset_id = os.environ['DATASET_ID']
    table_id = os.environ['TABLE_ID']
    
    scraper = StockDataScraper(project_id, dataset_id, table_id)
    scraper.fetch_data()
    scraper.create_bigquery_table()
    scraper.process_data()
    scraper.load_data_to_bigquery()

# Running our DAG
with dag:
    scrape_task = PythonOperator(
        task_id='scrape_and_load_data',
        python_callable=scrape_and_load_data,
    )

