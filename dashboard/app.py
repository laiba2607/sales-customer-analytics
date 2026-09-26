import streamlit as st
import pandas as pd
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sales & Customer Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Sales & Customer Analytics Dashboard")

st.markdown(
    """
    **Interactive Business Intelligence Dashboard**

    Analyze **sales performance, profitability, customer behavior,
    RFM segmentation, discounts, and delivery performance** using
    Python, Pandas and Streamlit.
    """
)

st.caption(
    "Use the sidebar filters to explore different customer and product segments."
)

# ==========================================
# LOAD DATA
# ==========================================

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data", "processed")

RAW_DATA_PATH = os.path.join(BASE_PATH, "data", "superstore.csv")

raw_df = pd.read_csv(RAW_DATA_PATH)

raw_df["order_date"] = pd.to_datetime(
    raw_df["order_date"],
    format="mixed",
    dayfirst=True
)

raw_df["sales"] = pd.to_numeric(
    raw_df["sales"],
    errors="coerce"
)

raw_df = raw_df.dropna(subset=["sales"])
raw_df = raw_df[raw_df["sales"] > 0]

category = pd.read_csv(
    os.path.join(DATA_PATH, "category_analysis.csv")
)

monthly_sales = pd.read_csv(
    os.path.join(DATA_PATH, "monthly_sales.csv")
)

customer_profitability = pd.read_csv(
    os.path.join(DATA_PATH, "customer_profitability.csv")
)

rfm = pd.read_csv(
    os.path.join(DATA_PATH, "rfm_customer_segments.csv")
)

subcategory = pd.read_csv(
    os.path.join(DATA_PATH, "subcategory_profitability.csv")
)

discount = pd.read_csv(
    os.path.join(DATA_PATH, "discount_analysis.csv")
)

shipping = pd.read_csv(
    os.path.join(DATA_PATH, "shipping_analysis.csv")
)

product = pd.read_csv(
    os.path.join(DATA_PATH, "product_profitability.csv")
)

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore sales and customer performance."
)

st.sidebar.divider()

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=category["category"].unique(),
    default=category["category"].unique()
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=rfm["segment"].unique(),
    default=rfm["segment"].unique()
)

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = raw_df[
    raw_df["category"].isin(selected_categories)
].copy()

selected_customers = rfm[
    rfm["segment"].isin(selected_segments)
]["customer_name"]

filtered_df = filtered_df[
    filtered_df["customer_name"].isin(selected_customers)
].copy()

# ==========================================
# BASIC KPIs
# ==========================================

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_customers = filtered_df["customer_name"].nunique()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0
    else 0
)
# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col4.metric(
    "🛒 Orders",
    f"{total_orders:,}"
)

col5.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# ==========================================
# MONTHLY SALES TREND
# ==========================================

st.subheader("📈 Monthly Sales Trend")

filtered_monthly_sales = (
    filtered_df
    .assign(
        month=filtered_df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum")
    )
    .reset_index()
)

filtered_monthly_sales["month"] = pd.to_datetime(
    filtered_monthly_sales["month"]
)

st.line_chart(
    filtered_monthly_sales,
    x="month",
    y="total_sales"
)

# ==========================================
# CATEGORY PERFORMANCE
# ==========================================

# ==========================================
# SALES BY CATEGORY
# ==========================================

st.subheader("📊 Sales by Category")

filtered_category = (
    filtered_df
    .groupby("category")
    .agg(
        total_sales=("sales", "sum")
    )
    .reset_index()
)

st.bar_chart(
    filtered_category,
    x="category",
    y="total_sales"
)

# ==========================================
# PROFITABILITY BY CATEGORY
# ==========================================

# ==========================================
# PROFITABILITY BY CATEGORY
# ==========================================

st.subheader("💰 Profitability by Category")

filtered_profitability = (
    filtered_df
    .groupby("category")
    .agg(
        total_profit=("profit", "sum")
    )
    .reset_index()
)

st.bar_chart(
    filtered_profitability,
    x="category",
    y="total_profit"
)

# ==========================================
# CUSTOMER SEGMENTATION
# ==========================================

st.subheader("👥 Customer Segmentation")

filtered_segment_counts = (
    rfm[
        rfm["customer_name"].isin(
            filtered_df["customer_name"].unique()
        )
    ]["segment"]
    .value_counts()
    .reset_index()
)

filtered_segment_counts.columns = ["segment", "customers"]

st.bar_chart(
    filtered_segment_counts,
    x="segment",
    y="customers"
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Tip: Change the filters to see how sales, "
    "profitability and customer insights change dynamically."
)

# ==========================================
# TOP 10 CUSTOMERS BY SALES
# ==========================================

# ==========================================
# TOP 10 CUSTOMERS BY SALES
# ==========================================

st.subheader("🏆 Top 10 Customers by Sales")

filtered_customers = (
    filtered_df
    .groupby("customer_name")
    .agg(
        total_sales=("sales", "sum")
    )
    .reset_index()
)

top_customers = (
    filtered_customers
    .sort_values("total_sales", ascending=False)
    .head(10)
)

st.bar_chart(
    top_customers,
    x="customer_name",
    y="total_sales"
)

# ==========================================
# TOP 10 LOSS-MAKING CUSTOMERS
# ==========================================

# ==========================================
# TOP 10 LOSS-MAKING CUSTOMERS
# ==========================================

st.subheader("⚠️ Top 10 Loss-Making Customers")

filtered_loss_customers = (
    filtered_df
    .groupby("customer_name")
    .agg(
        total_profit=("profit", "sum")
    )
    .reset_index()
)

loss_customers = (
    filtered_loss_customers
    .sort_values("total_profit", ascending=True)
    .head(10)
)

st.bar_chart(
    loss_customers,
    x="customer_name",
    y="total_profit"
)
# ==========================================
# DISCOUNT VS PROFIT
# ==========================================

# ==========================================
# DISCOUNT VS PROFIT
# ==========================================

st.subheader("📉 Discount vs Profit")

filtered_discount = (
    filtered_df
    .groupby("discount")
    .agg(
        total_profit=("profit", "sum")
    )
    .reset_index()
    .sort_values("discount")
)

st.line_chart(
    filtered_discount,
    x="discount",
    y="total_profit"
)

st.caption(
    "This analysis shows how total profit changes across different discount levels."
)

# ==========================================
# SUB-CATEGORY PROFITABILITY
# ==========================================

# ==========================================
# PROFITABILITY BY SUB-CATEGORY
# ==========================================

st.subheader("📦 Profitability by Sub-Category")

filtered_subcategory = (
    filtered_df
    .groupby("sub_category")
    .agg(
        total_profit=("profit", "sum")
    )
    .reset_index()
    .sort_values("total_profit", ascending=False)
)

st.bar_chart(
    filtered_subcategory,
    x="sub_category",
    y="total_profit"
)
# ==========================================
# SHIPPING & DELIVERY PERFORMANCE
# ==========================================

# ==========================================
# DELIVERY PERFORMANCE
# ==========================================

# ==========================================
# DELIVERY PERFORMANCE
# ==========================================

st.subheader("🚚 Delivery Performance by Ship Mode")

filtered_shipping = filtered_df.copy()

filtered_shipping["ship_date"] = pd.to_datetime(
    filtered_shipping["ship_date"],
    format="mixed",
    dayfirst=True
)

filtered_shipping["delivery_days"] = (
    filtered_shipping["ship_date"]
    - filtered_shipping["order_date"]
).dt.days

filtered_shipping = (
    filtered_shipping
    .groupby("ship_mode")
    .agg(
        average_delivery_days=("delivery_days", "mean")
    )
    .reset_index()
    .sort_values("average_delivery_days", ascending=True)
)

st.bar_chart(
    filtered_shipping,
    x="ship_mode",
    y="average_delivery_days"
)

st.caption(
    "Average delivery time by shipping mode."
)

# ==========================================
# RFM CUSTOMER ANALYTICS
# ==========================================

st.subheader("🎯 RFM Customer Analytics")

filtered_rfm = rfm[
    rfm["customer_name"].isin(
        filtered_df["customer_name"].unique()
    )
].copy()

rfm_summary = (
    filtered_rfm
    .groupby("segment")
    .agg(
        customers=("customer_name", "nunique"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .reset_index()
)

rfm_summary["avg_recency"] = rfm_summary["avg_recency"].round(1)
rfm_summary["avg_frequency"] = rfm_summary["avg_frequency"].round(1)
rfm_summary["avg_monetary"] = rfm_summary["avg_monetary"].round(2)

st.dataframe(
    rfm_summary,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# RFM SEGMENT DISTRIBUTION
# ==========================================

st.subheader("📊 Customer Distribution by RFM Segment")

rfm_segment_chart = (
    filtered_rfm["segment"]
    .value_counts()
    .reset_index()
)

rfm_segment_chart.columns = ["segment", "customers"]

st.bar_chart(
    rfm_segment_chart,
    x="segment",
    y="customers"
)

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.subheader("💡 Business Insights")

high_value_customers = (
    filtered_rfm[filtered_rfm["segment"] == "High Value"]
    .shape[0]
)

at_risk_customers = (
    filtered_rfm[filtered_rfm["segment"] == "At Risk"]
    .shape[0]
)

loss_making_customers = (
    filtered_df.groupby("customer_name")["profit"]
    .sum()
)

loss_making_customers = (
    loss_making_customers[loss_making_customers < 0]
    .count()
)

best_category = (
    filtered_df.groupby("category")["sales"]
    .sum()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)

best_profit_category = (
    filtered_df.groupby("category")["profit"]
    .sum()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⭐ High Value Customers",
    f"{high_value_customers:,}"
)

col2.metric(
    "⚠️ At Risk Customers",
    f"{at_risk_customers:,}"
)

col3.metric(
    "📉 Loss-Making Customers",
    f"{loss_making_customers:,}"
)

col4.metric(
    "🏆 Best Sales Category",
    best_category
)

st.info(
    f"📊 **Key Insight:** {best_category} generates the highest sales "
    f"among the currently selected data, while {best_profit_category} "
    f"generates the highest total profit."
)

# ==========================================
# DATA QUALITY SUMMARY
# ==========================================

st.subheader("🧹 Data Quality Summary")

quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

quality_col1.metric(
    "📦 Raw Records",
    f"{len(raw_df):,}"
)

quality_col2.metric(
    "✅ Analysis Records",
    "48,659"
)

quality_col3.metric(
    "❌ Missing Sales",
    "2,630"
)

quality_col4.metric(
    "🔄 Duplicate Rows",
    "0"
)

st.caption(
    "Sales-based analysis excludes records with missing or zero sales values. "
    "The original raw dataset is retained separately."
)

# ==========================================
# PROJECT METHODOLOGY
# ==========================================

st.subheader("🔍 Project Methodology")

st.markdown(
    """
    **Data Processing**
    - Cleaned and validated raw sales data using Pandas.
    - Converted date and numerical columns into appropriate data types.
    - Handled missing sales values for sales-based analysis.
    - Created derived metrics such as delivery days and profit margin.

    **Exploratory Data Analysis**
    - Analyzed sales and profit trends.
    - Compared category and sub-category performance.
    - Evaluated discount and profitability relationships.
    - Analyzed shipping and delivery performance.

    **Customer Analytics**
    - Implemented RFM analysis using Recency, Frequency and Monetary value.
    - Segmented customers into High Value, Loyal, Potential, At Risk and Needs Attention groups.

    **Dashboard**
    - Built an interactive Streamlit dashboard.
    - Added category and customer-segment filters.
    - Designed KPI cards, charts, customer analytics and business insights.
    """
)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align: center; padding: 15px;">
        <p><strong>Sales & Customer Analytics Dashboard</strong></p>
        <p>Built with Python, Pandas & Streamlit</p>
        <p>© 2026 <strong>Laiba Mudassir</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)