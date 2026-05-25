import os
from google.cloud import bigquery

# Set credentials path
script_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(script_dir, "..", "credentials", "service-account.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

# Initialize BigQuery client
client = bigquery.Client()

print("Connection successful! Fetching datasets...")

# List datasets in the project to verify connection
datasets = list(client.list_datasets())
if datasets:
    print("Datasets found:")
    for dataset in datasets:
        print(f"- {dataset.dataset_id}")
else:
    print("No datasets found in this project.")

# Optional: Run a simple query to test
# query = "SELECT 1 AS test"
# query_job = client.query(query)
# for row in query_job:
#     print(f"Query Result: {row.test}")
