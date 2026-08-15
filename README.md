# Npontu Technologies - E-Commerce Data Analysis

This repository contains the solution for the **Intelligent Systems Services Engineer** interview assignment for Npontu Technologies.

## Project Overview

The goal of this project is to analyze a synthetic dataset representing customer activity on an e-commerce platform to extract actionable insights, build a predictive churn model, and demonstrate big data processing capabilities.

**Key Features:**
1. **Synthetic Data Generation**: Simulates a realistic e-commerce environment with 50,000 customers, 500,000 transactions, and over 1.8M behavioral events, specifically tailored to African markets (e.g., Mobile Money preference, key African cities).
2. **Big Data / Data Processing**: Uses optimized **Pandas** to process and aggregate millions of rows of transaction and browsing data efficiently. (Note: Elasticsearch handles the Big Data search/dashboarding requirement).
3. **Data Science & ML**: A complete Jupyter Notebook (`notebooks/analysis.ipynb`) featuring:
   - Exploratory Data Analysis (EDA) and Data Cleaning
   - Feature Engineering (RFM and Behavioral metrics)
   - Predictive Modeling (Logistic Regression baseline & XGBoost)
   - Business Insights and Recommendations
4. **Elasticsearch & Kibana Integration**: Scripts provided to ingest the processed data into **Elastic Cloud** for real-time search and interactive dashboarding, fulfilling the Big Data tooling requirement.

## Directory Structure

```text
Npontu_application/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/                              # Generated CSV datasets and processed features
├── scripts/
│   ├── generate_data.py               # Generates synthetic customers, transactions, sessions
│   ├── pandas_processing.py           # Pandas script for aggregation & feature engineering
│   ├── elasticsearch_ingest.py        # Pushes processed data to Elastic Cloud
│   └── create_notebook.py             # Utility to generate the analysis notebook
├── notebooks/
│   └── analysis.ipynb                 # The main analysis notebook
└── reports/
    └── (Export your notebook to PDF/HTML here)
```

## How to Run the Pipeline

### 1. Setup Environment
Ensure you have Python 3.10+ installed.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Synthetic Data
This script creates the raw datasets (`customers.csv`, `transactions.csv`, `browsing_sessions.csv`, `product_interactions.csv`).

```bash
python scripts/generate_data.py
```
*(Note: This generates ~2.5 million rows total and may take a minute or two.)*

### 3. Run Data Processing
This aggregates transaction history and browsing behavior into customer-level features.

```bash
python scripts/pandas_processing.py
```

### 4. Explore the Analysis
Launch Jupyter Notebook to view the analysis, models, and insights.

```bash
jupyter notebook notebooks/analysis.ipynb
```

### 5. (Optional) Elastic Cloud Ingestion
To view the data in Kibana dashboards, you need an Elastic Cloud account (free trial available). 

1. Set your environment variables:
   ```bash
   export ELASTIC_CLOUD_ID="your_cloud_id_here"
   export ELASTIC_PASSWORD="your_elastic_password_here"
   ```
2. Run the ingestion script:
   ```bash
   python scripts/elasticsearch_ingest.py
   ```
3. Open Kibana, create Data Views for `npontu-customers` and `npontu-transactions`, and build your dashboards.

## Technology Choices & Justification

- **PySpark**: Chosen over pure Pandas for data preparation because joining and aggregating 2.5 million event records can cause memory bottlenecks. PySpark demonstrates an understanding of distributed computing principles essential for "Intelligent Systems."
- **Elasticsearch + Kibana**: The perfect fit for e-commerce event data (like browsing sessions and transactions). It provides out-of-the-box time-series analysis and dashboarding without needing to build custom frontends.
- **XGBoost**: Selected for the churn prediction model due to its robust handling of imbalanced datasets (churn is typically ~25%), non-linear feature relationships, and built-in handling of missing values.
- **African Context**: The synthetic dataset heavily features African cities and Mobile Money to align with the regional realities of African e-commerce, showing domain awareness.
