import streamlit as st
import pandas as pd
import plotly.express as px
from ml.src.skill_gap import get_skill_gap_report

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🎯", layout="wide")

st.title("🎯 Precision Skill Gap Analysis")
st.markdown("Compare your current technical stack against real-time market requirements derived from thousands of salary data points.")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("Your Profile")
    job_title = st.text_input("Target Job Title", value="Data Scientist")
    user_skills = st.text_area("Your Current Skills (comma separated)", value="Python, SQL, Tableau", help="e.g. Python, SQL, AWS, Docker")
    analyze_btn = st.button("Run Gap Analysis 🚀", type="primary", use_container_width=True)

with col2:
    if analyze_btn:
        with st.spinner("Mining market requirements and calculating structural gaps..."):
            try:
                report = get_skill_gap_report(job_title, user_skills)
                
                # Top metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Market Match", f"{report['match_percentage']}%")
                m2.metric("Missing Skills", len(report['missing_skills']))
                m3.metric("Matched Skills", len(report['matched_skills']))
                
                # Radar-style Bar Chart for Skills
                st.subheader("Market Demand vs. Your Stack")
                
                # Prepare data for plotting
                plot_data = []
                for s in report['market_top_skills']:
                    plot_data.append({
                        "Skill": s.upper(),
                        "Status": "Matched" if s in report['matched_skills'] else "Gap",
                        "Value": 1 # Uniform weight for now
                    })
                
                fig = px.bar(
                    plot_data,
                    x="Skill",
                    y="Value",
                    color="Status",
                    color_discrete_map={"Matched": "#4CAF50", "Gap": "#FFC107"},
                    title=f"Core Competency Benchmarking: {job_title}",
                    labels={"Value": "Priority"}
                )
                fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Gap Table & Path
                cA, cB = st.columns(2)
                
                with cA:
                    st.subheader("Priority Gap List")
                    if report['missing_skills']:
                        df_gap = pd.DataFrame({"Missing Skill": [s.upper() for s in report['missing_skills']]})
                        st.dataframe(df_gap, use_container_width=True, hide_index=True)
                    else:
                        st.success("No critical gaps detected! You are market-ready.")
                
                with cB:
                    st.subheader("Recommended Learning Path")
                    for step in report['learning_path']:
                        st.info(f"📍 {step}")
                        
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    else:
        st.info("Enter your target job and skills on the left to begin the analysis.")

st.divider()
st.subheader("How it works")
st.markdown("""
1. **Market Mining**: The system scans the historical dataset for the provided job title.
2. **Frequency Analysis**: It identifies the top 10 most frequent skills associated with that role.
3. **Set Comparison**: Your skills are mathematically compared against the market set to identify missing nodes.
4. **Heuristic Pathing**: A custom heuristic algorithm clusters missing skills into Foundational, Scalability, and Expert phases.
""")
