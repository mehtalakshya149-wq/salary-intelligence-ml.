import streamlit as st
import pandas as pd
from api.model_comparison import evaluate_models
from app import page_header, stat_card

st.set_page_config(page_title="Model Comparison", page_icon="⚖️", layout="wide")

page_header("AI Architecture", "Model Engine Comparison", "Inspect the architectural performance differences between the Random Forest and Gradient Boosting engines powering our predictions.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to view model architecture diagnostics.")
    st.stop()

with st.spinner("Executing model verification routines against the test hold-out set..."):
    try:
        metrics = evaluate_models()
    except Exception as e:
        st.error(f"Failed to execute model comparison. Ensure models are trained. Error: {e}")
        st.stop()

rf = metrics["random_forest"]
gb = metrics["gradient_boosting"]

st.markdown("### Top-Level Analytics")
col1, col2 = st.columns(2)

# Stat cards identifying winners
with col1:
    st.markdown('<div class="section-label-text">RANDOM FOREST</div>', unsafe_allow_html=True)
    stat_card("RF Accuracy (R²)", f"{rf['r2'] * 100:.1f}%")
    stat_card("RF RMSE Variance", f"${rf['rmse']:,.0f}")

with col2:
    st.markdown('<div class="section-label-text">GRADIENT BOOSTING</div>', unsafe_allow_html=True)
    stat_card("GB Accuracy (R²)", f"{gb['r2'] * 100:.1f}%")
    stat_card("GB RMSE Variance", f"${gb['rmse']:,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Model Variance Plotting")

# Visual comparison Bar Charts
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("**(RMSE) Root Mean Squared Error** - *Lower is better*")
    df_rmse = pd.DataFrame({
        "Model": ["Random Forest", "Gradient Boosting"],
        "RMSE Error ($)": [rf["rmse"], gb["rmse"]]
    }).set_index("Model")
    st.bar_chart(df_rmse, color="#A32D2D")

with c_right:
    st.markdown("**(Accuracy) R² Score** - *Higher is better*")
    df_acc = pd.DataFrame({
        "Model": ["Random Forest", "Gradient Boosting"],
        "Model Accuracy (%)": [rf["r2"] * 100, gb["r2"] * 100]
    }).set_index("Model")
    st.bar_chart(df_acc, color="#0F6E56")

st.markdown("<br><p style='font-size:13px;color:grey'>Note: Both models are ultimately ensembled in production within a VotingRegressor using optimized variance weighting for maximum stability.</p>", unsafe_allow_html=True)
