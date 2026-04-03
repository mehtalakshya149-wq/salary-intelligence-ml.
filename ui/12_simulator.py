import streamlit as st
from ml.src.predict import run_prediction
from app import page_header, result_card, empty_state

st.set_page_config(page_title="What-If Simulator", page_icon="🎛️", layout="wide")

page_header("Career Simulator", "What-If Salary Modeler", "Adjust your core levers like experience and skills to instantly recompute your market value prediction without manual submits.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to use the What-If Simulator.")
    st.stop()

# Base layout setup
col_inputs, col_outputs = st.columns([1, 2], gap="large")

with col_inputs:
    st.markdown("### Adjust Levers")
    st.markdown("<p style='font-size:13px;color=gray'>Any change made here will instantly compute a new salary simulation.</p>", unsafe_allow_html=True)
    
    # Currency & Location Config
    CURRENCY_MAP = {
        "US": {"symbol": "$", "rate": 1.0, "name": "United States"},
        "GB": {"symbol": "£", "rate": 0.8, "name": "United Kingdom"},
        "CA": {"symbol": "$", "rate": 1.35, "name": "Canada"},
        "DE": {"symbol": "€", "rate": 0.92, "name": "Germany"},
        "IN": {"symbol": "₹", "rate": 83.0, "name": "India"},
        "FR": {"symbol": "€", "rate": 0.92, "name": "France"},
        "ES": {"symbol": "€", "rate": 0.92, "name": "Spain"},
        "AU": {"symbol": "$", "rate": 1.5, "name": "Australia"},
        "BR": {"symbol": "R$", "rate": 5.0, "name": "Brazil"},
        "JP": {"symbol": "¥", "rate": 150.0, "name": "Japan"}
    }
    
    # Notice we don't use 'with st.form' here. Streamlit natively responds to widget changes.
    job_title = st.selectbox("Simulated Job Title", ["Data Scientist", "ML Engineer", "Data Analyst", "Data Engineer", "AI Researcher"])
    exp = st.select_slider("Experience Level", options=["EN", "MI", "SE", "EX"], value="MI")
    
    # Expand location options
    loc_options = list(CURRENCY_MAP.keys())
    loc = st.selectbox("Company Location", options=loc_options, index=0)
    
    rem = st.slider("Remote Work Ratio (%)", min_value=0, max_value=100, step=50, value=100)
    skills = st.text_area("Skillset", value="Python, SQL")
    
    # Get currency details
    curr_symbol = CURRENCY_MAP[loc]["symbol"]
    curr_rate = CURRENCY_MAP[loc]["rate"]

    # We will freeze some sensible defaults behind the scenes so the model doesn't complain
    emp = "FT"
    size = "M"
    yr = 2024

with col_outputs:
    st.markdown("### Real-Time Simulation Result")
    
    inputs = {
        "job_title": job_title, 
        "experience_level": exp,
        "employment_type": emp, 
        "company_location": loc,
        "company_size": size, 
        "remote_ratio": rem,
        "skills": skills, 
        "work_year": int(yr)
    }
    
    if not job_title or not loc:
        empty_state("⏳", "Incomplete Data", "Fill out the fields to instantly see the simulation.")
    else:
        try:
            res = run_prediction(inputs, "ml/config.yaml")
            
            # Convert USD results to local currency
            median = res['salary']['average'] * curr_rate
            low = res['salary']['min'] * curr_rate
            high = res['salary']['max'] * curr_rate
            adj = res['inflation_adjusted']['adjusted'] * curr_rate
            
            # Show big main card for the adjusted value
            result_card("SIMULATED MEDIAN SALARY", f"{curr_symbol}{median:,.0f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Low Band (P10)", f"{curr_symbol}{low:,.0f}")
            c2.metric("Inflation Adj (2024)", f"{curr_symbol}{adj:,.0f}")
            c3.metric("High Band (P90)", f"{curr_symbol}{high:,.0f}")
            
            # Minor confidence text
            conf_str = f"**Confidence Score:** {res['confidence']['score']}%"
            if res['confidence']['score'] > 85:
                st.success(conf_str)
            else:
                st.warning(conf_str)
                
            st.markdown("<hr style='margin-bottom: 0'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:12px;color=grey'><em>This simulation relies purely on existing model weights and inference caching. No retraining has occurred during this computation.</em></p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Inference error computing simulation: {e}")
