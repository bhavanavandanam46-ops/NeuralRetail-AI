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
    page_title="Customer Churn",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Customer Churn Prediction")

st.markdown("### Predict Customers Likely to Leave")

try:
    df = pd.read_csv("../reports/customer_churn_predictions.csv")
except:
    st.error("Churn prediction report not found!")
    st.stop()

total = len(df)

churn = len(df[df["Prediction"] == 1])

retained = total - churn

c1, c2, c3 = st.columns(3)

c1.metric("👥 Total Customers", total)
c2.metric("⚠️ Predicted Churn", churn)
c3.metric("😊 Retained", retained)

st.divider()

fig = px.pie(
    values=[retained, churn],
    names=["Retained", "Likely to Churn"],
    title="Customer Churn Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Predicted Customers")

st.dataframe(df.head(20), use_container_width=True)

st.success("Customer Churn module loaded successfully.")