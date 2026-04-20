"""
etl_pipeline.py — Standalone ETL script
Run: python etl_pipeline.py
Reads  : Sample - Superstore.csv
Outputs: cleaned_data.csv
"""

import pandas as pd
import numpy as np
import os

RAW_FILE     = "Sample - Superstore.csv"
OUTPUT_FILE  = "cleaned_data.csv"

# ── STEP 1: EXTRACT ──────────────────────────────────────────
print("🔄 [1/4] Extracting data...")
df = pd.read_csv(RAW_FILE, encoding='latin1')
print(f"   Loaded {len(df):,} rows × {len(df.columns)} columns")

# ── STEP 2: CLEAN ────────────────────────────────────────────
print("🔄 [2/4] Cleaning data...")

# Normalise column names
df.columns = [c.strip().replace(' ', '_').replace('-', '_') for c in df.columns]

# Parse dates
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%m/%d/%Y', errors='coerce')
df['Ship_Date']  = pd.to_datetime(df['Ship_Date'],  format='%m/%d/%Y', errors='coerce')

# Numeric coercion
for col in ['Sales', 'Profit', 'Discount', 'Quantity']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop nulls on critical fields
before = len(df)
df.dropna(subset=['Sales', 'Profit', 'Order_Date'], inplace=True)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"   Removed {before - after:,} invalid/duplicate rows → {after:,} clean records")

# ── STEP 3: TRANSFORM ────────────────────────────────────────
print("🔄 [3/4] Transforming data...")

df['Year']          = df['Order_Date'].dt.year
df['Month']         = df['Order_Date'].dt.month
df['Month_Name']    = df['Order_Date'].dt.strftime('%b')
df['Month_Num']     = df['Order_Date'].dt.to_period('M').astype(str)
df['Quarter']       = 'Q' + df['Order_Date'].dt.quarter.astype(str)
df['YearQuarter']   = df['Year'].astype(str) + ' ' + df['Quarter']
df['Days_to_Ship']  = (df['Ship_Date'] - df['Order_Date']).dt.days.clip(lower=0)
df['Profit_Margin'] = (df['Profit'] / df['Sales'].replace(0, np.nan) * 100).round(2)
df['Revenue_Band']  = pd.cut(
    df['Sales'],
    bins=[0, 50, 200, 500, df['Sales'].max() + 1],
    labels=['Low (<$50)', 'Medium ($50-200)', 'High ($200-500)', 'Premium (>$500)'],
    right=False
)

# ── STEP 4: VALIDATE ─────────────────────────────────────────
print("🔄 [4/4] Validating data...")
assert df['Sales'].min() > 0,                   "❌ Sales has non-positive values"
assert df['Days_to_Ship'].min() >= 0,           "❌ Negative ship days found"
assert df.duplicated().sum() == 0,              "❌ Duplicates still present"
assert df['Order_Date'].isnull().sum() == 0,    "❌ Null order dates found"
print("   ✅ All validation checks passed")

# ── OUTPUT ────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n✅ ETL Complete!")
print(f"   Output : {OUTPUT_FILE}")
print(f"   Rows   : {len(df):,}")
print(f"   Columns: {len(df.columns)}")
print(f"   Revenue: ${df['Sales'].sum():,.2f}")
print(f"   Profit : ${df['Profit'].sum():,.2f}")
print(f"   Margin : {df['Profit'].sum()/df['Sales'].sum()*100:.2f}%")
print(f"   Years  : {sorted(df['Year'].unique().tolist())}")
