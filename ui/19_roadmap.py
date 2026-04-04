import streamlit as st
import pandas as pd
from ml.src.skill_gap import get_skill_gap_report
from ml.src.roadmaps import generate_roadmap

st.set_page_config(page_title="Learning Roadmap", page_icon="🛣️", layout="wide")

st.title("🛣️ Career Learning Roadmap")
st.markdown("Transform your identified skill gaps into a structured, chronological curriculum with estimated timelines and curated resources.")

colA, colB = st.columns([1, 2], gap="large")

with colA:
    st.subheader("Your Career Target")
    job_title = st.text_input("Target Job Title", value="Senior Data Scientist")
    user_skills = st.text_area("Existing Skills", value="Python, SQL")
    weekly_hours = st.slider("Weekly Learning Commitment (Hours)", 5, 40, 10)
    gen_btn = st.button("Generate Roadmap 🚀", type="primary", use_container_width=True)

with colB:
    if gen_btn:
        with st.spinner("Analyzing skill dependencies and hydrating resources..."):
            try:
                # 1. Identity Gaps
                gap_report = get_skill_gap_report(job_title, user_skills)
                missing = gap_report["missing_skills"]
                
                if not missing:
                    st.success("🎉 You are fully market-compliant for this role! No major gaps detected.")
                    st.balloons()
                else:
                    # 2. Hydrate Roadmap
                    roadmap = generate_roadmap(missing, weekly_hours)
                    
                    st.metric("Estimated Journey Time", f"{roadmap['estimated_weeks']} Weeks", delta=f"{roadmap['total_estimated_hours']} Total Hours")
                    
                    # 3. Horizontal Progress Visual (Phases)
                    st.subheader("Journey Phases")
                    p1, p2, p3 = st.columns(3)
                    p1.markdown(f"**🟢 Foundational**\n{len(roadmap['phases']['Foundational'])} Skills")
                    p2.markdown(f"**🟡 Professional**\n{len(roadmap['phases']['Professional'])} Skills")
                    p3.markdown(f"**🔴 Expert**\n{len(roadmap['phases']['Expert'])} Skills")
                    
                    st.divider()
                    
                    # 4. Vertical Timeline (The Roadmap)
                    st.subheader("Step-by-Step Curriculum")
                    for i, step in enumerate(roadmap['chronological_steps']):
                        with st.container(border=True):
                            st.markdown(f"### Step {i+1}: {step['skill']}")
                            c1, c2 = st.columns([2, 1])
                            with c1:
                                st.write(f"📖 **Recommended Resource:** {step['resource']}")
                            with c2:
                                st.write(f"⏳ **Effort:** {step['hours']} Hours")
                            st.progress((i+1) / len(roadmap['chronological_steps']))
                            
                    st.success("💡 Pro Tip: Prioritize hands-on projects alongside these courses to solidify the ROI.")
                    
            except Exception as e:
                st.error(f"Roadmap generation failed: {e}")
    else:
        st.info("Input your target role and hours on the left to generate your personalized career jump-start.")
