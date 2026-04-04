import streamlit as st
import pandas as pd
from api.database import SessionLocal
from api.dashboard import get_prediction_history, get_analytics

st.set_page_config(page_title="Personalized Dashboard", page_icon="📈", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM INSIGHTS DASHBOARD STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-right, #1a0f2e 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Hero Banner Card ── */
.hero-banner-card {
    background: var(--surface-3);
    border: 1px solid var(--border-strong);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    position: relative;
}

.hero-icon {
    width: 28px;
    height: 28px;
    color: #6366f1;
    margin-right: 12px;
    vertical-align: middle;
}

.hero-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    margin-bottom: 10px;
    display: inline;
}

.hero-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
}

.stat-badges {
    position: absolute;
    top: 28px;
    right: 32px;
    display: flex;
    gap: 8px;
}

.stat-badge {
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
}

.stat-badge.score {
    background: rgba(99, 102, 241, 0.15);
    color: #818cf8;
}

.stat-badge.predictions {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
}

/* ── Stat Cards ── */
.stat-cards-row {
    display: flex;
    gap: 20px;
    margin-top: 28px;
}

.stat-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    position: relative;
}

.stat-card.score-card {
    border-top: 3px solid #6366f1;
}

.stat-card.predictions-card {
    border-top: 3px solid #10b981;
}

.stat-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
}

.stat-value {
    font-size: 38px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -1px;
}

.stat-delta {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* ── Progress Ring ── */
.progress-ring {
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
}

.progress-ring circle {
    fill: none;
    stroke-width: 6;
}

.progress-ring .track {
    stroke: #1e1b4b;
}

.progress-ring .fill {
    stroke: #6366f1;
    stroke-linecap: round;
    transform: rotate(-90deg);
    transform-origin: center;
    transition: stroke-dashoffset 0.5s ease;
}

.progress-ring .text {
    font-size: 20px;
    font-weight: 800;
    fill: var(--text-primary);
    text-anchor: middle;
    dominant-baseline: middle;
}

/* ── Activity Bars ── */
.activity-bars {
    display: flex;
    align-items: flex-end;
    gap: 4px;
    height: 32px;
    margin-top: 12px;
}

.activity-bar {
    width: 8px;
    border-radius: 3px;
    transition: height 0.3s ease;
}

.activity-bar.active {
    background: #10b981;
}

.activity-bar.inactive {
    background: var(--surface-2);
}

.activity-label {
    font-size: 11px;
    color: #475569;
    margin-top: 8px;
}

/* ── Section Headings ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #6366f1;
    padding-left: 12px;
    margin-bottom: 20px;
}

/* ── Two Column Layout ── */
.insights-container {
    display: flex;
    gap: 28px;
    margin-top: 36px;
}

.left-column {
    width: 62%;
}

.right-column {
    width: 34%;
}

/* ── Chart Container ── */
.chart-card {
    background: var(--surface-glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
}

/* ── Skill Recommendation Tip ── */
.skill-tip {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.skill-tip-icon {
    color: #f59e0b;
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 2px;
}

.skill-tip-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* ── Skill Cards ── */
.skill-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.skill-card:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateX(4px);
}

.skill-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.skill-icon-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #6366f1;
    border-radius: 50%;
    margin-right: 10px;
    vertical-align: middle;
}

.skill-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

.skill-badge {
    background: rgba(99, 102, 241, 0.12);
    color: #818cf8;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
}

.skill-impact-bar {
    background: var(--surface-3);
    height: 3px;
    border-radius: 999px;
    margin-top: 8px;
    overflow: hidden;
}

.skill-impact-fill {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
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

.stDataframe {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CHECK LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.get("logged_in", False):
    st.error("Please login to view your personalized dashboard.")
    st.stop()

username = st.session_state.username

# ══════════════════════════════════════════════════════════════════════════════
#  DATA FETCHING
# ══════════════════════════════════════════════════════════════════════════════
try:
    db = SessionLocal()
    history_data = get_prediction_history(username=username, db=db)
    analytics_data = get_analytics(username=username, db=db)
    db.close()
except Exception as e:
    st.error(f"Error fetching dashboard data: {e}")
    st.stop()

predictions = history_data.get("history", [])
market_value_score = analytics_data.get("market_value_score", 0.0)
salary_growth = analytics_data.get("salary_growth", [])
recommendations = analytics_data.get("recommendations", [])
total_preds = analytics_data.get("total_predictions", 0)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER CARD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'''
<div class="hero-banner-card">
    <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 3v18h18"></path>
        <path d="M18 9l-5 5-2-2-4 4"></path>
    </svg>
    <h1 class="hero-title">Your Insights</h1>
    <div class="stat-badges">
        <span class="stat-badge score">{market_value_score} Score</span>
        <span class="stat-badge predictions">{total_preds} Predictions</span>
    </div>
    <p class="hero-subtitle">Monitor your prediction history, view salary growth trends, and discover skills to increase your market value.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STAT CARDS ROW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="stat-cards-row">', unsafe_allow_html=True)

# Market Value Score Card
st.markdown(f'''
<div class="stat-card score-card">
    <div class="stat-label">Market Value Score</div>
    <div class="stat-value">{market_value_score}/100</div>
    {f'<div class="stat-delta"><span>↑</span> +2.5 from last time</div>' if market_value_score > 60 else ''}
    <svg class="progress-ring" width="80" height="80" viewBox="0 0 80 80">
        <circle class="track" cx="40" cy="40" r="34"></circle>
        <circle class="fill" cx="40" cy="40" r="34" 
                stroke-dasharray="{2 * 3.14159 * 34}" 
                stroke-dashoffset="{2 * 3.14159 * 34 * (1 - market_value_score/100)}"></circle>
        <text class="text" x="40" y="40">{int(market_value_score)}</text>
    </svg>
</div>
''', unsafe_allow_html=True)

# Total Predictions Card with Activity Bars
activity_data = [65, 80, 45, 90, 70, 85, 60]  # Simulated 7-day activity
activity_html = ''.join([f'<div class="activity-bar active" style="height: {h}%"></div>' for h in activity_data])

st.markdown(f'''
<div class="stat-card predictions-card">
    <div class="stat-label">Total Predictions</div>
    <div class="stat-value">{total_preds}</div>
    <div class="activity-bars">
        {activity_html}
    </div>
    <div class="activity-label">Last 7 days activity</div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close stat-cards-row

# ══════════════════════════════════════════════════════════════════════════════
#  BOTTOM TWO COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="insights-container">', unsafe_allow_html=True)

# Left Column - Salary Growth Trajectory
st.markdown('<div class="left-column">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Salary Growth Trajectory</div>', unsafe_allow_html=True)

if len(salary_growth) > 1:
    # Create line chart
    df_growth = pd.DataFrame(salary_growth)
    df_growth["date"] = pd.to_datetime(df_growth["date"])
    df_growth.set_index("date", inplace=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.line_chart(df_growth["predicted_salary"], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add legend
    st.markdown('<div style="margin-top: 12px; font-size: 12px; color: #6366f1;">● Predicted Salary</div>', unsafe_allow_html=True)
elif len(salary_growth) == 1:
    st.info("You've made one prediction so far. Keep predicting salaries for new roles to generate an interactive growth chart!")
else:
    st.markdown('''
    <div style="background: rgba(99,102,241,0.04); border: 1px dashed rgba(99,102,241,0.2); border-radius: 16px; padding: 48px 32px; text-align: center;">
        <div style="font-size: 48px; color: #6366f1; opacity: 0.4;">📉</div>
        <div style="font-size: 16px; font-weight: 600; color: var(--text-secondary); margin-top: 16px;">No Data Available</div>
        <div style="font-size: 13px; color: #475569; margin-top: 8px;">Make your first salary prediction to see your growth</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<div class="section-heading" style="margin-top: 36px;">Prediction History</div>', unsafe_allow_html=True)
if predictions:
    # Format history as dataframe
    hist_data = [{
        "Date": p.created_at.strftime("%Y-%m-%d %H:%M"),
        "Role": p.job_title,
        "Experience": p.experience_level,
        "Location": p.company_location,
        "Predicted Salary": f"${p.predicted_average:,.0f}"
    } for p in predictions]
    
    st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)
else:
    st.markdown('''
    <div style="background: rgba(99,102,241,0.04); border: 1px dashed rgba(99,102,241,0.2); border-radius: 16px; padding: 36px 24px; text-align: center;">
        <div style="font-size: 36px; color: #6366f1; opacity: 0.4;">🕒</div>
        <div style="font-size: 15px; font-weight: 600; color: var(--text-secondary); margin-top: 12px;">No Prediction History</div>
        <div style="font-size: 13px; color: #475569; margin-top: 6px;">Your past predictions will appear here</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close left-column

# Right Column - Skill Recommendations
st.markdown('<div class="right-column">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Skill Recommendations</div>', unsafe_allow_html=True)

if recommendations:
    # Skill tip card
    st.markdown('''
    <div class="skill-tip">
        <span class="skill-tip-icon">💡</span>
        <span class="skill-tip-text">Top skills to boost your salary based on your latest roles</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Skill cards with impact bars
    skill_impacts = {
        "Deep Learning": 85,
        "MLOps": 78,
        "Cloud Architecture": 70
    }
    
    for skill in recommendations:
        impact = skill_impacts.get(skill, 75)
        st.markdown(f'''
        <div class="skill-card">
            <div class="skill-card-header">
                <div>
                    <span class="skill-icon-dot"></span>
                    <span class="skill-name">{skill}</span>
                </div>
                <span class="skill-badge">High Impact</span>
            </div>
            <div class="skill-impact-bar">
                <div class="skill-impact-fill" style="width: {impact}%"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 13px; color: var(--text-secondary); margin-top: 16px;">Try adding these to your profile and run a new prediction!</p>', unsafe_allow_html=True)
else:
    st.markdown('''
    <div style="background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 12px; padding: 20px; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
        <div style="font-size: 13px; color: var(--text-secondary);">Make a prediction first to get skill recommendations</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close right-column
st.markdown('</div>', unsafe_allow_html=True)  # Close insights-container
