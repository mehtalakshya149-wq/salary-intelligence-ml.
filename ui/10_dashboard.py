import streamlit as st
import pandas as pd
from api.database import SessionLocal
from api.dashboard import get_prediction_history, get_analytics

# Helper functions provided heavily in app.py to be accessed 
from app import page_header, stat_card, section_label, result_card, banner, empty_state

st.set_page_config(page_title="Personalized Dashboard", page_icon="📈", layout="wide")

page_header("Your insights", "Personalized Dashboard", "Monitor your prediction history, view salary growth trends, and discover skills to increase your market value.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to view your personalized dashboard.")
    st.stop()

username = st.session_state.username

# Data Fetching
try:
    db = SessionLocal()
    history_data = get_prediction_history(username=username, db=db)
    analytics_data = get_analytics(username=username, db=db)
    db.close()
except Exception as e:
    st.error(f"Error fetching dashboard data: {e}")
    st.stop()

predictions = history_data.get("history", [])
market_value_score = analytics_data.get("market_value_score", 0.0)
salary_growth = analytics_data.get("salary_growth", [])
recommendations = analytics_data.get("recommendations", [])
total_preds = analytics_data.get("total_predictions", 0)

# Main Metrics Row
c1, c2 = st.columns(2)
with c1:
    stat_card("MARKET VALUE SCORE", f"{market_value_score}/100", "+2.5 from last time" if market_value_score > 60 else "")
with c2:
    stat_card("TOTAL PREDICTIONS", str(total_preds), "Activity Metric", positive=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Content
col_main, col_side = st.columns([2, 1])

with col_main:
    section_label("Salary Growth Trajectory")
    if len(salary_growth) > 1:
        # Create line chart
        df_growth = pd.DataFrame(salary_growth)
        df_growth["date"] = pd.to_datetime(df_growth["date"])
        df_growth.set_index("date", inplace=True)
        st.line_chart(df_growth["predicted_salary"], use_container_width=True)
    elif len(salary_growth) == 1:
        st.info("You've made one prediction so far. Keep predicting salaries for new roles to generate an interactive growth chart!")
    else:
        empty_state("📉", "No Data Available", "Make your first salary prediction to see your growth.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    section_label("Prediction History")
    if predictions:
        # Format history as dataframe
        hist_data = [{
            "Date": p.created_at.strftime("%Y-%m-%d %H:%M"),
            "Role": p.job_title,
            "Experience": p.experience_level,
            "Location": p.company_location,
            "Predicted Salary": f"${p.predicted_average:,.0f}"
        } for p in predictions]
        
        st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)
    else:
        empty_state("🕒", "No Prediction History", "Your past predictions will appear here.")

with col_side:
    section_label("Skill Recommendations")
    if recommendations:
        banner("💡 **Top skills to boost your salary** based on your latest roles.", variant="info")
        for skill in recommendations:
            st.markdown(f"- **{skill}**")
        st.markdown("<br><p style='font-size: 13px; color: var(--text-muted);'>Try adding these to your profile and run a new prediction!</p>", unsafe_allow_html=True)
    else:
        banner("Make a prediction first to get skill recommendations.", variant="warning")
