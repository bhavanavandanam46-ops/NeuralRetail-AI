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
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Business Insights")
st.subheader("AI Generated Retail Business Recommendations")

# -----------------------
# Load Dataset
# -----------------------
try:
    df = pd.read_csv("../data/clean_retail_data.csv")
except:
    st.error("Dataset not found!")
    st.stop()

# -----------------------
# KPIs
# -----------------------

total_sales = df["TotalSales"].sum()
total_orders = len(df)
avg_order = df["TotalSales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("🛒 Orders", total_orders)
col3.metric("📈 Avg Order", f"₹ {avg_order:.0f}")

st.divider()

# -----------------------
# Country-wise Sales
# -----------------------

country_sales = (
    df.groupby("Country")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    country_sales,
    x="Country",
    y="TotalSales",
    color="TotalSales",
    title="Top Countries by Sales"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# AI Recommendations
# -----------------------

st.subheader("🤖 AI Recommendations")

st.success("""
✅ Focus marketing on high-value customers.

✅ Increase inventory for top-selling products.

✅ Launch retention campaigns for churn-prone customers.

✅ Improve stock planning using demand forecasting.

✅ Offer personalized discounts based on customer segments.

✅ Expand sales strategies in top-performing countries.
""")