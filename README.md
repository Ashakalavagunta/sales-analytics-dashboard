# Sales Analytics Dashboard
### Power BI–Style Live Interactive Dashboard | Asha Kalavagunta — Data Analyst

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sales-analytics-dashboard-rtbidn7ctap4xfhj3aqgr6.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=flat&logo=streamlit&logoColor=white)

---

## Live Demo

> ** [Open Live Dashboard](https://sales-analytics-dashboard-rtbidn7ctap4xfhj3aqgr6.streamlit.app/)**

---

## Project Overview

A complete **end-to-end data analytics project** built on the **Kaggle Superstore dataset** (9,994 transaction records across 4 years). This project demonstrates the full data pipeline from raw CSV ingestion to a deployed, interactive Power BI–style dashboard.

### What this project covers:
- **ETL Pipeline** — Extract, Transform, Load with Python & Pandas
- **Data Cleaning** — type coercion, deduplication, null handling, validation
- **Feature Engineering** — 9 derived columns (Year, Quarter, Month, Days to Ship, Profit Margin, Revenue Band, etc.)
- **Data Modeling** — Fact/Dimension structure for analytics
- **Live Dashboard** — 14 interactive charts, 6 sidebar filters, KPI cards
- **Deployed** — publicly accessible via Streamlit Cloud

---

## Key Business Metrics (FY 2014–2017)

| KPI | Value |
|---|---|
| Total Revenue | $2,297,200 |
| Net Profit | $286,397 |
| Profit Margin | 12.47% |
| Total Orders | 5,009 |
| Unique Customers | 793 |
| Top Category | Technology (36.4%) |
| Top Region | West ($725K) |
| Lowest Margin Sub-Cat | Tables (negative on discounts) |

---

## Tech Stack

| Layer | Tools Used |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |
| Dashboard Framework | Streamlit |
| Deployment | Streamlit Cloud |
| Data Source | Kaggle — Sample Superstore CSV |
| Version Control | Git + GitHub |

---

## 📁 Project Structure

    sales-analytics-dashboard/
    │
    ├── app.py                  ← Streamlit dashboard
    ├── etl_pipeline.py         ← Standalone ETL script
    ├── cleaned_data.csv        ← ETL output (9,994 rows × 30 cols)
    ├── requirements.txt        ← Python dependencies
    └── README.md               ← You are here

---

## ETL Pipeline Summary

**Step 1 — Extract**
- Loaded raw CSV (9,994 rows × 21 columns) with latin-1 encoding

**Step 2 — Clean**
- Parsed `Order_Date` and `Ship_Date` as datetime
- Coerced Sales, Profit, Discount, Quantity to numeric
- Removed nulls and duplicates → 0 bad records found

**Step 3 — Transform (Derived Columns)**

| New Column | Logic |
|---|---|
| `Year` | Extracted from Order_Date |
| `Month` / `Month_Name` | Extracted from Order_Date |
| `Quarter` | Q1–Q4 from Order_Date |
| `YearQuarter` | e.g. "2017 Q4" |
| `Days_to_Ship` | Ship_Date − Order_Date (days) |
| `Profit_Margin` | (Profit / Sales) × 100 |
| `Revenue_Band` | Low / Medium / High / Premium |

**Step 4 — Validate**
- Sales minimum > 0 
- No negative ship days 
- Zero duplicates 
- Zero null order dates 

---

## Dashboard Features

### KPI Cards
- Total Revenue, Net Profit, Total Orders, Unique Customers, Avg Discount
- All update dynamically based on sidebar filters

### Charts (14 total — all interactive)
- Monthly Revenue & Profit trend (line chart)
- Revenue by Region (horizontal bar)
- Category distribution (donut chart)
- Revenue by Customer Segment (bar chart)
- Sub-category performance (ranked bars)
- Profit Margin by Sub-Category (red = negative margin)
- Ship Mode distribution (donut)
- Discount vs Profit impact (scatter bubble)
- Revenue & Profit by Year (grouped bar)
- Top 10 Products table
- US State Choropleth map
- Avg Days to Ship by mode (bar)
- Month × Year Revenue Heatmap

### Sidebar Filters
- Year (multi-select)
- Quarter (Q1–Q4)
- Region (4 US regions)
- Customer Segment
- Category
- Ship Mode
- Date range picker

### Bonus Features
- Download filtered data as CSV
- Anomaly highlights (loss orders, top customers, best-margin products)
- Auto-refresh button

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Ashakalavagunta/sales-analytics-dashboard.git
cd sales-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run ETL (generates cleaned_data.csv)
python etl_pipeline.py

# 4. Launch dashboard
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## Requirements
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0

---

## Dataset

**Source:** [Kaggle — Sample Superstore](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

| Field | Details |
|---|---|
| Records | 9,994 rows |
| Columns (raw) | 21 |
| Columns (cleaned) | 30 |
| Date Range | January 2014 – December 2017 |
| Geography | United States (4 regions, 49 states) |
| Categories | Furniture, Office Supplies, Technology |
| Segments | Consumer, Corporate, Home Office |

---

## About the Author

**Asha Kalavagunta** — Data Analyst

Skilled in Python · SQL · Power BI · Tableau · Excel · Machine Learning · Streamlit

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/asha-kalavagunta-80031b223/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github&logoColor=white)](https://github.com/Ashakalavagunta)

---

* If you found this project useful, please consider giving it a star!*
