import streamlit as st
import os
from ml.src.story_ai import generate_story

st.set_page_config(page_title="Explainability", page_icon="🧠", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM SHAP EXPLAINABILITY STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-right, #1f0a2e 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 28px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #ec4899;
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

.shap-badge {
    background: rgba(236, 72, 153, 0.15);
    color: #ec4899;
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
    max-width: 700px;
}

.highlight-aggressive {
    color: #ec4899;
    font-style: italic;
    font-weight: 600;
}

/* ── Tab Switcher ── */
.tab-container {
    background: #0d1117;
    border-radius: 999px;
    padding: 4px;
    display: inline-flex;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 32px;
}

.tab-pill {
    padding: 8px 24px;
    font-size: 13px;
    cursor: pointer;
    border-radius: 999px;
    transition: all 0.2s ease;
}

.tab-pill.active {
    background: rgba(236, 72, 153, 0.2);
    color: #ec4899;
    border: 1px solid rgba(236, 72, 153, 0.3);
    font-weight: 600;
}

.tab-pill.inactive {
    color: var(--text-secondary);
    border: 1px solid transparent;
}

.tab-pill.inactive:hover {
    color: #ec4899;
    border-color: rgba(236, 72, 153, 0.2);
}

/* ── Section Headings ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #ec4899;
    padding-left: 12px;
    margin-bottom: 16px;
}

/* ── Two Column Layout ── */
.two-column-layout {
    display: flex;
    gap: 24px;
}

.column-left {
    width: 48%;
}

.column-right {
    width: 48%;
}

/* ── Chart Containers ── */
.chart-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 20px;
    overflow: hidden;
}

.chart-caption {
    font-size: 12px;
    color: #475569;
    text-align: center;
    margin-top: 12px;
    font-style: italic;
}

/* ── Input Row ── */
.input-row {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}

.input-column {
    flex: 1;
}

.field-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    display: block;
}

/* ── Input & Selectbox Styling ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #3b0a2a !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input {
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ec4899 !important;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.12) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    padding: 0 !important;
}

.stSelectbox > div > div:hover {
    border-color: #ec4899 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Skill Pills ── */
.skill-pills {
    display: inline-flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
}

.skill-pill {
    background: rgba(236, 72, 153, 0.1);
    color: #ec4899;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
}

/* ── Generate Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #be185d, #ec4899) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 32px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 20px !important;
    line-height: normal !important;
    width: auto !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(115%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(236, 72, 153, 0.35) !important;
}

/* ── Empty State ── */
.empty-state-container {
    background: rgba(236, 72, 153, 0.03);
    border: 1px dashed rgba(236, 72, 153, 0.15);
    border-radius: 16px;
    padding: 48px 32px;
    text-align: center;
    margin-top: 28px;
}

.empty-state-icon {
    color: #ec4899;
    opacity: 0.25;
    font-size: 48px;
}

.empty-state-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 16px;
}

.empty-state-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 8px;
}

.feature-hints {
    display: inline-flex;
    gap: 12px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.feature-hint {
    background: var(--bg-surface);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 12px;
    color: var(--text-secondary);
}

/* ── Story Card ── */
.story-card {
    background: rgba(236, 72, 153, 0.05);
    border: 1px solid rgba(236, 72, 153, 0.15);
    border-radius: 14px;
    padding: 28px 32px;
    margin-top: 28px;
    position: relative;
}

.quote-icon {
    position: absolute;
    top: 20px;
    left: 24px;
    font-size: 32px;
    color: #ec4899;
    opacity: 0.4;
}

.story-text {
    font-size: 15px;
    color: #e2e8f0;
    line-height: 1.8;
    font-family: 'Sora', sans-serif;
    padding-left: 40px;
}

.feature-highlight {
    color: #ec4899;
    font-weight: 600;
}

.feature-chips {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 20px;
    padding-left: 40px;
}

.feature-chip {
    background: rgba(236, 72, 153, 0.1);
    color: #ec4899;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Salary Info Card ── */
.salary-info {
    background: rgba(236, 72, 153, 0.06);
    border: 1px solid rgba(236, 72, 153, 0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 16px 0;
    display: flex;
    gap: 24px;
}

.salary-item {
    flex: 1;
}

.salary-label {
    font-size: 11px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 4px;
}

.salary-value {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
}

/* ── Section Title ── */
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 20px 0 12px;
}

/* ── Insight Text ── */
.insight-text {
    font-size: 14px;
    color: var(--text-secondary);
    font-style: italic;
    line-height: 1.7;
    margin-top: 20px;
    padding: 16px 20px;
    background: rgba(236, 72, 153, 0.04);
    border-left: 3px solid #ec4899;
    border-radius: 8px;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stTabs {
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
        <path d="M12 2a10 10 0 0 1 0 20 10 10 0 0 1 0-20z"></path>
        <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
        <line x1="9" y1="9" x2="9.01" y2="9"></line>
        <line x1="15" y1="9" x2="15.01" y2="9"></line>
        <path d="M12 2v4"></path>
        <path d="M12 18v4"></path>
        <path d="M4.93 4.93l2.83 2.83"></path>
        <path d="M16.24 16.24l2.83 2.83"></path>
        <path d="M2 12h4"></path>
        <path d="M18 12h4"></path>
    </svg>
    <h1 class="header-title">Advanced AI Explainability (SHAP)</h1>
    <span class="shap-badge">SHAP</span>
    <p class="header-subtitle">Unlock the 'black box' of the prediction pipeline utilizing SHAP (SHapley Additive exPlanations). These charts quantify precisely <span class="highlight-aggressive">how aggressively</span> specific input features shift the output scale universally across your dataset.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB SWITCHER
# ══════════════════════════════════════════════════════════════════════════════
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Mathematical Charts"

st.markdown(f'''
<div class="tab-container">
    <div class="tab-pill {'active' if st.session_state.active_tab == 'Mathematical Charts' else 'inactive'}" 
         onclick="document.getElementById('tab-charts').click()">
        Mathematical Charts
    </div>
    <div class="tab-pill {'active' if st.session_state.active_tab == 'Personalized Story' else 'inactive'}"
         onclick="document.getElementById('tab-story').click()">
        Personalized Story
    </div>
</div>
''', unsafe_allow_html=True)

# Hidden buttons for tab switching
st.button("", key="tab-charts", on_click=lambda: st.session_state.update(active_tab="Mathematical Charts"), type="secondary")
st.button("", key="tab-story", on_click=lambda: st.session_state.update(active_tab="Personalized Story"), type="secondary")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 - MATHEMATICAL CHARTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Mathematical Charts":
    shap_sum_path = os.path.join("ml", "models", "metadata", "shap", "shap_summary.png")
    shap_bar_path = os.path.join("ml", "models", "metadata", "shap", "shap_bar.png")
    
    st.markdown('<div class="two-column-layout">', unsafe_allow_html=True)
    
    # Left Column
    st.markdown('<div class="column-left">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Absolute Impact Values</div>', unsafe_allow_html=True)
    
    if os.path.exists(shap_bar_path):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.image(shap_bar_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-caption">Feature Importance Bar Chart (Global Averages)</div>', unsafe_allow_html=True)
    else:
        st.warning(f"File {shap_bar_path} omitted. Please trigger the underlying `explainability.py` framework.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right Column
    st.markdown('<div class="column-right">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">High Dimensionality Heatmaps</div>', unsafe_allow_html=True)
    
    if os.path.exists(shap_sum_path):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.image(shap_sum_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-caption">SHAP Distribution Swarm Matrix (Higher Density/Color indicate intense correlation weight)</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 - PERSONALIZED STORY
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('''
    <div style="font-size: 18px; font-weight: 700; color: var(--text-primary); border-left: 3px solid #ec4899; padding-left: 14px; margin-bottom: 8px;">
        The Human Story behind your Prediction
    </div>
    <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 24px;">
        Enter your profile details to generate a natural language explanation of the decision drivers.
    </div>
    ''', unsafe_allow_html=True)
    
    # Experience level mapping
    exp_mapping = {"EN": "Entry Level", "MI": "Mid Level", "SE": "Senior Level", "EX": "Executive"}
    exp_options = ["EN", "MI", "SE", "EX"]
    exp_labels = ["Entry Level", "Mid Level", "Senior Level", "Executive"]
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<label class="field-label">Job Title</label>', unsafe_allow_html=True)
        job_title = st.text_input("", value="Data Scientist", label_visibility="collapsed", key="explain_job")
    
    with c2:
        st.markdown('<label class="field-label">Skills</label>', unsafe_allow_html=True)
        skills = st.text_input("", value="Python, SQL, AWS", label_visibility="collapsed", key="explain_skills")
        
        # Show skill pills
        if skills.strip():
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
            pills_html = ''.join([f'<span class="skill-pill">{skill}</span>' for skill in skills_list])
            st.markdown(f'<div class="skill-pills">{pills_html}</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<label class="field-label">Experience Level</label>', unsafe_allow_html=True)
        exp_index = exp_options.index("SE")
        exp_label = st.selectbox("", exp_labels, index=exp_index, label_visibility="collapsed", key="explain_exp")
        exp = exp_options[exp_labels.index(exp_label)]
    
    gen_btn = st.button("✨ Generate Narrative Explanation", type="primary")
    
    # Results
    if gen_btn:
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
                    # Story card
                    st.markdown('<div class="story-card">', unsafe_allow_html=True)
                    st.markdown('<div class="quote-icon">"</div>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color: #ec4899; font-size: 18px; font-weight: 700; margin-bottom: 16px; padding-left: 40px;">{story["headline"]}</h3>', unsafe_allow_html=True)
                    
                    # Salary info
                    st.markdown(f'''
                    <div class="salary-info" style="padding-left: 40px;">
                        <div class="salary-item">
                            <div class="salary-label">Baseline Market Salary</div>
                            <div class="salary-value">${story['base_salary']:,.0f}</div>
                        </div>
                        <div class="salary-item">
                            <div class="salary-label">Your Estimated Salary</div>
                            <div class="salary-value" style="color: #ec4899;">${story['predicted_salary']:,.0f}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Primary Positive Drivers
                    st.markdown('<div class="section-title" style="padding-left: 40px;">✅ Primary Positive Drivers</div>', unsafe_allow_html=True)
                    for p in story["positives"]:
                        # Highlight feature names
                        p_highlighted = p.replace("experience_level", "<span class='feature-highlight'>Experience Level</span>")
                        p_highlighted = p_highlighted.replace("skills", "<span class='feature-highlight'>Skills</span>")
                        p_highlighted = p_highlighted.replace("job_title", "<span class='feature-highlight'>Job Title</span>")
                        st.markdown(f'<div style="padding-left: 40px; margin-bottom: 8px; color: #e2e8f0; font-size: 14px; line-height: 1.6;">{p_highlighted}</div>', unsafe_allow_html=True)
                    
                    # Competitive Inhibitors
                    if story["negatives"]:
                        st.markdown('<div class="section-title" style="padding-left: 40px;">⚠️ Competitive Inhibitors</div>', unsafe_allow_html=True)
                        for n in story["negatives"]:
                            n_highlighted = n.replace("experience_level", "<span class='feature-highlight'>Experience Level</span>")
                            n_highlighted = n_highlighted.replace("skills", "<span class='feature-highlight'>Skills</span>")
                            n_highlighted = n_highlighted.replace("job_title", "<span class='feature-highlight'>Job Title</span>")
                            st.markdown(f'<div style="padding-left: 40px; margin-bottom: 8px; color: var(--text-secondary); font-size: 14px; line-height: 1.6;">{n_highlighted}</div>', unsafe_allow_html=True)
                    
                    # Feature impact chips
                    features_mentioned = story["positives"] + story["negatives"]
                    unique_features = list(set([f.split()[0] for f in features_mentioned if f]))
                    if unique_features:
                        chips_html = ''.join([f'<span class="feature-chip">{feat}</span>' for feat in unique_features[:5]])
                        st.markdown(f'<div class="feature-chips">{chips_html}</div>', unsafe_allow_html=True)
                    
                    # Insight summary
                    summary_highlighted = story['summary'].replace("experience_level", "<span class='feature-highlight'>Experience Level</span>")
                    summary_highlighted = summary_highlighted.replace("skills", "<span class='feature-highlight'>Skills</span>")
                    st.markdown(f'<div class="insight-text" style="padding-left: 40px;"><strong>Insight:</strong> {summary_highlighted}</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Close story-card
                    
            except Exception as e:
                st.error(f"Story generation failed: {e}")
    else:
        # Empty state
        st.markdown('''
        <div class="empty-state-container">
            <div class="empty-state-icon">🧠</div>
            <div class="empty-state-title">Your personalized SHAP story will appear here</div>
            <div class="empty-state-subtitle">We'll explain in plain language why your salary was predicted</div>
            <div class="feature-hints">
                <span class="feature-hint">🧠 Key Drivers</span>
                <span class="feature-hint">📊 Feature Impact</span>
                <span class="feature-hint">💡 Plain English</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
