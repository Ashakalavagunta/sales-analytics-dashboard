"""
╔══════════════════════════════════════════════════════════════════╗
║   Sales Analytics Dashboard — Power BI Style                    ║
║   Author : Asha Kalavagunta  |  Built with Streamlit + Plotly   ║
║   Dataset: Kaggle Superstore (Sample - Superstore.csv)           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard | Asha Kalavagunta",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] { background:#0b0e1a; }
[data-testid="stSidebar"] { background:#111625 !important; border-right:1px solid #252d42; }
[data-testid="stSidebar"] * { color:#dde3f0 !important; }
.main .block-container { padding:1.2rem 1.8rem 2rem; }
h1,h2,h3,h4 { color:#fff !important; }

/* ── KPI Cards ── */
.kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:1.2rem; }
.kpi-card {
    background:#111625; border-radius:12px; padding:16px 18px;
    border:1px solid #252d42; position:relative; overflow:hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0;
}
.kpi-revenue::before  { background:linear-gradient(90deg,#f2c94c,#f2994a); }
.kpi-profit::before   { background:linear-gradient(90deg,#6fcf97,#27ae60); }
.kpi-orders::before   { background:linear-gradient(90deg,#56ccf2,#2f80ed); }
.kpi-customers::before{ background:linear-gradient(90deg,#bb6bd9,#9b51e0); }
.kpi-margin::before   { background:linear-gradient(90deg,#f2994a,#eb5757); }

.kpi-label { font-size:10px; font-weight:600; color:#6b7a99; text-transform:uppercase; letter-spacing:.7px; margin-bottom:8px; font-family:'Segoe UI',sans-serif; }
.kpi-value { font-size:26px; font-weight:800; color:#fff; line-height:1; letter-spacing:-.5px; font-family:'Segoe UI',sans-serif; }
.kpi-badge { display:inline-block; margin-top:8px; font-size:11px; padding:3px 9px; border-radius:20px; font-weight:600; font-family:'Segoe UI',sans-serif; }
.badge-up { background:rgba(111,207,151,.15); color:#6fcf97; }
.badge-dn { background:rgba(235,87,87,.15); color:#eb5757; }

/* ── Section Headers ── */
.section-header {
    font-size:11px; font-weight:700; color:#6b7a99; text-transform:uppercase;
    letter-spacing:.8px; margin-bottom:10px; padding-bottom:6px;
    border-bottom:1px solid #1f2840;
}

/* ── Insight cards ── */
.insight-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:1.2rem; }
.insight-card {
    background:#111625; border-radius:12px; padding:14px 16px;
    border:1px solid #252d42; display:flex; align-items:flex-start; gap:12px;
}
.insight-icon { font-size:22px; flex-shrink:0; }
.insight-title { font-size:12px; font-weight:700; color:#dde3f0; margin-bottom:4px; font-family:'Segoe UI',sans-serif; }
.insight-text { font-size:11px; color:#6b7a99; line-height:1.55; font-family:'Segoe UI',sans-serif; }
.insight-hl { color:#f2c94c; font-weight:600; }

/* ── Author banner ── */
.author-bar {
    background:linear-gradient(135deg,#13172a,#1a1f35);
    border-radius:12px; padding:14px 20px; margin-bottom:1.2rem;
    border:1px solid rgba(242,201,76,.2);
    display:flex; align-items:center; justify-content:space-between;
}
.author-name { font-size:16px; font-weight:800; color:#fff; font-family:'Segoe UI',sans-serif; }
.author-role { font-size:11px; color:#f2c94c; font-weight:500; font-family:'Segoe UI',sans-serif; }
.live-badge {
    background:rgba(111,207,151,.12); border:1px solid rgba(111,207,151,.3);
    border-radius:20px; padding:5px 14px; font-size:11px; font-weight:700;
    color:#6fcf97; font-family:'Segoe UI',sans-serif;
}

/* ── Plotly containers ── */
.chart-card {
    background:#111625; border-radius:12px; padding:16px;
    border:1px solid #252d42; margin-bottom:12px;
}
/* ── Sidebar ── */
.sidebar-title { font-size:13px; font-weight:700; color:#f2c94c !important; margin-bottom:4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ETL — LOAD & CLEAN
# ─────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#8892a4', family='Segoe UI, sans-serif', size=11),
    margin=dict(l=8, r=8, t=36, b=8),
)

@st.cache_data(ttl=300)
def load_data():
    """ETL pipeline — extract, clean, transform."""
    # ── 1. EXTRACT ──
    candidates = [
        "cleaned_data.csv",
        "Sample - Superstore.csv",
        "sales_dashboard_data.csv",
    ]
    df = None
    for path in candidates:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding='latin1')
                break
            except Exception:
                continue
    if df is None:
        st.error("❌ No data file found. Place cleaned_data.csv or Sample - Superstore.csv in the app directory.")
        st.stop()

    # ── 2. CLEAN ──
    df.columns = [c.strip().replace(' ', '_').replace('-', '_') for c in df.columns]

    # Standardise key column names
    rename_map = {
        'Sub_Category': 'Sub_Category',
        'Sub-Category': 'Sub_Category',
        'Product_Name': 'Product_Name',
        'Product Name': 'Product_Name',
        'Customer_Name': 'Customer_Name',
        'Customer Name': 'Customer_Name',
        'Ship_Mode': 'Ship_Mode',
        'Ship Mode': 'Ship_Mode',
        'Order_ID': 'Order_ID',
        'Order ID': 'Order_ID',
        'Order_Date': 'Order_Date',
        'Order Date': 'Order_Date',
        'Ship_Date': 'Ship_Date',
        'Ship Date': 'Ship_Date',
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    # Date parsing (infer_datetime_format removed in pandas 2.x)
    for col in ['Order_Date', 'Ship_Date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Numeric coercion
    for col in ['Sales', 'Profit', 'Discount', 'Quantity']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=['Sales', 'Profit'], inplace=True)
    df.drop_duplicates(inplace=True)

    # ── 3. TRANSFORM — derived columns ──
    if 'Order_Date' in df.columns:
        df['Year']       = df['Order_Date'].dt.year.astype('Int64')
        df['Month']      = df['Order_Date'].dt.month
        df['Month_Name'] = df['Order_Date'].dt.strftime('%b')
        df['Month_Num']  = df['Order_Date'].dt.to_period('M').astype(str)
        df['Quarter']    = 'Q' + df['Order_Date'].dt.quarter.astype(str)
        df['YearQuarter']= df['Year'].astype(str) + ' ' + df['Quarter']

    if 'Order_Date' in df.columns and 'Ship_Date' in df.columns:
        df['Days_to_Ship'] = (df['Ship_Date'] - df['Order_Date']).dt.days.clip(lower=0)

    df['Profit_Margin'] = (df['Profit'] / df['Sales'].replace(0, np.nan) * 100).round(2)
    df['Revenue_Band']  = pd.cut(
        df['Sales'],
        bins=[0, 50, 200, 500, df['Sales'].max() + 1],
        labels=['Low (<$50)', 'Medium ($50-200)', 'High ($200-500)', 'Premium (>$500)'],
        right=False
    )

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Dashboard Filters</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Year
    years = sorted(df['Year'].dropna().unique().tolist())
    sel_years = st.multiselect("📅 Year", years, default=years)

    # Quarter
    quarters = sorted(df['Quarter'].dropna().unique().tolist())
    sel_quarters = st.multiselect("🗓 Quarter", quarters, default=quarters)

    # Region
    regions = sorted(df['Region'].dropna().unique().tolist())
    sel_regions = st.multiselect("🗺 Region", regions, default=regions)

    # Segment
    segments = sorted(df['Segment'].dropna().unique().tolist())
    sel_segments = st.multiselect("👥 Segment", segments, default=segments)

    # Category
    categories = sorted(df['Category'].dropna().unique().tolist())
    sel_categories = st.multiselect("📦 Category", categories, default=categories)

    # Ship Mode
    ship_modes = sorted(df['Ship_Mode'].dropna().unique().tolist())
    sel_ship = st.multiselect("🚚 Ship Mode", ship_modes, default=ship_modes)

    st.markdown("---")

    # Date range
    if 'Order_Date' in df.columns:
        min_date = df['Order_Date'].min().date()
        max_date = df['Order_Date'].max().date()
        date_range = st.date_input("📆 Order Date Range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)

    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;color:#4a5568;'>Dataset: {len(df):,} rows · {len(df.columns)} cols</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
mask = (
    df['Year'].isin(sel_years) &
    df['Quarter'].isin(sel_quarters) &
    df['Region'].isin(sel_regions) &
    df['Segment'].isin(sel_segments) &
    df['Category'].isin(sel_categories) &
    df['Ship_Mode'].isin(sel_ship)
)
if 'Order_Date' in df.columns and len(date_range) == 2:
    mask &= (df['Order_Date'].dt.date >= date_range[0]) & (df['Order_Date'].dt.date <= date_range[1])

fdf = df[mask].copy()

# ─────────────────────────────────────────────
# AUTHOR BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="author-bar">
  <div>
    <div class="author-name">📊 Sales Analytics Dashboard</div>
    <div class="author-role">Asha Kalavagunta &nbsp;·&nbsp; Data Analyst &nbsp;·&nbsp; BI Developer &nbsp;·&nbsp; Kaggle Superstore Dataset</div>
  </div>
  <div class="live-badge">⚡ LIVE · {len(fdf):,} records filtered</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
total_rev   = fdf['Sales'].sum()
total_prf   = fdf['Profit'].sum()
total_ord   = fdf['Order_ID'].nunique()
total_cust  = fdf['Customer_ID'].nunique() if 'Customer_ID' in fdf.columns else fdf['Customer_Name'].nunique()
avg_margin  = (total_prf / total_rev * 100) if total_rev > 0 else 0
avg_discount= fdf['Discount'].mean() * 100

def fmt(v):
    if abs(v) >= 1_000_000: return f"${v/1e6:.2f}M"
    if abs(v) >= 1_000:     return f"${v/1e3:.1f}K"
    return f"${v:.0f}"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-revenue">
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">{fmt(total_rev)}</div>
    <span class="kpi-badge badge-up">📈 FY All Years</span>
  </div>
  <div class="kpi-card kpi-profit">
    <div class="kpi-label">Net Profit</div>
    <div class="kpi-value">{fmt(total_prf)}</div>
    <span class="kpi-badge {'badge-up' if total_prf>0 else 'badge-dn'}">{avg_margin:.1f}% Margin</span>
  </div>
  <div class="kpi-card kpi-orders">
    <div class="kpi-label">Total Orders</div>
    <div class="kpi-value">{total_ord:,}</div>
    <span class="kpi-badge badge-up">Unique Orders</span>
  </div>
  <div class="kpi-card kpi-customers">
    <div class="kpi-label">Unique Customers</div>
    <div class="kpi-value">{total_cust:,}</div>
    <span class="kpi-badge badge-up">3 Segments</span>
  </div>
  <div class="kpi-card kpi-margin">
    <div class="kpi-label">Avg Discount</div>
    <div class="kpi-value">{avg_discount:.1f}%</div>
    <span class="kpi-badge badge-dn">Margin Impact</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
COLORS = ['#f2c94c','#56ccf2','#bb6bd9','#6fcf97','#f2994a','#eb5757','#2f80ed','#27ae60']
CAT_COLORS = {'Furniture':'#56ccf2','Office Supplies':'#bb6bd9','Technology':'#f2c94c'}
SEG_COLORS = {'Consumer':'#f2c94c','Corporate':'#56ccf2','Home Office':'#bb6bd9'}

# ─────────────────────────────────────────────
# INSIGHTS
# ─────────────────────────────────────────────
top_cat    = fdf.groupby('Category')['Sales'].sum().idxmax() if len(fdf) else '–'
top_region = fdf.groupby('Region')['Sales'].sum().idxmax()   if len(fdf) else '–'
top_sub    = fdf.groupby('Sub_Category')['Sales'].sum().idxmax() if len(fdf) else '–'
worst_margin_sub = fdf.groupby('Sub_Category')['Profit_Margin'].mean().idxmin() if len(fdf) else '–'
worst_val = fdf.groupby('Sub_Category')['Profit_Margin'].mean().min() if len(fdf) else 0

st.markdown(f"""
<div class="insight-row">
  <div class="insight-card">
    <div class="insight-icon">🏆</div>
    <div>
      <div class="insight-title">Top Category: {top_cat}</div>
      <div class="insight-text"><span class="insight-hl">{top_cat}</span> leads revenue across the selected period. Technology consistently drives the highest sales volume across all regions.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon">🗺️</div>
    <div>
      <div class="insight-title">Top Region: {top_region}</div>
      <div class="insight-text">The <span class="insight-hl">{top_region} region</span> generates the highest revenue. Sub-category <span class="insight-hl">{top_sub}</span> is the top-performing product group.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon">⚠️</div>
    <div>
      <div class="insight-title">Margin Risk: {worst_margin_sub}</div>
      <div class="insight-text"><span class="insight-hl">{worst_margin_sub}</span> has the lowest avg margin at <span class="insight-hl">{worst_val:.1f}%</span>. High-discount orders are compressing profitability — review discount policy.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1 — TIME SERIES  +  REVENUE BY REGION
# ─────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-header">📈 Monthly Revenue & Profit Trend</div>', unsafe_allow_html=True)
    if 'Month_Num' in fdf.columns:
        ts = fdf.groupby('Month_Num').agg(Revenue=('Sales','sum'), Profit=('Profit','sum')).reset_index()
        ts = ts.sort_values('Month_Num')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ts['Month_Num'], y=ts['Revenue'], name='Revenue',
            line=dict(color='#f2c94c', width=2.5), fill='tozeroy',
            fillcolor='rgba(242,201,76,0.06)', mode='lines+markers',
            marker=dict(size=4, color='#f2c94c')))
        fig.add_trace(go.Scatter(x=ts['Month_Num'], y=ts['Profit'], name='Profit',
            line=dict(color='#6fcf97', width=2.5), fill='tozeroy',
            fillcolor='rgba(111,207,151,0.06)', mode='lines+markers',
            marker=dict(size=4, color='#6fcf97')))
        fig.update_layout(**PLOTLY_THEME, height=280,
            legend=dict(orientation='h', y=1.1, x=0, font=dict(size=11, color='#8892a4')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickfont=dict(size=10)),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$', tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<div class="section-header">🗺 Revenue by Region</div>', unsafe_allow_html=True)
    reg = fdf.groupby('Region')['Sales'].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(reg, x='Sales', y='Region', orientation='h',
                 color='Region', color_discrete_sequence=COLORS,
                 labels={'Sales':'Revenue ($)', 'Region':''})
    fig.update_layout(**PLOTLY_THEME, height=280, showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# ROW 2 — CATEGORY DONUT + SEGMENT BAR + SUB-CAT
# ─────────────────────────────────────────────
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown('<div class="section-header">📦 Category Distribution</div>', unsafe_allow_html=True)
    cat = fdf.groupby('Category')['Sales'].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=cat['Category'], values=cat['Sales'],
        hole=0.65, marker=dict(colors=['#f2c94c','#56ccf2','#bb6bd9']),
        textinfo='percent+label', textfont=dict(size=11, color='#dde3f0'),
    ))
    fig.update_layout(**PLOTLY_THEME, height=260,
        legend=dict(orientation='h', y=-0.15, font=dict(size=10, color='#8892a4')))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col4:
    st.markdown('<div class="section-header">👥 Revenue by Segment</div>', unsafe_allow_html=True)
    seg = fdf.groupby('Segment')['Sales'].sum().reset_index()
    fig = px.bar(seg, x='Segment', y='Sales', color='Segment',
                 color_discrete_map=SEG_COLORS,
                 labels={'Sales':'Revenue ($)', 'Segment':''})
    fig.update_layout(**PLOTLY_THEME, height=260, showlegend=False,
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$'))
    fig.update_traces(marker_line_width=0, marker_cornerradius=6)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col5:
    st.markdown('<div class="section-header">📊 Top Sub-Categories by Revenue</div>', unsafe_allow_html=True)
    sub = fdf.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=False).head(8).reset_index()
    fig = px.bar(sub, x='Sales', y='Sub_Category', orientation='h',
                 color='Sales', color_continuous_scale=['#1c2235','#f2c94c'],
                 labels={'Sales':'Revenue ($)', 'Sub_Category':''})
    fig.update_layout(**PLOTLY_THEME, height=260, showlegend=False, coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# ROW 3 — PROFIT MARGIN BY CATEGORY + SHIP MODE + DISCOUNT vs PROFIT
# ─────────────────────────────────────────────
col6, col7, col8 = st.columns(3)

with col6:
    st.markdown('<div class="section-header">💰 Profit Margin by Sub-Category</div>', unsafe_allow_html=True)
    pm = fdf.groupby('Sub_Category').agg(
        Margin=('Profit_Margin','mean')
    ).sort_values('Margin').reset_index()
    colors = ['#eb5757' if m < 0 else '#6fcf97' for m in pm['Margin']]
    fig = go.Figure(go.Bar(
        x=pm['Margin'], y=pm['Sub_Category'], orientation='h',
        marker_color=colors, marker_line_width=0,
    ))
    fig.update_layout(**PLOTLY_THEME, height=300, showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', ticksuffix='%', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10)))
    fig.add_vline(x=0, line_color='#252d42', line_width=1)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col7:
    st.markdown('<div class="section-header">🚚 Ship Mode Distribution</div>', unsafe_allow_html=True)
    sm = fdf['Ship_Mode'].value_counts().reset_index()
    sm.columns = ['Ship_Mode', 'Count']
    fig = go.Figure(go.Pie(
        labels=sm['Ship_Mode'], values=sm['Count'],
        hole=0.6, marker=dict(colors=['#f2c94c','#56ccf2','#bb6bd9','#6fcf97']),
        textinfo='percent+label', textfont=dict(size=11, color='#dde3f0'),
    ))
    fig.update_layout(**PLOTLY_THEME, height=300,
        legend=dict(orientation='h', y=-0.18, font=dict(size=10, color='#8892a4')))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col8:
    st.markdown('<div class="section-header">🔍 Discount vs Profit Impact</div>', unsafe_allow_html=True)
    disc = fdf[fdf['Discount'] > 0].copy()
    disc['Discount_Pct'] = (disc['Discount'] * 100).round(0).astype(int)
    dp = disc.groupby('Discount_Pct').agg(Avg_Profit=('Profit','mean'), Count=('Sales','count')).reset_index()
    fig = px.scatter(dp, x='Discount_Pct', y='Avg_Profit',
                     size='Count', color='Avg_Profit',
                     color_continuous_scale=['#eb5757','#f2c94c','#6fcf97'],
                     labels={'Discount_Pct':'Discount %','Avg_Profit':'Avg Profit ($)','Count':'# Orders'})
    fig.update_layout(**PLOTLY_THEME, height=300, coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', ticksuffix='%'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$'))
    fig.add_hline(y=0, line_color='#eb5757', line_dash='dash', line_width=1)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# ROW 4 — YEARLY TREND + TOP PRODUCTS TABLE
# ─────────────────────────────────────────────
col9, col10 = st.columns([2, 3])

with col9:
    st.markdown('<div class="section-header">📅 Revenue & Profit by Year</div>', unsafe_allow_html=True)
    yr = fdf.groupby('Year').agg(Revenue=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    yr = yr.sort_values('Year')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=yr['Year'].astype(str), y=yr['Revenue'], name='Revenue',
        marker_color='#f2c94c', marker_line_width=0))
    fig.add_trace(go.Bar(x=yr['Year'].astype(str), y=yr['Profit'], name='Profit',
        marker_color='#6fcf97', marker_line_width=0))
    fig.update_layout(**PLOTLY_THEME, height=280, barmode='group',
        legend=dict(orientation='h', y=1.1, font=dict(size=11, color='#8892a4')),
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickprefix='$'))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col10:
    st.markdown('<div class="section-header">🏅 Top 10 Products by Revenue</div>', unsafe_allow_html=True)
    top_prod = (fdf.groupby(['Product_Name','Category','Sub_Category'])
                .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order_ID','count'))
                .sort_values('Revenue', ascending=False).head(10).reset_index())
    top_prod['Margin'] = (top_prod['Profit'] / top_prod['Revenue'] * 100).round(1)
    top_prod['Revenue'] = top_prod['Revenue'].apply(lambda x: f"${x:,.0f}")
    top_prod['Profit']  = top_prod['Profit'].apply(lambda x: f"${x:,.0f}")
    top_prod['Margin']  = top_prod['Margin'].apply(lambda x: f"{x}%")
    top_prod.index = range(1, len(top_prod)+1)
    top_prod.columns = ['Product','Category','Sub-Cat','Revenue','Profit','Orders','Margin']
    st.dataframe(top_prod, use_container_width=True, height=280)

# ─────────────────────────────────────────────
# ROW 5 — STATE HEATMAP / SALES MAP
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🗺 Sales by US State (Choropleth)</div>', unsafe_allow_html=True)
state_df = fdf.groupby('State').agg(Revenue=('Sales','sum'), Profit=('Profit','sum')).reset_index()
fig = px.choropleth(
    state_df, locations='State', locationmode='USA-states',
    color='Revenue', scope='usa',
    color_continuous_scale=['#1c2235','#2a3a5c','#f2c94c'],
    hover_data={'Revenue': ':$,.0f', 'Profit': ':$,.0f'},
    labels={'Revenue': 'Revenue ($)'}
)
fig.update_layout(**PLOTLY_THEME, height=380,
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)',
             landcolor='#1c2235', subunitcolor='#252d42'),
    coloraxis_colorbar=dict(tickprefix='$', title='Revenue', tickfont=dict(color='#8892a4')))
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# ROW 6 — DAYS TO SHIP + QUARTERLY HEATMAP
# ─────────────────────────────────────────────
col11, col12 = st.columns(2)

with col11:
    st.markdown('<div class="section-header">⏱ Avg Days to Ship by Ship Mode</div>', unsafe_allow_html=True)
    if 'Days_to_Ship' in fdf.columns:
        dts = fdf.groupby('Ship_Mode')['Days_to_Ship'].mean().sort_values().reset_index()
        fig = px.bar(dts, x='Days_to_Ship', y='Ship_Mode', orientation='h',
                     color='Ship_Mode', color_discrete_sequence=COLORS,
                     labels={'Days_to_Ship':'Avg Days','Ship_Mode':''})
        fig.update_layout(**PLOTLY_THEME, height=240, showlegend=False,
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0)'))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col12:
    st.markdown('<div class="section-header">🗓 Revenue Heatmap — Month × Year</div>', unsafe_allow_html=True)
    if 'Year' in fdf.columns and 'Month' in fdf.columns:
        heat = fdf.groupby(['Year','Month'])['Sales'].sum().reset_index()
        heat_piv = heat.pivot(index='Year', columns='Month', values='Sales').fillna(0)
        month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        cols_present = [m for m in range(1,13) if m in heat_piv.columns]
        heat_piv = heat_piv[cols_present]
        fig = go.Figure(go.Heatmap(
            z=heat_piv.values,
            x=[month_labels[m-1] for m in cols_present],
            y=heat_piv.index.astype(str),
            colorscale=[[0,'#1c2235'],[0.5,'#2a3a5c'],[1,'#f2c94c']],
            hovertemplate='Year: %{y}<br>Month: %{x}<br>Revenue: $%{z:,.0f}<extra></extra>',
        ))
        fig.update_layout(**PLOTLY_THEME, height=240,
            xaxis=dict(gridcolor='rgba(0,0,0,0)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# RAW DATA TABLE + DOWNLOAD
# ─────────────────────────────────────────────
with st.expander("📋 Raw / Filtered Data Table", expanded=False):
    show_cols = ['Order_ID','Order_Date','Customer_Name','Segment','Region','State',
                 'Category','Sub_Category','Product_Name','Ship_Mode',
                 'Sales','Quantity','Discount','Profit','Profit_Margin','Days_to_Ship']
    show_cols = [c for c in show_cols if c in fdf.columns]
    st.dataframe(fdf[show_cols].reset_index(drop=True), use_container_width=True, height=320)

    csv_out = fdf[show_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Download Filtered Data as CSV",
        data=csv_out,
        file_name=f"filtered_sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
        use_container_width=True
    )

# ─────────────────────────────────────────────
# ANOMALY / TREND HIGHLIGHTS
# ─────────────────────────────────────────────
with st.expander("🔎 Anomaly & Trend Highlights", expanded=False):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**🔴 High-Discount Loss Orders**")
        loss = fdf[(fdf['Discount'] >= 0.4) & (fdf['Profit'] < 0)][
            ['Order_ID','Product_Name','Sales','Discount','Profit']].head(10)
        loss['Sales']    = loss['Sales'].apply(lambda x: f"${x:,.0f}")
        loss['Discount'] = loss['Discount'].apply(lambda x: f"{int(x*100)}%")
        loss['Profit']   = loss['Profit'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(loss.reset_index(drop=True), use_container_width=True, height=220)

    with c2:
        st.markdown("**🟡 Top Customers by Revenue**")
        cust = fdf.groupby('Customer_Name').agg(
            Revenue=('Sales','sum'), Orders=('Order_ID','nunique')
        ).sort_values('Revenue', ascending=False).head(10).reset_index()
        cust['Revenue'] = cust['Revenue'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(cust, use_container_width=True, height=220)

    with c3:
        st.markdown("**🟢 Best Profit Margin Products (min 5 orders)**")
        best = (fdf.groupby('Product_Name')
                .agg(Margin=('Profit_Margin','mean'), Orders=('Order_ID','count'), Revenue=('Sales','sum'))
                .query('Orders >= 5')
                .sort_values('Margin', ascending=False).head(10).reset_index())
        best['Margin']  = best['Margin'].apply(lambda x: f"{x:.1f}%")
        best['Revenue'] = best['Revenue'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(best, use_container_width=True, height=220)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-size:11px;color:#4a5568;padding:8px 0;'>
  <strong style='color:#8892a4;'>Asha Kalavagunta</strong> &nbsp;·&nbsp; Data Analyst Portfolio &nbsp;·&nbsp;
  Kaggle Superstore Dataset &nbsp;·&nbsp; Built with Python · Streamlit · Plotly &nbsp;·&nbsp;
  <a href='https://github.com/Ashakalavagunta' target='_blank' style='color:#6b7a99;'>GitHub</a> &nbsp;·&nbsp;
  <a href='https://www.linkedin.com/in/asha-kalavagunta-80031b223/' target='_blank' style='color:#6b7a99;'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
