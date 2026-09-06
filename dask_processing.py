import dask.dataframe as dd
import logging

logging.basicConfig(
    filename="dask_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Starting scalable Dask processing...")

# Read the transformed dataset with Dask
df = dd.read_csv("processed_data.csv")

print("Dask DataFrame created successfully.")
print(f"Number of partitions: {df.npartitions}")

# Perform parallel aggregation
summary = df.groupby("churn")[
    ["age", "income", "purchases", "website_visits"]
].mean()

print("\nComputing customer summary in parallel...")
result = summary.compute()

print("\nAverage normalized values by churn status:")
print(result)

# Save results
result.to_csv("dask_summary.csv")

print("\nDask results saved to dask_summary.csv")
print("DASK PROCESSING COMPLETED SUCCESSFULLY")

logging.info("Dask processing completed successfully.")