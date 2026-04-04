import streamlit as st
from ml.src.interview_data import get_suggested_questions

st.set_page_config(page_title="Interview Prep", page_icon="👔", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM INTERVIEW PREP STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at bottom-right, #1a0533 0%, var(--bg-app) 55%, var(--bg-app) 100%) !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 36px;
}

.header-icon {
    width: 32px;
    height: 32px;
    color: #a855f7;
    margin-bottom: 12px;
}

.header-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
}

/* ── Two Column Layout ── */
.interview-container {
    display: flex;
    gap: 40px;
    align-items: flex-start;
}

.left-column {
    width: 38%;
    position: relative;
}

.right-column {
    width: 58%;
}

.column-divider {
    position: absolute;
    right: -20px;
    top: 0;
    bottom: 0;
    width: 1px;
    background: var(--border);
}

/* ── Section Heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #a855f7;
    padding-left: 12px;
    margin-bottom: 24px;
}

/* ── Labels ── */
.field-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    display: block;
}

/* ── Selectbox Styling ── */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid #2d1b4e !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #a855f7 !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    line-height: normal !important;
}

/* ── Difficulty Button Specifics ── */
div.diff-selected-easy button {
    border-color: #10b981 !important;
    background: rgba(16, 185, 129, 0.1) !important;
    color: #10b981 !important;
    font-weight: 700 !important;
}

div.diff-selected-medium button {
    border-color: #f59e0b !important;
    background: rgba(245, 158, 11, 0.1) !important;
    color: #f59e0b !important;
    font-weight: 700 !important;
}

div.diff-selected-hard button {
    border-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.1) !important;
    color: #ef4444 !important;
    font-weight: 700 !important;
}

div.diff-row-container button {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    height: 48px !important;
    width: 100% !important;
}

div.diff-row-container button p::before {
    content: "●";
    margin-right: 8px;
    font-size: 10px;
    vertical-align: middle;
}


/* ── Fetch Button ── */
.stButton > button[kind="primary"] {
    width: 100% !important;
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 24px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 28px !important;
    line-height: normal !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(115%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4) !important;
}

/* ── Results Heading ── */
.results-heading {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    border-left: 3px solid #a855f7;
    padding-left: 12px;
    margin-bottom: 20px;
}

.role-highlight {
    color: #a855f7;
}

.difficulty-badge {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
    margin-left: 8px;
}

/* ── Question Cards ── */
.question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    transition: all 0.2s ease;
}

.question-card:hover {
    border-color: rgba(168, 85, 247, 0.25);
    transform: translateY(-1px);
}

.question-badge {
    background: rgba(168, 85, 247, 0.15);
    color: #a855f7;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 10px;
}

.question-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
}

.answer-toggle {
    color: #a855f7;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: none;
    border: none;
    padding: 0;
}

.answer-toggle:hover {
    color: var(--text-primary);
}

.chevron {
    transition: transform 0.2s ease;
}

.chevron.expanded {
    transform: rotate(180deg);
}

.answer-content {
    background: var(--surface-glass);
    border-left: 3px solid #a855f7;
    border-radius: 0 8px 8px 0;
    padding: 14px 16px;
    margin-top: 10px;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* ── Load More Button ── */
.load-more-btn {
    display: block;
    margin: 24px auto 0;
    background: transparent;
    border: 1px solid #7c3aed;
    color: #a855f7;
    border-radius: 10px;
    padding: 12px 32px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Sora', sans-serif;
    cursor: pointer;
    transition: all 0.2s ease;
}

.load-more-btn:hover {
    background: rgba(168, 85, 247, 0.1);
    border-color: #a855f7;
    color: var(--text-primary);
}

/* ── Pro Tip Section ── */
.pro-tip {
    background: var(--surface-glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 24px;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
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
        <path d="M12 2a7 7 0 0 1 7 7c0 2.38-1.19 4.47-3 5.74V17a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2v-2.26C6.19 13.47 5 11.38 5 9a7 7 0 0 1 7-7z"></path>
        <path d="M9 21h6"></path>
        <path d="M10 17v4"></path>
        <path d="M14 17v4"></path>
    </svg>
    <h1 class="header-title">Interview Preparation System</h1>
    <p class="header-subtitle">Sharpen your knowledge with curated interview questions and expert-verified answers designed for elite data roles.</p>
</div>
''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# Initialize session state
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = get_suggested_questions("Data Scientist", "Medium")
    st.session_state.current_role = "Data Scientist"
    st.session_state.current_diff = "Medium"
    st.session_state.display_limit = 3
    st.session_state.expanded_answers = {}

# Create columns
st.markdown('<div class="interview-container">', unsafe_allow_html=True)

# Left Column - Session Settings
st.markdown('<div class="left-column">', unsafe_allow_html=True)
st.markdown('<div class="column-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Session Settings</div>', unsafe_allow_html=True)

# Target Role
st.markdown('<label class="field-label">Target Role</label>', unsafe_allow_html=True)
role = st.selectbox("", ["Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer"], label_visibility="collapsed", key="role_select")

# Difficulty Level Pills
st.markdown('<label class="field-label" style="margin-top: 20px; margin-bottom: 12px;">Difficulty Level</label>', unsafe_allow_html=True)

diff_options = ["Easy", "Medium", "Hard"]
diff_themes = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}

# Use a container to inject the row-level class
st.markdown('<div class="diff-row-container">', unsafe_allow_html=True)
diff_cols = st.columns(3)

for i, opt in enumerate(diff_options):
    is_selected = st.session_state.current_diff == opt
    theme_class = f"diff-{diff_themes[opt]}"
    selected_class = f"diff-selected-{diff_themes[opt]}" if is_selected else ""
    
    with diff_cols[i]:
        st.markdown(f'<div class="{theme_class} {selected_class}">', unsafe_allow_html=True)
        if st.button(f"{opt}", key=f"diff_btn_{opt}", use_container_width=True):
            st.session_state.current_diff = opt
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

diff = st.session_state.current_diff

# Fetch New Questions button
if st.button("✨ Fetch New Questions", type="primary", use_container_width=True):
    with st.spinner("Extracting elite question pool..."):
        questions = get_suggested_questions(role, diff)
        st.session_state.interview_questions = questions
        st.session_state.current_role = role
        st.session_state.current_diff = diff
        st.session_state.display_limit = 3
        st.session_state.expanded_answers = {}

st.markdown('</div>', unsafe_allow_html=True)  # Close left-column

# Right Column - Results Panel
st.markdown('<div class="right-column">', unsafe_allow_html=True)

qs = st.session_state.interview_questions
limit = st.session_state.display_limit

# Results heading
st.markdown(f'''
<div class="results-heading">
    Results: <span class="role-highlight">{st.session_state.current_role}</span>
    <span class="difficulty-badge">{st.session_state.current_diff}</span>
</div>
''', unsafe_allow_html=True)

# Display questions
for i in range(min(len(qs), limit)):
    item = qs[i]
    is_expanded = st.session_state.expanded_answers.get(i, False)
    
    st.markdown(f'''
    <div class="question-card">
        <div class="question-badge">Q{i+1}</div>
        <div class="question-text">{item['question']}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Answer toggle button
    if st.button(f"{'▼' if is_expanded else '▶'} View Expert Answer", key=f"toggle_{i}"):
        st.session_state.expanded_answers[i] = not is_expanded
        st.rerun()
    
    # Show answer if expanded
    if is_expanded:
        st.markdown(f'''
        <div class="answer-content">
            {item['answer']}
        </div>
        ''', unsafe_allow_html=True)

# Load More Questions button
if limit < len(qs):
    if st.button("+ Load More Questions", key="load_more"):
        st.session_state.display_limit += 3
        st.rerun()

# Pro Tip
st.markdown('''
<div class="pro-tip">
    <strong style="color: #a855f7;">💡 Pro Tip: STAR Method</strong><br>
    <span style="color: var(--text-secondary); font-size: 13px; line-height: 1.6;">When answering behavioral or scenario-based questions (Medium/Hard), use the <strong style="color: var(--text-primary);">Situation, Task, Action, Result</strong> framework to provide structured, data-driven responses.</span>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close right-column
st.markdown('</div>', unsafe_allow_html=True)  # Close interview-container
