# Architecture Overview

## Data Flow

The analytics platform follows a standard data engineering and analytics engineering flow:

1. Raw data is sourced from CSV files in `data/`.
2. Data is loaded into BigQuery using Python ingestion scripts.
3. dbt cleans, standardizes, and transforms the raw data.
4. dbt snapshots capture changing customer attributes over time.
5. dbt incremental models process only new transaction records from a landing source, including `raw_transactions_incremental`.
6. Analytical marts expose business metrics for dashboards and experimental analysis.

```text
Raw Data
      ↓
BigQuery Warehouse
      ↓
 dbt
   ├─ Staging
   ├─ Snapshots
   ├─ Incremental Models
   └─ Marts
      ↓
Dashboards / Analytics
```

## Star Schema

The core analytical schema centers on a transaction fact table joined to dimension tables:

```text
           dim_customers
                 |
 dim_products -- fct_transactions -- dim_campaigns
```

This model supports high-performance analytics and makes it easy to answer business questions across customers, products, and campaigns.

## dbt Layers

### Staging

The staging layer cleans and standardizes raw source tables.

- `stg_transactions`
- `stg_products`
- `stg_customers`
- `stg_campaigns`
- `stg_events`

### Dimensions

The dimension layer creates analytical lookup tables.

- `dim_products`
- `dim_customers`
- `dim_campaigns`

### Facts

The fact layer stores event-level metrics and joins the dimensions.

- `fct_transactions`
- `fct_events`

### Incremental Models

The incremental model reduces compute and time by processing only new transactions:

- `fct_transactions_incremental`

This model uses `transaction_id` as the unique key and a timestamp watermark to load new rows.

### Snapshots

The snapshot layer preserves historical state for slowly changing customer data:

- `customer_snapshot`

This snapshot tracks updates to customer attributes such as country, age, gender, loyalty tier, and acquisition channel.

### Analytical Marts

Business-facing marts are built for reporting use cases.

- `mart_sales_summary`
- `mart_campaign_performance`
- `mart_customer_analytics`
- `mart_conversion_funnel`
- `mart_ab_test_performance`
- `mart_customer_cohort_retention`

## Pipeline Execution

The pipeline order is typically:

1. Load raw data into BigQuery.
2. Run dbt models (`dbt run`).
3. Run dbt snapshots (`dbt snapshot`).
4. Validate data with dbt tests (`dbt test`).

## Dashboard Story

Although dashboard artifacts are not included in the repository, the analytics marts support the following reporting areas:

- Sales Performance
- Funnel Conversion Analysis
- A/B Testing Insights
- Marketing Campaign Performance

These dashboards would consume the marts and deliver insights to business leaders, growth teams, and product managers.

There is also an analytics script in `analysis/ab_test_analysis.py` that reads the A/B test mart and performs statistical significance testing.
