import streamlit as st
import pandas as pd
from ml.src.skill_roi import get_roi_report

st.set_page_config(page_title="Skill ROI Calculator", page_icon="💡", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM SKILL ROI CALCULATOR STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-left, #1c1408 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 28px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #eab308;
    margin-bottom: 12px;
}

.header-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
    display: inline-block;
}

.roi-badge {
    background: rgba(234, 179, 8, 0.15);
    color: #eab308;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
    margin-left: 10px;
    vertical-align: middle;
    display: inline-block;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 580px;
}

/* ── Section Label ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    border-left: 3px solid #eab308;
    padding-left: 10px;
    margin-bottom: 16px;
}

/* ── Input Row ── */
.input-row {
    display: flex;
    gap: 16px;
    align-items: flex-end;
    margin-bottom: 20px;
}

.input-column {
    flex: 1;
}

.field-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    display: block;
}

/* ── Input & Selectbox Styling ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #3b2f00 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input {
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

.stTextInput > div > div > input:focus {
    border-color: #eab308 !important;
    box-shadow: 0 0 0 3px rgba(234, 179, 8, 0.12) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    padding: 0 !important;
}

.stSelectbox > div > div:hover {
    border-color: #eab308 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Skill Tags ── */
.skill-tags {
    display: inline-flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 6px;
}

.skill-tag {
    background: rgba(234, 179, 8, 0.1);
    color: #eab308;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 11px;
}

/* ── Calculate Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ca8a04, #eab308) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 32px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 20px !important;
    line-height: normal !important;
    width: auto !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(110%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(234, 179, 8, 0.35) !important;
}

/* ── Top Recommendation Banner ── */
.recommendation-banner {
    background: linear-gradient(135deg, rgba(234,179,8,0.1), rgba(234,179,8,0.05));
    border: 1px solid rgba(234, 179, 8, 0.25);
    border-radius: 14px;
    padding: 18px 24px;
    margin-top: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.recommendation-left {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
}

.recommendation-icon {
    color: #eab308;
    font-size: 20px;
}

.recommendation-label {
    color: #eab308;
    font-weight: 700;
    font-size: 13px;
}

.recommendation-text {
    color: #e2e8f0;
    font-size: 13px;
    line-height: 1.6;
}

.skill-pill {
    background: rgba(234, 179, 8, 0.15);
    color: #eab308;
    border-radius: 6px;
    padding: 1px 10px;
    font-weight: 700;
}

.impact-positive {
    color: #10b981;
    font-weight: 700;
    font-size: 14px;
}

.impact-negative {
    color: #ef4444;
    font-weight: 700;
    font-size: 14px;
}

.impact-mixed {
    color: #f59e0b;
    font-weight: 700;
    font-size: 14px;
}

.view-details-link {
    color: #eab308;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    white-space: nowrap;
    cursor: pointer;
}

.view-details-link:hover {
    text-decoration: underline;
}

/* ── Table Container ── */
.table-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    overflow: hidden;
    margin-top: 24px;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #eab308;
    padding-left: 12px;
    margin-bottom: 16px;
}

/* ── HTML Table Styling ── */
.custom-table {
    width: 100%;
    border-collapse: collapse;
}

.custom-table thead {
    background: rgba(234, 179, 8, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.custom-table th {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 14px 20px;
    text-align: left;
}

.custom-table tbody tr {
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 0.15s ease;
}

.custom-table tbody tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.015);
}

.custom-table tbody tr:hover {
    background: rgba(234, 179, 8, 0.05);
    border-left: 2px solid #eab308;
}

.custom-table td {
    padding: 14px 20px;
    vertical-align: middle;
}

/* ── Rank Badges ── */
.rank-badge {
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 700;
    min-width: 28px;
    text-align: center;
    display: inline-block;
}

.rank-gold {
    background: #eab308;
    color: #000000;
}

.rank-silver {
    background: var(--text-secondary);
    color: #000000;
}

.rank-bronze {
    background: #b45309;
    color: var(--text-primary);
}

.rank-plain {
    background: var(--surface-2);
    color: var(--text-secondary);
}

/* ── Impact Values ── */
.impact-up {
    color: #10b981;
    font-weight: 700;
    font-size: 13px;
}

.impact-down {
    color: #ef4444;
    font-weight: 700;
    font-size: 13px;
}

.impact-mixed-val {
    color: #f59e0b;
    font-weight: 700;
    font-size: 13px;
}

/* ── Salary Bars ── */
.salary-bar-container {
    display: flex;
    align-items: center;
    gap: 8px;
}

.salary-bar {
    height: 3px;
    border-radius: 999px;
    flex: 1;
}

.salary-bar-positive {
    background: #10b981;
}

.salary-bar-negative {
    background: #ef4444;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stDataframe {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="page-header">
    <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="12" y1="1" x2="12" y2="23"></line>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
    </svg>
    <h1 class="header-title">Skill ROI Calculator</h1>
    <span class="roi-badge">ROI Engine</span>
    <p class="header-subtitle">Quantify exactly how much acquiring a specific new tool impacts your compensation tier via structural perturbation.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Your Profile</div>', unsafe_allow_html=True)

# Experience level mapping
exp_mapping = {"EN": "Entry", "MI": "Mid Level", "SE": "Senior", "EX": "Executive"}
exp_options = ["EN", "MI", "SE", "EX"]
exp_labels = ["Entry", "Mid Level", "Senior", "Executive"]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<label class="field-label">Current Role</label>', unsafe_allow_html=True)
    job_title = st.text_input("", value="Data Analyst", label_visibility="collapsed", key="job_title_input")

with col2:
    st.markdown('<label class="field-label">Current Skills</label>', unsafe_allow_html=True)
    skills = st.text_input("", value="SQL, Excel", label_visibility="collapsed", key="skills_input")
    
    # Show skill tags
    if skills.strip():
        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        tags_html = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in skills_list])
        st.markdown(f'<div class="skill-tags">{tags_html}</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<label class="field-label">Experience Level</label>', unsafe_allow_html=True)
    exp_index = exp_options.index("MI")  # Default to MI
    exp_label = st.selectbox("", exp_labels, index=exp_index, label_visibility="collapsed", key="exp_select")
    exp = exp_options[exp_labels.index(exp_label)]

# Calculate button
calc_btn = st.button("⚡ Calculate Marginal ROI Impacts", type="primary")

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if calc_btn:
    with st.spinner("Analyzing high-dimensional skill permutations via Random Forest Evaluator..."):
        try:
            profile = {
                "job_title": job_title, "skills": skills, "experience_level": exp,
                "employment_type": "FT", "company_location": "US", "company_size": "L", "remote_ratio": 100, "work_year": 2024
            }
            res = get_roi_report(profile, "ml/config.yaml")
            
            if "message" in res:
                st.warning(res["message"])
            else:
                # Top Recommendation Banner
                best_skill = res['best_skill']
                best_impact = res['best_impact_pct']
                
                # Determine impact color
                if '+' in str(best_impact) and '-' not in str(best_impact):
                    impact_class = "impact-positive"
                    impact_icon = "↑"
                elif '-' in str(best_impact):
                    impact_class = "impact-negative"
                    impact_icon = "↓"
                else:
                    impact_class = "impact-mixed"
                    impact_icon = "↔"
                
                st.markdown(f'''
                <div class="recommendation-banner">
                    <div class="recommendation-left">
                        <span class="recommendation-icon">🏆</span>
                        <div>
                            <span class="recommendation-label">Top Recommendation:</span>
                            <span class="recommendation-text"> Target acquiring <span class="skill-pill">{best_skill}</span> for a projected </span>
                            <span class="{impact_class}">{impact_icon} {best_impact}%</span>
                            <span class="recommendation-text"> initial uplift!</span>
                        </div>
                    </div>
                    <a class="view-details-link">View Details →</a>
                </div>
                ''', unsafe_allow_html=True)
                
                # Global Skill Rankings
                st.markdown('<div class="section-heading">Global Skill Rankings</div>', unsafe_allow_html=True)
                df = pd.DataFrame(res["ranked_skills"])
                
                # Build custom HTML table
                table_html = '<div class="table-container"><table class="custom-table"><thead><tr>'
                table_html += '<th>Rank</th><th>Skill Name</th><th>Impact %</th><th>Salary Change</th><th>Base Salary</th><th>New Salary</th>'
                table_html += '</tr></thead><tbody>'
                
                for idx, row in df.iterrows():
                    # Rank badge
                    if idx == 0:
                        rank_class = "rank-gold"
                        rank_display = "🥇"
                    elif idx == 1:
                        rank_class = "rank-silver"
                        rank_display = "🥈"
                    elif idx == 2:
                        rank_class = "rank-bronze"
                        rank_display = "🥉"
                    else:
                        rank_class = "rank-plain"
                        rank_display = str(idx)
                    
                    # Impact display
                    impact_val = row['impact_pct']
                    if '+' in str(impact_val) and '-' not in str(impact_val):
                        impact_class = "impact-up"
                        impact_display = f"↑ +{impact_val}%"
                    elif '-' in str(impact_val):
                        impact_class = "impact-down"
                        impact_display = f"↓ {impact_val}%"
                    else:
                        impact_class = "impact-mixed-val"
                        impact_display = f"↔ {impact_val}%"
                    
                    # Salary increase
                    salary_inc = row['salary_increase']
                    salary_abs = abs(salary_inc)
                    if salary_inc > 0:
                        salary_class = "salary-bar-positive"
                        salary_color = "#10b981"
                        salary_icon = "↑"
                    elif salary_inc < 0:
                        salary_class = "salary-bar-negative"
                        salary_color = "#ef4444"
                        salary_icon = "↓"
                    else:
                        salary_class = "salary-bar-positive"
                        salary_color = "var(--text-secondary)"
                        salary_icon = "→"
                    
                    # Bar width (normalize to max 100px)
                    max_salary = df['salary_increase'].abs().max()
                    bar_width = (salary_abs / max_salary * 100) if max_salary > 0 else 0
                    
                    table_html += f'<tr>'
                    table_html += f'<td><span class="rank-badge {rank_class}">{rank_display}</span></td>'
                    table_html += f'<td style="font-size: 14px; font-weight: 600; color: var(--text-primary);">{row["skill"]}</td>'
                    table_html += f'<td><span class="{impact_class}">{impact_display}</span></td>'
                    table_html += f'''<td>
                        <div class="salary-bar-container">
                            <span style="color: {salary_color}; font-weight: 600; min-width: 90px;">{salary_icon} ${salary_abs:,.0f}</span>
                            <div class="salary-bar {salary_class}" style="width: {bar_width}px;"></div>
                        </div>
                    </td>'''
                    table_html += f'<td style="color: var(--text-secondary); font-size: 13px;">${row["base_salary"]:,.0f}</td>'
                    table_html += f'<td style="color: var(--text-primary); font-weight: 600; font-size: 13px;">${row["new_salary"]:,.0f}</td>'
                    table_html += '</tr>'
                
                table_html += '</tbody></table></div>'
                st.markdown(table_html, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Model calculation failed. Verify `ml/models` are fully populated. Error: {e}")
