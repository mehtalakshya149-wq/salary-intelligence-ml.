import os
import sys
import streamlit as st
import pandas as pd

# Add the project root to sys.path so we can import ml.src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml.src.predict import run_prediction

# -- UI Configuration --
st.set_page_config(
    page_title="Salary Intelligence Platform",
    page_icon="💸",
    layout="wide"
)

st.title("💸 AI-Powered Salary Intelligence")
st.markdown("Predict accurate global salaries for Data Science & Engineering roles using Machine Learning.")
st.markdown("---")

# -- Sidebar Inputs --
st.sidebar.header("Job Parameters")

job_title = st.sidebar.text_input("Job Title", value="Data Scientist")

experience_level = st.sidebar.selectbox(
    "Experience Level",
    options=["EN", "MI", "SE", "EX"],
    index=2,
    format_func=lambda x: {"EN": "Entry-level", "MI": "Mid-level", "SE": "Senior", "EX": "Executive"}[x]
)

employment_type = st.sidebar.selectbox(
    "Employment Type",
    options=["FT", "PT", "CT", "FL"],
    index=0,
    format_func=lambda x: {"FT": "Full-Time", "PT": "Part-Time", "CT": "Contract", "FL": "Freelance"}[x]
)

company_location = st.sidebar.text_input("Company Location (Country Code)", value="US", max_chars=2)

company_size = st.sidebar.selectbox(
    "Company Size",
    options=["S", "M", "L"],
    index=2,
    format_func=lambda x: {"S": "Small (<50)", "M": "Medium (50-250)", "L": "Large (>250)"}[x]
)

remote_ratio = st.sidebar.select_slider(
    "Remote Ratio (%)",
    options=[0, 50, 100],
    value=100
)

skills = st.sidebar.text_input("Core Skills (comma-separated)", value="Python, SQL, Machine Learning")

work_year = st.sidebar.number_input(
    "Work Year", 
    min_value=2020, 
    max_value=2030, 
    value=2024,
    step=1
)

st.sidebar.markdown("---")
predict_btn = st.sidebar.button("Predict Salary 🚀", type="primary")

# -- Main Page Results --
if predict_btn:
    with st.spinner("Analyzing parameters and running ensemble prediction..."):
        try:
            # Build input dictionary exactly as model expects
            input_dict = {
                "job_title": job_title,
                "experience_level": experience_level,
                "employment_type": employment_type,
                "company_location": company_location,
                "company_size": company_size,
                "remote_ratio": remote_ratio,
                "skills": skills,
                "work_year": int(work_year),
            }
            
            # Run inference
            result = run_prediction(input_dict, config_path="ml/config.yaml")
            
            # Parsing Results
            avg_salary = result["salary"]["average"]
            min_salary = result["salary"]["min"]
            max_salary = result["salary"]["max"]
            
            confidence_score = result["confidence"]["score"]
            confidence_lbl = result["confidence"]["label"]
            
            inflated = result["inflation_adjusted"]["adjusted"]
            base_yr = result["inflation_adjusted"]["base_year"]
            
            # Display Metrics
            st.subheader(f"Estimated Base Salary ({work_year})")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Expected Salary", value=f"${avg_salary:,.0f}")
            with col2:
                st.metric(label="10th Percentile (Min)", value=f"${min_salary:,.0f}")
            with col3:
                st.metric(label="90th Percentile (Max)", value=f"${max_salary:,.0f}")
                
            st.markdown("---")
            
            st.subheader("Model Insights")
            colA, colB = st.columns(2)
            
            with colA:
                st.info(f"**Confidence Score:** {confidence_score}% - {confidence_lbl}")
                st.markdown(
                    f"The model has a {confidence_lbl.lower()} confidence in this prediction "
                    f"based on target variance and training data proximity."
                )
                
            with colB:
                if work_year < base_yr:
                    st.success(f"**Inflation Adjusted to {base_yr}:** ${inflated:,.0f}")
                    st.markdown(
                        f"Adjusted for historic CPI inflation from {work_year} to {base_yr}."
                    )
                else:
                    st.success(f"**Current Year Projection**")
                    st.markdown("No historical inflation adjustment required.")
                    
        except Exception as e:
            st.error(f"Error during prediction: {e}")
else:
    st.info("👈 Enter job parameters in the sidebar and click **Predict Salary** to view estimates.")
    
    # Show pre-computed SHAP plots if available
    st.markdown("---")
    st.markdown("### Global Feature Importance")
    shap_path = os.path.join("ml", "models", "metadata", "shap", "shap_summary.png")
    if os.path.exists(shap_path):
        st.image(shap_path, caption="SHAP Summary Plot (Model Global Insights)", use_container_width=True)
    else:
        st.markdown("*Run the training pipeline to generate SHAP plots.*")
