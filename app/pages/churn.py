import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="⚠️",
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
# Title
# -----------------------------
st.title("⚠️ Customer Churn Prediction")
st.caption("Identify customers likely to leave the business")

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
# Create Customer Summary
# -----------------------------
customer_df = (
    df.groupby("CustomerID")
    .agg(
        TotalSales=("TotalSales", "sum"),
        Orders=("Invoice", "nunique")
    )
    .reset_index()
)

# Simple churn logic for demo
avg_sales = customer_df["TotalSales"].mean()

customer_df["Prediction"] = (
    customer_df["TotalSales"] < avg_sales
).astype(int)

# -----------------------------
# KPIs
# -----------------------------
total = len(customer_df)
churn = customer_df["Prediction"].sum()
retained = total - churn

c1, c2, c3 = st.columns(3)

c1.metric("👥 Total Customers", total)
c2.metric("⚠️ Predicted Churn", int(churn))
c3.metric("😊 Retained", int(retained))

st.divider()

# -----------------------------
# Churn Distribution
# -----------------------------
fig = px.pie(
    values=[retained, churn],
    names=["Retained", "Likely to Churn"],
    title="Customer Churn Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Customer Table
# -----------------------------
st.subheader("Predicted Customer Status")

customer_df["Status"] = customer_df["Prediction"].map({
    0: "Retained",
    1: "Likely to Churn"
})

st.dataframe(customer_df, use_container_width=True)

st.success("Customer Churn Prediction module loaded successfully.")