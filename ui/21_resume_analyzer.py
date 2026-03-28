import streamlit as st
import json
from ml.src.resume_service import analyze_resume_text, get_company_recommendations

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Resume Analyzer & Job Recommendation")
st.markdown("Upload your resume to receive AI-powered job matches, skill gap analysis, and profile improvement tips.")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("Your Profile")
    upload_file = st.file_uploader("Upload Resume (TXT/PDF)", type=["txt", "pdf"])
    manual_text = st.text_area("Or Paste Resume Text", height=200, placeholder="Paste your resume content here...")
    
    target_role = st.selectbox("Optional: Target Role", ["None", "Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer"])
    
    analyze_btn = st.button("Analyze Resume 🚀", type="primary", use_container_width=True)
    
with col2:
    input_text = ""
    if upload_file:
        if upload_file.type == "application/pdf":
            try:
                with pdfplumber.open(upload_file) as pdf:
                    pages = [page.extract_text() for page in pdf.pages]
                    input_text = "\n".join(filter(None, pages))
            except Exception as e:
                st.error(f"Error parsing PDF: {e}")
        elif upload_file.type == "text/plain":
            input_text = upload_file.read().decode("utf-8")

    if not input_text and manual_text.strip():
        input_text = manual_text
        
    if analyze_btn:
        if not input_text:
            st.error("Please provide resume text via upload or manual paste.")
        else:
            with st.spinner("Decoding profile and matching against market datasets..."):
                role_val = None if target_role == "None" else target_role
                res = analyze_resume_text(input_text, role_val)
                res["companies"] = get_company_recommendations(res["target_analysis"]["role"])
                
                # Results Section
                st.subheader("Analysis Results")
                
                # Probability Score Gauge-like Display
                prob = res["target_analysis"]["probability_score"]
                color = "green" if prob > 70 else "orange" if prob > 40 else "red"
                st.markdown(f"""
                <div style="background:{color}; padding: 20px; border-radius: 10px; text-align: center; color: white;">
                    <h1 style="color: white; margin:0;">{prob}%</h1>
                    <p style="margin:0;">Selection Probability (Target: {res['target_analysis']['role']})</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                # Recommendation Cards
                c_role, c_match = st.columns(2)
                best_role, best_score = res["recommendations"][0]
                c_role.metric("Best Fit Role", best_role)
                c_match.metric("Skill Match Score", f"{res['target_analysis']['match_score']}%")
                
                st.markdown("#### ✅ Extracted Skills")
                st.write(", ".join(res["extracted_skills"]))
                
                st.markdown("#### 🏢 Recommended Companies")
                st.success(", ".join(res["companies"]))
                
                # Improvement HUD
                st.markdown("#### 💡 Resume Improvement Tips")
                for tip in res["tips"]:
                    st.info(f"👉 {tip}")
                    
                if res["target_analysis"]["missing_skills"]:
                    st.markdown("#### 🎯 Skill Gaps for Target Role")
                    st.warning(f"Add these to your profile: {', '.join(res['target_analysis']['missing_skills'])}")

    elif not manual_text:
        st.info("Paste your CV in the left panel to begin your career analysis.")
        
with st.sidebar:
    st.divider()
    st.subheader("Why use this?")
    st.markdown("""
    - Personalized Role Matching
    - Keyword Optimization
    - Demand-Based Probability
    - Company Discovery
    """)
