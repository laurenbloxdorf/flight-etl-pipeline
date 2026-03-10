from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, "/opt/airflow/include")

from extract import extract_flights
from transform import transform_flights
from load import load_flights

US_BBOX = (24.5, 49.5, -125.0, -66.0)  # Continental US bounding box

def run_extract(**context):
    raw = extract_flights(US_BBOX)
    context["ti"].xcom_push(key="raw_flights", value=raw)

def run_transform(**context):
    raw = context["ti"].xcom_pull(key="raw_flights", task_ids="extract")
    cleaned = transform_flights(raw)
    context["ti"].xcom_push(key="clean_flights", value=cleaned)

def run_load(**context):
    flights = context["ti"].xcom_pull(key="clean_flights", task_ids="transform")
    load_flights(flights)

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="flight_etl",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/15 * * * *",  # runs every 15 minutes
    catchup=False,
    tags=["flights", "etl"],
) as dag:

    extract = PythonOperator(task_id="extract", python_callable=run_extract)
    transform = PythonOperator(task_id="transform", python_callable=run_transform)
    load = PythonOperator(task_id="load", python_callable=run_load)

    extract >> transform >> load