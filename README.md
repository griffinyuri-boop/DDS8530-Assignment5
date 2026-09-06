\# DDS8530 Assignment 5: Scalable ETL and MLOps Pipeline



\## Project Overview



This project demonstrates the design and implementation of a scalable ETL and MLOps workflow using Python and AWS. The pipeline extracts customer data, performs data cleaning and transformation, loads processed data into structured storage, trains a machine learning model, tracks model experiments, and serves predictions through a REST API.



\## Pipeline Architecture



The project follows the following workflow:



Raw Data → ETL Processing → Dask Processing → AWS S3 → Machine Learning → MLflow → Flask REST API



Apache Airflow is represented through a DAG that defines scheduled orchestration of the ETL, Dask, and machine learning workflow. GitHub Actions provides a CI pipeline for automatically testing the workflow when changes are pushed to the repository.



\## Technologies



\- Python

\- pandas

\- Dask

\- SQLite

\- SQLAlchemy

\- AWS S3

\- scikit-learn

\- MLflow

\- Flask

\- Apache Airflow DAG

\- GitHub Actions



\## ETL Pipeline



The ETL pipeline reads customer data from a CSV file and processes the dataset using pandas. Missing numerical values are replaced with median values. Numerical features are normalized using MinMaxScaler, and a purchase-per-visit feature is created through feature engineering.



The transformed dataset is saved as `processed\_data.csv` and loaded into a SQLite database. The processed CSV is also stored in an AWS S3 bucket to demonstrate cloud-based storage.



\## Scalable Processing



Dask is used to demonstrate scalable dataframe processing. The Dask workflow reads the transformed dataset and computes grouped customer statistics. Although the demonstration dataset is small, the same approach can partition larger datasets for parallel processing.



\## Machine Learning



A Random Forest classifier predicts customer churn using five features:



\- Age

\- Income

\- Purchases

\- Website visits

\- Purchases per visit



The dataset is divided into training and testing subsets. The model achieved 83.33% accuracy on the demonstration test dataset.



\## MLflow Experiment Tracking



MLflow records the machine learning experiment, including:



\- Number of estimators

\- Maximum tree depth

\- Test set size

\- Model accuracy

\- Trained model artifact



The experiment is stored under `DDS8530\_Churn\_Prediction`.



\## Model API



Flask provides a REST API for model inference. The `/predict` endpoint accepts JSON input and returns a churn prediction.



Example response:



```json

{

&#x20; "prediction": 1,

&#x20; "result": "Customer likely to churn"

}

Yuri Griffin
National University
DDS8530