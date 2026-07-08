import streamlit as st
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="NeuralRetail AI",
    page_icon="🛍️",
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------
css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# -----------------------------
# Home Page
# -----------------------------
st.title("🛍️ NeuralRetail AI")
st.subheader("AI Powered Retail Business Intelligence Platform")

st.markdown("""
Welcome to **NeuralRetail AI**, an intelligent analytics platform that helps
retail businesses analyze sales, customer behavior, inventory,
and future demand using Artificial Intelligence and Machine Learning.
""")

st.divider()

st.markdown("""
## 🚀 Modules Included

- 📊 Executive Dashboard
- 👥 Customer Segmentation
- 📈 Demand Forecasting
- ⚠️ Customer Churn Prediction
- 📦 Inventory Analysis
- 🤖 AI Business Insights

---

## 💡 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-Learn
- NumPy

---

## 🎯 Objective

Transform raw retail data into actionable business insights that improve customer retention, inventory planning, sales forecasting, and business growth.

👈 Select any module from the sidebar to begin.
""")
