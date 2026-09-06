import pandas as pd
import requests
from sqlalchemy import create_engine
import logging

logging.basicConfig(
    filename="multi_source_extract.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Starting multi-source data extraction...")

# --------------------------------------------------
# 1. Extract CSV data using batch processing
# --------------------------------------------------
print("\n1. Extracting CSV data in batches...")

csv_batches = pd.read_csv("raw_data.csv", chunksize=5)
csv_data = pd.concat(csv_batches, ignore_index=True)

print(f"CSV extraction successful: {len(csv_data)} records")
logging.info("Extracted %s CSV records using batch processing.", len(csv_data))

# --------------------------------------------------
# 2. Extract database data using SQLAlchemy
# --------------------------------------------------
print("\n2. Extracting database data with SQLAlchemy...")

engine = create_engine("sqlite:///etl_database.db")

database_data = pd.read_sql(
    "SELECT * FROM customer_data",
    engine
)

print(f"Database extraction successful: {len(database_data)} records")
logging.info(
    "Extracted %s database records using SQLAlchemy.",
    len(database_data)
)

# --------------------------------------------------
# 3. Extract web API data using requests
# --------------------------------------------------
print("\n3. Extracting web API data with requests...")

api_url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(api_url, timeout=10)
response.raise_for_status()

api_data = pd.DataFrame(response.json())

print(f"Web API extraction successful: {len(api_data)} records")
logging.info(
    "Extracted %s records from the web API.",
    len(api_data)
)

# Save API data for inspection
api_data.to_csv("api_data.csv", index=False)

print("\nSources successfully extracted:")
print(f"CSV records: {len(csv_data)}")
print(f"Database records: {len(database_data)}")
print(f"Web API records: {len(api_data)}")
print("API data saved to api_data.csv")
print("\nMULTI-SOURCE EXTRACTION COMPLETED SUCCESSFULLY")

logging.info("Multi-source extraction completed successfully.")