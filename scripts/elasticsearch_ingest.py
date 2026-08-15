import os
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import warnings

# Suppress some elasticsearch warnings for cleaner output
warnings.filterwarnings('ignore')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def connect_elasticsearch():
    print("Connecting to Elasticsearch...")
    print("---")
    print("NOTE: To connect to Elastic Cloud, set the following environment variables:")
    print("export ELASTIC_CLOUD_ID='your_cloud_id'")
    print("export ELASTIC_PASSWORD='your_password'")
    print("---\n")
    
    cloud_id = os.environ.get("ELASTIC_CLOUD_ID")
    password = os.environ.get("ELASTIC_PASSWORD")
    
    try:
        if cloud_id and password:
            print("Using Elastic Cloud credentials...")
            es = Elasticsearch(
                cloud_id=cloud_id,
                basic_auth=("elastic", password)
            )
        else:
            print("No Elastic Cloud credentials found. Attempting to connect to localhost:9200...")
            es = Elasticsearch("http://localhost:9200")
            
        if es.ping():
            print("Connected successfully!")
            return es
        else:
            print("Could not connect to Elasticsearch. Is the cluster running?")
            return None
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def ingest_customers(es):
    print("\nLoading customer features data...")
    features_dir = os.path.join(DATA_DIR, 'customer_features_processed')
    if not os.path.exists(features_dir):
        print(f"Features directory not found at {features_dir}. Did you run spark_processing.py?")
        return
        
    csv_files = [f for f in os.listdir(features_dir) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in features directory.")
        return
        
    # PySpark outputs as part-00000...csv
    df = pd.read_csv(os.path.join(features_dir, csv_files[0]))
    print(f"Loaded {len(df)} customer records.")
    
    index_name = 'npontu-customers'
    
    # Map specific types for Kibana
    mapping = {
        "mappings": {
            "properties": {
                "signup_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "last_purchase_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "total_spent": {"type": "double"},
                "purchase_frequency": {"type": "integer"},
                "country": {"type": "keyword"},
                "city": {"type": "keyword"},
                "membership_tier": {"type": "keyword"},
                "preferred_device": {"type": "keyword"},
                "referral_source": {"type": "keyword"}
            }
        }
    }
    
    if es.indices.exists(index=index_name):
        print(f"Index {index_name} already exists. Deleting it...")
        es.indices.delete(index=index_name)
        
    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")
    
    def generate_actions():
        for _, row in df.iterrows():
            doc = row.dropna().to_dict()
            yield {
                "_index": index_name,
                "_id": doc['customer_id'],
                "_source": doc
            }
            
    print(f"Ingesting customers into {index_name}...")
    success, failed = helpers.bulk(es, generate_actions(), chunk_size=500, stats_only=True)
    print(f"Ingested {success} documents. Failed: {failed}")

def ingest_transactions(es):
    print("\nLoading transaction data...")
    tx_file = os.path.join(DATA_DIR, 'transactions.csv')
    if not os.path.exists(tx_file):
        print("transactions.csv not found.")
        return
        
    df = pd.read_csv(tx_file)
    # We sample 50k transactions to not overload a free tier Elastic Cloud instance
    sample_size = min(50000, len(df))
    print(f"Loaded {len(df)} transactions. Sampling {sample_size} for Elastic Cloud...")
    df = df.sample(n=sample_size, random_state=42)
    
    index_name = 'npontu-transactions'
    mapping = {
        "mappings": {
            "properties": {
                "transaction_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "product_category": {"type": "keyword"},
                "payment_method": {"type": "keyword"},
                "total_amount": {"type": "double"},
                "unit_price": {"type": "double"},
                "quantity": {"type": "integer"}
            }
        }
    }
    
    if es.indices.exists(index=index_name):
        print(f"Index {index_name} already exists. Deleting it...")
        es.indices.delete(index=index_name)
        
    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")
    
    def generate_actions():
        for _, row in df.iterrows():
            doc = row.dropna().to_dict()
            yield {
                "_index": index_name,
                "_id": doc['transaction_id'],
                "_source": doc
            }
            
    print(f"Ingesting transactions into {index_name}...")
    success, failed = helpers.bulk(es, generate_actions(), chunk_size=1000, stats_only=True)
    print(f"Ingested {success} documents. Failed: {failed}")

if __name__ == "__main__":
    es_client = connect_elasticsearch()
    if es_client:
        ingest_customers(es_client)
        ingest_transactions(es_client)
        print("\nElasticsearch ingestion complete!")
        print("You can now open Kibana and create Data Views for 'npontu-customers' and 'npontu-transactions'.")
