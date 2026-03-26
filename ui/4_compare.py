import streamlit as st
import pandas as pd
from ml.src.salary_trends import compute_filtered_trends, load_data, clean_data, load_config

st.title("📊 Trend Comparison & Benchmarking")
st.markdown("Compare dynamic compensation aggregates based on granular sub-filters like remote modality.")

try:
    config = load_config("ml/config.yaml")
    df = clean_data(load_data(config["paths"]["raw_data"]), config)
    
    st.info("Powered by structural Time-Series Regressors natively bridging historical inputs.")
    
    col1, col2 = st.columns(2)
    filter_col = col1.selectbox("Filter Demographic", ["experience_level", "company_location", "company_size"])
    # Convert everything to string for consistency
    unique_vals = sorted(list(set([str(x) for x in df[filter_col].dropna().unique()])))
    filter_val = col2.selectbox("Isolate Specific Target", unique_vals)
    
    if st.button("Generate Extrapolations", type="primary"):
        with st.spinner("Computing time-series trajectories..."):
            res = compute_filtered_trends(df, filter_col, filter_val, n_forecast_years=1)
            if "error" in res:
                st.warning(res["error"])
            else:
                st.subheader(f"Historical Isolations for {filter_col.replace('_', ' ').title()}: `{filter_val}`")
                df_out = pd.DataFrame(res["yearly_stats"])
                st.dataframe(df_out, use_container_width=True)
                
                trend = res["trend"]
                st.success(f"**Model Observation:** {trend['interpretation']}")
                
except Exception as e:
    st.error(f"Failed to isolate dataset streams. Exception Output: {e}")
