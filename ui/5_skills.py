import streamlit as st
import pandas as pd
from ml.src.skill_roi import get_roi_report

st.title("💡 Skill ROI Calculator")
st.markdown("Quantify exactly how much acquiring a specific new tool impacts your compensation tier via structural perturbation.")

col1, col2, col3 = st.columns(3)
job_title = col1.text_input("Current Title", value="Data Analyst")
skills = col2.text_input("Current Skills", value="SQL, Excel")
exp = col3.selectbox("Experience Level", ["EN", "MI", "SE", "EX"], index=1)

if st.button("Calculate Marginal ROI Impacts", use_container_width=True):
    with st.spinner("Analyzing high-dimensional skill permutations via Random Forest Evaluator..."):
        try:
            profile = {
                "job_title": job_title, "skills": skills, "experience_level": exp,
                "employment_type": "FT", "company_location": "US", "company_size": "L", "remote_ratio": 100, "work_year": 2024
            }
            res = get_roi_report(profile, "ml/config.yaml")
            
            if "message" in res:
                st.warning(res["message"])
            else:
                st.success(f"**Top Recommendation:** Target acquiring **{res['best_skill']}** for a projected **+{res['best_impact_pct']}%** initial uplift!")
                
                st.subheader("Global Skill Rankings")
                df = pd.DataFrame(res["ranked_skills"])
                
                # Format for readability
                df["impact_pct"] = df["impact_pct"].apply(lambda x: f"+{x}%")
                df["salary_increase"] = df["salary_increase"].apply(lambda x: f"${x:,.0f}")
                df["new_salary"] = df["new_salary"].apply(lambda x: f"${x:,.0f}")
                
                st.dataframe(df[["skill", "impact_pct", "salary_increase", "base_salary", "new_salary"]], use_container_width=True)
                
        except Exception as e:
            st.error(f"Model calculation failed. Verify `ml/models` are fully populated. Error: {e}")
