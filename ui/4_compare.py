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
    filter_col = col1.selectbox("Filter Demographic", ["job_title", "experience_level", "company_location", "company_size", "employment_type"])
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
                
                trend = res["trend"]
                st.success(f"**Model Observation:** {trend['interpretation']}")

                # Show the Extrapolations (Forecast)
                st.subheader("🔮 Extrapolated Trajectories")
                df_forecast = pd.DataFrame(res["forecast"])
                for col in ["predicted_median", "confidence_low", "confidence_high"]:
                    if col in df_forecast.columns:
                        df_forecast[col] = df_forecast[col].apply(lambda x: f"${x:,.0f}")
                df_forecast = df_forecast.rename(columns={
                    "year": "Year", "predicted_median": "Predicted Median",
                    "confidence_low": "95% CI Low", "confidence_high": "95% CI High"
                })
                st.dataframe(df_forecast, use_container_width=True)
                
except Exception as e:
    st.error(f"Failed to isolate dataset streams. Exception Output: {e}")
