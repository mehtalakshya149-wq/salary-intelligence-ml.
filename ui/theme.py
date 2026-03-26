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
        use_container_width=True
    )

    # CSS overrides for accessible contrasts mapping to Streamlit's internal variables
    if st.session_state.theme == "dark":
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        [data-testid="stSidebar"] {
            background-color: #262730 !important;
        }
        [data-testid="stHeader"] {
            background-color: #0e1117 !important;
        }
        /* Make inputs readable against dark background */
        input, select, textarea {
            color: #fafafa !important;
            background-color: #1a1c24 !important;
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
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #31333F !important;
        }
        .stMetricValue, .stMetricLabel {
            color: #31333F !important;
        }
        </style>
        """

    # Inject the payload globally into the React DOM
    st.markdown(css, unsafe_allow_html=True)
