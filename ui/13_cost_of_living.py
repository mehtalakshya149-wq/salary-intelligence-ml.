import streamlit as st
import pandas as pd
from api.cost_of_living import get_cost_of_living_adjusted_salary, COST_OF_LIVING_INDICES
from app import page_header, result_card, stat_card

st.set_page_config(page_title="Cost of Living Adjuster", page_icon="🌍", layout="wide")

page_header("Global Mobility", "Cost of Living Adjuster", "Convert your current salary across global tech hubs to understand true purchasing power and evaluate international offers.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to access the Cost of Living tools.")
    st.stop()

st.markdown("### Input Current Conditions")
col1, col2 = st.columns([1, 1])
countries = list(COST_OF_LIVING_INDICES.keys())
with col1:
    base_salary = st.number_input("Base Salary (Annual USD)", min_value=10000, max_value=2000000, value=120000, step=5000)
with col2:
    base_country = st.selectbox("Current Location", options=countries, index=countries.index("United States"))

try:
    data = get_cost_of_living_adjusted_salary(base_salary, base_country)
    comparisons = data.comparisons
except Exception as e:
    st.error(f"Computation Error: {e}")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📊 Real Purchasing Power Equivalence")
st.markdown(f"<p style='font-size: 14px; color: gray'>The chart below illustrates the exact salary you would need in each country to maintain the same lifestyle that <b>${base_salary:,.0f}</b> provides in <b>{base_country}</b>.</p>", unsafe_allow_html=True)

# Prepare dataframe for charting
df = pd.DataFrame([{
    "Country": c.target_country,
    "Salary Required": c.target_salary_required
} for c in comparisons])

# Add the base country for visual reference
df.loc[len(df)] = {"Country": f"{base_country} (Base)", "Salary Required": base_salary}

# Clean styling chart
st.bar_chart(df.set_index("Country")["Salary Required"])

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### Country Detail Breakdown")
col_cards1, col_cards2, col_cards3 = st.columns(3)

cols = [col_cards1, col_cards2, col_cards3]
for idx, comp in enumerate(comparisons):
    col = cols[idx % 3]
    with col:
        # If PP ratio > 1, the target country is cheaper. So you have stronger PP
        if comp.purchasing_power_ratio > 1:
            delta_str = f"+{(comp.purchasing_power_ratio - 1)*100:.0f}% Purchasing Power"
            positive = True
        else:
            delta_str = f"-{(1 - comp.purchasing_power_ratio)*100:.0f}% Purchasing Power"
            positive = False
            
        stat_card(comp.target_country.upper(), f"${comp.target_salary_required:,.0f}", delta=delta_str, positive=positive)
