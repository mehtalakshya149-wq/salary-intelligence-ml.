import streamlit as st
import requests

st.set_page_config(page_title="Download Report", page_icon="📄", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM PDF REPORT GENERATOR STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-right, var(--bg-app) 0%, var(--bg-app) 60%, var(--bg-app) 100%) !important;
}

/* ── Hero Banner Card ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(59,130,246,0.08) 100%);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}

.hero-icon {
    width: 32px;
    height: 32px;
    color: #10b981;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
}

.hero-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
}

.ai-badge {
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(16,185,129,0.15);
    color: #10b981;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #10b981;
    padding-left: 12px;
    margin-bottom: 6px;
}

.section-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 6px;
    margin-bottom: 28px;
}

/* ── Form Field Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    transition: all 0.2s ease !important;
    line-height: normal !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
    outline: none !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 6px !important;
    display: block !important;
    visibility: visible !important;
}

/* ── Submit & Download Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    line-height: normal !important;
}

.stButton > button:hover {
    filter: brightness(110%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(16,185,129,0.3) !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 10px !important;
    font-size: 13px !important;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="hero-banner">
    <div class="ai-badge">AI Powered</div>
    <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
    <h1 class="hero-title">PDF Report Generator</h1>
    <p class="hero-subtitle">Aggregate your personalized AI predictions into a clean, downloadable PDF report.</p>
</div>
''', unsafe_allow_html=True)

# Check login
if not st.session_state.get("logged_in", False):
    st.error("Please login to generate a report.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  REPORT PARAMETERS SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-heading">Report Parameters</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Confirm the details you want to inject into your official PDF export.</div>', unsafe_allow_html=True)

# Use defaults aligned to generic examples in case DB history is empty
with st.form("report_form"):
    st.markdown('<label style="font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; display: block;">Your Name</label>', unsafe_allow_html=True)
    user_name = st.text_input("", value=st.session_state.username, label_visibility="collapsed")
    
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<label style="font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; display: block;">Job Title</label>', unsafe_allow_html=True)
    job_title = st.text_input("", value="Data Scientist", label_visibility="collapsed")
    
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<label style="font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; display: block;">Predicted Salary</label>', unsafe_allow_html=True)
    predicted_salary = st.text_input("", value="$125,000 USD", label_visibility="collapsed")
    
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    # Input CSV styles for lists
    skills_raw = st.text_area("High-ROI Skills (comma separated)", value="Python, SQL, PyTorch, Cloud Architecture")
    roadmap_raw = st.text_area("Career Milestones (comma separated)", value="Master MLOps paradigms, Scale backend architectures, Transition to Lead Data Scientist")
    
    submit = st.form_submit_button("Generate PDF", use_container_width=True)

if submit:
    skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
    roadmap_list = [r.strip() for r in roadmap_raw.split(",") if r.strip()]
    
    payload = {
        "user_name": user_name,
        "job_title": job_title,
        "predicted_salary": predicted_salary,
        "skills": skills_list,
        "roadmap": roadmap_list
    }
    
    with st.spinner("Compiling PDF bytes in-memory via ReportLab..."):
        try:
            # We call the FastAPI backend to securely generate and stream the PDF
            # URL assumes local usage standard for this project (FastAPI on 8000)
            # If standard backend isn't up during Streamlit dev, we fallback to direct function usage.
            
            # For reliability during synchronous Streamlit standalone execution, we'll invoke the python module natively:
            from api.report import create_pdf_report, ReportRequest
            req = ReportRequest(**payload)
            pdf_bytes = create_pdf_report(req).getvalue()
            
            st.success("Report successfully generated!")
            
            st.download_button(
                label="⬇️ Download Official Salary Report (PDF)",
                data=pdf_bytes,
                file_name=f"Career_Report_{user_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error generating PDF report: {e}")
