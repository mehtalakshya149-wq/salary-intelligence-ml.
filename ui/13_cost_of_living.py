import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api.cost_of_living import get_cost_of_living_adjusted_salary, COST_OF_LIVING_INDICES

st.set_page_config(page_title="Cost of Living Adjuster", page_icon="🌍", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM GLOBAL MOBILITY STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-left, #001a3d 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

/* ── Page Header ── */
.mobility-header {
    background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(14,165,233,0.06));
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 32px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-icon {
    width: 28px;
    height: 28px;
    color: #38bdf8;
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

.ppp-badge {
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
    border-radius: 999px;
    padding: 4px 14px;
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
    border-left: 3px solid #38bdf8;
    padding-left: 12px;
    margin-bottom: 20px;
}

/* ── Input Section ── */
.input-row {
    display: flex;
    gap: 24px;
    margin-bottom: 32px;
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
}

.salary-input-container {
    position: relative;
}

.salary-prefix {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #38bdf8;
    font-size: 16px;
    font-weight: 700;
    z-index: 1;
}

.salary-input {
    background: var(--surface-2);
    border: 1px solid #0c2a3d;
    border-radius: 10px;
    padding: 8px 80px 8px 40px;
    color: var(--text-primary);
    font-size: 18px;
    font-weight: 700;
    font-family: 'Sora', sans-serif;
    width: 100%;
    transition: all 0.2s ease;
    line-height: normal !important;
}

.salary-input:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12);
    outline: none;
}

.salary-buttons {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    gap: 4px;
}

.salary-btn {
    background: var(--surface-2);
    border: 1px solid var(--border);
    width: 36px;
    height: 36px;
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 18px;
    font-weight: 300;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.salary-btn:hover {
    border-color: #38bdf8;
    color: #38bdf8;
}

/* ── Quick Select Pills ── */
.quick-select-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.quick-select-pill {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-select-pill:hover,
.quick-select-pill.active {
    background: rgba(56,189,248,0.12);
    color: #38bdf8;
    border-color: rgba(56,189,248,0.3);
}

/* ── Dropdown Styling ── */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #0c2a3d !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #38bdf8 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Purchasing Power Section ── */
.pp-heading {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    border-left: 3px solid #38bdf8;
    padding-left: 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.pp-description {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 20px;
}

.pp-highlight {
    color: #38bdf8;
    font-weight: 700;
}

.pp-highlight-white {
    color: var(--text-primary);
    font-weight: 700;
}

/* ── Chart Container ── */
.chart-container {
    background: var(--bg-app);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    padding: 24px;
    margin-bottom: 20px;
}

.chart-legend {
    display: flex;
    gap: 20px;
    margin-top: 16px;
    font-size: 11px;
    color: var(--text-secondary);
}

/* ── Sort Controls ── */
.sort-controls {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.sort-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 600;
}

.sort-pills {
    display: flex;
    gap: 8px;
}

.sort-pill {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.sort-pill.active {
    background: rgba(56,189,248,0.12);
    border-color: rgba(56,189,248,0.3);
    color: #38bdf8;
    font-weight: 600;
}

.sort-pill:hover {
    border-color: rgba(56,189,248,0.2);
}

/* ── Country Cards Grid ── */
.country-cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.country-card {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 24px;
    transition: all 0.2s ease;
}

.country-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    border-color: rgba(56,189,248,0.2);
}

.country-card-positive {
    border-top: 2px solid #10b981;
}

.country-card-negative {
    border-top: 2px solid #ef4444;
}

.country-name {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.country-salary {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin-top: 6px;
}

.pp-badge-card {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
}

.pp-badge-positive {
    background: rgba(16,185,129,0.12);
    color: #10b981;
}

.pp-badge-negative {
    background: rgba(239,68,68,0.1);
    color: #ef4444;
}

.pp-bar-track {
    background: var(--surface-2);
    height: 4px;
    border-radius: 999px;
    margin-top: 12px;
    overflow: hidden;
}

.pp-bar-fill-positive {
    background: #10b981;
    height: 100%;
    border-radius: 999px;
}

.pp-bar-fill-negative {
    background: #ef4444;
    height: 100%;
    border-radius: 999px;
}

.vs-label {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
}

/* ── Hide Streamlit Number Input Arrows ── */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="mobility-header">
    <div>
        <div class="header-left">
            <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
            <div class="header-title">Global Mobility</div>
        </div>
        <div class="header-subtitle">Convert your current salary across global tech hubs to understand true purchasing power and evaluate international offers.</div>
    </div>
    <div class="ppp-badge">PPP Adjusted</div>
</div>
''', unsafe_allow_html=True)

if not st.session_state.get("logged_in", False):
    st.error("Please login to access the Cost of Living tools.")
    st.stop()

# ── INPUT SECTION ──
st.markdown('<div class="section-heading">Input Current Conditions</div>', unsafe_allow_html=True)

countries = list(COST_OF_LIVING_INDICES.keys())

# Initialize session state for inputs
if 'base_salary' not in st.session_state:
    st.session_state.base_salary = 120000
if 'base_country' not in st.session_state:
    st.session_state.base_country = "United States"

# Two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="field-label">Base Salary (Annual USD)</div>', unsafe_allow_html=True)
    
    # Salary input with +/- buttons
    salary_change = st.number_input(
        "",
        min_value=10000,
        max_value=2000000,
        value=st.session_state.base_salary,
        step=5000,
        label_visibility="collapsed",
        key="salary_input"
    )
    st.session_state.base_salary = salary_change
    
    # Quick select pills
    quick_salaries = [80000, 100000, 120000, 150000, 200000]
    st.markdown('<div class="quick-select-row">', unsafe_allow_html=True)
    for qs in quick_salaries:
        is_active = "active" if qs == salary_change else ""
        st.markdown(f'<div class="quick-select-pill {is_active}" onclick="document.querySelector(\'input[aria-label=""]\').value={qs};">${qs//1000}k</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="field-label">Current Location</div>', unsafe_allow_html=True)
    st.session_state.base_country = st.selectbox(
        "",
        options=countries,
        index=countries.index(st.session_state.base_country),
        label_visibility="collapsed",
        key="country_select"
    )

# Get calculations
try:
    data = get_cost_of_living_adjusted_salary(st.session_state.base_salary, st.session_state.base_country)
    comparisons = data.comparisons
except Exception as e:
    st.error(f"Computation Error: {e}")
    st.stop()

# ── PURCHASING POWER SECTION ──
st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)
st.markdown(f'''
<div class="pp-heading">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="2" y1="12" x2="22" y2="12"></line>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>
    Real Purchasing Power Equivalence
</div>
<div class="pp-description">
The chart below illustrates the exact salary you would need in each country to maintain the same lifestyle that <span class="pp-highlight">${st.session_state.base_salary:,.0f}</span> provides in <span class="pp-highlight-white">{st.session_state.base_country}</span>.
</div>
''', unsafe_allow_html=True)

# Prepare dataframe for charting
df = pd.DataFrame([{
    "Country": c.target_country,
    "Salary Required": c.target_salary_required,
    "PP_Ratio": c.purchasing_power_ratio
} for c in comparisons])

# Add the base country for visual reference
df.loc[len(df)] = {"Country": f"{st.session_state.base_country} (Base)", "Salary Required": st.session_state.base_salary, "PP_Ratio": 1.0}

# Create custom bar chart with smart colors
fig = go.Figure()

for idx, row in df.iterrows():
    # Determine color based on purchasing power
    if "Base" in row['Country']:
        color = '#38bdf8'  # Blue for baseline
    elif row['PP_Ratio'] > 1:
        color = '#10b981'  # Green for higher PP (cheaper country)
    else:
        color = '#ef4444'  # Red for lower PP (more expensive)
    
    fig.add_trace(go.Bar(
        x=[row['Country']],
        y=[row['Salary Required']],
        marker_color=color,
        hovertemplate=f'<b>{row["Country"]}</b><br>' +
                      f'Salary: ${{row["Salary Required"]:,.0f}}<br>' +
                      f'PP Ratio: {row["PP_Ratio"]:.2f}<extra></extra>'
    ))

fig.update_layout(
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(family='Sora', size=11, color='var(--text-secondary)'),
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)'
    ),
    yaxis=dict(
        tickfont=dict(family='Sora', size=11, color='#475569'),
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)',
        title='Salary Required (USD)'
    ),
    plot_bgcolor='var(--bg-app)',
    paper_bgcolor='var(--bg-app)',
    margin=dict(l=60, r=20, t=20, b=100),
    height=400,
    bargap=0.3,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Chart legend
st.markdown('''
<div class="chart-legend">
    <span>🟢 Higher purchasing power</span>
    <span>🔴 Lower purchasing power</span>
    <span>🔵 Your baseline</span>
</div>
''', unsafe_allow_html=True)

# ── COUNTRY DETAIL BREAKDOWN ──
st.markdown('<div class="section-heading" style="margin-top: 36px;">Country Detail Breakdown</div>', unsafe_allow_html=True)

# Sort controls
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = 'salary'

st.markdown('<div class="sort-controls">', unsafe_allow_html=True)
st.markdown('<span class="sort-label">Sort by:</span>', unsafe_allow_html=True)

sort_options = [
    ('salary', 'Salary ↓'),
    ('pp', 'Purchasing Power ↓'),
    ('alpha', 'Alphabetical')
]

st.markdown('<div class="sort-pills">', unsafe_allow_html=True)
for sort_key, sort_label in sort_options:
    is_active = "active" if st.session_state.sort_by == sort_key else ""
    st.markdown(f'<div class="sort-pill {is_active}" onclick="document.getElementById(\'sort-{sort_key}\').click();">{sort_label}</div>', unsafe_allow_html=True)
    st.button("", key=f"sort-{sort_key}", on_click=lambda k=sort_key: st.session_state.update(sort_by=k), type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sort comparisons based on selection
sorted_comparisons = comparisons.copy()
if st.session_state.sort_by == 'pp':
    sorted_comparisons.sort(key=lambda x: x.purchasing_power_ratio, reverse=True)
elif st.session_state.sort_by == 'alpha':
    sorted_comparisons.sort(key=lambda x: x.target_country)

# Country cards grid (3 columns)
st.markdown('<div class="country-cards-grid">', unsafe_allow_html=True)

for comp in sorted_comparisons:
    # Calculate purchasing power percentage
    pp_percent = (comp.purchasing_power_ratio - 1) * 100
    is_positive = pp_percent >= 0
    
    # Determine bar width (50% = neutral)
    if is_positive:
        bar_width = 50 + (pp_percent / 2)  # Scale: 0% to 100% = 50% to 100%
        bar_class = "pp-bar-fill-positive"
    else:
        bar_width = 50 + (pp_percent / 2)  # Scale: 0% to -50% = 50% to 0%
        bar_class = "pp-bar-fill-negative"
    
    card_class = "country-card-positive" if is_positive else "country-card-negative"
    badge_class = "pp-badge-positive" if is_positive else "pp-badge-negative"
    arrow = "↑" if is_positive else "↓"
    pp_text = f"{pp_percent:+.0f}% Purchasing Power"
    
    st.markdown(f'''
    <div class="country-card {card_class}">
        <div class="country-name">{comp.target_country.upper()}</div>
        <div class="country-salary">${comp.target_salary_required:,.0f}</div>
        <div class="pp-badge-card {badge_class}">
            <span>{arrow}</span>
            <span>{pp_text}</span>
        </div>
        <div class="pp-bar-track">
            <div class="{bar_class}" style="width: {max(0, min(100, bar_width))}%;"></div>
        </div>
        <div class="vs-label">vs your ${st.session_state.base_salary:,.0f}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
