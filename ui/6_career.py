import streamlit as st
import pandas as pd
from ml.src.career_growth import get_growth_report

st.set_page_config(page_title="Career Growth Simulator", page_icon="📈", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CAREER GROWTH SIMULATOR STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at center-top, #0d1f3c 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 28px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #22d3ee;
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

.multiyear-badge {
    background: rgba(34, 211, 238, 0.15);
    color: #22d3ee;
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
    max-width: 680px;
}

.highlight-year {
    color: #22d3ee;
    font-weight: 600;
}

/* ── Collapsible Panel ── */
.collapsible-panel {
    background: rgba(34, 211, 238, 0.05);
    border: 1px solid rgba(34, 211, 238, 0.15);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 24px;
}

.panel-header {
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.panel-header:hover {
    background: rgba(34, 211, 238, 0.08);
}

.panel-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.panel-icon {
    color: #22d3ee;
    font-size: 16px;
}

.panel-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

.panel-chevron {
    color: #22d3ee;
    transition: transform 0.2s ease;
}

.panel-chevron.open {
    transform: rotate(180deg);
}

.panel-body {
    padding: 24px;
    border-top: 1px solid rgba(34, 211, 238, 0.1);
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
    border: 1px solid #0e3a4a !important;
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
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.12) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    padding: 0 !important;
}

.stSelectbox > div > div:hover {
    border-color: #22d3ee !important;
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
    background: rgba(34, 211, 238, 0.1);
    color: #22d3ee;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
}

/* ── Simulation Horizon Pills ── */
.horizon-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 20px;
    margin-bottom: 10px;
    display: block;
}

.horizon-pills {
    display: inline-flex;
    gap: 10px;
    margin-top: 10px;
}

.horizon-pill {
    background: var(--surface-2);
    border: 1px solid #0e3a4a;
    border-radius: 999px;
    padding: 8px 24px;
    font-size: 13px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.horizon-pill.active {
    background: rgba(34, 211, 238, 0.15);
    border-color: #22d3ee;
    color: #22d3ee;
    font-weight: 600;
}

.horizon-pill:hover {
    border-color: rgba(34, 211, 238, 0.3);
    color: #22d3ee;
}

/* ── Simulation Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0891b2, #22d3ee) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 36px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 28px !important;
    line-height: normal !important;
    width: auto !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(110%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(34, 211, 238, 0.35) !important;
}

/* ── Empty State ── */
.empty-state-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px dashed rgba(34, 211, 238, 0.15);
    border-radius: 16px;
    padding: 56px 32px;
    text-align: center;
    margin-top: 32px;
}

.timeline-illustration {
    opacity: 0.35;
    margin: 0 auto;
}

.empty-state-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 20px;
}

.empty-state-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 8px;
}

/* ── Year Milestone Cards ── */
.milestone-cards {
    display: flex;
    gap: 16px;
    margin-top: 28px;
    opacity: 0.6;
}

.milestone-card {
    flex: 1;
    background: rgba(34, 211, 238, 0.04);
    border: 1px solid rgba(34, 211, 238, 0.1);
    border-radius: 12px;
    padding: 16px 24px;
    text-align: center;
}

.milestone-year {
    font-size: 11px;
    color: #22d3ee;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.milestone-salary {
    font-size: 28px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 4px;
}

.milestone-role {
    font-size: 12px;
    color: #334155;
}

/* ── Result Cards ── */
.result-card {
    background: rgba(34, 211, 238, 0.06);
    border: 1px solid rgba(34, 211, 238, 0.15);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.result-year {
    font-size: 11px;
    color: #22d3ee;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.result-salary {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
}

.growth-badge {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 12px;
}

.result-role {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 6px;
}

.confidence-bar {
    background: #0f2533;
    height: 4px;
    border-radius: 999px;
    margin-top: 12px;
    overflow: hidden;
}

.confidence-fill {
    background: #22d3ee;
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}

/* ── Section Titles ── */
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 28px 0 16px;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stExpander {
    display: none !important;
}

.stDataframe {
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
        <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
        <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
        <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path>
        <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path>
    </svg>
    <h1 class="header-title">Career Growth Simulator</h1>
    <span class="multiyear-badge">Multi-Year</span>
    <p class="header-subtitle">Using probabilistic decision pathways, simulate overarching salary trajectories over <span class="highlight-year">+1</span>, <span class="highlight-year">+3</span>, and <span class="highlight-year">+5 years</span> and recommend exact titles for your next leap.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  COLLAPSIBLE PANEL
# ══════════════════════════════════════════════════════════════════════════════
# Experience level mapping
exp_mapping = {"EN": "Entry Level", "MI": "Mid Level", "SE": "Senior Level", "EX": "Executive"}
exp_options = ["EN", "MI", "SE", "EX"]
exp_labels = ["Entry Level", "Mid Level", "Senior Level", "Executive"]

# Initialize session state for panel
if 'panel_expanded' not in st.session_state:
    st.session_state.panel_expanded = True

if 'sim_horizon' not in st.session_state:
    st.session_state.sim_horizon = "+3 Years"

# Panel toggle
def toggle_panel():
    st.session_state.panel_expanded = not st.session_state.panel_expanded

# Render collapsible panel
st.markdown(f'''
<div class="collapsible-panel">
    <div class="panel-header" onclick="document.getElementById('panel-toggle').click()">
        <div class="panel-header-left">
            <span class="panel-icon">⚙️</span>
            <span class="panel-title">Current Parameters</span>
        </div>
        <span class="panel-chevron {'open' if st.session_state.panel_expanded else ''}">▼</span>
    </div>
    {'<div class="panel-body">' if st.session_state.panel_expanded else ''}
''', unsafe_allow_html=True)

# Hidden toggle button
st.button("", key="panel-toggle", on_click=toggle_panel, type="secondary")

if st.session_state.panel_expanded:
    # Input Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<label class="field-label">Current Job Title</label>', unsafe_allow_html=True)
        job_title = st.text_input("", value="Data Analyst", label_visibility="collapsed", key="cg_job")
    
    with col2:
        st.markdown('<label class="field-label">Experience Level</label>', unsafe_allow_html=True)
        exp_index = exp_options.index("EN")
        exp_label = st.selectbox("", exp_labels, index=exp_index, label_visibility="collapsed", key="cg_exp")
        exp = exp_options[exp_labels.index(exp_label)]
    
    with col3:
        st.markdown('<label class="field-label">Current Skills</label>', unsafe_allow_html=True)
        skills = st.text_input("", value="SQL, Python", label_visibility="collapsed", key="cg_skills")
        
        # Show skill pills
        if skills.strip():
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
            pills_html = ''.join([f'<span class="skill-pill">{skill}</span>' for skill in skills_list])
            st.markdown(f'<div class="skill-pills">{pills_html}</div>', unsafe_allow_html=True)
    
    # Simulation Horizon Selector
    st.markdown('<label class="horizon-label">Simulation Horizon</label>', unsafe_allow_html=True)
    
    horizon_options = ["+1 Year", "+3 Years", "+5 Years"]
    
    st.markdown('<div class="horizon-pills">', unsafe_allow_html=True)
    for horizon in horizon_options:
        is_active = "active" if horizon == st.session_state.sim_horizon else ""
        st.markdown(f'''<div class="horizon-pill {is_active}" onclick="document.getElementById('horizon-{horizon.replace("+", "").replace(" ", "-")}".click()">{horizon}</div>''', unsafe_allow_html=True)
        st.button("", key=f"horizon-{horizon.replace('+', '').replace(' ', '-')}", on_click=lambda h=horizon: st.session_state.update(sim_horizon=h), type="secondary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulation Button
    sim_btn = st.button("🚀 Initiate Multi-Year Simulation", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close panel-body

st.markdown('</div>', unsafe_allow_html=True)  # Close collapsible-panel

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS AREA
# ══════════════════════════════════════════════════════════════════════════════
if 'sim_btn' in dir() and sim_btn:
    with st.spinner("Compiling growth paths..."):
        try:
            profile = {
                "job_title": job_title, "experience_level": exp, "skills": skills,
                "employment_type": "FT", "company_location": "US", "company_size": "M", "remote_ratio": 50, "work_year": 2024
            }
            rep = get_growth_report(profile, "ml/config.yaml")

            # Salary Trajectory Paths
            st.markdown('<div class="section-title">Salary Trajectory Paths</div>', unsafe_allow_html=True)
            proj = rep["trajectory"]["projections"]
            
            if proj:
                # Show year milestone cards
                st.markdown('<div class="milestone-cards" style="opacity: 1;">', unsafe_allow_html=True)
                
                for p in proj:
                    year_offset = p['year_offset']
                    salary_data = p['predicted_salary']
                    avg_salary = salary_data['average']
                    growth_pct = p.get('growth_from_current_pct', 0)
                    confidence = p['confidence']['score']
                    exp_level = p.get('experience_level', '—')
                    
                    st.markdown(f'''
                    <div class="result-card" style="flex: 1; margin-bottom: 0;">
                        <div class="result-year">+{year_offset} Year{"s" if year_offset > 1 else ""}</div>
                        <div>
                            <span class="result-salary">${avg_salary:,.0f}</span>
                            <span class="growth-badge">+{growth_pct:.1f}%</span>
                        </div>
                        <div class="result-role">Recommended: {exp_level}</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {confidence}%"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Line chart
                df = pd.DataFrame(proj)
                df["Predicted Average ($)"] = df["predicted_salary"].apply(lambda x: x["average"])
                df["Confidence Score (%)"] = df["confidence"].apply(lambda x: x["score"])
                
                display_df = df[["year_offset", "experience_level", "Predicted Average ($)", "growth_from_current_pct", "Confidence Score (%)"]]
                st.line_chart(data=display_df, x="year_offset", y="Predicted Average ($)", use_container_width=True)

            # Top Recommended Title Leaps
            st.markdown('<div class="section-title">Top Recommended Title Leaps</div>', unsafe_allow_html=True)
            df_recs = pd.DataFrame(rep["top_3_new_roles"])
            if not df_recs.empty:
                df_recs["Projected Salary"] = df_recs["predicted_salary"].apply(lambda x: f"${x['average']:,.0f}")
                st.dataframe(df_recs[["role", "change_pct", "Projected Salary"]], use_container_width=True)
            
        except Exception as e:
             st.error(f"Generative projection mapping encountered an error: {e}")
else:
    # Empty state
    st.markdown('''
    <div class="empty-state-container">
        <svg class="timeline-illustration" width="200" height="60" viewBox="0 0 200 60">
            <circle cx="30" cy="30" r="8" fill="none" stroke="#22d3ee" stroke-width="2"/>
            <circle cx="100" cy="30" r="8" fill="none" stroke="#22d3ee" stroke-width="2"/>
            <circle cx="170" cy="30" r="8" fill="none" stroke="#22d3ee" stroke-width="2"/>
            <line x1="38" y1="30" x2="92" y2="30" stroke="rgba(34,211,238,0.3)" stroke-width="2"/>
            <line x1="108" y1="30" x2="162" y2="30" stroke="rgba(34,211,238,0.3)" stroke-width="2"/>
        </svg>
        <div class="empty-state-title">Run a simulation to see your career trajectory</div>
        <div class="empty-state-subtitle">Salary projections for +1, +3, and +5 years will appear here</div>
        <div class="milestone-cards">
            <div class="milestone-card">
                <div class="milestone-year">+1 Year</div>
                <div class="milestone-salary">—</div>
                <div class="milestone-role">—</div>
            </div>
            <div class="milestone-card">
                <div class="milestone-year">+3 Years</div>
                <div class="milestone-salary">—</div>
                <div class="milestone-role">—</div>
            </div>
            <div class="milestone-card">
                <div class="milestone-year">+5 Years</div>
                <div class="milestone-salary">—</div>
                <div class="milestone-role">—</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
