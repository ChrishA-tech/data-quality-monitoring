"""Airflow DAG: daily data-quality run with retries. Runs in the Docker setup (docker-compose.yml)."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG("data_quality_monitoring", start_date=datetime(2026, 10, 1), schedule="@daily", catchup=False,
         default_args={"retries": 2, "retry_delay": timedelta(minutes=5)}) as dag:
    gen = BashOperator(task_id="load_batches", bash_command="cd /opt/airflow/project && python src/gen_data.py")
    chk = BashOperator(task_id="run_checks", bash_command="cd /opt/airflow/project && python src/run_checks.py")
    star = BashOperator(task_id="export_star_schema", bash_command="cd /opt/airflow/project && python src/star.py")
    gen >> chk >> star
