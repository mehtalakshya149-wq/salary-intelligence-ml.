import streamlit as st
import os
from ml.src.story_ai import generate_story

st.set_page_config(page_title="Explainability", page_icon="🧠", layout="wide")

st.title("🧠 Advanced AI Explainability (SHAP)")
st.markdown("Unlock the 'black box' of the prediction pipeline utilizing SHAP (SHapley Additive exPlanations). These charts quantify precisely *how aggressively* specific input features shift the output scale universally across your dataset.")

tab1, tab2 = st.tabs(["Mathematical Charts", "Personalized Story"])

with tab1:
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

with tab2:
    st.subheader("The Human Story behind your Prediction")
    st.markdown("Enter your profile details to generate a natural language explanation of the decision drivers.")
    
    c1, c2, c3 = st.columns(3)
    job_title = c1.text_input("Job Title", value="Data Scientist")
    skills = c2.text_input("Skills", value="Python, SQL, AWS")
    exp = c3.selectbox("Experience", ["EN", "MI", "SE", "EX"], index=2)
    
    if st.button("Generate Narrative Explanation 🗣️", type="primary", use_container_width=True):
        with st.spinner("Decoding SHAP tensors into human language..."):
            try:
                profile = {
                    "job_title": job_title, "skills": skills, "experience_level": exp,
                    "employment_type": "FT", "company_location": "US", "company_size": "L", "remote_ratio": 100, "work_year": 2024
                }
                story = generate_story(profile)
                
                if "error" in story:
                    st.error(story["error"])
                else:
                    st.success(f"### {story['headline']}")
                    
                    st.info(f"**Baseline Market Salary:** ${story['base_salary']:,.0f}  \n**Your Estimated Salary:** ${story['predicted_salary']:,.0f}")
                    
                    st.markdown("#### Primary Positive Drivers")
                    for p in story["positives"]:
                        st.write(f"✅ {p}")
                        
                    if story["negatives"]:
                        st.markdown("#### Competitive Inhibitors")
                        for n in story["negatives"]:
                            st.write(f"⚠️ {n}")
                    
                    st.divider()
                    st.write(f"*Insight: {story['summary']}*")
                    
            except Exception as e:
                st.error(f"Story generation failed: {e}")
