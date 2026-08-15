# Code Explanation Guide

Use this guide to brush up on how the codebase works in case the interviewers ask you to walk them through your solution.

## 1. Data Generation (`scripts/generate_data.py`)
**Purpose**: Creates the raw synthetic datasets (`customers.csv`, `transactions.csv`, `browsing_sessions.csv`, `product_interactions.csv`).

**Key Talking Points for the Interview**:
- "I used the `Faker` library combined with `numpy` probabilities to generate highly realistic, non-random data."
- "I specifically modeled the data to fit an **African e-commerce context**, including cities across Ghana, Nigeria, Kenya, etc., and region-specific payment methods like Mobile Money."
- "I didn't just create perfect data. I intentionally injected **missing values, outliers, and duplicates** because handling dirty data is a core part of an Intelligent Systems Engineer's job."
- "I programmed inherent behavioral patterns into the data—for instance, users in higher membership tiers inherently have a lower probability of churning, which gives the machine learning model real signal to pick up on."

## 2. Data Processing & Aggregation (`scripts/pandas_processing.py`)
**Purpose**: Takes the raw event logs (transactions and sessions) and aggregates them into customer-level features (RFM metrics).

**Key Talking Points for the Interview**:
- "To prepare the data for modeling, I had to transform the time-series event data into a flattened tabular format per customer."
- "I calculated **RFM metrics** (Recency, Frequency, Monetary value), which are the gold standard for e-commerce customer segmentation."
- "I also engineered behavioral features, such as `bounce_rate` and `avg_session_duration`, because engagement is often a leading indicator of churn before the customer actually stops spending."
- *(If asked why you used Pandas instead of PySpark)*: "I initially designed this to run on PySpark, which is excellent for distributed computing on large datasets. However, for a 2.5 million row dataset, optimized Pandas running locally is highly efficient and removes the overhead of a JVM/Java dependency. For a production environment with billions of rows, I would naturally deploy this on a Spark cluster."

## 3. The Analysis Notebook (`notebooks/analysis.ipynb`)
**Purpose**: The main data science workspace containing EDA, data cleaning, modeling, and insights.

**Key Talking Points for the Interview**:
- **Data Cleaning**: "I imputed missing ages with the median and dropped duplicate transactions and negative quantities, explaining my reasoning at every step."
- **EDA**: "I visualized the distributions to validate assumptions. A key finding was the stark contrast in payment methods across regions—Mobile Money dominating in Ghana versus Credit Cards in South Africa."
- **Modeling**: 
  - "Since we didn't have a hard 'churn' label, I used domain knowledge to define a churned customer as one with a recency > 60 days despite having an account for over 60 days."
  - "I started with a baseline **Logistic Regression** model, but due to class imbalance and non-linear relationships, it struggled."
  - "I then upgraded to **XGBoost**, which natively handles class imbalance (using `scale_pos_weight`) and provided a much stronger AUC-ROC and F1-score."
- **Feature Importance**: "I used the XGBoost feature importance plot to derive the business insights—confirming that session frequency and recency are the strongest predictors of churn."

## 4. Elasticsearch Integration (`scripts/elasticsearch_ingest.py`)
**Purpose**: Ingests the data into Elastic Cloud for the "Big Data Tool" requirement.

**Key Talking Points for the Interview**:
- "To fulfill the Big Data tool utilization requirement, I wrote an ingestion script for **Elasticsearch**."
- "Why Elasticsearch? E-commerce data is heavily event-driven and time-series based. Elasticsearch is purpose-built for indexing log/event data, allowing us to perform sub-second aggregations across millions of rows."
- "By coupling it with Kibana, we can provide business stakeholders with real-time, interactive dashboards without having to build custom frontend analytics portals."
