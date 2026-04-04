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
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

:root {
    /* ── BASE TOKENS (Dark Mode Default) ── */
    --primary:        #0A1128;
    --primary-glass:  rgba(10,17,40,0.85);
    --primary-mid:    #001F54;
    --accent:         #00D2FF;
    --accent-glow:    rgba(0,210,255,0.15);
    --accent-light:   #E0F7FA;
    --surface:        rgba(10,17,40,0.92);
    --surface-glass:  rgba(255,255,255,0.05);
    --surface-2:      #0F172A;
    --surface-3:      rgba(255, 255, 255, 0.05);
    --border:         rgba(0,210,255,0.12);
    --border-strong:  rgba(0,210,255,0.25);
    
    /* ── THEME-AWARE VARIABLES ── */
    --bg-app:         radial-gradient(circle at 50% 0%, #0D2149 0%, var(--primary) 70%);
    --bg-surface:     rgba(255, 255, 255, 0.04);
    --sidebar-bg:     #060d1f;
    --text-primary:   #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted:     #64748B;
    
    /* ── COMMON UTILITIES ── */
    --radius-md:      12px;
    --radius-lg:      20px;
    --radius-xl:      28px;
    --font-body:      'DM Sans', sans-serif;
    --font-display:   'Playfair Display', serif;
    --shadow-soft:    0 4px 20px -2px rgba(27,43,75,0.08), 0 2px 10px -1px rgba(27,43,75,0.04);
    --shadow-glass:   0 8px 32px 0 rgba(31, 38, 135, 0.07);
    --transition:     all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="light-theme"], body[data-theme="light-theme"] .stApp, body[data-theme="light-theme"] {
    --primary:        #2563EB;
    --accent:         #2563EB;
    --accent-light:   rgba(37, 99, 235, 0.08);
    --bg-app:         #ffffff;
    --bg-surface:     #f8f9fa;
    --sidebar-bg:     #f1f5f9;
    --surface:        #f8f9fa;
    --surface-2:      #f1f5f9;
    --surface-3:      #e2e8f0;
    --text-primary:   #0a0a0a;
    --text-secondary: #334155;
    --text-muted:     #64748B;
    --surface-glass:  rgba(0, 0, 0, 0.03);
    --border:         rgba(0, 0, 0, 0.1);
    --border-strong:  rgba(0, 0, 0, 0.15);
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
    background: var(--bg-app) !important;
}

/* ── Hide Streamlit Header ── */
header[data-testid="stHeader"], [data-testid="stHeader"], header {
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
}

/* Adjust top padding since header is gone */
.main .block-container {
    padding-top: 2rem !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    width: 260px !important;
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    padding: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* Scrollbar */
[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 3px !important;
}
[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: #1e293b !important;
    border-radius: 999px !important;
}

/* Collapse Buttons */
[data-testid="stSidebarCollapseButton"],
button[aria-label="Expand sidebar"],
button[aria-label="Collapse sidebar"] {
    width: 28px !important;
    height: 28px !important;
    border-radius: 6px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #64748b !important;
    font-size: 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarCollapseButton"]:hover,
button[aria-label="Expand sidebar"]:hover,
button[aria-label="Collapse sidebar"]:hover {
    background: rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
}

/* App Branding */
.sidebar-brand {
    padding: 16px 20px 12px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 16px !important;
    margin-bottom: 8px !important;
}

.sidebar-logo {
    width: 32px !important;
    height: 32px !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border-radius: 8px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.sidebar-logo-text {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    font-family: 'Sora', sans-serif !important;
}

.sidebar-brand-info {
    flex: 1 !important;
}

.sidebar-brand-title {
    font-size: 14px !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    font-family: 'Sora', sans-serif !important;
    margin: 0 !important;
}

.sidebar-brand-sub {
    font-size: 9px !important;
    color: #475569 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    display: block !important;
    margin-top: 1px !important;
    font-family: 'Sora', sans-serif !important;
}

/* Section Labels */
.sidebar-section-label {
    font-size: 9px !important;
    font-weight: 600 !important;
    color: #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    padding: 10px 20px 6px !important;
    display: block !important;
    font-family: 'Sora', sans-serif !important;
}

/* Section Dividers */
.sidebar-divider {
    height: 1px !important;
    background: rgba(255,255,255,0.05) !important;
    margin: 8px 20px !important;
}

/* Navigation Items */
[data-testid="stSidebarNav"] {
    padding: 0 !important;
}

[data-testid="stSidebarNav"] a {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 10px 20px !important;
    margin: 1px 10px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    font-family: 'Sora', sans-serif !important;
}

[data-testid="stSidebarNav"] a span:first-child {
    font-size: 16px !important;
    width: 20px !important;
    flex-shrink: 0 !important;
}

[data-testid="stSidebarNav"] a span:last-child {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    font-family: 'Sora', sans-serif !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.05) !important;
}

[data-testid="stSidebarNav"] a:hover span:last-child {
    color: #94a3b8 !important;
}

/* Active State - Default (Indigo) */
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(129,140,248,0.15) !important;
    border: 1px solid rgba(129,140,248,0.2) !important;
    border-left: 3px solid #818cf8 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebarNav"] a[aria-selected="true"] span:last-child {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* Per-Item Accent Colors */
/* Home Overview - Blue */
[data-testid="stSidebarNav"] a[href*="Home_Overview"][aria-selected="true"] {
    background: rgba(59,130,246,0.12) !important;
    border-left: 3px solid #3b82f6 !important;
}

/* Personalized Dashboard - Blue */
[data-testid="stSidebarNav"] a[href*="Personalized_Dashboard"][aria-selected="true"] {
    background: rgba(59,130,246,0.12) !important;
    border-left: 3px solid #3b82f6 !important;
}

/* Salary Prediction - Purple */
[data-testid="stSidebarNav"] a[href*="Salary_Prediction"][aria-selected="true"] {
    background: rgba(139,92,246,0.12) !important;
    border-left: 3px solid #8b5cf6 !important;
}

/* Trend Comparison - Rose */
[data-testid="stSidebarNav"] a[href*="Trend_Comparison"][aria-selected="true"] {
    background: rgba(225,29,72,0.12) !important;
    border-left: 3px solid #e11d48 !important;
}

/* Skill ROI Calculator - Yellow */
[data-testid="stSidebarNav"] a[href*="Skill_ROI_Calculator"][aria-selected="true"] {
    background: rgba(234,179,8,0.12) !important;
    border-left: 3px solid #eab308 !important;
}

/* Skill Gap Analysis - Green */
[data-testid="stSidebarNav"] a[href*="Skill_Gap_Analysis"][aria-selected="true"] {
    background: rgba(34,197,94,0.12) !important;
    border-left: 3px solid #22c55e !important;
}

/* Learning Roadmap - Cyan */
[data-testid="stSidebarNav"] a[href*="Learning_Roadmap"][aria-selected="true"] {
    background: rgba(6,182,212,0.12) !important;
    border-left: 3px solid #06b6d4 !important;
}

/* Interview Preparation - Purple */
[data-testid="stSidebarNav"] a[href*="Interview_Preparation"][aria-selected="true"] {
    background: rgba(168,85,247,0.12) !important;
    border-left: 3px solid #a855f7 !important;
}

/* Resume Analyzer - Amber */
[data-testid="stSidebarNav"] a[href*="Resume_Analyzer"][aria-selected="true"] {
    background: rgba(245,158,11,0.12) !important;
    border-left: 3px solid #f59e0b !important;
}

/* Career Simulator - Sky */
[data-testid="stSidebarNav"] a[href*="Career_Simulator"][aria-selected="true"] {
    background: rgba(34,211,238,0.12) !important;
    border-left: 3px solid #22d3ee !important;
}

/* AI Explainability - Pink */
[data-testid="stSidebarNav"] a[href*="AI_Explainability"][aria-selected="true"] {
    background: rgba(236,72,153,0.12) !important;
    border-left: 3px solid #ec4899 !important;
}

/* Ethical AI & Limits - Indigo */
[data-testid="stSidebarNav"] a[href*="Ethical_AI"][aria-selected="true"] {
    background: rgba(129,140,248,0.12) !important;
    border-left: 3px solid #818cf8 !important;
}

/* Global Salary Heatmap - Sky Blue */
[data-testid="stSidebarNav"] a[href*="Global_Salary_Heatmap"][aria-selected="true"] {
    background: rgba(14,165,233,0.12) !important;
    border-left: 3px solid #0ea5e9 !important;
}

/* AI Career Assistant - Orange */
[data-testid="stSidebarNav"] a[href*="AI_Career_Assistant"][aria-selected="true"] {
    background: rgba(249,115,22,0.12) !important;
    border-left: 3px solid #f97316 !important;
}

/* What-If Simulator - Emerald */
[data-testid="stSidebarNav"] a[href*="What-If_Simulator"][aria-selected="true"] {
    background: rgba(16,185,129,0.12) !important;
    border-left: 3px solid #10b981 !important;
}

/* Cost of Living - Light Blue */
[data-testid="stSidebarNav"] a[href*="Cost_of_Living"][aria-selected="true"] {
    background: rgba(56,189,248,0.12) !important;
    border-left: 3px solid #38bdf8 !important;
}

/* Download Report - Green */
[data-testid="stSidebarNav"] a[href*="Download_Report"][aria-selected="true"] {
    background: rgba(16,185,129,0.12) !important;
    border-left: 3px solid #10b981 !important;
}

/* Model Evaluation - Violet */
[data-testid="stSidebarNav"] a[href*="Model_Evaluation"][aria-selected="true"] {
    background: rgba(129,140,248,0.12) !important;
    border-left: 3px solid #818cf8 !important;
}

/* Notifications - Light Purple */
[data-testid="stSidebarNav"] a[href*="Notifications"][aria-selected="true"] {
    background: rgba(192,132,252,0.12) !important;
    border-left: 3px solid #c084fc !important;
}

/* User Profile Section */
.sidebar-user-section {
    margin-top: auto !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    padding: 16px 20px !important;
}

.sidebar-user-label {
    font-size: 9px !important;
    color: #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    margin-bottom: 6px !important;
    display: block !important;
    font-family: 'Sora', sans-serif !important;
}

.sidebar-user-row {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}

.sidebar-user-avatar {
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.sidebar-user-avatar-text {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
}

.sidebar-user-info {
    flex: 1 !important;
}

.sidebar-user-name {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-family: 'Sora', sans-serif !important;
    margin: 0 !important;
}

.sidebar-user-role {
    font-size: 11px !important;
    color: #475569 !important;
    display: block !important;
    font-family: 'Sora', sans-serif !important;
}

/* Session Badge */
.session-badge {
    background: rgba(16,185,129,0.12) !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
    border-radius: 999px !important;
    padding: 4px 12px !important;
    font-size: 11px !important;
    color: #10b981 !important;
    font-weight: 600 !important;
    margin-top: 8px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    font-family: 'Sora', sans-serif !important;
}

.session-dot {
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    background: #10b981 !important;
    animation: pulse 2s ease infinite !important;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Logout Button */
.sidebar-logout-btn {
    background: transparent !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    color: #ef4444 !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-top: 10px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-family: 'Sora', sans-serif !important;
}

.sidebar-logout-btn:hover {
    background: rgba(239,68,68,0.1) !important;
}

/* Theme Toggle */
.sidebar-theme-toggle {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-top: 12px !important;
    padding: 4px 0 !important;
}

.theme-icon {
    font-size: 14px !important;
    color: #64748b !important;
    line-height: 1 !important;
}

.theme-toggle-switch {
    width: 36px !important;
    height: 20px !important;
    border-radius: 999px !important;
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    position: relative !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    flex-shrink: 0 !important;
}

.theme-toggle-switch.active {
    background: #3b82f6 !important;
    border-color: #3b82f6 !important;
}

.theme-toggle-thumb {
    width: 16px !important;
    height: 16px !important;
    border-radius: 50% !important;
    background: white !important;
    position: absolute !important;
    top: 50% !important;
    left: 2px !important;
    transform: translateY(-50%) !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

.theme-toggle-switch.active .theme-toggle-thumb {
    left: calc(100% - 18px) !important;
}

.theme-label {
    font-size: 12px !important;
    color: #64748b !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    margin-left: 2px !important;
}

/* Theme Toggle Checkbox Styling */
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) {
    padding: 12px 20px !important;
    margin: 0 !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) label {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    cursor: pointer !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) input[type="checkbox"] {
    appearance: none !important;
    -webkit-appearance: none !important;
    width: 36px !important;
    height: 20px !important;
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 999px !important;
    position: relative !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    flex-shrink: 0 !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) input[type="checkbox"]:checked {
    background: #3b82f6 !important;
    border-color: #3b82f6 !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) input[type="checkbox"]::after {
    content: '' !important;
    position: absolute !important;
    width: 16px !important;
    height: 16px !important;
    background: white !important;
    border-radius: 50% !important;
    top: 50% !important;
    left: 2px !important;
    transform: translateY(-50%) !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) input[type="checkbox"]:checked::after {
    left: 18px !important;
}
div[data-testid="stCheckbox"]:has(input[key="sidebar_theme_toggle"]) span {
    font-size: 12px !important;
    color: #64748b !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
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
p, li, span, div:not([data-testid="stSidebar"]) {
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

/* Hide the redundant "Press Enter to submit form" hint which overlaps icons */
div[data-testid="InputInstructions"],
div[data-testid="stInputInstructions"],
div[data-testid="stFieldDescription"],
div[data-testid="stFormSubmitButton"] + div,
.stTextInput p:last-child {
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    font-size: 0px !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Ensure the password eye icon doesn't overlap text */
.stTextInput input[type="password"] {
    padding-right: 3rem !important;
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
    background: var(--surface-glass) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
    box-shadow: var(--shadow-glass) !important;
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
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
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
    height: 4px;
    background: linear-gradient(90deg, #00D2FF, #0072FF, #00D2FF);
    background-size: 200% auto;
    animation: gradient-flow 6s linear infinite;
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}
@keyframes gradient-flow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
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
    color: var(--text-primary); line-height: 1; margin-bottom: 6px;
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
    font-size: 2.1rem; font-weight: 700; color: var(--text-primary);
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
    color: var(--text-primary); letter-spacing: -0.01em; line-height: 1.3;
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
    st.session_state.token       = None
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
        # App Branding at top
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">
                <span class="sidebar-logo-text">S</span>
            </div>
            <div class="sidebar-brand-info">
                <div class="sidebar-brand-title">Salary Intelligence</div>
                <span class="sidebar-brand-sub">DATA SCIENCE · ANALYTICS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Menu Section Label
        st.markdown("""
        <span class="sidebar-section-label">MAIN MENU</span>
        """, unsafe_allow_html=True)
        
        # Navigation will be rendered here automatically by Streamlit
        
        username = st.session_state.username or "User"
        role     = (st.session_state.user_role or "").capitalize()
        initial = username[0].upper() if username else "U"
        
        # Theme toggle function
        def toggle_theme():
            if st.session_state.theme == "dark":
                st.session_state.theme = "light"
            else:
                st.session_state.theme = "dark"
        
        is_dark = st.session_state.theme == "dark"
        
        # User Profile Section at bottom
        st.markdown(f"""
        <div class="sidebar-user-section">
            <span class="sidebar-user-label">SIGNED IN AS</span>
            <div class="sidebar-user-row">
                <div class="sidebar-user-avatar">
                    <span class="sidebar-user-avatar-text">{initial}</span>
                </div>
                <div class="sidebar-user-info">
                    <div class="sidebar-user-name">{username}</div>
                    <span class="sidebar-user-role">{role}</span>
                </div>
            </div>
            <div class="session-badge">
                <span class="session-dot"></span> Session active
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add theme toggle checkbox
        st.checkbox(
            "Dark Mode",
            value=is_dark,
            on_change=toggle_theme,
            key="sidebar_theme_toggle"
        )


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

# Inject section dividers and labels into navigation
if st.session_state.logged_in:
    # Add light mode fix script
    st.markdown("""
    <script>
    // Check if we're in light mode and fix all text colors
    function applyLightModeFix() {
        const themeAttr = document.body.getAttribute('data-theme');
        const isLight = themeAttr === 'light-theme';
        
        if (isLight) {
            // Create a style element that overrides everything
            const styleId = 'light-mode-text-fix';
            let styleEl = document.getElementById(styleId);
            
            if (!styleEl) {
                styleEl = document.createElement('style');
                styleEl.id = styleId;
                document.head.appendChild(styleEl);
            }
            
            styleEl.innerHTML = `
                /* Main Text Visibility */
                body[data-theme="light-theme"] .main p, 
                body[data-theme="light-theme"] .main span, 
                body[data-theme="light-theme"] .main li,
                body[data-theme="light-theme"] .main div:not([data-testid="stSidebar"]) {
                    color: #1e293b !important;
                }
                
                /* Headers */
                body[data-theme="light-theme"] .main h1,
                body[data-theme="light-theme"] .main h2,
                body[data-theme="light-theme"] .main h3,
                body[data-theme="light-theme"] .main h4 {
                    color: #0f172a !important;
                }
                
                /* Metrics & Stats */
                body[data-theme="light-theme"] [data-testid="stMetricValue"],
                body[data-theme="light-theme"] [data-testid="stMetricLabel"],
                body[data-theme="light-theme"] .stat-value,
                body[data-theme="light-theme"] .stat-label {
                    color: #0f172a !important;
                }
                
                /* DataFrames & Tables */
                body[data-theme="light-theme"] [data-testid="stDataFrame"] *,
                body[data-theme="light-theme"] [data-testid="stTable"] * {
                    color: #334155 !important;
                }
                
                /* Custom Cards and Headers */
                body[data-theme="light-theme"] .page-header-title,
                body[data-theme="light-theme"] .stat-card .stat-value {
                    color: #0f172a !important;
                }

                /* Override persistent white/light text */
                body[data-theme="light-theme"] .main *[style*="color: #ffffff"],
                body[data-theme="light-theme"] .main *[style*="color:#ffffff"],
                body[data-theme="light-theme"] .main *[style*="color: white"],
                body[data-theme="light-theme"] .main *[style*="color: #F8FAFC"],
                body[data-theme="light-theme"] .main *[style*="color:rgba(255, 255, 255, 0.02)"],
                body[data-theme="light-theme"] .main *[style*="background: rgba(255, 255, 255, 0.06)"] {
                    color: #1e293b !important;
                }
                
                /* Kill Redundant Toggle Button (Force Hidden) */
                [data-testid="stSidebar"] button:has(div:contains("Toggle")),
                [data-testid="stSidebar"] button:has(div:contains("Mode")),
                .stButton > button:has(div:contains("Toggle Dark/Light Mode")) {
                    display: none !important;
                    visibility: hidden !important;
                }
            `;
            
            // MutationObserver to catch and kill the redundant toggle button
            const observer = new MutationObserver((mutations) => {
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText && (btn.innerText.includes('Toggle Dark/Light Mode') || btn.innerText.includes('🌓'))) {
                        btn.style.display = 'none';
                        btn.style.visibility = 'hidden';
                        if (btn.parentElement) btn.parentElement.style.display = 'none';
                    }
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }
    
    // Run immediately and multiple times
    setTimeout(applyLightModeFix, 100);
    setTimeout(applyLightModeFix, 500);
    setTimeout(applyLightModeFix, 1500);
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <script>
    setTimeout(function() {
        // Find all sidebar nav links
        const navContainer = document.querySelector('[data-testid="stSidebarNav"]');
        if (!navContainer) return;
        
        const links = navContainer.querySelectorAll('a');
        if (!links.length) return;
        
        // Find indices for section breaks
        let reportIndex = -1;
        let modelIndex = -1;
        
        links.forEach((link, index) => {
            const text = link.textContent || link.innerText;
            if (text.includes('Download Report')) reportIndex = index;
            if (text.includes('Model Evaluation')) modelIndex = index;
        });
        
        // Insert "TOOLS" section before Download Report
        if (reportIndex > 0) {
            const toolsLabel = document.createElement('span');
            toolsLabel.className = 'sidebar-section-label';
            toolsLabel.textContent = 'TOOLS';
            
            const divider = document.createElement('div');
            divider.className = 'sidebar-divider';
            
            // Insert before the report link
            const reportLink = links[reportIndex];
            reportLink.parentNode.insertBefore(divider, reportLink);
            reportLink.parentNode.insertBefore(toolsLabel, divider);
        }
        
        // Insert "SYSTEM" section before Model Evaluation
        if (modelIndex > 0) {
            const systemLabel = document.createElement('span');
            systemLabel.className = 'sidebar-section-label';
            systemLabel.textContent = 'SYSTEM';
            
            const divider = document.createElement('div');
            divider.className = 'sidebar-divider';
            
            // Find the model evaluation link (might have shifted)
            const allLinks = navContainer.querySelectorAll('a');
            let currentModelIndex = -1;
            allLinks.forEach((link, index) => {
                const text = link.textContent || link.innerText;
                if (text.includes('Model Evaluation')) currentModelIndex = index;
            });
            
            if (currentModelIndex > 0) {
                const modelLink = allLinks[currentModelIndex];
                modelLink.parentNode.insertBefore(divider, modelLink);
                modelLink.parentNode.insertBefore(systemLabel, divider);
            }
        }
    }, 500);
    </script>
    """, unsafe_allow_html=True)

pg.run()