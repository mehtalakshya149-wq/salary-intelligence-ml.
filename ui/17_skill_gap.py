import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ml.src.skill_gap import get_skill_gap_report

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🎯", layout="wide")

# Add custom CSS for precision analysis styling
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');

.main {
    padding: 0 24px !important;
}

* {
    font-family: 'Sora', sans-serif !important;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(16,185,129,0.06));
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 32px;
    position: relative;
}

.hero-content {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.hero-icon {
    width: 28px;
    height: 28px;
    flex-shrink: 0;
}

.hero-text {
    flex: 1;
}

.hero-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
}

.realtime-badge {
    position: absolute;
    top: 24px;
    right: 28px;
    background: rgba(34,197,94,0.15);
    color: #22c55e;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Two Column Layout ── */
.two-col-layout {
    display: flex;
    gap: 36px;
}

.left-column {
    width: 36%;
}

.right-column {
    width: 60%;
}

/* ── Section Headers ── */
.section-label-text {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #22c55e;
    padding-left: 12px;
    margin-bottom: 20px;
}

/* ── Input Fields ── */
.input-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}

.input-label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.help-icon {
    background: var(--surface-2);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 11px;
    color: var(--text-secondary);
    cursor: help;
}

/* ── Stat Cards ── */
.stat-cards-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card-green {
    background: rgba(34,197,94,0.06);
    border: 1px solid rgba(34,197,94,0.15);
    border-top: 3px solid #22c55e;
    border-radius: 14px;
    padding: 20px 24px;
}

.stat-card-red {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.12);
    border-top: 3px solid #ef4444;
    border-radius: 14px;
    padding: 20px 24px;
}

.stat-label {
    font-size: 10px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value-green {
    font-size: 32px;
    font-weight: 900;
    color: #22c55e;
    letter-spacing: -1px;
    margin-top: 6px;
}

.stat-value-red {
    font-size: 32px;
    font-weight: 900;
    color: #ef4444;
    letter-spacing: -1px;
    margin-top: 6px;
}

.stat-sublabel {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
}

.stat-indicator {
    font-size: 11px;
    font-weight: 600;
    margin-top: 6px;
}

.stat-indicator-green {
    color: #22c55e;
}

.stat-indicator-red {
    color: #ef4444;
}

/* ── Chart Container ── */
.chart-container-dark {
    background: var(--bg-app);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    padding: 20px;
}

/* ── Skill Breakdown ── */
.skill-breakdown-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 14px;
}

.skill-pill-green {
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin: 4px;
}

.skill-pill-red {
    background: rgba(239,68,68,0.1);
    color: #ef4444;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin: 4px;
}

/* ── Style Streamlit Inputs ── */
input[type="text"], textarea {
    background: var(--surface-2) !important;
    border: 1px solid #0d3318 !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    line-height: normal !important;
}

input[type="text"]:focus, textarea:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.12) !important;
}

textarea {
    min-height: 100px !important;
    resize: vertical !important;
}

/* ── Skill Pills Below Textarea ── */
.skill-pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.skill-pill {
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* ── Style Streamlit Primary Button ── */
button[kind="primary"] {
    background: linear-gradient(135deg, #15803d, #22c55e) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 15px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    line-height: normal !important;
}

button[kind="primary"]:hover {
    brightness: 115% !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(34,197,94,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# ── HERO BANNER ──
st.markdown(f'''
<div class="hero-banner">
    <div class="hero-content">
        <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="6"></circle>
            <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <div class="hero-text">
            <div class="hero-title">Precision Analysis</div>
            <div class="hero-subtitle">Compare your current technical stack against real-time market requirements derived from thousands of salary data points to identify critical skill gaps.</div>
        </div>
    </div>
    <div class="realtime-badge">Real-Time</div>
</div>
''', unsafe_allow_html=True)

# Initialize session state for inputs
if "job_title" not in st.session_state:
    st.session_state.job_title = "Data Scientist"
if "user_skills" not in st.session_state:
    st.session_state.user_skills = "Python, SQL, Tableau"
if "analyze_btn" not in st.session_state:
    st.session_state.analyze_btn = False

# ── TWO COLUMN LAYOUT ──
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="section-label-text">Your Profile</div>', unsafe_allow_html=True)
    
    # Job Title Input
    st.markdown('<div class="input-label">Job Title</div>', unsafe_allow_html=True)
    job_title = st.text_input("", value=st.session_state.job_title, label_visibility="collapsed", key="job_title_input")
    st.session_state.job_title = job_title
    
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    # Skills Textarea with help icon
    st.markdown(f'''
<div class="input-label-row">
    <div class="input-label" style="margin-bottom: 0;">Current Skills</div>
    <div class="help-icon" title="Enter skills separated by commas">?</div>
</div>
''', unsafe_allow_html=True)
    user_skills = st.text_area("", value=st.session_state.user_skills, label_visibility="collapsed", key="skills_input")
    st.session_state.user_skills = user_skills
    
    # Show skill pills
    if user_skills.strip():
        skills_list = [s.strip() for s in user_skills.split(",") if s.strip()]
        pills_html = "".join([f'<span class="skill-pill">{skill} ✓</span>' for skill in skills_list])
        st.markdown(f'<div class="skill-pills-row">{pills_html}</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Analyze button
    analyze_btn = st.button("🎯 Run Gap Analysis", type="primary", use_container_width=True, key="run_analysis")

with col2:
    if analyze_btn or st.session_state.get("has_run_analysis", False):
        if analyze_btn:
            st.session_state.has_run_analysis = True
            
        with st.spinner("Mining market requirements and calculating structural gaps..."):
            try:
                report = get_skill_gap_report(job_title, user_skills)
                st.session_state.last_report = report
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()
        
        report = st.session_state.get("last_report", report)
        
        # ── THREE STAT CARDS ──
        match_pct = report['match_percentage']
        missing_count = len(report['missing_skills'])
        matched_count = len(report['matched_skills'])
        
        # Create SVG circular progress ring
        circumference = 2 * 3.14159 * 20
        offset = circumference - (match_pct / 100) * circumference
        
        st.markdown(f'''
<div class="stat-cards-row">
    <div class="stat-card-green">
        <div class="stat-label">MARKET MATCH</div>
        <div class="stat-value-green">{match_pct}%</div>
        <div class="stat-sublabel">of required skills matched</div>
        <svg width="52" height="52" style="position: absolute; top: 20px; right: 20px;">
            <circle cx="26" cy="26" r="20" stroke="#1e293b" stroke-width="5" fill="none"/>
            <circle cx="26" cy="26" r="20" stroke="#22c55e" stroke-width="5" fill="none"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 26 26)" stroke-linecap="round"/>
        </svg>
    </div>
    <div class="stat-card-red">
        <div class="stat-label">MISSING SKILLS</div>
        <div class="stat-value-red">{missing_count}</div>
        <div class="stat-sublabel">skills to acquire for full match</div>
        <div class="stat-indicator stat-indicator-red">⚠ Gaps detected</div>
    </div>
    <div class="stat-card-green">
        <div class="stat-label">MATCHED SKILLS</div>
        <div class="stat-value-green">{matched_count}</div>
        <div class="stat-sublabel">skills already in your stack</div>
        <div class="stat-indicator stat-indicator-green">✓ Strong foundation</div>
    </div>
</div>
''', unsafe_allow_html=True)
        
        # ── CHART SECTION ──
        st.markdown('<div class="section-label-text">Market Demand vs. Your Stack</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 16px;">Core Competency Benchmarking: {job_title}</div>', unsafe_allow_html=True)
        
        # Prepare data for plotting
        plot_data = []
        for s in report['market_top_skills']:
            plot_data.append({
                "Skill": s.upper(),
                "Status": "Matched" if s in report['matched_skills'] else "Gap",
                "Value": 1
            })
        
        # Create custom bar chart with gradient colors
        fig = go.Figure()
        
        for idx, row in enumerate(plot_data):
            if row['Status'] == 'Matched':
                color = '#22c55e'
            else:
                color = '#ef4444'
            
            fig.add_trace(go.Bar(
                x=[row['Skill']],
                y=[row['Value']],
                marker_color=color,
                name=row['Status'],
                hovertemplate=f'<b>{row["Skill"]}</b><br>Status: {row["Status"]}<extra></extra>'
            ))
        
        fig.update_layout(
            barmode='group',
            xaxis=dict(
                tickfont=dict(family='Sora', size=11, color='var(--text-secondary)'),
                gridcolor='rgba(255,255,255,0.04)',
                linecolor='rgba(255,255,255,0.08)'
            ),
            yaxis=dict(
                visible=False,
                showticklabels=False,
                gridcolor='rgba(255,255,255,0.04)',
            ),
            plot_bgcolor='var(--bg-app)',
            paper_bgcolor='var(--bg-app)',
            margin=dict(l=40, r=20, t=20, b=80),
            height=300,
            bargap=0.3,
            showlegend=False,
            hoverlabel=dict(
                bgcolor='rgba(6,13,31,0.95)',
                bordercolor='rgba(34,197,94,0.3)',
                font=dict(family='Sora', size=13, color='var(--text-primary)')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        st.markdown(f'''
<div style="display: flex; justify-content: center; gap: 16px; margin-top: 12px; font-size: 12px; color: var(--text-secondary);">
    <div>Status</div>
    <span style="background: rgba(34,197,94,0.12); color: #22c55e; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600;">Matched</span>
    <span style="background: rgba(239,68,68,0.1); color: #ef4444; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600;">Gap</span>
</div>
''', unsafe_allow_html=True)
        
        # ── SKILL BREAKDOWN SECTION ──
        st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label-text" style="margin: 24px 0 14px;">Skill Breakdown</div>', unsafe_allow_html=True)
        
        # Create two columns for skill breakdown
        sb_col1, sb_col2 = st.columns(2)
        
        with sb_col1:
            st.markdown('<div style="font-size: 12px; color: #22c55e; font-weight: 700; margin-bottom: 10px;">✅ You Have</div>', unsafe_allow_html=True)
            if report['matched_skills']:
                matched_pills = "".join([f'<span class="skill-pill-green">✓ {skill}</span>' for skill in report['matched_skills']])
                st.markdown(f'<div>{matched_pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size: 13px; color: var(--text-secondary);">No skills matched yet</div>', unsafe_allow_html=True)
        
        with sb_col2:
            st.markdown('<div style="font-size: 12px; color: #ef4444; font-weight: 700; margin-bottom: 10px;">❌ You Need</div>', unsafe_allow_html=True)
            if report['missing_skills']:
                missing_pills = "".join([f'<span class="skill-pill-red">+ {skill}</span>' for skill in report['missing_skills']])
                st.markdown(f'<div>{missing_pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size: 13px; color: #22c55e; font-weight: 600;">🎉 No gaps detected! You are market-ready.</div>', unsafe_allow_html=True)
        
        # ── LEARNING PATH ──
        if report.get('learning_path'):
            st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label-text" style="margin: 24px 0 14px;">Recommended Learning Path</div>', unsafe_allow_html=True)
            
            for idx, step in enumerate(report['learning_path'], 1):
                st.markdown(f'''
<div style="background: rgba(34,197,94,0.05); border-left: 3px solid #22c55e; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; font-size: 13px; color: var(--text-secondary);">
    <span style="color: #22c55e; font-weight: 700;">Step {idx}:</span> {step}
</div>
''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
<div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(34,197,94,0.15); border-radius: 14px; padding: 40px; text-align: center; margin-top: 40px;">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" style="opacity: 0.3;">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="6"></circle>
        <circle cx="12" cy="12" r="2"></circle>
    </svg>
    <div style="font-size: 15px; font-weight: 600; color: var(--text-secondary); margin-top: 12px;">Ready to Analyze</div>
    <div style="font-size: 13px; color: #475569; margin-top: 6px;">Enter your target job and skills on the left to begin</div>
</div>
''', unsafe_allow_html=True)
