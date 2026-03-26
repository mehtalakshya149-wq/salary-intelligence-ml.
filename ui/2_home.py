import streamlit as st
from ml.src.salary_trends import get_trend_report

# Header Area with User Details
col1, col2 = st.columns([4, 1])
col1.title("🏠 Platform Overview")
if col2.button("Logout", key="logout_btn"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()

st.markdown(f"**Welcome back, {st.session_state.username}!** Here is the live status of the Salary AI models.")

with st.spinner("Loading dataset trends..."):
    try:
        report = get_trend_report("ml/config.yaml")
        summary = report["data_summary"]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Extracted Records", f"{summary['total_records']:,}")
        c2.metric("Median Machine Salary", f"${summary['overall_median']:,.0f}")
        c3.metric("Data Range", summary["year_range"])
        
        st.divider()
        st.subheader("Aggregate Yearly Data Trends")
        st.dataframe(report["yearly_stats"], use_container_width=True)
        
    except Exception as e:
        st.warning("Failed to load aggregate stats. Ensure pipeline data exists in `ml/data/processed/salaries_clean.csv`.")
        st.error(f"Details: {e}")
