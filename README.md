# DDS8530 Assignment 5: Scalable ETL and MLOps Pipeline

## Project Overview

This project implements an end-to-end ETL and MLOps workflow using Python, AWS, machine learning, automation, and monitoring tools. The pipeline demonstrates data extraction from multiple sources, data cleaning and transformation, scalable processing, cloud storage, machine learning model training, experiment tracking, REST API deployment, CI/CD automation, and real-time model monitoring.

## Architecture

CSV / SQLite Database / Web API  
↓  
Multi-Source Extraction  
↓  
Pandas ETL Processing  
↓  
Dask Scalable Processing  
↓  
SQLite Database and AWS S3  
↓  
Random Forest Model Training  
↓  
MLflow Experiment Tracking  
↓  
Flask REST API  
↓  
Prometheus Metrics  
↓  
Grafana Monitoring

Apache Airflow provides the workflow orchestration design, while GitHub Actions provides automated CI pipeline execution.

## Technologies

- Python
- pandas
- Dask
- SQLAlchemy
- requests
- SQLite
- AWS S3
- scikit-learn
- MLflow
- Flask
- Apache Airflow
- GitHub Actions
- Prometheus
- Grafana

## Multi-Source Data Extraction

The `multi_source_extract.py` script demonstrates extraction from three different data sources.

1. CSV data is extracted from `raw_data.csv` using pandas batch processing with a chunk size of five records.
2. Structured database data is extracted from the SQLite database using SQLAlchemy.
3. Web API data is extracted using the Python requests library and saved as `api_data.csv`.

The web API returns JSON records containing both structured fields and textual content.

## ETL Pipeline

The `etl_pipeline.py` script performs the main Extract, Transform, and Load workflow.

### Extract

Customer data is loaded from the source CSV file.

### Transform

The transformation process includes:

- Handling missing numerical values using median imputation
- Normalizing numerical features with MinMaxScaler
- Creating the engineered feature `purchase_per_visit`
- Preparing the processed dataset for machine learning

### Load

Processed data is saved to:

- `processed_data.csv`
- SQLite database `etl_database.db`
- AWS S3 for cloud-based storage

## Scalable Processing with Dask

The `dask_processing.py` script uses Dask DataFrames to demonstrate parallel and scalable data processing. Customer records are grouped by churn status and average normalized values are calculated.

The demonstration dataset is intentionally small, so Dask uses a single partition locally. The same Dask workflow can partition larger datasets for distributed processing.

## Machine Learning Model

A Random Forest classifier is trained using scikit-learn to predict customer churn.

Model features include:

- age
- income
- purchases
- website_visits
- purchase_per_visit

The model achieved 83.33 percent accuracy on the test dataset and is saved as `churn_model.pkl` for deployment.

## MLflow Experiment Tracking

MLflow is used to track the machine learning experiment.

Tracked information includes:

- Number of estimators
- Maximum tree depth
- Test split
- Model accuracy
- Trained model artifact

The experiment is stored under `DDS8530_Churn_Prediction`.

## Flask REST API

The trained model is deployed through `model_api.py`.

The API provides:

- `/` for service status
- `/predict` for churn predictions
- `/metrics` for Prometheus monitoring metrics

The prediction endpoint accepts JSON feature values and returns the predicted churn classification.

## Apache Airflow Orchestration

The `airflow_pipeline.py` file defines an Apache Airflow DAG named `dds8530_etl_mlops_pipeline`.

The DAG automates the following task sequence:

1. Run the ETL pipeline
2. Run Dask processing
3. Train and track the machine learning model with MLflow

Because the local development environment uses Windows and Python 3.13, the DAG is provided as an orchestration design for deployment in an Airflow-supported environment rather than being executed natively on Windows.

## CI/CD with GitHub Actions

The GitHub Actions workflow is located at:

`.github/workflows/mlops_pipeline.yml`

The workflow automatically runs on pushes and pull requests to the main branch. It:

1. Checks out the repository
2. Configures Python
3. Installs project dependencies
4. Runs the ETL pipeline
5. Runs Dask processing
6. Trains the machine learning model
7. Runs the MLflow experiment

Multiple successful GitHub Actions runs verify that the automated pipeline executes correctly.

## Monitoring and Logging

Python logging is implemented throughout the ETL, Dask, model training, and REST API components.

The Flask model API also exposes Prometheus metrics through the `/metrics` endpoint. Metrics include:

- Total churn predictions
- Prediction classifications
- Prediction processing latency
- Python runtime metrics

A Prometheus server scrapes the Flask metrics endpoint at regular intervals. Grafana is connected to Prometheus and visualizes the `churn_predictions_total` metric for real-time model monitoring.

## Project Files

- `raw_data.csv` - source customer dataset
- `api_data.csv` - extracted web API data
- `multi_source_extract.py` - CSV, SQLAlchemy database, and web API extraction
- `etl_pipeline.py` - ETL processing pipeline
- `processed_data.csv` - transformed dataset
- `etl_database.db` - SQLite database
- `dask_processing.py` - scalable Dask processing
- `dask_summary.csv` - Dask output
- `train_model.py` - Random Forest model training
- `mlflow_training.py` - MLflow experiment tracking
- `churn_model.pkl` - trained deployment model
- `churn_model_mlflow.pkl` - MLflow model copy
- `model_api.py` - Flask REST API and Prometheus metrics
- `airflow_pipeline.py` - Airflow DAG
- `.github/workflows/mlops_pipeline.yml` - GitHub Actions CI workflow
- `requirements.txt` - project dependencies
- `README.md` - project documentation

## Running the Project

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt

python multi_source_extract.py
python etl_pipeline.py
python dask_processing.py
python train_model.py
python mlflow_training.py
python model_api.py