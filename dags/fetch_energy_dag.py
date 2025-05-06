from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'chirdeep',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='uk_energy_generation_fetch',
    default_args=default_args,
    description='Fetch UK energy generation data daily',
    schedule_interval='@hourly',  #Change according to preference
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    fetch_energy = BashOperator(
        task_id='run_fetch_script',
        bash_command='cd /Users/chirdeep/Desktop/GitHubProject/uk-energy-trends && source .venv/bin/activate && python scripts/fetch_generation_mix.py'
    )

    fetch_energy
