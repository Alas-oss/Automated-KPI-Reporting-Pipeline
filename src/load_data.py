import sqlite3
from pathlib import Path
import pandas as pd

# Ensure data folder exists
Path("data").mkdir(exist_ok=True)

# Connect to database
conn = sqlite3.connect("data/business.db")

# Load CSV (start with ONE table first)
df = pd.read_csv("data/olist_orders_dataset.csv")

# Save to SQLite
df.to_sql("orders", conn, if_exists="replace", index=False)

print("Loaded data into SQLite")
print(df.head())

# Load order items (contains price data)
order_items = pd.read_csv("data/olist_order_items_dataset.csv")

order_items.to_sql("order_items", conn, if_exists="replace", index=False)

print("Loaded order_items table")
print(order_items.head())

# Load customers table
customers = pd.read_csv("data/olist_customers_dataset.csv")

customers.to_sql("customers", conn, if_exists="replace", index=False)

print("Loaded customers table")
print(customers.head())

conn.close()
