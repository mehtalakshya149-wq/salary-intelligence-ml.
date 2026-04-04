import streamlit as st
import uuid
from api.database import SessionLocal, engine, Base
from api.models import User, ModelLog
from api.security import get_password_hash, verify_password, create_access_token

# Ensure tables exist for standalone testing
Base.metadata.create_all(bind=engine)

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM AUTH PORTAL - ENHANCED CSS OVERLAY APPROACH
# ══════════════════════════════════════════════════════════════════════════════

# Apply comprehensive CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');

/* ── Hide Sidebar & Headers ── */
[data-testid="stSidebar"] {display: none !important;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ── Deep Space Background ── */
.stApp {
    background: radial-gradient(ellipse at top-left, var(--bg-app) 0%, var(--bg-app) 60%, var(--bg-app) 100%) !important;
    font-family: 'Sora', sans-serif !important;
}

/* ── Center Content ── */
.main .block-container {
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 500px !important;
}

/* ── Override All Typography ── */
* {
    font-family: 'Sora', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

p, span, label, div {
    color: var(--text-secondary) !important;
}

/* ── Title Styling ── */
.stMarkdown h1 {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    text-align: center !important;
    margin-bottom: 8px !important;
}

.stMarkdown p {
    font-size: 13px !important;
    color: var(--text-secondary) !important;
    text-align: center !important;
    line-height: 1.6 !important;
}

/* ── Tabs (Login/Register Switcher) ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface-2) !important;
    border-radius: 999px !important;
    padding: 4px !important;
    gap: 4px !important;
    width: 100% !important;
    justify-content: center !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: 8px 24px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
}

.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── Form Containers ── */
[data-testid="stForm"] {
    background: var(--bg-surface) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 32px !important;
    margin-top: 24px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

/* ── Input Fields ── */
.stTextInput > div > div > input,
.stTextInput input[type="text"],
.stTextInput input[type="password"],
.stTextInput input[type="email"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
    transition: all 0.2s ease !important;
    margin-top: 4px !important;
    line-height: normal !important;
}

.stTextInput > div > div > input:focus,
.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder,
.stTextInput input::placeholder {
    color: #475569 !important;
}

/* Hide labels */
label[data-testid="stWidgetLabel"] {
    display: none !important;
}

/* ── Submit Buttons ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Sora', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 8px !important;
    line-height: normal !important;
}

.stButton > button:hover {
    filter: brightness(110%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Alert Messages ── */
.stAlert {
    border-radius: 10px !important;
    margin-bottom: 16px !important;
    font-size: 13px !important;
    font-family: 'Sora', sans-serif !important;
}

div[data-testid="stAlert"] {
    border: none !important;
}

/* ── Theme Toggle (Top Right) ── */
.theme-toggle-wrapper {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
}

/* ── Spacer for vertical centering ── */
.vertical-spacer {
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

# Theme toggle button
st.markdown("""
<div class="theme-toggle-wrapper">
    <button style="
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: var(--surface-2);
        border: 1px solid var(--border);
        color: var(--text-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 18px;
    " onclick="alert('Theme toggle coming soon!')">☀️</button>
</div>
""", unsafe_allow_html=True)

# ── Vertical spacing for centering ──
st.markdown('<div class="vertical-spacer"></div>', unsafe_allow_html=True)

# ── Title Section ──
st.markdown("""
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
     style="display:block;margin:0 auto 12px auto;color:#60a5fa;">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
</svg>
""", unsafe_allow_html=True)

st.markdown("### Authentication Portal")
st.markdown("Please authenticate securely through the unified database bridge.")

# ── Tabs ──
tab1, tab2 = st.tabs(["Login", "Register"])

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN FORM
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.username == username).first()
                    if user and verify_password(password, user.hashed_password):
                        st.session_state.logged_in = True
                        st.session_state.user_role = user.role
                        st.session_state.username = user.username
                        st.session_state.user_id = user.id
                        st.session_state.token = create_access_token(data={"sub": user.username, "role": user.role})
                        st.session_state.last_active = __import__('time').time()
                        
                        # Log Frontend Login
                        login_log = ModelLog(user_id=user.id, action=f"Frontend Login (Role: {user.role})", endpoint="UI/Login")
                        db.add(login_log)
                        db.commit()
                        
                        st.success(f"Welcome back, {user.username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
                finally:
                    db.close()

# ══════════════════════════════════════════════════════════════════════════════
#  REGISTER FORM
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    with st.form("register_form", clear_on_submit=True):
        new_user = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed")
        new_email = st.text_input("Email", placeholder="Email address", label_visibility="collapsed")
        new_pass = st.text_input("Password", type="password", placeholder="Create a password", label_visibility="collapsed")
        new_role = "user"
        reg_submit = st.form_submit_button("Register", use_container_width=True)
        
        if reg_submit:
            if not new_user or not new_email or not new_pass:
                st.error("Please fill in all fields")
            else:
                db = SessionLocal()
                try:
                    existing = db.query(User).filter((User.username == new_user) | (User.email == new_email)).first()
                    if existing:
                        st.error("Username or email already exists!")
                    else:
                        u = User(
                            id=str(uuid.uuid4()),
                            username=new_user,
                            email=new_email,
                            hashed_password=get_password_hash(new_pass),
                            role=new_role
                        )
                        db.add(u)
                        db.commit()
                        st.success("Account created successfully! Please switch to the Login tab.")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
                finally:
                    db.close()

# ── Footer spacing ──
st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
