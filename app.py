import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Salary Intelligence Platform",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --primary:        #1B2B4B;
    --primary-mid:    #243A63;
    --accent:         #2F80ED;
    --accent-light:   #EBF3FD;
    --accent-glow:    rgba(47,128,237,0.12);
    --success:        #0F6E56;
    --success-bg:     #E1F5EE;
    --warning:        #BA7517;
    --warning-bg:     #FAEEDA;
    --danger:         #A32D2D;
    --danger-bg:      #FCEBEB;
    --surface:        #FFFFFF;
    --surface-2:      #F7F8FA;
    --surface-3:      #EEF0F5;
    --border:         rgba(27,43,75,0.10);
    --border-strong:  rgba(27,43,75,0.20);
    --text-primary:   #1B2B4B;
    --text-secondary: #52637A;
    --text-muted:     #8B9DB5;
    --radius-sm:      6px;
    --radius-md:      10px;
    --radius-lg:      16px;
    --radius-xl:      22px;
    --font-body:      'DM Sans', sans-serif;
    --font-display:   'Playfair Display', serif;
    --font-mono:      'DM Mono', monospace;
    --shadow-sm:      0 1px 3px rgba(27,43,75,0.06), 0 1px 2px rgba(27,43,75,0.04);
    --shadow-md:      0 4px 12px rgba(27,43,75,0.08), 0 2px 4px rgba(27,43,75,0.04);
    --shadow-lg:      0 12px 32px rgba(27,43,75,0.10), 0 4px 8px rgba(27,43,75,0.04);
    --transition:     all 0.22s cubic-bezier(0.4,0,0.2,1);
}

html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ── Restore Material Icons ── */
.material-symbols-rounded,
[class*="material-symbols"],
.stIcon,
[data-testid="stIconMaterial"],
[data-testid="stChatMessageAvatar"],
[data-testid="stChatMessageAvatar"] *,
summary [data-testid="stIconMaterial"],
summary svg,
summary span[class*="css-"],
.streamlit-expanderHeader svg {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}

/* ── App Background ── */
.stApp {
    background: var(--surface-2) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--primary) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(27,43,75,0.14) !important;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.88) !important;
    font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] .material-symbols-rounded,
[data-testid="stSidebar"] [class*="material-symbols"],
[data-testid="stSidebar"] .stIcon {
    font-family: "Material Symbols Rounded", "Material Icons" !important;
}
[data-testid="stSidebarNav"] a {
    border-radius: var(--radius-md) !important;
    margin: 2px 8px !important;
    padding: 9px 14px !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.72) !important;
    transition: var(--transition) !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.10) !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(47,128,237,0.22) !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    border-left: 3px solid #2F80ED !important;
}

/* ── Main Content ── */
.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1240px !important;
}

/* ── Typography ── */
h1 {
    font-family: var(--font-display) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--primary) !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}
h2 {
    font-family: var(--font-display) !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    color: var(--primary) !important;
    letter-spacing: -0.01em !important;
}
h3 {
    font-family: var(--font-body) !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}
p, li, span {
    font-family: var(--font-body) !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
    color: var(--text-secondary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 2px 8px rgba(47,128,237,0.28) !important;
    transition: var(--transition) !important;
}
.stButton > button:hover {
    background: #1A6DD4 !important;
    box-shadow: 0 4px 14px rgba(47,128,237,0.38) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Form Inputs ── */
.stTextInput > div > input,
.stNumberInput > div > input,
.stTextArea > div > textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTextInput > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
.stSelectbox > div > div,
.stMultiselect > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stTextArea label, .stSlider label, .stMultiselect label,
.stRadio label, .stCheckbox label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.01em !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: var(--border-strong) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11.5px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    color: var(--primary) !important;
    font-family: var(--font-display) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface-3) !important;
    border-radius: var(--radius-lg) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-md) !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    padding: 8px 18px !important;
    transition: var(--transition) !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--primary) !important;
    font-weight: 500 !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
    padding: 0.75rem 1rem !important;
    transition: var(--transition) !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--accent) !important;
    background: var(--accent-light) !important;
}
.streamlit-expanderContent {
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    background: var(--surface) !important;
    padding: 1rem !important;
}

/* ── Data Tables ── */
.stDataFrame, .stTable {
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    border: 1px solid var(--border) !important;
}
.stDataFrame table thead tr th {
    background: var(--surface-3) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    padding: 12px 16px !important;
}
.stDataFrame table tbody tr td {
    font-size: 13.5px !important;
    color: var(--text-secondary) !important;
    padding: 10px 16px !important;
    border-bottom: 1px solid var(--border) !important;
}
.stDataFrame table tbody tr:hover td {
    background: var(--accent-light) !important;
}

/* ── Progress Bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #2F80ED 0%, #6BAAFF 100%) !important;
    border-radius: 100px !important;
}
.stProgress > div > div > div {
    border-radius: 100px !important;
    background: var(--surface-3) !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: var(--radius-md) !important;
    border-left-width: 4px !important;
    font-size: 14px !important;
    font-family: var(--font-body) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Code ── */
code, pre {
    font-family: var(--font-mono) !important;
    background: var(--surface-3) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 13px !important;
    color: var(--primary) !important;
}

/* ════════════════════════════════
   CUSTOM COMPONENT CLASSES
   Use these via the helper functions below
   or directly in st.markdown(..., unsafe_allow_html=True)
   ════════════════════════════════ */

.page-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.8rem 2rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2F80ED 0%, #6BAAFF 60%, transparent 100%);
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}
.page-header-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
    font-family: var(--font-body);
}
.page-header-title {
    font-family: var(--font-display);
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 8px;
}
.page-header-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 640px;
    margin: 0;
    font-family: var(--font-body);
}

.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}
.stat-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-strong);
    transform: translateY(-1px);
}
.stat-label {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 8px;
    font-family: var(--font-body);
}
.stat-value {
    font-family: var(--font-display);
    font-size: 1.9rem; font-weight: 700;
    color: var(--primary); line-height: 1; margin-bottom: 6px;
}
.stat-delta-pos { color: var(--success); font-size: 12px; font-weight: 500; }
.stat-delta-neg { color: var(--danger);  font-size: 12px; font-weight: 500; }

.section-label {
    display: flex; align-items: center;
    gap: 10px; margin: 1.4rem 0 1rem;
}
.section-label-text {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.10em; text-transform: uppercase;
    color: var(--text-muted); white-space: nowrap;
    font-family: var(--font-body);
}
.section-label-line { flex: 1; height: 1px; background: var(--border); }

.result-card {
    background: var(--accent-light);
    border: 1px solid rgba(47,128,237,0.18);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.4rem;
}
.result-card-label {
    font-size: 11.5px; font-weight: 600;
    color: var(--accent); letter-spacing: 0.06em;
    text-transform: uppercase; font-family: var(--font-body); margin-bottom: 4px;
}
.result-card-value {
    font-family: var(--font-display);
    font-size: 2.1rem; font-weight: 700; color: var(--primary);
}

.session-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(47,128,237,0.18); color: #7BB8FF;
    border-radius: 100px; font-size: 11.5px; font-weight: 500;
    padding: 4px 10px; margin: 0.5rem 1rem; letter-spacing: 0.01em;
    font-family: var(--font-body);
}
.session-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #2F80ED; animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

.sidebar-brand {
    padding: 1.2rem 1rem 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 0.5rem;
}
.sidebar-brand-title {
    font-family: var(--font-display);
    font-size: 1.15rem; font-weight: 700;
    color: #FFFFFF; letter-spacing: -0.01em; line-height: 1.3;
}
.sidebar-brand-sub {
    font-family: var(--font-body);
    font-size: 11px; font-weight: 400;
    color: rgba(255,255,255,0.45);
    letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px;
}

.timeout-banner {
    background: var(--warning-bg);
    border: 1px solid rgba(186,117,23,0.25);
    border-left: 4px solid var(--warning);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    font-size: 13.5px; color: #7A4A06;
    margin-bottom: 1rem; font-family: var(--font-body);
}

.app-footer {
    margin-top: 3rem; padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
}
.app-footer-left { font-size: 12px; color: var(--text-muted); font-family: var(--font-body); }
.app-footer-badge {
    font-size: 11px; font-weight: 500;
    background: var(--surface-3); color: var(--text-muted);
    padding: 4px 10px; border-radius: 100px;
    border: 1px solid var(--border); font-family: var(--font-body);
}

.empty-state {
    text-align: center; padding: 3rem 1rem;
    background: var(--surface);
    border: 1px dashed var(--border-strong);
    border-radius: var(--radius-xl); margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  REUSABLE UI HELPER FUNCTIONS
#  Import these in any page:  from app import page_header, section_label, ...
#  Or copy individual functions directly into your page files.
# ══════════════════════════════════════════════════════════════════════════════

def page_header(eyebrow: str, title: str, description: str = ""):
    """Top-of-page hero strip — eyebrow label, display title, optional description."""
    desc_html = f'<p class="page-header-desc">{description}</p>' if description else ""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-eyebrow">{eyebrow}</div>
        <div class="page-header-title">{title}</div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


def section_label(text: str):
    """Uppercase section divider with a horizontal rule."""
    st.markdown(f"""
    <div class="section-label">
        <span class="section-label-text">{text}</span>
        <span class="section-label-line"></span>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, delta: str = "", positive: bool = True):
    """Single KPI card. Wrap in st.columns() for a metric row."""
    delta_class = "stat-delta-pos" if positive else "stat-delta-neg"
    delta_html  = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def result_card(label: str, value: str):
    """Blue-accented highlight card — ideal for prediction results."""
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-label">{label}</div>
        <div class="result-card-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def banner(text: str, variant: str = "info"):
    """Inline contextual banner.  variant: 'info' | 'success' | 'warning' | 'danger'"""
    styles = {
        "info":    ("#EBF3FD", "rgba(47,128,237,0.18)",  "#2F80ED", "#1A4F8C"),
        "success": ("#E1F5EE", "rgba(15,110,86,0.18)",   "#0F6E56", "#063D2E"),
        "warning": ("#FAEEDA", "rgba(186,117,23,0.22)",  "#BA7517", "#7A4A06"),
        "danger":  ("#FCEBEB", "rgba(163,45,45,0.20)",   "#A32D2D", "#6B1515"),
    }
    bg, bc, lc, tc = styles.get(variant, styles["info"])
    st.markdown(f"""
    <div style="background:{bg};border:1px solid {bc};border-left:4px solid {lc};
        border-radius:10px;padding:0.85rem 1.1rem;font-size:13.5px;color:{tc};
        line-height:1.55;margin:0.5rem 0;font-family:'DM Sans',sans-serif;">{text}</div>
    """, unsafe_allow_html=True)


def empty_state(icon: str, heading: str, sub: str = ""):
    """Centered empty/zero-state panel for sections with no data yet."""
    sub_html = f'<p style="font-size:13.5px;color:#8B9DB5;margin:0;">{sub}</p>' if sub else ""
    st.markdown(f"""
    <div class="empty-state">
        <div style="font-size:2.2rem;margin-bottom:0.75rem;">{icon}</div>
        <p style="font-size:15px;font-weight:600;color:#1B2B4B;margin:0 0 6px;">{heading}</p>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def footer(version: str = "v1.0"):
    """Minimal page footer with version badge."""
    st.markdown(f"""
    <div class="app-footer">
        <span class="app-footer-left">Salary Intelligence Platform &nbsp;·&nbsp; Data Science Project</span>
        <span class="app-footer-badge">{version}</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE & TIMEOUT
# ══════════════════════════════════════════════════════════════════════════════
SESSION_TIMEOUT_SECONDS = 1800  # 30 minutes

if "logged_in" not in st.session_state:
    st.session_state.logged_in   = False
    st.session_state.user_role   = None
    st.session_state.username    = None
    st.session_state.last_active = time.time()

if st.session_state.logged_in:
    current_time = time.time()
    elapsed      = current_time - st.session_state.last_active

    if elapsed > SESSION_TIMEOUT_SECONDS:
        st.session_state.logged_in   = False
        st.session_state.user_role   = None
        st.session_state.username    = None
        st.markdown("""
        <div class="timeout-banner">
            🔒 <strong>Session expired</strong> — Your secure session ended after
            30 minutes of inactivity. Please sign in again.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.last_active = current_time


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  (your existing module — untouched)
# ══════════════════════════════════════════════════════════════════════════════
from ui.theme import apply_theme
apply_theme()


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR BRANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">💸 Salary Intelligence</div>
            <div class="sidebar-brand-sub">Data Science · Analytics</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.session_state.username or "User"
        role     = (st.session_state.user_role or "").capitalize()
        st.markdown(f"""
        <div style="padding:0.6rem 1rem 0.3rem;">
            <div style="font-size:11px;color:rgba(255,255,255,0.40);letter-spacing:0.06em;
                        text-transform:uppercase;margin-bottom:4px;font-family:'DM Sans',sans-serif;">
                Signed in as
            </div>
            <div style="font-size:14px;font-weight:500;color:#FFFFFF;font-family:'DM Sans',sans-serif;">
                {username}
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.45);font-family:'DM Sans',sans-serif;">
                {role}
            </div>
        </div>
        <div class="session-badge">
            <span class="session-dot"></span> Session active
        </div>
        <div style="padding:0 1rem 0.5rem;">
            <div style="height:1px;background:rgba(255,255,255,0.10);"></div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGES  (exactly as your original — zero changes)
# ══════════════════════════════════════════════════════════════════════════════
login_page   = st.Page("ui/1_login.py",   title="Login / Register",    icon="🔐")
home_page    = st.Page("ui/2_home.py",    title="Home Overview",        icon="🏠")
predict_page = st.Page("ui/3_predict.py", title="Salary Prediction",    icon="🤖")
compare_page = st.Page("ui/4_compare.py", title="Trend Comparison",     icon="📊")
skills_page  = st.Page("ui/5_skills.py",  title="Skill ROI Calculator", icon="💡")
career_page  = st.Page("ui/6_career.py",  title="Career Simulator",     icon="📈")
explain_page = st.Page("ui/7_explain.py", title="AI Explainability",    icon="🧠")
admin_page   = st.Page("ui/8_admin.py",   title="Admin Dashboard",      icon="⚙️")
ethics_page  = st.Page("ui/9_ethics.py",  title="Ethical AI & Limits",  icon="🛡️")
dashboard_page = st.Page("ui/10_dashboard.py", title="Personalized Dashboard", icon="📈")
chatbot_page   = st.Page("ui/11_chatbot.py", title="AI Career Assistant", icon="💬")
simulator_page = st.Page("ui/12_simulator.py", title="What-If Simulator", icon="🎛️")
col_page       = st.Page("ui/13_cost_of_living.py", title="Cost of Living", icon="🌍")
report_page    = st.Page("ui/14_report.py", title="Download Report", icon="📄")
model_compare_page = st.Page("ui/15_model_compare.py", title="Model Evaluation", icon="⚖️")
notifications_page = st.Page("ui/16_notifications.py", title="Notifications", icon="🔔")
skill_gap_page     = st.Page("ui/17_skill_gap.py",     title="Skill Gap Analysis", icon="🎯")
heatmap_page       = st.Page("ui/18_heatmap.py",       title="Global Salary Heatmap", icon="🌍")
roadmap_page       = st.Page("ui/19_roadmap.py",       title="Learning Roadmap", icon="🛣️")
interview_page     = st.Page("ui/20_interview_prep.py", title="Interview Preparation", icon="👔")
resume_page        = st.Page("ui/21_resume_analyzer.py", title="Resume Analyzer", icon="📄")

if not st.session_state.logged_in:
    pg = st.navigation([login_page])
else:
    pages = [
        home_page, dashboard_page, predict_page, compare_page, 
        skills_page, skill_gap_page, roadmap_page, interview_page, resume_page,
        career_page, explain_page, ethics_page, heatmap_page,
        chatbot_page, simulator_page, col_page, report_page, 
        model_compare_page, notifications_page
    ]
    if st.session_state.user_role == "admin":
        pages.append(admin_page)
    pg = st.navigation(pages)

pg.run()