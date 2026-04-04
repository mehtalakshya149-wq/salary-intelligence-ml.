import streamlit as st
from ml.src.predict import run_prediction

st.set_page_config(page_title="What-If Simulator", page_icon="🎛️", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CAREER SIMULATOR STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-left, #0a1f1a 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

/* ── Page Header ── */
.simulator-header {
    background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.06));
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 28px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-icon {
    width: 28px;
    height: 28px;
    color: #10b981;
}

.header-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
    margin-top: 8px;
}

.live-badge {
    background: rgba(16,185,129,0.15);
    color: #10b981;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
    animation: live-pulse 1.5s ease infinite;
}

@keyframes live-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Two Column Layout ── */
.two-column-layout {
    display: flex;
    gap: 36px;
}

.left-column {
    width: 38%;
}

.right-column {
    width: 58%;
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

.section-description {
    font-size: 13px;
    color: #475569;
    line-height: 1.6;
    margin-bottom: 24px;
}

/* ── Field Label ── */
.field-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ── Input & Selectbox Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stSlider > div > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #0d3326 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    padding: 0 !important;
}

.stSelectbox > div > div:hover {
    border-color: #10b981 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Slider Styling ── */
.slider-track {
    height: 6px;
    border-radius: 999px;
    background: #0f2d24;
}

.slider-fill {
    background: linear-gradient(90deg, #10b981, #06b6d4);
}

.slider-ticks {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #475569;
    margin-top: 8px;
}

/* ── Skill Pills ── */
.skill-pills {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
}

.skill-pill {
    background: rgba(16,185,129,0.1);
    color: #10b981;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
}

/* ── Result Card ── */
.salary-result-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.08));
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 16px;
    position: relative;
}

.salary-label {
    font-size: 11px;
    font-weight: 600;
    color: #10b981;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.live-indicator {
    color: #10b981;
    font-size: 10px;
    font-weight: 600;
    animation: live-pulse 1.5s ease infinite;
}

.salary-value {
    font-size: 48px;
    font-weight: 900;
    color: var(--text-primary);
    letter-spacing: -2px;
    margin-top: 8px;
    text-shadow: 0 0 40px rgba(16,185,129,0.3);
}

.change-indicator {
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
}

.change-positive {
    color: #10b981;
}

.change-negative {
    color: #ef4444;
}

.salary-timestamp {
    position: absolute;
    bottom: 12px;
    right: 16px;
    font-size: 11px;
    color: #475569;
}

/* ── Band Cards ── */
.band-cards {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

.band-card {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 20px;
    flex: 1;
}

.band-card-low {
    border-top: 2px solid #ef4444;
}

.band-card-inflation {
    border-top: 2px solid #f59e0b;
}

.band-card-high {
    border-top: 2px solid #10b981;
}

.band-label {
    font-size: 10px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.band-value-low {
    font-size: 20px;
    font-weight: 800;
    color: #ef4444;
    margin-top: 4px;
}

.band-value-inflation {
    font-size: 20px;
    font-weight: 800;
    color: #f59e0b;
    margin-top: 4px;
}

.band-value-high {
    font-size: 20px;
    font-weight: 800;
    color: #10b981;
    margin-top: 4px;
}

.band-sublabel {
    font-size: 10px;
    color: #475569;
    margin-top: 4px;
}

/* ── Confidence Card ── */
.confidence-card {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 12px;
}

.confidence-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.confidence-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
}

.confidence-value {
    font-size: 16px;
    font-weight: 800;
    color: #10b981;
}

.confidence-bar-bg {
    background: #0f2d24;
    height: 6px;
    border-radius: 999px;
    margin-top: 10px;
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #06b6d4);
    border-radius: 999px;
}

.confidence-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #475569;
    margin-top: 8px;
}

/* ── Disclaimer Card ── */
.disclaimer-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #475569;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.disclaimer-icon {
    color: var(--text-secondary);
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
}

.disclaimer-text {
    font-size: 12px;
    color: #475569;
    line-height: 1.6;
}

/* ── Hide Streamlit Elements ── */
.stSlider > div {
    padding: 0 !important;
}

.stSlider > div > div > div {
    margin: 0 !important;
}

/* ── Custom Slider Styling ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #10b981, #06b6d4) !important;
}

[data-testid="stSlider"] > div > div > div {
    background: #0f2d24 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div {
    background: #0f2d24 !important;
    height: 6px !important;
    border-radius: 999px !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [data-baseweb="thumb"] {
    width: 18px !important;
    height: 18px !important;
    background: var(--text-primary) !important;
    border: 3px solid #10b981 !important;
    border-radius: 50% !important;
    box-shadow: 0 0 8px rgba(16,185,129,0.5) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [data-baseweb="inner-thumb"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="simulator-header">
    <div>
        <div class="header-left">
            <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="4" y1="21" x2="4" y2="14"></line>
                <line x1="4" y1="10" x2="4" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12" y2="3"></line>
                <line x1="20" y1="21" x2="20" y2="16"></line>
                <line x1="20" y1="12" x2="20" y2="3"></line>
                <line x1="1" y1="14" x2="7" y2="14"></line>
                <line x1="9" y1="8" x2="15" y2="8"></line>
                <line x1="17" y1="16" x2="23" y2="16"></line>
            </svg>
            <div class="header-title">Career Simulator</div>
        </div>
        <div class="header-subtitle">Adjust your core levers like experience and skills to instantly recompute your market value prediction without manual submits.</div>
    </div>
    <div class="live-badge">
        <div class="live-dot"></div>
        Live
    </div>
</div>
''', unsafe_allow_html=True)

if not st.session_state.get("logged_in", False):
    st.error("Please login to use the What-If Simulator.")
    st.stop()

# Currency & Location Config
CURRENCY_MAP = {
    "US": {"symbol": "$", "rate": 1.0, "name": "United States"},
    "GB": {"symbol": "£", "rate": 0.8, "name": "United Kingdom"},
    "CA": {"symbol": "$", "rate": 1.35, "name": "Canada"},
    "DE": {"symbol": "€", "rate": 0.92, "name": "Germany"},
    "IN": {"symbol": "₹", "rate": 83.0, "name": "India"},
    "FR": {"symbol": "€", "rate": 0.92, "name": "France"},
    "ES": {"symbol": "€", "rate": 0.92, "name": "Spain"},
    "AU": {"symbol": "$", "rate": 1.5, "name": "Australia"},
    "BR": {"symbol": "R$", "rate": 5.0, "name": "Brazil"},
    "JP": {"symbol": "¥", "rate": 150.0, "name": "Japan"}
}

# ── TWO COLUMN LAYOUT ──
st.markdown('<div class="two-column-layout">', unsafe_allow_html=True)

# ── LEFT COLUMN: ADJUST LEVERS ──
st.markdown('<div class="left-column">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Adjust Levers</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Any change made here will instantly compute a new salary simulation.</div>', unsafe_allow_html=True)

# Job Title
st.markdown('<div class="field-label">Simulated Job Title</div>', unsafe_allow_html=True)
job_title = st.selectbox("", ["Data Scientist", "ML Engineer", "Data Analyst", "Data Engineer", "AI Researcher"], label_visibility="collapsed", key="sim_job")

# Experience Level
st.markdown('<div class="field-label">Experience Level</div>', unsafe_allow_html=True)
exp_options = ["EN", "MI", "SE", "EX"]
exp_labels = ["Entry", "Mid", "Senior", "Executive"]

# Create a custom experience selector
exp_col1, exp_col2 = st.columns([4, 1])
with exp_col1:
    exp_index = st.slider("", min_value=0, max_value=3, value=1, label_visibility="collapsed", key="sim_exp")
    exp = exp_options[exp_index]
with exp_col2:
    st.markdown(f'<div style="background: rgba(16,185,129,0.12); color: #10b981; border-radius: 6px; padding: 6px 12px; font-size: 13px; font-weight: 700; text-align: center; margin-top: 4px;">{exp_labels[exp_index]}</div>', unsafe_allow_html=True)

# Level labels below slider
st.markdown('<div style="display: flex; justify-content: space-between; font-size: 10px; color: #475569; margin-top: 4px;">', unsafe_allow_html=True)
st.markdown('<span>Entry</span><span>Mid</span><span>Senior</span><span>Executive</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Company Location
st.markdown('<div class="field-label" style="margin-top: 20px;">Company Location</div>', unsafe_allow_html=True)
loc_options = list(CURRENCY_MAP.keys())
loc_names = [CURRENCY_MAP[loc]["name"] for loc in loc_options]
loc_index = st.selectbox("", loc_names, index=0, label_visibility="collapsed", key="sim_loc")
loc = loc_options[loc_names.index(loc_index)]

# Remote Work Ratio
st.markdown('<div class="field-label" style="margin-top: 20px;">Remote Work Ratio (%)</div>', unsafe_allow_html=True)
rem = st.slider("", min_value=0, max_value=100, step=50, value=100, label_visibility="collapsed", key="sim_rem")
st.markdown('<div class="slider-ticks">', unsafe_allow_html=True)
st.markdown('<span>0%</span><span>50%</span><span>100%</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Skillset
st.markdown('<div class="field-label" style="margin-top: 20px;">Skillset</div>', unsafe_allow_html=True)
skills = st.text_area("", value="Python, SQL", label_visibility="collapsed", key="sim_skills", height=80)

# Show skill pills
if skills.strip():
    skills_list = [s.strip() for s in skills.split(',') if s.strip()]
    pills_html = ''.join([f'<span class="skill-pill">{skill}</span>' for skill in skills_list])
    st.markdown(f'<div class="skill-pills">{pills_html}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close left-column

# ── RIGHT COLUMN: REAL-TIME SIMULATION RESULT ──
st.markdown('<div class="right-column">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Real-Time Simulation Result</div>', unsafe_allow_html=True)
st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

# Get currency details
curr_symbol = CURRENCY_MAP[loc]["symbol"]
curr_rate = CURRENCY_MAP[loc]["rate"]

# Defaults
emp = "FT"
size = "M"
yr = 2024

inputs = {
    "job_title": job_title, 
    "experience_level": exp,
    "employment_type": emp, 
    "company_location": loc,
    "company_size": size, 
    "remote_ratio": rem,
    "skills": skills, 
    "work_year": int(yr)
}

if not job_title or not loc:
    st.markdown('''
    <div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(16,185,129,0.2); border-radius: 16px; padding: 48px 32px; text-align: center;">
        <div style="font-size: 36px; margin-bottom: 16px;">⏳</div>
        <div style="font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">Incomplete Data</div>
        <div style="font-size: 13px; color: var(--text-secondary);">Fill out the fields to instantly see the simulation.</div>
    </div>
    ''', unsafe_allow_html=True)
else:
    try:
        res = run_prediction(inputs, "ml/config.yaml")
        
        # Convert USD results to local currency
        median = res['salary']['average'] * curr_rate
        low = res['salary']['min'] * curr_rate
        high = res['salary']['max'] * curr_rate
        adj = res['inflation_adjusted']['adjusted'] * curr_rate
        
        # Main Salary Card
        st.markdown(f'''
        <div class="salary-result-card">
            <div class="salary-label">
                SIMULATED MEDIAN SALARY
                <span class="live-indicator">● LIVE</span>
            </div>
            <div class="salary-value">{curr_symbol}{median:,.0f}</div>
            <div class="salary-timestamp">Updated just now</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Band Cards
        st.markdown(f'''
        <div class="band-cards">
            <div class="band-card band-card-low">
                <div class="band-label">Low Band</div>
                <div class="band-value-low">{curr_symbol}{low:,.0f}</div>
                <div class="band-sublabel">10th Percentile</div>
            </div>
            <div class="band-card band-card-inflation">
                <div class="band-label">Inflation Adj (2025)</div>
                <div class="band-value-inflation">{curr_symbol}{adj:,.0f}</div>
                <div class="band-sublabel">2025 Adjusted</div>
            </div>
            <div class="band-card band-card-high">
                <div class="band-label">High Band</div>
                <div class="band-value-high">{curr_symbol}{high:,.0f}</div>
                <div class="band-sublabel">90th Percentile</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Confidence Card
        confidence_score = res['confidence']['score']
        st.markdown(f'''
        <div class="confidence-card">
            <div class="confidence-header">
                <span class="confidence-label">Confidence Score</span>
                <span class="confidence-value">{confidence_score}%</span>
            </div>
            <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: {confidence_score}%;"></div>
            </div>
            <div class="confidence-labels">
                <span>Low (0%)</span>
                <span>Medium (50%)</span>
                <span>High (100%)</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Disclaimer Card
        st.markdown('''
        <div class="disclaimer-card">
            <div class="disclaimer-icon">ℹ</div>
            <div class="disclaimer-text">This simulation relies purely on existing model weights and inference caching. No retraining has occurred during this computation.</div>
        </div>
        ''', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Inference error computing simulation: {e}")

st.markdown('</div>', unsafe_allow_html=True)  # Close right-column
st.markdown('</div>', unsafe_allow_html=True)  # Close two-column-layout
