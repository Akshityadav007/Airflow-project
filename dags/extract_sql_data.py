from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import io

def extract_and_upload(**context):
    pg_hook = PostgresHook(postgres_conn_id="source_postgres")
    sql = "SELECT * FROM orders;"
    df = pg_hook.get_pandas_df(sql)

    # convert to CSV
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer_value = buffer.getvalue()

    today = datetime.now()
    timestamp = today.strftime("%Y-%m-%dT%H-%M-%S")
    blob_path = f"sql/orders/{today.year}/{timestamp}/orders.csv"


    azure_hook = WasbHook(wasb_conn_id="azure_blob_conn")
    azure_hook.upload(
        container_name="landing",
        blob_name=blob_path,
        data=buffer_value,
        overwrite=True
    )

    print("Uploaded:", blob_path)


with DAG(
    dag_id="extract_sql_data",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ingestion", "sql", "azure"]
):

    run = PythonOperator(
        task_id="extract_and_upload",
        python_callable=extract_and_upload
    )
