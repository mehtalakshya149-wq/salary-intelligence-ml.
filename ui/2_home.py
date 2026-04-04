import streamlit as st
from ml.src.salary_trends import get_trend_report
import pandas as pd

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM DASHBOARD STYLING
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

/* ── Top Navigation Bar ── */
.navbar {
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
}

.navbar-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.3px;
}

.logout-btn {
    background: transparent;
    border: 1px solid #ef4444;
    color: #ef4444;
    border-radius: 8px;
    padding: 7px 18px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Sora', sans-serif;
    cursor: pointer;
    transition: all 0.2s ease;
}

.logout-btn:hover {
    background: #ef4444;
    color: var(--text-primary);
}

/* ── Glowing Orb ── */
.glowing-orb {
    position: absolute;
    top: -100px;
    left: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(26, 75, 189, 0.09) 0%, transparent 70%);
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
}

/* ── Main Content Container ── */
.dashboard-content {
    position: relative;
    z-index: 1;
    padding: 32px 24px;
}

/* ── Welcome Section ── */
.welcome-section {
    margin-top: 32px;
    margin-bottom: 32px;
}

.welcome-title {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.welcome-highlight {
    color: #3b82f6;
}

.welcome-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
}

/* ── Stats Cards Grid ── */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 48px;
}

.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    position: relative;
    transition: all 0.2s ease;
    overflow: hidden;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.stat-card.card-blue {
    border-top: 3px solid #3b82f6;
}

.stat-card.card-green {
    border-top: 3px solid #10b981;
}

.stat-card.card-purple {
    border-top: 3px solid #8b5cf6;
}

.stat-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 20px;
}

.stat-card.card-blue .stat-icon {
    color: #3b82f6;
}

.stat-card.card-green .stat-icon {
    color: #10b981;
}

.stat-card.card-purple .stat-icon {
    color: #8b5cf6;
}

.stat-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 32px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

/* ── Section Title ── */
.section-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 48px;
    margin-bottom: 16px;
    border-left: 3px solid #3b82f6;
    padding-left: 14px;
}

/* ── Data Table Container ── */
.table-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Hide backup logout button */
button[key="logout_backup"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
    <div class="navbar-title">🏠 Platform Overview</div>
    <button class="logout-btn" onclick="document.getElementById('logout-hidden-btn').click()">Logout</button>
</div>
""", unsafe_allow_html=True)

# Hidden logout button (triggered by navbar button)
logout_clicked = st.button("", key="logout-hidden-btn", type="secondary")
if logout_clicked:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD CONTENT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="glowing-orb"></div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)

# Welcome Section
username = st.session_state.get('username', 'User')
st.markdown(f'''
<div class="welcome-section">
    <div class="welcome-title">Welcome back, <span class="welcome-highlight">{username}</span>!</div>
    <div class="welcome-subtitle">Here is the live status of the Salary AI models.</div>
</div>
''', unsafe_allow_html=True)

# Load Data
report = None
try:
    with st.spinner("Loading dataset trends..."):
        report = get_trend_report("ml/config.yaml")
except Exception as e:
    st.warning("Failed to load aggregate stats. Ensure pipeline data exists in `ml/data/processed/salaries_clean.csv`.")
    st.error(f"Details: {e}")

if report:
    try:
        summary = report["data_summary"]
        yearly_stats = report["yearly_stats"]
        
        # Convert list of dicts to DataFrame if needed
        if isinstance(yearly_stats, list):
            df = pd.DataFrame(yearly_stats)
        else:
            df = yearly_stats.copy()
        
        # Stats Cards
        st.markdown(f'''
        <div class="stats-grid">
            <div class="stat-card card-blue">
                <div class="stat-icon">📊</div>
                <div class="stat-label">Total Extracted Records</div>
                <div class="stat-value">{summary['total_records']:,}</div>
            </div>
            <div class="stat-card card-green">
                <div class="stat-icon">💰</div>
                <div class="stat-label">Median Machine Salary</div>
                <div class="stat-value">${summary['overall_median']:,.0f}</div>
            </div>
            <div class="stat-card card-purple">
                <div class="stat-icon">📅</div>
                <div class="stat-label">Data Range</div>
                <div class="stat-value">{summary["year_range"]}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Section Title
        st.markdown('<div class="section-title">Aggregate Yearly Data Trends</div>', unsafe_allow_html=True)
        
        # Build custom HTML table
        table_html = '<div class="table-container"><table style="width: 100%; border-collapse: collapse;">'
        
        # Header row
        table_html += '<thead><tr style="background: var(--surface-3);">'
        for col in df.columns:
            table_html += f'<th style="padding: 14px 20px; text-align: left; font-size: 12px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 1px solid var(--border);">{col}</th>'
        table_html += '</tr></thead>'
        
        # Data rows
        table_html += '<tbody>'
        for idx, row in df.iterrows():
            bg_color = 'var(--surface-glass)' if idx % 2 == 0 else 'transparent'
            table_html += f'<tr style="background: {bg_color}; transition: background 0.15s ease;" onmouseover="this.style.background=\'rgba(59,130,246,0.07)\'" onmouseout="this.style.background=\'{bg_color}\'">'
            
            for col_idx, col in enumerate(df.columns):
                value = row[col]
                
                # Format values based on column
                if col == 'work_year':
                    cell_value = str(int(value)) if pd.notna(value) else 'None'
                    align = 'left'
                elif col in ['count']:
                    cell_value = f"{int(value):,}" if pd.notna(value) else 'None'
                    align = 'right'
                elif col in ['mean', 'median', 'std', 'p10', 'p90']:
                    cell_value = f"{value:,.2f}" if pd.notna(value) else 'None'
                    align = 'right'
                elif col == 'yoy_growth_pct':
                    if pd.isna(value) or value == 'None':
                        cell_value = '<span style="color: #475569; font-style: italic;">None</span>'
                        align = 'right'
                    else:
                        if value > 0:
                            cell_value = f'<span style="color: #10b981; font-weight: 600;">{value:.2f}</span>'
                        elif value < 0:
                            cell_value = f'<span style="color: #ef4444; font-weight: 600;">{value:.2f}</span>'
                        else:
                            cell_value = f'<span style="color: var(--text-secondary);">{value:.2f}</span>'
                        align = 'right'
                else:
                    cell_value = str(value) if pd.notna(value) else 'None'
                    align = 'left'
                
                table_html += f'<td style="padding: 14px 20px; font-size: 14px; color: var(--text-primary); border-bottom: 1px solid var(--border); text-align: {align};">{cell_value}</td>'
            
            table_html += '</tr>'
        table_html += '</tbody></table></div>'
        
        st.markdown(table_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning("Failed to load aggregate stats. Ensure pipeline data exists in `ml/data/processed/salaries_clean.csv`.")
        st.error(f"Details: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Backup logout button (hidden, just in case navbar JS doesn't work)
if st.button("Logout", key="logout_backup", type="secondary"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()
