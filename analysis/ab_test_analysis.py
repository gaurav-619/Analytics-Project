import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account
import os

from statsmodels.stats.proportion import proportions_ztest


# ==========================================
# Create BigQuery Client
# ==========================================

# ==========================================
# BigQuery Authentication
# ==========================================

cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    cred_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "credentials", "service-account.json")
    )

credentials = service_account.Credentials.from_service_account_file(cred_path)

client = bigquery.Client(
    credentials=credentials,
    project="dark-bit-493307-d3"
)

# ==========================================
# Query Experiment Mart
# ==========================================

query = """

select
    experiment_group,
    total_users,
    purchase_users,
    conversion_rate
from marketing_analytics.mart_ab_test_performance

"""


# ==========================================
# Load Data Into Pandas
# ==========================================

experiment_data = client.query(query).to_dataframe()


print("\n=== Experiment Metrics ===\n")
print(experiment_data)


# ==========================================
# Function To Run Z-Test
# ==========================================

def run_ab_test(control_row, variant_row):

    count = [
        control_row['purchase_users'],
        variant_row['purchase_users']
    ]

    nobs = [
        control_row['total_users'],
        variant_row['total_users']
    ]

    z_score, p_value = proportions_ztest(
        count,
        nobs
    )

    print("\n====================================")
    print(f"Control vs {variant_row['experiment_group']}")
    print("====================================")

    print(f"Control Conversion Rate : {control_row['conversion_rate']:.4f}")

    print(
        f"{variant_row['experiment_group']} Conversion Rate : "
        f"{variant_row['conversion_rate']:.4f}"
    )

    uplift = (
        variant_row['conversion_rate']
        - control_row['conversion_rate']
    )

    print(f"Observed Difference : {uplift:.4f}")

    print(f"Z-Score : {z_score:.4f}")
    print(f"P-Value : {p_value:.10f}")

    if p_value < 0.05:
        print("Result : Statistically Significant")
    else:
        print("Result : NOT Statistically Significant")

    if uplift > 0:
        print("Business Outcome : Variant Improved Conversion")
    else:
        print("Business Outcome : Variant Reduced Conversion")


# ==========================================
# Extract Control Group
# ==========================================

control_group = experiment_data[
    experiment_data['experiment_group'] == 'Control'
].iloc[0]


# ==========================================
# Run Tests For All Variants
# ==========================================

variants = experiment_data[
    experiment_data['experiment_group'] != 'Control'
]


for _, variant_row in variants.iterrows():

    run_ab_test(
        control_group,
        variant_row
    )
