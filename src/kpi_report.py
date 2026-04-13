import sqlite3
from pathlib import Path
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# Ensure output folder exists
Path("output").mkdir(exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect("data/business.db")

queries = {
    "total_orders": """
        SELECT COUNT(*) AS total_orders
        FROM orders;
    """,

    "orders_by_status": """
        SELECT order_status, COUNT(*) AS total_orders
        FROM orders
        GROUP BY order_status
        ORDER BY total_orders DESC;
    """,

    "orders_by_month": """
        SELECT
            substr(order_purchase_timestamp, 1, 7) AS month,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY month
        ORDER BY month;
    """,

    "delivered_orders": """
        SELECT COUNT(*) AS delivered_orders
        FROM orders
        WHERE order_status = 'delivered';
    """,

    "cancelled_orders": """
        SELECT COUNT(*) AS cancelled_orders
        FROM orders
        WHERE order_status = 'canceled';
    """,

    "total_revenue": """
        SELECT ROUND(SUM(price), 2) AS total_revenue
        FROM order_items;
    """,

    "revenue_by_month": """
        SELECT
            substr(o.order_purchase_timestamp, 1, 7) AS month,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY month
        ORDER BY month;
    """,

    "average_order_value": """
        SELECT
            ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id;
    """,

    "unique_customers": """
        SELECT COUNT(DISTINCT customer_id) AS unique_customers
        FROM customers;
    """,

    "orders_per_customer": """
        SELECT
            ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT customer_id), 2) AS orders_per_customer
        FROM orders;
    """,

    "repeat_customers": """
        SELECT COUNT(*) AS repeat_customers
        FROM (
            SELECT customer_id
            FROM orders
            GROUP BY customer_id
            HAVING COUNT(order_id) > 1
        );
    """,

    "top_customers": """
        SELECT
            o.customer_id,
            ROUND(SUM(oi.price), 2) AS total_spent
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY o.customer_id
        ORDER BY total_spent DESC
        LIMIT 10;
    """,

    "revenue_by_status": """
        SELECT
            o.order_status,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY o.order_status
        ORDER BY revenue DESC;
    """
}

results = {}

# Run queries and save CSVs
for name, query in queries.items():
    df = pd.read_sql_query(query, conn)
    results[name] = df
    df.to_csv(f"output/{name}.csv", index=False)
    print(f"Saved: output/{name}.csv")

conn.close()

# Revenue by month chart
revenue_month_df = results["revenue_by_month"]
plt.figure(figsize=(12, 6))
plt.plot(revenue_month_df["month"], revenue_month_df["revenue"])
plt.xticks(rotation=45)
plt.title("Revenue by Month")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("output/revenue_by_month.png")
plt.close()

# Orders by status chart
orders_status_df = results["orders_by_status"]
plt.figure(figsize=(10, 6))
plt.bar(orders_status_df["order_status"], orders_status_df["total_orders"])
plt.xticks(rotation=45)
plt.title("Orders by Status")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("output/orders_by_status.png")
plt.close()

# Revenue by status chart
revenue_status_df = results["revenue_by_status"]
plt.figure(figsize=(10, 6))
plt.bar(revenue_status_df["order_status"], revenue_status_df["revenue"])
plt.xticks(rotation=45)
plt.title("Revenue by Order Status")
plt.xlabel("Order Status")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("output/revenue_by_status.png")
plt.close()

# Top customers chart
top_customers_df = results["top_customers"]
plt.figure(figsize=(12, 6))
plt.bar(top_customers_df["customer_id"], top_customers_df["total_spent"])
plt.xticks(rotation=90)
plt.title("Top 10 Customers by Spend")
plt.xlabel("Customer ID")
plt.ylabel("Total Spent")
plt.tight_layout()
plt.savefig("output/top_customers.png")
plt.close()

# Summary values
total_orders = int(results["total_orders"]["total_orders"].iloc[0])
delivered_orders = int(results["delivered_orders"]["delivered_orders"].iloc[0])
cancelled_orders = int(results["cancelled_orders"]["cancelled_orders"].iloc[0])
total_revenue = float(results["total_revenue"]["total_revenue"].iloc[0])
avg_order_value = float(results["average_order_value"]["avg_order_value"].iloc[0])
unique_customers = int(results["unique_customers"]["unique_customers"].iloc[0])
orders_per_customer = float(results["orders_per_customer"]["orders_per_customer"].iloc[0])
repeat_customers = int(results["repeat_customers"]["repeat_customers"].iloc[0])

repeat_customer_rate = round((repeat_customers / unique_customers) * 100, 2) if unique_customers else 0
delivery_rate = round((delivered_orders / total_orders) * 100, 2) if total_orders else 0
cancellation_rate = round((cancelled_orders / total_orders) * 100, 2) if total_orders else 0

summary = f"""
Business Intelligence Summary
=============================

Core KPIs
---------
Total Orders: {total_orders}
Delivered Orders: {delivered_orders}
Cancelled Orders: {cancelled_orders}
Total Revenue: {total_revenue}
Average Order Value: {avg_order_value}
Unique Customers: {unique_customers}

Customer Metrics
----------------
Orders per Customer: {orders_per_customer}
Repeat Customers: {repeat_customers}
Repeat Customer Rate: {repeat_customer_rate}%

Operational Metrics
-------------------
Delivery Rate: {delivery_rate}%
Cancellation Rate: {cancellation_rate}%

Key Insights
------------
1. The business processed a large order volume, with a very high delivery rate.
2. Revenue rose strongly through 2017 and into 2018, suggesting marketplace growth over time.
3. Cancellation rate is relatively low, indicating stable order fulfillment performance.
4. Orders per customer and repeat customer rate suggest many customers may be one-time purchasers.
5. Revenue concentration among top customers can be used to study customer value distribution.
"""

with open("output/summary.txt", "w", encoding="utf-8") as f:
    f.write(summary.strip())

print("Saved: output/revenue_by_month.png")
print("Saved: output/orders_by_status.png")
print("Saved: output/revenue_by_status.png")
print("Saved: output/top_customers.png")
print("Saved: output/summary.txt")

# Auto-generate HTML report
subprocess.run(["python3", "src/generate_html_report.py"], check=True)

print("Project report generation complete.")
