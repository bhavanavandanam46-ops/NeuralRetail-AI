import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

css_path = Path(__file__).parent.parent / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Demand Forecasting")

st.markdown("### Monthly Sales Analysis & Future Demand")

# Load Data
try:
    df = pd.read_csv("../data/clean_retail_data.csv")
except:
    st.error("Dataset not found!")
    st.stop()

# KPIs
total_sales = df["TotalSales"].sum()
avg_sales = df["TotalSales"].mean()
highest_sale = df["TotalSales"].max()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("📦 Average Sales", f"₹ {avg_sales:,.0f}")
col3.metric("🔥 Highest Sale", f"₹ {highest_sale:,.0f}")

st.divider()

# Monthly Sales
monthly = df.groupby("Month")["TotalSales"].sum().reset_index()

fig = px.line(
    monthly,
    x="Month",
    y="TotalSales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📊 Monthly Revenue")

st.dataframe(monthly, use_container_width=True)

st.success("Demand Forecasting module loaded successfully.")