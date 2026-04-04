import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta
from app import page_header
from api.database import SessionLocal
from api.models import Notification, SalaryPrediction, User

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")

# Add custom CSS for notifications styling
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&display=swap');

.main {
    padding: 0 24px !important;
}

* {
    font-family: 'Sora', sans-serif !important;
}

/* ── Animations ── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(168,85,247,0.1), rgba(139,92,246,0.06));
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 28px;
    position: relative;
}

.hero-content {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.hero-icon {
    width: 28px;
    height: 28px;
    flex-shrink: 0;
}

.hero-text {
    flex: 1;
}

.hero-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 560px;
}

.unread-badge {
    position: absolute;
    top: 24px;
    right: 28px;
    background: rgba(239,68,68,0.15);
    color: #ef4444;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #ef4444;
    animation: pulse 1.5s ease infinite;
}

/* ── AI Opportunity Scan Button ── */
.scan-button {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 11px 24px;
    font-size: 13px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
}

.scan-button:hover {
    brightness: 115%;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(168,85,247,0.4);
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-label-text {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    border-left: 3px solid #c084fc;
    padding-left: 12px;
}

/* ── Unread Messages Chip ── */
.unread-chip {
    background: rgba(239,68,68,0.1);
    color: #ef4444;
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 20px;
}

/* ── Alert Cards ── */
.alert-card-red {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #ef4444;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}

.alert-card-amber {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #f59e0b;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}

.alert-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.alert-type-badge {
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.alert-type-badge-red {
    background: rgba(239,68,68,0.12);
    color: #ef4444;
}

.alert-type-badge-amber {
    background: rgba(245,158,11,0.12);
    color: #f59e0b;
}

.alert-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin-left: 8px;
}

.alert-timestamp {
    margin-left: auto;
    font-size: 11px;
    color: #475569;
}

.alert-body {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-top: 12px;
}

.highlight-purple {
    color: #c084fc;
    font-weight: 600;
}

.highlight-amber {
    color: #f59e0b;
    font-weight: 700;
}

/* ── Action Buttons ── */
.action-buttons {
    display: flex;
    gap: 10px;
    margin-top: 16px;
}

.btn-mark-read {
    background: rgba(16,185,129,0.12);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
}

.btn-mark-read:hover {
    background: rgba(16,185,129,0.2);
}

.btn-delete {
    background: rgba(239,68,68,0.08);
    color: #ef4444;
    border: 1px solid rgba(239,68,68,0.15);
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
}

.btn-delete:hover {
    background: rgba(239,68,68,0.15);
}

/* ── Empty State ── */
.empty-state {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(168,85,247,0.15);
    border-radius: 14px;
    padding: 40px;
    text-align: center;
}

.empty-state-icon {
    color: #c084fc;
    opacity: 0.3;
    font-size: 40px;
}

.empty-state-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 12px;
}

.empty-state-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 6px;
}

/* ── Insight Categories ── */
.insight-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.insight-tab {
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.insight-tab-active {
    background: rgba(168,85,247,0.15);
    color: #c084fc;
    border: 1px solid rgba(168,85,247,0.3);
}

.insight-tab-inactive {
    background: var(--bg-surface);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text-secondary);
}

.insight-tab-inactive:hover {
    background: rgba(255,255,255,0.06);
    color: var(--text-secondary);
}

/* ── Style Streamlit Buttons ── */
[data-testid="stButton"] button {
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    background: rgba(16,185,129,0.12) !important;
    color: #10b981 !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
}

[data-testid="stButton"] button:hover {
    background: rgba(16,185,129,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

page_header("Alerts & AI Insights", "Notification Center", "Personalized skill expansion opportunities and salary growth warnings natively tracking your career profile.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to access notifications.")
    st.stop()

# Resolve user_id from DB if not already cached in session
if not st.session_state.get("user_id"):
    try:
        _db = SessionLocal()
        _user = _db.query(User).filter(User.username == st.session_state.username).first()
        _db.close()
        if _user:
            st.session_state.user_id = _user.id
        else:
            st.error("Could not resolve your user account. Please log out and log back in.")
            st.stop()
    except Exception as _e:
        st.error(f"DB lookup error: {_e}")
        st.stop()

user_id = st.session_state.user_id

# Load notifications
db = SessionLocal()
notifications = (
    db.query(Notification)
    .filter(Notification.user_id == user_id)
    .order_by(Notification.created_at.desc())
    .all()
)

for n in notifications:
    n.is_read = bool(n.is_read)

unread_count = sum(1 for a in notifications if not a.is_read)

# ── HERO BANNER ──
st.markdown(f'''
<div class="hero-banner">
    <div class="hero-content">
        <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <div class="hero-text">
            <div class="hero-title">Alerts & AI Insights</div>
            <div class="hero-subtitle">Real-time notifications about market shifts, trending roles, and emerging opportunities in the AI & tech landscape tailored to your career profile.</div>
        </div>
    </div>
    {f'<div class="unread-badge"><div class="pulse-dot"></div>{unread_count} Unread</div>' if unread_count > 0 else ''}
</div>
''', unsafe_allow_html=True)

# ── AI OPPORTUNITY SCAN BUTTON ──
if st.button("✨ AI Opportunity Scan", key="scan_opportunity", use_container_width=False):
    try:
        # Dynamic Market Cache from ml/market_data.json
        market_data_path = "ml/market_data.json"
        skill_alerts = []
        salary_alerts = []
        last_scan_date = "Unknown"
        
        if os.path.exists(market_data_path):
            with open(market_data_path, "r") as f:
                data = json.load(f)
                skill_alerts = [(a["title"], a["message"]) for a in data.get("skill_alerts", [])]
                salary_alerts = [(a["title"], a["message"]) for a in data.get("salary_alerts", [])]
                last_scan_date = data.get("metadata", {}).get("last_scan", "Unknown")

        # Fetch existing notification titles to prevent duplicates
        existing_notifs = db.query(Notification.title).filter(Notification.user_id == user_id).all()
        existing_titles = {n[0] for n in existing_notifs}

        # Filter for new alerts only
        available_skill_alerts = [a for a in skill_alerts if a[0] not in existing_titles]
        available_salary_alerts = [a for a in salary_alerts if a[0] not in existing_titles]

        latest_pred = (
            db.query(SalaryPrediction)
            .filter(SalaryPrediction.user_id == user_id)
            .order_by(SalaryPrediction.created_at.desc())
            .first()
        )

        # Generate new notifications
        new_count = 0
        if available_salary_alerts:
            sal_title, sal_msg = random.choice(available_salary_alerts)
            if latest_pred:
                sal_msg = f"For trailing '{latest_pred.job_title}' roles: " + sal_msg
            db.add(Notification(user_id=user_id, title=sal_title, message=sal_msg))
            new_count += 1

        if available_skill_alerts and (random.choice([True, False]) or not available_salary_alerts):
            sk_title, sk_msg = random.choice(available_skill_alerts)
            db.add(Notification(user_id=user_id, title=sk_title, message=sk_msg))
            new_count += 1

        if new_count == 0:
            st.info(f"Market remains stable since scan on {last_scan_date}. No new unique AI insights found for your profile today.")
        else:
            db.commit()
            st.success(f"Market scan complete! {new_count} new AI insight(s) added based on 2026 data.")
        
        db.close()
        if new_count > 0:
            st.rerun()
    except Exception as e:
        st.error(f"Error generating notifications: {e}")
        db.close()

# ── RECENT ALERTS SECTION ──
st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
st.markdown(f'''
<div class="section-header">
    <div class="section-label-text">Recent Alerts</div>
</div>
''', unsafe_allow_html=True)

if unread_count > 0:
    st.markdown(f'''
<div class="unread-chip">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
        <polyline points="22,6 12,13 2,6"></polyline>
    </svg>
    {unread_count} Unread Messages
</div>
''', unsafe_allow_html=True)

# ── DISPLAY NOTIFICATIONS ──
if not notifications:
    st.markdown(f'''
<div class="empty-state">
    <div class="empty-state-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
    </div>
    <div class="empty-state-title">You're all caught up!</div>
    <div class="empty-state-subtitle">New AI insights will appear here when detected</div>
</div>
''', unsafe_allow_html=True)
else:
    for alert in notifications:
        # Determine card styling based on title keywords
        is_market_shift = "Market Shift" in alert.title or "Infrastructure" in alert.title
        is_trending = "Trending" in alert.title or "CAIO" in alert.title
        
        if is_market_shift:
            card_class = "alert-card-red"
            badge_class = "alert-type-badge-red"
            badge_text = "⚡ MARKET SHIFT"
            highlight_terms = [
                ("Applied AI", "highlight-purple"),
                ("MLOps", "highlight-purple"),
                ("60%", "highlight-amber"),
            ]
        elif is_trending:
            card_class = "alert-card-amber"
            badge_class = "alert-type-badge-amber"
            badge_text = "📈 TRENDING"
            highlight_terms = [
                ("Chief AI Officer", "highlight-purple"),
                ("Mid-to-Large enterprises", "highlight-amber"),
            ]
        else:
            # Default styling
            card_class = "alert-card-red"
            badge_class = "alert-type-badge-red"
            badge_text = "🔔 ALERT"
            highlight_terms = []
        
        # Calculate time ago
        time_delta = datetime.now() - alert.created_at
        if time_delta.days > 0:
            time_ago = f"{time_delta.days} day{'s' if time_delta.days > 1 else ''} ago"
        elif time_delta.seconds > 3600:
            time_ago = f"{time_delta.seconds // 3600} hour{'s' if time_delta.seconds // 3600 > 1 else ''} ago"
        else:
            time_ago = f"{time_delta.seconds // 60} minute{'s' if time_delta.seconds // 60 > 1 else ''} ago"
        
        # Format message with highlights
        formatted_message = alert.message.replace("—", "—").replace("'", "'").replace("'", "'")
        for term, css_class in highlight_terms:
            formatted_message = formatted_message.replace(term, f'<span class="{css_class}">{term}</span>')
        
        if not alert.is_read:
            st.markdown(f'''
<div class="{card_class}">
    <div class="alert-card-header">
        <span class="alert-type-badge {badge_class}">{badge_text}</span>
        <span class="alert-title">{alert.title}</span>
        <span class="alert-timestamp">{time_ago}</span>
    </div>
    <div class="alert-body">{formatted_message}</div>
</div>
''', unsafe_allow_html=True)
            
            # Action buttons using Streamlit columns
            btn_col1, btn_col2, _ = st.columns([1, 1, 3])
            with btn_col1:
                if st.button("✓ Mark Read", key=f"read_{alert.id}", use_container_width=True):
                    _db_temp = SessionLocal()
                    _a = _db_temp.query(Notification).get(alert.id)
                    _a.is_read = 1
                    _db_temp.commit()
                    _db_temp.close()
                    st.rerun()
            
            with btn_col2:
                if st.button("🗑 Delete", key=f"del_{alert.id}", use_container_width=True):
                    _db_temp = SessionLocal()
                    _a = _db_temp.query(Notification).get(alert.id)
                    _db_temp.delete(_a)
                    _db_temp.commit()
                    _db_temp.close()
                    st.rerun()
        else:
            # Read alert styling
            st.markdown(f'''
<div class="{card_class}" style="opacity: 0.5;">
    <div class="alert-card-header">
        <span class="alert-type-badge {badge_class}">{badge_text}</span>
        <span class="alert-title" style="color: var(--text-secondary);">{alert.title}</span>
        <span class="alert-timestamp">{time_ago}</span>
    </div>
    <div class="alert-body" style="color: #475569;">{formatted_message}</div>
</div>
''', unsafe_allow_html=True)
            
            # Delete button for read alerts
            _, del_btn, __ = st.columns([1, 1, 3])
            with del_btn:
                if st.button("🗑 Delete", key=f"del_{alert.id}", use_container_width=True):
                    _db_temp = SessionLocal()
                    _a = _db_temp.query(Notification).get(alert.id)
                    _db_temp.delete(_a)
                    _db_temp.commit()
                    _db_temp.close()
                    st.rerun()

db.close()

# ── INSIGHT CATEGORIES SECTION ──
st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label-text" style="margin: 32px 0 16px;">AI Intelligence Feed</div>', unsafe_allow_html=True)

st.markdown(f'''
<div class="insight-tabs">
    <div class="insight-tab insight-tab-active">🔴 Market Shifts</div>
    <div class="insight-tab insight-tab-inactive">📈 Trending Roles</div>
    <div class="insight-tab insight-tab-inactive">💡 Skill Opportunities</div>
</div>
''', unsafe_allow_html=True)
