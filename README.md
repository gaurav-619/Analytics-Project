# Marketing Analytics Platform

## Project Overview

This repository demonstrates a complete marketing analytics engineering workflow built on BigQuery and dbt. The project turns raw customer, product, campaign, event, and transaction data into analytical marts, snapshots, and dashboards.

-it is an analytics platform:

- Raw CSV data is loaded into BigQuery.
- dbt staging models clean and standardize data.
- dbt snapshots preserve historical customer state.
- dbt incremental models process only new transactions.
- Analytical marts answer key business questions.
- Dashboards are described conceptually based on the created marts.

## Business Problem

The goal is to help a marketing and analytics team answer questions such as:

- Which products and campaigns are driving revenue?
- Where are customers dropping off in the conversion funnel?
- Which customer segments are most valuable?
- How do A/B test variants perform?
- How can incremental ingestion reduce cost and processing time?

## Architecture

```
Raw CSV Data
      ↓
BigQuery Data Warehouse
      ↓
dbt Transformation Layer
 ├─ Staging
 ├─ Snapshots
 ├─ Incremental Models
 └─ Marts
      ↓
Analytics Dashboards
```

A more detailed architecture view is available in `docs/architecture.md`.

## What Was Built

### Incremental Loading

- Implemented an incremental dbt model: `dbt/models/marts/fct_transactions_incremental.sql`
- Used `transaction_id` as the unique key.
- Applied timestamp-based watermarking to process only newly arrived records.
- Avoided rebuilding the full fact table on every run.
- Used a landing source table called `raw_transactions_incremental` to support incremental ingestion.

### Snapshots

- Implemented `customer_snapshot` in `dbt/snapshots/customer_snapshot.sql`
- Tracked customer attribute changes over time with a dbt snapshot strategy.
- Preserved historical customer state for analytics.

### dbt Modeling

- Staging models: `stg_transactions`, `stg_products`, `stg_customers`, `stg_campaigns`, `stg_events`
- Dimension models: `dim_products`, `dim_customers`, `dim_campaigns`
- Fact models: `fct_transactions`, `fct_events`
- `fct_transactions` and `fct_events` are both materialized incrementally to support efficient data processing.
- Marts:
  - `mart_sales_summary`
  - `mart_campaign_performance`
  - `mart_customer_analytics`
  - `mart_conversion_funnel`
  - `mart_ab_test_performance`
  - `mart_customer_cohort_retention`

### Data Quality

- dbt tests are defined in `dbt/models/staging/schema.yml`.
- Quality checks include `not_null`, `unique`, `relationships`, and `accepted_values`.

### Dashboards (Conceptual)

This repository does not include actual Looker or dashboard files. The dashboard layer is documented conceptually using the analytics marts.

There is also an analytics script at `analysis/ab_test_analysis.py` that queries `mart_ab_test_performance` and performs statistical comparison across experiment groups.

Key dashboard themes:

- Sales & Business Performance
- Customer Funnel Analytics
- Experimentation & A/B Test Analytics
- Marketing Campaign Performance

## Repository Structure

- `data/` — source CSV files used to populate BigQuery
- `python/` — BigQuery utilities and analytics helpers
  - `load_all_tables.py`
  - `load_products_to_bigquery.py`
  - `query.py` — BigQuery connection verification utility
  - `ingestion.py` — optional Google Trends enrichment script
- `analysis/` — experiment analysis script for evaluating A/B test results
- `ai/` — AI helper scripts and prompt assets
  - `generate_insights.py`
  - `prompts/marketing_prompt.txt`
- `dbt/` — dbt project with models, tests, and snapshots
- `docs/` — architecture documentation
- `dashboards/` — present but currently empty

## Key Files

- `dbt/dbt_project.yml`
- `dbt/models/staging/schema.yml`
- `dbt/models/marts/fct_transactions_incremental.sql`
- `dbt/snapshots/customer_snapshot.sql`
- `python/load_all_tables.py`
- `python/load_products_to_bigquery.py`
- `python/query.py`
- `python/ingestion.py`
- `analysis/ab_test_analysis.py`
- `ai/generate_insights.py`
- `ai/prompts/marketing_prompt.txt`

## How to Run

1. Install dependencies for Python and dbt.
2. Ensure the service account JSON is available at `credentials/service-account.json`.
3. Load raw CSV data into BigQuery:
   - `python python/load_all_tables.py`
   - `python python/load_products_to_bigquery.py`
4. Run dbt:
   - `cd dbt`
   - `dbt deps`
   - `dbt run`
   - `dbt test`
   - `dbt snapshot`

> Note: The Python ingestion scripts are configured for the Google Cloud project `dark-bit-493307-d3` and load data into the dataset `marketing_analytics`.

## Business Impact

This project demonstrates how to build a scalable analytics platform that supports:

- revenue and product performance analysis
- marketing campaign optimization
- customer journey and funnel analysis
- A/B test evaluation
- efficient incremental ingestion
- trusted data via dbt testing and snapshots

## What to Highlight in a Portfolio

- Data warehouse architecture, not just a dashboard
- dbt transformation layer with staging, snapshots, incremental models, and marts
- The star schema design around the transaction fact table and dimensions
- The incremental processing strategy for transaction ingestion
- Analytical output aligned to business questions

## Notes

- `docs/architecture.md` contains a more detailed architecture diagram and explanation.
- The `dashboard/` folder is empty, so dashboard details are described rather than implemented.
