import streamlit as st
import uuid
from ml.src.predict import run_prediction
from api.database import SessionLocal
from api.models import SalaryPrediction, ModelLog

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM SALARY PREDICTION ENGINE STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-left, var(--bg-app) 0%, var(--bg-app) 60%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 36px;
}

.header-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    max-width: 520px;
    line-height: 1.7;
}

/* ── Column Headings ── */
.column-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 24px;
    position: relative;
    padding-bottom: 12px;
}

/* ── Form Field Styling ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
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
.stNumberInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12) !important;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #3b82f6 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Labels ─ */
label[data-testid="stWidgetLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 6px !important;
}

/* ── Slider Styling ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
}

.stSlider > div > div > div {
    background: var(--surface-2) !important;
    height: 6px !important;
    border-radius: 999px !important;
}

/* ── Submit Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
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
}

.stButton > button:hover {
    filter: brightness(115%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4) !important;
}

/* ── Result Card ── */
.result-card {
    background: var(--surface-3);
    border: 1px solid var(--border-strong);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 20px;
}

.result-value {
    font-size: 40px;
    font-weight: 800;
    color: var(--text-primary);
    text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
}

/* ── Empty State ── */
.empty-state-card {
    background: var(--bg-surface);
    border: 1px dashed var(--border);
    border-radius: 16px;
    padding: 40px 32px;
    text-align: center;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="page-header">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" style="margin-bottom: 12px;">
        <path d="M12 2a7 7 0 0 1 7 7c0 2.38-1.19 4.47-3 5.74V17a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2v-2.26C6.19 13.47 5 11.38 5 9a7 7 0 0 1 7-7z"></path>
        <path d="M9 21h6"></path>
        <path d="M10 17v4"></path>
        <path d="M14 17v4"></path>
    </svg>
    <h1 class="header-title">Salary Prediction Engine</h1>
    <p class="header-subtitle">Use the advanced RandomForest / Gradient Boosting ensemble to calculate highly accurate benchmarks.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([45, 55], gap="large")

with col1:
    st.markdown('<div class="column-heading">Job Parameters</div>', unsafe_allow_html=True)
    
    job_title = st.text_input("Job Title", value="Data Scientist")
    exp = st.selectbox("Experience Level", ["SE - Senior", "MI - Mid", "EN - Entry", "EX - Executive"], index=0)
    emp = st.selectbox("Employment Type", ["FT - Full Time", "PT - Part Time", "CT - Contract", "FL - Freelance"], index=0)
    loc = st.text_input("Employee Residence", value="US")
    size = st.selectbox("Company Size", ["L - Large", "M - Medium", "S - Small"], index=0)
    rem = st.slider("Remote Ratio", min_value=0, max_value=100, value=100, step=50)
    skills = st.text_input("Required Skills", value="Python, SQL, Machine Learning")
    yr = st.number_input("Work Year", min_value=2020, max_value=2030, value=2024)
    predict_btn = st.button("⚡ Run Prediction", type="primary", use_container_width=True)

with col2:
    st.markdown('<div class="column-heading" style="color: #8b5cf6;">Intelligence Output</div>', unsafe_allow_html=True)
    
    if predict_btn:
        # Map display values back to codes
        exp_map = {"SE - Senior": "SE", "MI - Mid": "MI", "EN - Entry": "EN", "EX - Executive": "EX"}
        emp_map = {"FT - Full Time": "FT", "PT - Part Time": "PT", "CT - Contract": "CT", "FL - Freelance": "FL"}
        size_map = {"L - Large": "L", "M - Medium": "M", "S - Small": "S"}
        
        with st.spinner("Running ensemble models..."):
            try:
                inputs = {
                    "job_title": job_title,
                    "experience_level": exp_map[exp],
                    "employment_type": emp_map[emp],
                    "company_location": loc,
                    "company_size": size_map[size],
                    "remote_ratio": rem,
                    "skills": skills,
                    "work_year": int(yr)
                }
                res = run_prediction(inputs, "ml/config.yaml")

                # Store prediction in DB
                try:
                    db = SessionLocal()
                    from api.models import User
                    u = db.query(User).filter(User.username == st.session_state.username).first()
                    if u:
                        sp = SalaryPrediction(
                            id=str(uuid.uuid4()),
                            user_id=u.id,
                            job_title=job_title,
                            experience_level=exp_map[exp],
                            company_location=loc,
                            company_size=size_map[size],
                            remote_ratio=rem,
                            skills=skills,
                            predicted_average=res['salary']['average'],
                            confidence_score=float(res['confidence']['score'])
                        )
                        db.add(sp)
                        
                        # Log Prediction Activity
                        pred_log = ModelLog(user_id=u.id, action=f"Prediction: {job_title}", endpoint="UI/Predict")
                        db.add(pred_log)
                        
                        db.commit()
                    db.close()
                except Exception as db_e:
                    st.toast(f"Silent logger warning: {db_e}")

                # Display results
                st.markdown(f'''
                <div class="result-card">
                    <div style="font-size: 11px; color: #8b5cf6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; font-weight: 600;">Predicted Annual Salary (USD)</div>
                    <div class="result-value">${res['salary']['average']:,.0f}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Low Estimate (P10)", f"${res['salary']['min']:,.0f}")
                c2.metric("Median Average", f"${res['salary']['average']:,.0f}")
                c3.metric("High Estimate (P90)", f"${res['salary']['max']:,.0f}")

                # Confidence score
                score = float(res['confidence']['score'])
                label = res['confidence']['label']
                adj = res['inflation_adjusted']['adjusted']

                conf_col1, conf_col2 = st.columns([1, 1.3])
                with conf_col1:
                    st.metric("Confidence Score", f"{score:.1f}%", delta=label)
                with conf_col2:
                    st.success(f"**Inflation Adjusted Projection (2024):** ${adj:,.0f}")

            except Exception as e:
                st.error(f"Prediction failed: Ensure models are thoroughly trained: {e}")
    else:
        st.markdown('''
        <div class="empty-state-card">
            <div style="font-size: 36px; color: #8b5cf6; margin-bottom: 12px;">✨</div>
            <div style="font-size: 14px; color: #475569;">Run prediction to see salary insights</div>
        </div>
        ''', unsafe_allow_html=True)
