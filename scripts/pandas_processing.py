import os
import pandas as pd
import numpy as np

print("Initializing Data Processing (Pandas)...")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def process_data():
    print("Loading data...")
    customers_df = pd.read_csv(os.path.join(DATA_DIR, 'customers.csv'))
    transactions_df = pd.read_csv(os.path.join(DATA_DIR, 'transactions.csv'))
    sessions_df = pd.read_csv(os.path.join(DATA_DIR, 'browsing_sessions.csv'))
    
    # --- Clean Transactions ---
    print("Cleaning transactions...")
    transactions_df = transactions_df.drop_duplicates()
    transactions_df = transactions_df[transactions_df['quantity'] > 0]
    
    # --- Feature Engineering: Transactions (RFM & Purchase Behavior) ---
    print("Aggregating transaction features...")
    # Convert date to datetime
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
    customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
    
    txn_features = transactions_df.groupby('customer_id').agg(
        last_purchase_date=('transaction_date', 'max'),
        purchase_frequency=('transaction_id', 'count'),
        total_spent=('total_amount', 'sum'),
        avg_order_value=('total_amount', 'mean'),
        total_returns=('is_returned', 'sum'),
        unique_categories=('product_category', 'nunique')
    ).reset_index()
    
    txn_features['return_rate'] = (txn_features['total_returns'] / txn_features['purchase_frequency']).round(4)
    txn_features['total_spent'] = txn_features['total_spent'].round(2)
    txn_features['avg_order_value'] = txn_features['avg_order_value'].round(2)
    
    # --- Feature Engineering: Sessions (Browsing Behavior) ---
    print("Aggregating session features...")
    sess_features = sessions_df.groupby('customer_id').agg(
        avg_session_duration=('duration_minutes', 'mean'),
        avg_pages_per_session=('pages_viewed', 'mean'),
        total_sessions=('session_id', 'count'),
        bounced_sessions=('bounced', 'sum')
    ).reset_index()
    
    sess_features['bounce_rate'] = (sess_features['bounced_sessions'] / sess_features['total_sessions']).round(4)
    sess_features['avg_session_duration'] = sess_features['avg_session_duration'].round(2)
    sess_features['avg_pages_per_session'] = sess_features['avg_pages_per_session'].round(2)
    
    # Drop bounced_sessions as we have bounce_rate
    sess_features = sess_features.drop(columns=['bounced_sessions'])
    
    # --- Join Everything ---
    print("Joining features to customer profiles...")
    final_df = customers_df.merge(txn_features, on='customer_id', how='left')
    final_df = final_df.merge(sess_features, on='customer_id', how='left')
    
    # Compute recency (days between last purchase and end date 2026-06-01)
    end_date = pd.to_datetime('2026-06-01')
    final_df['recency_days'] = (end_date - final_df['last_purchase_date']).dt.days
    
    # Calculate customer tenure
    final_df['customer_tenure_days'] = (end_date - final_df['signup_date']).dt.days
    
    # Fill nulls for customers who never bought anything or had sessions
    fill_values = {
        'purchase_frequency': 0,
        'total_spent': 0,
        'avg_order_value': 0,
        'total_returns': 0,
        'unique_categories': 0,
        'return_rate': 0.0,
        'total_sessions': 0,
        'bounce_rate': 0.0,
        'avg_session_duration': 0.0,
        'avg_pages_per_session': 0.0,
        'recency_days': 999  # Large number for never purchased
    }
    final_df = final_df.fillna(value=fill_values)
    
    # Convert dates back to strings for CSV output
    final_df['last_purchase_date'] = final_df['last_purchase_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    final_df['signup_date'] = final_df['signup_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print("Saving processed features...")
    out_dir = os.path.join(DATA_DIR, 'customer_features_processed')
    os.makedirs(out_dir, exist_ok=True)
    
    output_path = os.path.join(out_dir, 'features.csv')
    final_df.to_csv(output_path, index=False)
    print(f"Features saved to {output_path}")

if __name__ == "__main__":
    process_data()
