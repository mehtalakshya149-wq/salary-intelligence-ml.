import streamlit as st
import os

st.title("🧠 Advanced AI Explainability (SHAP)")
st.markdown("Unlock the 'black box' of the prediction pipeline utilizing SHAP (SHapley Additive exPlanations). These charts quantify precisely *how aggressively* specific input features shift the output scale universally across your dataset.")

shap_sum_path = os.path.join("ml", "models", "metadata", "shap", "shap_summary.png")
shap_bar_path = os.path.join("ml", "models", "metadata", "shap", "shap_bar.png")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Absolute Impact Values")
    if os.path.exists(shap_bar_path):
        st.image(shap_bar_path, caption="Feature Importance Bar Chart (Global Averages)", use_container_width=True)
    else:
        st.warning(f"File {shap_bar_path} omitted. Please trigger the underlying `explainability.py` framework.")

with col2:
    st.subheader("High Dimensionality Heatmaps")
    if os.path.exists(shap_sum_path):
        st.image(shap_sum_path, caption="SHAP Distribution Swarm Matrix (Higher Density/Color indicate intense correlation weight)", use_container_width=True)
