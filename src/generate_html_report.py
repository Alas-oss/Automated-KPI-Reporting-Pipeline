from pathlib import Path
import pandas as pd

Path("output").mkdir(exist_ok=True)

# Load outputs
total_orders = pd.read_csv("output/total_orders.csv")
delivered_orders = pd.read_csv("output/delivered_orders.csv")
cancelled_orders = pd.read_csv("output/cancelled_orders.csv")
total_revenue = pd.read_csv("output/total_revenue.csv")
average_order_value = pd.read_csv("output/average_order_value.csv")
unique_customers = pd.read_csv("output/unique_customers.csv")
orders_per_customer = pd.read_csv("output/orders_per_customer.csv")
repeat_customers = pd.read_csv("output/repeat_customers.csv")
top_customers = pd.read_csv("output/top_customers.csv")
orders_by_status = pd.read_csv("output/orders_by_status.csv")
revenue_by_status = pd.read_csv("output/revenue_by_status.csv")

with open("output/summary.txt", "r", encoding="utf-8") as f:
    summary_text = f.read()

# Scalar KPI values
total_orders_value = int(total_orders["total_orders"].iloc[0])
delivered_orders_value = int(delivered_orders["delivered_orders"].iloc[0])
cancelled_orders_value = int(cancelled_orders["cancelled_orders"].iloc[0])
total_revenue_value = float(total_revenue["total_revenue"].iloc[0])
avg_order_value_value = float(average_order_value["avg_order_value"].iloc[0])
unique_customers_value = int(unique_customers["unique_customers"].iloc[0])
orders_per_customer_value = float(orders_per_customer["orders_per_customer"].iloc[0])
repeat_customers_value = int(repeat_customers["repeat_customers"].iloc[0])

repeat_customer_rate = round((repeat_customers_value / unique_customers_value) * 100, 2) if unique_customers_value else 0
delivery_rate = round((delivered_orders_value / total_orders_value) * 100, 2) if total_orders_value else 0
cancellation_rate = round((cancelled_orders_value / total_orders_value) * 100, 2) if total_orders_value else 0

# Convert tables to HTML
top_customers_html = top_customers.to_html(index=False, classes="table")
orders_by_status_html = orders_by_status.to_html(index=False, classes="table")
revenue_by_status_html = revenue_by_status.to_html(index=False, classes="table")

insight_cards = f"""
<div class="insight-grid">
    <div class="insight-card">
        <h3>Delivery Performance</h3>
        <p>{delivery_rate}% of all orders were delivered successfully, indicating strong fulfillment outcomes.</p>
    </div>
    <div class="insight-card">
        <h3>Customer Retention</h3>
        <p>{repeat_customer_rate}% of customers placed more than one order, suggesting retention is an area worth improving.</p>
    </div>
    <div class="insight-card">
        <h3>Commercial Efficiency</h3>
        <p>Average order value was ${avg_order_value_value:,.2f}, which gives a useful benchmark for basket-size monitoring.</p>
    </div>
</div>
"""

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-commerce Business Intelligence Report</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f6fb;
            color: #1f2937;
        }}

        .container {{
            width: 92%;
            max-width: 1280px;
            margin: 32px auto;
        }}

        .hero {{
            background: linear-gradient(135deg, #1f3c88, #2563eb);
            color: white;
            padding: 36px;
            border-radius: 18px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}

        .hero h1 {{
            margin: 0 0 10px 0;
            font-size: 34px;
        }}

        .hero p {{
            margin: 0;
            font-size: 16px;
            opacity: 0.95;
        }}

        .section {{
            background: white;
            padding: 28px;
            border-radius: 18px;
            margin-bottom: 24px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        }}

        .section h2 {{
            margin-top: 0;
            margin-bottom: 18px;
            font-size: 24px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
        }}

        .kpi-card {{
            background: linear-gradient(180deg, #ffffff, #f8fafc);
            border: 1px solid #e5e7eb;
            padding: 20px;
            border-radius: 16px;
        }}

        .kpi-label {{
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .kpi-value {{
            font-size: 30px;
            font-weight: bold;
            color: #111827;
        }}

        .insight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 18px;
        }}

        .insight-card {{
            background: #f8fbff;
            border: 1px solid #dbeafe;
            border-left: 6px solid #2563eb;
            padding: 18px;
            border-radius: 14px;
        }}

        .insight-card h3 {{
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 18px;
        }}

        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
        }}

        .chart-card img {{
            width: 100%;
            border-radius: 12px;
            margin-top: 10px;
        }}

        .table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 14px;
            font-size: 14px;
        }}

        .table th,
        .table td {{
            border: 1px solid #e5e7eb;
            padding: 10px 12px;
            text-align: left;
        }}

        .table th {{
            background: #f9fafb;
        }}

        .summary-box {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 18px;
            line-height: 1.7;
            white-space: pre-wrap;
        }}

        .footer {{
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin: 28px 0 10px;
        }}
    </style>
</head>
<body>
    <div class="container">

        <div class="hero">
            <h1>E-commerce Business Intelligence Report</h1>
            <p>
                End-to-end student BI project using Python, SQL, SQLite, Pandas, and Matplotlib to analyze e-commerce performance, customer behavior, and revenue trends.
            </p>
        </div>

        <div class="section">
            <h2>Executive KPI Overview</h2>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Total Orders</div>
                    <div class="kpi-value">{total_orders_value:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Delivered Orders</div>
                    <div class="kpi-value">{delivered_orders_value:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Cancelled Orders</div>
                    <div class="kpi-value">{cancelled_orders_value:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Revenue</div>
                    <div class="kpi-value">${total_revenue_value:,.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Average Order Value</div>
                    <div class="kpi-value">${avg_order_value_value:,.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Unique Customers</div>
                    <div class="kpi-value">{unique_customers_value:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Orders per Customer</div>
                    <div class="kpi-value">{orders_per_customer_value:.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Repeat Customer Rate</div>
                    <div class="kpi-value">{repeat_customer_rate}%</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Key Business Insights</h2>
            {insight_cards}
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            <div class="summary-box">{summary_text}</div>
        </div>

        <div class="section">
            <h2>Trend Analysis</h2>
            <div class="chart-grid">
                <div class="chart-card">
                    <h3>Revenue by Month</h3>
                    <img src="revenue_by_month.png" alt="Revenue by Month">
                </div>
                <div class="chart-card">
                    <h3>Orders by Status</h3>
                    <img src="orders_by_status.png" alt="Orders by Status">
                </div>
                <div class="chart-card">
                    <h3>Revenue by Order Status</h3>
                    <img src="revenue_by_status.png" alt="Revenue by Status">
                </div>
                <div class="chart-card">
                    <h3>Top 10 Customers by Spend</h3>
                    <img src="top_customers.png" alt="Top Customers by Spend">
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Top Customers by Spend</h2>
            {top_customers_html}
        </div>

        <div class="section">
            <h2>Orders by Status Table</h2>
            {orders_by_status_html}
        </div>

        <div class="section">
            <h2>Revenue by Status Table</h2>
            {revenue_by_status_html}
        </div>

        <div class="footer">
            Generated automatically from the project pipeline as part of a student business intelligence portfolio project.
        </div>
    </div>
</body>
</html>
"""

with open("output/report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved: output/report.html")
