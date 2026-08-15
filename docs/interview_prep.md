# Interview Preparation & Reviewer Critique

This document contains a self-audit of your submission against the assignment requirements, an honest critique from the perspective of a Senior Engineer/Hiring Manager, and potential interview questions you should be prepared for.

---

## Part 1: Requirements Cross-Check

| Requirement | Status | How We Met It |
|---|---|---|
| **Synthetic Dataset** (Demographics, browsing, purchase, interactions) | ✅ PASS | `generate_data.py` builds ~2.5M rows across 4 tables with realistic African market patterns. |
| **Data Analysis** (EDA, missing values, duplicates, outliers) | ✅ PASS | Addressed in `analysis.ipynb` (Sections 1-3). Imputed missing ages, dropped duplicate transactions and negative quantities. |
| **Feature Engineering** (Meaningful features, normalization) | ✅ PASS | Aggregated RFM (Recency, Frequency, Monetary) and engagement metrics via Pandas. Used `StandardScaler` in the ML pipeline. |
| **Predictive Modeling** (Churn/Sales/Recs, validation metrics) | ✅ PASS | Built a baseline Logistic Regression and a final XGBoost model predicting Churn. Evaluated using F1-score, Precision, Recall, and AUC-ROC on a stratified hold-out test set. |
| **Big Data Tool Utilization** (Kafka/Grafana/Elasticsearch) | ✅ PASS | Built `elasticsearch_ingest.py` to index the processed data, and justified Elasticsearch in the README as the optimal tool for time-series event data. |
| **Insight and Visualization** (Actionable business insights) | ✅ PASS | Visualized feature correlations, geographical distributions, and XGBoost feature importance. Provided 4 specific business recommendations in the notebook. |
| **Documentation and Presentation** (Report, comments) | ✅ PASS | Comprehensive `README.md`, well-commented code, plus this `docs/` folder for presentation support. |

---

## Part 2: The "HR & Technical Reviewer" Critique

If I were reviewing this submission as a Senior Data/Systems Engineer at Npontu, here is my honest assessment:

### 🌟 What I Love (Standout Features)
1. **End-to-End Architecture**: Most candidates just submit a single, messy Jupyter notebook. You submitted a proper software engineering pipeline (generation script -> processing script -> notebook -> database ingestion). This shows you understand production systems, not just academic data science.
2. **Domain Awareness**: Tailoring the data to the African context (Ghana/Nigeria/Kenya, Mobile Money vs Credit Card) shows immense commercial awareness. You didn't just analyze numbers; you analyzed the *business*.
3. **Pipeline Modularity**: Separating the heavy data aggregation (`pandas_processing.py`) from the machine learning (`analysis.ipynb`) is exactly how things are done in the real world.
4. **Tool Justification**: You explicitly justified *why* you chose Elasticsearch and XGBoost in the README, which hits the assignment's grading criteria perfectly.

### ⚠️ Where I Will Probe (Potential Weaknesses to Defend)
1. **No Explicit Cross-Validation**: 
   - *Critique*: The assignment mentions using techniques "such as cross-validation". You used a standard 80/20 train/test split.
   - *Your Defense*: "Given the dataset size (~50k customers) and the fact that I used `stratify=y` to maintain the class balance, a hold-out test set provides a reliable estimate. However, for a production model, I would implement `StratifiedKFold` (5-fold) during the hyperparameter tuning phase to ensure the model's stability."
2. **Pandas instead of PySpark**: 
   - *Critique*: You used Pandas for data processing instead of a distributed tool like Spark.
   - *Your Defense*: "I initially considered PySpark, but for a 2.5 million row dataset, Pandas is actually faster and more resource-efficient when run locally, avoiding the JVM overhead. I fulfilled the Big Data requirement by architecting the Elasticsearch integration, which is where the real-time scale happens in an event-driven e-commerce environment."
3. **Heuristic Churn Definition**: 
   - *Critique*: You defined churn manually as `recency_days > 60`.
   - *Your Defense*: "Because the data is synthetic and lacked a hard 'account closed' flag, I applied a standard e-commerce heuristic. In a real-world scenario at Npontu, I would collaborate with the product team to define the exact window for churn based on historical customer lifetime value (CLV) decay."

---

## Part 3: Potential Interview Questions & Answers

**Q1: Why did you choose XGBoost over a simpler model or a Neural Network?**
**Answer**: "I started with Logistic Regression as a baseline, but e-commerce behavior features often have non-linear relationships (e.g., spending frequency vs. age). XGBoost is currently the industry standard for tabular data because it handles these non-linearities natively, deals gracefully with missing values, and allows us to easily extract feature importance to drive business decisions. A Neural Network would be overkill for 50,000 rows and lacks the interpretability the business needs."

**Q2: How would you deploy this pipeline into a production environment?**
**Answer**: "I would containerize the ingestion scripts using Docker and schedule them via Apache Airflow to run nightly. The aggregated features would be stored in a feature store or data warehouse (like BigQuery or Snowflake). The XGBoost model could be served via a FastAPI microservice, where the frontend queries the API to get a real-time churn risk score for a user."

**Q3: If you had an extra week, what would you add to this analysis?**
**Answer**: "I would add an RFM clustering model (using K-Means) to automatically segment customers into 'Champions', 'At Risk', and 'Hibernating'. I would also spend more time tuning the XGBoost hyperparameters using Bayesian Optimization, and perhaps add SHAP values to explain individual predictions—for instance, telling the marketing team exactly *why* a specific user is at 85% risk of churning."

**Q4: Can you explain the Elastic Cloud architecture you proposed?**
**Answer**: "Because browsing sessions and transactions are time-series events, traditional relational databases can get slow when doing heavy aggregations. By pushing this data into Elasticsearch, we leverage its inverted indices to allow business stakeholders to instantly search and visualize live data—like tracking cart abandonment in real-time—using Kibana, without writing SQL."
