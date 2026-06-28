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

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Inventory Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Analysis")
st.subheader("Product Inventory & Stock Performance")

# -----------------------------
# Load Data
# -----------------------------
try:
    df = pd.read_csv("../data/clean_retail_data.csv")
except:
    st.error("clean_retail_data.csv not found!")
    st.stop()

# -----------------------------
# Inventory Summary
# -----------------------------
inventory = (
    df.groupby("Description")
    .agg(
        TotalSales=("TotalSales", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

# Top Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📦 Products", inventory.shape[0])

with col2:
    st.metric("📈 Total Quantity", int(inventory["Quantity"].sum()))

with col3:
    st.metric("💰 Total Sales", f"₹ {inventory['TotalSales'].sum():,.0f}")

st.divider()

# -----------------------------
# Top Products Chart
# -----------------------------
top_products = inventory.sort_values(
    "TotalSales",
    ascending=False
).head(10)

fig = px.bar(
    top_products,
    x="Description",
    y="TotalSales",
    color="Quantity",
    title="Top 10 Products by Sales"
)

fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Sales",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Inventory Table
# -----------------------------
st.subheader("Inventory Summary")

st.dataframe(
    inventory.sort_values("TotalSales", ascending=False),
    use_container_width=True
)