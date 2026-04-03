import streamlit as st
import pandas as pd
from ml.src.career_growth import get_growth_report

st.title("📈 Career Growth Simulator")
st.markdown("Using probabilistic decision pathways, simulate overarching salary trajectories over +1, +3, and +5 years and recommend exact titles for your next leap.")

with st.expander("Update Current Parameters", expanded=True):
    col1, col2, col3 = st.columns(3)
    job_title = col1.text_input("Current Title", value="Data Analyst", key="cg_job")
    exp = col2.selectbox("Current Experience", ["EN", "MI", "SE", "EX"], index=0, key="cg_exp")
    skills = col3.text_input("Current Skills", value="SQL, Python", key="cg_skills")

if st.button("Initiate Multi-Year Simulation", type="primary", use_container_width=True):
    with st.spinner("Compiling growth paths..."):
        try:
            profile = {
                "job_title": job_title, "experience_level": exp, "skills": skills,
                "employment_type": "FT", "company_location": "US", "company_size": "M", "remote_ratio": 50, "work_year": 2024
            }
            rep = get_growth_report(profile, "ml/config.yaml")

            st.subheader("Salary Trajectory Paths")
            proj = rep["trajectory"]["projections"]
            if proj:
                df = pd.DataFrame(proj)
                df["Predicted Average ($)"] = df["predicted_salary"].apply(lambda x: x["average"])
                df["Confidence Score (%)"] = df["confidence"].apply(lambda x: x["score"])
                
                display_df = df[["year_offset", "experience_level", "Predicted Average ($)", "growth_from_current_pct", "Confidence Score (%)"]]
                st.dataframe(display_df, use_container_width=True)
                
                st.line_chart(data=display_df, x="year_offset", y="Predicted Average ($)", use_container_width=True)

            st.subheader("Top Recommended Title Leaps")
            df_recs = pd.DataFrame(rep["top_3_new_roles"])
            if not df_recs.empty:
                df_recs["Projected Salary"] = df_recs["predicted_salary"].apply(lambda x: f"${x['average']:,.0f}")
                st.dataframe(df_recs[["role", "change_pct", "Projected Salary"]], use_container_width=True)
            
        except Exception as e:
             st.error(f"Generative projection mapping encountered an error: {e}")
