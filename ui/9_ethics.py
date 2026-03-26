import streamlit as st
import pandas as pd
from ml.src.fairness import get_fairness_report
from ml.src.monitoring import detect_live_drift

st.title("🛡️ Ethical AI & System Robustness")
st.markdown("Absolute transparency into the structural limitations, inherent systemic biases, and live predictive drift tracking of the Random Forest ensemble.")

st.info("**AI Manifesto:** We explicitly acknowledge that machine learning models amplify historical dataset inequalities if left unchecked. This dashboard mathematically tracks demographic representations to isolate potential discrimination alongside live model degradation boundaries.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bias & Statistical Fairness")
    with st.spinner("Calculating mathematical Disparate Impact across protected attributes..."):
        try:
            report = get_fairness_report()
            st.success(f"Evaluated across {report['records_evaluated']:,} structural records.")
            
            st.write("##### Structural Equity by Experience Level")
            exp = report["experience_level_bias"]["group_medians"]
            df_exp = pd.DataFrame(list(exp.items()), columns=["Proxy", "Median Bound ($)"])
            st.dataframe(df_exp, use_container_width=True)
            
            flags = report["experience_level_bias"]["disparate_impact_flags"]
            if flags:
                st.warning("⚠️ Traditional 80% Disparate Impact limits breached for:")
                for k, v in flags.items():
                    st.write(f"- **{k}**: {v['status']} (Ratio: {v['ratio_to_global']}x global)")
            else:
                st.success("Strict mathematical parity achieved across demographic bounds.")
        except Exception as e:
            st.error(f"Fairness Evaluation Exception: {e}")

with col2:
    st.subheader("Live Operational Monitoring")
    with st.spinner("Connecting to Postgres Live Inference Streams..."):
        try:
            drift = detect_live_drift()
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
                    
        except Exception as e:
            st.error(f"Monitoring Exception: {e}")

st.divider()
st.subheader("Known Global Model Limitations")
st.markdown("""
1. **Reporting Bias**: Salary figures are self-reported and skewed heavily towards US-centric hubs. Approximations for low-count regions operate with substantially widened interpolation limits.
2. **Missing Inflation Dynamics**: Unless actively patched by our `inflation_adjusted` pipeline, raw models intrinsically undervalue current macroeconomic dynamics natively stored in older dataset rows.
3. **Implicit Demographics**: The model actively abstracts away Age and Gender to deliberately restrict targeted discrimination logic inside the decision trees.
""")
