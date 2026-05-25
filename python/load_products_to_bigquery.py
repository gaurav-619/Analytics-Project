import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Step 1: Load credentials
script_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(script_dir, "..", "credentials", "service-account.json")
credentials = service_account.Credentials.from_service_account_file(cred_path)

client = bigquery.Client(
    project="dark-bit-493307-d3",
    credentials=credentials
)

# Step 3: Load CSV
file_path = os.path.join(script_dir, "..", "data", "products.csv")
df = pd.read_csv(file_path)

# Step 4: Table ID
# Ensure the dataset exists before loading
dataset_id = f"{credentials.project_id}.marketing_analytics"
table_id = f"{dataset_id}.raw_products"

from google.api_core import exceptions

# Create dataset if it doesn't exist
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"  # Adjust location if needed
try:
    client.get_dataset(dataset_id)
except exceptions.NotFound:
    print(f"Dataset {dataset_id} not found. Creating it...")
    client.create_dataset(dataset)
except Exception as e:
    print(f"An unexpected error occurred while checking dataset: {e}")
    raise

# Step 5: Upload
print(f"Loading data into {table_id}...")
job = client.load_table_from_dataframe(df, table_id)

job.result()  # Wait for the job to complete

print("Products data loaded successfully")