# Automated-KPI-Reporting-Pipeline

## Overview
This project simulates the work of a Business Intelligence Engineer by building an end-to-end analytics pipeline on e-commerce data.

The project:
- loads raw CSV data into a SQLite database
- uses SQL to calculate key business metrics
- generates output files and visualizations
- summarizes findings in a business-oriented report

## Tech Stack
- Python
- SQLite
- Pandas
- Matplotlib
- SQL

## Dataset
Olist Brazilian E-Commerce dataset from Kaggle.

## Key Metrics
- Total orders
- Orders by status
- Orders by month
- Total revenue
- Revenue by month
- Average order value
- Unique customers
- Top customers by spend

## Project Structure
- `src/load_data.py` loads raw CSV files into SQLite
- `src/kpi_report.py` runs KPI queries and generates outputs
- `output/` stores CSV exports, charts, and a summary report

## Example Insights
- Most orders were successfully delivered.
- Revenue increased significantly through 2017 and early 2018.
- Order volume peaked around late 2017 and early 2018.
- Average order value helps benchmark commercial performance.

## How to Run
bash
python3 src/load_data.py
python3 src/kpi_report.py
