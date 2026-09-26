import pandas as pd

# Load dataset
df = pd.read_csv("data/superstore.csv")

# Convert date columns
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    dayfirst=True
)

df["ship_date"] = pd.to_datetime(
    df["ship_date"],
    format="mixed",
    dayfirst=True
)

# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Check duplicate rows
print("Duplicate Rows:", df.duplicated().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)

# Basic statistics
print("\nNumerical Summary:")
print(
    df[
        ["sales", "quantity", "discount", "profit", "shipping_cost"]
    ].describe()
)

# Check negative values
print("\nNegative Sales:", (df["sales"] < 0).sum())
print("Negative Quantity:", (df["quantity"] < 0).sum())

# Create useful columns
df["profit_margin"] = (df["profit"] / df["sales"]) * 100

df["delivery_days"] = (
    df["ship_date"] - df["order_date"]
).dt.days

# Display results
print("\nFirst 5 Cleaned Rows:")
print(df.head())

print("\nDataset Shape:", df.shape)

# Check missing sales
print("\nMissing Sales:", df["sales"].isnull().sum())

# Check missing values in all columns
print("\nMissing Values:")
print(df.isnull().sum())

# Check zero sales
print("\nZero Sales:", (df["sales"] == 0).sum())

# Check profit statistics
print("\nProfit Summary:")
print(df["profit"].describe())


# Create analysis dataset
analysis_df = df.dropna(subset=["sales"]).copy()

# Remove zero-sales record from sales analysis
analysis_df = analysis_df[analysis_df["sales"] > 0].copy()

# Recalculate profit margin
analysis_df["profit_margin"] = (
    analysis_df["profit"] / analysis_df["sales"]
) * 100

print("\nAnalysis Dataset Shape:", analysis_df.shape)

print("\nMissing Sales After Cleaning:",
      analysis_df["sales"].isnull().sum())

print("\nZero Sales After Cleaning:",
      (analysis_df["sales"] == 0).sum())

      # ==========================================
# CATEGORY PERFORMANCE ANALYSIS
# ==========================================

category_analysis = (
    analysis_df
    .groupby("category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        average_sales=("sales", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nCategory Performance:")
print(category_analysis.round(2))

# ==========================================
# SUB-CATEGORY PERFORMANCE ANALYSIS
# ==========================================

subcategory_analysis = (
    analysis_df
    .groupby("sub_category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        average_sales=("sales", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nSub-Category Performance:")
print(subcategory_analysis.round(2))

# ==========================================
# REGION PERFORMANCE ANALYSIS
# ==========================================

region_analysis = (
    analysis_df
    .groupby("region")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        average_sales=("sales", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nRegion Performance:")
print(region_analysis.round(2))

# ==========================================
# MONTHLY SALES TREND
# ==========================================

analysis_df["month"] = analysis_df["order_date"].dt.to_period("M")

monthly_sales = (
    analysis_df
    .groupby("month")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum")
    )
    .reset_index()
)

monthly_sales["month"] = monthly_sales["month"].astype(str)

print("\nMonthly Sales Trend:")
print(monthly_sales.round(2).to_string(index=False))

# ==========================================
# TOP PRODUCTS ANALYSIS
# ==========================================

product_analysis = (
    analysis_df
    .groupby(["product_id", "product_name"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nTop 10 Products by Sales:")
print(product_analysis.head(10).round(2).to_string())

# ==========================================
# CUSTOMER SEGMENT ANALYSIS
# ==========================================

segment_analysis = (
    analysis_df
    .groupby("segment")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        unique_customers=("customer_name", "nunique"),
        average_sales=("sales", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nCustomer Segment Performance:")
print(segment_analysis.round(2).to_string())

# ==========================================
# CUSTOMER PERFORMANCE ANALYSIS
# ==========================================

customer_analysis = (
    analysis_df
    .groupby("customer_name")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nTop 10 Customers by Sales:")
print(customer_analysis.head(10).round(2).to_string())

print("\nTop 10 Customers by Profit:")
print(
    customer_analysis
    .sort_values("total_profit", ascending=False)
    .head(10)
    .round(2)
    .to_string()
)

# ==========================================
# RFM CUSTOMER ANALYSIS
# ==========================================

# Reference date = dataset ki latest order date ke next day
reference_date = analysis_df["order_date"].max() + pd.Timedelta(days=1)

rfm = (
    analysis_df
    .groupby("customer_name")
    .agg(
        recency=("order_date", lambda x: (reference_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("sales", "sum")
    )
)

print("\nRFM Customer Analysis:")
print(rfm.head(10).round(2).to_string())

print("\nRFM Shape:", rfm.shape)

# ==========================================
# RFM SCORING
# ==========================================

# Recency:
# Lower recency = better customer engagement
rfm["R_score"] = pd.qcut(
    rfm["recency"],
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Frequency:
# Higher frequency = better customer engagement
rfm["F_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Monetary:
# Higher monetary value = higher customer value
rfm["M_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM Score
rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)

print("\nRFM Scoring:")
print(
    rfm[
        [
            "recency",
            "frequency",
            "monetary",
            "R_score",
            "F_score",
            "M_score",
            "RFM_score"
        ]
    ]
    .head(10)
    .to_string()
)

# ==========================================
# RFM CUSTOMER SEGMENTATION
# ==========================================

def assign_segment(row):
    if row["R_score"] >= 4 and row["F_score"] >= 4 and row["M_score"] >= 4:
        return "High Value"

    elif row["R_score"] >= 3 and row["F_score"] >= 4:
        return "Loyal Customers"

    elif row["R_score"] >= 4 and row["F_score"] <= 3:
        return "Potential Customers"

    elif row["R_score"] <= 2 and row["F_score"] >= 3:
        return "At Risk"

    else:
        return "Needs Attention"


rfm["segment"] = rfm.apply(assign_segment, axis=1)

print("\nCustomer Segments:")
print(rfm["segment"].value_counts())

print("\nSample Customer Segments:")
print(
    rfm[
        [
            "recency",
            "frequency",
            "monetary",
            "R_score",
            "F_score",
            "M_score",
            "RFM_score",
            "segment"
        ]
    ]
    .head(20)
    .to_string()
)

# ==========================================
# RFM SEGMENT BUSINESS PERFORMANCE
# ==========================================

segment_performance = (
    rfm
    .groupby("segment")
    .agg(
        customer_count=("segment", "count"),
        total_sales=("monetary", "sum"),
        average_sales=("monetary", "mean"),
        average_frequency=("frequency", "mean"),
        average_recency=("recency", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nRFM Segment Business Performance:")
print(segment_performance.round(2).to_string())

# ==========================================
# SHIPPING & DELIVERY ANALYSIS
# ==========================================

shipping_analysis = (
    analysis_df
    .groupby("ship_mode")
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        average_delivery_days=("delivery_days", "mean"),
        average_shipping_cost=("shipping_cost", "mean")
    )
    .sort_values("total_sales", ascending=False)
)

print("\nShipping Mode Performance:")
print(shipping_analysis.round(2).to_string())

# ==========================================
# DISCOUNT VS PROFIT ANALYSIS
# ==========================================

discount_analysis = (
    analysis_df
    .groupby("discount")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        average_profit=("profit", "mean"),
        order_count=("order_id", "nunique")
    )
    .sort_index()
)

print("\nDiscount vs Profit Analysis:")
print(discount_analysis.round(2).to_string())

# ==========================================
# PROFITABILITY ANALYSIS
# ==========================================

profitability = {
    "total_profit": analysis_df["profit"].sum(),
    "average_profit": analysis_df["profit"].mean(),
    "profitable_records": (analysis_df["profit"] > 0).sum(),
    "loss_making_records": (analysis_df["profit"] < 0).sum(),
    "zero_profit_records": (analysis_df["profit"] == 0).sum()
}

print("\nProfitability Analysis:")
for key, value in profitability.items():
    print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")

# Profitability by Category
category_profitability = (
    analysis_df
    .groupby("category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        average_profit=("profit", "mean"),
        profit_margin=("profit_margin", "mean")
    )
    .sort_values("total_profit", ascending=False)
)

print("\nCategory Profitability:")
print(category_profitability.round(2).to_string())

# Loss-making Sub-Categories
subcategory_profitability = (
    analysis_df
    .groupby("sub_category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        average_profit=("profit", "mean"),
        profit_margin=("profit_margin", "mean")
    )
    .sort_values("total_profit")
)

print("\nSub-Category Profitability:")
print(subcategory_profitability.round(2).to_string())

# ==========================================
# LOSS-MAKING PRODUCTS ANALYSIS
# ==========================================

product_profitability = (
    analysis_df
    .groupby(["product_id", "product_name"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        average_discount=("discount", "mean")
    )
    .sort_values("total_profit")
)

loss_making_products = product_profitability[
    product_profitability["total_profit"] < 0
]

print("\nLoss-Making Products:")
print(loss_making_products.head(15).round(2).to_string())

print("\nTotal Loss-Making Products:", len(loss_making_products))

# ==========================================
# CUSTOMER PROFITABILITY ANALYSIS
# ==========================================

customer_profitability = (
    analysis_df
    .groupby("customer_name")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique"),
        average_discount=("discount", "mean")
    )
    .sort_values("total_profit", ascending=False)
)

print("\nTop 10 Most Profitable Customers:")
print(customer_profitability.head(10).round(2).to_string())

print("\nTop 10 Loss-Making Customers:")
print(customer_profitability.tail(10).round(2).to_string())

print("\nTotal Customers:", len(customer_profitability))

print(
    "Loss-Making Customers:",
    (customer_profitability["total_profit"] < 0).sum()
)

# ==========================================
# SAVE ANALYSIS RESULTS
# ==========================================

import os

os.makedirs("data/processed", exist_ok=True)

category_analysis.to_csv(
    "data/processed/category_analysis.csv"
)

subcategory_profitability.to_csv(
    "data/processed/subcategory_profitability.csv"
)

monthly_sales.to_csv(
    "data/processed/monthly_sales.csv",
    index=False
)

product_profitability.to_csv(
    "data/processed/product_profitability.csv"
)

customer_profitability.to_csv(
    "data/processed/customer_profitability.csv"
)

rfm.to_csv(
    "data/processed/rfm_customer_segments.csv"
)

shipping_analysis.to_csv(
    "data/processed/shipping_analysis.csv"
)

discount_analysis.to_csv(
    "data/processed/discount_analysis.csv"
)

print("\nAnalysis files saved successfully!")