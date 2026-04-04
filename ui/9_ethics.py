import streamlit as st
import pandas as pd
import plotly.express as px
from ml.src.fairness import run_bias_audit
from ml.src.monitoring import detect_live_drift

st.set_page_config(page_title="Ethics & Fairness", page_icon="🛡️", layout="wide")

st.title("🛡️ Ethical AI & Bias Auditor")
st.markdown("Mathematical transparency into systemic biases, demographic parity, and live predictive drift tracking of the Salary Intelligence Platform.")

# Header info
st.info("**AI Manifesto:** We explicitly acknowledge that machine learning models amplify historical dataset inequalities if left unchecked. This dashboard mathematically tracks statistical parity to isolate potential discrimination.")

with st.spinner("Running full bias audit & drift analysis..."):
    try:
        report = run_bias_audit()
        drift = detect_live_drift()
    except Exception as e:
        st.error(f"Audit Exception: {e}")
        st.stop()

# --- Top metrics ---
c1, c2, c3 = st.columns(3)
score = report["fairness_score"]
color = "green" if score >= 80 else "orange" if score >= 60 else "red"
c1.metric("Overall Fairness Score", f"{score}/100", delta=f"{score-100 if score < 100 else 0}%")
c2.metric("Records Analyzed", f"{report['records_analyzed']:,}")
c3.metric("Bias Flags", f"{len(report['bias_flags'])}")

# --- Main Dashboard ---
tab1, tab2, tab3, tab4 = st.tabs(["Dimension Analysis", "Bias Flags", "Bias Narrative", "Live Drift"])

with tab1:
    st.subheader("Statistical Parity by Dimension")
    st.write("Bars show group median vs global median (1.0 = perfect parity). Red bars indicate breached 80% rule.")
    
    col_sel = st.selectbox("Select Dimension to Isolate", list(report["dimensions"].keys()))
    dim_data = pd.DataFrame(report["dimensions"][col_sel])
    
    # Visual chart
    fig = px.bar(
        dim_data, 
        x='group', 
        y='impact_ratio', 
        color='status',
        color_discrete_map={
            "Fair": "#4CAF50",
            "Flagged - Underrepresented": "#F44336",
            "Flagged - Overrepresented": "#FF9800"
        },
        labels={'impact_ratio': 'Impact Ratio (Global=1.0)', 'group': col_sel.replace('_', ' ').title()},
        title=f"Disparate Impact Analysis: {col_sel.replace('_', ' ').title()}"
    )
    fig.add_hline(y=1.0, line_dash="dash", line_color="white", annotation_text="Global Parity")
    fig.add_hline(y=0.8, line_dash="dot", line_color="red", annotation_text="Lower Threshold (80%)")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Table data
    st.dataframe(dim_data[['group', 'median', 'gini', 'impact_ratio', 'status']].rename(columns={
        'group': 'Value', 'median': 'Median Salary', 'gini': 'Inequality (Gini)', 'impact_ratio': 'Parity Ratio'
    }), use_container_width=True)

with tab2:
    st.subheader("Active Bias Flags")
    if not report["bias_flags"]:
        st.success("✅ No critical bias patterns detected based on current thresholds.")
    else:
        flags_df = pd.DataFrame(report["bias_flags"])
        st.table(flags_df.rename(columns={
            'dimension': 'Dimension', 'group': 'Category', 'ratio': 'Ratio to Global', 'status': 'Critique'
        }))

with tab3:
    st.subheader("AI-Generated Bias Narrative")
    for bullet in report["narrative"]:
        if "Skewed" in bullet or "Lower" in bullet:
            st.warning(f"- {bullet}")
        else:
            st.success(f"- {bullet}")

with tab4:
    st.subheader("Live Operational Drift Monitoring")
    # Using existing logic from original ethics page
    if "error" in drift:
        st.warning(drift["error"])
    elif drift.get("status") == "Awaiting Live Data":
        st.info(drift["message"])
    else:
        st.metric("Live Postgres Queries Analyzed", f"{drift['live_queries_analyzed']}")
        
        cA, cB = st.columns(2)
        cA.metric("Historical Training Median", f"${drift['historic_median']:,.0f}")
        cB.metric("Live Inference Median", f"${drift['live_inference_median']:,.0f}")
        
        if abs(drift["drift_z_score"]) > 1.5:
            st.error(f"⚠️ {drift['status']} (Z-Score: {drift['drift_z_score']}) - Recalibration Highly Recommended.")
        else:
            st.success(f"✅ System Intact. Structural drift within mathematical bounds (Z-Score: {drift['drift_z_score']}).")

st.divider()
st.subheader("Known Global Model Limitations")
st.markdown("""
1. **Reporting Bias**: Salary figures are self-reported and skewed heavily towards US-centric hubs. Approximations for low-count regions operate with substantially widened interpolation limits.
2. **Missing Inflation Dynamics**: Unless actively patched by our `inflation_adjusted` pipeline, raw models intrinsically undervalue current macroeconomic dynamics natively stored in older dataset rows.
3. **Implicit Demographics**: The model actively abstracts away Age and Gender to deliberately restrict targeted discrimination logic inside the decision trees.
""")
