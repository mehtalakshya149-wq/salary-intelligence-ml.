# import streamlit as st
# from api.chat import 
import streamlit as st
import os
from dotenv import load_dotenv
from api.chat import generate_ai_chat_response

load_dotenv()

st.set_page_config(page_title="Career AI Assistant", page_icon="💬", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM AI ADVISORY CHAT STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ── Global Font & Background ── */
* {
    font-family: 'Sora', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top, #0a1f3d 0%, var(--bg-app) 40%, var(--bg-app) 100%) !important;
}

/* ── Hide Streamlit Elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stSubheader {
    display: none !important;
}

/* ── Chat Header ── */
.chat-header {
    background: linear-gradient(135deg, rgba(251,146,60,0.1), rgba(234,88,12,0.06));
    border: 1px solid rgba(251,146,60,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.bot-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f97316, #fb923c);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(249,115,22,0.4);
    flex-shrink: 0;
}

.header-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.header-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 2px;
}

.online-badge {
    display: flex;
    align-items: center;
    gap: 8px;
}

.online-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
    50% { opacity: 0.8; box-shadow: 0 0 0 6px rgba(16,185,129,0); }
}

.online-text {
    font-size: 11px;
    color: #10b981;
    font-weight: 600;
}

/* ── Quick Prompts ── */
.quick-prompts-section {
    margin-bottom: 24px;
}

.quick-prompts-label {
    font-size: 11px;
    color: #475569;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}

.quick-prompts-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.quick-prompt-chip {
    background: rgba(249,115,22,0.08);
    border: 1px solid rgba(249,115,22,0.2);
    border-radius: 999px;
    padding: 8px 18px;
    font-size: 12px;
    color: #fb923c;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
}

.quick-prompt-chip:hover {
    background: rgba(249,115,22,0.15);
    border-color: rgba(249,115,22,0.4);
    transform: translateY(-1px);
}

/* ── Chat Messages Container ── */
.chat-messages {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
}

/* ── AI Message ── */
.ai-message-container {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.ai-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f97316, #fb923c);
    box-shadow: 0 0 12px rgba(249,115,22,0.3);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ai-message-bubble {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 0 16px 16px 16px;
    padding: 14px 18px;
    max-width: 75%;
}

.ai-message-label {
    font-size: 11px;
    color: #fb923c;
    font-weight: 600;
    margin-bottom: 4px;
}

.ai-message-text {
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.7;
}

.ai-timestamp {
    font-size: 10px;
    color: #475569;
    margin-top: 4px;
}

/* ── User Message ── */
.user-message-container {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    flex-direction: row-reverse;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--surface-2);
    border: 2px solid #334155;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 700;
    flex-shrink: 0;
}

.user-message-bubble {
    background: linear-gradient(135deg, #ea580c, #f97316);
    border-radius: 16px 0 16px 16px;
    padding: 14px 18px;
    max-width: 75%;
}

.user-message-text {
    color: var(--text-primary);
    font-size: 14px;
    line-height: 1.7;
}

/* ── Feature Cards ── */
.feature-cards {
    display: flex;
    gap: 16px;
    margin-top: 32px;
    margin-bottom: 24px;
}

.feature-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    flex: 1;
    transition: all 0.2s ease;
}

.feature-card:hover {
    border-color: rgba(249,115,22,0.2);
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 24px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.feature-desc {
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 4px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: var(--surface-2);
    border-radius: 999px;
}

/* ── Hide Default Chat Message Display (but keep input) ── */
.stChatMessage {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# if not st.session_state.get("logged_in", False):
#     st.error("Please login to use the AI Assistant.")
#     st.stop()


if not st.session_state.get("logged_in", False):
    st.error("Please login to use the AI Assistant.")
    st.stop()

# ── Initialize chat history EARLY (before any access) ──
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": f"Hi {st.session_state.get('username', 'there')}! I am your AI Career Advisor. You can ask me about salary bands for specific roles, skill development, or how to negotiate promotions."}
    ]

# ── Page Header ──
st.markdown('''
<div class="chat-header">
    <div class="header-left">
        <div class="bot-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                <path d="M12 2a10 10 0 0 1 0 20 10 10 0 0 1 0-20z"></path>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
                <path d="M12 2v4"></path>
                <path d="M12 18v4"></path>
            </svg>
        </div>
        <div>
            <div class="header-title">AI Career Advisor</div>
            <div class="header-subtitle">Context-aware • Salary data • Career paths • Skill ROI</div>
        </div>
    </div>
    <div class="online-badge">
        <div class="online-dot"></div>
        <span class="online-text">Online</span>
    </div>
</div>
''', unsafe_allow_html=True)

# --- Sidebar Configuration ---
# with st.sidebar:
#     st.markdown("### ⚙️ Chat Settings")
#     api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your free key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    
#     if st.button("🗑️ Clear Chat History"):
#         st.session_state.chat_messages = [
#             {"role": "assistant", "content": f"Hi {st.session_state.username}! I am your AI Career Advisor. You can ask me about salary bands for specific roles, skill development, or how to negotiate promotions."}
#         ]
#         st.rerun()

# # Initialize chat history
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = [
#         {"role": "assistant", "content": f"Hi {st.session_state.username}! I am your AI Career Advisor. You can ask me about salary bands for specific roles, skill development, or how to negotiate promotions."}
#     ]
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    default_key = os.getenv("XAI_API_KEY", "")
    api_key = st.text_input(
        "Grok API Key",
        value=default_key,
        type="password",
        help="Get your key from [xAI Console](https://console.x.ai/)"
    )

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": f"Hi {st.session_state.username}! I am your AI Career Advisor."}
        ]
        st.rerun()

# ── Quick Prompts ──
st.markdown('<div class="quick-prompts-section">', unsafe_allow_html=True)
st.markdown('<div class="quick-prompts-label">Try asking:</div>', unsafe_allow_html=True)
st.markdown('<div class="quick-prompts-row">', unsafe_allow_html=True)

prompt_suggestions = [
    ("💰", "Salary for Data Scientist"),
    ("🚀", "Skills to become ML Engineer"),
    ("📈", "How to negotiate a raise")
]

for icon, text in prompt_suggestions:
    st.markdown(f'''<div class="quick-prompt-chip" onclick="document.getElementById('chat-input').value='{text}'; document.getElementById('chat-input').focus();">{icon} {text}</div>''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Chat Messages ──
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

for message in st.session_state.chat_messages:
    if message["role"] == "assistant":
        st.markdown(f'''
        <div class="ai-message-container">
            <div class="ai-avatar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                </svg>
            </div>
            <div>
                <div class="ai-message-label">AI Career Advisor</div>
                <div class="ai-message-bubble">
                    <div class="ai-message-text">{message["content"]}</div>
                </div>
                <div class="ai-timestamp">Just now</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # User message
        initial = st.session_state.username[0].upper() if st.session_state.username else "U"
        st.markdown(f'''
        <div class="user-message-container">
            <div class="user-avatar">{initial}</div>
            <div class="user-message-bubble">
                <div class="user-message-text">{message["content"]}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Cards (Empty State) ──
if len(st.session_state.chat_messages) <= 1:
    st.markdown('''
    <div class="feature-cards">
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Salary Intelligence</div>
            <div class="feature-desc">Get real-time salary bands for any role</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Career Pathing</div>
            <div class="feature-desc">Map your journey to your next promotion</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Skill ROI Analysis</div>
            <div class="feature-desc">Discover which skills pay most in your field</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ── Chat Input (at bottom) ──
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

if prompt := st.chat_input("E.g: What skills do I need to be an ML Engineer?"):
    # Add user message to chat history
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Get conversational logic from the backend
    with st.spinner("Analyzing career path..."):
        response = generate_ai_chat_response(user_message=prompt, history=st.session_state.chat_messages, api_key=api_key)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
    
    st.rerun()
