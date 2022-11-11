from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import \
    AirbyteTriggerSyncOperator

with DAG(
    dag_id="ExtractAndLoad",
    schedule_interval="@daily",
    start_date=datetime(2022, 9, 9),
    dagrun_timeout=timedelta(minutes=30),
    catchup=False,
) as dag:

    rds_to_s3_task = AirbyteTriggerSyncOperator(
        task_id="rds_to_s3_task",
        airbyte_conn_id="airbyte_conn",
        connection_id="ec890ba2-7a47-4a38-8f1e-4bd11aafaf94",
        asynchronous=False,
    )

    rds_to_s3_task
