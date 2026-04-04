import streamlit as st
import pandas as pd
from ml.src.skill_gap import get_skill_gap_report
from ml.src.roadmaps import generate_roadmap

st.set_page_config(page_title="Learning Roadmap", page_icon="🛣️", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CAREER ROADMAP STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at bottom-left, #0d2618 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 36px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #06b6d4;
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

.personalized-badge {
    background: rgba(6, 182, 212, 0.15);
    color: #06b6d4;
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
    max-width: 580px;
}

/* ── Two Column Layout ── */
.roadmap-container {
    display: flex;
    gap: 40px;
    align-items: flex-start;
}

.left-column {
    width: 36%;
    position: relative;
}

.right-column {
    width: 60%;
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
    border-left: 3px solid #06b6d4;
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
    margin-bottom: 8px;
    display: block;
}

/* ── Input & Textarea Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
    background: var(--surface-2) !important;
    border: 1px solid #164e63 !important;
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
    border-color: #06b6d4 !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.12) !important;
    outline: none !important;
}

.stTextArea > div > textarea {
    min-height: 100px !important;
}

.stTextArea > div > textarea::placeholder {
    color: #475569 !important;
}

/* ── Skill Pills ── */
.skill-pills {
    display: inline-flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
}

.skill-pill {
    background: rgba(6, 182, 212, 0.1);
    color: #06b6d4;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 12px;
}

/* ── Slider Styling ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #06b6d4, #3b82f6) !important;
}

.stSlider > div > div > div {
    background: #0f2533 !important;
    height: 6px !important;
    border-radius: 999px !important;
}

/* ── Generate Button ── */
.stButton > button[kind="primary"] {
    width: 100% !important;
    background: linear-gradient(135deg, #0891b2, #06b6d4) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 28px !important;
    line-height: normal !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(115%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(6, 182, 212, 0.35) !important;
}

/* ── Journey Time Card ── */
.journey-card {
    background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(59,130,246,0.08));
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 28px;
}

.journey-label {
    font-size: 11px;
    font-weight: 600;
    color: #06b6d4;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.journey-value {
    font-size: 36px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin-top: 6px;
}

.journey-badge {
    background: rgba(6, 182, 212, 0.15);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.25);
    border-radius: 999px;
    padding: 5px 16px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 10px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Phase Cards ── */
.phases-container {
    display: flex;
    gap: 12px;
    margin: 16px 0 28px;
}

.phase-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    position: relative;
    overflow: hidden;
}

.phase-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
}

.phase-card.foundational::before {
    background: #10b981;
}

.phase-card.professional::before {
    background: #f59e0b;
}

.phase-card.expert::before {
    background: #ef4444;
}

.phase-count {
    font-size: 24px;
    font-weight: 800;
    color: var(--text-primary);
}

.phase-label {
    font-size: 11px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Step Cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}

.step-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: #06b6d4;
}

.step-card:hover {
    border-color: rgba(6, 182, 212, 0.25);
    transform: translateY(-1px);
}

.step-badge {
    background: rgba(6, 182, 212, 0.15);
    color: #06b6d4;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
    display: inline-block;
}

.step-skill {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin-left: 10px;
}

.resource-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 12px;
    font-size: 13px;
    color: var(--text-primary);
}

.effort-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 6px;
    font-size: 13px;
}

.effort-value {
    color: #f59e0b;
    font-weight: 600;
}

.progress-bar {
    background: #0f2533;
    height: 4px;
    border-radius: 999px;
    margin-top: 14px;
    overflow: hidden;
}

.progress-fill {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stMetric {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="page-header">
    <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
        <line x1="8" y1="2" x2="8" y2="18"></line>
        <line x1="16" y1="6" x2="16" y2="22"></line>
    </svg>
    <h1 class="header-title">Career Learning Roadmap</h1>
    <span class="personalized-badge">Personalized</span>
    <p class="header-subtitle">Transform your identified skill gaps into a structured, chronological curriculum with estimated timelines and curated resources.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)

# Left Column - Your Career Target
st.markdown('<div class="left-column">', unsafe_allow_html=True)
st.markdown('<div class="column-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Your Career Target</div>', unsafe_allow_html=True)

# Target Role
st.markdown('<label class="field-label">Target Role</label>', unsafe_allow_html=True)
job_title = st.text_input("", value="Senior Data Scientist", label_visibility="collapsed", key="job_title_input")

# Existing Skills
st.markdown('<label class="field-label" style="margin-top: 20px;">Existing Skills</label>', unsafe_allow_html=True)
user_skills = st.text_area("", value="Python, SQL", placeholder="e.g. Python, SQL, Excel...", label_visibility="collapsed", key="skills_textarea")

# Show skill pills
if user_skills.strip():
    skills_list = [s.strip() for s in user_skills.split(',') if s.strip()]
    pills_html = ''.join([f'<span class="skill-pill">{skill}</span>' for skill in skills_list])
    st.markdown(f'<div class="skill-pills">{pills_html}</div>', unsafe_allow_html=True)

# Weekly Learning Commitment
st.markdown('<label class="field-label" style="margin-top: 20px;">Weekly Learning Commitment</label>', unsafe_allow_html=True)
weekly_hours = st.slider("", min_value=1, max_value=20, value=10, step=1, label_visibility="collapsed", key="hours_slider")

# Generate Roadmap button
gen_btn = st.button("🗺️ Generate Roadmap", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close left-column

# Right Column - Output Panel
st.markdown('<div class="right-column">', unsafe_allow_html=True)

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
                
                # Journey Time Card
                st.markdown(f'''
                <div class="journey-card">
                    <div class="journey-label">Estimated Journey Time</div>
                    <div class="journey-value">{roadmap['estimated_weeks']} Weeks</div>
                    <div class="journey-badge">
                        <span style="color: #10b981;">↑</span>
                        {roadmap['total_estimated_hours']} Total Hours
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Journey Phases
                st.markdown('<div class="section-heading">Journey Phases</div>', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div class="phases-container">
                    <div class="phase-card foundational">
                        <div class="phase-count">{len(roadmap['phases']['Foundational'])}</div>
                        <div class="phase-label">Foundational Skills</div>
                    </div>
                    <div class="phase-card professional">
                        <div class="phase-count">{len(roadmap['phases']['Professional'])}</div>
                        <div class="phase-label">Professional Skills</div>
                    </div>
                    <div class="phase-card expert">
                        <div class="phase-count">{len(roadmap['phases']['Expert'])}</div>
                        <div class="phase-label">Expert Skills</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Step-by-Step Curriculum
                st.markdown('<div class="section-heading">Step-by-Step Curriculum</div>', unsafe_allow_html=True)
                
                for i, step in enumerate(roadmap['chronological_steps']):
                    progress_pct = ((i + 1) / len(roadmap['chronological_steps'])) * 100
                    
                    st.markdown(f'''
                    <div class="step-card">
                        <div>
                            <span class="step-badge">Step {i+1}</span>
                            <span class="step-skill">{step['skill']}</span>
                        </div>
                        <div class="resource-row">
                            <span style="color: #06b6d4;">📖</span>
                            <span><strong>Recommended Resource:</strong> {step['resource']}</span>
                        </div>
                        <div class="effort-row">
                            <span style="color: #f59e0b;">⏳</span>
                            <span><strong>Effort:</strong> <span class="effort-value">{step['hours']} Hours</span></span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {progress_pct}%"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.success("💡 Pro Tip: Prioritize hands-on projects alongside these courses to solidify the ROI.")
                
        except Exception as e:
            st.error(f"Roadmap generation failed: {e}")
else:
    st.markdown('''
    <div style="background: var(--surface-glass); border: 1px dashed var(--border); border-radius: 16px; padding: 48px 32px; text-align: center;">
        <div style="font-size: 48px; color: #06b6d4; opacity: 0.4;">🗺️</div>
        <div style="font-size: 16px; font-weight: 600; color: var(--text-secondary); margin-top: 16px;">Your personalized roadmap will appear here</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-top: 8px; line-height: 1.6;">Input your target role and hours to generate your career jump-start plan</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close right-column
st.markdown('</div>', unsafe_allow_html=True)  # Close roadmap-container
