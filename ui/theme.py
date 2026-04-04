import streamlit as st

def apply_theme():
    """
    Injects JS to toggle a data-theme attribute on the body tag dynamically.
    Also provides a UI toggle button for the user to switch modes explicitly.
    """
    if "theme" not in st.session_state:
        # Default to dark mode
        st.session_state.theme = "dark"

    def toggle_theme():
        if st.session_state.theme == "dark":
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"

    # Add a meta tag or data attribute to body to indicate theme
    is_dark = st.session_state.get("theme", "dark") == "dark"
    theme_class = "dark-theme" if is_dark else "light-theme"
    
    st.markdown(f"""
    <script>
    document.documentElement.setAttribute('data-theme', '{theme_class}');
    document.body.setAttribute('data-theme', '{theme_class}');
    </script>
    """, unsafe_allow_html=True)
    
    if not is_dark:
        # Heavily assert CSS variables for light mode
        light_mode_css = """
        <style>
        *, :root, body, html, .stApp, [data-testid="stAppViewContainer"], .main {
            --primary: #2563EB !important;
            --accent: #2563EB !important;
            --accent-light: rgba(37, 99, 235, 0.08) !important;
            --bg-app: #ffffff !important;
            --bg-surface: #f8f9fa !important;
            --sidebar-bg: #f1f5f9 !important;
            --surface: #f8f9fa !important;
            --surface-2: #f1f5f9 !important;
            --surface-3: #e2e8f0 !important;
            --text-primary: #0a0a0a !important;
            --text-secondary: #334155 !important;
            --text-muted: #64748B !important;
            --surface-glass: rgba(0, 0, 0, 0.03) !important;
            --border: rgba(0, 0, 0, 0.1) !important;
            --border-strong: rgba(0, 0, 0, 0.15) !important;
        }
        
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: var(--bg-app) !important;
            background-color: var(--bg-app) !important;
            color: var(--text-primary) !important;
        }

        /* Specific Overrides for Streamlit Elements that ignore variables */
        header[data-testid="stHeader"], [data-testid="stHeader"], header {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
        }
        
        .stMetricValue, .stMetricLabel, .stat-value, .stat-label, h1, h2, h3, h4, p, span {
            color: var(--text-primary) !important;
        }
        
        .welcome-subtitle, .stat-label {
            color: var(--text-secondary) !important;
        }
        
        .stat-card, .table-container, .page-header {
            background: var(--bg-surface) !important;
            border-color: var(--border) !important;
        }
        
        /* Inputs */
        input, select, textarea, div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #0a0a0a !important;
            border: 1px solid rgba(0, 0, 0, 0.2) !important;
            line-height: normal !important;
        }
        
        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            color: #2563eb !important;
            background: rgba(37, 99, 235, 0.1) !important;
            font-weight: 600 !important;
        }
        </style>
        """
        st.markdown(light_mode_css, unsafe_allow_html=True)
        
    else:
        # Heavily assert CSS variables for dark mode
        dark_mode_css = """
        <style>
        *, :root, body, html, .stApp, [data-testid="stAppViewContainer"], .main {
            --primary: #0A1128 !important;
            --accent: #00D2FF !important;
            --bg-app: radial-gradient(circle at 50% 0%, #0D2149 0%, #0A1128 70%) !important;
            --bg-surface: rgba(255, 255, 255, 0.04) !important;
            --sidebar-bg: #060d1f !important;
            --surface: rgba(10,17,40,0.92) !important;
            --surface-2: #0F172A !important;
            --surface-3: rgba(255, 255, 255, 0.05) !important;
            --text-primary: #F8FAFC !important;
            --text-secondary: #94A3B8 !important;
            --text-muted: #64748B !important;
            --surface-glass: rgba(255, 255, 255, 0.05) !important;
            --border: rgba(0, 210, 255, 0.12) !important;
            --border-strong: rgba(0, 210, 255, 0.25) !important;
        }
        
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: var(--bg-app) !important;
            background-color: #0A1128 !important;
            color: var(--text-primary) !important;
        }

        /* Specific Overrides for Streamlit Elements that ignore variables */
        header[data-testid="stHeader"], [data-testid="stHeader"], header {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
        }
        
        .stMetricValue, .stMetricLabel, .stat-value, .stat-label, h1, h2, h3, h4, p, span {
            color: var(--text-primary) !important;
        }
        
        .welcome-subtitle, .stat-label {
            color: var(--text-secondary) !important;
        }
        
        .stat-card, .table-container, .page-header {
            background: var(--bg-surface) !important;
            border-color: var(--border) !important;
        }
        
        /* Inputs */
        input, select, textarea, div[data-baseweb="select"] > div {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(0, 210, 255, 0.25) !important;
            line-height: normal !important;
        }
        
        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            color: #F8FAFC !important;
            background: rgba(129, 140, 248, 0.15) !important;
            font-weight: 600 !important;
        }
        </style>
        """
        st.markdown(dark_mode_css, unsafe_allow_html=True)
