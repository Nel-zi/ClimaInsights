from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from utils import extract_data, load_data

default_args = {
    "owner" : "airflow",
    "email" : "nelxzxi@gmail.com",
    "email_on_failure" : False,
    "depends_on_past" : True,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=1)
}

with DAG(
    'ClimaInsights_weather_pipeline',
    default_args=default_args,
    description='ClimaInsights data pipeline',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['ETL', 'ClimaInsights Weather Data', 'Data Engineering']
) as dag:


    
    
    extract_weather_data = PythonOperator(
        task_id = 'extract_weather_data',
        python_callable = extract_data
    )

    load_weather_data = PythonOperator(
        task_id = 'load_weather_data',
        python_callable = load_data
    )


    extract_weather_data >> load_weather_data
