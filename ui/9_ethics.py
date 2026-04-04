import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ml.src.fairness import run_bias_audit
from ml.src.monitoring import detect_live_drift

st.set_page_config(page_title="Ethics & Fairness", page_icon="🛡️", layout="wide")

# Add comprehensive CSS for ethics page
st.markdown("""
<style>
/* ── Global ─ */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');

.main {
    padding: 0 24px !important;
}

* {
    font-family: 'Sora', sans-serif !important;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Page Header ── */
.ethics-header-icon {
    width: 24px;
    height: 24px;
    color: #60a5fa;
    margin-bottom: 12px;
}

.ethics-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.ethics-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 680px;
    margin-bottom: 20px;
}

/* ── AI Manifesto Card ── */
.manifesto-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(59,130,246,0.06));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 28px;
    position: relative;
}

.manifesto-icon {
    color: #818cf8;
    font-size: 20px;
    margin-bottom: 8px;
}

.manifesto-label {
    color: #818cf8;
    font-weight: 700;
    font-size: 13px;
}

.manifesto-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-top: 8px;
}

/* ── Stat Cards ── */
.stat-card-red {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.15);
    border-top: 3px solid #ef4444;
    border-radius: 14px;
    padding: 22px 26px;
}

.stat-card-blue {
    background: rgba(59,130,246,0.04);
    border: 1px solid rgba(59,130,246,0.12);
    border-top: 3px solid #3b82f6;
    border-radius: 14px;
    padding: 22px 26px;
}

.stat-card-amber {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.15);
    border-top: 3px solid #f59e0b;
    border-radius: 14px;
    padding: 22px 26px;
}

.stat-label {
    font-size: 10px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value-red {
    font-size: 34px;
    font-weight: 900;
    color: #ef4444;
    letter-spacing: -1px;
    margin-top: 6px;
}

.stat-value-blue {
    font-size: 34px;
    font-weight: 900;
    color: #60a5fa;
    letter-spacing: -1px;
    margin-top: 6px;
}

.stat-value-amber {
    font-size: 34px;
    font-weight: 900;
    color: #f59e0b;
    letter-spacing: -1px;
    margin-top: 6px;
}

.stat-sublabel {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
}

.stat-sublabel-red {
    font-size: 11px;
    color: #ef4444;
    opacity: 0.7;
    margin-top: 4px;
}

.stat-delta-badge {
    background: rgba(239,68,68,0.12);
    color: #ef4444;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
    display: inline-flex;
}

.stat-attention {
    font-size: 11px;
    color: #f59e0b;
    margin-top: 6px;
}

/* ── Tab Switcher ── */
.tab-container {
    background: #0d1117;
    border-radius: 12px;
    padding: 4px;
    display: inline-flex;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 28px;
}

.tab-pill {
    padding: 8px 20px;
    font-size: 13px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.tab-active {
    background: rgba(99,102,241,0.2);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.3);
    font-weight: 600;
}

.tab-inactive {
    color: var(--text-secondary);
}

.tab-inactive:hover {
    color: var(--text-secondary);
}

/* ── Section Headings ── */
.section-label-text {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    border-left: 3px solid #818cf8;
    padding-left: 12px;
    margin-bottom: 8px;
}

.section-subheading {
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 16px;
}

/* ── Chart Container ── */
.chart-container-dark {
    background: var(--bg-app);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    padding: 20px;
}

/* ── Table Styling ── */
.data-table-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    margin-top: 16px;
}

/* ── Limitation Cards ── */
.limitation-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #f59e0b;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}

/* ── Narrative Cards ── */
.narrative-card-red {
    background: rgba(239,68,68,0.05);
    border: 1px solid rgba(239,68,68,0.12);
    border-left: 3px solid #ef4444;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

.narrative-card-amber {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.12);
    border-left: 3px solid #f59e0b;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

.narrative-text {
    color: #e2e8f0;
    font-size: 13px;
    line-height: 1.6;
}

/* ── Drift Cards ── */
.drift-card-blue {
    background: rgba(59,130,246,0.05);
    border: 1px solid rgba(59,130,246,0.12);
    border-top: 3px solid #3b82f6;
    border-radius: 14px;
    padding: 22px 26px;
}

.drift-card-indigo {
    background: rgba(99,102,241,0.05);
    border: 1px solid rgba(99,102,241,0.12);
    border-top: 3px solid #6366f1;
    border-radius: 14px;
    padding: 22px 26px;
}

.drift-card-green {
    background: rgba(16,185,129,0.05);
    border: 1px solid rgba(16,185,129,0.12);
    border-top: 3px solid #10b981;
    border-radius: 14px;
    padding: 22px 26px;
}

.drift-delta-badge {
    background: rgba(16,185,129,0.12);
    color: #10b981;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
    display: inline-flex;
}

.status-card {
    background: rgba(16,185,129,0.06);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.pulse-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #10b981;
    animation: pulse 1.5s ease infinite;
    flex-shrink: 0;
}

.live-badge {
    color: #10b981;
    font-size: 11px;
    font-weight: 700;
    animation: pulse 1.5s ease infinite;
    margin-left: 12px;
}

/* ── Summary Bar ── */
.summary-bar-red {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.12);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
}

/* ── Style Streamlit Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #818cf8 !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
}

/* ── Style Streamlit Selectbox ── */
[data-testid="stSelectbox"] {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
}

[data-testid="stSelectbox"]:hover {
    border-color: #818cf8;
}
</style>
""", unsafe_allow_html=True)

# ── PAGE HEADER ──
st.markdown(f'''
<svg class="ethics-header-icon" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
</svg>
<div class="ethics-title">Ethical AI & Bias Auditor</div>
<div class="ethics-subtitle">Mathematical transparency into systemic biases, demographic parity, and live predictive drift tracking of the Salary Intelligence Platform.</div>
''', unsafe_allow_html=True)

# Run audit
with st.spinner("Running full bias audit & drift analysis..."):
    try:
        report = run_bias_audit()
        drift = detect_live_drift()
    except Exception as e:
        st.error(f"Audit Exception: {e}")
        st.stop()

# ── AI MANIFESTO CARD ──
st.markdown(f'''
<div class="manifesto-card">
    <div class="manifesto-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
            <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"></path>
        </svg>
    </div>
    <div class="manifesto-label">AI Manifesto:</div>
    <div class="manifesto-text">We explicitly acknowledge that machine learning models amplify historical dataset inequalities if left unchecked. This dashboard mathematically tracks statistical parity to isolate potential discrimination.</div>
</div>
''', unsafe_allow_html=True)

# ── TOP 3 STAT CARDS ──
score = report["fairness_score"]
records = report["records_analyzed"]
bias_count = len(report["bias_flags"])

# Circular gauge SVG
circumference = 2 * 3.14159 * 22
offset = circumference - (score / 100) * circumference

st.markdown(f'''
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px;">
    <div class="stat-card-red" style="position: relative;">
        <div class="stat-label">OVERALL FAIRNESS SCORE</div>
        <div class="stat-value-red">{score}/100</div>
        <div class="stat-delta-badge">↓ {score-100}%</div>
        <div class="stat-sublabel-red">Critical — far below 80% threshold</div>
        <svg width="56" height="56" style="position: absolute; top: 22px; right: 26px;">
            <circle cx="28" cy="28" r="22" stroke="#1e293b" stroke-width="5" fill="none"/>
            <circle cx="28" cy="28" r="22" stroke="#ef4444" stroke-width="5" fill="none"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 28 28)" stroke-linecap="round"/>
        </svg>
    </div>
    <div class="stat-card-blue">
        <div class="stat-label">RECORDS ANALYZED</div>
        <div class="stat-value-blue">{records:,}</div>
        <div class="stat-sublabel">salary records audited</div>
    </div>
    <div class="stat-card-amber">
        <div class="stat-label">BIAS FLAGS</div>
        <div class="stat-value-amber">{bias_count}</div>
        <div class="stat-sublabel">active parity violations</div>
        <div class="stat-attention">⚠ Requires attention</div>
    </div>
</div>
''', unsafe_allow_html=True)

# ── TAB SWITCHER ──
selected_tab = st.radio("Navigation", ["Dimension Analysis", "Bias Flags", "Bias Narrative", "Live Drift"], 
                        horizontal=True, label_visibility="collapsed", key="ethics_tab")

# Helper function to humanize labels
def humanize_dimension(dim):
    mapping = {
        'experience_level': 'Experience Level',
        'company_size': 'Company Size',
        'company_location': 'Company Location'
    }
    return mapping.get(dim, dim.replace('_', ' ').title())

def humanize_value(val):
    mapping = {
        'en': 'Entry', 'mi': 'Mid', 'se': 'Senior', 'ex': 'Executive',
        's': 'Small'
    }
    return mapping.get(val, val.upper())

# ═══════════════════════════════
# TAB 1 — DIMENSION ANALYSIS
# ═══════════════════════════════
if selected_tab == "Dimension Analysis":
    st.markdown('<div class="section-label-text">Statistical Parity by Dimension</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Bars show group median vs global median (1.0 = perfect parity). Red bars indicate breached 80% rule.</div>', unsafe_allow_html=True)
    
    # Dimension selector
    st.markdown('<div style="font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">Select Dimension to Isolate</div>', unsafe_allow_html=True)
    dim_options = list(report["dimensions"].keys())
    dim_labels = [humanize_dimension(d) for d in dim_options]
    selected_idx = st.selectbox("", dim_labels, index=0, label_visibility="collapsed", key="dim_select")
    col_sel = dim_options[dim_labels.index(selected_idx)]
    dim_data = pd.DataFrame(report["dimensions"][col_sel])
    
    # Chart
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container-dark">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">Disparate Impact Analysis: {humanize_dimension(col_sel)}</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    for idx, row in dim_data.iterrows():
        color = '#10b981' if row['status'] == 'Fair' else '#ef4444' if 'Underrepresented' in row['status'] else '#f59e0b'
        fig.add_trace(go.Bar(
            x=[humanize_value(row['group'])],
            y=[row['impact_ratio']],
            marker_color=color,
            name=row['status'],
            hovertemplate=f'<b>{humanize_value(row["group"])}</b><br>Ratio: {row["impact_ratio"]:.2f}<br>Status: {row["status"]}<extra></extra>'
        ))
    
    # Reference lines
    fig.add_hline(y=1.0, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Parity = 1.0",
                  annotation_font=dict(size=11, color='var(--text-secondary)'))
    fig.add_hline(y=0.8, line_dash="dash", line_color="rgba(239,68,68,0.4)", annotation_text="80% Rule threshold",
                  annotation_font=dict(size=11, color='#ef4444'))
    
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(family='Sora', size=11, color='var(--text-secondary)'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)',
            title=''
        ),
        yaxis=dict(
            tickfont=dict(family='Sora', size=11, color='#475569'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)',
            title='Impact Ratio'
        ),
        plot_bgcolor='var(--bg-app)',
        paper_bgcolor='var(--bg-app)',
        margin=dict(l=60, r=20, t=40, b=60),
        height=300,
        bargap=0.4,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Table
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Build custom HTML table
    table_html = '<div class="data-table-container"><table style="width: 100%; border-collapse: collapse;">'
    table_html += '<thead><tr style="background: rgba(99,102,241,0.06); border-bottom: 1px solid rgba(255,255,255,0.07);">'
    table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">#</th>'
    table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Group</th>'
    table_html += '<th style="padding: 14px 20px; text-align: right; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Median Salary</th>'
    table_html += '<th style="padding: 14px 20px; text-align: right; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Inequality (Gini)</th>'
    table_html += '<th style="padding: 14px 20px; text-align: right; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Parity Ratio</th>'
    table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Status</th>'
    table_html += '</tr></thead><tbody>'
    
    for idx, row in dim_data.iterrows():
        bg = 'rgba(255,255,255,0.015)' if idx % 2 == 0 else 'transparent'
        salary = f"${row['median']:,.0f}"
        parity_color = '#ef4444' if row['impact_ratio'] < 0.8 else '#10b981' if row['impact_ratio'] <= 1.2 else '#f59e0b'
        
        status_class = 'background: rgba(16,185,129,0.1); color: #10b981;' if row['status'] == 'Fair' else \
                      'background: rgba(239,68,68,0.1); color: #ef4444;' if 'Underrepresented' in row['status'] else \
                      'background: rgba(245,158,11,0.1); color: #f59e0b;'
        
        table_html += f'<tr style="background: {bg}; border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s;" onmouseover="this.style.background=\'rgba(99,102,241,0.05)\'" onmouseout="this.style.background=\'{bg}\'">'
        table_html += f'<td style="padding: 14px 20px;"><span style="background: var(--surface-2); color: var(--text-secondary); border-radius: 6px; padding: 2px 8px; font-size: 11px;">{idx}</span></td>'
        table_html += f'<td style="padding: 14px 20px; color: var(--text-primary); font-weight: 600; font-size: 13px;">{humanize_value(row["group"])}</td>'
        table_html += f'<td style="padding: 14px 20px; text-align: right; color: #60a5fa; font-weight: 600;">{salary}</td>'
        table_html += f'<td style="padding: 14px 20px; text-align: right; color: var(--text-secondary);">{row["gini"]:.3f}</td>'
        table_html += f'<td style="padding: 14px 20px; text-align: right; color: {parity_color}; font-weight: 700;">{row["impact_ratio"]:.2f}</td>'
        table_html += f'<td style="padding: 14px 20px;"><span style="{status_class} border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600;">{row["status"]}</span></td>'
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Known Limitations
    st.markdown('<div class="section-label-text" style="margin: 32px 0 16px;">Known Global Model Limitations</div>', unsafe_allow_html=True)
    
    limitations = [
        ("Reporting Bias", "Salary figures are self-reported and skewed heavily towards US-centric hubs. Approximations for low-count regions operate with substantially widened interpolation limits."),
        ("Missing Inflation Dynamics", "Unless actively patched by our pipeline, raw models intrinsically undervalue current macroeconomic dynamics natively stored in older dataset rows."),
        ("Implicit Demographics", "The model actively abstracts away Age and Gender to deliberately restrict targeted discrimination logic inside the decision trees.")
    ]
    
    for title, desc in limitations:
        st.markdown(f'''
<div class="limitation-card">
    <span style="color: #f59e0b; font-weight: 700; font-size: 13px;">{title}:</span>
    <span style="color: var(--text-secondary); font-size: 13px; line-height: 1.6; margin-left: 8px;">{desc}</span>
</div>
''', unsafe_allow_html=True)

# ═══════════════════════════════
# TAB 2 — BIAS FLAGS  
# ═══════════════════════════════
elif selected_tab == "Bias Flags":
    st.markdown('<div class="section-label-text">Active Bias Flags</div>', unsafe_allow_html=True)
    
    if not report["bias_flags"]:
        st.markdown('''
<div style="background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.2); border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
        <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <span style="color: #10b981; font-size: 13px; font-weight: 600;">No critical bias patterns detected based on current thresholds.</span>
</div>
''', unsafe_allow_html=True)
    else:
        # Summary bar
        st.markdown(f'''
<div class="summary-bar-red">
    <div style="font-size: 13px; color: #ef4444; font-weight: 600;">⚠ {len(report["bias_flags"])} active bias flags detected across all dimensions</div>
    <div style="font-size: 11px; color: #475569;">Last updated: just now</div>
</div>
''', unsafe_allow_html=True)
        
        # Build table
        flags_df = pd.DataFrame(report["bias_flags"])
        table_html = '<div class="data-table-container"><table style="width: 100%; border-collapse: collapse;">'
        table_html += '<thead><tr style="background: rgba(99,102,241,0.06); border-bottom: 1px solid rgba(255,255,255,0.07);">'
        table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">#</th>'
        table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Dimension</th>'
        table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Category</th>'
        table_html += '<th style="padding: 14px 20px; text-align: right; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Ratio to Global</th>'
        table_html += '<th style="padding: 14px 20px; text-align: left; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px;">Critique</th>'
        table_html += '</tr></thead><tbody>'
        
        for idx, row in flags_df.iterrows():
            bg = 'rgba(255,255,255,0.015)' if idx % 2 == 0 else 'transparent'
            ratio_color = '#ef4444' if row['ratio'] < 0.8 else '#f59e0b' if row['ratio'] > 1.2 else '#10b981'
            
            dim_text = humanize_dimension(row['dimension'])
            cat_text = humanize_value(row['group'])
            
            status_class = 'background: rgba(16,185,129,0.1); color: #10b981;' if row['status'] == 'Fair' else \
                          'background: rgba(239,68,68,0.1); color: #ef4444;' if 'Underrepresented' in row['status'] else \
                          'background: rgba(245,158,11,0.1); color: #f59e0b;'
            
            table_html += f'<tr style="background: {bg}; border-bottom: 1px solid rgba(255,255,255,0.04);">'
            table_html += f'<td style="padding: 14px 20px;"><span style="background: var(--surface-2); color: var(--text-secondary); border-radius: 6px; padding: 2px 8px; font-size: 11px;">{idx}</span></td>'
            table_html += f'<td style="padding: 14px 20px; color: var(--text-secondary); font-size: 13px;">{dim_text}</td>'
            table_html += f'<td style="padding: 14px 20px;"><span style="background: rgba(255,255,255,0.06); color: var(--text-primary); border-radius: 6px; padding: 2px 10px; font-size: 11px; font-weight: 700;">{cat_text}</span></td>'
            table_html += f'<td style="padding: 14px 20px; text-align: right; color: {ratio_color}; font-weight: 700;">{row["ratio"]:.4f}</td>'
            table_html += f'<td style="padding: 14px 20px;"><span style="{status_class} border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600;">{row["status"]}</span></td>'
            table_html += '</tr>'
        
        table_html += '</tbody></table></div>'
        st.markdown(table_html, unsafe_allow_html=True)

# ═══════════════════════════════
# TAB 3 — BIAS NARRATIVE
# ═══════════════════════════════
elif selected_tab == "Bias Narrative":
    st.markdown('<div class="section-label-text">AI-Generated Bias Narrative</div>', unsafe_allow_html=True)
    
    for bullet in report["narrative"]:
        # Determine severity
        is_underrepresented = "Lower" in bullet or "underrepresented" in bullet.lower()
        is_overrepresented = "Skewed" in bullet or "overrepresented" in bullet.lower()
        
        # Humanize the text
        humanized = bullet.replace('experience_level', 'Experience Level') \
                         .replace('company_size', 'Company Size') \
                         .replace('company_location', 'Company Location') \
                         .replace(' en ', ' Entry Level ') \
                         .replace(' ex ', ' Executive ') \
                         .replace(' mi ', ' Mid Level ') \
                         .replace(' se ', ' Senior ') \
                         .replace(' s ', ' Small ')
        
        # Highlight ratio values
        import re
        highlighted = re.sub(r'(\d+\.\d+x)', r'<span style="color: {"#ef4444" if is_underrepresented else "#f59e0b"}; font-weight: 700;">\1</span>', humanized)
        
        if is_underrepresented:
            st.markdown(f'''
<div class="narrative-card-red">
    <div class="narrative-text">
        <span style="color: #ef4444; font-size: 14px; margin-right: 8px;">⚠</span>
        {highlighted}
    </div>
</div>
''', unsafe_allow_html=True)
        elif is_overrepresented:
            st.markdown(f'''
<div class="narrative-card-amber">
    <div class="narrative-text">
        <span style="color: #f59e0b; font-size: 14px; margin-right: 8px;">↑</span>
        {highlighted}
    </div>
</div>
''', unsafe_allow_html=True)

# ═══════════════════════════════
# TAB 4 — LIVE DRIFT
# ═══════════════════════════════
elif selected_tab == "Live Drift":
    st.markdown(f'''
<div style="display: flex; align-items: center; margin-bottom: 8px;">
    <div class="section-label-text" style="margin-bottom: 0;">Live Operational Drift Monitoring</div>
    <div class="live-badge">● LIVE</div>
</div>
''', unsafe_allow_html=True)
    
    if "error" in drift:
        st.markdown(f'''
<div style="background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.2); border-radius: 12px; padding: 16px 20px;">
    <span style="color: #f59e0b; font-size: 13px;">⚠ {drift["error"]}</span>
</div>
''', unsafe_allow_html=True)
    elif drift.get("status") == "Awaiting Live Data":
        st.markdown(f'''
<div style="background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.2); border-radius: 12px; padding: 16px 20px;">
    <span style="color: #60a5fa; font-size: 13px;">ℹ {drift["message"]}</span>
</div>
''', unsafe_allow_html=True)
    else:
        # Live queries card
        st.markdown(f'''
<div class="drift-card-blue" style="margin-bottom: 16px;">
    <div class="stat-label">LIVE POSTGRES QUERIES ANALYZED</div>
    <div class="stat-value-blue">{drift['live_queries_analyzed']}</div>
    <div class="stat-sublabel">queries analyzed in this session</div>
</div>
''', unsafe_allow_html=True)
        
        # Training vs Live cards
        st.markdown(f'''
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
    <div class="drift-card-indigo">
        <div class="stat-label">HISTORICAL TRAINING MEDIAN</div>
        <div style="font-size: 28px; font-weight: 800; color: #818cf8; margin-top: 6px;">${drift['historic_median']:,.0f}</div>
        <div class="stat-sublabel">Historical training baseline</div>
    </div>
    <div class="drift-card-green">
        <div class="stat-label">LIVE INFERENCE MEDIAN</div>
        <div style="font-size: 28px; font-weight: 800; color: #10b981; margin-top: 6px;">${drift['live_inference_median']:,.0f}</div>
        <div class="stat-sublabel">Current live predictions</div>
        <div class="drift-delta-badge">+${drift['live_inference_median'] - drift['historic_median']:,.0f} vs baseline</div>
    </div>
</div>
''', unsafe_allow_html=True)
        
        # System status
        if abs(drift["drift_z_score"]) > 1.5:
            st.markdown(f'''
<div style="background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.2); border-radius: 12px; padding: 16px 20px; margin-top: 16px; display: flex; align-items: center; gap: 12px;">
    <div style="width: 10px; height: 10px; border-radius: 50%; background: #ef4444; animation: pulse 1.5s ease infinite; flex-shrink: 0;"></div>
    <span style="color: #ef4444; font-size: 13px; font-weight: 600;">⚠ {drift['status']} (Z-Score: {drift['drift_z_score']}) - Recalibration Highly Recommended.</span>
</div>
''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
<div class="status-card">
    <div class="pulse-dot"></div>
    <span style="color: #10b981; font-size: 13px; font-weight: 600;">✅ System Intact. Structural drift within mathematical bounds (Z-Score: {drift['drift_z_score']}).</span>
</div>
''', unsafe_allow_html=True)
