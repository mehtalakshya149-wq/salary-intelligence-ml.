import streamlit as st
import pandas as pd
import plotly.express as px
from ml.src.preprocess import load_data, clean_data, load_config

st.set_page_config(page_title="Global Salary Heatmap", page_icon="🌍", layout="wide")

st.title("🌍 Global Salary Heatmap")
st.markdown("Visualize compensation distributions across international borders based on historical data aggregates.")

# Country Code Mapping (ISO-2 to ISO-3 for Plotly)
ISO2_TO_ISO3 = {
    'AU': 'AUS', 'BR': 'BRA', 'CA': 'CAN', 'DE': 'DEU', 
    'ES': 'ESP', 'FR': 'FRA', 'GB': 'GBR', 'IN': 'IND', 
    'NL': 'NLD', 'US': 'USA'
}

try:
    config = load_config("ml/config.yaml")
    df_raw = load_data(config["paths"]["raw_data"])
    df = clean_data(df_raw, config)
    
    # Sidebar Filters
    st.sidebar.header("Map Filters")
    job_titles = ["All"] + sorted(df["job_title"].unique().tolist())
    selected_title = st.sidebar.selectbox("Filter by Job Title", job_titles)
    
    exp_levels = ["All"] + sorted(df["experience_level"].unique().tolist())
    selected_exp = st.sidebar.selectbox("Filter by Experience Level", exp_levels)
    
    # Apply Filters
    df_filtered = df.copy()
    if selected_title != "All":
        df_filtered = df_filtered[df_filtered["job_title"] == selected_title]
    if selected_exp != "All":
        df_filtered = df_filtered[df_filtered["experience_level"] == selected_exp]
        
    if df_filtered.empty:
        st.warning("No data found for the selected filters. Please adjust your criteria.")
    else:
        # Aggregate by country
        geo_stats = df_filtered.groupby("company_location").agg(
            median_salary=("salary_in_usd", "median"),
            avg_salary=("salary_in_usd", "mean"),
            count=("salary_in_usd", "count")
        ).reset_index()
        
        # Map to ISO-3 (ensure uppercase for mapping)
        geo_stats["iso_alpha"] = geo_stats["company_location"].str.upper().map(ISO2_TO_ISO3)
        
        # Plotly Choropleth
        fig = px.choropleth(
            geo_stats,
            locations="iso_alpha",
            color="median_salary",
            hover_name="company_location",
            hover_data=["avg_salary", "count"],
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Median Salary Distribution (USD) - {selected_title}",
            labels={'median_salary': 'Median Salary ($)', 'iso_alpha': 'Country'}
        )
        
        fig.update_layout(
            margin={"r":0, "t":50, "l":0, "b":0},
            coloraxis_colorbar=dict(title="Median Salary"),
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display Stats Table
        st.subheader("Country-Level Benchmarks")
        display_df = geo_stats.sort_values("median_salary", ascending=False).copy()
        display_df["median_salary"] = display_df["median_salary"].apply(lambda x: f"${x:,.0f}")
        display_df["avg_salary"] = display_df["avg_salary"].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(display_df.rename(columns={
            "company_location": "Country Code",
            "median_salary": "Median",
            "avg_salary": "Average",
            "count": "Total Records"
        })[["Country Code", "Median", "Average", "Total Records"]], use_container_width=True)

except Exception as e:
    st.error(f"Failed to load geospatial data: {e}")
