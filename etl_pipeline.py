import pandas as pd
import sqlite3
import logging
from sklearn.preprocessing import MinMaxScaler

# Configure logging
logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL pipeline started.")

# -------------------------
# EXTRACT
# -------------------------
print("Starting Extract phase...")

df = pd.read_csv("raw_data.csv")

print(f"Extracted {len(df)} records from raw_data.csv")
logging.info("Extracted %s records from CSV.", len(df))

# -------------------------
# TRANSFORM
# -------------------------
print("Starting Transform phase...")

# Fill missing numerical values with column medians
numeric_columns = ["age", "income", "purchases", "website_visits"]

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Create a new feature
df["purchase_per_visit"] = (
    df["purchases"] / df["website_visits"]
)

# Normalize selected numerical columns
scaler = MinMaxScaler()

columns_to_normalize = [
    "age",
    "income",
    "purchases",
    "website_visits"
]

df[columns_to_normalize] = scaler.fit_transform(
    df[columns_to_normalize]
)

print("Missing values handled.")
print("Numerical features normalized.")
print("New feature created: purchase_per_visit")

logging.info("Data transformation completed.")

# -------------------------
# LOAD
# -------------------------
print("Starting Load phase...")

# Save transformed CSV
df.to_csv("processed_data.csv", index=False)

# Load transformed data into SQLite
connection = sqlite3.connect("etl_database.db")

df.to_sql(
    "customer_data",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Processed data saved to processed_data.csv")
print("Processed data loaded into SQLite database.")
print("ETL PIPELINE COMPLETED SUCCESSFULLY")

logging.info("Processed data saved to CSV and SQLite.")
logging.info("ETL pipeline completed successfully.")