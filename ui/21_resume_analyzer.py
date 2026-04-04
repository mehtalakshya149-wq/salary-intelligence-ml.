import streamlit as st
import json
from ml.src.resume_service import analyze_resume_text, get_company_recommendations
import pdfplumber

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM RESUME ANALYZER STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-left, #0c2340 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 36px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #f59e0b;
    margin-bottom: 12px;
}

.header-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
    display: inline-block;
}

.ai-badge {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
    margin-left: 10px;
    vertical-align: middle;
    display: inline-block;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
}

/* ── Two Column Layout ── */
.resume-container {
    display: flex;
    gap: 40px;
    align-items: flex-start;
}

.left-column {
    width: 40%;
    position: relative;
}

.right-column {
    width: 56%;
}

.column-divider {
    position: absolute;
    right: -20px;
    top: 0;
    bottom: 0;
    width: 1px;
    background: var(--border);
}

/* ── Section Heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #f59e0b;
    padding-left: 12px;
    margin-bottom: 24px;
}

/* ── Labels ── */
.field-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
    display: block;
}

/* ── File Upload Dropzone ── */
.file-dropzone {
    background: rgba(245, 158, 11, 0.04);
    border: 2px dashed rgba(245, 158, 11, 0.25);
    border-radius: 14px;
    padding: 32px 24px;
    text-align: center;
    transition: all 0.2s ease;
    margin-bottom: 20px;
}

.file-dropzone:hover,
.file-dropzone.drag-over {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
}

.dropzone-icon {
    font-size: 32px;
    color: #f59e0b;
    margin-bottom: 12px;
}

.dropzone-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.dropzone-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 4px;
}

.browse-btn {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Sora', sans-serif;
}

.browse-btn:hover {
    background: #f59e0b;
    color: #000000;
}

/* ── OR Divider ── */
.or-divider {
    display: flex;
    align-items: center;
    margin: 20px 0;
}

.or-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

.or-text {
    font-size: 11px;
    color: #475569;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 0 16px;
}

/* ── Textarea ── */
.stTextArea > div > textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 13px !important;
    line-height: normal !important;
    min-height: 180px !important;
    font-family: 'Sora', sans-serif !important;
    transition: all 0.2s ease !important;
}

.stTextArea > div > textarea:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.12) !important;
    outline: none !important;
}

.stTextArea > div > textarea::placeholder {
    color: #475569 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #f59e0b !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(245, 158, 11, 0.04) !important;
    border: 2px dashed rgba(245, 158, 11, 0.25) !important;
    border-radius: 14px !important;
    padding: 32px 24px !important;
    text-align: center !important;
    transition: all 0.2s ease !important;
    margin-bottom: 20px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #f59e0b !important;
    background: rgba(245, 158, 11, 0.08) !important;
}

[data-testid="stFileUploader"] label {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 8px !important;
}

[data-testid="stFileUploader"] small {
    font-size: 12px !important;
    color: var(--text-secondary) !important;
}

/* ── Analyze Button ── */
.stButton > button[kind="primary"] {
    width: 100% !important;
    background: linear-gradient(135deg, #d97706, #f59e0b) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 20px !important;
    line-height: normal !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(110%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(245, 158, 11, 0.35) !important;
}

/* ── Empty State Card ── */
.empty-state-card {
    background: rgba(245, 158, 11, 0.04);
    border: 1px dashed rgba(245, 158, 11, 0.2);
    border-radius: 16px;
    padding: 48px 32px;
    text-align: center;
}

.empty-state-icon {
    font-size: 48px;
    color: #f59e0b;
    opacity: 0.4;
}

.empty-state-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 16px;
}

.empty-state-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 8px;
    line-height: 1.6;
}

.feature-pills {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 24px;
    flex-wrap: wrap;
}

.feature-pill {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--text-secondary);
}

/* ── Result Cards ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}

.result-section-title {
    font-size: 13px;
    font-weight: 700;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
}

/* ── Probability Score Display ── */
.probability-display {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: var(--text-primary);
    margin-bottom: 20px;
}

.probability-value {
    font-size: 48px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}

.probability-label {
    margin: 0;
    font-size: 13px;
    color: var(--text-primary);
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

/* ── Style Streamlit File Uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface-2) !important;
    border: 2px dashed #0d3318 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #f59e0b !important;
    background: rgba(245,158,11,0.05) !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] .stMarkdown {
    color: var(--text-secondary) !important;
    font-size: 14px !important;
}

[data-testid="stFileUploader"] button {
    background: rgba(245,158,11,0.15) !important;
    color: #f59e0b !important;
    border: 1px solid rgba(245,158,11,0.3) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] button:hover {
    background: rgba(245,158,11,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="page-header">
    <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
    <h1 class="header-title">Resume Analyzer & Job Recommendation</h1>
    <span class="ai-badge">AI Powered</span>
    <p class="header-subtitle">Upload your resume to receive AI-powered job matches, skill gap analysis, and profile improvement tips.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="resume-container">', unsafe_allow_html=True)

# Left Column - Your Profile
st.markdown('<div class="left-column">', unsafe_allow_html=True)
st.markdown('<div class="column-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Your Profile</div>', unsafe_allow_html=True)

# File Upload
st.markdown('<label class="field-label">Upload Resume (TXT/PDF)</label>', unsafe_allow_html=True)
upload_file = st.file_uploader("Drag and drop file here or click to browse", type=["txt", "pdf"], label_visibility="visible", key="resume_uploader")

# OR Divider
st.markdown('''
<div class="or-divider">
    <div class="or-line"></div>
    <div class="or-text">OR</div>
    <div class="or-line"></div>
</div>
''', unsafe_allow_html=True)

# Paste Resume Text
manual_text = st.text_area("", height=200, placeholder="Paste your resume content here...", label_visibility="collapsed", key="resume_text")

# Target Role
st.markdown('<label class="field-label" style="margin-top: 20px; margin-bottom: 8px;">Optional: Target Role</label>', unsafe_allow_html=True)
target_role = st.selectbox("", ["None", "Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer"], label_visibility="collapsed", key="target_role_select")

# Analyze Button
analyze_btn = st.button("✨ Analyze Resume", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close left-column

# Right Column - Analysis Output
st.markdown('<div class="right-column">', unsafe_allow_html=True)

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
            
            # Probability Score Display
            prob = res["target_analysis"]["probability_score"]
            color = "#10b981" if prob > 70 else "#f59e0b" if prob > 40 else "#ef4444"
            st.markdown(f'''
            <div class="probability-display" style="background: {color};">
                <h1 class="probability-value">{prob}%</h1>
                <p class="probability-label">Selection Probability (Target: {res['target_analysis']['role']})</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Recommendation Cards
            c_role, c_match = st.columns(2)
            best_role, best_score = res["recommendations"][0]
            
            st.markdown(f'''
            <div class="result-card">
                <div class="result-section-title">🎯 Best Fit Analysis</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div>
                        <div style="font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px;">Best Fit Role</div>
                        <div style="font-size: 18px; font-weight: 700; color: var(--text-primary);">{best_role}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px;">Skill Match Score</div>
                        <div style="font-size: 18px; font-weight: 700; color: #f59e0b;">{res['target_analysis']['match_score']}%</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Extracted Skills
            st.markdown(f'''
            <div class="result-card">
                <div class="result-section-title">✅ Extracted Skills</div>
                <div style="font-size: 14px; color: #cbd5e1; line-height: 1.6;">{', '.join(res['extracted_skills'])}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Recommended Companies
            st.markdown(f'''
            <div class="result-card">
                <div class="result-section-title">🏢 Recommended Companies</div>
                <div style="font-size: 14px; color: #10b981; font-weight: 600;">{', '.join(res['companies'])}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Resume Improvement Tips
            st.markdown(f'''
            <div class="result-card">
                <div class="result-section-title">💡 Resume Improvement Tips</div>
                {''.join([f'<div style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px; padding-left: 16px; border-left: 2px solid #f59e0b;">👉 {tip}</div>' for tip in res['tips']])}
            </div>
            ''', unsafe_allow_html=True)
            
            # Skill Gaps
            if res["target_analysis"]["missing_skills"]:
                st.markdown(f'''
                <div class="result-card">
                    <div class="result-section-title">🎯 Skill Gaps for Target Role</div>
                    <div style="font-size: 13px; color: #f59e0b; font-weight: 600;">Add these to your profile: {', '.join(res['target_analysis']['missing_skills'])}</div>
                </div>
                ''', unsafe_allow_html=True)

elif not manual_text:
    st.markdown('''
    <div class="empty-state-card">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-title">Your analysis will appear here</div>
        <div class="empty-state-subtitle">Upload or paste your resume, then click Analyze Resume</div>
        <div class="feature-pills">
            <span class="feature-pill">🎯 Job Matches</span>
            <span class="feature-pill">📊 Skill Gap</span>
            <span class="feature-pill">💡 Profile Tips</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close right-column
st.markdown('</div>', unsafe_allow_html=True)  # Close resume-container
