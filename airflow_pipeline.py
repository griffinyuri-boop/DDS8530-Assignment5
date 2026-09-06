from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the Airflow workflow
with DAG(
    dag_id="dds8530_etl_mlops_pipeline",
    description="Automates the DDS8530 ETL and machine learning workflow",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=False,
    tags=["DDS8530", "ETL", "MLOps"],
) as dag:

    # Step 1: Run ETL pipeline
    run_etl = BashOperator(
        task_id="run_etl_pipeline",
        bash_command="python etl_pipeline.py"
    )

    # Step 2: Run scalable Dask processing
    run_dask = BashOperator(
        task_id="run_dask_processing",
        bash_command="python dask_processing.py"
    )

    # Step 3: Train and track machine learning model
    train_model = BashOperator(
        task_id="train_mlflow_model",
        bash_command="python mlflow_training.py"
    )

    # Define execution order
    run_etl >> run_dask >> train_model