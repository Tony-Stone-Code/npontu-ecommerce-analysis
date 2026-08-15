import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import uuid

print("Initializing data generation...")

# Initialize Faker
fake = Faker()
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 50000
NUM_TRANSACTIONS = 500000
NUM_SESSIONS = 800000
NUM_INTERACTIONS = 1000000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 6, 1)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

os.makedirs(DATA_DIR, exist_ok=True)

AFRICAN_CITIES = {
    'Ghana': ['Accra', 'Kumasi', 'Tamale', 'Takoradi', 'Cape Coast'],
    'Nigeria': ['Lagos', 'Abuja', 'Kano', 'Ibadan', 'Port Harcourt'],
    'Kenya': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'],
    'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth'],
    'Tanzania': ['Dar es Salaam', 'Mwanza', 'Arusha', 'Dodoma', 'Mbeya'],
    'Rwanda': ['Kigali', 'Butare', 'Gitarama', 'Ruhengeri', 'Gisenyi']
}

def generate_customers():
    print(f"Generating {NUM_CUSTOMERS} customers...")
    customers = []
    countries = list(AFRICAN_CITIES.keys())
    country_weights = [0.25, 0.35, 0.15, 0.15, 0.05, 0.05]
    days_range = (END_DATE - START_DATE).days
    
    # To model churn, let's designate some as churned so we can adjust their activity later
    # We won't output the "is_churned" flag explicitly, they have to find it, 
    # but we will use it to shape the data. A churned user stops acting before END_DATE.
    
    for i in range(1, NUM_CUSTOMERS + 1):
        country = np.random.choice(countries, p=country_weights)
        city = random.choice(AFRICAN_CITIES[country])
        
        # Age distribution
        age = int(np.random.gamma(shape=5.0, scale=6.0) + 18)
        if age > 75: age = random.randint(18, 75)
            
        gender = np.random.choice(['Male', 'Female', 'Non-binary'], p=[0.48, 0.48, 0.04])
        
        signup_offset = random.randint(0, days_range - 30) # at least 30 days before end
        signup_date = START_DATE + timedelta(days=signup_offset)
        
        tier = np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], p=[0.5, 0.3, 0.15, 0.05])
        device = np.random.choice(['Mobile', 'Desktop', 'Tablet'], p=[0.7, 0.25, 0.05])
        source = np.random.choice(['Organic', 'Social Media', 'Email', 'Paid Ads', 'Friend Referral'])
        
        # Determine internal churn status (approx 25%)
        # Bronze users churn more
        churn_prob = 0.35 if tier == 'Bronze' else (0.25 if tier == 'Silver' else (0.15 if tier == 'Gold' else 0.05))
        is_churned = random.random() < churn_prob
        
        last_active_date = END_DATE
        if is_churned:
            # They stopped being active between signup + 10 days and END_DATE - 30 days
            active_days_max = (END_DATE - signup_date).days - 30
            if active_days_max > 10:
                active_days = random.randint(10, active_days_max)
                last_active_date = signup_date + timedelta(days=active_days)
        
        customers.append({
            'customer_id': f"CUST-{i:06d}",
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'gender': gender,
            'age': age,
            'city': city,
            'country': country,
            'signup_date': signup_date,
            'membership_tier': tier,
            'preferred_device': device,
            'referral_source': source,
            '_is_churned': is_churned,
            '_last_active_date': last_active_date
        })
        
    df = pd.DataFrame(customers)
    df['email'] = df.apply(lambda x: f"{x['first_name'].lower()}.{x['last_name'].lower()}{random.randint(1,99)}@example.com", axis=1)
    
    # Inject intentional missing values
    mask_age = np.random.rand(NUM_CUSTOMERS) < 0.02
    df.loc[mask_age, 'age'] = np.nan
    mask_gender = np.random.rand(NUM_CUSTOMERS) < 0.01
    df.loc[mask_gender, 'gender'] = np.nan
    
    return df

def get_product_catalog():
    categories = {
        'Electronics': [('Smartphone X', 300), ('Laptop Pro', 800), ('Wireless Earbuds', 50), ('Smartwatch', 150)],
        'Clothing': [('T-Shirt Basic', 15), ('Jeans Classic', 40), ('Sneakers', 60), ('Winter Jacket', 80)],
        'Home & Kitchen': [('Coffee Maker', 45), ('Blender', 35), ('Bed Sheets Set', 30), ('Cookware Set', 100)],
        'Beauty': [('Face Cream', 25), ('Shampoo', 10), ('Lipstick', 15), ('Perfume', 50)],
        'Groceries': [('Rice 5kg', 12), ('Cooking Oil 2L', 8), ('Snack Box', 20), ('Coffee Beans', 15)],
        'Books': [('Fiction Novel', 12), ('Business Guide', 18), ('Sci-Fi Paperback', 10), ('Cookbook', 22)],
        'Sports': [('Yoga Mat', 20), ('Dumbbells Set', 45), ('Running Shoes', 70), ('Water Bottle', 15)]
    }
    catalog = []
    pid = 1
    for cat, items in categories.items():
        for name, price in items:
            catalog.append({
                'product_id': f"PROD-{pid:04d}",
                'product_category': cat,
                'product_name': name,
                'base_price': price
            })
            pid += 1
    return pd.DataFrame(catalog)

def generate_transactions(customers_df, catalog_df):
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    
    # We will sample customers based on tier (higher tier buys more)
    tier_weights = {'Bronze': 1, 'Silver': 2, 'Gold': 4, 'Platinum': 8}
    weights = customers_df['membership_tier'].map(tier_weights).values
    weights = weights / weights.sum()
    
    sampled_customers = customers_df.sample(n=NUM_TRANSACTIONS, replace=True, weights=weights)
    
    transactions = []
    products = catalog_df.to_dict('records')
    
    # Seasonality weights (Nov/Dec higher)
    def get_seasonal_date(start, end):
        # simple rejection sampling for seasonality
        while True:
            days = (end - start).days
            if days <= 0: return start
            random_date = start + timedelta(days=random.randint(0, days))
            month = random_date.month
            # boost probability in nov/dec
            prob = 0.8 if month in [11, 12] else 0.4
            if random.random() < prob:
                return random_date

    count = 1
    for _, cust in sampled_customers.iterrows():
        txn_date = get_seasonal_date(cust['signup_date'], cust['_last_active_date'])
        
        prod = random.choice(products)
        qty = int(np.random.choice([1, 2, 3, 4, 5], p=[0.7, 0.15, 0.08, 0.05, 0.02]))
        
        # Discounts
        discount = 0.0
        if random.random() < 0.3:
            discount = round(random.uniform(0.05, 0.25), 2)
            
        unit_price = prod['base_price']
        total = round(qty * unit_price * (1 - discount), 2)
        
        # Payment method depends on country
        if cust['country'] in ['Ghana', 'Kenya', 'Rwanda', 'Tanzania']:
            methods = ['Mobile Money', 'Credit Card', 'Cash on Delivery']
            probs = [0.7, 0.15, 0.15]
        else:
            methods = ['Credit Card', 'Mobile Money', 'Bank Transfer', 'Cash on Delivery']
            probs = [0.6, 0.1, 0.2, 0.1]
            
        payment_method = np.random.choice(methods, p=probs)
        
        # Return rate ~7%
        is_returned = random.random() < 0.07
        
        transactions.append({
            'transaction_id': f"TXN-{count:06d}",
            'customer_id': cust['customer_id'],
            'transaction_date': txn_date.strftime("%Y-%m-%d %H:%M:%S"),
            'product_id': prod['product_id'],
            'product_category': prod['product_category'],
            'product_name': prod['product_name'],
            'quantity': qty,
            'unit_price': unit_price,
            'total_amount': total,
            'payment_method': payment_method,
            'discount_percent': discount,
            'is_returned': is_returned
        })
        count += 1
        
    df = pd.DataFrame(transactions)
    
    # Inject errors
    # 1. Duplicates
    if len(df) > 400:
        dups = df.sample(400)
        df = pd.concat([df, dups])
        
    # 2. Negative quantity
    neg_idx = df.sample(50).index
    df.loc[neg_idx, 'quantity'] = df.loc[neg_idx, 'quantity'] * -1
    
    # 3. Future dates
    future_idx = df.sample(30).index
    future_dates = [(END_DATE + timedelta(days=random.randint(1, 100))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(30)]
    df.loc[future_idx, 'transaction_date'] = future_dates
    
    # 4. Outliers (crazy amounts)
    outlier_idx = df.sample(10).index
    df.loc[outlier_idx, 'total_amount'] = df.loc[outlier_idx, 'total_amount'] * random.choice([10, 50, 100])
    
    return df

def generate_sessions(customers_df):
    print(f"Generating {NUM_SESSIONS} browsing sessions...")
    
    # Similar sampling, higher engagement = more sessions
    sampled_customers = customers_df.sample(n=NUM_SESSIONS, replace=True)
    
    sessions = []
    count = 1
    for _, cust in sampled_customers.iterrows():
        # Session date
        days = (cust['_last_active_date'] - cust['signup_date']).days
        if days <= 0:
            sess_date = cust['signup_date']
        else:
            sess_date = cust['signup_date'] + timedelta(days=random.randint(0, days), hours=random.randint(0,23), minutes=random.randint(0,59))
            
        duration = round(random.uniform(0.5, 60.0), 1)
        
        # If mobile, shorter duration on average
        device = cust['preferred_device']
        if device == 'Mobile' and duration > 30:
            duration = duration * 0.5
            
        pages = int(duration / 2) + random.randint(1, 5) # Rough correlation
        if pages < 1: pages = 1
        
        bounced = duration < 1.0 and pages == 1
        
        sessions.append({
            'session_id': f"SESS-{count:06d}",
            'customer_id': cust['customer_id'],
            'session_date': sess_date.strftime("%Y-%m-%d %H:%M:%S"),
            'duration_minutes': duration,
            'pages_viewed': pages,
            'device_type': device,
            'bounced': bounced
        })
        count += 1
        
    return pd.DataFrame(sessions)

def generate_interactions(customers_df, catalog_df):
    print(f"Generating {NUM_INTERACTIONS} product interactions...")
    
    sampled_customers = customers_df.sample(n=NUM_INTERACTIONS, replace=True)
    products = catalog_df['product_id'].tolist()
    
    interactions = []
    types = ['view', 'add_to_cart', 'add_to_wishlist', 'review']
    # funnel probabilities basically
    probs = [0.70, 0.15, 0.10, 0.05]
    
    for _, cust in sampled_customers.iterrows():
        days = (cust['_last_active_date'] - cust['signup_date']).days
        if days <= 0:
            int_date = cust['signup_date']
        else:
            int_date = cust['signup_date'] + timedelta(days=random.randint(0, days))
            
        itype = np.random.choice(types, p=probs)
        rating = None
        if itype == 'review':
            rating = float(np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.1, 0.2, 0.3, 0.3]))
            
        interactions.append({
            'customer_id': cust['customer_id'],
            'product_id': random.choice(products),
            'interaction_type': itype,
            'interaction_date': int_date.strftime("%Y-%m-%d %H:%M:%S"),
            'rating': rating
        })
        
    return pd.DataFrame(interactions)

if __name__ == "__main__":
    customers = generate_customers()
    catalog = get_product_catalog()
    transactions = generate_transactions(customers, catalog)
    sessions = generate_sessions(customers)
    interactions = generate_interactions(customers, catalog)
    
    # Remove internal columns from customers before saving
    final_customers = customers.drop(columns=['_is_churned', '_last_active_date'])
    
    print("Saving to CSV...")
    final_customers.to_csv(os.path.join(DATA_DIR, 'customers.csv'), index=False)
    transactions.to_csv(os.path.join(DATA_DIR, 'transactions.csv'), index=False)
    sessions.to_csv(os.path.join(DATA_DIR, 'browsing_sessions.csv'), index=False)
    interactions.to_csv(os.path.join(DATA_DIR, 'product_interactions.csv'), index=False)
    
    print("Data generation complete!")
    print(f"Customers: {len(final_customers)}")
    print(f"Transactions: {len(transactions)}")
    print(f"Sessions: {len(sessions)}")
    print(f"Interactions: {len(interactions)}")
