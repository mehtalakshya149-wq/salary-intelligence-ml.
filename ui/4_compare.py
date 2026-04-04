import streamlit as st
import pandas as pd
from ml.src.salary_trends import compute_filtered_trends, load_data, clean_data, load_config

st.set_page_config(page_title="Trend Comparison", page_icon="📊", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM TREND COMPARISON STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-center, #0f1f3d 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 20px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #e11d48;
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

.timeseries-badge {
    background: rgba(225, 29, 72, 0.15);
    color: #e11d48;
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

/* ── AI Tech Banner ── */
.ai-banner {
    background: linear-gradient(135deg, rgba(225,29,72,0.08), rgba(99,102,241,0.06));
    border: 1px solid rgba(225, 29, 72, 0.2);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.ai-banner-icon {
    color: #e11d48;
    font-size: 20px;
    margin-right: 14px;
}

.ai-banner-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    flex: 1;
}

.ai-engine-badge {
    background: rgba(225, 29, 72, 0.12);
    color: #e11d48;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
}

/* ── Section Label ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    border-left: 3px solid #e11d48;
    padding-left: 10px;
    margin-bottom: 16px;
}

/* ── Filter Controls ── */
.filter-controls-row {
    display: flex;
    gap: 20px;
    margin-bottom: 14px;
}

.filter-column {
    width: 46%;
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

/* ── Dropdown Styling ── */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #3b0f1a !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #e11d48 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Quick Filter Chips ── */
.filter-chips {
    display: inline-flex;
    gap: 8px;
    margin-top: 14px;
    flex-wrap: wrap;
}

.filter-chip {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.filter-chip:hover {
    border-color: rgba(225, 29, 72, 0.2);
    color: #f4a0b0;
}

.filter-chip.active {
    background: rgba(225, 29, 72, 0.12);
    border-color: rgba(225, 29, 72, 0.3);
    color: #e11d48;
    font-weight: 600;
}

/* ── Generate Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #be123c, #e11d48) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 28px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 24px !important;
    line-height: normal !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(115%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(225, 29, 72, 0.35) !important;
}

/* ── Empty State ── */
.empty-state-container {
    background: var(--surface-glass);
    border: 1px dashed var(--border-strong);
    border-radius: 16px;
    padding: 56px 32px;
    text-align: center;
    margin-top: 32px;
}

.empty-state-icon {
    font-size: 64px;
    color: #e11d48;
    opacity: 0.2;
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
}

.feature-pills {
    display: inline-flex;
    gap: 12px;
    margin-top: 24px;
    flex-wrap: wrap;
}

.feature-pill {
    background: var(--bg-surface);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 12px;
    color: var(--text-secondary);
}

/* ── Chart Container ── */
.chart-container {
    background: var(--surface-glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-top: 28px;
}

.chart-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 16px;
}

.chart-legend {
    display: flex;
    gap: 12px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.legend-pill {
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Result Cards ── */
.result-section {
    margin-top: 28px;
}

.result-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
}

.model-observation {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 20px 0;
    font-size: 13px;
    color: #10b981;
    line-height: 1.6;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stInfo {
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
        <line x1="18" y1="20" x2="18" y2="10"></line>
        <line x1="12" y1="20" x2="12" y2="4"></line>
        <line x1="6" y1="20" x2="6" y2="14"></line>
    </svg>
    <h1 class="header-title">Trend Comparison & Benchmarking</h1>
    <span class="timeseries-badge">Time-Series</span>
    <p class="header-subtitle">Compare dynamic compensation aggregates based on granular sub-filters like remote modality.</p>
</div>
''', unsafe_allow_html=True)

try:
    config = load_config("ml/config.yaml")
    df = clean_data(load_data(config["paths"]["raw_data"]), config)
    
    # ══════════════════════════════════════════════════════════════════════════════
    #  AI TECH BANNER
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('''
    <div class="ai-banner">
        <div style="display: flex; align-items: center; flex: 1; gap: 14px;">
            <span style="font-size: 20px; color: #e11d48;">⚙️</span>
            <div class="ai-banner-text">Powered by structural Time-Series Regressors natively bridging historical inputs.</div>
        </div>
        <span class="ai-engine-badge">AI Engine</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # ══════════════════════════════════════════════════════════════════════════════
    #  FILTER CONTROLS
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">Configure Filters</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<label class="field-label">Filter Demographic</label>', unsafe_allow_html=True)
        filter_col = st.selectbox("", ["job_title", "experience_level", "company_location", "company_size", "employment_type"], label_visibility="collapsed", key="filter_demographic")
    
    with col2:
        st.markdown('<label class="field-label">Specific Target</label>', unsafe_allow_html=True)
        # Convert everything to string for consistency
        unique_vals = sorted(list(set([str(x) for x in df[filter_col].dropna().unique()])))
        filter_val = st.selectbox("", unique_vals, label_visibility="collapsed", key="specific_target")
    
    # Quick filter chips
    st.markdown('''
    <div class="filter-chips">
        <span class="filter-chip active">By Job Title</span>
        <span class="filter-chip">By Country</span>
        <span class="filter-chip">By Experience</span>
        <span class="filter-chip">By Company Size</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Generate button
    gen_btn = st.button("📈 Generate Extrapolations", type="primary")
    
    # ══════════════════════════════════════════════════════════════════════════════
    #  RESULTS AREA
    # ══════════════════════════════════════════════════════════════════════════════
    if gen_btn:
        with st.spinner("Computing time-series trajectories..."):
            res = compute_filtered_trends(df, filter_col, filter_val, n_forecast_years=1)
            
            if "error" in res:
                st.warning(res["error"])
            else:
                # Historical Data
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="chart-title">Historical Isolations for {filter_col.replace("_", " ").title()}: `{filter_val}`</div>', unsafe_allow_html=True)
                
                df_out = pd.DataFrame(res["yearly_stats"])
                
                # Format for display
                df_display = df_out.copy()
                for col in ["mean", "median", "std", "p10", "p90"]:
                    if col in df_display.columns:
                        df_display[col] = df_display[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
                if "yoy_growth_pct" in df_display.columns:
                    df_display["yoy_growth_pct"] = df_display["yoy_growth_pct"].apply(
                        lambda x: f"{x:+.2f}%" if pd.notna(x) and str(x) != "None" else "—"
                    )
                df_display = df_display.rename(columns={
                    "work_year": "Year", "count": "Samples", "mean": "Mean Salary",
                    "median": "Median Salary", "std": "Std Dev",
                    "p10": "P10 (Low)", "p90": "P90 (High)", "yoy_growth_pct": "YoY Growth"
                })
                st.dataframe(df_display, use_container_width=True)
                
                # Model Observation
                trend = res["trend"]
                st.markdown(f'<div class="model-observation">💡 <strong>Model Observation:</strong> {trend["interpretation"]}</div>', unsafe_allow_html=True)
                
                # Forecast
                st.markdown('<div class="result-title">🔮 Extrapolated Trajectories</div>', unsafe_allow_html=True)
                df_forecast = pd.DataFrame(res["forecast"])
                for col in ["predicted_median", "confidence_low", "confidence_high"]:
                    if col in df_forecast.columns:
                        df_forecast[col] = df_forecast[col].apply(lambda x: f"${x:,.0f}")
                df_forecast = df_forecast.rename(columns={
                    "year": "Year", "predicted_median": "Predicted Median",
                    "confidence_low": "95% CI Low", "confidence_high": "95% CI High"
                })
                st.dataframe(df_forecast, use_container_width=True)
                
                # Chart legend
                st.markdown('''
                <div class="chart-legend">
                    <span class="legend-pill" style="background: rgba(225,29,72,0.15); color: #e11d48;">● Median Salary</span>
                    <span class="legend-pill" style="background: rgba(244,63,94,0.15); color: #f43f5e;">● Confidence Band</span>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)  # Close chart-container
    else:
        # Empty state
        st.markdown('''
        <div class="empty-state-container">
            <svg class="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <div class="empty-state-title">Select filters and generate extrapolations</div>
            <div class="empty-state-subtitle">Salary trends will appear here as interactive charts</div>
            <div class="feature-pills">
                <span class="feature-pill">📈 Trend Lines</span>
                <span class="feature-pill">📊 Salary Bands</span>
                <span class="feature-pill">🌍 Geographic Split</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
except Exception as e:
    st.error(f"Failed to isolate dataset streams. Exception Output: {e}")
