from datetime import datetime
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

with DAG(
    dag_id="databricks_test_job",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["databricks"],
) as dag:

    run_job = DatabricksRunNowOperator(
        task_id="run_TestNotebook",
        databricks_conn_id="databricks_default",
        job_id=506081232181301,
    )
    run_job
