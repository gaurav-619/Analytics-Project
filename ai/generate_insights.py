from google.cloud import bigquery
from google.oauth2 import service_account
from openai import OpenAI
import glob
import os
import pandas as pd

# Read .env file directly
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_file = os.path.join(project_root, ".env")

if os.path.exists(env_file):
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
            for line in content.split("\n"):
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    os.environ[key] = value
    except Exception as e:
        raise ValueError(f"Failed to read .env file: {e}")
else:
    raise FileNotFoundError(f".env file not found at: {env_file}")

api_key = os.getenv("OPENROUTER_API_KEY")

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_dir = os.path.join(script_dir, "..", "credentials")
cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not cred_path:
    default_path = os.path.join(credentials_dir, "service-account.json")
    if os.path.exists(default_path):
        cred_path = default_path
    else:
        json_files = glob.glob(os.path.join(credentials_dir, "*.json"))
        if json_files:
            cred_path = json_files[0]

if cred_path and os.path.exists(cred_path):
    credentials = service_account.Credentials.from_service_account_file(cred_path)
    client = bigquery.Client(project="dark-bit-493307-d3", credentials=credentials)
else:
    raise FileNotFoundError(
        "No Google Cloud service account JSON file found. "
        "Set GOOGLE_APPLICATION_CREDENTIALS or place a JSON key in credentials/."
    )

# SALES SUMMARY
# =====================================================

sales_query = """
SELECT
    ROUND(SUM(net_revenue),2) AS total_revenue,
    SUM(total_transactions) AS total_transactions,
    ROUND(AVG(avg_order_value),2) AS avg_order_value
FROM marketing_analytics.mart_sales_summary
"""

sales_df = client.query(sales_query).to_dataframe()

# =====================================================
# TOP SALES CHANNEL
# =====================================================

top_channel_query = """
SELECT
    channel,
    ROUND(SUM(net_revenue),2) AS revenue
FROM marketing_analytics.mart_sales_summary
GROUP BY channel
ORDER BY revenue DESC
LIMIT 1
"""

top_channel_df = client.query(top_channel_query).to_dataframe()

# =====================================================
# FUNNEL SUMMARY
# =====================================================

funnel_query = """
SELECT
    event_type,
    overall_conversion_rate,
    dropoff_rate
FROM marketing_analytics.mart_conversion_funnel
ORDER BY stage_order
"""

funnel_df = client.query(funnel_query).to_dataframe()

purchase_row = funnel_df[
    funnel_df["event_type"].str.lower() == "purchase"
]

if purchase_row.empty:
    raise ValueError("Purchase row not found in funnel data")

purchase_conversion = purchase_row[
    "overall_conversion_rate"
].iloc[0]

highest_dropoff = funnel_df.loc[
    funnel_df["dropoff_rate"].idxmax(),
    "event_type"
]

# =====================================================
# A/B TEST SUMMARY
# =====================================================

ab_query = """
SELECT *
FROM marketing_analytics.mart_ab_test_performance
"""

ab_df = client.query(ab_query).to_dataframe()

best_variant = ab_df.loc[
    ab_df["conversion_rate"].idxmax(),
    "experiment_group"
]

best_conversion = ab_df["conversion_rate"].max()

# =====================================================
# CAMPAIGN SUMMARY
# =====================================================

campaign_query = """
SELECT
    channel,
    ROUND(SUM(total_revenue),2) AS revenue,
    ROUND(AVG(expected_uplift),3) AS avg_uplift
FROM marketing_analytics.mart_campaign_performance
GROUP BY channel
ORDER BY revenue DESC
"""

campaign_df = client.query(campaign_query).to_dataframe()

best_channel = campaign_df.iloc[0]["channel"]
top_marketing_channel = campaign_df.iloc[0]["channel"]
top_marketing_revenue = campaign_df.iloc[0]["revenue"]

# =====================================================
# BUILD BUSINESS CONTEXT
# =====================================================

total_revenue = sales_df.iloc[0]["total_revenue"]

business_context = f"""
SALES SUMMARY

Total Revenue:
{total_revenue:,.2f}

Total Transactions:
{sales_df.iloc[0]["total_transactions"]}

Average Order Value:
{sales_df.iloc[0]["avg_order_value"]}

Top Revenue Channel:
{top_channel_df.iloc[0]["channel"]}


FUNNEL SUMMARY

Purchase Conversion Rate:
{purchase_conversion:.2%}

Highest Dropoff Stage:
{highest_dropoff}


A/B TEST SUMMARY

Best Variant:
{best_variant}

Best Conversion Rate:
{best_conversion:.2%}


MARKETING SUMMARY

Top Marketing Channel:
{top_marketing_channel}

Marketing Revenue:
{top_marketing_revenue:,.2f}

Campaign Performance:

{campaign_df.to_string(index=False)}

TOP INSIGHTS

Highest Revenue Marketing Channel:
{best_channel}

Best Experiment Group:
{best_variant}

Highest Funnel Dropoff:
{highest_dropoff}
"""

# =====================================================
# PROMPT
# =====================================================

prompt = f"""
You are a Senior Business Analytics Director.

Analyze the following business performance metrics.

Generate a structured executive report using the following sections:

1. Executive Summary
2. Sales Performance Analysis
3. Marketing Performance Analysis
4. Funnel Analysis
5. Experiment Analysis
6. Strategic Recommendations
7. Risks & Opportunities

Requirements:
- Use markdown headings.
- Reference the provided metrics.
- Do not invent values.
- Avoid recalculating metrics.
- Focus on business impact.

Business Metrics:

{business_context}
"""

print("\n=== BUSINESS CONTEXT ===\n")
print(business_context)

# Call OpenAI API via OpenRouter
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

client_ai = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

print("\nCalling OpenRouter...")
try:
    response = client_ai.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": """
                You are a Senior Business Analytics Director.

                Your role is to analyze sales,
                marketing, customer funnel,
                and experimentation metrics.

                Produce executive-level insights,
                recommendations, risks, and opportunities.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )
except Exception as e:
    raise ValueError(f"OpenRouter API call failed: {e}")

print("\nAI response received.")

insights = response.choices[0].message.content

report_path = os.path.join(
    script_dir,
    "executive_report.md"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:
    f.write(insights)

print(insights)
print(f"\nExecutive report saved to {report_path}")
