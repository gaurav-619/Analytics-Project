# Marketing Analytics Platform – Project Journey & Technical Documentation

## Project Objective
The goal of this project was to build an end-to-end Marketing Analytics Platform that simulates a real-world Analytics Engineering workflow.

Rather than focusing only on dashboards, the project was designed to cover:

- Data Warehousing
- Analytics Engineering
- Dimensional Modeling
- dbt Transformations
- Data Quality
- Incremental Processing
- Historical Tracking
- Business Intelligence
- AI-Powered Reporting

The objective was to understand not only how to create reports but also how modern analytics platforms are architected.

---

# Phase 1 – Understanding the Business Problem
We started by identifying the key business questions stakeholders would ask.

### Sales Questions

- What products generate the most revenue?
- Which customer segments perform best?
- What is the average order value?
- Which channels drive sales?

### Marketing Questions

- Which campaigns are effective?
- Which channels generate the highest revenue?
- Which target segments respond best?
- Which campaign objectives create the highest uplift?

### Funnel Questions

- Where do customers drop off?
- What is the overall conversion rate?
- Which stage causes the largest loss?

### Experimentation Questions

- Which variant performs best?
- Should the business deploy a new version?
- How do variants compare to the control group?

---

# Phase 2 – Data Source Selection

## What We Chose
A retail and marketing dataset sourced from Kaggle.

### Why?

- Large enough for analytical use cases.
- Contains transactions, customer behavior, marketing campaigns, and events.
- Supports multiple business domains.

### Why Not Generate Synthetic Data?
Although synthetic generation was discussed, the Kaggle dataset provided richer and more realistic business scenarios.

Decision:

Use Kaggle as the source system.

---

# Phase 3 – BigQuery Data Warehouse
The raw data was loaded into BigQuery.

Purpose:

- Centralized analytical storage.
- Scalable querying.
- Integration with dbt.
- Integration with Looker Studio.

Architecture:

Raw Data → BigQuery → dbt → Analytics Marts → Dashboards

---

# Phase 4 – Staging Layer
Created:

- stg_customers
- stg_products
- stg_campaigns
- stg_transactions
- stg_events

Purpose:

- Standardize data.
- Clean source inconsistencies.
- Isolate raw source logic.

Why?

Because raw data should not directly feed business reports.

Benefits:

- Reusable transformations.
- Easier maintenance.
- Better debugging.

---

# Phase 5 – Dimensional Modeling
Created:

- dim_customers
- dim_products
- dim_campaigns

Purpose:

Provide business context.

Example:

Instead of storing only product_id, analysts can access:

- Brand
- Category
- Product attributes

Why Dimensions?

Dimensions provide descriptive information used for slicing and filtering.

---

# Phase 6 – Fact Tables
Created:

- fct_transactions
- fct_events

Purpose:

Store measurable business events.

Transactions represent:

- Revenue
- Quantity
- Orders

Events represent:

- Views
- Clicks
- Add-to-Cart
- Purchases

Why Facts?

Facts are the foundation for analytical calculations.

---

# Phase 7 – Star Schema Design
Implemented:

Dimensions connected to facts.

Benefits:

- Faster analytical queries.
- Industry-standard warehouse design.
- Easier reporting.

Why Star Schema?

Because analytical workloads benefit from denormalized access patterns.

---

# Phase 8 – Data Quality Testing
Implemented dbt tests:

- unique
- not_null
- relationships

Purpose:

Ensure trusted data.

Why?

Dashboards are only as reliable as the underlying data.

---

# Phase 9 – Customer Snapshot
Implemented:

customer_snapshot

Purpose:

Track customer attribute changes over time.

Problem Solved:

Without snapshots:

Current state only.

With snapshots:

Historical state preserved.

Example:

A customer changing loyalty tiers can be analyzed historically.

Why Not Store Only Current Data?

Because historical analysis becomes impossible.

---

# Phase 10 – Incremental Processing
Implemented:

fct_transactions_incremental

Purpose:

Process only new records.

Logic:

SELECT *
FROM raw_transactions_incremental

WHERE timestamp >
(
SELECT MAX(timestamp)
FROM target_table
)

Problem Solved:

Avoid full-table rebuilds.

Benefits:

- Faster processing.
- Lower cost.
- Scalable architecture.

Why Not Full Refresh Every Time?

Because production systems receive continuous data and full refreshes become expensive.

---

# Phase 11 – Analytics Marts
Created:

## mart_sales_summary
Answers:

- Revenue
- Transactions
- Units Sold
- Average Order Value

---

## mart_conversion_funnel
Answers:

- Conversion Rate
- Drop-off Rate

Key Calculation:

Drop-off Rate = 1 - Current Stage Users / Previous Stage Users

Observation:

Largest drop-off occurs before purchase.

---

## mart_ab_test_performance
Answers:

- Variant Performance
- Conversion Rate
- Experiment Outcome

Observation:

Control group outperformed both variants.

Decision:

Do not deploy variants.

---

## mart_campaign_performance
Answers:

- Revenue by Channel
- Revenue by Objective
- Revenue by Segment
- Expected Uplift

Observation:

Affiliate generated highest revenue.

---

## mart_customer_analytics
Purpose:

Customer segmentation analysis.

Why Created?

To support future customer-focused reporting.

---

## mart_customer_cohort_retention
Purpose:

Track retention by cohort.

Why Created?

To support long-term retention analysis.

Why No Dashboard?

The mart itself provides analytical value and can support future visualizations.

---

# Phase 12 – Dashboard Development
Dashboard 1:

Sales Analytics

KPIs:

- Revenue
- Transactions
- Units Sold
- Average Order Value

---
Dashboard 2:

Conversion Funnel Analytics

KPIs:

- Overall Conversion Rate
- Purchase Conversion Rate
- Drop-off Analysis

Key Insight:

Largest drop-off occurs before purchase.

---
Dashboard 3:

A/B Testing Analytics

KPIs:

- Conversion Rate
- Purchase Users
- Session Duration

Key Insight:

Control group significantly outperformed variants.

---
Dashboard 4:

Campaign Performance Analytics

KPIs:

- Revenue by Channel
- Revenue by Objective
- Revenue by Segment
- Expected Uplift

Key Insight:

Affiliate campaigns generated the highest revenue.

---

# Phase 13 – Live Data Discussion
We evaluated two approaches:

## Google Trends
Pros:

- Real-world data.
- Live updates.

Cons:

- No natural relationship to warehouse entities.
- No shared keys.
- Separate analytics domain.

Decision:

Not selected.

---

## Incremental Transactions
Pros:

- Directly connected to existing facts.
- Same schema.
- Same marts.
- Same dashboards.

Decision:

Selected.

Reason:

Strengthens existing architecture.

---

# Phase 14 – AI Layer
Objective:

Generate automated executive reports.

Architecture:

BigQuery
↓
Analytics Marts
↓
Python KPI Layer
↓
OpenRouter LLM
↓
Executive Report

---

## Why Not Chatbot?
Chatbots answer questions.

The business need was:

Automated reporting.

Decision:

Executive Reporting Automation.

---

## AI Workflow
Step 1:

Query marts.

Step 2:

Calculate business KPIs.

Step 3:

Build business context.

Step 4:

Send context to OpenRouter.

Step 5:

Generate insights.

---

## Why Not Send Raw Tables?
Problems:

- Large token usage.
- Higher cost.
- Increased hallucination risk.

Decision:

Summarize data before sending to AI.

---

## Executive Report Sections
Generated:

- Executive Summary
- Sales Analysis
- Marketing Analysis
- Funnel Analysis
- Experiment Analysis
- Recommendations
- Risks & Opportunities

---

# Final Architecture
Kaggle Dataset
↓
BigQuery
↓
dbt Staging
↓
Dimensions & Facts
↓
Snapshots
↓
Incremental Models
↓
Analytics Marts
↓
├── Looker Dashboards
└── AI Executive Reporting

---

# Technologies Used

- Python
- SQL
- BigQuery
- dbt
- Looker Studio
- OpenRouter
- Llama 3

---

# Key Concepts Learned

- Data Warehousing
- Star Schema Design
- Fact & Dimension Modeling
- Analytics Engineering
- dbt Testing
- Snapshots
- Incremental Models
- Funnel Analytics
- A/B Testing Analytics
- Marketing Analytics
- BI Dashboard Design
- Prompt Engineering
- AI-Powered Reporting

---

# Project Outcome
Built a complete analytics platform capable of:

- Processing historical data
- Handling incremental data loads
- Tracking customer history
- Delivering business dashboards
- Producing AI-generated executive reports

The project demonstrates a full analytics engineering workflow from raw data ingestion to business decision support.
