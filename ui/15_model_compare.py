import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from api.model_comparison import evaluate_models
from app import page_header

st.set_page_config(page_title="Model Comparison", page_icon="⚖️", layout="wide")

# Add custom CSS for model comparison styling
st.markdown("""
<style>
/* ── Model Label Badges ── */
.model-badge-rf {
    background: rgba(59,130,246,0.12);
    color: #60a5fa;
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.model-badge-gb {
    background: rgba(139,92,246,0.12);
    color: #a78bfa;
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Metric Cards ── */
.metric-card-blue {
    background: rgba(59,130,246,0.06);
    border: 1px solid rgba(59,130,246,0.15);
    border-top: 3px solid #3b82f6;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.metric-card-purple {
    background: rgba(139,92,246,0.06);
    border: 1px solid rgba(139,92,246,0.15);
    border-top: 3px solid #8b5cf6;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.metric-label {
    font-size: 10px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.metric-value-blue {
    font-size: 36px;
    font-weight: 900;
    color: #60a5fa;
}

.metric-value-purple {
    font-size: 36px;
    font-weight: 900;
    color: #a78bfa;
}

.metric-description {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
}

.metric-better {
    font-size: 11px;
    color: #10b981;
    font-weight: 600;
    margin-top: 6px;
}

.winner-badge {
    background: rgba(234,179,8,0.15);
    color: #eab308;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
    margin-top: 8px;
    display: inline-flex;
}

.lower-error-badge {
    background: rgba(16,185,129,0.12);
    color: #10b981;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}

/* ── Comparison Bar ── */
.comparison-bar {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    margin-top: 16px;
}

.comparison-text {
    font-size: 13px;
    color: var(--text-secondary);
}

.comparison-highlight {
    font-size: 13px;
    color: #10b981;
    font-weight: 600;
}

/* ── Chart Containers ── */
.chart-container-dark {
    background: var(--bg-app);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    padding: 20px;
}

.chart-legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 12px;
    font-size: 12px;
    color: var(--text-secondary);
}

/* ── Key Takeaways ── */
.takeaways-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
}

.takeaway-card-purple {
    background: rgba(139,92,246,0.05);
    border: 1px solid rgba(139,92,246,0.12);
    border-radius: 12px;
    padding: 16px 20px;
}

.takeaway-card-gold {
    background: rgba(234,179,8,0.05);
    border: 1px solid rgba(234,179,8,0.12);
    border-radius: 12px;
    padding: 16px 20px;
}

.takeaway-icon {
    font-size: 20px;
    color: #a78bfa;
}

.takeaway-icon-gold {
    font-size: 20px;
    color: #eab308;
}

.takeaway-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 8px;
}

.takeaway-body {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 4px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

page_header("AI Architecture", "Model Engine Comparison", "Inspect the architectural performance differences between the Random Forest and Gradient Boosting engines powering our predictions.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to view model architecture diagnostics.")
    st.stop()

with st.spinner("Executing model verification routines against the test hold-out set..."):
    try:
        metrics = evaluate_models()
    except Exception as e:
        st.error(f"Failed to execute model comparison. Ensure models are trained. Error: {e}")
        st.stop()

rf = metrics["random_forest"]
gb = metrics["gradient_boosting"]

# ── TOP-LEVEL ANALYTICS ──
st.markdown('<div class="section-label-text">Top-Level Analytics</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Random Forest model badge
    st.markdown('<div class="model-badge-rf">🌲 RANDOM FOREST</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    
    # RF Accuracy card
    st.markdown(f'''
    <div class="metric-card-blue">
        <div class="metric-label">RF ACCURACY (R²)</div>
        <div class="metric-value-blue">{rf['r2'] * 100:.1f}%</div>
        <div class="metric-description">Variance explained by model</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # RF RMSE card
    st.markdown(f'''
    <div class="metric-card-blue">
        <div class="metric-label">RF RMSE VARIANCE</div>
        <div class="metric-value-blue">${rf['rmse']:,.0f}</div>
        <div class="metric-better">Lower is better ↓</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    # Gradient Boosting model badge
    st.markdown('<div class="model-badge-gb">⚡ GRADIENT BOOSTING</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    
    # GB Accuracy card
    st.markdown(f'''
    <div class="metric-card-purple">
        <div class="metric-label">GB ACCURACY (R²)</div>
        <div class="metric-value-purple">{gb['r2'] * 100:.1f}%</div>
        <div class="winner-badge">🏆 Best Model</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # GB RMSE card
    st.markdown(f'''
    <div class="metric-card-purple">
        <div class="metric-label">GB RMSE VARIANCE</div>
        <div class="metric-value-purple">${gb['rmse']:,.0f}</div>
        <div class="lower-error-badge">✓ Lower Error</div>
    </div>
    ''', unsafe_allow_html=True)

# Comparison bar
accuracy_diff = (gb['r2'] - rf['r2']) * 100
rmse_diff = gb['rmse'] - rf['rmse']

st.markdown(f'''
<div class="comparison-bar">
    <div class="comparison-text">Gradient Boosting outperforms Random Forest</div>
    <div class="comparison-highlight">GB leads by +{accuracy_diff:.1f}% accuracy · ${rmse_diff:,.0f} RMSE</div>
</div>
''', unsafe_allow_html=True)

# ── MODEL VARIANCE PLOTTING ──
st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label-text">Model Variance Plotting</div>', unsafe_allow_html=True)
st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

c_left, c_right = st.columns(2)

with c_left:
    st.markdown('<div class="chart-container-dark">', unsafe_allow_html=True)
    st.markdown('''
    <div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">(RMSE) Root Mean Squared Error</div>
    <div style="color: #10b981; font-style: italic; font-size: 13px; margin-bottom: 16px;">Lower is better</div>
    ''', unsafe_allow_html=True)
    
    # Create RMSE chart with custom colors
    fig_rmse = go.Figure(data=[
        go.Bar(
            x=['Random Forest', 'Gradient Boosting'],
            y=[rf['rmse'], gb['rmse']],
            marker_color=['#3b82f6', '#8b5cf6'],
            text=[f'${rf["rmse"]:,.0f}', f'${gb["rmse"]:,.0f}'],
            textposition='outside',
            textfont=dict(size=13, color='var(--text-primary)', family='Sora'),
        )
    ])
    
    # Add annotation for GB advantage - positioned higher to avoid overlap
    fig_rmse.add_annotation(
        x='Gradient Boosting',
        y=gb['rmse'] + 8000,  # Increased offset to prevent overlap
        text=f'✓ -${abs(rmse_diff):,.0f}',
        showarrow=False,
        font=dict(size=12, color='#10b981', family='Sora', weight='bold'),
        bgcolor='rgba(16,185,129,0.15)',
        bordercolor='rgba(16,185,129,0.3)',
        borderwidth=1,
        borderpad=6
    )
    
    fig_rmse.update_layout(
        xaxis=dict(
            tickfont=dict(family='Sora', size=11, color='var(--text-secondary)'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)'
        ),
        yaxis=dict(
            tickfont=dict(family='Sora', size=11, color='#475569'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)',
            title='RMSE ($)'
        ),
        plot_bgcolor='var(--bg-app)',
        paper_bgcolor='var(--bg-app)',
        margin=dict(l=60, r=20, t=40, b=60),
        height=300,
        bargap=0.4,
        showlegend=False
    )
    
    st.plotly_chart(fig_rmse, use_container_width=True)
    
    # Chart legend
    st.markdown('''
    <div class="chart-legend">
        <span>🔵 Random Forest</span>
        <span>🟣 Gradient Boosting</span>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="chart-container-dark">', unsafe_allow_html=True)
    st.markdown('''
    <div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">(Accuracy) R² Score</div>
    <div style="color: #10b981; font-style: italic; font-size: 13px; margin-bottom: 16px;">Higher is better</div>
    ''', unsafe_allow_html=True)
    
    # Create Accuracy chart with custom colors
    fig_acc = go.Figure(data=[
        go.Bar(
            x=['Random Forest', 'Gradient Boosting'],
            y=[rf['r2'] * 100, gb['r2'] * 100],
            marker_color=['#3b82f6', '#8b5cf6'],
            text=[f'{rf["r2"] * 100:.1f}%', f'{gb["r2"] * 100:.1f}%'],
            textposition='outside',
            textfont=dict(size=13, color='var(--text-primary)', family='Sora'),
        )
    ])
    
    # Add annotation for GB advantage - positioned higher to avoid overlap
    fig_acc.add_annotation(
        x='Gradient Boosting',
        y=gb['r2'] * 100 + 4,  # Increased offset to prevent overlap
        text=f'+{accuracy_diff:.1f}% better',
        showarrow=False,
        font=dict(size=12, color='#10b981', family='Sora', weight='bold'),
        bgcolor='rgba(16,185,129,0.15)',
        bordercolor='rgba(16,185,129,0.3)',
        borderwidth=1,
        borderpad=6
    )
    
    fig_acc.update_layout(
        xaxis=dict(
            tickfont=dict(family='Sora', size=11, color='var(--text-secondary)'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)'
        ),
        yaxis=dict(
            tickfont=dict(family='Sora', size=11, color='#475569'),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.08)',
            title='Accuracy (%)'
        ),
        plot_bgcolor='var(--bg-app)',
        paper_bgcolor='var(--bg-app)',
        margin=dict(l=60, r=20, t=40, b=60),
        height=300,
        bargap=0.4,
        showlegend=False
    )
    
    st.plotly_chart(fig_acc, use_container_width=True)
    
    # Chart legend
    st.markdown('''
    <div class="chart-legend">
        <span>🔵 Random Forest</span>
        <span>🟣 Gradient Boosting</span>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ── KEY TAKEAWAYS ──
st.markdown('<div class="section-label-text" style="margin: 32px 0 16px; border-left: 3px solid #818cf8; padding-left: 12px;">Key Takeaways</div>', unsafe_allow_html=True)

st.markdown(f'''
<div class="takeaways-grid">
    <div class="takeaway-card-purple">
        <div class="takeaway-icon">🎯</div>
        <div class="takeaway-title">GB Wins on Accuracy</div>
        <div class="takeaway-body">{gb['r2'] * 100:.1f}% vs {rf['r2'] * 100:.1f}% — Gradient Boosting explains more salary variance</div>
    </div>
    <div class="takeaway-card-purple">
        <div class="takeaway-icon">📉</div>
        <div class="takeaway-title">GB Wins on Precision</div>
        <div class="takeaway-body">${gb['rmse']:,.0f} vs ${rf['rmse']:,.0f} — lower average prediction error</div>
    </div>
    <div class="takeaway-card-gold">
        <div class="takeaway-icon-gold">🏆</div>
        <div class="takeaway-title">Recommended: Gradient Boosting</div>
        <div class="takeaway-body">Consistently outperforms RF across both key metrics</div>
    </div>
</div>
''', unsafe_allow_html=True)
