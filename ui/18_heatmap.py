import streamlit as st
import pandas as pd
import plotly.express as px
from ml.src.preprocess import load_data, clean_data, load_config

st.set_page_config(page_title="Global Salary Heatmap", page_icon="🌍", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM GLOBAL SALARY HEATMAP STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top-center, #001a2e 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 24px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #0ea5e9;
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

.live-badge {
    background: rgba(14, 165, 233, 0.15);
    color: #0ea5e9;
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

/* ── Filter Pills ── */
.filter-row {
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 16px;
}

.filter-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 600;
}

.filter-pills {
    display: inline-flex;
    gap: 8px;
}

.filter-pill {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.filter-pill.active {
    background: rgba(14, 165, 233, 0.12);
    border-color: rgba(14, 165, 233, 0.3);
    color: #0ea5e9;
    font-weight: 600;
}

.filter-pill:hover {
    border-color: rgba(14, 165, 233, 0.2);
    color: #0ea5e9;
}

/* ── Map Container ── */
.map-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    padding: 0;
    margin-bottom: 24px;
}

.map-title {
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    padding: 20px 24px 0 24px;
}

.stat-pills {
    padding: 12px 24px;
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
}

.stat-pill {
    font-size: 12px;
    color: var(--text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #0ea5e9;
    padding-left: 12px;
    margin: 32px 0 16px;
}

/* ── Search Bar ── */
.search-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 16px;
}

.search-input {
    background: var(--surface-2);
    border: 1px solid #0c2a3d;
    border-radius: 10px;
    padding: 10px 16px 10px 40px;
    color: var(--text-primary);
    font-size: 13px;
    width: 280px;
    font-family: 'Sora', sans-serif;
    transition: all 0.2s ease;
}

.search-input:focus {
    border-color: #0ea5e9;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12);
    outline: none;
}

.search-input::placeholder {
    color: #475569;
}

/* ── Table Container ── */
.table-container {
    background: var(--surface-glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}

/* ── HTML Table Styling ── */
.custom-table {
    width: 100%;
    border-collapse: collapse;
}

.custom-table thead {
    background: var(--accent-light);
    border-bottom: 1px solid var(--border);
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
    border-bottom: 1px solid var(--border);
    transition: all 0.15s ease;
}

.custom-table tbody tr:nth-child(even) {
    background: var(--surface-glass);
}

.custom-table tbody tr:hover {
    background: rgba(14, 165, 233, 0.05);
    border-left: 2px solid #0ea5e9;
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
    display: inline-block;
}

.rank-1 {
    background: rgba(234, 179, 8, 0.2);
    color: #eab308;
}

.rank-2 {
    background: rgba(148, 163, 184, 0.2);
    color: var(--text-secondary);
}

.rank-3 {
    background: rgba(180, 83, 9, 0.2);
    color: #b45309;
}

.rank-plain {
    background: var(--surface-2);
    color: var(--text-secondary);
}

/* ── Country Code Badge ── */
.country-badge {
    background: var(--bg-surface);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
}

/* ── Salary Bar ── */
.salary-bar-container {
    display: flex;
    align-items: center;
    gap: 8px;
}

.salary-bar {
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, #0ea5e9, #7c3aed);
    max-width: 80px;
}

/* ── Records Pill ── */
.records-pill {
    background: rgba(14, 165, 233, 0.08);
    color: #0ea5e9;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* ── Pagination ── */
.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 16px;
    padding: 0 4px;
}

.pagination-text {
    font-size: 12px;
    color: #475569;
}

.pagination-buttons {
    display: flex;
    gap: 8px;
}

.page-btn {
    background: var(--surface-2);
    border: 1px solid #0c2a3d;
    border-radius: 8px;
    padding: 6px 16px;
    color: var(--text-secondary);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Sora', sans-serif;
}

.page-btn:hover {
    border-color: #0ea5e9;
    color: #0ea5e9;
}

.page-btn.disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

.stSidebar {
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
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="2" y1="12" x2="22" y2="12"></line>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>
    <h1 class="header-title">Global Salary Heatmap</h1>
    <span class="live-badge">Live Data</span>
    <p class="header-subtitle">Visualize compensation distributions across international borders based on historical data aggregates.</p>
</div>
''', unsafe_allow_html=True)

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
    
    # Initialize session state
    if 'selected_title' not in st.session_state:
        st.session_state.selected_title = "All"
    if 'selected_exp' not in st.session_state:
        st.session_state.selected_exp = "All"
    
    # Filter Row
    st.markdown('<div class="filter-row">', unsafe_allow_html=True)
    st.markdown('<span class="filter-label">Filter by:</span>', unsafe_allow_html=True)
    
    job_titles = ["All", "Data Scientist", "Software Engineer", "Data Analyst"]
    st.markdown('<div class="filter-pills">', unsafe_allow_html=True)
    for title in job_titles:
        is_active = "active" if title == st.session_state.selected_title else ""
        st.markdown(f'''<div class="filter-pill {is_active}" onclick="document.getElementById('filter-{title.replace(" ", "-")}''.click()">{title}</div>''', unsafe_allow_html=True)
        st.button("", key=f"filter-{title.replace(' ', '-')}", on_click=lambda t=title: st.session_state.update(selected_title=t), type="secondary")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply Filters
    df_filtered = df.copy()
    if st.session_state.selected_title != "All":
        df_filtered = df_filtered[df_filtered["job_title"] == st.session_state.selected_title]
        
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
        
        # Get stats for pills
        max_country = geo_stats.loc[geo_stats['median_salary'].idxmax()]
        min_salary = geo_stats['median_salary'].min()
        
        # Map Container
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="map-title">Median Salary Distribution (USD) - {st.session_state.selected_title}</div>', unsafe_allow_html=True)
        
        # Stat Pills
        st.markdown(f'''
        <div class="stat-pills">
            <span class="stat-pill">🌍 Countries Covered: {len(geo_stats)}+</span>
            <span class="stat-pill">💰 Max Salary: ${max_country['median_salary']:,.0f} ({max_country['company_location'].upper()})</span>
            <span class="stat-pill">📊 Min Salary: ${min_salary:,.0f}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Plotly Choropleth with dark theme
        fig = px.choropleth(
            geo_stats,
            locations="iso_alpha",
            color="median_salary",
            hover_name="company_location",
            hover_data=["avg_salary", "count"],
            color_continuous_scale="Plasma",
            labels={'median_salary': 'Median Salary ($)', 'iso_alpha': 'Country'}
        )
        
        fig.update_layout(
            margin={"r":0, "t":0, "l":0, "b":0},
            paper_bgcolor='var(--bg-app)',
            plot_bgcolor='var(--bg-app)',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                landcolor='#334155' if st.session_state.theme == 'dark' else '#CBD5E1',
                countrycolor='var(--border)',
                bgcolor='var(--bg-app)'
            ),
            coloraxis_colorbar=dict(
                title="Median Salary",
                tickfont=dict(family='Sora', size=10, color='var(--text-secondary)'),
                len=0.6,
                thickness=15,
                x=0.95,
                y=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close map-container
        
        # Country-Level Benchmarks
        st.markdown('<div class="section-heading">Country-Level Benchmarks</div>', unsafe_allow_html=True)
        
        display_df = geo_stats.sort_values("median_salary", ascending=False).copy()
        
        # Build custom HTML table
        table_html = '<div class="table-container"><table class="custom-table"><thead><tr>'
        table_html += '<th>Rank</th><th>Country</th><th>Median Salary</th><th>Avg Salary</th><th>Records</th>'
        table_html += '</tr></thead><tbody>'
        
        max_median = display_df['median_salary'].max()
        
        for idx, row in display_df.iterrows():
            # Rank badge
            if idx == display_df.index[0]:
                rank_class = "rank-1"
                rank_display = "🥇"
            elif idx == display_df.index[1]:
                rank_class = "rank-2"
                rank_display = "🥈"
            elif idx == display_df.index[2]:
                rank_class = "rank-3"
                rank_display = "🥉"
            else:
                rank_class = "rank-plain"
                rank_display = str(idx - display_df.index[0] + 1)
            
            # Country code badge
            country_code = row['company_location'].upper()
            
            # Median salary with bar
            median_val = row['median_salary']
            bar_width = (median_val / max_median * 80) if max_median > 0 else 0
            
            # Records pill
            records = int(row['count'])
            
            table_html += f'<tr>'
            table_html += f'<td><span class="rank-badge {rank_class}">{rank_display}</span></td>'
            table_html += f'<td><span class="country-badge">{country_code}</span></td>'
            table_html += f'''<td>
                <div style="color: var(--text-primary); font-weight: 700; font-size: 14px;">${median_val:,.0f}</div>
                <div class="salary-bar" style="width: {bar_width}px; margin-top: 4px;"></div>
            </td>'''
            table_html += f'<td style="color: var(--text-secondary); font-size: 13px;">${row["avg_salary"]:,.0f}</td>'
            table_html += f'<td><span class="records-pill">{records}</span></td>'
            table_html += '</tr>'
        
        table_html += '</tbody></table></div>'
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Pagination
        total_countries = len(display_df)
        st.markdown(f'''
        <div class="pagination">
            <span class="pagination-text">Showing 1–{min(10, total_countries)} of {total_countries} countries</span>
            <div class="pagination-buttons">
                <button class="page-btn disabled">← Prev</button>
                <button class="page-btn">Next →</button>
            </div>
        </div>
        ''', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Failed to load geospatial data: {e}")
