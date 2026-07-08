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
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Segmentation")

st.markdown("### Analyze Customer Groups using RFM Metrics")

try:
    report_path = Path(__file__).parent.parent.parent / "reports" / "customer_segments.csv"
    df = pd.read_csv(report_path)
except:
    st.error("Customer segmentation report not found!")
    st.stop()

col1, col2 = st.columns(2)

col1.metric("👥 Total Customers", len(df))
col2.metric("🧩 Customer Segments", df["Cluster"].nunique())

st.divider()

fig = px.pie(
    df,
    names="Cluster",
    title="Customer Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

fig2 = px.scatter(
    df,
    x="Frequency",
    y="Monetary",
    color="Cluster",
    size="Recency",
    title="Customer Segmentation"
)

st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df.head(20), use_container_width=True)

st.success("Customer Segmentation module loaded successfully.")
