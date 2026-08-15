import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, avg, max as _max, min as _min, expr, round, when, countDistinct

print("Initializing PySpark...")

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("NpontuECommerceAnalysis") \
    .config("spark.driver.memory", "4g") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def process_data():
    print("Loading data...")
    customers_df = spark.read.csv(os.path.join(DATA_DIR, 'customers.csv'), header=True, inferSchema=True)
    transactions_df = spark.read.csv(os.path.join(DATA_DIR, 'transactions.csv'), header=True, inferSchema=True)
    sessions_df = spark.read.csv(os.path.join(DATA_DIR, 'browsing_sessions.csv'), header=True, inferSchema=True)
    
    # --- Clean Transactions ---
    print("Cleaning transactions...")
    # Remove negative quantities and duplicates
    transactions_df = transactions_df.dropDuplicates()
    transactions_df = transactions_df.filter(col("quantity") > 0)
    
    # --- Feature Engineering: Transactions (RFM & Purchase Behavior) ---
    print("Aggregating transaction features...")
    txn_features = transactions_df.groupBy("customer_id").agg(
        _max("transaction_date").alias("last_purchase_date"),
        count("transaction_id").alias("purchase_frequency"),
        round(_sum("total_amount"), 2).alias("total_spent"),
        round(avg("total_amount"), 2).alias("avg_order_value"),
        _sum(when(col("is_returned") == True, 1).otherwise(0)).alias("total_returns"),
        countDistinct("product_category").alias("unique_categories")
    )
    
    # Calculate return rate
    txn_features = txn_features.withColumn("return_rate", round(col("total_returns") / col("purchase_frequency"), 4))
    
    # --- Feature Engineering: Sessions (Browsing Behavior) ---
    print("Aggregating session features...")
    sess_features = sessions_df.groupBy("customer_id").agg(
        round(avg("duration_minutes"), 2).alias("avg_session_duration"),
        round(avg("pages_viewed"), 2).alias("avg_pages_per_session"),
        count("session_id").alias("total_sessions"),
        _sum(when(col("bounced") == True, 1).otherwise(0)).alias("bounced_sessions")
    )
    
    sess_features = sess_features.withColumn("bounce_rate", round(col("bounced_sessions") / col("total_sessions"), 4))
    
    # --- Join Everything ---
    print("Joining features to customer profiles...")
    final_df = customers_df.join(txn_features, on="customer_id", how="left") \
                           .join(sess_features, on="customer_id", how="left")
                           
    # Compute recency (days between last purchase and end date 2026-06-01)
    final_df = final_df.withColumn("recency_days", 
                                   expr("datediff(to_date('2026-06-01'), to_date(last_purchase_date))"))
    
    # Calculate customer tenure
    final_df = final_df.withColumn("customer_tenure_days", 
                                   expr("datediff(to_date('2026-06-01'), to_date(signup_date))"))
                                   
    # Fill nulls for customers who never bought anything or had sessions
    final_df = final_df.fillna({
        'purchase_frequency': 0,
        'total_spent': 0,
        'avg_order_value': 0,
        'total_returns': 0,
        'unique_categories': 0,
        'return_rate': 0.0,
        'total_sessions': 0,
        'bounce_rate': 0.0,
        'avg_session_duration': 0.0,
        'avg_pages_per_session': 0.0
    })
    
    print("Saving processed features...")
    # Save as CSV (coalesce to 1 partition for easy notebook loading)
    output_path = os.path.join(DATA_DIR, 'customer_features_processed')
    final_df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")
    print(f"Features saved to {output_path}")

if __name__ == "__main__":
    process_data()
    spark.stop()
