from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def test_run():
    print("SQL Extract DAG is running successfully!")

with DAG(
    dag_id="test_sql_extract",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["test"]
):
    t1 = PythonOperator(
        task_id="test_task",
        python_callable=test_run
    )
