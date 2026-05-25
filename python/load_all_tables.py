import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Load credentials
script_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(script_dir, "..", "credentials", "service-account.json")

credentials = service_account.Credentials.from_service_account_file(cred_path)

client = bigquery.Client(
    project="dark-bit-493307-d3",
    credentials=credentials
)

dataset_id = f"{credentials.project_id}.marketing_analytics"

tables = {
    "products.csv": "raw_products",
    "customers.csv": "raw_customers",
    "campaigns.csv": "raw_campaigns",
    "events.csv": "raw_events",
    "transactions.csv": "raw_transactions"
}

for file_name, table_name in tables.items():

    file_path = os.path.join(script_dir, "..", "data", file_name)

    print(f"Loading {file_name}...")

    df = pd.read_csv(file_path)

    # 🔧 Fix common dtype issues BEFORE loading

    if "product_id" in df.columns:
        df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce").astype("Int64")

    if "campaign_id" in df.columns:
        df["campaign_id"] = pd.to_numeric(df["campaign_id"], errors="coerce").astype("Int64")

    if "customer_id" in df.columns:
        df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")

    if "gross_revenue" in df.columns:
        df["gross_revenue"] = pd.to_numeric(df["gross_revenue"], errors="coerce")

    # Define schema explicitly (IMPORTANT)
    schema = []

    for col in df.columns:
        if "id" in col:
            schema.append(bigquery.SchemaField(col, "INTEGER"))
        elif "date" in col or "timestamp" in col:
            schema.append(bigquery.SchemaField(col, "TIMESTAMP"))
        elif "revenue" in col or "price" in col:
            schema.append(bigquery.SchemaField(col, "FLOAT"))
        else:
            schema.append(bigquery.SchemaField(col, "STRING"))

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE"  # 🔥 prevents duplicates
    )

    table_id = f"{dataset_id}.{table_name}"

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    job.result()

    print(f"{table_name} loaded successfully")

print("All tables loaded successfully")