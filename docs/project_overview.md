# Project Overview

This repository contains a marketing analytics platform built with dbt, BigQuery, and AI-driven reporting.

## What’s included

- `dbt/`: transformation models, snapshots, macros, and tests.
- `ai/`: scripts to generate executive marketing reports and AI-powered insights.
- `docs/`: architecture documentation, project overview, and project journey.
- `screenshots/`: visual assets for dashboards and executive summaries.
- `data/`: source descriptions and supporting data documentation.

## Project Journey

Read the full project journey and technical documentation in `docs/project_journey.md`.

## Purpose

The project is designed to extract, transform, and analyze marketing and sales data, then generate executive-ready insights using an LLM.

## How to run

1. Create a `.env` file with your OpenRouter API key.
2. Place your Google Cloud service account JSON file in `credentials/`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the AI report generator:

```bash
python ai/generate_insights.py
```
