import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from supabase import create_client, Client

print("🚀 Mock Data Generate Ho Raha Hai...")
np.random.seed(42)
n_records = 10500

# Generating Data Fields
order_ids = [f"CA-2025-{100000 + i}" for i in range(n_records)]
order_dates = [datetime(2024, 1, 1) + timedelta(days=int(np.random.randint(0, 800))) for i in range(n_records)]
customer_ids = [f"CS-{np.random.randint(1001, 1500)}" for i in range(n_records)]
segments = np.random.choice(['Consumer', 'Corporate', 'Home Office'], size=n_records, p=[0.5, 0.3, 0.2])
regions = np.random.choice(['North', 'South', 'East', 'West'], size=n_records)

states_map = {
    'North': ['Delhi', 'Punjab', 'Haryana', 'UP'],
    'South': ['Karnataka', 'Tamil Nadu', 'Telangana', 'Kerala'],
    'East': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand'],
    'West': ['Maharashtra', 'Gujarat', 'Rajasthan', 'Goa']
}
states = [np.random.choice(states_map[r]) for r in regions]
categories = np.random.choice(['Furniture', 'Office Supplies', 'Technology'], size=n_records, p=[0.3, 0.4, 0.3])

sub_cats_map = {
    'Furniture': ['Chairs', 'Tables', 'Furnishings'],
    'Office Supplies': ['Paper', 'Binders', 'Art', 'Fasteners'],
    'Technology': ['Phones', 'Accessories', 'Copiers']
}
sub_cats = [np.random.choice(sub_cats_map[c]) for c in categories]

quantities = np.random.randint(1, 10, size=n_records)
base_prices = np.random.uniform(10, 500, size=n_records)
sales = base_prices * quantities
discounts = np.random.choice([0.0, 0.1, 0.2, 0.5], size=n_records, p=[0.6, 0.2, 0.1, 0.1])
sales = sales * (1 - discounts)

profits = []
for i in range(n_records):
    if sub_cats[i] == 'Tables' and regions[i] == 'South':
        p = -float(sales[i] * np.random.uniform(0.1, 0.4))
    else:
        p = float(sales[i] * np.random.uniform(0.05, 0.25))
    profits.append(p)

df = pd.DataFrame({
    'order_id': order_ids, 'order_date': order_dates, 'customer_id': customer_ids,
    'segment': segments, 'region': regions, 'state': states,
    'category': categories, 'sub_category': sub_cats,
    'sales': np.round(sales, 2), 'quantity': quantities, 'discount': discounts, 'profit': np.round(profits, 2)
})

# Missing value introduce karna profile optimization tracking ke liye
df.loc[df.sample(frac=0.01).index, 'discount'] = np.nan

print("🧹 Data Preprocessing Aur Cleaning Shuru...")
df.dropna(subset=['order_id', 'sales'], inplace=True)

# Fixed Copy-on-Write assignment warnings
df['discount'] = df['discount'].fillna(0.0)
df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

# Feature Engineering Vector Analytics
df['profit_margin'] = np.round((df['profit'] / df['sales']) * 100, 2)
df['calculated_cost_basis'] = np.round(df['sales'] - df['profit'], 2)

# --- CRITICAL INTEGRATION FIX: Replace non-JSON compliant NaN values ---
df['profit_margin'] = df['profit_margin'].replace([np.inf, -np.inf], np.nan).fillna(0.0)
df['calculated_cost_basis'] = df['calculated_cost_basis'].fillna(0.0)
# ------------------------------------------------------------------------

# Local Checkpoint Backup
df.to_csv('cleaned_sales_data.csv', index=False)
print("✨ Cleaned data local save ho gaya: cleaned_sales_data.csv")

# 🔗 LIVE INSTANTIATED SUPABASE API CONFIGURATION
SUPABASE_URL = "https://rlcxkqirdjgwpsnxobrx.supabase.co"
SUPABASE_KEY = "sb_publishable_7dA8YRoBh9HxjvjrLvSPHA_uOnSJkOy"

try:
    print("🔌 Supabase Secure REST Tunnel Se Connection Set Ho Raha Hai...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Batch formatting structure serialization
    records = df.to_dict(orient='records')
    
    print("📤 Transmitting Data Records to 'corporate_sales_records' Table...")
    # Cloud matrix server synchronization execution line
    supabase.table('corporate_sales_records').upsert(records).execute()
    print("⚡ Success! Saara Analytical Data API Key Ke Through Supabase Me Live Chala Gaya.")
except Exception as e:
    print(f"❌ Handshake Validation Failure: {e}")