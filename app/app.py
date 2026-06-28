import streamlit as st
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.write(e)

st.set_page_config(
    page_title="NeuralRetail AI",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ NeuralRetail AI")
st.markdown("## AI Powered Retail Business Intelligence")

st.info("""
👈 Select a page from the **left sidebar**.

Available Modules:

- 📊 Executive Dashboard
- 👥 Customer Segmentation
- 📈 Demand Forecasting
- ⚠️ Churn Prediction
- 📦 Inventory Analysis
- 🤖 AI Insights
""")