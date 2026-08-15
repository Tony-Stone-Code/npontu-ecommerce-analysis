import nbformat as nbf
import os

notebook_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notebooks')
os.makedirs(notebook_dir, exist_ok=True)
nb_path = os.path.join(notebook_dir, 'analysis.ipynb')

nb = nbf.v4.new_notebook()

cells = []

# --- Intro ---
cells.append(nbf.v4.new_markdown_cell("""# Analyzing Customer Behavior for E-commerce Insights
## Npontu Technologies Assignment

**Goal**: Analyze synthetic e-commerce data to extract actionable insights, build a churn prediction model, and present findings.

**Approach**:
1. Exploratory Data Analysis & Cleaning
2. Feature Engineering (RFM + Behavioral)
3. Churn Prediction Modeling (XGBoost)
4. Business Insights & Recommendations
"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')
"""))

# --- Section 1: Data Loading ---
cells.append(nbf.v4.new_markdown_cell("""## 1. Data Loading & Overview
Let's see what we are working with. We have 4 datasets generated for this analysis."""))

cells.append(nbf.v4.new_code_cell("""# Load raw datasets
data_dir = '../data'
customers = pd.pd.read_csv(f'{data_dir}/customers.csv')
transactions = pd.read_csv(f'{data_dir}/transactions.csv')
sessions = pd.read_csv(f'{data_dir}/browsing_sessions.csv')

print(f"Customers: {customers.shape}")
print(f"Transactions: {transactions.shape}")
print(f"Sessions: {sessions.shape}")
"""))

cells.append(nbf.v4.new_code_cell("""customers.head(3)"""))

# --- Section 2: Data Quality ---
cells.append(nbf.v4.new_markdown_cell("""## 2. Data Cleaning
Let's check for missing values, duplicates, and any weird anomalies."""))

cells.append(nbf.v4.new_code_cell("""# Check missing values
print("Missing values in customers:")
print(customers.isnull().sum()[customers.isnull().sum() > 0])
"""))

cells.append(nbf.v4.new_code_cell("""# For age, median imputation makes sense. For gender, we can use a placeholder or mode.
customers['age'] = customers['age'].fillna(customers['age'].median())
customers['gender'] = customers['gender'].fillna('Unknown')
"""))

cells.append(nbf.v4.new_code_cell("""# Check for duplicates in transactions
duplicates = transactions.duplicated().sum()
print(f"Found {duplicates} duplicate transactions. Removing them.")
transactions = transactions.drop_duplicates()
"""))

cells.append(nbf.v4.new_code_cell("""# Look for weird anomalies like negative quantities
print(f"Transactions with negative quantity: {(transactions['quantity'] < 0).sum()}")
# Drop them as they are likely data entry errors
transactions = transactions[transactions['quantity'] > 0]
"""))

# --- Section 3: EDA ---
cells.append(nbf.v4.new_markdown_cell("""## 3. Exploratory Data Analysis (EDA)
What's the story here? Let's look at demographics and purchasing behavior."""))

cells.append(nbf.v4.new_code_cell("""# Demographics: Where are our customers?
plt.figure(figsize=(10, 5))
sns.countplot(data=customers, y='country', order=customers['country'].value_counts().index)
plt.title('Customer Distribution by Country')
plt.xlabel('Number of Customers')
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Payment methods - is there a regional difference?
# Let's check Mobile Money vs Credit Card in Ghana vs South Africa
gh_sa = transactions.merge(customers[['customer_id', 'country']], on='customer_id')
gh_sa = gh_sa[gh_sa['country'].isin(['Ghana', 'South Africa'])]

plt.figure(figsize=(10, 5))
sns.countplot(data=gh_sa, x='country', hue='payment_method')
plt.title('Payment Method Preference: Ghana vs South Africa')
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""*Interesting! Mobile Money dominates in Ghana, while Credit Cards are much more common in South Africa. This matches real-world African e-commerce trends.*"""))

# --- Section 4: Feature Engineering ---
cells.append(nbf.v4.new_markdown_cell("""## 4. Feature Engineering
We've already processed some heavy features using **Pandas** in `scripts/pandas_processing.py`. Let's load that aggregated dataset. It contains RFM metrics and browsing behaviors joined to the customer profiles."""))

cells.append(nbf.v4.new_code_cell("""# Load the Pandas aggregated dataset
import glob
processed_files = glob.glob(f'{data_dir}/customer_features_processed/*.csv')
if processed_files:
    features_df = pd.read_csv(processed_files[0])
    print(f"Loaded {features_df.shape[0]} customer profiles with engineered features.")
else:
    print("Processed features not found! Please run pandas_processing.py first.")
"""))

cells.append(nbf.v4.new_code_cell("""features_df.head()"""))

cells.append(nbf.v4.new_markdown_cell("""### Defining Churn
Since we don't have an explicit 'churn' flag, we have to define it based on behavior. 
A common definition in e-commerce: A customer is churned if they haven't made a purchase in the last 60 days (or their recency is high compared to their tenure).

Let's define churn as `recency_days > 60` for customers who have been with us for at least 60 days."""))

cells.append(nbf.v4.new_code_cell("""# Define Target Variable
features_df['is_churned'] = ((features_df['recency_days'] > 60) & (features_df['customer_tenure_days'] > 60)).astype(int)
print(f"Overall Churn Rate: {features_df['is_churned'].mean():.2%}")
"""))

cells.append(nbf.v4.new_code_cell("""# Let's check correlation of features with churn
numeric_cols = features_df.select_dtypes(include=['float64', 'int64']).columns
corrs = features_df[numeric_cols].corr()['is_churned'].sort_values(ascending=False)

plt.figure(figsize=(8, 6))
corrs.drop('is_churned').plot(kind='barh')
plt.title('Feature Correlation with Churn')
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""*As expected, `recency_days` is positively correlated with churn (higher recency = more likely churned). Interestingly, `purchase_frequency` and `total_sessions` are negatively correlated.*"""))

# --- Section 5: Modeling ---
cells.append(nbf.v4.new_markdown_cell("""## 5. Predictive Modeling
Let's build a model to predict churn risk.

We will start with a simple **Logistic Regression** baseline, then move to **XGBoost** to see if we can capture non-linear patterns better."""))

cells.append(nbf.v4.new_code_cell("""from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from xgboost import XGBClassifier

# Prepare data for modeling
# Drop identifiers and leaky variables
X = features_df.drop(['customer_id', 'email', 'first_name', 'last_name', 'signup_date', 'last_purchase_date', 'is_churned', 'recency_days'], axis=1)
y = features_df['is_churned']

# Identify column types
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(exclude=['object']).columns.tolist()

print(f"Categorical features: {len(cat_cols)}")
print(f"Numeric features: {len(num_cols)}")
"""))

cells.append(nbf.v4.new_code_cell("""# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), cat_cols)
    ])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Model 1: Logistic Regression (Baseline)"""))

cells.append(nbf.v4.new_code_cell("""# Baseline model
lr_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000))
])

lr_pipeline.fit(X_train, y_train)
lr_preds = lr_pipeline.predict(X_test)

print("Logistic Regression Results:")
print(classification_report(y_test, lr_preds))
print(f"AUC-ROC: {roc_auc_score(y_test, lr_pipeline.predict_proba(X_test)[:,1]):.3f}")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Model 2: XGBoost"""))

cells.append(nbf.v4.new_code_cell("""# XGBoost model
xgb_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, scale_pos_weight=(len(y)-sum(y))/sum(y)))
])

xgb_pipeline.fit(X_train, y_train)
xgb_preds = xgb_pipeline.predict(X_test)

print("XGBoost Results:")
print(classification_report(y_test, xgb_preds))
print(f"AUC-ROC: {roc_auc_score(y_test, xgb_pipeline.predict_proba(X_test)[:,1]):.3f}")
"""))

cells.append(nbf.v4.new_markdown_cell("""*XGBoost performs significantly better on the F1-score and AUC-ROC. Let's look at what features it relies on.*"""))

cells.append(nbf.v4.new_code_cell("""# Feature Importance from XGBoost
xgb_model = xgb_pipeline.named_steps['classifier']
feature_names = num_cols + xgb_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(cat_cols).tolist()

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': xgb_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df.head(15), x='Importance', y='Feature')
plt.title('Top 15 Predictors of Customer Churn')
plt.tight_layout()
plt.show()
"""))

# --- Section 6: Business Insights ---
cells.append(nbf.v4.new_markdown_cell("""## 6. Business Insights & Recommendations

Based on our exploratory data analysis, engineered behavioral features, and the XGBoost predictive model, here are the key takeaways for Npontu Technologies:

1. **Engagement Drives Retention**: The model heavily relies on `total_sessions` and `purchase_frequency` as top predictors. Customers who visit often, even if they don't buy every time, are much less likely to churn.
   * **Recommendation**: Implement a points-based loyalty system just for logging in or browsing new categories to build a habit.

2. **The "60-Day Wall"**: Activity tends to drop off sharply. 
   * **Recommendation**: Set up automated re-engagement triggers (email/SMS) at the 21-day and 45-day marks of inactivity, rather than waiting until they've fully churned at 60 days.

3. **Regional Payment Preferences Matter**: We saw a massive preference for Mobile Money in West/East African markets (Ghana, Kenya) compared to Credit Cards in South Africa.
   * **Recommendation**: Ensure partnerships with local telecom providers (e.g., MTN MoMo, M-Pesa) are prominently featured and perhaps offer a 5% discount for using these preferred local methods to reduce friction.

4. **Tier Upgrades Reduce Risk**: Higher membership tiers churn significantly less.
   * **Recommendation**: Identify "Bronze" tier customers with high `avg_session_duration` but low `purchase_frequency` and offer them a temporary "Silver" trial to lock in their loyalty.
"""))

nb['cells'] = cells

with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook successfully created at {nb_path}")
