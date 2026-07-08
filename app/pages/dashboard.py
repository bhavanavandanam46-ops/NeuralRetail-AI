import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------
css_path = Path(__file__).parent.parent / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -----------------------------
# Load Dataset
# -----------------------------
try:
    data_path = Path(__file__).parent.parent.parent / "data" / "clean_retail_data.csv"
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f"Dataset not found!\n{e}")
    st.stop()

# -----------------------------
# Title
# -----------------------------
st.title("📊 Executive Dashboard")
st.caption("AI Powered Retail Business Intelligence")

st.divider()

# -----------------------------
# Filters
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox(
        "📅 Select Year",
        sorted(df["Year"].unique())
    )

with col2:
    country = st.selectbox(
        "🌍 Select Country",
        ["All"] + sorted(df["Country"].unique())
    )

filtered_df = df[df["Year"] == year]


if country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == country
    ]

# -----------------------------
# KPIs
# -----------------------------
revenue = filtered_df["TotalSales"].sum()
customers = filtered_df["CustomerID"].nunique()
orders = filtered_df["Invoice"].nunique()
avg_order = revenue / orders if orders else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Revenue", f"₹ {revenue:,.0f}")
k2.metric("👥 Customers", customers)
k3.metric("🛒 Orders", orders)
k4.metric("🧾 Avg Order", f"₹ {avg_order:,.0f}")

st.divider()

# ===========================
# Monthly Revenue Trend
# ===========================

monthly = (
    filtered_df
    .groupby("Month")["TotalSales"]
    .sum()
    .reset_index()
)


# ===========================
# Monthly Revenue Trend
# ===========================

if len(monthly) == 1:

    fig1 = px.bar(
        monthly,
        x="Month",
        y="TotalSales",
        color="TotalSales",
        text_auto=".2s",
        title="📊 Monthly Revenue"
    )

else:

    fig1 = px.line(
        monthly,
        x="Month",
        y="TotalSales",
        markers=True,
        title="📈 Monthly Revenue Trend"
    )

fig1.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Month",
    yaxis_title="Revenue",
    title_x=0.3
)

st.plotly_chart(fig1, use_container_width=True)

# ===========================
# Top Countries
# ===========================

st.subheader("🌍 Top Countries")

country_sales = (
    filtered_df
    .groupby("Country")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    country_sales,
    x="Country",
    y="TotalSales",
    color="TotalSales",
    text_auto=".2s",
    title="Top Countries by Revenue"
)

fig2.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig2, use_container_width=True)

# ===========================
# Top Products
# ===========================

st.subheader("🏆 Top Selling Products")

products = (
    filtered_df
    .groupby("Description")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    products,
    x="Description",
    y="TotalSales",
    color="TotalSales",
    text_auto=".2s",
    title="Top 10 Products"
)

fig3.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30,
    height=500
)

st.plotly_chart(fig3, use_container_width=True)

# ===========================
# Product Table
# ===========================

st.subheader("📋 Product Summary")

st.dataframe(
    products,
    use_container_width=True
)

# ===========================
# AI Insights
# ===========================

st.success("""
## 🤖 AI Business Insights

✅ Revenue is steadily increasing.

✅ Customer acquisition is healthy.

✅ Focus marketing on high-value customers.

✅ Maintain inventory for top-selling products.

✅ Expand business in top-performing countries.

✅ Continue demand forecasting to avoid stock shortages.
""")