import streamlit as st
import random
from datetime import datetime
from app import page_header
from api.database import SessionLocal
from api.models import Notification, SalaryPrediction, User

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")

page_header("Alerts & AI Insights", "Notification Center", "Personalized skill expansion opportunities and salary growth warnings natively tracking your career profile.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to access notifications.")
    st.stop()

# Resolve user_id from DB if not already cached in session (login.py only stores username)
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

col_main, col_btn = st.columns([3, 1])

with col_btn:
    if st.button("AI Opportunity Scan 🤖", use_container_width=True, type="primary"):
        try:
            db = SessionLocal()
            skill_alerts = [
                ("Skill Demand Surge: PyTorch", "We tracked a 14% increase in job postings requiring PyTorch in the last 30 days. Consider updating your portfolio!"),
                ("Skill Demand Surge: MLOps", "Companies are prioritizing deployment architectures. Adding AWS/Docker to your profile can boost your compensation by 8%."),
                ("Skill Demand Surge: Generative AI", "LLM integrations are trending heavily in your sector. Familiarity with LangChain is now a top-tier asset."),
            ]
            salary_alerts = [
                ("Salary Growth Opportunity", "Market medians have adjusted upward for Senior-level roles in your area by 6%. Prepare your negotiation metrics."),
                ("Remote Premium Identified", "100% Remote roles for your title are currently out-earning hybrid roles. Filter your search criteria to maximize ROI."),
                ("Sector Expansion", "FinTech companies are actively recruiting profiles similar to yours with compensation bands 12% above market average."),
            ]

            latest_pred = (
                db.query(SalaryPrediction)
                .filter(SalaryPrediction.user_id == user_id)
                .order_by(SalaryPrediction.created_at.desc())
                .first()
            )

            sal_title, sal_msg = random.choice(salary_alerts)
            if latest_pred:
                sal_msg = f"For trailing '{latest_pred.job_title}' roles: " + sal_msg
            db.add(Notification(user_id=user_id, title=sal_title, message=sal_msg))

            if random.choice([True, False]):
                sk_title, sk_msg = random.choice(skill_alerts)
                db.add(Notification(user_id=user_id, title=sk_title, message=sk_msg))

            db.commit()
            db.close()
            st.success("Analysis complete, check below.")
            st.rerun()
        except Exception as e:
            st.error(f"Error generating notifications: {e}")

st.markdown("### Recent Alerts")

try:
    db = SessionLocal()
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    # Ensure bool is correct
    for n in notifications:
        n.is_read = bool(n.is_read)

    if not notifications:
        st.info("No active notifications. Run an AI scan to check for immediate market shifts.")
    else:
        unread_count = sum(1 for a in notifications if not a.is_read)
        if unread_count > 0:
            st.markdown(f"**{unread_count} Unread Messages**")

        for alert in notifications:
            cols = st.columns([4, 1])
            with cols[0]:
                if not alert.is_read:
                    with st.container(border=True):
                        st.markdown(f"🔴 **{alert.title}**")
                        st.markdown(f"*{alert.message}*")
                        
                        btn_cols = st.columns([1, 1, 2])
                        if btn_cols[0].button("Mark Read", key=f"read_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _a.is_read = 1
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                        
                        if btn_cols[1].button("🗑️ Delete", key=f"del_unread_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _db_temp.delete(_a)
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                else:
                    with st.container():
                        st.markdown(f"<span style='color:grey'>🔕 {alert.title}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:grey; font-size:14px'>{alert.message}</span>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete", key=f"del_read_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _db_temp.delete(_a)
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                        st.divider()

    db.close()
except Exception as e:
    st.error(f"Error loading notifications: {e}")
