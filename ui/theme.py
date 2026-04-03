import streamlit as st

def apply_theme():
    """
    Injects custom CSS to override the Streamlit theme dynamically 
    based on the current session state, ensuring user-level theme persistence.
    """
    if "theme" not in st.session_state:
        # Default to dark mode
        st.session_state.theme = "dark"

    def toggle_theme():
        if st.session_state.theme == "dark":
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"

    # Insert a highly visible global toggle switch in the sidebar
    st.sidebar.button(
        "🌓 Toggle Dark/Light Mode",
        on_click=toggle_theme,
        use_container_width=True,
        type="secondary"
    )

    # CSS overrides for accessible contrasts mapping to Streamlit's internal variables
    if st.session_state.theme == "dark":
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0A1128 !important;
            color: #F8FAFC !important;
        }
        [data-testid="stSidebar"] {
            background-color: #001F54 !important;
        }
        [data-testid="stHeader"] {
            background-color: #0e1117 !important;
        }
        /* Make inputs readable against dark background */
        input, select, textarea {
            color: #F8FAFC !important;
            background-color: #0F172A !important;
            border: 1px solid rgba(0,210,255,0.2) !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #1a1c24 !important;
            color: #fafafa !important;
        }
        .stMetricValue, .stMetricLabel {
            color: #fafafa !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
            color: #31333F !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
        }
        [data-testid="stHeader"] {
            background-color: #ffffff !important;
        }
        /* High contrast light mode inputs */
        input, select, textarea {
            color: #31333F !important;
            background-color: #ffffff !important;
        }
        [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #1B2B4B !important;
            border: 1px solid rgba(27,43,75,0.1) !important;
        }
        .stMetricValue, .stMetricLabel {
            color: #1B2B4B !important;
        }
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] a {
            color: #1B2B4B !important;
        }
        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            color: #00D2FF !important;
            background: rgba(0,210,255,0.08) !important;
            font-weight: 600 !important;
        }
        h1, h2, h3, .page-header-title {
            color: #1B2B4B !important;
        }
        .page-header {
            background: #ffffff !important;
            box-shadow: 0 4px 20px rgba(27,43,75,0.05) !important;
        }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.9) !important;
            border: 1px solid rgba(27,43,75,0.05) !important;
        }
        </style>
        """

    # Inject the payload globally into the React DOM
    st.markdown(css, unsafe_allow_html=True)
