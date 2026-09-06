from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_DIR = "/mnt/c/Users/rowey/DDS8530_Assignment5"
PYTHON = "/home/rowey/airflow_assignment5/airflow_venv/bin/python"

with DAG(
    dag_id="dds8530_etl_mlops_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=False,
    tags=["DDS8530", "ETL", "MLOps"],
) as dag:

    run_etl = BashOperator(
        task_id="run_etl_pipeline",
        bash_command=f"cd {PROJECT_DIR} && {PYTHON} etl_pipeline.py",
    )

    run_dask = BashOperator(
        task_id="run_dask_processing",
        bash_command=f"cd {PROJECT_DIR} && {PYTHON} dask_processing.py",
    )

    train_mlflow = BashOperator(
    task_id="train_mlflow_model",
    bash_command=f"cd /home/rowey/mlflow_assignment5 && {PYTHON} {PROJECT_DIR}/mlflow_training.py",
)

    run_etl >> run_dask >> train_mlflow