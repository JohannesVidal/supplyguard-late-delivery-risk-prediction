import streamlit as st

st.set_page_config(page_title="SupplyGuard", layout="wide")

st.title("SupplyGuard")
st.subheader("Delivery Delay Risk Prediction for E-Commerce Operations")

st.write(
    """
    This Streamlit app will be used to estimate late delivery risk for e-commerce orders.

    The final version will include:
    - Single order prediction
    - Batch CSV scoring
    - Risk level classification
    - Business recommendations
    """
)

st.info("App under development.")
